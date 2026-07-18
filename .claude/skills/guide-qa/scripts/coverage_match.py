# -*- coding: utf-8 -*-
"""
coverage_match.py
将题目的 golden_context 与 chunks.jsonl 匹配，输出覆盖率报告和增强的题目文件。

匹配算法：
  复用 clean_text() 清洗逻辑（NFKC → 去引文标记 → 去方括号 → 去空白）
  对每个 question，清洗其 golden_context 后在所有 chunk.content 中做子串查找
  找到则记录 matched_chunk_id、matched_guide、match_score（清洗后重叠率）

跨书题数组格式保持：
  - 输入检测：如果 golden_context 是 list，则逐个 element 的 context 分别匹配
  - 输出时 golden_context 保持原始格式（数组/字符串），不展平
  - 在 questions_with_chunks.json 中记录每个 question 的 matched_chunks 列表及来源

CLI:
  python coverage_match.py <chunks.jsonl> <questions.json> <output_dir>

输出文件：
  - coverage_report.txt  — 可读摘要
  - coverage_report.json — 结构化数据
  - questions_with_chunks.json — 每个 question 附加 matched_chunks 字段
"""

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def clean_text(s):
    """统一清洗文本：NFKC → 去引文标记 → 去方括号 → 去空白"""
    if not s:
        return ""
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\[[\d,\-\sA-Za-z]+\]', '', s)
    s = s.replace('[', '').replace(']', '')
    s = re.sub(r'\s+', '', s)
    return s


