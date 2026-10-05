# Los Angeles 2026 区域赛复盘

比赛 2026-05-09，环境 TEF-POR（比现在少 CRI、PBL、30C 三个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-05-09_558_regional-los-angeles-ca。八强：Hedrick（Dragapult ex，冠军，后来的世界冠军）、Pitcher（Dragapult Dudunsparce，亚军）、Moffitt、Rutledge（都是 Dragapult Dusknoir）、Obernolte（Mega Lopunny Dudunsparce）、Phelan（Lucario Hariyama）、De Velasco（Dragapult ex）、Marzan（Raging Bolt Ogerpon）。看了决赛和一场四强；八强 Moffitt 对 Phelan 两边都不在我们的推荐卡组里，没看。

做法：没有调用 API，在你电脑上看截图、对照解说写成。两场都是左边对手、右边 Hedrick。

判断台账（data/judgments/）：决赛按镜像对照了 dpx-mir-01，两局都没出现 Budew 互锁，记 n/a，见 data/judgments/sources/2026-10-05_video_los-angeles-2026.yaml。四强的对局（Dragapult ex 对 Dragapult Dusknoir）之前没有登记判断。这次写进手册的关键判断登记成了新判断，编号写在各场的"写进手册的"里。

## 决赛：Hedrick（Dragapult ex）2-0 Pitcher（Dragapult Dudunsparce）

视频：https://www.youtube.com/watch?v=m8np08cT-TQ 。Andrew Hedrick 是手册主线（4 张 Crushing Hammer）。Jack Pitcher 的 Dragapult Dudunsparce 也是 Dreepy 线加 Munkidori，带 2 张 Rare Candy，没有 Hammer；这个变体在 LA 有 99 人用，世界赛之后的四场比赛里每场只有 3 到 18 人，手册把它算在镜像里。

### 第 1 局：Hedrick 胜

