"""
fix_golden_context.py
修正 golden_context 与原文档 chunks 的一致性。

策略：
  1. 加载 chunks 到内存，对 content 做清洗（不修改源文件）
  2. 加载 questions，对 golden_context 做清洗
  3. 精确子串匹配：cleaned_gc in cleaned_content
  4. 匹配失败则用最佳匹配 chunk 的 cleaned content 替换
  5. 保存 question 文件（chunks 源文件不动）
"""

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent.parent
CHUNKS_DIR = ROOT / "chunks"

# ─── 单指南文件 → 对应 chunk 目录 ───
SINGLE_GUIDE_MAP = {
    ROOT / "question" / "HICH" / "HICH_questions.json": "2020_HICH指南",
    ROOT / "question" / "ICH2019" / "ICH2019_questions.json": "2019_中国脑出血诊治指南",
    ROOT / "question" / "STROKE2024" / "stroke2024_questions.json": "2024_中国重症卒中管理指南",
    ROOT / "question" / "PREV2024" / "prev2024_questions.json": "2024_脑血管病防治指南",
}

# ─── crossbook evidence_doc → chunk 目录（完整名直接映射） ───
CROSSBOOK_CODE_MAP = {
    "2019_中国脑出血诊治指南": "2019_中国脑出血诊治指南",
    "2020_HICH指南": "2020_HICH指南",
    "2024_脑血管病防治指南": "2024_脑血管病防治指南",
    "2024_中国重症卒中管理指南": "2024_中国重症卒中管理指南",
}

# ─── 所有跨指南文件 ───
CROSS_GUIDE_FILES = [
    ROOT / "question" / "merged" / "crossbook_questions.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集_20260623_1.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集_20260623_2.json",
]


# ═══════════════════════════════════════
# 文本清洗（仅在内存中操作）
# ═══════════════════════════════════════

def clean_text(s):
    """统一清洗文本，返回新字符串"""
    if not s:
        return s
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\[[\d,\-\sA-Za-z]+\]', '', s)
    s = s.replace('[', '').replace(']', '')
    s = re.sub(r'\s+', '', s)
    return s


def clean_question_gc(gc):
    """清洗 golden_context（str 或 list）"""
    if isinstance(gc, str):
        return clean_text(gc)
    elif isinstance(gc, list):
        result = []
        for item in gc:
            if isinstance(item, dict):
                new_item = dict(item)
                if "context" in new_item:
                    new_item["context"] = clean_text(new_item["context"])
                result.append(new_item)
            elif isinstance(item, str):
                result.append(clean_text(item))
            else:
                result.append(item)
        return result
    return gc


# ═══════════════════════════════════════
# 加载 chunks（内存清洗，不改源文件）
# ═══════════════════════════════════════

def load_all_chunks():
    """加载所有 chunks，对 content 做内存清洗后返回"""
    all_chunks = {}
    for d in CHUNKS_DIR.iterdir():
        if d.is_dir() and d.name.startswith("chunks_"):
            data_file = d / "chunks_data.json"
            if data_file.exists():
                dir_name = d.name.replace("chunks_", "", 1)
                with open(data_file, "r", encoding="utf-8") as f:
                    chunks = json.load(f)
                # 内存清洗 content，不修改源文件
                for chunk in chunks:
                    if "content" in chunk:
                        chunk["_cleaned_content"] = clean_text(chunk["content"])
                all_chunks[dir_name] = chunks
    return all_chunks


# ═══════════════════════════════════════
# 精确匹配（使用清洗后的文本）
# ═══════════════════════════════════════

def is_exact_match(cleaned_context, cleaned_contents):
    """精确子串匹配：cleaned_context in cleaned_content"""
    if not cleaned_context or not cleaned_context.strip():
        return True
    for content in cleaned_contents:
        if cleaned_context in content:
            return True
    return False


# ═══════════════════════════════════════
# 关键词匹配（用于寻找最佳替换 chunk）
# ═══════════════════════════════════════

