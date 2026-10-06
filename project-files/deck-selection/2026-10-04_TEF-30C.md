# 当前 Standard 环境选卡组分析（TEF-30C，2026-10-04）

数字来自 `selection_TEF-30C.json`（`python -m ptcg.selection` 生成）。

## 用了哪些数据

- **环境（会遇到谁）**：TEF-30C 卡池窗口，也就是 30th Celebration 上市后的两场区域赛：
  Frankfurt（2793 人）和 Brisbane（817 人），都在 2026-09-26，合计 3610 人、656 人进 Day 2。
- **对位胜率**：把上一个窗口 TEF-PBL（Worlds 2026，2026-08-28；Baltimore，2026-09-19）也算进来，
  四场比赛合计约 7500 名选手的每一轮对局。30th Celebration 对环境改动很小（Frankfurt 508 份卡表里只有
  54 份用了它的 Mew ex、15 份用了 Unown），所以两个窗口的对位可以合并。
- 胜率 = 每局得分率，平局算 1/3 胜（比赛积分 3/1/0）。因为平局多，**全场平均只有 47.6%**，
  高于 47.6% 就是赢面。镜像对局不计。
- **期望胜率**：按 Day 2 各卡组的份额加权它的对位胜率。Day 2 是想进前排一定会遇到的环境。
  小样本对位向平均值收缩（每个对位加 20 局"平均局"），避免十几局的对位左右结论。

## 结论

| 推荐 | 卡组 | 理由 |
|---|---|---|
| **首选** | Basic Box（Mega Kangaskhan） | 两个窗口都高于平均，打赢最大的 Dragapult，平局最少 |
| 高上限 | Alakazam Dusknoir | 数字最好，Frankfurt 包揽冠亚军，但样本小、操作难 |
| 稳妥 | Dragapult ex | 环境第一，下限高，但在 Day 2 被针对后只剩平均水平 |
| 稳妥 | Slowking | 两个窗口都约 50%，打 Dragapult 和 Excadrill 有利 |
| 针对 | Crustle | 只在 Dragapult 特别多的比赛带：打 Dragapult ex 69% |
| **避开** | Alakazam Dudunsparce、Mega Excadrill、Dragapult Dusknoir | 份额都在 5–6%，胜率却只有 44–47%，进 Day 2 的比例低 |

### 1. 首选：Basic Box（Mega Kangaskhan ex）

- 份额 6.1%，Day 2 份额 7.9%（晋级率 1.30 倍）。
- 胜率 51.5%（3702 局），Day 2 对局 50.7%（597 局，Day 2 平均 47.8%）。TEF-PBL 52.4%、TEF-30C 50.6%，两段都稳。
- 期望胜率对 Day 2 环境 50.5%，样本足够的卡组里最高。
- 打 Dragapult ex 52.7%（732 局）、Dragapult Dusknoir 52.9%、Mega Excadrill 54.0%、Dhelmise 62.9%、Lucario Hariyama 71.2%。
- 平局率 11.6%，主流卡组里最低。Bo3 50 分钟的赛制里平局等于输掉 2 分，这一点很值钱。
- 怕：Ogerpon Meganium Hydrapple 33.3%（110 局）、Rocket's Honchkrow 37.3%、Alakazam Dudunsparce 42.1%、Crustle 42.6%。这几套加起来约 10% 的 Day 2。
- 拿过 Baltimore 冠军，Baltimore 前 8 有 3 套。

### 2. 高上限：Alakazam Dusknoir

- 只有 0.9% 的人带（TEF-30C 34 人），但 Day 2 份额 1.7%（晋级率 1.78 倍，所有卡组最高），Frankfurt 冠亚军都是它。
- 胜率 53.5%（656 局），Day 2 55.2%（125 局）。期望胜率对 Day 2 环境 51.2%，排第一。
- 打 Basic Box 71.5%、Slowking 70.6%、Mega Excadrill 88.2%、Alakazam Dudunsparce 66.7%。
- 怕：Dhelmise 24.4%、Crustle 26.9%、Lopunny Dudunsparce 19.0%、Lucario Hariyama 23.5%（都只有 14–26 局，方向可信，具体数字不可信）；打 Dragapult ex 46.0%（113 局），略低于平均。
- 风险：样本只有 Basic Box 的六分之一；TEF-PBL 窗口只有 50.9%，好成绩主要来自 Frankfurt 一场。
  Stage 2 双进化线（Alakazam + Dusknoir），没练过不建议直接上。夺冠后份额大概率上涨，对手也会开始准备它。
