# Indianapolis 2026 区域赛复盘

比赛 2026-05-30，环境 TEF-POR（比现在少 CRI、PBL、30C 三个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-05-30_559_regional-indianapolis-in。八强：Jones（Alakazam Dudunsparce，冠军）、Reddy（Crustle，亚军）、Newdorf（Dragapult Dusknoir）、Melville、Hamilton、Hedrick、Sakadjian、Lu（都是 Dragapult ex）。决赛圈直播只播了八强、四强、决赛各一场，都已看完；后来又看了直播里有推荐卡组的四场瑞士轮（第 2 天第 11、12、13 轮，第 1 天第 4 轮），放在后面。

做法：没有调用 API，在你电脑上逐张看截图、对照解说写成。决赛和八强用的是旧版侧边面板，工具读出的奖赏卡变化不全（决赛还切错了局数），拿奖时间按解说；四强用的是 Baltimore 那一款面板，读数和解说一致。

判断台账（data/judgments/）：决赛圈三场的对局当时还没有登记判断，没有要记的验证结果。台账里 Alakazam Dudunsparce 对 Dragapult 的三条判断说的是纯 Dragapult ex，四强的对手是 Dragapult Dusknoir，没有算进去。这次写进手册的关键判断登记成了新判断，编号写在各场的"写进手册的"里。瑞士轮第 12 轮是 Alakazam Dudunsparce 对纯 Dragapult ex，验证结果和第 13 轮发现的纠错记在 data/judgments/sources/2026-10-05_video_indianapolis-2026.yaml。

## 决赛：Jones（Alakazam Dudunsparce）2-0 Reddy（Crustle）

视频：https://www.youtube.com/watch?v=nlj_HY9SoJo 。Cerys Jones 的 Alakazam：Dedenne、Genesect、Psyduck、Fezandipiti ex，2 张 Enhanced Hammer、2 张 Handheld Fan、Sacred Ash、Lucky Helmet、Lana's Aid、4 张 Nighttime Mine。Rahul Reddy 的 Crustle 和 crustle-dri.md 的核心基本一致，差别是 4 张 Crushing Hammer、场地只有 1 张 Team Rocket's Factory、基本能量是 1 张 Fighting 而不是 Grass，另带 Cornerstone Mask Ogerpon ex 和 Psyduck。

### 第 1 局：Jones 胜

- Reddy 3 张 Growing Grass Energy 和 1 张 Mist Energy 在奖赏卡里，牌库里能提供草能量的只剩 1 张 Growing Grass。
- Jones 第 1 回合用 Telepathic Psychic Energy 拿出 Dedenne。Reddy 用 Superb Scissors 先拿 1 张，之后一直用 Boss's Orders 拉 Dedenne；Dedenne 挂着 Handheld Fan，被打时把 Reddy 攻击手身上的 1 个能量挪走。
- Jones 找到 Enhanced Hammer，用 Sacred Ash 把 Dedenne 洗回牌库；之后 Dedenne 的 Electromagnetic Sonar 每次都把 Hammer 捡回来，Reddy 每回合掉一个能量。
- Reddy 换上挂 Hero's Cape 的 Kangaskhan（400），没贴 Mist。Jones 手牌凑到 20 张，Powerful Hand 一击拿 3 张，Reddy 投降。

### 第 2 局：Jones 胜

- Reddy 给 Kangaskhan 挂上 Cape，用 Hilda 找到 Mist；他的两张 Crushing Hammer 都是反面。
- Jones 要同时凑齐 20 张手牌、一张 Enhanced Hammer 和撤退用的能量，差了一阵。Reddy 没有去击倒 Dedenne（复盘的理解：留着它当 Boss 的目标），又贴上第二张 Mist。
- Jones 一回合摸到两张 Enhanced Hammer，弃掉两张 Mist，Powerful Hand 一击 Kangaskhan，拿 3 张。

### 对照手册

Crustle vs Alakazam Dudunsparce（65.6%）说中的：Enhanced Hammer 决定这个对局（数据：对手带它 60.0%，不带 18.8%）；没贴 Mist 的 Kangaskhan 不能站战斗场；要备第二张 Mist。

