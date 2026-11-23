# 赛前简报（TEF-DLR）

环境取自 LAIC 2026–27, São Paulo（2026-11-20），共 2646 人、474 人进 Day 2；对位胜率合并了 TEF-DLR、TEF-30C 两个窗口。胜率里平局算 1/3 胜，全场平均 47.5%，高于它就是赢面。数字随每周一的数据更新自动重算；推荐分档是人工判断，定于 2026-10-04。

## 1. 会遇到谁

按 Day 2 份额排（想进前排一定会遇到的环境）。这是上一场的环境，不是对下一场的预测。

| 卡组 | Day 2 份额 | 全场份额 | 上个窗口 | 走势 |
|---|---|---|---|---|
| Dragapult | 23.0% | 19.4% | 18.5% | ↑ |
| Basic Box | 11.0% | 9.0% | 7.0% | ↑ |
| N's Zoroark | 9.9% | 9.3% | 6.0% | ↑ |
| Slowking | 7.2% | 6.1% | 6.0% | → |
| Dragapult Dudunsparce | 5.9% | 5.2% | 0.8% | ↑ |
| Crustle | 5.1% | 2.9% | 2.4% | ↑ |
| Ogerpon Meganium Hydrapple | 4.9% | 5.1% | 3.9% | ↑ |
| Mega Excadrill | 4.4% | 2.4% | 4.3% | ↓ |
| Alakazam Dudunsparce | 4.2% | 5.2% | 5.3% | → |
| Mega Rayquaza | 3.8% | 4.1% | 0.0% | ↑ |
| Dhelmise | 3.2% | 3.6% | 4.6% | ↓ |
| Festival Lead | 2.9% | 1.5% | 3.5% | ↓ |

- Frankfurt 夺冠后，Alakazam Dusknoir 和 Festival Lead 大概率变多；按 Day 2 份额 5% 和 7% 重算，Basic Box 仍在前列。
- Dragapult ex 份额在下降，但仍是遇到最多的对手；不能打 Dragapult 的卡组不要带。

## 2. 带哪套

| 档 | 卡组 | 对 Day 2 期望胜率 | 胜率（局数） | 理由 | 适合谁 |
|---|---|---|---|---|---|
| 首选 | [Basic Box](TEF-DLR/basic-box-m.md) | 47.7% | 49.5%（9777） | 两个窗口都高于平均，打赢最多的 Dragapult ex，平局最少 | 想要稳定成绩的人；全是基础宝可梦，上手快 |
| 高上限 | [Alakazam Dusknoir](TEF-DLR/alakazam-dusknoir.md) | 47.5% | 47.8%（2508） | 对 Day 2 环境期望胜率最高，Frankfurt 冠亚军，但样本只有 Basic Box 的六分之一 | 练熟了 Stage 2 双进化线的人；夺冠后对手会开始准备它 |
| 稳妥 | [Dragapult](TEF-DLR/dragapult-ex.md) | 48.1% | 50.8%（21385） | 环境第一，下限高，但 Day 2 被针对后只剩平均水平 | 熟练度高、求稳进 Day 2 的人 |
| 稳妥 | [Slowking](TEF-DLR/slowking-scr.md) | 49.2% | 49.4%（8133） | 两个窗口都约 50%，打 Dragapult 和 Excadrill 有利 | 熟悉复制招式工具箱的人；怕 Alakazam 系和 Dhelmise |
| 针对 | [Crustle](TEF-DLR/crustle-dri.md) | 51.0% | 50.5%（3504） | 打 Dragapult ex 69%，但打 Festival Lead、Mega Excadrill、Slowking 几乎不能打 | 只在预计 Dragapult 特别多的比赛带 |

**避开**：Alakazam Dudunsparce（打最常遇到的 Dragapult ex 只有约三成）；Mega Excadrill（打 Slowking、Alakazam Dudunsparce、Dragapult Blaziken 都很差）；Dragapult Dusknoir（各方面都不如纯 Dragapult ex）

> 注意：最新数字和推荐分档不一致，`data/brief/picks.yaml` 需要重新看：
>
> - 推荐分档是按 TEF-30C 定的，这里的数字已经是 TEF-DLR
> - Basic Box 标为首选，但现在按对 Day 2 期望胜率只排第 8（局数 ≥ 300 的卡组里）
> - Alakazam Dusknoir 标为高上限，但现在按对 Day 2 期望胜率只排第 9（局数 ≥ 300 的卡组里）

点卡组名看它的对局速查。

## 3. 卡表怎么微调

公开卡表里带和不带某张卡的胜率差，按对手的 Day 2 份额加权。只有成绩靠前的选手公开卡表，这是相关，不是证明：差值可能来自同一组一起出现的卡或选手水平。各卡组的速查页里有完整列表。

**Basic Box**

- **Iron Crown ex**（60.2% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -5.4 个百分点；差得最多的是对 Dhelmise，带 68.4%（114 局）对不带 86.8%（53 局）
- **Jamming Tower**（15.5% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -11.9 个百分点；差得最多的是对 Slowking，带 45.5%（33 局）对不带 67.3%（205 局）

**Alakazam Dusknoir**：没有哪张卡的差值够明显（样本或差值太小），按常见卡表带。

**Dragapult**：没有哪张卡的差值够明显（样本或差值太小），按常见卡表带。

**Slowking**

- **Mew ex**（53.5% 的卡表带）：带上或多带，对 Day 2 环境加权胜率差 +4.6 个百分点；差得最多的是对 Alakazam Dudunsparce，带 45.0%（57 局）对不带 24.6%（61 局）

**Crustle**

- **Tool Scrapper**（19.2% 的卡表带）：带上或多带，对 Day 2 环境加权胜率差 +7.2 个百分点；差得最多的是对 Slowking，带 60.8%（17 局）对不带 26.4%（58 局）
- **Azurill**（18.4% 的卡表带）：带上或多带，对 Day 2 环境加权胜率差 +6.9 个百分点；差得最多的是对 N's Zoroark，带 89.9%（23 局）对不带 73.3%（110 局）
- **Team Rocket's Factory**（78.0% 的卡表带）：考虑少带或不带，对 Day 2 环境加权胜率差 -7.0 个百分点；差得最多的是对 Dhelmise，带 58.3%（40 局）对不带 91.7%（12 局）
