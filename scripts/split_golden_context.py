# -*- coding: utf-8 -*-
"""
split_golden_context.py
自动将共用的多子项推荐意见 golden_context 切分为与题目对应的单子句。
"""

import json, re, unicodedata, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
MD_GUIDELINE = ROOT / "md" / "ICHGuideline"


def clean_text(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\[[\d,\-\sA-Za-z]+\]", "", s)
    s = s.replace("[", "").replace("]", "")
    s = re.sub(r"\s+", "", s)
    return s


def split_clauses(text):
    """将文本按多种编号格式切分为子句，返回 {编号: 文本}
    支持: （N）、(N)、N.、N、 等格式
    """
    # 尝试 （N） 格式
    parts = re.split(r"(?=[（(]\d+[）)])", text)
    clauses = {}
    for p in parts:
        p = p.strip()
        m = re.match(r"[（](\d+)[）)]", p)
        if m:
            clauses[int(m.group(1))] = p
    if len(clauses) >= 2:
        return clauses

    # 尝试 N. 格式（如 1. 2. 3.）
    parts = re.split(r"(?=\b\d+[.、])", text)
    clauses = {}
    for p in parts:
        p = p.strip()
        m = re.match(r"(\d+)[.、]", p)
        if m:
            clauses[int(m.group(1))] = p
    if len(clauses) >= 2:
        return clauses

    # 尝试混合格式：文本中可能有 1.xxx 2.xxx 等
    # 使用更宽松的匹配
    parts = re.split(r"(?=(?:^|\n)\s*\d+[.、])", text, flags=re.MULTILINE)
    clauses = {}
    for p in parts:
        p = p.strip()
        m = re.match(r"(\d+)[.、]", p)
        if m:
            clauses[int(m.group(1))] = p
    return clauses


def split_sentences(text):
    """按中文句号切分（保留句号）"""
    parts = re.split(r"(?<=。)", text)
    return [p.strip() for p in parts if p.strip()]


def keyword_overlap_score(question, candidate):
    q = clean_text(question)
    c = clean_text(candidate)
    if len(q) < 2:
        return 0
    overlap = sum(1 for i in range(len(q) - 1) if q[i : i + 2] in c)
    return overlap / (len(q) - 1)


def best_match(question, candidates):
    scores = [keyword_overlap_score(question, c) for c in candidates]
    return scores.index(max(scores))


def collect_rec_paragraphs(md_text):
    """
    从 MD 全文中收集所有推荐意见段落。
    推荐意见可能有两种格式：
    1. 单行多子句: （1）...（2）...（3）...
    2. 多行单子句: 每个 （N） 占一行，中间有空行
    返回 list of (paragraph_text, clause_dict)
    """
    paragraphs = []
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 检测子句开头（可能有 推荐意见： 前缀）
        if re.search(r"[（(]\d+[）)]", line):
            # 收集连续的子句行（跳过空行）
            clause_lines = [lines[i]]
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if next_line == "":
                    # 空行：检查下一行是否还是子句
                    if j + 1 < len(lines) and re.search(
                        r"[（(]\d+[）)]", lines[j + 1].strip()
                    ):
                        j += 1  # 跳过空行
                        continue
                    else:
                        break
                elif re.search(r"[（(]\d+[）)]", next_line):
                    clause_lines.append(lines[j])
                    j += 1
                else:
                    # 非子句行，可能是子句的续行
                    if not re.match(r"^[#\-]", next_line) and len(next_line) > 5:
                        clause_lines[-1] += next_line
                    j += 1

            full_text = "\n".join(clause_lines)
            clauses = split_clauses(full_text)
            if clauses:
                paragraphs.append((full_text, clauses))
            i = j
        else:
            i += 1

    # 也收集单行多子句的情况（包括有 推荐意见： 前缀的）
    for line in lines:
        line_s = line.strip()
        if re.search(r"[（(]1[）)]", line_s):
            clauses = split_clauses(line_s)
            if len(clauses) >= 2:
                # 检查是否已经收集过
                already = False
                for _, existing_clauses in paragraphs:
                    if 1 in existing_clauses and clean_text(
                        existing_clauses[1]
                    ) == clean_text(clauses.get(1, "")):
                        already = True
                        break
                if not already:
                    paragraphs.append((line_s, clauses))

    return paragraphs


def find_best_paragraph(gc_clean, paragraphs, md_clean):
    """找到与 golden_context 最匹配的段落。
    优先在已收集的推荐意见段落中查找，找不到则在全文中查找。"""
    # 策略1: 在已收集的段落中查找
    best_score = 0
    best_idx = -1
    for i, (_, clauses) in enumerate(paragraphs):
        combined = "".join(clauses.values())
        combined_c = clean_text(combined)
        if not combined_c:
            continue
        for window in [80, 50, 30]:
            chunk = gc_clean[:window]
            if chunk in combined_c:
                if window > best_score:
                    best_score = window
                    best_idx = i
                break
    if best_score > 0:
        return best_idx

    # 策略2: 在全文中查找，然后从已收集的段落中找最近的
    for window in [80, 50, 30, 20]:
        chunk = gc_clean[:window]
        idx = md_clean.find(chunk)
        if idx >= 0:
            # 找到了，检查哪个已收集的段落与之最近
            if paragraphs:
                best_pidx = 0
                best_dist = float("inf")
                for i, (para_text, _) in enumerate(paragraphs):
                    para_c = clean_text(para_text)
                    pidx = md_clean.find(para_c[:30])
                    if pidx >= 0:
                        dist = abs(pidx - idx)
                        if dist < best_dist:
                            best_dist = dist
                            best_pidx = i
                if best_dist < 500:
                    return best_pidx
            break

    return -1


def process_file(qpath, md_path):
    print(f"\n{'='*60}")
    print(f"处理: {qpath.name}")

    with open(qpath, "r", encoding="utf-8") as f:
        questions = json.load(f)
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    md_clean = clean_text(md_text)

    # 收集所有推荐意见段落
    paragraphs = collect_rec_paragraphs(md_text)
    print(f"  MD中找到 {len(paragraphs)} 个推荐意见段落")

    # 找出共用 golden_context 的组
    gc_groups = {}
    for q in questions:
        gc = q.get("golden_context", "")
        if not gc:
            continue
        if gc not in gc_groups:
            gc_groups[gc] = []
        gc_groups[gc].append(q)

    updated = 0
    skipped = 0
    for gc, q_list in gc_groups.items():
        if len(q_list) < 2:
            continue
        has_multi = bool(re.search(r"[（(][2-9][）)]", gc))
        if not has_multi or len(gc) <= 150:
            continue

        gc_clean = clean_text(gc)
        ids = [q["id"] for q in q_list]

        # 找到最匹配的推荐意见段落
        pidx = find_best_paragraph(gc_clean, paragraphs, md_clean)
        if pidx < 0:
            print(f"  跳过 ids={ids}: 无法定位MD原文")
            skipped += 1
            continue

        _, clauses = paragraphs[pidx]
        clause_list = list(clauses.values())
        clause_keys = list(clauses.keys())

        if len(clauses) < 2:
            # 只有1个子句，尝试按句号切分
            sentences = split_sentences(clause_list[0])
            if len(sentences) < 2:
                print(f"  跳过 ids={ids}: 只有1个子句1个句子")
                skipped += 1
                continue
            print(f"  ids={ids} 按句号切分 ({len(sentences)} 句)")
            for q in q_list:
                si = best_match(q["question"], sentences)
                new_gc = sentences[si]
                if clean_text(new_gc) in md_clean:
                    q["golden_context"] = new_gc
                    updated += 1
                    print(f"    id={q['id']}: {new_gc[:70]}...")
                else:
                    # 尝试组合相邻句子
                    combined = "".join(
                        sentences[max(0, si - 1) : si + 2]
                    )
                    if clean_text(combined) in md_clean:
                        q["golden_context"] = combined
                        updated += 1
                        print(f"    id={q['id']}: (组合) {combined[:70]}...")
                    else:
                        print(f"    id={q['id']}: 匹配失败")
        else:
            print(f"  ids={ids} 按子句切分 ({len(clauses)} 个子句)")
            for q in q_list:
                ci = best_match(q["question"], clause_list)
                new_gc = clause_list[ci]
                cid = clause_keys[ci]

                # 子句仍很长时，进一步按句子匹配
                sub_sents = split_sentences(new_gc)
                if len(sub_sents) > 1 and len(new_gc) > 200:
                    si = best_match(q["question"], sub_sents)
                    candidate = sub_sents[si]
                    if clean_text(candidate) in md_clean and len(candidate) > 30:
                        new_gc = candidate

                if clean_text(new_gc) in md_clean:
                    q["golden_context"] = new_gc
                    updated += 1
                    print(
                        f"    id={q['id']}: [子句{cid}] {new_gc[:70]}..."
                    )
                else:
                    print(f"    id={q['id']}: 匹配失败 [子句{cid}]")

    if updated > 0:
        with open(qpath, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f"\n  已更新 {updated} 条, 跳过 {skipped} 组")
    else:
        print(f"\n  无需更新 (跳过 {skipped} 组)")
    return updated


def main():
    FILE_MD_MAP = {
        ROOT / "question" / "HICH" / "HICH_questions.json": MD_GUIDELINE
        / "2020_HICH指南.md",
        ROOT / "question" / "ICH2019" / "ICH2019_questions.json": MD_GUIDELINE
        / "2019_中国脑出血诊治指南.md",
        ROOT
        / "question"
        / "STROKE2024"
        / "stroke2024_questions.json": MD_GUIDELINE
        / "2024_中国重症卒中管理指南.md",
        ROOT
        / "question"
        / "PREV2024"
        / "prev2024_questions.json": MD_GUIDELINE
        / "2024_脑血管病防治指南.md",
    }
    total = 0
    for qpath, md_path in FILE_MD_MAP.items():
        total += process_file(qpath, md_path)
    print(f"\n{'='*60}")
    print(f"总计更新: {total} 条")


if __name__ == "__main__":
    main()
