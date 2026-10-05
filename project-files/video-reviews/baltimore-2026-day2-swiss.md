# Baltimore 2026 区域赛第 2 天瑞士轮复盘

比赛 2026-09-19，环境 TEF-PBL（比现在少 30C 一个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-09-19_577_regional-baltimore-md。这里收第 2 天主舞台直播（https://www.youtube.com/watch?v=nLkFmtXdXGE）里有推荐卡组的两场瑞士轮；决赛圈见 baltimore-2026-top-cut.md，第 1 天见 baltimore-2026-day1.md。

做法：没有调用 API，在你电脑上看截图、对照解说写成。电脑上的复盘把第 13 轮记成了第 12 轮，按比赛数据改正。三个第三方上传（1esvHhud8ew、slNSyuvZoMs、gbRRf9Ca2so）分别是第 14 轮、四强 Dreitzler 对 Dobberstein 和第 13 轮，主舞台都播了，不用再看。

判断台账（data/judgments/）：第 14 轮是 Dragapult ex 镜像，dpx-mir-01 的验证结果记在 data/judgments/sources/2026-10-05_video_baltimore-2026.yaml。第 13 轮的对手 Rocket's Honchkrow 不在手册里，没有判断可验证。

## 第 14 轮：Halliburton（Dragapult ex）2-0 Melville（Dragapult ex）

视频：https://www.youtube.com/watch?v=nLkFmtXdXGE&t=9990s （约 2:46-3:28）。Liam Halliburton 最终第 7，Kira Melville 第 27。两人的 Hammer 版 Dragapult 是同样的 60 张：4 张 Crushing Hammer、2 只 Budew、2 张 Risky Ruins、2 只 Munkidori、2 个 Darkness、Rosa's Encouragement、Judge、Unfair Stamp。

### 第 1 局：Halliburton 胜（35 分钟）

- Melville 先攻，第 1 回合先把物品用完，之后用 Budew 锁物品。Halliburton 没有先锁，之后几乎每回合都被锁，手里全是物品。
- 双方各用了一次同一个组合：Risky Ruins 放的 2 个指示物，用 Munkidori 挪到对方的 Budew 上，再用 Itchy Pollen 击倒它（[2:59:00](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=10740s)、[3:01:00](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=10860s)）。
- Melville 先用 Crushing Hammer 拆掉 Halliburton 的 Munkidori 的 Darkness，再用 Boss's Orders + Phantom Dive 一次收掉两只 Drakloak（[3:08:30](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=11310s)）。
- Halliburton 翻盘：放下 Meowth ex，用 Last-Ditch Catch 找到 Rosa's Encouragement 贴能量，Night Stretcher 拿回 Darkness，再打 Unfair Stamp（[3:11:30](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=11490s)）。Melville 只差一张 Boss's Orders，没摸到。
- Halliburton 不赌 Mind Bend 的混乱硬币；他用 Boss's Orders 把对方撤退不了的 Dunsparce 拉到战斗场困住，再收掉它，断掉对方的抽牌。

### 第 2 局：Halliburton 胜

- Melville 的 Dunsparce、Fezandipiti ex、Unfair Stamp 都在奖赏卡里，第 1 回合没有支援者。Halliburton 第 3 回合用 Phantom Dive 收掉她的 Dreepy，Melville 投降。

### 对照手册

dragapult-ex.md 的镜像一节说中的：Crushing Hammer 先拆 Darkness；Boss's Orders + Phantom Dive 一次多张；Hammer 互拆后用 Rosa（只能在落后时用）；Unfair Stamp 留到对手快拿完时；被混乱时不赌硬币。

台账：dpx-mir-01 第 1 局 held（互锁时双方都先用 Itchy Pollen 击倒对方的 Budew 解锁；Halliburton 解锁后才打得出 Night Stretcher 和 Unfair Stamp），第 2 局 n/a（没有互锁）。dpx-mir-02 两局都没有记：Melville 能出 Dragapult ex 时先用 Hammer 拆 Darkness、继续 Itchy Pollen，没有撒指示物（[3:04:00](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=11040s)），方向一致，但用的是 Budew，不是 Jet Headbutt。

写进手册的（PR #34）：

1. 新判断 dpx-mir-03（信心 60%）：第一次拿奖用 Itchy Pollen 击倒对方的 Budew，拿 1 张、对方下回合锁不了我们、还锁住对方，对方被锁时也打不出 Unfair Stamp（物品）。电脑上的复盘建议 65%；只有两场录像，先定 60%。另一场是 2026 世界赛第 1 天第 3 轮，见 worlds2026-swiss.md。
2. 镜像一节加了这一场的小节。

没写进手册的：对方的 Dudunsparce 在奖赏卡里时，用 Boss's Orders 把对方的 Dunsparce 拉到战斗场困住（推断，只有这一局）。

dragapult-ex.yaml 补了这一场的录像证据。

## 第 13 轮：Potti（Dragapult ex）2-0 Siu（Rocket's Honchkrow）

视频：https://www.youtube.com/watch?v=nLkFmtXdXGE&t=6420s 。Rohit Potti 最终第 3（Hammer 版，带 Special Red Card），四强输给了后来的冠军 Kasturi；Ethan Siu 最终第 74。手册没有 Honchkrow 一节，只做简要记录。

- 第 1 局：Siu 先拿 1 张后，Potti 马上打 Unfair Stamp（[1:47:00](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=6420s)）。之后 Phantom Dive 每回合收进化后的 Honchkrow：Team Rocket's Articuno 的 Repelling Veil 只挡招式对基础 Team Rocket's 宝可梦的效果。Potti 三张 Crushing Hammer 都是反面，但 Siu 一直没能一击 Dragapult ex。Munkidori 从奖赏卡出来后收尾。
- 第 2 局：Potti 一路领先，时间快到时收尾。
- Siu 给战斗场的 Articuno 挂 Lucky Helmet，被打时抽 2，用来抵消 Unfair Stamp。

dragapult-ex.yaml 补了这一场的录像证据。
