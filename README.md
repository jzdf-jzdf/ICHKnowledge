# ICH Knowledge Base

脑出血（Intracerebral Hemorrhage, ICH）领域结构化知识库，为脑出血 AI 临床决策辅助系统提供知识支撑。知识库涵盖教材、临床指南和 PubMed 研究文献，并附带基于指南构建的问答数据集，可用于 RAG 评估或模型微调。

## 目录结构

```
├── md/                          # 知识文档（Markdown）
│   ├── ICHBooks/                #   教材与专著（27 篇）
│   ├── ICHGuideline/            #   临床指南与专家共识（38 篇）
│   └── ICHResearch/PubMed/      #   PubMed 研究文献（1569 篇）
├── chunks/                      # 预切块数据（由 md/ 文档切分生成）
│   └── chunks_<指南名>/         #   每个指南一个目录，含 chunks_data.json 等
├── question/                    # 问答数据集
│   ├── HICH/                    #   2020 中国高血压性脑出血多学科诊治指南
│   ├── ICH2019/                 #   2019 中国脑出血诊治指南
│   ├── PREV2024/                #   2024 脑血管病防治指南
│   ├── STROKE2024/              #   2024 中国重症卒中管理指南
│   ├── merged/                  #   跨指南合并数据集
│   └── 2026_06_23/              #   批次跨指南题目
└── scripts/                     # 维护脚本
```

## 知识文档

所有文档均为 Markdown 格式，按来源分为三类：

| 类别 | 文件数 | 时间跨度 | 说明 |
|------|--------|----------|------|
| ICHBooks | 27 | 1990–2023 | 神经外科教材及专著，如 Rhoton 颅脑解剖、Greenberg 神经外科手册等 |
| ICHGuideline | 38 | 2014–2026 | 中国脑出血诊治指南、AHA/ASA 指南、各类专家共识 |
| ICHResearch/PubMed | 1569 | 1989–2025 | PubMed 研究论文全文，涵盖血压管理、手术方式、血肿扩大预测、止血药物等领域 |

### 预切块（chunks）

`md/ICHGuideline/` 下的指南已按章节切块，存放在 `chunks/` 目录下。每个指南对应一个子目录，包含：

- `chunks_data.json` — 切块数据数组（含 `chunk_id`、`section`、`content`、`type` 等字段）
- `chunks.jsonl` — 同上，JSONL 格式
- `mapping.csv` — 章节映射
- `sections.json` — 章节元数据

切块与源 MD 文件的映射关系记录在 `chunks/chunk_summary.json` 中。

## 问答数据集

基于中文临床指南提取的结构化问答对，每条记录包含以下字段：

| 字段 | 说明 |
|------|------|
| `id` | 序号 |
| `level` | 难度等级（L1 基础记忆 → L4 综合推理） |
| `question` | 临床问题（中文） |
| `golden_context` | 对应指南中的原始证据段落（单指南为字符串，跨指南为对象数组） |

跨指南数据集（`merged/crossbook_questions.json`、`2026_06_23/`）额外包含：

| 字段 | 说明 |
|------|------|
| `evidence_doc` | 证据来源文档全名列表（如 `2019_中国脑出血诊治指南`） |
| `golden_context[].evidence_doc` | 每条证据的来源文档全名 |
| `golden_context[].context` | 证据原文 |

所有 `golden_context` 均已校验为对应 MD 原文件的精确子串（经 NFKC 规范化、去引文标记、去空白后比较）。

## 维护脚本

| 脚本 | 功能 |
|------|------|
| `verify_golden_context_md.py` | 校验 golden_context 是否为 MD 原文件的精确子串 |
| `verify_golden_context.py` | 校验 golden_context 是否为 chunk content 的精确子串 |
| `split_golden_context.py` | 自动将共用的多子项推荐意见切分为与题目对应的单子句 |
| `clean_text.py` | 清洗 question 文件中的 golden_context（NFKC + 去引文 + 去空白） |
| `fix_golden_context.py` | 修复不匹配的 golden_context（替换为 chunk 中的最佳匹配） |

## 使用场景

- **RAG 知识库**：直接作为检索增强生成系统的知识源
- **QA 评测基准**：使用问答数据集评估临床问答系统的准确性
- **模型微调**：基于 golden_context 构建监督微调数据
