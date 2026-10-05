# Melbourne 2026 区域赛复盘

比赛 2026-05-23，环境 TEF-POR（比现在少 CRI、PBL、30C 三个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-05-23_550_regional-melbourne。八强：Sasaki（Dragapult ex，冠军）、Murphy（Dragapult ex，亚军）、Takemasa（Dragapult Dusknoir）、Akita（Ogerpon Meganium Arboliva）、Krishnan（Raging Bolt Ogerpon）、Kasai（Dragapult ex）、Kodama（Basic Box）、Golding（Dragapult Blaziken）。看了决赛和一场四强，另外看了第 1 天第 6 轮 Kwak（Slowking）对 Palmer（Festival Lead）；直播里的八强 Akita 对 Krishnan 两边都不在我们的推荐卡组里，没看。

做法：没有调用 API，在你电脑上看截图、对照解说写成。Melbourne 的直播记分牌没有奖赏卡读数，奖赏卡数取自解说。

判断台账（data/judgments/）：决赛是 Dragapult ex 镜像，对照了 dpx-mir-01（Budew 互锁物品时先保住自己能用物品），两局都没出现互锁，记 n/a，见 data/judgments/sources/2026-10-05_video_melbourne-2026.yaml。四强是 Dragapult ex 对 Dragapult Dusknoir，第 1 天第 6 轮是 Slowking 对 Festival Lead，这两个对局之前都没有登记判断。这次写进手册的关键判断登记成了新判断，编号写在"写进手册的"里。

## 决赛：Sasaki（Dragapult ex）2-0 Murphy（Dragapult ex）

视频：https://www.youtube.com/watch?v=QiiKAduK9HE （26 分钟，两局完整）。两人都是手册主线（4 张 Crushing Hammer）。Hiromu Sasaki：2 张 Budew、Dawn、1 张 Watchtower、9 个能量（3 张 Darkness）；Gareth Murphy：1 张 Budew、2 张 Watchtower、10 个能量，没有 Dawn。第 1 局的记分牌把两人的名字放反了，解说中途更正；两局都是左边 Sasaki（黄色卡套）。

### 第 1 局：Sasaki 胜

