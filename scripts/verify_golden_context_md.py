# -*- coding: utf-8 -*-
"""
verify_golden_context_md.py
验证每个子问题的 golden_context 是否为对应 evidence_doc 的 MD 原文件的精确子串。

与 verify_golden_context.py 不同：本脚本直接与 md/ 目录下的原始 Markdown 文件比较，
而非与 chunks 比较。

清洗规则（与 clean_text.py 一致）：
  1. NFKC 统一全角/半角
  2. 去除引文标记 ［数字］ 等
  3. 去除杂散 [ ]
  4. 去除所有空白字符
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

# Windows 控制台 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
MD_DIR = ROOT / "md"
CHUNKS_DIR = ROOT / "chunks"

# ── 单指南文件 → 对应 chunk 目录名（与 verify_golden_context.py 一致） ──
SINGLE_GUIDE_CHUNK_MAP = {
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

# ── 跨指南 short-code → chunk 目录名 → MD 文件 ──
CROSSBOOK_CODE_MAP = {
    "ICH2019": "2019_中国脑出血诊治指南",
    "HICH": "2020_HICH指南",
    "STROKE2024": "2024_中国重症卒中管理指南",
    "PREV2024": "2024_脑血管病防治指南",
}


def clean_text(s):
    """统一清洗文本"""
    if not s:
        return ""
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\[[\d,\-\sA-Za-z]+\]', '', s)
    s = s.replace('[', '').replace(']', '')
    s = re.sub(r'\s+', '', s)
    return s


def build_chunkdir_to_md():
    """从 chunk_summary.json 构建 chunk 目录名 → MD 文件路径 的映射"""
    summary_file = CHUNKS_DIR / "chunk_summary.json"
    mapping = {}
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            summary = json.load(f)
        for entry in summary:
            dir_name = entry.get("dir_name", "")
            md_file = entry.get("file", "")
            if dir_name and md_file:
                mapping[dir_name] = MD_DIR / "ICHGuideline" / md_file
    # 也扫描 ICHBooks 目录
    books_dir = MD_DIR / "ICHBooks"
    if books_dir.exists():
        for md_file in books_dir.glob("*.md"):
            # 尝试匹配 chunks 目录
            stem = md_file.stem
            for d in CHUNKS_DIR.iterdir():
                if d.is_dir() and d.name.startswith("chunks_"):
                    chunk_dir_name = d.name.replace("chunks_", "", 1)
                    if chunk_dir_name == stem:
                        mapping[chunk_dir_name] = md_file
    return mapping


def fuzzy_match_evidence_doc(evidence_doc, chunk_dir_names):
    """将 evidence_doc 模糊匹配到 chunk 目录名"""
    if evidence_doc in chunk_dir_names:
        return evidence_doc
    for dn in chunk_dir_names:
        if evidence_doc in dn or dn in evidence_doc:
            return dn
    # 处理已知拼写变体（如 Angiopathy ↔ Angiopathye）
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


def load_md_cleaned(md_path):
    """加载 MD 文件并返回清洗后的全文字符串"""
    if not md_path.exists():
        return None
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    return clean_text(text)


def main():
    print("=" * 60)
    print("golden_context → MD 原文件 精确子串校验")
    print("=" * 60)

    # 构建 chunk_dir_name → MD 文件路径
    chunkdir_to_md = build_chunkdir_to_md()

    # 缓存已加载的 MD 文件清洗内容
    md_cache = {}

    def get_md_cleaned(md_path):
        key = str(md_path)
        if key not in md_cache:
            md_cache[key] = load_md_cleaned(md_path)
        return md_cache[key]

    total = 0
    matched = 0
    skipped = 0
    unmatched = []

    # ── 1. 单指南文件 ──
    print("\n[单指南文件]")
    for filepath, chunk_dir in SINGLE_GUIDE_CHUNK_MAP.items():
        if not filepath.exists():
            print(f"  跳过（不存在）: {filepath.name}")
            continue
        md_path = chunkdir_to_md.get(chunk_dir)
        if not md_path:
            print(f"  警告：找不到 chunk 目录 {chunk_dir} 对应的 MD 文件")
            continue
        md_cleaned = get_md_cleaned(md_path)
        if md_cleaned is None:
            print(f"  警告：MD 文件不存在 {md_path}")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)
        file_total = 0
        file_matched = 0
        for q in questions:
            ctx = q.get("golden_context", "")
            cleaned_ctx = clean_text(ctx)
            if not cleaned_ctx:
                skipped += 1
                continue
            total += 1
            file_total += 1
            if cleaned_ctx in md_cleaned:
                matched += 1
                file_matched += 1
            else:
                unmatched.append({
                    "file": filepath.name,
                    "id": q.get("id", "?"),
                    "evidence_doc": md_path.stem,
                    "preview": cleaned_ctx[:120],
                })
        print(f"  {filepath.name}: {file_matched}/{file_total} 匹配 (MD: {md_path.name})")

    # ── 2. 跨指南文件 ──
    print("\n[跨指南文件]")
    for filepath in CROSS_GUIDE_FILES:
        if not filepath.exists():
            print(f"  跳过（不存在）: {filepath.name}")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)
        file_total = 0
        file_matched = 0
        for q in questions:
            gc = q.get("golden_context")
            if gc is None:
                skipped += 1
                continue

            # golden_context 是 list[str]（无 evidence_doc）
            if isinstance(gc, list) and len(gc) > 0 and isinstance(gc[0], str):
                for ctx_str in gc:
                    cleaned_ctx = clean_text(ctx_str)
                    if not cleaned_ctx:
                        skipped += 1
                        continue
                    total += 1
                    file_total += 1
                    # 搜索所有 MD 文件
                    found = False
                    for dir_name, md_path in chunkdir_to_md.items():
                        md_cleaned = get_md_cleaned(md_path)
                        if md_cleaned and cleaned_ctx in md_cleaned:
                            found = True
                            break
                    if found:
                        matched += 1
                        file_matched += 1
                    else:
                        unmatched.append({
                            "file": filepath.name,
                            "id": q.get("id", "?"),
                            "evidence_doc": "(全局搜索)",
                            "preview": cleaned_ctx[:120],
                        })

            # golden_context 是 list[{evidence_doc, context}]
            elif isinstance(gc, list):
                for item in gc:
                    if not isinstance(item, dict):
                        continue
                    ctx = item.get("context", "")
                    ed = item.get("evidence_doc", "")
                    cleaned_ctx = clean_text(ctx)
                    if not cleaned_ctx:
                        skipped += 1
                        continue
                    total += 1
                    file_total += 1

                    # 定位 MD 文件
                    md_path = None
                    if ed in CROSSBOOK_CODE_MAP:
                        chunk_dir = CROSSBOOK_CODE_MAP[ed]
                        md_path = chunkdir_to_md.get(chunk_dir)
                    else:
                        # 尝试直接匹配或模糊匹配
                        if ed in chunkdir_to_md:
                            md_path = chunkdir_to_md[ed]
                        else:
                            matched_dir = fuzzy_match_evidence_doc(
                                ed, list(chunkdir_to_md.keys()))
                            if matched_dir:
                                md_path = chunkdir_to_md[matched_dir]

                    if md_path:
                        md_cleaned = get_md_cleaned(md_path)
                        if md_cleaned and cleaned_ctx in md_cleaned:
                            matched += 1
                            file_matched += 1
                        else:
                            unmatched.append({
                                "file": filepath.name,
                                "id": q.get("id", "?"),
                                "evidence_doc": ed,
                                "preview": cleaned_ctx[:120],
                            })
                    else:
                        unmatched.append({
                            "file": filepath.name,
                            "id": q.get("id", "?"),
                            "evidence_doc": f"NO_MD:{ed}",
                            "preview": cleaned_ctx[:120],
                        })

        print(f"  {filepath.name}: {file_matched}/{file_total} 匹配")

    # ── 汇总 ──
    print("\n" + "=" * 60)
    print(f"总计: {total} 个 context（跳过空值: {skipped}）")
    print(f"已匹配: {matched}")
    print(f"未匹配: {len(unmatched)}")
    if total > 0:
        print(f"匹配率: {matched / total * 100:.1f}%")

    if unmatched:
        print(f"\n未匹配列表（共 {len(unmatched)} 条）:")
        for item in unmatched:
            print(f"  [{item['file']}] id={item['id']} "
                  f"evidence_doc={item['evidence_doc']}")
            print(f"    {item['preview']}...")


if __name__ == "__main__":
    main()
