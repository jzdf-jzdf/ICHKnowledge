# -*- coding: utf-8 -*-
"""
fix_hich_concise_v2.py
精确修复 HICH golden_context：从指定 chunk 中提取特定句子。
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
QUESTION_FILE = ROOT / "question" / "HICH" / "HICH_questions.json"
REVIEW_FILE = ROOT / "question" / "HICH" / "context_review.json"
CHUNKS_FILE = ROOT / "chunks" / "chunks_2020_高血压性脑出血中国多学科诊治指南" / "chunks_data.json"


def clean_text(s):
    if not s:
        return s
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\[[\d,\-\sA-Za-z]+]', '', s)
    s = s.replace('[', '').replace(']', '')
    s = re.sub(r'\s+', '', s)
    return s


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("chunks", [])


def extract_by_keywords(chunk_content, keywords, max_chars=300):
    """从 chunk 中提取包含关键词的连续子串，总长度不超过 max_chars"""
    # 按句号分句，记录位置
    sentences = []
    pos = 0
    for m in re.finditer(r'[。；]', chunk_content):
        end = m.end()
        sentences.append((pos, end))
        pos = end
    if pos < len(chunk_content):
        sentences.append((pos, len(chunk_content)))

    # 找到包含关键词的句子索引
    relevant_indices = []
    for i, (s, e) in enumerate(sentences):
        sent = chunk_content[s:e]
        for kw in keywords:
            if kw in sent:
                relevant_indices.append(i)
                break

    if not relevant_indices:
        return ""

    # 扩展到相邻句子以保持上下文连续
    start_idx = max(0, relevant_indices[0] - 1)
    end_idx = min(len(sentences) - 1, relevant_indices[-1] + 1)

    # 提取连续子串
    start_pos = sentences[start_idx][0]
    end_pos = sentences[end_idx][1]
    result = chunk_content[start_pos:end_pos]

    # 如果太长，从前面截断
    if len(result) > max_chars:
        # 保留最后 max_chars 个字符，从句子边界开始
        trim_start = len(result) - max_chars
        # 找到下一个句子边界
        next_period = result.find('。', trim_start)
        if next_period >= 0 and next_period < trim_start + 50:
            result = result[next_period + 1:]
        else:
            result = result[trim_start:]

    return result.strip()


def find_chunk_by_id(chunk_id, chunks):
    for c in chunks:
        if c.get("chunk_id") == chunk_id:
            return c.get("content", "")
    return None


def find_chunk_by_phrases(phrases, chunks, min_match=2):
    """找到匹配最多短语的 chunk"""
    best = None
    best_score = 0
    for c in chunks:
        content = c.get("content", "")
        score = sum(1 for p in phrases if p in content)
        if score > best_score:
            best_score = score
            best = content
    return best if best_score >= min_match else None


# 精确修复：(chunk_id, 关键词列表, 最大长度)
EXACT_FIXES = {
    4: ("HICH2020_2_FACT_005", ["斑点征", "灵敏度为91%", "特异度为89%"], 200),
    6: ("HICH2020_2_FACT_008", ["发生率高达67%"], 200),
    7: ("HICH2020_2_FACT_009", ["血浆渗透压", "320"], 150),
    8: ("HICH2020_2_FACT_014", ["高血糖", "7.8~10.0"], 200),
    9: ("HICH2020_2_REC_009", ["体温过高", "38.5"], 100),
    10: ("HICH2020_2_FACT_011", ["INTERACT2", "强化降压", "安全性"], 300),
    11: ("HICH2020_2_FACT_017", ["STICH", "Mendelow"], 250),
    12: ("HICH2020_2_FACT_018", ["MISTIE", "506例"], 300),
    13: ("HICH2020_2_FACT_014", ["间歇性空气压缩装置", "深静脉血栓"], 150),
    15: ("HICH2020_2_FACT_009", ["ICP", "20mmHg", "甘露醇"], 250),
    18: ("HICH2020_2_FACT_014", ["感染相关并发症", "30d内再入院", "肺炎"], 150),
    21: ("HICH2020_2_FACT_016", ["血肿量", "20ml", "内科治疗"], 200),
    22: ("HICH2020_2_FACT_023", ["小脑出血", "12~15"], 200),
    23: ("HICH2020_2_FACT_024", ["脑干出血", "血肿量>5"], 200),
    24: ("HICH2020_2_FACT_009", ["ICP", "20mmHg", "降颅压"], 200),
    25: ("HICH2020_2_FACT_008", ["GCS3-8分", "ICP监测", "GCS9-12分"], 250),
    26: ("HICH2020_2_FACT_012", ["PATICH", "201例"], 200),
    27: ("HICH2020_2_FACT_014", ["预防性抗癫痫", "皮质受累"], 200),
    28: ("HICH2020_2_FACT_022", ["阿替普酶", "1mg"], 200),
    33: ("HICH2020_2_FACT_005", ["渗漏征", "93.3%", "88.9%"], 200),
    34: ("HICH2020_2_FACT_005", ["黑洞征", "混杂征", "岛征"], 300),
    35: ("HICH2020_2_FACT_006", ["BRAIN", "24分"], 200),
    37: ("HICH2020_2_FACT_012", ["乌拉地尔", "拉贝洛尔"], 150),
    38: ("HICH2020_2_FACT_011", ["收缩压≤130mmHg", "颅外缺血"], 150),
    39: ("HICH2020_2_FACT_011", ["120-130", "110"], 150),
    40: ("HICH2020_2_FACT_012", ["第1小时", "140mmHg", "维持7天"], 200),
    42: ("HICH2020_2_FACT_013", ["TICH-2", "8小时"], 250),
    43: ("HICH2020_2_FACT_016", ["ICP>25", "颞叶钩回疝"], 250),
    44: ("HICH2020_2_FACT_018", ["MISTIE", "15ml", "终点指标"], 300),
    45: ("HICH2020_2_FACT_023", ["小脑出血", "12~15"], 200),
    46: ("HICH2020_2_FACT_022", ["脑室出血", "脑室外引流"], 300),
    47: ("HICH2020_2_FACT_024", ["脑干无牵拉", "轻吸引", "弱电凝"], 200),
    48: ("HICH2020_2_FACT_027", ["24~72h", "早期离开床位"], 200),
    49: ("HICH2020_2_FACT_005", ["HE", "33%", "12.5"], 200),
    50: ("HICH2020_2_FACT_002", ["急诊", "生命体征", "影像学"], 300),
    51: ("HICH2020_2_FACT_005", ["超早期", "72小时", "增强MRI"], 200),
    52: ("HICH2020_2_FACT_014", ["治疗性降温", "血肿周围水肿"], 150),
    53: ("HICH2020_2_FACT_009", ["0.25-1.5", "320"], 200),
    57: ("HICH2020_2_FACT_028", ["复发", "危险因素", "微出血"], 250),
    58: ("HICH2020_2_FACT_026", ["术后24", "复查头颅CT"], 200),
    60: ("HICH2020_2_FACT_002", ["院前急救", "迅速判断"], 300),
    62: ("HICH2020_2_FACT_011", ["INTERACT2", "ATACH"], 350),
    64: ("HICH2020_2_FACT_005", ["黑洞征", "混杂征", "岛征"], 300),
    65: ("HICH2020_2_FACT_017", ["STICH", "Mendelow", "1033"], 300),
    66: ("HICH2020_2_FACT_016", ["骨瓣开颅", "小骨窗开颅"], 250),
    67: ("HICH2020_2_FACT_020", ["神经内镜", "血肿清除率"], 300),
    68: ("HICH2020_2_FACT_022", ["脑室出血", "脑室外引流", "20ml"], 300),
    70: ("HICH2020_2_FACT_002", ["院前急救", "迅速判断", "病史"], 300),
    72: ("HICH2020_2_FACT_026", ["术后24", "复查头颅CT", "术后处理"], 250),
    76: ("HICH2020_2_FACT_028", ["复发", "亚洲人群", "深部出血"], 250),
    77: ("HICH2020_2_FACT_028", ["复发", "高龄", "微出血", "血压"], 300),
    78: ("HICH2020_2_FACT_028", ["他汀类药物", "争议", "荟萃分析"], 250),
    79: ("HICH2020_2_FACT_023", ["小脑出血", "12~15", "生存率"], 300),
    84: ("HICH2020_2_REC_007", ["130mmHg", "颅外缺血"], 150),
    85: ("HICH2020_2_FACT_013", ["氨甲环酸", "TICH-2", "HE"], 250),
    91: ("HICH2020_2_FACT_014", ["血栓形成", "间歇性空气压缩装置"], 150),
    97: ("HICH2020_2_FACT_002", ["院前急救", "降血压"], 200),
    99: ("HICH2020_2_REC_010", ["血肿量>30ml", "GCS<9分", "脑疝"], 250),
    100: ("HICH2020_2_REC_007", ["收缩压", "150~220", "140mmHg"], 200),
}


def main():
    with open(QUESTION_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    with open(REVIEW_FILE, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    chunks = load_chunks()
    review_map = {r["id"]: r for r in reviews}

    fixed = 0
    failed = 0

    for q in questions:
        qid = q["id"]
        if qid not in review_map:
            continue
        cr = review_map[qid].get("context_review", {})
        if cr.get("passed", False):
            continue

        if qid not in EXACT_FIXES:
            continue

        chunk_id, keywords, max_chars = EXACT_FIXES[qid]
        chunk_content = find_chunk_by_id(chunk_id, chunks)

        if not chunk_content:
            # 回退：用关键词搜索
            chunk_content = find_chunk_by_phrases(keywords, chunks)
            if not chunk_content:
                failed += 1
                print(f"  Q{qid}: 找不到 chunk {chunk_id}")
                continue

        # 提取包含关键词的精简内容
        concise = extract_by_keywords(chunk_content, keywords, max_chars)
        if concise and len(concise) > 20:
            q["golden_context"] = concise
            fixed += 1
        else:
            # 回退：用整个 chunk
            q["golden_context"] = chunk_content
            fixed += 1
            print(f"  Q{qid}: 使用整个 chunk (len={len(chunk_content)})")

    with open(QUESTION_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"\n修复: {fixed}, 失败: {failed}")
    print(f"已保存到 {QUESTION_FILE}")


if __name__ == "__main__":
    main()