- Hedrick 手里没有 Lillie's Determination，先打 Risky Ruins，用 Crispin 给 Munkidori 贴 Darkness，Mind Bend 击倒 Dunsparce（[8:00](https://www.youtube.com/watch?v=m8np08cT-TQ&t=480s)）。
- 下一回合 Munkidori 把我方身上 Ruins 放的 20 挪到对方 Drakloak 上，Drakloak 的 Dragon Headbutt 70 加 20 正好 90，击倒对方的 Drakloak（[13:30](https://www.youtube.com/watch?v=m8np08cT-TQ&t=810s)）。Pitcher 以为 Hedrick 没有 Rare Candy、Drakloak 是安全的，第 2 回合就投降。

### 第 2 局：Hedrick 胜

- Hedrick 起手 Budew（撤退费 0，省下一次手贴）。Pitcher 上回合没贴能量，Hedrick 用 Crushing Hammer 拆掉他唯一的 Fire，再打 Judge 加 Itchy Pollen（[22:30](https://www.youtube.com/watch?v=m8np08cT-TQ&t=1350s)）。
- 第一次攻击用 Jet Headbutt，不用 Phantom Dive（[29:00](https://www.youtube.com/watch?v=m8np08cT-TQ&t=1740s)）。解说说这是不给对手的 Munkidori 送弹药。
- Pitcher 用 Unfair Stamp 加 Phantom Dive 反扑。Hedrick 第二次因为出牌太慢（Pace of Play）被判罚，Pitcher 直接多拿 2 张（Double Prize Penalty，[36:00](https://www.youtube.com/watch?v=m8np08cT-TQ&t=2160s)），只差 1 张。
- Hedrick 两张 Crushing Hammer 都是正面：先拆对手 Munkidori 的 Darkness，再拆 Drakloak 的 Fire（[42:30](https://www.youtube.com/watch?v=m8np08cT-TQ&t=2550s)）。然后 Unfair Stamp，放下 Meowth ex 找 Crispin，Phantom Dive 一回合拿 3 张；最后撤到自己的 Munkidori，用 Adrena-Brain 挪完指示物再 Mind Bend 收尾（[47:30](https://www.youtube.com/watch?v=m8np08cT-TQ&t=2850s)）。

### 对照手册

dragapult-ex.md 镜像一节说中的：Hammer 先拆 Munkidori 的 Darkness；Judge 在对手被锁物品时打才有用（和 Melbourne 决赛那张适得其反的 Judge 正好一正一反）；被 Mind Bend 混乱时撤回去解除；Risky Ruins 先削对手。

写进手册的（PR #31）：

1. 镜像一节新加这一场：有 Risky Ruins 时 Drakloak 不安全，Ruins 的 20 加 Dragon Headbutt 70 正好是 90，不用 Rare Candy，第 2 回合就能打。
2. 对手的 Munkidori 有 Darkness 能量时，没有击倒目标就别用 Phantom Dive 撒指示物，先用 Jet Headbutt（登记成判断 dpx-mir-02，信心 60%）：Adrena-Brain 从对手自己的宝可梦挪指示物，我们没打死的指示物就是它的弹药。
3. 没写进手册的：Hedrick 被判罚 2 张。Hammer 版要想的东西多，75 分钟的决赛也要注意出牌速度，这条只留在复盘里。

dragapult-ex.yaml 也补了这一场的录像证据。

## 四强：Hedrick（Dragapult ex）2-0 Rutledge（Dragapult Dusknoir）

视频：https://www.youtube.com/watch?v=HVAsRXDFn04 。Preston Rutledge 的 Dragapult Dusknoir：3 张 Rare Candy、Neo Upper Energy、只有 1 张 Crispin，没有 Crushing Hammer。

### 第 1 局：Hedrick 胜

- Rutledge 两只 Duskull 都在奖赏卡里。
- Hedrick 后攻，Budew 一直锁物品，Dreepy 留到回合最后才放。他三个回合都摸不到 Fire。
- 之后 Hammer 正面，拆掉 Rutledge 唯一的 Fire。Hedrick 打 Unfair Stamp，Phantom Dive 的指示物分散放、故意不击倒：对手没有宝可梦被击倒，Fezandipiti ex 抽不了牌，也打不了 Unfair Stamp（[18:30](https://www.youtube.com/watch?v=HVAsRXDFn04&t=1110s)）。Rutledge 投降。

### 第 2 局：Hedrick 胜

- Hedrick 先攻，第 1 回合用 Ultra Ball 拿 Budew，和两只 Dreepy 一起放下，第 2 回合起锁住对手的 3 张 Rare Candy（[25:00](https://www.youtube.com/watch?v=HVAsRXDFn04&t=1500s)）。
- Hammer 正面，拆掉唯一的 Fire；Phantom Dive 收掉 Duskull（[32:30](https://www.youtube.com/watch?v=HVAsRXDFn04&t=1950s)）。
- Rutledge 用 Lillie's Determination 和 Fez 找到 Rare Candy 反扑。Hedrick 又一次不击倒，把对方的 Fez 和 Meowth ex 都打进下一发的范围（[40:00](https://www.youtube.com/watch?v=HVAsRXDFn04&t=2400s)）。
- Hammer 正面，拆掉 Neo Upper；Boss's Orders 拉出 Meowth ex；最后 Munkidori 收尾（[49:30](https://www.youtube.com/watch?v=HVAsRXDFn04&t=2970s)）。

### 对照手册

dragapult-ex.md 的 vs Dragapult Dusknoir（55.5%）说中的：先收 Duskull；防法三 Hammer 打攻击能量（四次正面，三次拆掉唯一的攻击能量）；Budew 挡 Rare Candy（先攻也照锁）；防法二"Fezandipiti ex / Meowth ex 别留在后备区"（第 2 局对手正是这样被凑成一次 4 张）。

写进手册的（PR #31）：

1. 奖赏卡路线加了"故意不击倒"：对手可能握着 Unfair Stamp、后备区有 Fezandipiti ex 时，Phantom Dive 先不击倒，把指示物分到下一发能一次收两只的位置；对手的 Munkidori 有 Darkness 能量时不这样打（登记成判断 dpx-dpd-02，信心 60%）。镜像一节已有 Hedrick 世界赛四强的同一种打法。
2. 先攻也要放 Budew，是 dpx-dpd-01 的依据之一（见 melbourne-2026.md）。
3. 没写进手册的：Neo Upper Energy 是 Hammer 的最佳目标，但 92 份 Dragapult Dusknoir 卡表里只有 5 份带。

dragapult-ex.yaml 和 dragapult-dusknoir.yaml 也补了这一场的录像证据。