写进手册的（PR #30）：

1. Dedenne 的 Electromagnetic Sonar 每回合捡回 Enhanced Hammer，两张 Hammer 就变成每回合都有，Eri 弃掉的也会被捡回；所以 Dedenne 是第一个要击倒的目标（登记成判断 cru-adu-01，信心 60%）。数据也支持：带 Dedenne 的 Alakazam 对 Crustle 56.2%（16 局），不带的 30.0%（20 局）。
2. Handheld Fan 挂在 Dedenne 上会挪走攻击手的能量；但数据里带 Fan 的 Alakazam 对 Crustle 反而更差（25.5% 对 56.1%），两样都写了。
3. 挂 Hero's Cape 的 Kangaskhan 只是把门槛从 15 张提到 20 张，这两局都被凑到了；两张 Mist 也挡不住一回合两张 Hammer。
4. Enhanced Hammer 弃的是特殊能量：Growing Grass、Mist、Spiky 都是，只有基本 Grass Energy 弃不掉。
5. 没写进手册的：复盘建议"Growing Grass 被压在奖赏卡里时，改靠 Pokémon Center Lady 和 Jumbo Ice Cream 撑"，这是奖赏卡运气下的应变，不是这个对局特有的打法。

crustle-dri.yaml 和 alakazam-dudunsparce.yaml 也补了这一场的录像证据。

## 四强：Jones（Alakazam Dudunsparce）2-0 Newdorf（Dragapult Dusknoir）

视频：https://www.youtube.com/watch?v=bnVzhTKp3jg （474 帧读出 359 帧，和解说一致）。Justin Newdorf 的 Dragapult Dusknoir：3 只 Dragapult ex、3 张 Crushing Hammer、Unfair Stamp、2 张 Watchtower，没有 Judge 和 Special Red Card。Jones 的卡表见决赛一节。括号里是剩余奖赏卡，Newdorf 在前。

### 第 1 局：Jones 胜

- Jones 的 Psyduck（Damp 关掉 Cursed Blast）一开始在奖赏卡里；Kadabra 击倒一只宝可梦时正好把它拿了出来（6/5）。
- Newdorf 三次用 Cursed Blast 清 Abra，每次都送 1 张；Jones 打出 Nighttime Mine，用 Lana's Aid 捡回 Abra。
- Newdorf 把 Watchtower 留到关键回合才打，顶掉 Nighttime Mine，Phantom Dive 一次击倒 Alakazam 和 Abra（3/2）。
- 他摸不到 Crispin，三只 Dragapult ex 有两只在奖赏卡里，接不上第二只。Jones 手牌养到 30 张左右，用 Nighttime Mine 加 Boss's Orders 拿下最后 2 张。

### 第 2 局：Jones 胜

- Jones 每次都先给 Genesect 挂上道具再击倒，Newdorf 一次 Unfair Stamp 也打不出来；Psyduck 放在后备区，关掉 Cursed Blast。
- Newdorf 没有 Judge 和 Special Red Card，压不住 Jones 的手牌。Jones 每回合拿 1 张（5/1），拿下。

### 对照手册

Dragapult ex vs Alakazam Dudunsparce（60.4%）说中的：场地之争（Watchtower 能顶掉 Nighttime Mine）；Genesect 挂道具封住 Unfair Stamp；要靠 Judge、Special Red Card 控手牌。

写进手册的（PR #30）：

1. dragapult-ex.md 控手牌那条加了第 2 局作反面例子：只靠 Unfair Stamp、没有 Judge 和 Special Red Card，碰上先挂道具的 Genesect 就压不住对手手牌。手册主线的卡表带 Judge（279 份里 227 份），构筑不用改。
2. 关键卡 Watchtower 那条加了第 1 局：留到关键回合顶掉 Nighttime Mine，一发 Phantom Dive 拿 2 张。
3. Psyduck 关掉 Cursed Blast 只影响 Dusknoir 版，alakazam-dusknoir.md 和 dragapult-dusknoir.yaml 里已经有，没再加。