- Sasaki 先攻，起手只有 Fezandipiti ex 在战斗场，贴 Darkness 结束。Murphy 用 Budew 锁物品，后备区铺了两只 Dreepy 和 Munkidori。
- Sasaki 用 Crispin 凑齐 3 个能量，Cruel Arrow（对手任意一只 100）收掉一只 Dreepy（[4:00](https://www.youtube.com/watch?v=QiiKAduK9HE&t=240s)）。
- Murphy 用 Crushing Hammer 拆掉 Fez 的 Darkness，并且放弃锁物品，改用 Munkidori 的 Mind Bend 让 Fez 混乱（[7:00](https://www.youtube.com/watch?v=QiiKAduK9HE&t=420s)）。
- Sasaki 两次混乱判定都是正面，Cruel Arrow 先后收掉 Drakloak 和最后一只 Dreepy 线（[7:30](https://www.youtube.com/watch?v=QiiKAduK9HE&t=450s)、[9:00](https://www.youtube.com/watch?v=QiiKAduK9HE&t=540s)）。Murphy 投降，这一局 Sasaki 没放下 Dragapult ex。

### 第 2 局：Sasaki 胜

- Murphy 选后攻，第 1 回合 Judge 加 Itchy Pollen（[14:45](https://www.youtube.com/watch?v=QiiKAduK9HE&t=885s)）。
- Sasaki 打出 Dawn，不用物品就从牌库拿到 Munkidori、Drakloak 和 Dragapult ex（[16:30](https://www.youtube.com/watch?v=QiiKAduK9HE&t=990s)）。解说："这张 Judge 适得其反。"
- Sasaki 立起三条进化线，Phantom Dive 一次收两只 Dreepy；他的 Watchtower 封住了 Murphy 的 Meowth ex（[21:00](https://www.youtube.com/watch?v=QiiKAduK9HE&t=1260s)）。
- Murphy 的 Crushing Hammer 整个系列都是反面，Sasaki 收尾（[25:30](https://www.youtube.com/watch?v=QiiKAduK9HE&t=1530s)）。

### 对照手册

dragapult-ex.md 镜像一节说中的：保住自己能用物品比锁住对手更重要；Judge 会把自己也打乱（这一局是对手的 Judge 帮了 Sasaki）；Hammer 先拆 Darkness；Watchtower 封 Meowth ex。

写进手册的（PR #31）：

1. 镜像一节新加这一场：Fezandipiti ex 的 Cruel Arrow 也是开局武器，后备区的 Dreepy（70）和 Drakloak（90）都是一击；对手的 Mind Bend 混乱要抛反面才挡得住。
2. 第 1 回合的 Judge 碰上 Dawn 会适得其反：Dawn 是支援者，被锁物品也能找齐三条进化。Dawn 在四场比赛 279 份 Dragapult 卡表里只有 10 份带，没有建议加进核心。
3. 没写进手册的：两局都是先攻的 Sasaki 赢，只有一场，不改先后攻的写法。

dragapult-ex.yaml 也补了这一场的录像证据。

## 四强：Murphy（Dragapult ex）2-1 Takemasa（Dragapult Dusknoir）

视频：第 2 天直播 https://www.youtube.com/watch?v=rHifbhgkGpw&t=24000s （约 6:40-7:59）。Shun Takemasa 的 Dragapult Dusknoir：2-2-1 Duskull 线、2 只 Munkidori、2 张 Budew、2 张 Rare Candy、Rosa's Encouragement、Judge、Unfair Stamp、2 张 Watchtower，只有 2 个 Darkness，没有 Crushing Hammer 和 Patrat。Murphy 的卡表见决赛一节。

### 第 1 局：Murphy 胜

- Murphy 先用 Itchy Pollen 加 Munkidori 收掉对方的 Budew，赢下 Budew 之争（[6:46:00](https://www.youtube.com/watch?v=rHifbhgkGpw&t=24360s)）。
- 之后 Boss's Orders 拉出 Drakloak，Phantom Dive 击倒，指示物收掉最后一只 Dreepy（[6:49:00](https://www.youtube.com/watch?v=rHifbhgkGpw&t=24540s)）。Takemasa 场上只剩 Munkidori 和 Duskull，投降。

### 第 2 局：Takemasa 胜

- Murphy 先攻（解说只说 Murphy 调度；Takemasa 第 1 回合就打了 Judge 和 Itchy Pollen，后攻方才能这样做），用 Buddy-Buddy Poffin 放了两只 Dreepy，没放 Budew。
- Takemasa 第 1 回合 Judge 加 Itchy Pollen（[7:01:00](https://www.youtube.com/watch?v=rHifbhgkGpw&t=25260s)），后来又打 Unfair Stamp，再换回 Budew 锁物品（[7:05:30](https://www.youtube.com/watch?v=rHifbhgkGpw&t=25530s)）。
- Murphy 手里几乎全是物品，只能放下 Fezandipiti ex 抽牌。Takemasa 用 Boss's Orders 拉出 Fez，Munkidori 挪 3 个指示物加 Dusclops 自爆放 5 个，一回合拿 3 张收尾（[7:17:30](https://www.youtube.com/watch?v=rHifbhgkGpw&t=26250s)）。

### 第 3 局：Murphy 胜

- Murphy 用 Fez 抽到 Boss's Orders，拉出带能量的 Drakloak 击倒，指示物收掉后备区 60 HP 的 Duskull（[7:30:30](https://www.youtube.com/watch?v=rHifbhgkGpw&t=27030s)）。
- Crushing Hammer 正面，拆掉对方 Munkidori 的 Darkness（[7:34:30](https://www.youtube.com/watch?v=rHifbhgkGpw&t=27270s)）。
- 等 Takemasa 把手牌攒起来，Murphy 才打 Judge，接着打 Risky Ruins（[7:41:30](https://www.youtube.com/watch?v=rHifbhgkGpw&t=27690s)）。
- Takemasa 只能用 Rosa's Encouragement 补能量，Murphy 最后用 Boss's Orders 收尾（[7:57:30](https://www.youtube.com/watch?v=rHifbhgkGpw&t=28650s)）。赛后 Takemasa 说他手里一直有 Meowth ex，被 Murphy 的 Watchtower 封着用不了。
- 这一局 Murphy 被 Mind Bend 混乱时赌了一次硬币，反面，自己吃 30。

### 对照手册

dragapult-ex.md 的 vs Dragapult Dusknoir（55.5%）说中的：先收 Duskull；防法二"Fezandipiti ex / Meowth ex 别留在后备区"（第 2 局就是这样输的）；Munkidori 要有 Darkness 才有用，Hammer 先拆它；Judge 别早打（第 3 局等对手手牌攒起来再打，有效）。

写进手册的（PR #31）：

1. 开局：先攻时第 1 回合就把 Budew 放上场，Buddy-Buddy Poffin 能同时放 Budew 和 Dreepy（登记成判断 dpx-dpd-01，信心 60%）。第 2 局 Murphy 只放了 Dreepy，被锁了两次物品；LA 四强 Hedrick 先攻第 1 回合就放下 Budew，见 los-angeles-2026.md。
2. 我方 Watchtower 也封得住对手的 Meowth ex（第 3 局）。
3. 防法二和 Judge 那两条各加了这一场作例子；常见失误加一条"被 Mind Bend 混乱时赌硬币"，撤到 Budew 就能解除（镜像一节 Hedrick 的做法）。
4. 没写进手册的：对手的能量被 Hammer 拆光后用 Rosa's Encouragement 补回 2 个，手册已经写了。

dragapult-ex.yaml 和 dragapult-dusknoir.yaml 也补了这一场的录像证据。

## 第 1 天第 6 轮：Kwak（Slowking）2-1 Palmer（Festival Lead）

视频：第 1 天直播 https://www.youtube.com/watch?v=xiA34-ViCgc&t=8700s （约 2:25-3:12）。按比赛数据第 6 轮第 3 桌的对阵确认是 Myeongsub Kwak（卡表上写作 Sobi Kwak），最终第 9。那时还没有 Metagross（CRI），Kwak 的复制来源是 2 只 Kyurem、Spectrier（ASC 98）、Haxorus（BLK 70）、Cofagrigus（WHT 40）、SSP 100 版 Annihilape，另带 Genesect（SFA 40）、3 张 Powerglass、4 张 Academy at Night，没有 Prime Catcher。Declan Palmer 最终第 75，他的 Festival Lead 带 Shaymin、1 只 Rellor 和 1 只 Rabsca、Tool Scrapper、2 张 Black Belt's Training、2 张 Brave Bangle、Lana's Aid。

### 第 1 局：Kwak 胜

- 双方来回换场地。Academy at Night 留在场上时，Dipplin 只能打一次，战斗场的 Kangaskhan 没事。
- Genesect 挂上道具后，Palmer 打不出 ACE SPEC（他的卡表里是 Secret Box）。
- 关键一步：Kwak 复制 Cofagrigus 的 Extended Damagriiigus，把自己后备区一只宝可梦身上的 8 个指示物挪到 Palmer 后备区的 Shaymin 上，收掉它（Flower Curtain 只挡伤害，挡不住指示物）；下回合 Kyurem 的 Trifrost 清场（[2:43:00](https://www.youtube.com/watch?v=xiA34-ViCgc&t=9780s)）。
- Kwak 起手把 Spectrier 放上了场，这一局复制不到它。

### 第 2 局：Palmer 胜

- Tool Scrapper 拆掉 Genesect 的道具，Lana's Aid 把 Shaymin 拿回来。
- Black Belt's Training 加 Brave Bangle，两次 Do the Wave 击倒战斗场的 Mega Kangaskhan ex，一次拿 3 张（[3:04:30](https://www.youtube.com/watch?v=xiA34-ViCgc&t=11070s)）。

### 第 3 局：Kwak 胜

- 复制 Spectrier 的 Phantasmal Barrage，12 个指示物收掉 Shaymin（[3:09:30](https://www.youtube.com/watch?v=xiA34-ViCgc&t=11370s)）。
- Trifrost 连续两次清场，Palmer 只剩 Psyduck。

### 对照手册

slowking-scr.md 的 vs Festival Lead（49.0%）说中的：核心是 Academy at Night 盖掉 Festival Grounds、先拆 Shaymin 和 Rabsca；Academy at Night 在场时 Dipplin 只能打一次；Kangaskhan 会被一回合打掉送 3 张；Tool Scrapper 会拆道具。

写进手册的（PR #33）：

1. 拆 Shaymin 不只有 Prime Catcher：Spectrier（ASC 98）放 12 个指示物、WHT 40 版 Cofagrigus 挪指示物，在后备区就能收掉它。Rabsca 在场时这条路不通（Spherical Shield 连招式的效果也挡），这一场 Palmer 一直没进化出 Rabsca。"有 Shaymin、没有 Rabsca 时先收 Shaymin，下回合再 Trifrost"登记成判断 slk-fes-01，信心 60%。现在的卡表里这两只复制来源各只有 2 份（103 份）；SSP 83 版 Cofagrigus 只放 6 个，一下收不掉 Shaymin。
2. 开局一条加上 Black Belt's Training：加 Brave Bangle 是 170×2 = 340，Kangaskhan 一回合就倒（第 2 局）。现在的 Festival Lead 卡表 51 份里只有 2 份带它，Kieran（48 份）加 Bangle 也有 320。常见失误加了对应的一条。
3. 复制工具箱加了 Cofagrigus（WHT 40）、Spectrier（ASC 98）、Haxorus（BLK 70）三行；通用部分加一条：复制来源别在开局放上场。

没写进手册的：Genesect（SFA 40）挂道具能封对手的 ACE SPEC，但现在的 Slowking 卡表一份都没带它，Festival Lead 又多半带 Tool Scrapper（51 份里 35 份）。

slowking-scr.yaml 和 festival-lead.yaml 也补了这一场的录像证据。
