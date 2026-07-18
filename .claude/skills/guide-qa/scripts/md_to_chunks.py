# -*- coding: utf-8 -*-
"""
md_to_chunks.py
将 chunks_data.json 转换为标准 chunks 输出，或合并多个 chunks 目录。

模式一：生成（默认）
  输入: chunks_data.json（含 guide, sections, chunks）
  输出: chunks.jsonl, sections.json, mapping.csv

模式二：合并
  输入: 多个 chunks 目录
  输出: 合并后的 chunks.jsonl, sections.json, mapping.csv

CLI:
  # 生成模式
  python md_to_chunks.py chunks_data.json chunks_<prefix>/

  # 合并模式
  python md_to_chunks.py merge <dir1> <dir2> ... -o chunks_merged/
"""

import csv
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


# ───────────────────── 生成模式 ─────────────────────

def generate_output(data, output_dir):
    """将 chunks_data.json 的内容写入标准输出文件"""
    guide = data.get("guide", "")
    sections = data.get("sections", [])
    chunks = data.get("chunks", [])

    # 构建 section_id → title 映射
    section_map = {s["section_id"]: s["title"] for s in sections}

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 写入 sections.json
    sections_path = output_dir / "sections.json"
    with open(sections_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)
    print(f"  -> {sections_path} ({len(sections)} sections)")

    # 2. 写入 chunks.jsonl
    chunks_path = output_dir / "chunks.jsonl"
    chunk_count = 0
    with open(chunks_path, "w", encoding="utf-8") as f:
        for c in chunks:
            line = dict(c)
            # 添加 guide 字段
            line["guide"] = guide
            # 将 section ID 解析为标题
            sec_id = c.get("section", "")
            if sec_id in section_map:
                line["section"] = section_map[sec_id]
            json.dump(line, f, ensure_ascii=False)
            f.write("\n")
            chunk_count += 1
    print(f"  -> {chunks_path} ({chunk_count} chunks)")

    # 3. 写入 mapping.csv
    mapping_path = output_dir / "mapping.csv"
    with open(mapping_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["chunk_id", "section_id", "type", "topic_tags",
                         "summary", "已出题", "题目数量", "题目IDs", "题目等级分布"])
        for c in chunks:
            section_title = section_map.get(c.get("section", ""), c.get("section", ""))
            writer.writerow([
                c.get("chunk_id", ""),
                section_title,
                c.get("type", ""),
                "|".join(c.get("topic_tags", [])),
                c.get("summary", ""),
                0,  # 已出题
                0,  # 题目数量
                "",  # 题目IDs
                "",  # 题目等级分布
            ])
    print(f"  -> {mapping_path}")

    return chunk_count, len(sections)


# ───────────────────── 合并模式 ─────────────────────