def load_chunks(chunks_path):
    """加载 chunks.jsonl，返回 list[dict]"""
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def load_questions(questions_path):
    """加载 questions.json，返回 list[dict]"""
    with open(questions_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_cleaned_chunks(chunks):
    """为每个 chunk 预计算 cleaned_content"""
    for c in chunks:
        c["_cleaned_content"] = clean_text(c.get("content", ""))
    return chunks


def match_context(cleaned_ctx, chunks):
    """在 chunks 中查找 cleaned_ctx 的匹配，返回最优匹配信息或 None"""
    if not cleaned_ctx:
        return None

    best = None
    best_score = 0

    for c in chunks:
        cleaned_content = c.get("_cleaned_content", "")
        if not cleaned_content:
            continue

        # 子串匹配
        if cleaned_ctx in cleaned_content:
            score = len(cleaned_ctx) / len(cleaned_content) if cleaned_content else 0
        elif cleaned_content in cleaned_ctx:
            score = len(cleaned_content) / len(cleaned_ctx) if cleaned_ctx else 0
        else:
            continue

        if score > best_score:
            best_score = score
            best = {
                "chunk_id": c.get("chunk_id"),
                "guide": c.get("guide"),
                "section": c.get("section"),
                "type": c.get("type"),
                "match_score": round(score, 4),
            }

    return best


def match_questions(questions, chunks):
    """为每个 question 匹配 golden_context 到 chunks"""
    results = []

    for q in questions:
        gc = q.get("golden_context")
        matched_chunks = []

        if gc is None:
            pass  # no golden_context
        elif isinstance(gc, list):
            # 跨书题：逐个 element 匹配
            for item in gc:
                if isinstance(item, dict):
                    ctx = item.get("context", "")
                    ed = item.get("evidence_doc", "")
                    cleaned_ctx = clean_text(ctx)
                    match = match_context(cleaned_ctx, chunks)
                    if match:
                        match["evidence_doc"] = ed
                        matched_chunks.append(match)
        elif isinstance(gc, str):
            # 单书题：直接匹配
            cleaned_ctx = clean_text(gc)
            match = match_context(cleaned_ctx, chunks)
            if match:
                matched_chunks.append(match)

        # 构建输出
        result = dict(q)
        result["matched_chunks"] = matched_chunks
        results.append(result)

    return results


def generate_coverage_report(chunks, results, output_dir):
    """生成覆盖率报告"""
    total_chunks = len(chunks)
    matched_chunk_ids = set()
    for r in results:
        for mc in r.get("matched_chunks", []):
            if mc.get("chunk_id"):
                matched_chunk_ids.add(mc["chunk_id"])

    matched_count = len(matched_chunk_ids)
    coverage_pct = (matched_count / total_chunks * 100) if total_chunks > 0 else 0

    # 按 section 分布
    section_stats = defaultdict(lambda: {"total": 0, "matched": 0})
    for c in chunks:
        sec = c.get("section", "Unknown")
        section_stats[sec]["total"] += 1
        if c.get("chunk_id") in matched_chunk_ids:
            section_stats[sec]["matched"] += 1

    # 按 type 分布
    type_stats = defaultdict(lambda: {"total": 0, "matched": 0})
    for c in chunks:
        tp = c.get("type", "Unknown")
        type_stats[tp]["total"] += 1
        if c.get("chunk_id") in matched_chunk_ids:
            type_stats[tp]["matched"] += 1

    # 未覆盖列表
    uncovered = []
    for c in chunks:
        if c.get("chunk_id") not in matched_chunk_ids:
            uncovered.append({
                "chunk_id": c.get("chunk_id"),
                "guide": c.get("guide"),
                "section": c.get("section"),
                "type": c.get("type"),
                "summary": c.get("summary", "")[:100],
            })

    # 按 guide 分布
    guide_stats = defaultdict(lambda: {"total": 0, "matched": 0})
    for c in chunks:
        g = c.get("guide", "Unknown")
        guide_stats[g]["total"] += 1
        if c.get("chunk_id") in matched_chunk_ids:
            guide_stats[g]["matched"] += 1

    report = {
        "total_chunks": total_chunks,
        "matched_chunks": matched_count,
        "unmatched_chunks": total_chunks - matched_count,
        "coverage_pct": round(coverage_pct, 1),
        "by_section": {k: dict(v) for k, v in sorted(section_stats.items())},
        "by_type": {k: dict(v) for k, v in sorted(type_stats.items())},
        "by_guide": {k: dict(v) for k, v in sorted(guide_stats.items())},
        "uncovered": uncovered,
    }

    return report


def write_txt_report(report, output_path):
    """写入可读文本报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("chunks 覆盖率报告")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"总 chunks 数: {report['total_chunks']}")
    lines.append(f"已覆盖: {report['matched_chunks']}")
    lines.append(f"未覆盖: {report['unmatched_chunks']}")
    lines.append(f"覆盖率: {report['coverage_pct']}%")
    lines.append("")

    # 按 guide
    if report.get("by_guide"):
        lines.append("── 按指南分布 ──")
        for guide, stats in report["by_guide"].items():
            pct = (stats["matched"] / stats["total"] * 100) if stats["total"] > 0 else 0
            lines.append(f"  {guide}: {stats['matched']}/{stats['total']} ({pct:.1f}%)")
        lines.append("")

    # 按 type
    if report.get("by_type"):
        lines.append("── 按类型分布 ──")
        for tp, stats in report["by_type"].items():
            pct = (stats["matched"] / stats["total"] * 100) if stats["total"] > 0 else 0
            lines.append(f"  {tp}: {stats['matched']}/{stats['total']} ({pct:.1f}%)")
        lines.append("")

    # 按 section
    if report.get("by_section"):
        lines.append("── 按 section 分布 ──")
        for sec, stats in report["by_section"].items():
            pct = (stats["matched"] / stats["total"] * 100) if stats["total"] > 0 else 0
            lines.append(f"  {sec}: {stats['matched']}/{stats['total']} ({pct:.1f}%)")
        lines.append("")

    # 未覆盖列表
    if report.get("uncovered"):
        lines.append(f"── 未覆盖 chunks（共 {len(report['uncovered'])} 条）──")
        for uc in report["uncovered"]:
            lines.append(f"  [{uc['type']}] {uc['chunk_id']} ({uc.get('guide', '')})")
            lines.append(f"    {uc.get('section', '')}")
            lines.append(f"    {uc.get('summary', '')}")
        lines.append("")

    lines.append("=" * 60)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    if len(sys.argv) < 4:
        print("用法: python coverage_match.py <chunks.jsonl> <questions.json> <output_dir>")
        print("示例: python coverage_match.py chunks_ICH2019/chunks.jsonl ICH2019_questions.json chunks_ICH2019/")
        sys.exit(1)

    chunks_path = Path(sys.argv[1])
    questions_path = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])

    if not chunks_path.exists():
        print(f"错误: chunks 文件不存在: {chunks_path}")
        sys.exit(1)
    if not questions_path.exists():
        print(f"错误: questions 文件不存在: {questions_path}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"加载 chunks: {chunks_path}")
    chunks = load_chunks(chunks_path)
    print(f"  共 {len(chunks)} 条 chunks")

    print(f"加载 questions: {questions_path}")
    questions = load_questions(questions_path)
    print(f"  共 {len(questions)} 道题目")

    print("预计算 cleaned_content...")
    chunks = build_cleaned_chunks(chunks)

    print("匹配 golden_context → chunks...")
    results = match_questions(questions, chunks)

    # 统计
    total_q = len(results)
    matched_q = sum(1 for r in results if r.get("matched_chunks"))
    unmatched_q = total_q - matched_q
    print(f"  题目匹配: {matched_q}/{total_q} ({matched_q / total_q * 100:.1f}%)" if total_q else "  无题目")

    # 生成覆盖率报告
    print("生成覆盖率报告...")
    report = generate_coverage_report(chunks, results, output_dir)

    txt_path = output_dir / "coverage_report.txt"
    write_txt_report(report, txt_path)
    print(f"  -> {txt_path}")

    json_path = output_dir / "coverage_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  -> {json_path}")

    # 输出 questions_with_chunks.json
    qc_path = output_dir / "questions_with_chunks.json"
    with open(qc_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  -> {qc_path}")

    # 摘要
    print()
    print("=" * 60)
    print(f"总 chunks: {report['total_chunks']}")
    print(f"已覆盖: {report['matched_chunks']} ({report['coverage_pct']}%)")
    print(f"未覆盖: {report['unmatched_chunks']}")
    print(f"题目匹配: {matched_q}/{total_q}")
    if unmatched_q > 0:
        print(f"  未匹配题目 id: {[r['id'] for r in results if not r.get('matched_chunks')]}")
    print("=" * 60)


if __name__ == "__main__":
    main()
