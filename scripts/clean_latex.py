r"""
clean_latex.py
将 LaTeX 数学表达式转换为纯文本。

处理规则：
  1. 引文标记 $^{[1-5]}$ → 移除
  2. 百分比 $91\%$ → 91%
  3. 数学符号 \sim → ~, \leqslant → ≤, \geqslant → ≥, \ge → ≥, \le → ≤
  4. \mathrm{...} → 移除命令，保留内容
  5. 下标 T_{1} → T1, T_{2} → T2
  6. 上标 ^{2} → ² (或移除)
  7. 其他 \xxx → 移除命令
  8. $...$ → 去掉 $，处理内部
  9. 剩余花括号 {} → 移除
"""
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).parent.parent


def clean_latex_text(s):
    """将 LaTeX 数学表达式转为纯文本"""
    if not s:
        return s

    # NFKC 归一化
    s = unicodedata.normalize('NFKC', s)

    # 处理 $...$ 内的 LaTeX
    def replace_latex(m):
        inner = m.group(1)
        # 引文标记 $^{[1-5]}$ → 移除
        if re.match(r'\^\{?\[', inner):
            return ''
        # $^{}$ → 移除
        if inner == '^{}':
            return ''
        # $@$ → @
        if inner == '@':
            return '@'
        # $\textcircled{1}$ → (1)
        mc = re.match(r'\\textcircled\{(\d+)\}', inner)
        if mc:
            return f'({mc.group(1)})'

        # 替换 LaTeX 命令为纯文本
        text = inner
        # \% → %
        text = text.replace('\\%', '%')
        # \sim → ~
        text = text.replace('\\sim', '~')
        # \leqslant, \le, \leq → ≤
        text = re.sub(r'\\le(?:qslant|q)?', '≤', text)
        # \geqslant, \ge, \geq → ≥
        text = re.sub(r'\\ge(?:qslant|q)?', '≥', text)
        # \times → ×
        text = text.replace('\\times', '×')
        # \pm → ±
        text = text.replace('\\pm', '±')
        # \neq → ≠
        text = text.replace('\\neq', '≠')
        # \approx → ≈
        text = text.replace('\\approx', '≈')
        # \infty → ∞
        text = text.replace('\\infty', '∞')
        # \beta → β, \alpha → α, etc.
        greek = {
            '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
            '\\theta': 'θ', '\\mu': 'μ', '\\sigma': 'σ', '\\pi': 'π',
            '\\lambda': 'λ', '\\omega': 'ω', '\\phi': 'φ', '\\psi': 'ψ',
            '\\chi': 'χ', '\\tau': 'τ', '\\rho': 'ρ', '\\eta': 'η',
            '\\epsilon': 'ε', '\\zeta': 'ζ', '\\kappa': 'κ', '\\nu': 'ν',
            '\\xi': 'ξ', '\\psi': 'ψ', '\\Psi': 'Ψ', '\\Omega': 'Ω',
            '\\Delta': 'Δ', '\\Sigma': 'Σ', '\\Pi': 'Π', '\\Phi': 'Φ',
        }
        for cmd, char in greek.items():
            text = text.replace(cmd, char)

        # \mathrm{...} → 内容
        text = re.sub(r'\\mathrm\{([^}]*)\}', r'\1', text)
        # \mathbf{...} → 内容
        text = re.sub(r'\\mathbf\{([^}]*)\}', r'\1', text)
        # \mathsf{...} → 内容
        text = re.sub(r'\\mathsf\{([^}]*)\}', r'\1', text)
        # \text{...} → 内容
        text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
        # \textbf{...} → 内容
        text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
        # \textit{...} → 内容
        text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
        # \boldsymbol{...} → 内容
        text = re.sub(r'\\boldsymbol\{([^}]*)\}', r'\1', text)

        # 下标 _{...} → 移除下标标记，保留内容
        text = re.sub(r'_\{([^}]*)\}', r'\1', text)
        text = re.sub(r'_([0-9a-zA-Z])', r'\1', text)

        # 上标 ^{...} → 移除上标标记（多数是引用或单位上标）
        text = re.sub(r'\^\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\^([0-9a-zA-Z])', r'\1', text)

        # \left( \right) → ( )
        text = text.replace('\\left(', '(')
        text = text.replace('\\right)', ')')
        text = text.replace('\\left[', '[')
        text = text.replace('\\right]', ']')
        text = text.replace('\\left|', '|')
        text = text.replace('\\right|', '|')

        # \circ → °
        text = text.replace('\\circ', '°')

        # \quad \qquad → 空格
        text = text.replace('\\qquad', ' ')
        text = text.replace('\\quad', ' ')

        # \; \: \, → 空格
        text = re.sub(r'\\[,;:!]\s*', ' ', text)

        # ~ → 空格（LaTeX 不换行空格）
        text = text.replace('~', ' ')

        # 移除剩余的 \命令
        text = re.sub(r'\\[a-zA-Z]+', '', text)

        # 移除花括号
        text = text.replace('{', '').replace('}', '')

        # 清理多余空格
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    # 匹配 $...$（非贪婪）
    s = re.sub(r'\$([^$]+)\$', replace_latex, s)

    # 清理引文标记 [数字] （非 LaTeX 的普通引文）
    s = re.sub(r'\[[\d,\-\s]+\]', '', s)

    # 去除所有空白（与 clean_text 一致）
    s = re.sub(r'\s+', '', s)

    return s