- 常见卡表（11 份 TEF-30C 卡表）：4 Abra、4 Kadabra、3 Alakazam（MEG）、4 Duskull、2 Dusclops、2 Dusknoir（PRE）、
  1 Fezandipiti ex、1 Shaymin、2 Budew；4 Dawn、3 Gwynn、4 Hilda、4 Rare Candy、4 Poké Pad、3 Buddy-Buddy Poffin、
  3 Strange Timepiece、2 Night Stretcher、2 Special Red Card、1 Boss's Orders、1 Prime Catcher、1 Sacred Ash；
  4 Telepathic Psychic Energy、1 Psychic Energy。

### 3. 稳妥：Dragapult ex

- 份额 15.3%（上个窗口 18.8%，在下降），Day 2 份额 19.2%，TEF-30C 25 个前排位置里占 8 个。
- 胜率 50.8%（8701 局），但 Day 2 只有 47.6%，等于平均：大家都在针对它。
- 打 Alakazam Dudunsparce 60.4%、Festival Lead 60.6%、Ogerpon Meganium Hydrapple 62.9%、Dragapult Dusknoir 55.5%。
- 怕：Crustle 26.1%（440 局，环境里最一边倒的大样本对位）、Slowking 40.1%、Basic Box 42.6%、N's Zoroark 43.6%。
- 适合熟练度高、想要稳定 Day 2 的人；想冲冠的话期望值不如前两套。

### 4. 稳妥：Slowking

- 份额 6.1%，Day 2 7.6%（1.25 倍），胜率 50.2%（3466 局），两个窗口都在 50% 左右。
- 打 Dragapult ex 53.6%、Mega Excadrill 64.0%、Crustle 68.0%、Lucario Hariyama 79.2%。
- 怕：Alakazam Dudunsparce 28.4%、Dhelmise 31.3%、Ogerpon Meganium Hydrapple 41.7%、Alakazam Dusknoir 29.4%（34 局）。

### 5. 针对 Dragapult 的选择：Crustle

- 胜率 50.1%，打 Dragapult ex 68.6%（440 局）、Dragapult Blaziken 68.7%、Alakazam Dudunsparce 65.6%、N's Zoroark 63.2%。
- 但打 Festival Lead 20.0%、Mega Excadrill 19.1%、Slowking 27.6%，几乎不能打。
- 只在预计 Dragapult 特别多的比赛里带。

### 避开

| 卡组 | 份额 | 胜率 | Day 2 晋级率 | 主要问题 |
|---|---|---|---|---|
| Alakazam Dudunsparce | 5.8% | 44.6% | 0.66 | 打 Dragapult ex 只有 33.2%（643 局），而 Dragapult ex 是最常遇到的对手 |
| Mega Excadrill ex | 5.1% | 44.8% | 0.71 | 打 Slowking 32.8%、Alakazam Dudunsparce 23.6%、Dragapult Blaziken 21.6%、Basic Box 43.0% |
| Dragapult Dusknoir | 6.1% | 46.8% | 1.05 | 打 Dragapult ex 40.8%（721 局），对其他主流卡组也大多在 40–43%，各方面都不如纯 Dragapult ex |

其余份额 1% 以上、胜率低于 46% 的还有 Lucario Hariyama、Lopunny Dudunsparce、Cynthia Garchomp ex、
Grimmsnarl Froslass、Mega Lucario ex、Sharpedo Toxtricity。

## 全部卡组（份额 ≥ 0.5%，按对 Day 2 环境的期望胜率排序）