dragapult-dusknoir.yaml 和 alakazam-dudunsparce.yaml 也补了这一场的录像证据。

## 八强：Reddy（Crustle）2-0 Sakadjian（Dragapult ex）

视频：https://www.youtube.com/watch?v=rFR1ZVFc5ic （456 帧读出 386 帧，但记下的变化很少，时间按解说）。Noah Sakadjian 的 Dragapult ex 是手册的主线，多 2 张 Team Rocket's Watchtower，能量 9 个。

### 第 1 局：Reddy 胜

- Reddy 在战斗场的 Kangaskhan 上贴 Spiky Energy，Budew 每次 Itchy Pollen 都要吃 20。
- Sakadjian 打出 Watchtower 和 Judge。Watchtower 关掉 Kangaskhan 的 Run Errand，Reddy 唯一的场地 Team Rocket's Factory 在奖赏卡里，换不掉它。
- Reddy 把 Hero's Cape 挂在 Crustle 上（290 以上）。Sakadjian 的 Crushing Hammer 连着 4 次反面。
- 解说算过：Dragapult 一方大约要 5 个回合才打得穿挂 Cape 的 Crustle，而 Jumbo Ice Cream 每回合都能回血。Reddy 拿下。

### 第 2 局：Reddy 胜

- Reddy 两张 Growing Grass 在奖赏卡里。Sakadjian 一直拆 Mist（他不知道 Growing Grass 在奖赏卡里），Hammer 中了一次，主要靠 Munkidori 的 Mind Bend。
- Reddy 用 Petrel 找来 Eri，弃掉 Sakadjian 手里的 Unfair Stamp 和 Night Stretcher。他放弃战斗场那只 Crustle，把能量堆到后备区挂 Cape 的 Crustle 上。
- 后备区没贴 Mist 的 Crustle 吃到了 Phantom Dive 的指示物（累计 100），和手册说的一样；Jumbo Ice Cream 回血后，Superb Scissors 收掉 Dragapult ex。

### 对照手册

Crustle vs Dragapult ex（68.6%）说中的：ex 打不动 Crustle；Jumbo Ice Cream 回得比 Munkidori 磨得快；对手真正的办法只有 Crushing Hammer；后备区的 Crustle 要贴 Mist；只有一张场地时 Watchtower 很难受。

写进手册的（PR #30）：

1. crustle-dri.md 的 Budew 锁物品那条：战斗场贴 Spiky Energy，Itchy Pollen 每次反吃 20，30 HP 的 Budew 打两次就倒。
2. 新加两条：Hero's Cape 挂 Crustle（手册原来没说挂在谁身上，登记成判断 cru-dpx-01，信心 70%）；用 Eri 弃掉对手的 Unfair Stamp。
3. 构筑建议"至少 2 张场地"加了这一场作旁证。dragapult-ex.md 的 vs Crustle 也在 Crushing Hammer 那条补了这一场。

crustle-dri.yaml 和 dragapult-ex.yaml 也补了这一场的录像证据。

## 第 2 天第 12 轮：Jones（Alakazam Dudunsparce）2-0 Hamilton（Dragapult ex）

视频：第 2 天直播 https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=5340s （约 1:29-2:21）。Jones 的卡表见决赛：4 张 Nighttime Mine，没有 Battle Cage，也没有 Eri。Alex Hamilton 当时 11-0，最终第 5：主线 Hammer 版，1 张 Judge、1 张 Unfair Stamp，没有 Special Red Card。奖赏卡数取自解说。

### 第 1 局：Jones 胜

- Hamilton 先攻，把唯一的能量贴在战斗场的 Drakloak 上。Jones 第 2 回合用 Rare Candy 进化 Alakazam，Powerful Hand 收掉这只 Drakloak；同一回合她给 Genesect 挂上道具、打出 Nighttime Mine（[1:37:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=5820s)）。Hamilton 的 Unfair Stamp 从此打不出来。
- Hamilton 用 Risky Ruins 换掉 Nighttime Mine，Phantom Dive 拿 2 张（[1:42:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=6120s)）。
- Jones 用 Lana's Aid 把手牌攒到 19 张，收掉 Dragapult ex（[1:45:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=6300s)）；Lucky Helmet 挂在 Alakazam 上（[1:50:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=6600s)）。之后她还有 Nighttime Mine 可打，Hamilton 的 2 张 Ruins 换不过来。

