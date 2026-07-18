import json
import os
import glob


def get_failed_ids(review_path: str) -> list:
    """从review文件中获取未通过审核的题目id列表"""
    with open(review_path, "r", encoding="utf-8") as f:
        review_data = json.load(f)
    return [
        item["id"]
        for item in review_data
        if isinstance(item, dict) and not item.get("overall_pass", True)
    ]


def split_questions(question_path: str, failed_ids: list, output_path: str):
    """将未通过的题目从原文件分离到新文件"""
    with open(question_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    failed_questions = [q for q in questions if q["id"] in failed_ids]
    kept_questions = [q for q in questions if q["id"] not in failed_ids]

    if not failed_questions:
        print(f"  无未通过题目，跳过")
        return

    # 写入未通过题目到新文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(failed_questions, f, ensure_ascii=False, indent=2)

    # 覆盖原文件（仅保留通过的题目）
    with open(question_path, "w", encoding="utf-8") as f:
        json.dump(kept_questions, f, ensure_ascii=False, indent=2)

    print(f"  分离 {len(failed_questions)} 道未通过题目 -> {output_path}")
    print(f"  原文件剩余 {len(kept_questions)} 道题目")


def process_all():
    """扫描所有review文件并处理对应题目"""
    base_dir = os.path.join(os.path.dirname(__file__), "..", "question")
    review_files = glob.glob(os.path.join(base_dir, "**", "*_review.json"), recursive=True)

    if not review_files:
        print("未找到 *_review.json 文件")
        return

    for review_path in sorted(review_files):
        # 推导对应的question文件路径：去掉 _review 后缀
        question_path = review_path.replace("_review.json", ".json")
        if not os.path.exists(question_path):
            print(f"[跳过] {os.path.basename(review_path)} -> 对应题目文件不存在: {os.path.basename(question_path)}")
            continue

        # 输出文件名：原文件名_failed.json
        base_name = question_path.replace(".json", "")
        output_path = f"{base_name}_failed.json"

        print(f"[处理] {os.path.basename(review_path)}")
        failed_ids = get_failed_ids(review_path)
        if not failed_ids:
            print(f"  全部通过，无需分离")
            continue

        print(f"  未通过ID: {failed_ids}")
        split_questions(question_path, failed_ids, output_path)


if __name__ == "__main__":
    process_all()
