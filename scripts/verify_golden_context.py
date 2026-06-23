"""
verify_golden_context.py
验证 golden_context 是否为 chunk content 的精确子串。

使用内存清洗：加载 chunks 和 questions 后，对两者做相同清洗，
再验证 cleaned_gc in cleaned_content。
chunks 源文件不做任何修改。
"""

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent.parent
CHUNKS_DIR = ROOT / "chunks"

# 单指南文件 → 对应 chunk 目录
SINGLE_GUIDE_MAP = {
    ROOT / "question" / "HICH" / "HICH_questions.json": "2020_HICH指南",
    ROOT / "question" / "ICH2019" / "ICH2019_questions.json": "2019_中国脑出血诊治指南",
    ROOT / "question" / "STROKE2024" / "stroke2024_questions.json": "2024_中国重症卒中管理指南",
    ROOT / "question" / "PREV2024" / "prev2024_questions.json": "2024_脑血管病防治指南",
}

CROSS_GUIDE_FILES = [
    ROOT / "question" / "merged" / "crossbook_questions.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集_20260623_1.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集_20260623_2.json",
]

CROSSBOOK_CODE_MAP = {
    "2019_中国脑出血诊治指南": "2019_中国脑出血诊治指南",
    "2020_HICH指南": "2020_HICH指南",
    "2024_脑血管病防治指南": "2024_脑血管病防治指南",
    "2024_中国重症卒中管理指南": "2024_中国重症卒中管理指南",
}


def clean_text(s):
    """统一清洗文本"""
    if not s:
        return s
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\[[\d,\-\sA-Za-z]+\]', '', s)
    s = s.replace('[', '').replace(']', '')
    s = re.sub(r'\s+', '', s)
    return s


def load_all_chunks():
    """加载所有 chunks，内存清洗 content（不修改源文件）"""
    all_chunks = {}
    for d in CHUNKS_DIR.iterdir():
        if d.is_dir() and d.name.startswith("chunks_"):
            data_file = d / "chunks_data.json"
            if data_file.exists():
                dir_name = d.name.replace("chunks_", "", 1)
                with open(data_file, "r", encoding="utf-8") as f:
                    chunks = json.load(f)
                for chunk in chunks:
                    if "content" in chunk:
                        chunk["_cleaned"] = clean_text(chunk["content"])
                all_chunks[dir_name] = chunks
    return all_chunks


def is_exact_match(cleaned_context, cleaned_contents):
    """精确子串匹配"""
    if not cleaned_context or not cleaned_context.strip():
        return True
    for content in cleaned_contents:
        if cleaned_context in content:
            return True
    return False


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


def clean_gc(gc):
    """清洗 golden_context"""
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


def main():
    print("加载 chunks（内存清洗）...")
    all_chunks = load_all_chunks()
    print(f"  已加载 {len(all_chunks)} 个指南的 chunks")

    total = 0
    matched = 0
    unmatched = []

    # 单指南文件
    for filepath, dir_name in SINGLE_GUIDE_MAP.items():
        if not filepath.exists():
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)
        chunks = all_chunks.get(dir_name, [])
        cleaned_contents = [c.get("_cleaned", "") for c in chunks]
        for q in questions:
            ctx = q.get("golden_context", "")
            cleaned_ctx = clean_text(ctx)
            if not cleaned_ctx.strip():
                continue
            total += 1
            if is_exact_match(cleaned_ctx, cleaned_contents):
                matched += 1
            else:
                unmatched.append((str(filepath.name), q.get("id", "?"), cleaned_ctx[:100]))

    # 跨指南文件
    for filepath in CROSS_GUIDE_FILES:
        if not filepath.exists():
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)
        for q in questions:
            gc = q.get("golden_context")
            if gc is None:
                continue
            # 特殊格式：golden_context 是 list[str]
            if isinstance(gc, list) and len(gc) > 0 and isinstance(gc[0], str):
                for ctx_str in gc:
                    cleaned_ctx = clean_text(ctx_str)
                    total += 1
                    found = False
                    for dir_name, chunks in all_chunks.items():
                        cleaned_contents = [c.get("_cleaned", "") for c in chunks]
                        if is_exact_match(cleaned_ctx, cleaned_contents):
                            found = True
                            break
                    if found:
                        matched += 1
                    else:
                        unmatched.append((str(filepath.name), q.get("id", "?"), cleaned_ctx[:100]))
            # 标准格式：golden_context 是 list[{evidence_doc, context}]
            elif isinstance(gc, list):
                for item in gc:
                    if not isinstance(item, dict):
                        continue
                    ctx = item.get("context", "")
                    ed = item.get("evidence_doc", "")
                    cleaned_ctx = clean_text(ctx)
                    if not cleaned_ctx.strip():
                        continue
                    total += 1
                    dir_name = None
                    if ed in CROSSBOOK_CODE_MAP:
                        dir_name = CROSSBOOK_CODE_MAP[ed]
                    else:
                        dir_name = fuzzy_match_evidence_doc(ed, list(all_chunks.keys()))
                    if dir_name and dir_name in all_chunks:
                        cleaned_contents = [c.get("_cleaned", "") for c in all_chunks[dir_name]]
                        if is_exact_match(cleaned_ctx, cleaned_contents):
                            matched += 1
                        else:
                            unmatched.append((str(filepath.name), q.get("id", "?"), f"[{ed}] {cleaned_ctx[:80]}"))
                    else:
                        unmatched.append((str(filepath.name), q.get("id", "?"), f"[NO_DIR:{ed}] {cleaned_ctx[:80]}"))

    print(f"\n总计: {total} 个 context")
    print(f"已匹配: {matched}")
    print(f"未匹配: {len(unmatched)}")
    if total > 0:
        print(f"匹配率: {matched/total*100:.1f}%")

    if unmatched:
        print(f"\n未匹配列表:")
        for fname, qid, ctx_preview in unmatched:
            print(f"  {fname} id={qid}: {ctx_preview}...")


if __name__ == "__main__":
    main()
