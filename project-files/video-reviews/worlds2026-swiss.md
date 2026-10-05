# 2026 世界赛瑞士轮复盘

比赛 2026-08-28 开始，环境 TEF-PBL（比现在少 30C 一个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-08-28_515_world-championships-2026。这里收第 1、2 天直播（第 1 天 iEM8bQbnA90、第 2 天 qwBID2ApsOY）里有我们推荐卡组的瑞士轮场次；决赛圈见 worlds2026-masters-top-cut.md 和 worlds2026-finals.md。按复盘的先后排列。

做法：没有调用 API，在你电脑上看截图、对照解说写成。奖赏卡数取自解说。

判断台账（data/judgments/）：前五场的对局之前都没有登记判断，没有要记的验证结果；这次写进手册的关键判断登记成了新判断，编号写在"写进手册的"里。crustle-dri.md 里两处 Special Red Card 的条件写错了，记成已核对的纠错；第 1 天第 3 轮的 Dragapult ex 镜像对 dpx-mir-01 有一次验证。这两项都记在 data/judgments/sources/2026-10-05_video_worlds-2026.yaml。第 11 轮的对手 Lopunny Dusknoir 不在手册里，没有判断可验证。

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

## 第 10 轮：Cassiraga（Alakazam Dudunsparce）2-1 Karjala（Slowking）

视频：第 2 天直播 https://www.youtube.com/watch?v=qwBID2ApsOY&t=10980s （约 3:03 起，只播了第 3 局）。电脑上的复盘把 Slowking 一方记成 Anie，按比赛数据第 10 轮的对阵确认是 Aarni Karjala，最终第 31。他的卡表：3 只 Kangaskhan、2 只 Metagross、2 只 Kyurem、Zeraora、2 张 Lucky Helmet、Secret Box、Surfer，没有 Annihilape、Cofagrigus 和 Prime Catcher。Diego Cassiraga 最终第 2：2 只 Genesect、Shaymin、Lucky Helmet、4 张 Battle Cage、2 张 Enhanced Hammer、1 张 Eri。

### 第 3 局：Cassiraga 胜

