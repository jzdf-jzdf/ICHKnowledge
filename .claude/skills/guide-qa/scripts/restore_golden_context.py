# -*- coding: utf-8 -*-
"""
restore_golden_context.py
将原始 question 文件的 golden_context 恢复到 questions_with_chunks.json 中。

coverage_match.py 输出的 questions_with_chunks.json 保留了 golden_context 原始格式，
但若在流程中 golden_context 曾被展平或修改，此脚本可按 id 匹配将原文件的 golden_context
复制到目标文件。

从 SKILL.md Step 5 内联代码固化为独立脚本。

CLI:
  python restore_golden_context.py <original_questions.json> <questions_with_chunks.json> [--in-place]

- 默认输出到 stdout（JSON）
- --in-place 直接覆盖 questions_with_chunks.json
- 按 id 匹配，将原文件的 golden_context 复制到目标文件
"""

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def restore_golden_context(original_path, target_path, in_place=False):
    """恢复 golden_context 格式"""
    # 加载原始 question 文件
    with open(original_path, "r", encoding="utf-8") as f:
        original_questions = json.load(f)

    # 加载目标文件（questions_with_chunks.json）
    with open(target_path, "r", encoding="utf-8") as f:
        target_data = json.load(f)

    # 构建 golden_context 映射：id → golden_context
    gc_map = {}
    for q in original_questions:
        gc_map[q["id"]] = q.get("golden_context")

    # 恢复
    restored_count = 0
    for item in target_data:
        item_id = item.get("id")
        if item_id in gc_map:
            item["golden_context"] = gc_map[item_id]
            restored_count += 1

    # 输出
    if in_place:
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(target_data, f, ensure_ascii=False, indent=2)
        print(f"已原地恢复 {restored_count}/{len(target_data)} 道题目的 golden_context -> {target_path}")
        # 检查是否有数组格式的跨书题
        array_count = sum(1 for item in target_data if isinstance(item.get("golden_context"), list))
        if array_count > 0:
            print(f"  其中 {array_count} 道为数组格式（跨书题）")
    else:
        output = json.dumps(target_data, ensure_ascii=False, indent=2)
        print(output)

    return restored_count


def main():
    if len(sys.argv) < 3:
        print("用法: python restore_golden_context.py <original_questions.json> <questions_with_chunks.json> [--in-place]")
        print()
        print("  将 original_questions.json 中的 golden_context 恢复到 questions_with_chunks.json")
        print("  按 id 匹配，保持原始格式（字符串/数组）")
        print()
        print("选项:")
        print("  --in-place  直接覆盖 questions_with_chunks.json（默认输出到 stdout）")
        print()
        print("示例:")
        print("  python restore_golden_context.py crossbook_questions.json questions_with_chunks.json --in-place")
        print("  python restore_golden_context.py crossbook_questions.json questions_with_chunks.json > restored.json")
        sys.exit(2)

    original_path = Path(sys.argv[1])
    target_path = Path(sys.argv[2])
    in_place = "--in-place" in sys.argv

    if not original_path.exists():
        print(f"错误: 原始文件不存在: {original_path}")
        sys.exit(1)
    if not target_path.exists():
        print(f"错误: 目标文件不存在: {target_path}")
        sys.exit(1)

    restore_golden_context(original_path, target_path, in_place=in_place)


if __name__ == "__main__":
    main()
