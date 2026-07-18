# -*- coding: utf-8 -*-
"""
review_questions.py
调用 DeepSeek 大模型对题目质量进行审核检测。

用法：
  # 设置环境变量
  export DEEPSEEK_API_KEY="sk-xxx"

  # 审核单个文件
  python scripts/review_questions.py question/HICH/HICH_questions.json

  # 审核所有文件
  python scripts/review_questions.py --all

  # 指定输出文件
  python scripts/review_questions.py question/HICH/HICH_questions.json -o review_output.json

  # 跳过已审核的题目（断点续传）
  python scripts/review_questions.py question/HICH/HICH_questions.json --resume

审核维度：
  1. 题目清晰度：题干是否明确、无歧义
  2. 上下文相关性：golden_context 是否包含答案
  3. 上下文充分性：golden_context 是否足以回答问题
  4. 上下文精简度：golden_context 是否有冗余内容
  5. 等级匹配度：L1-L4 是否与题目难度匹配
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent

# DeepSeek API 配置
API_BASE = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"

# 所有单指南题目文件
SINGLE_GUIDE_FILES = [
    ROOT / "question" / "HICH" / "HICH_questions.json",
    ROOT / "question" / "ICH2019" / "ICH2019_questions.json",
    ROOT / "question" / "STROKE2024" / "stroke2024_questions.json",
    ROOT / "question" / "PREV2024" / "prev2024_questions.json",
]

CROSS_GUIDE_FILES = [
    ROOT / "question" / "merged" / "crossbook_questions.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集1.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集2.json",
]


REVIEW_PROMPT = """你是一位医学教育专家，负责审核脑出血（ICH）相关题目的质量。

请对以下题目进行审核，从5个维度评估：

## 待审核题目
- 题目ID: {qid}
- 难度等级: {level}
- 题干: {question}
- 参考上下文: {golden_context}

## 审核维度

1. **题目清晰度** (pass/fail)
   - 题干是否表述清晰、无歧义
   - 是否有明确的答案指向
   - 专业术语是否准确

2. **上下文相关性** (pass/fail)
   - golden_context 是否包含该题目的答案
   - 是否有与题目无关的内容

3. **上下文充分性** (pass/fail)
   - golden_context 中的信息是否足以回答该题目
   - 是否缺少关键信息

4. **上下文精简度** (pass/fail)
   - golden_context 是否精炼，无大段冗余
   - 是否包含与题目无关的背景信息

5. **等级匹配度** (pass/fail)
   - L1=事实回忆（直接提取信息）
   - L2=理解推理（列举、比较、因果）
   - L3=跨段综合（分类、归纳、管理）
   - L4=辨析判断（否定辨析、条件判断）
   - 题目实际难度是否与标注等级一致

## 输出格式（严格 JSON）
{{
  "id": {qid},
  "review": {{
    "题目清晰度": {{"pass": true/false, "note": "说明"}},
    "上下文相关性": {{"pass": true/false, "note": "说明"}},
    "上下文充分性": {{"pass": true/false, "note": "说明"}},
    "上下文精简度": {{"pass": true/false, "note": "说明"}},
    "等级匹配度": {{"pass": true/false, "note": "说明"}}
  }},
  "overall_pass": true/false,
  "suggestion": "改进建议（如有）"
}}

