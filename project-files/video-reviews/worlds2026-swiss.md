# 2026 世界赛瑞士轮复盘

比赛 2026-08-28 开始，环境 TEF-PBL（比现在少 30C 一个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-08-28_515_world-championships-2026。这里收第 1、2 天直播（第 1 天 iEM8bQbnA90、第 2 天 qwBID2ApsOY）里有我们推荐卡组的瑞士轮场次；决赛圈见 worlds2026-masters-top-cut.md 和 worlds2026-finals.md。

做法：没有调用 API，在你电脑上看截图、对照解说写成。奖赏卡数取自解说。

判断台账（data/judgments/）：下面两个对局之前都没有登记判断，没有要记的验证结果；这次写进手册的关键判断登记成了新判断。crustle-dri.md 里两处 Special Red Card 的条件写错了，记成已核对的纠错，见 data/judgments/sources/2026-10-05_video_worlds-2026.yaml。

## 第 12 轮：Matsui（Crustle）2-0 Johnson（Alakazam Dusknoir）

视频：第 2 天直播 https://www.youtube.com/watch?v=qwBID2ApsOY&t=16920s （约 4:42-5:12）。Satoshi Matsui 最终第 6，卡表和 crustle-dri.md 的核心基本一致，另带 3 张 Eri、Enhanced Hammer、Special Red Card。Angus Johnson 的 Alakazam Dusknoir 和 Łaszkiewicz（最终第 7）的卡表一张不差，整副只有 5 个能量（4 张 Telepathic Psychic Energy、1 张 Psychic Energy）。

### 第 1 局：Matsui 胜

- Johnson 两只 Dusclops 在奖赏卡里，他用 Budew 锁物品。
- Matsui 把 Mist 贴在 Mega Kangaskhan ex 上，再用 Team Rocket's Petrel 拿 Hero's Cape 挂上去。Cape 是道具，Budew 锁不住。
- Kangaskhan 还剩 270/400，换下来的 Crustle 只剩 10/170（[4:55:20](https://www.youtube.com/watch?v=qwBID2ApsOY&t=17720s)）。Johnson 的两次 Cursed Blast 打不动 Kangaskhan，Powerful Hand 又被 Mist 挡住，Matsui 拿下。

### 第 2 局：Matsui 胜

- Johnson 两只 Kadabra 和一张 Rare Candy 在奖赏卡里。
- Matsui 用 Lumiose City 拿 Kangaskhan（场地，Budew 锁不住）。Crustle 击倒带能量的宝可梦，Johnson 场上没有能量了（[5:03:05](https://www.youtube.com/watch?v=qwBID2ApsOY&t=18185s)；画面只看到结果）。
- Boss's Orders 拉出没有能量的 Duskull 困在战斗场，Johnson 认输。

### 对照手册

crustle-dri.md 的 vs Alakazam Dusknoir（69.2%）说中的：第一时间贴 Mist；Boss 拉 Duskull 断 Dusknoir；"Dusknoir 130 加 Dusclops 50 能打倒 170，所以堆到 190"（这局 170 的 Crustle 被打到只剩 10）。

写进手册的（PR #32）：

1. crustle-dri.md：手里有 Kangaskhan 时，第一张 Mist 和 Hero's Cape 先给 Kangaskhan（登记成判断 cru-akd-01，信心 60%）；被 Budew 锁物品时，用 Petrel 拿 Cape、用 Lumiose City 找 Kangaskhan；对手只有 5 个能量，先击倒带能量的宝可梦。
2. alakazam-dusknoir.md 的 vs Crustle（26.9%）：路线 1"Kangaskhan 在战斗场时 Dusknoir 130 加 Powerful Hand"只在 Kangaskhan 没贴 Mist 时成立，贴了 Mist 再挂 Cape 是 400，三次 Cursed Blast（390）也打不倒；"选后攻、Budew 锁物品"那句补上挡不住 Hero's Cape（道具）和 Lumiose City（场地）；对方会先击倒带能量的宝可梦，Matsui 的卡表还带 Enhanced Hammer。

没写进手册的：Alakazam 一方在对方的 Kangaskhan 贴上 Mist 之后不再打它，改打没贴 Mist 的 Crustle 和 Dwebble。Johnson 没机会试，一局都没有检验；Alakazam Dusknoir 在现在的环境份额不到 1%，也没登记成待验证的论点。

crustle-dri.yaml 也补了这一场的录像证据。

## 第 1 天第 6 轮：Łaszkiewicz（Alakazam Dusknoir）2-1 Lepine（N's Zoroark）

视频：第 1 天直播 https://www.youtube.com/watch?v=iEM8bQbnA90&t=27960s （约 7:46-8:25）。Piper Lepine 的 N's Zoroark 是 N's Castle 版：Pecharunt ex 加 Binding Mochi、1 张 Special Red Card、2 张 N's Castle，没有 Watchtower，也没有 Judge。这是 alakazam-dusknoir.md 的 vs N's Zoroark 一节第一次有录像。

### 第 1 局：Łaszkiewicz 胜

- Lepine 复制 Shred，先拿第 1 张。
- Łaszkiewicz 拿到 2 张后就停手，只打伤、不击倒。解说讲得很清楚：Special Red Card 要等他剩 3 张以下才能打，他不进这个范围，Lepine 唯一的手牌干扰就打不出来（[7:59:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=28740s)）。
- 最后一回合 Rare Candy 进化 Dusknoir：Cursed Blast 收一只 Zoroark ex，Powerful Hand 收另一只，一回合拿 4 张（[8:02:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=28920s)）。

### 第 2 局：Lepine 胜

- Pecharunt ex 加 Binding Mochi 第 1 回合就收掉了 Łaszkiewicz 前场的 Budew，这局很快结束，细节没看清。

### 第 3 局：Łaszkiewicz 胜

- 同样的打法：不击倒，最后一回合用 Dusclops 和 Powerful Hand 收两只 Zoroark ex（[8:21:30](https://www.youtube.com/watch?v=iEM8bQbnA90&t=30090s)）。
- 他的 Patrat 让 Lepine 的 Munkidori 挪不了指示物。

### 对照手册

alakazam-dusknoir.md 的 vs N's Zoroark（46.7%）说中的：我方每只都是一击倒，对方一回合拿 1 张；6 张是两只 Zoroark ex 加 2 只单奖；Dusknoir 提前放好，Cursed Blast 不靠手牌；Binding Mochi 加 40。

写进手册的（PR #32）：

1. 防 Special Red Card 的拿奖节奏：拿到第 2 张后停在 4 张，最后一回合一次拿 4 张（登记成判断 akd-zor-01，信心 60%）。Lepine 没带 Judge，对方有 Judge 时停手期间手牌照样会被打乱。
2. "Patrat 在本对局没用"改成看对方卡表：Watchtower 版（3 到 4 张）里 Patrat 是空位；Lepine 这样的 N's Castle 版常常不带 Watchtower，Patrat 能关掉 Munkidori。
3. 解说讲的 Special Red Card 条件（对手剩 3 张以下才能打）和 dragapult-ex.md、alakazam-dusknoir.md 一致，crustle-dri.md 里写成"你拿了 3 张以后"的两处改正了。

n-zoroark.yaml 也补了这一场的录像证据（Lepine 一方）。
