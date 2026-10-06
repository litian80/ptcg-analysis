# Prague 2026 区域赛复盘

比赛 2026-04-25，环境 TEF-POR（比现在少 CRI、PBL、30C 三个系列），是轮换后的第一个大赛，下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-04-25_539_regional-prague。直播播了决赛圈的四场，都已看完：决赛 Łaszkiewicz（Dragapult Dudunsparce，冠军）2-0 Tresp（Crustle），四强 Łaszkiewicz 2-1 Kosek（Cynthia's Garchomp）、Tresp 2-1 Pires（Mega Starmie Dusknoir），八强 Tresp 2-0 Reklev（Dragapult ex，瑞士轮第一）。

做法：没有调用 API，在你电脑上看截图、对照解说写成。奖赏卡数取自解说。

判断台账（data/judgments/）：八强两局对照了 cru-dpx-01（Hero's Cape 挂 Crustle），都成立；决赛两局对手带 Dudunsparce ex，记 n/a，并给 cru-dpx-01 加了"对手没有 Dudunsparce ex 时"的限定。见 data/judgments/sources/2026-10-05_video_prague-2026.yaml。这次写进手册的关键判断登记成了新判断，编号写在"写进手册的"里；两条还不够把握的打法记成了待验证的论点。

## 决赛：Łaszkiewicz（Dragapult Dudunsparce）2-0 Tresp（Crustle）

视频：https://www.youtube.com/watch?v=vXSSxUzwDOE 。Mateusz Łaszkiewicz 的 Dragapult：1 张 Dudunsparce ex、2 只 Dunsparce 和 2 只 Dudunsparce、Hero's Cape、2 张 Risky Ruins、1 只 Budew，没有 Crushing Hammer，也没有 Unfair Stamp。Elmar Tresp 的 Crustle：只有 2 张 Mega Kangaskhan ex，另带 Cornerstone Mask Ogerpon ex、2 张 Colress's Tenacity、Super Potion，没有 Eri、Handheld Fan 和 Special Red Card，场地只有 Team Rocket's Factory 和 Forest of Vitality 各 1 张。

### 第 1 局：Łaszkiewicz 胜