def clean_question_gc(gc):
    """清洗 golden_context"""
    if isinstance(gc, str):
        return clean_latex_text(gc)
    elif isinstance(gc, list):
        result = []
        for item in gc:
            if isinstance(item, dict):
                new_item = dict(item)
                if "context" in new_item:
                    new_item["context"] = clean_latex_text(new_item["context"])
                result.append(new_item)
            elif isinstance(item, str):
                result.append(clean_latex_text(item))
            else:
                result.append(item)
        return result
    return gc


def main():
    # 清洗 question 文件
    question_files = [
        ROOT / "question" / "HICH" / "HICH_questions.json",
        ROOT / "question" / "ICH2019" / "ICH2019_questions.json",
        ROOT / "question" / "STROKE2024" / "stroke2024_questions.json",
        ROOT / "question" / "PREV2024" / "prev2024_questions.json",
        ROOT / "question" / "merged" / "crossbook_questions.json",
        ROOT / "question" / "2026_06_23" / "跨指南题目集1.json",
        ROOT / "question" / "2026_06_23" / "跨指南题目集2.json",
    ]

    print("=== 清洗 question 文件 ===")
    for f in question_files:
        if not f.exists():
            continue
        with open(f, "r", encoding="utf-8") as fh:
            qs = json.load(fh)
        for q in qs:
            if "golden_context" in q:
                q["golden_context"] = clean_question_gc(q["golden_context"])
            if "standard_answer" in q:
                q["standard_answer"] = clean_latex_text(q["standard_answer"])
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(qs, fh, ensure_ascii=False, indent=2)
        print(f"  {f.name}: 已清洗")

    # 清洗 chunks（内存清洗后保存）
    print("\n=== 清洗 chunks 文件 ===")
    chunks_dir = ROOT / "chunks"
    total = 0
    for d in sorted(chunks_dir.iterdir()):
        if not (d.is_dir() and d.name.startswith("chunks_")):
            continue
        data_file = d / "chunks_data.json"
        if not data_file.exists():
            continue
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 兼容新格式（dict with 'chunks' key）和旧格式（list）
        if isinstance(data, dict):
            chunks = data.get("chunks", [])
        else:
            chunks = data
        modified = False
        for c in chunks:
            if "content" in c:
                new_content = clean_latex_text(c["content"])
                if new_content != c["content"]:
                    c["content"] = new_content
                    modified = True
            if "summary" in c:
                new_summary = clean_latex_text(c["summary"])
                if new_summary != c["summary"]:
                    c["summary"] = new_summary
                    modified = True
        if modified:
            with open(data_file, "w", encoding="utf-8") as f:
                if isinstance(data, dict):
                    data["chunks"] = chunks
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    json.dump(chunks, f, ensure_ascii=False, indent=2)
            total += 1
            print(f"  {d.name}: 已清洗")
    print(f"\n共清洗 {total} 个 chunks 目录")


if __name__ == "__main__":
    main()