### 第 2 局：Jones 胜

- 解说复盘说前两回合和第 1 局几乎一样（[2:18:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=8280s)）。Genesect 又封住 Unfair Stamp，解说说这张 Stamp 比 Crushing Hammer 还没用；Hamilton 只有一张 Judge 能压对手手牌，Crispin 用完后撑不住。
- 两局 Hamilton 都没用 Budew 锁物品。

### 对照手册

dragapult-ex.md 的 vs Alakazam Dudunsparce（60.4%）说中的：胜负手是场地；Nighttime Mine 在场时 Phantom Dive 要 3 个能量；Genesect 封住 Unfair Stamp 时要靠 Special Red Card 或 Tool Scrapper。继上面四强 Newdorf 之后，这是第二场没带就输的录像。

台账：adu-dpx-02（第 2 回合有没有 Rare Candy 基本决定这局）两局都记 held，从 40% 升到 55%，Hamilton 两局都没锁物品；adu-dpx-01（先放 Battle Cage）记 n/a，Jones 没带 Battle Cage，赛后说觉得它对 Dragapult 没多大用；dpx-adu-01（后攻吃亏）记 n/a，第 1 局 Hamilton 先攻也输了。

写进手册的（PR #34）：

1. dragapult-ex.md "胜负手是场地"那条：对手可能完全不带 Battle Cage、只带 4 张 Nighttime Mine（现在 62 份卡表里 8 份），2 张 Risky Ruins 换不过来，留给要打 Phantom Dive 的那一回合（推断）。
2. Genesect 那条补了这一场。
3. 常见失误加一条：对手第 2 回合可能 Rare Candy 进化出 Alakazam 时，别把唯一的能量贴在战斗场的 Drakloak 上。

alakazam-dudunsparce.yaml 和 dragapult-ex.yaml 也补了这一场的录像证据。

## 第 2 天第 13 轮：Hope（Ogerpon Meganium Hydrapple）2-0 Zheng（Dragapult ex）

视频：第 2 天直播 https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=9540s （约 2:39-3:29）。Cody Hope 最终第 10，卡表带 Celebi、Briar、Unfair Stamp、Fezandipiti ex、14 个基本草能量。Bulin Zheng 最终第 33：主线 Hammer 版，带 Moltres、Watchtower，只有 1 只 Budew。dragapult-ex.md 的 vs Ogerpon Meganium Hydrapple 一节，这是第一场录像。奖赏卡数取自解说。

### 第 1 局：Hope 胜

- Zheng 开局没用 Budew 锁物品，两张 Crushing Hammer 都是反面。Hope 用 Dipplin 拿第 1 张。
- Zheng 用 Boss's Orders 拉出 Teal Mask Ogerpon ex，Moltres 打 220 击倒（[2:54:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=10440s)）。
- Hope 下一回合打 Unfair Stamp，Hydrapple ex 上场。Meganium 在场，6 个基本草能量算 12 个，Syrup Storm 打出 390（[2:55:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=10500s)），解说也这样算。后来 Meganium 被收掉，Hope 用 Night Stretcher 拿回来，赢下这一局。

### 第 2 局：Hope 胜

- Zheng 用 Budew 锁了物品，Hope 用 Celebi 的 Traverse Time（招式，物品锁挡不住）照样找齐进化线（[3:08:30](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=11310s)）。
- Zheng 打出 Unfair Stamp、Risky Ruins 加 Phantom Dive（[3:21:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=12060s)）；Hope 用 Lana's Aid 补回能量，Teal Mask Ogerpon ex 打 330。
- Zheng 剩 2 张时，Hope 用 Fezandipiti ex 的 Flip the Script 抽到 Briar，收尾（[3:27:30](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=12450s)）。

### 对照手册