- Łaszkiewicz 先把 Hero's Cape 挂在 Dunsparce 上（170），进化成 Dudunsparce ex 就是 370（[2:00](https://www.youtube.com/watch?v=vXSSxUzwDOE&t=120s)）。这只 Dunsparce 受伤后，他用 Run Away Draw 把它连 Cape 一起洗回牌库。
- Phantom Dive 加 Munkidori 收掉 Tresp 起手的 Cornerstone Mask Ogerpon ex。
- Dudunsparce ex 的 Destructive Drill 每回合 150，打穿了 Mysterious Rock Inn（[12:00](https://www.youtube.com/watch?v=vXSSxUzwDOE&t=720s)）。Tresp 用两张 Jumbo Ice Cream 回血也跟不上。

### 第 2 局：Łaszkiewicz 胜

- Tresp 起手 Mega Kangaskhan ex，被 Budew 锁物品困在前场；Łaszkiewicz 的 Dudunsparce ex 在奖赏卡里。
- Risky Ruins 加 Phantom Dive 收掉一只没进化的 Dwebble，拿到的奖赏卡正好是 Dudunsparce ex；下一回合击倒 Kangaskhan，拿 3 张（[26:00](https://www.youtube.com/watch?v=vXSSxUzwDOE&t=1560s)）。
- Tresp 叠了两张 Spiky Energy。最后一次 Drill 击倒 Crustle，反伤 40 也击倒了 Dudunsparce ex，双方同时倒下（[39:30](https://www.youtube.com/watch?v=vXSSxUzwDOE&t=2370s)）。Łaszkiewicz 只差 1 张，Tresp 投降。

### 对照手册

crustle-dri.md 的 vs Dragapult ex（68.6%）说中的：Mega Kangaskhan ex 是最大的奖赏卡漏洞；对手打出 Risky Ruins 后还在铺 Dwebble 会送奖赏卡（第 2 局还因此帮对手拿出了 Dudunsparce ex）。dragapult-ex.md 的 vs Crustle（26.1%）说中的：Crustle 多时加 Dudunsparce ex；Kangaskhan 一上前场就收；先打 Dwebble。

台账：cru-dpx-01 两局都是 n/a。第 1 局 Tresp 没把 Cape 挂上场；第 2 局他抽到了 Cape（[25:30](https://www.youtube.com/watch?v=vXSSxUzwDOE&t=1530s)），但看不清挂在哪只上，而且对手的主攻是 150 的 Drill，不是这条判断说的小伤害。

写进手册的（PR #32）：

1. Dudunsparce ex 能打穿 Mysterious Rock Inn：两局都打穿了，有裁判在场、没有人提出异议，解说也明说。两本手册原来都写"推断，需裁定"，现在改成录像证据（没找到官方 Q&A）。
2. 对手带 Dudunsparce ex 时，Hero's Cape 改挂 Kangaskhan，让它当主攻（登记成判断 cru-dpx-02，信心 55%，是 cru-dpx-01 的备选路线）。依据主要是下面四强对 Starmie 那场；这一场 Tresp 没这样打，0-2。cru-dpx-01 加了"对手没有 Dudunsparce ex 时"的限定。
3. 两张 Spiky Energy 让 Drill 每次反吃 40，两本手册都写了。Crustle 一方"改贴第二张 Spiky"只有这一局，记成待验证的论点。
4. crustle-dri.md 开局那条加了：先攻起手 Kangaskhan 时，对手后攻第 1 回合就能用 Budew 锁物品，Switch 打不出来，Kangaskhan 可能被困在前场。"第 1 回合就用 Switch 换上 Dwebble"记成待验证的论点。
5. 没写进手册的：Hero's Cape 挂在 Dunsparce 上、用 Run Away Draw 回收受伤的 Dunsparce，是这份卡表的细节，手册主线不带 Dudunsparce ex 和 Hero's Cape；Crustle 在现在的环境份额约 3%，只写成备注。

## 四强：Łaszkiewicz（Dragapult Dudunsparce）2-1 Kosek（Cynthia's Garchomp）

视频：https://www.youtube.com/watch?v=C_ttAu7bOcE （KFhDQLBjwbw 是同一场的转载）。简要记录，只按字幕读了。Cynthia's Garchomp 不在我们的推荐卡组里，手册没有这一节。

- 第 1 局 Kosek 胜：Łaszkiewicz 的 Hero's Cape 在奖赏卡里。三只 Cynthia's Roserade 每只给 Garchomp 加 30，一击打倒 Dragapult ex。
- 第 2 局 Łaszkiewicz 胜：他专打加伤的 Roserade（[32:00](https://www.youtube.com/watch?v=C_ttAu7bOcE&t=1920s)），Garchomp 就够不到一击线了。
- 第 3 局 Łaszkiewicz 胜：拿到 Hero's Cape 后 Dragapult ex 有 420 HP，Garchomp 加满也只有 410，打不倒（[55:00](https://www.youtube.com/watch?v=C_ttAu7bOcE&t=3300s)）。

没有改手册，也没有要记的台账。备忘：对 Garchomp 先打 Roserade；我们的主线不带 Hero's Cape，这个对局的一击线更危险（推断）。

## 四强：Tresp（Crustle）2-1 Pires（Mega Starmie Dusknoir）

视频：第 2 天直播 https://www.youtube.com/watch?v=5ewTXCpaGpA&t=16500s （约 4:35-5:37，赛后有 Tresp 的采访）。João Pires 的卡组：2 只 Mega Starmie ex、Dusknoir 线（4-3-2）、2 只 Munkidori、Budew、Bloodmoon Ursaluna ex，2 张 Ignition Energy、3 张 Risky Ruins、Wally's Compassion。

对手怎么打穿 Crustle：Mega Starmie ex 的 Nebula Beam（210）不受效果影响，穿过 Mysterious Rock Inn；Ignition Energy 让 Starmie 一上场就能打；再加 Cursed Blast。解说说"专门打 Crustle 的卡组大概就长这样"。

### 第 1 局：Tresp 胜

- Tresp 不再指望 Crustle，用 Team Rocket's Petrel 拿 Hero's Cape 挂在 Mega Kangaskhan ex 上（400），让 Kangaskhan 当主攻（[4:45:00](https://www.youtube.com/watch?v=5ewTXCpaGpA&t=17100s)）。
- Rapid-Fire Combo 两下收掉 Starmie（3 张）。Spiky Energy 让 Nebula Beam 吃了反伤；两张 Jumbo Ice Cream 回了 160。
- Pires 用两次 Cursed Blast 收掉 Kangaskhan，但 Tresp 只差 1 张。他用 Boss's Orders 把 Duskull 拉到前场拖时间，最后用 Boss 拿下（[4:55:30](https://www.youtube.com/watch?v=5ewTXCpaGpA&t=17730s)）。

### 第 2 局：Pires 胜

- Tresp 的 Cape 在奖赏卡里，Nebula Beam 击倒 Crustle。
- 解说指出 Pires 漏了一步：两次 Cursed Blast 加 50 就能直接收掉后备区的 Kangaskhan。
- Tresp 后来三次正面 350 收掉 Starmie，但 Pires 用 Wally's Compassion，再用两次 Cursed Blast 加 Bloodmoon Ursaluna ex 收尾。

### 第 3 局：Tresp 胜

- Cape 挂上 Kangaskhan，Switch 换到前场，三次正面 350 击倒 Starmie（[5:23:30](https://www.youtube.com/watch?v=5ewTXCpaGpA&t=19410s)）。
- 解说算过：Nebula Beam 210 加一次 Cursed Blast 130 是 340，打不倒 400。最后 Boss 拉出 Meowth ex 收尾。

### 对照手册

crustle-dri.md 没有 Starmie 一节（世界赛后份额约 1%），不单开，也没有要记的台账。

写进手册的（PR #32）：

1. 这场是 cru-dpx-02 的主要依据：对手的主攻能穿过 Mysterious Rock Inn 时，Hero's Cape 改挂 Kangaskhan，让它当主攻。Cape 挂上 Kangaskhan 的两局都赢，Cape 在奖赏卡里的一局输。Tresp 在采访里说，他赛前不了解这副牌，是朋友说 Zander 用 Kangaskhan 攻击赢过一局，他才照做的。

只记录：Boss 拉对手的 Duskull 到前场拖回合、拿最后 1 张；前场的 Kangaskhan 贴 Spiky。

## 八强：Tresp（Crustle）2-0 Reklev（Dragapult ex）

视频：第 2 天直播 https://www.youtube.com/watch?v=5ewTXCpaGpA&t=12720s （约 3:32-4:21）。Tord Reklev 是瑞士轮第一，卡表没有 Crushing Hammer 和 Dudunsparce ex，带 3 张 Rare Candy、Bloodmoon Ursaluna ex、Chien-Pao、Latias ex。

### 第 1 局：Tresp 胜，Reklev 只拿到 1 张

- Reklev 用 Boss's Orders 拉出 Tresp 后备区一只没能量的 Dwebble 收掉，这是他唯一的 1 张。
- Tresp 把 Cape 挂在 Crustle 上（250），贴上 Mist（[3:37:00](https://www.youtube.com/watch?v=5ewTXCpaGpA&t=13020s)）。之后 Superb Scissors 每回合收一只 Drakloak 或 Munkidori，Boss 拉后备区带能量的。
- 前场贴 Spiky，Budew 的 Itchy Pollen 每次都吃反伤。Reklev 投降时手里是三张 Dragapult ex、三张 Boss。

### 第 2 局：Tresp 胜

- Tresp 起手 Kangaskhan，Reklev 拿了 4 张（Dwebble 和 Kangaskhan）。
- 但 Cape 加 4 张 Growing Grass 的 Crustle 有 330（[4:16:30](https://www.youtube.com/watch?v=5ewTXCpaGpA&t=15390s)），Reklev 打不穿；Tresp 收掉两只 Munkidori 赢下。解说："送掉的 4 张都无所谓。"

### 对照手册

crustle-dri.md 的 vs Dragapult ex（68.6%）说中的：Hero's Cape 挂 Crustle；先 Boss 收 Munkidori、Drakloak 这些 1 张的引擎；Spiky 让 Budew 自伤；后备区的 Crustle 先贴 Mist。

台账：cru-dpx-01 两局都成立（held）。

写进手册的（PR #32）：

1. crustle-dri.md 的 cru-dpx-01 那条加了这一场，并写明分界线：对手没有 Dudunsparce ex 时，一只挂 Cape、堆满 Growing Grass 的 Crustle 就够了，送 4 张也无妨；有 Dudunsparce ex 时见 cru-dpx-02。
2. dragapult-ex.md 的 vs Crustle 在 Crushing Hammer 那条补了反面例子：没有 Hammer、也没有 Dudunsparce ex 时，330 的 Crustle 打不穿。

crustle-dri.yaml 和 dragapult-ex.yaml 也补了 Prague 的录像证据。
