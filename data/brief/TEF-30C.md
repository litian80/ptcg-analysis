# 赛前简报（TEF-30C）

环境取自 Brisbane（2026-09-26）、Frankfurt（2026-09-26）、Recife（2026-10-03）、Louisville, KY（2026-10-10），共 7611 人、1363 人进 Day 2；对位胜率合并了 TEF-30C、TEF-PBL 两个窗口。胜率里平局算 1/3 胜，全场平均 47.6%，高于它就是赢面。数字随每周一的数据更新自动重算；推荐分档是人工判断，定于 2026-10-04。

## 1. 会遇到谁

按 Day 2 份额排（想进前排一定会遇到的环境）。这是上一场的环境，不是对下一场的预测。

| 卡组 | Day 2 份额 | 全场份额 | 上个窗口 | 走势 |
|---|---|---|---|---|
| Dragapult | 22.4% | 17.7% | 18.8% | ↓ |
| N's Zoroark | 8.5% | 6.2% | 7.7% | ↓ |
| Basic Box | 7.9% | 6.7% | 6.0% | ↑ |
| Slowking | 7.9% | 6.2% | 5.6% | ↑ |
| Dragapult Dusknoir | 4.7% | 5.2% | 8.0% | ↓ |
| Festival Lead | 4.5% | 3.2% | 2.6% | ↑ |
| Dragapult Blaziken | 4.4% | 4.1% | 5.9% | ↓ |
| Alakazam Dudunsparce | 4.3% | 5.7% | 6.3% | ↓ |
| Ogerpon Meganium Hydrapple | 3.5% | 3.4% | 2.3% | ↑ |
| Mega Excadrill | 3.4% | 5.0% | 4.8% | → |
| Crustle | 3.0% | 2.9% | 4.0% | ↓ |
| Dhelmise | 2.9% | 3.5% | 2.6% | ↑ |

- Frankfurt 夺冠后，Alakazam Dusknoir 和 Festival Lead 大概率变多；按 Day 2 份额 5% 和 7% 重算，Basic Box 仍在前列。
- Dragapult ex 份额在下降，但仍是遇到最多的对手；不能打 Dragapult 的卡组不要带。

## 2. 带哪套

| 档 | 卡组 | 对 Day 2 期望胜率 | 胜率（局数） | 理由 | 适合谁 |
|---|---|---|---|---|---|
| 首选 | [Basic Box](TEF-30C/basic-box-m.md) | 50.1% | 51.0%（5843） | 两个窗口都高于平均，打赢最多的 Dragapult ex，平局最少 | 想要稳定成绩的人；全是基础宝可梦，上手快 |
| 高上限 | [Alakazam Dusknoir](TEF-30C/alakazam-dusknoir.md) | 48.9% | 49.9%（1445） | 对 Day 2 环境期望胜率最高，Frankfurt 冠亚军，但样本只有 Basic Box 的六分之一 | 练熟了 Stage 2 双进化线的人；夺冠后对手会开始准备它 |
| 稳妥 | [Dragapult](TEF-30C/dragapult-ex.md) | 49.6% | 51.3%（13857） | 环境第一，下限高，但 Day 2 被针对后只剩平均水平 | 熟练度高、求稳进 Day 2 的人 |
| 稳妥 | [Slowking](TEF-30C/slowking-scr.md) | 49.1% | 49.7%（5386） | 两个窗口都约 50%，打 Dragapult 和 Excadrill 有利 | 熟悉复制招式工具箱的人；怕 Alakazam 系和 Dhelmise |
| 针对 | [Crustle](TEF-30C/crustle-dri.md) | 50.1% | 49.8%（2983） | 打 Dragapult ex 69%，但打 Festival Lead、Mega Excadrill、Slowking 几乎不能打 | 只在预计 Dragapult 特别多的比赛带 |

**避开**：Alakazam Dudunsparce（打最常遇到的 Dragapult ex 只有约三成）；Mega Excadrill（打 Slowking、Alakazam Dudunsparce、Dragapult Blaziken 都很差）；Dragapult Dusknoir（各方面都不如纯 Dragapult ex）

> 注意：最新数字和推荐分档不一致，`data/brief/picks.yaml` 需要重新看：
>
> - Alakazam Dusknoir 标为高上限，但现在按对 Day 2 期望胜率只排第 6（局数 ≥ 300 的卡组里）

点卡组名看它的对局速查。

## 3. 卡表怎么微调

公开卡表里带和不带某张卡的胜率差，按对手的 Day 2 份额加权。只有成绩靠前的选手公开卡表，这是相关，不是证明：差值可能来自同一组一起出现的卡或选手水平。各卡组的速查页里有完整列表。

**Basic Box**

- **N's Plan**（15.3% 的卡表带）：带上或多带，对 Day 2 环境加权胜率差 +8.8 个百分点；差得最多的是对 Crustle，带 84.8%（11 局）对不带 48.0%（66 局）
- **Paldean Tauros**（14.3% 的卡表带）：带上或多带，对 Day 2 环境加权胜率差 +7.9 个百分点；差得最多的是对 Dragapult Blaziken，带 87.5%（16 局）对不带 65.6%（97 局）
- **Hero's Cape**（34.2% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -4.2 个百分点；差得最多的是对 Lucario Hariyama，带 53.3%（15 局）对不带 82.1%（28 局）
- **Crispin**（85.0% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -5.6 个百分点；差得最多的是对 Crustle，带 48.8%（67 局）对不带 83.3%（10 局）

**Alakazam Dusknoir**

- **Patrat**（26.2% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -7.2 个百分点；差得最多的是对 Basic Box，带 54.5%（11 局）对不带 76.1%（39 局）

**Dragapult**：没有哪张卡的差值够明显（样本或差值太小），按常见卡表带。

**Slowking**

- **Brave Bangle**（24.8% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -6.4 个百分点；差得最多的是对 Dhelmise，带 23.8%（14 局）对不带 55.0%（57 局）

**Crustle**

- **Special Red Card**（27.4% 的卡表带）：带上或多带，对 Day 2 环境加权胜率差 +4.7 个百分点；差得最多的是对 Dragapult Blaziken，带 83.3%（16 局）对不带 60.2%（31 局）
- **Handheld Fan**（71.4% 的卡表带）：带上或多带，对 Day 2 环境加权胜率差 +4.2 个百分点；差得最多的是对 Slowking，带 52.3%（37 局）对不带 28.3%（20 局）
- **Bianca's Devotion**（63.7% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -5.2 个百分点；差得最多的是对 Slowking，带 36.7%（40 局）对不带 60.8%（17 局）
- **Team Rocket's Factory**（87.5% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -16.6 个百分点；差得最多的是对 N's Zoroark，带 69.6%（79 局）对不带 93.9%（11 局）