dragapult-ex.md 的 vs Ogerpon Meganium Hydrapple（62.9%）说中的：Moltres 打弱火的 Teal Mask Ogerpon ex 是 220，一击；Risky Ruins 换掉 Forest of Vitality；Crushing Hammer 对十几个基本草能量效果有限；Briar。

写进手册的（PR #34）：

1. 改正两处写反的地方：Syrup Storm 数的是对手（Hydrapple 一方）自己全场的草能量，手册写成了我方；Briar 是对手在我们剩 2 张时打的，手册写成了对手剩 2 张时（"常见失误"里也是）。alakazam-dusknoir.md 的 Syrup Storm 也是同样的写法，一起改了。登记成已核对的纠错 c-20261005-indy-01。
2. 伤害计算：Meganium 在场时 6 个基本草能量就是 390，一击 Dragapult ex。"Meganium 一上场就收"加上"比 Teal Mask Ogerpon ex 优先"，登记成判断 dpx-omh-01，信心 60%。什么结果算推翻：收掉 Meganium 后，对手用 Night Stretcher 或 Lana's Aid 马上补回来，没有拖慢对手（第 1 局补回过一次）。
3. Celebi（37 份卡表里 36 份带）的 Traverse Time 是招式，Budew 锁不住。
4. 对手 92% 卡表带 Unfair Stamp（37 份里 34 份），我们击倒一只后要防。

ogerpon-meganium-hydrapple.yaml 和 dragapult-ex.yaml 也补了这一场的录像证据；ogerpon-meganium-hydrapple.yaml 里"Wild Growth 在计数里算 2 个"那条推断补上了解说的算法，还没找到正式裁定。

## 第 2 天第 11 轮：Aguilar（Dragapult ex）胜 Frink（Kangaskhan Bouffalant）

视频：第 2 天直播 https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=1260s 。Evan Aguilar 最终第 13，主线 Hammer 版；Joshua Frink 最终第 31（解说念成 Josh Frank），Joltik、Mega Kangaskhan ex、Bouffalant、Bloodmoon Ursaluna ex 的 box。手册没有这个卡组，只做简要记录；赛果按比赛数据。

- 第 1 局 Aguilar 胜：Itchy Pollen 锁住对手的 Precious Trolley；先收能量来源 Joltik；不碰 3 奖的 Mega Kangaskhan ex，把 Phantom Dive 的指示物和两次 Adrena-Brain 叠在 Bloodmoon Ursaluna ex 上（[45:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=2700s)）。Bouffalant 的 Curly Wall 只减招式伤害（基础无色宝可梦 −60），指示物不受影响。
- 第 2 局：Frink 的 Kangaskhan 充满能量开始拿奖，时间快到时他要连续两次正面才能逼出第 3 局，没成功（[1:11:00](https://www.youtube.com/watch?v=6Nl_UgEEXM8&t=4260s)）。后段只粗读了。

dragapult-ex.yaml 补了这一场的录像证据。

## 第 1 天第 4 轮：Yamaguchi（Dragapult ex）2-1 Tate（Mega Diancie Dusknoir）

视频：第 1 天直播 https://www.youtube.com/watch?v=1Z6jmnN6-Ks&t=1980s 。电脑上的复盘先把 Dragapult 一方认成了 Schemanske（字幕里的"Diancie"），比赛数据里是 Yoshiyuki Yamaguchi（Hammer 版，3 张 Crushing Hammer，带 Moltres）；赛果按比赛数据。比赛数据里没有 Yakira Tate 的卡表。手册没有这个卡组，只做简要记录。

- 第 1 局 Yamaguchi 胜：Phantom Dive 先打战斗场能攻击的 Latias；对手一直没找到 Lillie's Clefairy ex。
- 第 2 局 Tate 胜：Mega Diancie ex 的 Garland Ray（弃能量，每个 120）加 Powerglass（回合结束时从弃牌区贴回 1 个基本能量）连续攻击，Cursed Blast 收掉 Budew；Yamaguchi 两张 Hammer 都是反面。
- 第 3 局 Yamaguchi 胜：他打 Judge，把自己从一手死牌里救回来。后段只粗读了。

dragapult-ex.yaml 补了这一场的录像证据。