def merge_directories(input_dirs, output_dir):
    """合并多个 chunks 目录到统一输出目录"""
    all_chunks = []
    all_sections = []
    section_id_offset = 0
    chunk_ids_seen = set()
    guides_summary = {}

    for dir_path in input_dirs:
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            print(f"  警告: 目录不存在，跳过: {dir_path}")
            continue

        # 读取 chunks.jsonl
        chunks_file = dir_path / "chunks.jsonl"
        if not chunks_file.exists():
            print(f"  警告: 无 chunks.jsonl，跳过: {dir_path}")
            continue

        chunks_in_dir = 0
        with open(chunks_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                chunk = json.loads(line)
                chunk_id = chunk.get("chunk_id", "")
                if chunk_id in chunk_ids_seen:
                    print(f"  警告: 重复 chunk_id '{chunk_id}'，跳过")
                    continue
                chunk_ids_seen.add(chunk_id)
                all_chunks.append(chunk)
                chunks_in_dir += 1

        # 读取 sections.json
        sections_file = dir_path / "sections.json"
        if sections_file.exists():
            with open(sections_file, "r", encoding="utf-8") as f:
                sections_in_dir = json.load(f)
            # 重新索引 section_id 避免冲突 (S001 -> S001, S001 in dir2 -> S022 etc.)
            remap = {}
            for s in sections_in_dir:
                old_id = s["section_id"]
                new_id = f"S{section_id_offset + 1:03d}"
                remap[old_id] = new_id
                s["section_id"] = new_id
                section_id_offset += 1
            all_sections.extend(sections_in_dir)
            # 更新 chunks 中的 section 引用 (这些 chunk 已经添加，需要回退重做)
            # 简便处理: 不重映射，因为合并模式下 section 字段是标题文本而非 ID

        guide_name = dir_path.name.replace("chunks_", "", 1) if dir_path.name.startswith("chunks_") else dir_path.name
        guides_summary[guide_name] = chunks_in_dir
        print(f"  {dir_path.name}: {chunks_in_dir} chunks, {len(sections_in_dir) if sections_file.exists() else 0} sections")

    # 写入合并输出
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # chunks.jsonl
    chunks_out = output_dir / "chunks.jsonl"
    with open(chunks_out, "w", encoding="utf-8") as f:
        for c in all_chunks:
            json.dump(c, f, ensure_ascii=False)
            f.write("\n")
    print(f"  -> {chunks_out} ({len(all_chunks)} chunks total)")

    # sections.json
    sections_out = output_dir / "sections.json"
    with open(sections_out, "w", encoding="utf-8") as f:
        json.dump(all_sections, f, ensure_ascii=False, indent=2)
    print(f"  -> {sections_out} ({len(all_sections)} sections total)")

    # mapping.csv
    mapping_out = output_dir / "mapping.csv"
    with open(mapping_out, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["chunk_id", "section_id", "type", "topic_tags",
                         "summary", "已出题", "题目数量", "题目IDs", "题目等级分布"])
        for c in all_chunks:
            writer.writerow([
                c.get("chunk_id", ""),
                c.get("section", ""),
                c.get("type", ""),
                "|".join(c.get("topic_tags", [])),
                c.get("summary", ""),
                0, 0, "", "",
            ])
    print(f"  -> {mapping_out}")

    # 打印摘要
    print()
    print("合并摘要:")
    for guide, count in guides_summary.items():
        print(f"  {guide}: {count} chunks")
    print(f"  总计: {len(all_chunks)} chunks, {len(all_sections)} sections")

    return len(all_chunks), len(all_sections)


# ───────────────────── 主入口 ─────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  生成模式: python md_to_chunks.py <chunks_data.json> <output_dir>")
        print("  合并模式: python md_to_chunks.py merge <dir1> <dir2> ... -o <output_dir>")
        print()
        print("示例:")
        print("  python md_to_chunks.py chunks_data.json chunks_ICH2019/")
        print("  python md_to_chunks.py merge chunks_ICH2019/ chunks_HICH/ -o chunks_merged/")
        sys.exit(2)

    if sys.argv[1] == "merge":
        # 合并模式
        args = sys.argv[2:]
        output_dir = None
        input_dirs = []

        i = 0
        while i < len(args):
            if args[i] == "-o":
                if i + 1 < len(args):
                    output_dir = args[i + 1]
                    i += 2
                else:
                    print("错误: -o 需要指定输出目录")
                    sys.exit(2)
            else:
                input_dirs.append(args[i])
                i += 1

        if not input_dirs:
            print("错误: 至少需要指定一个输入目录")
            sys.exit(2)
        if not output_dir:
            output_dir = "chunks_merged/"

        print("合并模式")
        print(f"  输入目录: {', '.join(input_dirs)}")
        print(f"  输出目录: {output_dir}")
        print()

        merge_directories(input_dirs, output_dir)
    else:
        # 生成模式
        if len(sys.argv) < 3:
            print("错误: 生成模式需要 <chunks_data.json> <output_dir>")
            sys.exit(2)

        data_path = Path(sys.argv[1])
        output_dir = sys.argv[2]

        if not data_path.exists():
            print(f"错误: 文件不存在: {data_path}")
            sys.exit(1)

        print("生成模式")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        guide = data.get("guide", "Unknown")
        chunks_count = len(data.get("chunks", []))
        sections_count = len(data.get("sections", []))

        print(f"  指南: {guide}")
        print(f"  chunks: {chunks_count}")
        print(f"  sections: {sections_count}")
        print(f"  输出目录: {output_dir}")
        print()

        generate_output(data, output_dir)

        print()
        print(f"完成。输出到 {output_dir}/")


if __name__ == "__main__":
    main()