| 卡组 | 份额 | 上个窗口 | Day 2 晋级率 | 胜率 | Day 2 胜率 | 平局率 | 期望（全场） | 期望（Day 2） |
|---|---|---|---|---|---|---|---|---|
| Alakazam Dusknoir | 0.9% | 1.0% | 1.78 | 53.5% | 55.2% | 8.1% | 51.7% | 51.2% |
| Basic Box | 6.1% | 6.0% | 1.30 | 51.5% | 50.7% | 11.6% | 51.0% | 50.5% |
| Dragapult ex | 15.3% | 18.8% | 1.26 | 50.8% | 47.6% | 16.2% | 50.7% | 49.6% |
| Slowking | 6.1% | 5.6% | 1.25 | 50.2% | 48.1% | 13.7% | 50.0% | 49.6% |
| Crustle | 3.2% | 4.0% | 0.85 | 50.1% | 46.6% | 15.8% | 48.5% | 49.5% |
| Lopunny Dusknoir | 1.7% | 0.8% | 1.38 | 50.4% | 50.2% | 9.1% | 49.5% | 49.3% |
| Seaking | 0.6% | 0.6% | 1.91 | 50.9% | 45.8% | 15.2% | 48.6% | 48.3% |
| N's Zoroark | 6.7% | 7.7% | 1.25 | 49.0% | 51.4% | 15.3% | 49.0% | 48.2% |
| Festival Lead | 4.0% | 2.6% | 1.39 | 49.6% | 52.0% | 13.2% | 48.4% | 47.9% |
| Dragapult Blaziken | 4.4% | 5.9% | 1.03 | 48.0% | 44.2% | 17.2% | 48.4% | 47.2% |
| Dhelmise | 3.5% | 2.6% | 0.73 | 48.0% | 51.9% | 16.2% | 47.7% | 46.9% |
| Ogerpon Meganium Hydrapple | 3.2% | 2.3% | 1.14 | 47.1% | 49.4% | 13.9% | 47.5% | 46.9% |
| Dragapult Dusknoir | 6.1% | 8.0% | 1.05 | 46.8% | 44.7% | 12.8% | 47.0% | 46.4% |
| Mega Excadrill ex | 5.1% | 4.8% | 0.71 | 44.8% | 47.3% | 14.1% | 45.4% | 45.3% |
| Alakazam Dudunsparce | 5.8% | 6.3% | 0.66 | 44.6% | 45.9% | 16.2% | 45.5% | 44.6% |

完整表（含每个对位）见 `selection_TEF-30C.json`。全场平均胜率 47.6%，Day 2 平均 47.8%。

## 环境走向

- Frankfurt 夺冠后，Alakazam Dusknoir 和 Festival Lead（Frankfurt 前 16 有 2 套）大概率变多。
  假设 Alakazam Dusknoir 涨到 Day 2 的 5%、Festival Lead 涨到 7%，按同样的对位重算：
  Alakazam Dusknoir 50.6%、Basic Box 49.8%、Crustle 49.8%、Lopunny Dusknoir 49.7%、Dragapult ex 49.3%、Slowking 48.9%。
  Basic Box 会被 Alakazam Dusknoir 压一点，但仍在前列。
- Dragapult ex 份额从 18.8% 降到 15.3%，但仍是遇到最多的对手；不能打 Dragapult 的卡组不要带。
- Brisbane（大洋洲）的环境和全球基本一致：Dragapult ex 15.3%，接着是 Mega Excadrill 7.0%、Basic Box 6.7%、Slowking 6.6%。
  用 Brisbane 的份额重算，前三仍是 Alakazam Dusknoir 51.6%、Basic Box 50.7%、Slowking 49.8%。

## 局限

- 当前窗口只有两场比赛；10 月新的大赛进来后，每周一的 `collect` 会自动重算 `selection_*.json`，这份文字需要人工更新。
- 胜率反映"带这套卡组的人"的成绩，不只是卡组本身：强手集中的卡组（如 Dragapult ex）在 Day 1 胜率会偏高。
  Day 2 胜率只算双方都进了 Day 2 的轮次，更接近同水平对局，但样本小得多。
- 卡组分类沿用 Limitless Labs，同一名字下的不同构筑（例如带不带 Mew ex）没有拆开。
