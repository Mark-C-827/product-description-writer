# Product Description Writer

把一张枯燥的规格表，写成能卖货的商品详情页（PDP）文案。

原版来自 [SkillMedev/skills](https://github.com/SkillMedev/skills)（MIT 协议，
原始版本只有一份 3.6 KB 的 `SKILL.md`）。这一版在保留原版工作流与红线的基础上，
补齐了一个完整 Skill 应有的四件套：**SKILL.md / references / scripts / assets**，
并加入了输入契约、品类路由、合规审查和可执行的质量校验。

---

## 它做什么

输入：一份规格表 + 目标客户（+ 品牌语气）
输出：一段可直接粘贴的 PDP 主文案，外加一份「给商家的备注」

产出结构固定为：

```
Lead hook        一句话钩子，说出来的是"改变"，不是品类
Intro            2-3 句，每句 ≤ 20 词
Benefit bullets  3-5 条，加粗的卖点前置，每条都能追溯到一条规格
Good to know     诚实回答真实的购买顾虑（偏小就说偏小）
CTA              重申卖点，不是光秃秃的 "Buy now"
Details          所有数字、尺寸、材质、保养，一个都不能少
Notes to merchant  被舍弃的规格 / 无法证实的说法 / 待核实假设
```

核心立场：**只写来源能证明的东西**。性能数字、认证、材质、健康与安全声明，
不在规格表里就不许出现在页面上。这是这个 Skill 最硬的一条线。

---

## 目录结构

```
product-description-writer/
├── SKILL.md                       主指令（AI 读这个）
├── README.md
├── README.en.md
├── LICENSE                        MIT
├── references/                    按需加载的深度参考
│   ├── pdp-structure-playbook.md    F 型浏览与逐段规则
│   ├── benefit-translation.md       规格 → 卖点的翻译方法论
│   ├── objection-library.md         拦住购物车的那些疑虑
│   ├── voice-and-tone-matrix.md     品类语气对照
│   ├── compliance-redlines.md       合规红线与安全改写
│   └── category-playbooks.md        11 个品类的决策要点
├── scripts/                       可执行工具
│   ├── validate_pdp.py             文案质检（钩子/句长/卖点/数字覆盖/违禁词）
│   ├── extract_specs.py            从规格表提取规格清单
│   └── scaffold_pdp.py             生成空白骨架
├── assets/                        模板
│   ├── pdp-output-template.md       交付格式
│   ├── input-brief-template.md      写作前要收集什么
│   ├── qa-scorecard.md              加权评分表
│   ├── details-block-template.md    规格区模板
│   └── examples-before-after.md     正反例对照
└── examples/                      可直接跑的样例
    ├── spec-sheet.txt
    ├── sample-output-good.md
    └── sample-output-bad.md
```

---

## 安装

把整个目录放到你的 skills 目录即可。

```bash
# Claude Code / Codex
cp -r product-description-writer ~/.claude/skills/
cp -r product-description-writer ~/.codex/skills/

# Cursor：放到项目或全局的 skills 目录下
```

`SKILL.md` 的 frontmatter 里已有 `name` 与 `description`，会被自动识别触发。

---

## 三个脚本（需要 Python 3.9+，无第三方依赖）

```bash
# 1. 质检写好的文案 —— 有失败项则退出码 1
python scripts/validate_pdp.py path/to/copy.md
python scripts/validate_pdp.py copy.md --specs spec-sheet.txt   # 顺带检查数字覆盖
python scripts/validate_pdp.py copy.md --json                    # 机器可读输出

# 2. 从规格表抽出规格清单，确保没漏
python scripts/extract_specs.py spec-sheet.txt --out checklist.md

# 3. 生成空白骨架
python scripts/scaffold_pdp.py --category apparel --out draft.md
```

`validate_pdp.py` 会检查：钩子是否够短、句子是否超 20 词、卖点条数是否在 3-5、
卖点是否加粗前置、来源里的数字是否都出现在文案里、有无泛泛的违禁词、
CTA 是不是光秃秃的命令句、有没有 Details 区块。
另外会对临床声明、认证、安全承诺、虚假紧迫等**触发人工复核的告警**。

它是机械检查 —— 钩子写得好不好、卖点真不真，还是得人来判断，用 `assets/qa-scorecard.md`。

---

## 用法示例

给 AI 一段话就行：

> 用 product-description-writer 给这把刀写详情页文案。
> 规格：8 寸，316 不锈钢，61 HRC，15 度开刃，7.4 oz，Pakkawood 柄，只可手洗。
> 目标客户：家里做饭的人，受够了刀用两周就钝。
> 语气：像工具专家，不煽情。

AI 会先补问最多一个问题（通常是语气校准），然后按结构产出，并自行跑一次质检。

---

## 与原版的差异

| 项目 | 原版 | 这一版 |
| --- | --- | --- |
| SKILL.md | 单文件，3.6 KB | 增加输入契约、品类路由、合规审查、自检步骤、资源索引 |
| references | 无 | 6 篇深度参考 |
| scripts | 无 | 3 个可执行脚本 |
| assets | 无 | 5 份模板 + 正反例 |
| 质量校验 | 靠自觉 | 可执行的 linter + 加权评分表 |
| 合规 | 一条 Do NOT | 独立的红线文档 + 自动告警 |

原版的六步工作流、质量标准与 Do NOT 清单整体保留。

---

## 许可

MIT。原版版权归 SkillMedev，增强部分遵循同样的 MIT 条款。
详见 [LICENSE](LICENSE)。
