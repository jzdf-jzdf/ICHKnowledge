# -*- coding: utf-8 -*-
"""
check_guide_names.py
检查跨书题目中是否包含指南名/书名——跨书题最高优先级规则。

从 SKILL.md Step 3.1 内联代码固化为独立脚本。

CLI:
  python check_guide_names.py <questions.json> [--guide-names-file names.txt]

- 内置默认黑名单
- 支持自定义黑名单文件（每行一个名称）
- 违规时 exit(1) 并打印详情，全部通过 exit(0)
"""

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 内置默认黑名单（与 SKILL.md 一致）
DEFAULT_GUIDE_NAMES = [
    "ICH2019", "中国脑出血诊治指南", "脑出血诊治指南",
    "HICH", "高血压性脑出血", "多学科诊治指南",
    "STROKE2024", "重症卒中管理指南", "卒中管理指南",
    "PREV2024", "脑血管病防治指南", "脑血管病防治",
    "ESO指南", "ESO", "AHA/ASA", "AHA", "ASA",
    "各指南", "两本指南", "三本指南", "四本指南",
    "不同指南", "多个指南", "指南之间", "指南推荐",
]


def load_blacklist(filepath=None):
    """加载黑名单。如果提供了文件路径，则从文件加载；否则使用默认列表。"""
    if filepath:
        names = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name and not name.startswith("#"):
                    names.append(name)
        return names
    return DEFAULT_GUIDE_NAMES


def check_questions(questions, blacklist):
    """检查题目中是否包含黑名单词汇，返回违规列表"""
    violations = []
    for q in questions:
        for name in blacklist:
            question_text = q.get("question", "")
            if name in question_text:
                violations.append({
                    "id": q.get("id", "?"),
                    "guide_name": name,
                    "question_preview": question_text[:120],
                })
    return violations


def main():
    if len(sys.argv) < 2:
        print("用法: python check_guide_names.py <questions.json> [--guide-names-file names.txt]")
        print("示例: python check_guide_names.py crossbook_questions.json")
        print("      python check_guide_names.py crossbook_questions.json --guide-names-file extra_names.txt")
        sys.exit(2)

    questions_path = Path(sys.argv[1])
    if not questions_path.exists():
        print(f"错误: 文件不存在: {questions_path}")
        sys.exit(2)

    # 解析 --guide-names-file 参数
    names_file = None
    if len(sys.argv) >= 4 and sys.argv[2] == "--guide-names-file":
        names_file = sys.argv[3]

    # 加载数据
    blacklist = load_blacklist(names_file)
    with open(questions_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    print(f"检查文件: {questions_path.name}")
    print(f"题目总数: {len(questions)}")
    print(f"黑名单条目数: {len(blacklist)}")
    print()

    # 执行检查
    violations = check_questions(questions, blacklist)

    if violations:
        print(f"FAIL: 以下 {len(violations)} 道题目包含指南名：")
        # 按 id 去重（同一题目可能触发多条黑名单）
        seen_ids = set()
        for v in violations:
            if v["id"] not in seen_ids:
                seen_ids.add(v["id"])
                print(f"  Q{v['id']}: 包含 '{v['guide_name']}' -> {v['question_preview']}")
        print()
        print("必须修改上述题目，移除所有指南名引用。")
        sys.exit(1)
    else:
        print(f"PASS: 全部 {len(questions)} 道题目均不含指南名。")
        sys.exit(0)


if __name__ == "__main__":
    main()