- Karjala 起手很差：连着两回合把手贴的能量给了 Latias ex；在战斗场把 Slowking 进化出来时，它身上没有能量（[3:08:30](https://www.youtube.com/watch?v=qwBID2ApsOY&t=11310s)）。
- Cassiraga 在后备区放 Shaymin 防 Trifrost，解说也这样讲。Powerful Hand 收掉 Slowking 和 Lillie's Clefairy ex。Karjala 的 Lucky Helmet 没有触发：Powerful Hand 放的是指示物，不是伤害。
- Karjala 复制 Metagross 打倒一只（[3:12:30](https://www.youtube.com/watch?v=qwBID2ApsOY&t=11550s)）之后，Cassiraga 用 Battle Cage 盖掉 Academy at Night，Karjala 就控不了牌库顶了，Cassiraga 收尾。

### 对照手册

slowking-scr.md 的 vs Alakazam Dudunsparce（28.4%）说中的：Shaymin 挡 Trifrost 的后备区伤害；Battle Cage 和 Academy at Night 来回换，要多备一张；别把 Latias ex 放上场。Karjala 的卡表没有放指示物的复制来源，Shaymin 一直没收掉。

写进手册的（PR #33）：

1. "被 Powerful Hand 击倒时 Lucky Helmet 不抽牌"去掉"推断"，按卡牌文字写，加上这一局。
2. Battle Cage 一条加上这一局：对手的 Battle Cage 也会弃掉你的 Academy at Night。
3. 常见失误加一条：战斗场的 Slowpoke 没贴能量就进化。
4. Shaymin 的处理按卡牌原文重写：SSP 83 版 Cofagrigus 只放 6 个，收不掉 80 HP 的 Shaymin；Spectrier（ASC 98）和 WHT 40 版 Cofagrigus 能一下收掉（录像在 Melbourne，见 melbourne-2026.md）。

alakazam-dudunsparce.yaml 和 slowking-scr.yaml 也补了这一场的录像证据。

## 第 1 天第 4 轮：CAI YI（Slowking）2-0 Zapata（Mega Excadrill ex）

视频：第 1 天直播 https://www.youtube.com/watch?v=iEM8bQbnA90&t=19020s （约 5:17-5:57）。CAI YI 最终第 69，卡表在数据里写作 Cai Yi：SSP 100 和 PBL 41 版 Annihilape 各 1 只、Metagross、Zeraora、2 只 Kyurem、Prime Catcher、Brave Bangle、3 张 Boomerang Energy。Emiliano Zapata 最终第 39：18 个 Metal、4 只 Metang、2 只 Genesect ex、1 只 Mega Skarmory ex、1 张 Hero's Cape，没有 Shaymin。

### 第 1 局：CAI YI 胜

- Trifrost 一次收掉三只 Metang，拿 3 张，对手的能量加速全没了（[5:31:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=19860s)）。Zapata 的 Undermine 弃掉了 CAI YI 牌库顶的一张 Ciphermaniac's Codebreaking。
- 接着复制 Annihilape 的 Destined Fight，和战斗场的 Mega Excadrill ex 同归于尽，拿 3 张（[5:34:30](https://www.youtube.com/watch?v=iEM8bQbnA90&t=20070s)）。两次攻击拿完 6 张。

### 第 2 局：CAI YI 胜

- 又是 Trifrost 拿 3 张（[5:47:30](https://www.youtube.com/watch?v=iEM8bQbnA90&t=20850s)）。
- Zapata 追回 3 张。CAI YI 算准对手凑不到 5 个能量，才把 Kangaskhan 放到战斗场。
- 最后 Destined Fight 收尾（[5:54:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=21240s)）。

### 对照手册

slowking-scr.md 的 vs Mega Excadrill ex（64.0%）说中的：第 2 回合 Trifrost 取 3（对手没带 Shaymin）；Destined Fight 一换三；Undermine 会弃掉牌库顶的牌；Kangaskhan 别留在战斗场挨 330（第 2 局 CAI YI 算准了才放）。

写进手册的（PR #33）：

1. 两次攻击拿完 6 张的路线（Trifrost 收 3 只进化前宝可梦，再用 Destined Fight 换掉 Mega Excadrill ex）登记成判断 slk-mex-01，信心 70%；关键卡一节"Destined Fight（推断，数据样本不足）"改成引用这一场。
2. 对手的 Hero's Cape 挂在 Metang 上是 200，Trifrost 打不倒，这一回合少拿 1 张（这一场 Cape 在奖赏卡里，是解说提的）。
3. 通用部分"攻击前的顺序"加上手贴 Telepathic Psychic Energy：它找完宝可梦会洗牌，Academy at Night 要放在它之后（解说特别强调了这个顺序）。

没写进手册的：战斗场有贴了能量的 Slowpoke 时，用 Latias ex 换下来，别让 Undermine 90 收掉 80 HP 的 Slowpoke。只是一处小失误。

mega-excadrill-ex.yaml 和 slowking-scr.yaml 也补了这一场的录像证据。

## 第 1 天第 8 轮：Cassiraga（Alakazam Dudunsparce）2-0 Arai（Basic Box）

视频：第 1 天直播 https://www.youtube.com/watch?v=iEM8bQbnA90&t=38280s （约 10:38-11:32）。电脑上的复盘把 Basic Box 一方听成了 Kato；比赛数据里第 8 轮 Cassiraga 的对手是 Keito Arai（最终第 17），Yasunori Kato 第 5 轮后就退赛了。Arai 的卡表：2 只 Kangaskhan、Pecharunt（SVP 149）、Chien-Pao、Wellspring Mask Ogerpon ex、4 张 Energy Switch、Unfair Stamp，没有 Special Red Card。Cassiraga 的卡表见第 10 轮。

### 第 1 局：Cassiraga 胜

- Cassiraga 的 Shaymin 在奖赏卡里。Arai 第 1 回合用 Iron Leaves ex 拿 1 张，Cassiraga 马上用 Rare Candy 进化 Alakazam，Powerful Hand 回敬。
- Cassiraga 放下 Genesect 挂上道具，Arai 唯一的手牌干扰 Unfair Stamp 就打不出来了（[10:47:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=38820s)）。
- Arai 用 Pecharunt 的 Poison Chain 让战斗场的 Genesect 中毒、不能撤退，想毒倒它解锁（[10:57:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=39420s)）。Cassiraga 把它换下来，又放了第二只 Genesect。
- Arai 的 Kangaskhan 卡在战斗场撤不下来，Cassiraga 拿下。

### 第 2 局：Cassiraga 胜

- Arai 的 Wellspring Mask Ogerpon ex 用 Torrential Pump 拿 2 张；Cassiraga 手牌够多，Powerful Hand 收掉 Wellspring。
- 之后他把 Dunsparce 都进化成 Dudunsparce（140），Torrential Pump 后备区的 120 打不倒了，Cassiraga 收尾。
- 解说指出：Arai 整局一张 Energy Switch 都没摸到。

### 对照手册

basic-box-m.md 的 vs Alakazam Dudunsparce（42.1%）说中的：Genesect 带道具时不能打 ACE SPEC，这是整场的核心；Arai 没有别的手牌干扰，Cassiraga 的手牌一直在 11 到 16 张；Kangaskhan 卡在战斗场。

写进手册的（PR #33）：

1. Special Red Card 不是 ACE SPEC，Genesect 挡不住，手牌干扰要靠它而不是 Unfair Stamp（登记成判断 bbm-adu-01，信心 65%）。数据上带 Special Red Card 的卡表高 11 个百分点，Arai 不带。
2. 另一个对付 Genesect 的办法：Pecharunt（SVP 149）的 Poison Chain 加特性 Toxic Subjugation，战斗场的 Genesect 两次宝可梦检查就倒（前提是 80 HP 的 Pecharunt 撑过对手一回合）；对手能用换人的卡躲开。卡牌原文核对过：Poison Chain 是非 ex 的 Pecharunt 的招式，电脑上的复盘写成了 Pecharunt ex，已改正。

alakazam-dudunsparce.yaml 和 basic-box-m.yaml 也补了这一场的录像证据。

## 第 11 轮：Hedrick（Dragapult ex）2-0 Koyama（Lopunny Dusknoir）

视频：第 2 天直播 https://www.youtube.com/watch?v=qwBID2ApsOY&t=12990s （约 3:36-4:27）。Andrew Hedrick 是后来的世界冠军，卡表见 worlds2026-masters-top-cut.md。Joji Koyama 最终第 55：Mega Lopunny ex 加 4-2-4 的 Duskull 线和 2 只 Bronzong（招式 Evolution Jammer：对手下一回合不能从手牌进化），只有 6 个能量（4 张 Telepathic Psychic Energy、1 张 Psychic Energy、1 张 Enriching Energy）。手册没有这个卡组，只做简要记录。

- 第 1 局 Hedrick 先攻，Bronzong 第 1 回合上不来；Crushing Hammer 正面，拆掉一张 Telepathic Psychic Energy。被 Evolution Jammer 锁进化时，Fezandipiti ex 的 Cruel Arrow 专打 Duskull 和 Dusclops（解说说它是这局的 MVP，[3:49:00](https://www.youtube.com/watch?v=qwBID2ApsOY&t=13740s)），Munkidori 的 Mind Bend 让 Bronzong 混乱。锁一解开就进化，Phantom Dive 先收后备区的 Duskull，最后收掉 Mega Lopunny ex。
- 第 2 局 Bronzong 混乱时翻到反面，打倒了自己，锁解开（[4:13:00](https://www.youtube.com/watch?v=qwBID2ApsOY&t=15180s)）。Hedrick 用 Unfair Stamp 加 Phantom Dive 收尾。
- 解说总结："真正的威胁不是 Bronzong，而是那些 Duskull。"

dragapult-ex.yaml 补了这一场的录像证据。

## 第 1 天第 3 轮：Tonisson（Dragapult ex）2-0 Madsen（Dragapult ex）

视频：第 1 天直播 https://www.youtube.com/watch?v=iEM8bQbnA90&t=14400s （约 4:00-4:43）。Brent Tonisson 最终第 3（就是 Brisbane 的 BrentyMon），主线 Hammer 版，带 Special Red Card、Judge、Moltres。Oscar Madsen 也是 Hammer 版，没进第 2 天，比赛数据里没有他的卡表。Madsen 两局都选后攻，两局都输（只记录）。

### 第 1 局：Tonisson 胜

- Madsen 的 Unfair Stamp 和 Fezandipiti ex 都在奖赏卡里，开局只能放下 Meowth ex。
- Madsen 先用 Budew 锁物品；Tonisson 用 Itchy Pollen 击倒对方的 Budew，解开自己的锁，再锁住对方（[4:07:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=14820s)）。
- 之后 Tonisson 两次能打 Phantom Dive，但没有击倒目标，都改用 Itchy Pollen 继续锁（[4:09:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=14940s) 和 4:15）。他在对手被锁时打 Judge，Phantom Dive 一次收两只 Dreepy，最后 Boss's Orders 拉出 Meowth ex，一回合拿 3 张。解说："别人会更早出手，Brent 知道自己领先，一点风险不冒。"

### 第 2 局：Tonisson 胜

- Tonisson 先攻，先用 Drakloak 收掉 Dunsparce、再用 Munkidori 收掉 Drakloak，领先 3 张。Madsen 没有先锁（解说说他先锁的话，Tonisson 会放自己的 Budew 用 10 点收掉）。
- Madsen 用 Unfair Stamp、Crushing Hammer 和 Mind Bend 反扑。解说："这回合赢不了，没必要 Phantom Dive，用 Itchy Pollen 再拖。"（[4:34:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=16440s)）
- 最后 Tonisson 用 Mind Bend 60 加两只 Munkidori 的 Adrena-Brain 各 30，正好收掉对方受了伤的 Dragapult ex（[4:41:00](https://www.youtube.com/watch?v=iEM8bQbnA90&t=16860s)）。

### 对照手册

dragapult-ex.md 的镜像一节说中的：Judge 只在对手被锁时打（两局都是）；Boss's Orders + Phantom Dive 一回合多张；Meowth ex 别在开局放下（Madsen 被迫放下，最后成了拿 3 张那一回合的目标）。

台账：dpx-mir-01（先保住自己能用物品）第 1 局 held，第 2 局 n/a（Madsen 没先锁）；加上 Baltimore 第 14 轮那一次，从 65% 升到 75%。dpx-mir-02（没有击倒目标别用 Phantom Dive）两局都没有对上它的前提，方向一致：Tonisson 拖的时候用的是 Itchy Pollen，不是 Jet Headbutt。

写进手册的（PR #34）：

1. 新判断 dpx-mir-03（信心 60%）：第一次拿奖用 Itchy Pollen 击倒对方的 Budew。依据是这一场第 1 局和 Baltimore 2026 第 2 天第 14 轮（见 baltimore-2026-day2-swiss.md），解说给的理由一样。
2. dpx-mir-02 放宽成"先用 Jet Headbutt 或 Budew 的 Itchy Pollen 拖"，信心不变。
3. 镜像一节加了这一场的小节。

dragapult-ex.yaml 补了这一场的录像证据。