请直接输出 JSON，不要输出其他内容。"""


def call_deepseek(prompt, api_key, max_retries=3):
    """调用 DeepSeek API"""
    import urllib.request
    import urllib.error

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一位医学教育和考试题目审核专家。请严格按照要求的JSON格式输出。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 1024,
    }

    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions",
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                # 提取 JSON
                content = content.strip()
                if content.startswith("```"):
                    # 去掉 markdown 代码块
                    lines = content.split("\n")
                    content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
                return json.loads(content)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            print(f"    HTTP {e.code}: {body[:200]}")
            if e.code == 429:
                wait = 2 ** (attempt + 1)
                print(f"    等待 {wait}s 后重试...")
                time.sleep(wait)
            elif e.code >= 500:
                time.sleep(2)
            else:
                return None
        except Exception as e:
            print(f"    错误: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    return None


def review_question(q, api_key):
    """审核单个题目"""
    # 处理 golden_context（可能是 str 或 list）
    gc = q.get("golden_context", "")
    if isinstance(gc, list):
        # 跨指南题目的 golden_context 是 list[{evidence_doc, context}]
        parts = []
        for item in gc:
            if isinstance(item, dict):
                ed = item.get("evidence_doc", "")
                ctx = item.get("context", "")
                parts.append(f"[{ed}] {ctx}")
            elif isinstance(item, str):
                parts.append(item)
        gc_text = "\n".join(parts)
    else:
        gc_text = str(gc)

    # 截断过长的 golden_context
    if len(gc_text) > 2000:
        gc_text = gc_text[:2000] + "...(截断)"

    prompt = REVIEW_PROMPT.format(
        qid=q.get("id", "?"),
        level=q.get("level", "?"),
        question=q.get("question", ""),
        golden_context=gc_text,
    )

    return call_deepseek(prompt, api_key)


def load_existing_reviews(output_path):
    """加载已有的审核结果（用于断点续传）"""
    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {r["id"]: r for r in data}
        except:
            pass
    return {}


def review_file(filepath, api_key, output_path=None, resume=False):
    """审核一个题目文件"""
    print(f"\n{'='*60}")
    print(f"审核: {filepath.name}")
    print(f"{'='*60}")

    with open(filepath, "r", encoding="utf-8") as f:
        questions = json.load(f)

    print(f"题目数: {len(questions)}")

    # 确定输出路径
    if output_path is None:
        output_path = filepath.parent / f"{filepath.stem}_review.json"

    # 加载已有审核结果
    existing = {}
    if resume:
        existing = load_existing_reviews(output_path)
        if existing:
            print(f"已有审核: {len(existing)} 条，跳过已审核题目")

    results = []
    stats = {"total": 0, "passed": 0, "failed": 0, "error": 0}

    for i, q in enumerate(questions):
        qid = q.get("id", i + 1)
        stats["total"] += 1

        # 断点续传：跳过已审核的
        if resume and qid in existing:
            results.append(existing[qid])
            if existing[qid].get("overall_pass", False):
                stats["passed"] += 1
            else:
                stats["failed"] += 1
            continue

        print(f"  [{i+1}/{len(questions)}] Q{qid}: {q.get('question', '')[:50]}...", end=" ")

        result = review_question(q, api_key)
        if result:
            results.append(result)
            if result.get("overall_pass", False):
                stats["passed"] += 1
                print("✓")
            else:
                stats["failed"] += 1
                # 显示失败维度
                fails = [k for k, v in result.get("review", {}).items() if not v.get("pass", True)]
                print(f"✗ ({', '.join(fails)})")
        else:
            stats["error"] += 1
            results.append({"id": qid, "error": "API调用失败", "overall_pass": False})
            print("ERROR")

        # 保存进度（每10题）
        if (i + 1) % 10 == 0:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        # 限速
        time.sleep(0.5)

    # 最终保存
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'─'*40}")
    print(f"审核完成: {filepath.name}")
    print(f"  总计: {stats['total']}")
    print(f"  通过: {stats['passed']}")
    print(f"  失败: {stats['failed']}")
    print(f"  错误: {stats['error']}")
    if stats["total"] > 0:
        print(f"  通过率: {stats['passed']/stats['total']*100:.1f}%")
    print(f"  结果: {output_path}")

    return results, stats


def main():
    parser = argparse.ArgumentParser(description="调用 DeepSeek 审核题目质量")
    parser.add_argument("file", nargs="?", help="题目 JSON 文件路径")
    parser.add_argument("--all", action="store_true", help="审核所有题目文件")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--resume", action="store_true", help="断点续传，跳过已审核题目")
    parser.add_argument("--api-key", help="DeepSeek API Key（也可用 DEEPSEEK_API_KEY 环境变量）")
    parser.add_argument("--model", default="deepseek-chat", help="模型名称（默认 deepseek-chat）")
    parser.add_argument("--base-url", default="https://api.deepseek.com", help="API Base URL")
    args = parser.parse_args()

    global API_BASE, MODEL
    API_BASE = args.base_url
    MODEL = args.model

    # 获取 API Key
    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("错误: 请设置 DEEPSEEK_API_KEY 环境变量或使用 --api-key 参数")
        print("  export DEEPSEEK_API_KEY='sk-xxx'")
        sys.exit(1)

    if args.all:
        # 审核所有文件
        all_files = SINGLE_GUIDE_FILES + CROSS_GUIDE_FILES
        grand_stats = {"total": 0, "passed": 0, "failed": 0, "error": 0}
        for filepath in all_files:
            if not filepath.exists():
                print(f"跳过: {filepath} 不存在")
                continue
            output = filepath.parent / f"{filepath.stem}_review.json"
            _, stats = review_file(filepath, api_key, output, args.resume)
            for k in grand_stats:
                grand_stats[k] += stats[k]

        print(f"\n{'='*60}")
        print(f"全部审核完成")
        print(f"  总计: {grand_stats['total']}")
        print(f"  通过: {grand_stats['passed']}")
        print(f"  失败: {grand_stats['failed']}")
        print(f"  错误: {grand_stats['error']}")
    else:
        if not args.file:
            print("错误: 请指定题目文件路径或使用 --all")
            sys.exit(1)
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"错误: 文件不存在: {filepath}")
            sys.exit(1)
        output = Path(args.output) if args.output else None
        review_file(filepath, api_key, output, args.resume)


if __name__ == "__main__":
    main()
