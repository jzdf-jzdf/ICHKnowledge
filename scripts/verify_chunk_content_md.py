# -*- coding: utf-8 -*-
"""
verify_chunk_content_md.py
验证每个 chunk 的 content 是否为对应 MD 原文件的精确子串。

清洗规则（与 clean_text.py 一致）：
  1. NFKC 统一全角/半角
  2. 去除引文标记 [数字] 等
  3. 去除杂散 [ ]
  4. 去除所有空白字符
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
MD_DIR = ROOT / "md" / "ICHGuideline"
CHUNKS_DIR = ROOT / "chunks"


def clean_text(s):
    if not s:
        return ""
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\[[\d,\-\sA-Za-z]+\]', '', s)
    s = s.replace('[', '').replace(']', '')
    s = re.sub(r'\s+', '', s)
    return s


def build_chunkdir_to_md():
    """chunk 目录名 → MD 文件路径"""
    mapping = {}
    if MD_DIR.exists():
        for md_file in MD_DIR.glob("*.md"):
            stem = md_file.stem
            for d in CHUNKS_DIR.iterdir():
                if d.is_dir() and d.name.startswith("chunks_"):
                    chunk_dir_name = d.name.replace("chunks_", "", 1)
                    if chunk_dir_name == stem:
                        mapping[chunk_dir_name] = md_file
    return mapping


def main():
    print("=" * 60)
    print("chunk content → MD 原文件 精确子串校验")
    print("=" * 60)

    chunkdir_to_md = build_chunkdir_to_md()
    md_cache = {}

    def get_md_cleaned(md_path):
        key = str(md_path)
        if key not in md_cache:
            with open(md_path, "r", encoding="utf-8") as f:
                md_cache[key] = clean_text(f.read())
        return md_cache[key]

    total = 0
    matched = 0
    unmatched = []
    skipped_dirs = []

    for d in sorted(CHUNKS_DIR.iterdir()):
        if not (d.is_dir() and d.name.startswith("chunks_")):
            continue
        dir_name = d.name.replace("chunks_", "", 1)

        data_file = d / "chunks_data.json"
        if not data_file.exists():
            continue

        md_path = chunkdir_to_md.get(dir_name)
        if not md_path:
            skipped_dirs.append(dir_name)
            continue

        md_cleaned = get_md_cleaned(md_path)
        if md_cleaned is None:
            skipped_dirs.append(dir_name)
            continue

        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        chunks = data.get("chunks", []) if isinstance(data, dict) else data

        dir_total = 0
        dir_matched = 0
        for c in chunks:
            content = c.get("content", "")
            if not content or len(content) < 20:
                continue
            cleaned = clean_text(content)
            if not cleaned:
                continue
            total += 1
            dir_total += 1
            if cleaned in md_cleaned:
                matched += 1
                dir_matched += 1
            else:
                unmatched.append({
                    "dir": dir_name,
                    "chunk_id": c.get("chunk_id", "?"),
                    "type": c.get("type", "?"),
                    "preview": cleaned[:100],
                })

        status = "OK" if dir_total == dir_matched else f"FAIL ({dir_total - dir_matched} unmatched)"
        print(f"  {d.name}: {dir_matched}/{dir_total} {status}")

    if skipped_dirs:
        print(f"\n跳过（无对应 MD 文件）: {len(skipped_dirs)} 个目录")
        for name in skipped_dirs:
            print(f"  {name}")

    print(f"\n{'=' * 60}")
    print(f"总计: {total} 个 chunk")
    print(f"已匹配: {matched}")
    print(f"未匹配: {len(unmatched)}")
    if total > 0:
        print(f"匹配率: {matched / total * 100:.1f}%")

    if unmatched:
        print(f"\n未匹配列表（共 {len(unmatched)} 条）:")
        for item in unmatched:
            print(f"  [{item['dir']}] {item['chunk_id']} ({item['type']})")
            print(f"    {item['preview']}...")


if __name__ == "__main__":
    main()
