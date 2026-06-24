"""
clean_text.py
清洗 question 文件中的 golden_context 和 standard_answer。
chunks 源文件不做任何修改。

清洗规则：
  1. NFKC 统一全角/半角
  2. 去除引文标记 ［数字］ ［字母］ 及其变体
  3. 去除杂散的 [ ] 字符
  4. 去除所有空白字符
"""

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent.parent

QUESTION_FILES = [
    ROOT / "question" / "HICH" / "HICH_questions.json",
    ROOT / "question" / "ICH2019" / "ICH2019_questions.json",
    ROOT / "question" / "STROKE2024" / "stroke2024_questions.json",
    ROOT / "question" / "PREV2024" / "prev2024_questions.json",
    ROOT / "question" / "merged" / "crossbook_questions.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集1.json",
    ROOT / "question" / "2026_06_23" / "跨指南题目集2.json",
]


def clean_text(s):
    """统一清洗文本（不修改原始数据，返回新字符串）"""
    if not s:
        return s
    # 1. NFKC 统一全角/半角
    s = unicodedata.normalize('NFKC', s)
    # 2. 去除引文标记
    s = re.sub(r'\[[\d,\-\sA-Za-z]+\]', '', s)
    # 3. 去除杂散的 [ 或 ]
    s = s.replace('[', '').replace(']', '')
    # 4. 去除所有空白字符
    s = re.sub(r'\s+', '', s)
    return s


def clean_question_gc(gc):
    """清洗 golden_context（可能是 str 或 list）"""
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


def clean_all_questions():
    """清洗所有 question 文件的 golden_context 和 standard_answer"""
    count = 0
    for filepath in QUESTION_FILES:
        if not filepath.exists():
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)
        for q in questions:
            if "golden_context" in q:
                q["golden_context"] = clean_question_gc(q["golden_context"])
            if "standard_answer" in q:
                q["standard_answer"] = clean_text(q["standard_answer"])
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        count += 1
    return count


def main():
    print("清洗 question 文件...")
    n_questions = clean_all_questions()
    print(f"  已清洗 {n_questions} 个 question 文件")
    print("\n完成。chunks 源文件未修改。")


if __name__ == "__main__":
    main()
