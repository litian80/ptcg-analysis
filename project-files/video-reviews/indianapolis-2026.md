# Indianapolis 2026 区域赛复盘

比赛 2026-05-30，环境 TEF-POR（比现在少 CRI、PBL、30C 三个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-05-30_559_regional-indianapolis-in。八强：Jones（Alakazam Dudunsparce，冠军）、Reddy（Crustle，亚军）、Newdorf（Dragapult Dusknoir）、Melville、Hamilton、Hedrick、Sakadjian、Lu（都是 Dragapult ex）。直播只播了八强、四强、决赛各一场，都已看完。

做法：没有调用 API，在你电脑上逐张看截图、对照解说写成。决赛和八强用的是旧版侧边面板，工具读出的奖赏卡变化不全（决赛还切错了局数），拿奖时间按解说；四强用的是 Baltimore 那一款面板，读数和解说一致。

判断台账（data/judgments/）里还没有这几场对局的判断，没有要记的验证结果。台账里 Alakazam Dudunsparce 对 Dragapult 的三条判断说的是纯 Dragapult ex，四强的对手是 Dragapult Dusknoir，没有算进去。这次写进手册的关键判断登记成了新判断，编号写在各场的"写进手册的"里。

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