def extract_keywords(text, max_keywords=25):
    """提取中文关键词（含子短语）和英文关键词"""
    cn_runs = re.findall(r'[\u4e00-\u9fff]{3,}', text)
    cn_words = []
    for run in cn_runs:
        cn_words.append(run)
        if len(run) > 6:
            for w in [3, 4, 5, 6]:
                for i in range(0, len(run) - w + 1, max(1, w // 2)):
                    cn_words.append(run[i:i + w])
    en_words = re.findall(r'[A-Za-z]{3,}', text)
    seen = set()
    result = []
    for w in cn_words + en_words:
        if w.lower() not in seen:
            seen.add(w.lower())
            result.append(w)
        if len(result) >= max_keywords:
            break
    return result


def find_best_chunk(cleaned_context, chunks):
    """在 chunks 中找到与 cleaned_context 关键词重叠最多的 chunk（使用清洗后的 content）"""
    keywords = extract_keywords(cleaned_context)
    if not keywords:
        return None
    best_chunk = None
    best_score = 0
    for chunk in chunks:
        content = chunk.get("_cleaned_content", "")
        score = sum(1 for kw in keywords if kw in content)
        if score > best_score:
            best_score = score
            best_chunk = chunk
    if best_score >= 1:
        return best_chunk
    return None


# ═══════════════════════════════════════
# evidence_doc → dir_name 模糊映射
# ═══════════════════════════════════════

def fuzzy_match_evidence_doc(evidence_doc, chunk_dir_names):
    """将 evidence_doc 模糊匹配到 chunk 目录名"""
    if evidence_doc in chunk_dir_names:
        return evidence_doc
    for dn in chunk_dir_names:
        if evidence_doc in dn or dn in evidence_doc:
            return dn
    for dn in chunk_dir_names:
        ed_test = evidence_doc.replace("Angiopathy", "Angiopathye")
        if ed_test in dn or dn in ed_test:
            return dn
        dn_test = dn.replace("Angiopathye", "Angiopathy")
        if evidence_doc in dn_test or dn_test in evidence_doc:
            return dn
    def norm(s):
        return re.sub(r'\s+', '', s).lower()
    ed_norm = norm(evidence_doc)
    for dn in chunk_dir_names:
        if ed_norm == norm(dn):
            return dn
    return None


# ═══════════════════════════════════════
# 处理单指南文件
# ═══════════════════════════════════════

def process_single_guide(filepath, dir_name, all_chunks):
    with open(filepath, "r", encoding="utf-8") as f:
        questions = json.load(f)

    chunks = all_chunks.get(dir_name, [])
    if not chunks:
        print(f"  WARNING: 找不到 chunks 目录 {dir_name}")
        return len(questions), 0, 0

    cleaned_contents = [c.get("_cleaned_content", "") for c in chunks]
    total = 0
    fixed = 0
    failed = 0

    for q in questions:
        ctx = q.get("golden_context", "")
        cleaned_ctx = clean_text(ctx)
        if not cleaned_ctx.strip():
            # 同时清洗 standard_answer
            if "standard_answer" in q:
                q["standard_answer"] = clean_text(q["standard_answer"])
            continue
        total += 1

        if is_exact_match(cleaned_ctx, cleaned_contents):
            # 匹配成功，保存清洗后的 golden_context
            q["golden_context"] = cleaned_ctx
        else:
            # 匹配失败，找最佳 chunk 替换
            best = find_best_chunk(cleaned_ctx, chunks)
            if best:
                q["golden_context"] = best["_cleaned_content"]
                fixed += 1
            else:
                # 无法匹配，仍保存清洗后的版本
                q["golden_context"] = cleaned_ctx
                failed += 1
                print(f"    无法匹配 id={q.get('id', '?')}: {cleaned_ctx[:60]}...")

        # 同时清洗 standard_answer
        if "standard_answer" in q:
            q["standard_answer"] = clean_text(q["standard_answer"])

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    return total, fixed, failed


# ═══════════════════════════════════════
# 处理跨指南文件
# ═══════════════════════════════════════

def resolve_evidence_doc_to_dir(evidence_doc, all_chunks):
    if evidence_doc in CROSSBOOK_CODE_MAP:
        return CROSSBOOK_CODE_MAP[evidence_doc]
    return fuzzy_match_evidence_doc(evidence_doc, list(all_chunks.keys()))


def process_cross_guide(filepath, all_chunks):
    with open(filepath, "r", encoding="utf-8") as f:
        questions = json.load(f)

    total = 0
    fixed = 0
    failed = 0

    for q in questions:
        gc = q.get("golden_context")
        if gc is None:
            if "standard_answer" in q:
                q["standard_answer"] = clean_text(q["standard_answer"])
            continue

        # 特殊格式：golden_context 是 list[str]
        if isinstance(gc, list) and len(gc) > 0 and isinstance(gc[0], str):
            new_gc = []
            for ctx_str in gc:
                cleaned_ctx = clean_text(ctx_str)
                total += 1
                if not cleaned_ctx.strip():
                    new_gc.append(cleaned_ctx)
                    continue
                # 在所有 chunks 中精确匹配
                matched = False
                for dir_name, chunks in all_chunks.items():
                    cleaned_contents = [c.get("_cleaned_content", "") for c in chunks]
                    if is_exact_match(cleaned_ctx, cleaned_contents):
                        matched = True
                        break
                if matched:
                    new_gc.append(cleaned_ctx)
                else:
                    # 找最佳替换
                    best = None
                    best_score = 0
                    for dir_name, chunks in all_chunks.items():
                        candidate = find_best_chunk(cleaned_ctx, chunks)
                        if candidate:
                            keywords = extract_keywords(cleaned_ctx)
                            score = sum(1 for kw in keywords if kw in candidate.get("_cleaned_content", ""))
                            if score > best_score:
                                best_score = score
                                best = candidate
                    if best:
                        new_gc.append(best["_cleaned_content"])
                        fixed += 1
                    else:
                        new_gc.append(cleaned_ctx)
                        failed += 1
                        print(f"    无法匹配 id={q.get('id','?')}: {cleaned_ctx[:60]}...")
            q["golden_context"] = new_gc
            if "standard_answer" in q:
                q["standard_answer"] = clean_text(q["standard_answer"])
            continue

        # 标准格式：golden_context 是 list[{evidence_doc, context}]
        if isinstance(gc, list):
            for item in gc:
                if not isinstance(item, dict):
                    continue
                ctx = item.get("context", "")
                ed = item.get("evidence_doc", "")
                cleaned_ctx = clean_text(ctx)
                if not cleaned_ctx.strip():
                    continue
                total += 1

                dir_name = resolve_evidence_doc_to_dir(ed, all_chunks)
                if dir_name is None:
                    print(f"    无法映射 evidence_doc={ed}")
                    failed += 1
                    continue

                chunks = all_chunks.get(dir_name, [])
                if not chunks:
                    print(f"    找不到 chunks: {dir_name}")
                    failed += 1
                    continue

                cleaned_contents = [c.get("_cleaned_content", "") for c in chunks]

                if is_exact_match(cleaned_ctx, cleaned_contents):
                    item["context"] = cleaned_ctx
                else:
                    best = find_best_chunk(cleaned_ctx, chunks)
                    if best:
                        item["context"] = best["_cleaned_content"]
                        fixed += 1
                    else:
                        item["context"] = cleaned_ctx
                        failed += 1
                        print(f"    无法匹配 id={q.get('id','?')} ed={ed}: {cleaned_ctx[:60]}...")

        # 单指南格式（string）
        elif isinstance(gc, str):
            cleaned_gc = clean_text(gc)
            total += 1
            if cleaned_gc.strip():
                matched = False
                for dir_name, chunks in all_chunks.items():
                    cleaned_contents = [c.get("_cleaned_content", "") for c in chunks]
                    if is_exact_match(cleaned_gc, cleaned_contents):
                        matched = True
                        break
                if matched:
                    q["golden_context"] = cleaned_gc
                else:
                    best = None
                    best_score = 0
                    for dir_name, chunks in all_chunks.items():
                        candidate = find_best_chunk(cleaned_gc, chunks)
                        if candidate:
                            keywords = extract_keywords(cleaned_gc)
                            score = sum(1 for kw in keywords if kw in candidate.get("_cleaned_content", ""))
                            if score > best_score:
                                best_score = score
                                best = candidate
                    if best:
                        q["golden_context"] = best["_cleaned_content"]
                        fixed += 1
                    else:
                        q["golden_context"] = cleaned_gc
                        failed += 1

        if "standard_answer" in q:
            q["standard_answer"] = clean_text(q["standard_answer"])

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    return total, fixed, failed


# ═══════════════════════════════════════
# 主流程
# ═══════════════════════════════════════

def main():
    print("加载 chunks（内存清洗，不修改源文件）...")
    all_chunks = load_all_chunks()
    print(f"  已加载 {len(all_chunks)} 个指南的 chunks")

    grand_total = 0
    grand_fixed = 0
    grand_failed = 0

    # 单指南文件
    print("\n=== 单指南文件 ===")
    for filepath, dir_name in SINGLE_GUIDE_MAP.items():
        if not filepath.exists():
            print(f"  SKIP: {filepath} 不存在")
            continue
        print(f"\n处理: {filepath.name} → {dir_name}")
        total, fixed, failed = process_single_guide(filepath, dir_name, all_chunks)
        print(f"  总计 {total} 题, 修复 {fixed} 题, 失败 {failed} 题")
        grand_total += total
        grand_fixed += fixed
        grand_failed += failed

    # 跨指南文件
    print("\n=== 跨指南文件 ===")
    for filepath in CROSS_GUIDE_FILES:
        if not filepath.exists():
            print(f"  SKIP: {filepath} 不存在")
            continue
        print(f"\n处理: {filepath.name}")
        total, fixed, failed = process_cross_guide(filepath, all_chunks)
        print(f"  总计 {total} 题, 修复 {fixed} 题, 失败 {failed} 题")
        grand_total += total
        grand_fixed += fixed
        grand_failed += failed

    print(f"\n{'='*50}")
    print(f"总计: {grand_total} 个 context, 修复 {grand_fixed}, 失败 {grand_failed}")
    if grand_total > 0:
        print(f"修复率: {grand_fixed/grand_total*100:.1f}%")
    print("\nchunks 源文件未修改。")


if __name__ == "__main__":
    main()
