# 逐个对局的打法

当前推荐的 5 套卡组，每套一个对局手册，覆盖它对 12 套主流卡组怎么打：

| 文件 | 卡组 | 推荐理由（见 `data/selection/TEF-30C.md`） |
|---|---|---|
| `basic-box-m.md` | Basic Box（Mega Kangaskhan） | 首选 |
| `alakazam-dusknoir.md` | Alakazam Dusknoir | 高上限，样本小 |
| `dragapult-ex.md` | Dragapult ex | 稳妥，环境第一 |
| `slowking-scr.md` | Slowking | 稳妥 |
| `crustle-dri.md` | Crustle | 针对 Dragapult |

每个对局写了：对局性质（谁快、奖赏卡交换）、开局与先后攻、按卡牌伤害算好的奖赏卡路线、对手的套路和怎么防、
关键卡与构筑、常见失误。没有卡牌文字或数据直接支持的判断标了"（推断）"。
比赛录像（`video/` 工具复盘的直播和 VOD）得出的打法标了"（录像）"并附带时间戳链接，只代表那几局。
关键判断带"（信心 70%，akd-mir-01）"：数字是这条判断现在的信心，随之后的录像、对局记录和玩家反馈更新，编号对应 `data/judgments/` 里的记录。

数据：Worlds 2026、Baltimore、Frankfurt、Brisbane（2026-08-28 到 2026-09-26）的逐轮对局和公开卡表。
`tech_<窗口>.json` 由 `python -m ptcg.matchups` 生成：每个对局里带某张卡和不带的胜率差。只有公开卡表的选手
（成绩靠前的）计入，绝对值偏高，只看差值，局数少时是噪声。卡牌效果取自 PokemonTCG/pokemon-tcg-data。

写手册时发现并已改正的 `data/archetypes/*.yaml` 错误：Moltres 打 Crustle 是 40（弱火）不是 20；Dusknoir 的 130
差 10 点击倒 Alakazam；Phantom Dive 的 6 个指示物收不了两只 70 HP；贴 Hero's Cape 的 Excadrill 扛得住 400；
Chi-Yu 有场地时打 Crustle 是 240；Slowking 可复制的 Annihilape SSP 100 Destined Fight；太晶 ex 在后备区不吃
Thunder Raid；先攻第 1 回合不能用支援者等。
