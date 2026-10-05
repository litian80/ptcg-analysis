# video：Pokémon TCG 对局视频分析

把一场 YouTube 上的对局（Worlds、国际赛、Regional 直播等）变成可以复盘的时间线和对局报告。

## 它做什么

1. **取素材**：用 yt-dlp 下载字幕（优先人工字幕，没有就用自动字幕）和视频（默认 ≤720p）。直播动辄几小时，可以用 `--start/--end` 或 `--chapter` 只分析其中一局（视频整段下载、本地截取：yt-dlp 按时间段下载要经过 ffmpeg，慢几十倍）。也可以直接给本地视频文件和字幕文件。
2. **读字幕**（不花钱，总会跑）：清理 YouTube 自动字幕的滚动重复，按时间戳找出解说提到的卡名（容忍自动字幕的拼写错误，比如 "charizard x" → Charizard ex，"garde voir" → Gardevoir）和关键动作（击倒、拿奖、进化、换位、认输、"that's game"、"your new world champion"），据此切分每一局。解说经常在讨论"能不能 KO"，这类带假设语气的句子会标成 `definite=false`，不算作发生了的事件，也不会切断对局。
3. **抽帧**：每 N 秒抽一帧，比较缩略图像素，只保留局面有变化的关键帧。压缩噪点、面板边框发光这类一直在闪的像素、只出现一下的卡牌放大图和横幅都不算变化。官方直播（Play! Pokémon）两侧是每位选手的数据面板，中间是一直在动的手部镜头，用 `--hash-regions sides` 只看两侧面板，关键帧就是真正的局面变化。区域赛直播（如 2026 Brisbane）没有侧边面板，用 `--hash-regions regional` 看顶部记分条（已赢局数和每人 6 个奖赏卡标记）和左侧弹出的卡图。
   - **读奖赏卡**：`sides` 布局下，每帧数两侧面板上亮着的奖赏卡小球（每人 6 个），得到一条精确的"剩几张"时间线，写进 `prizes.json`、`report.md` 和 `review_pack.md` 的每个窗口。连续两帧读数一致才算；读数只减不增，所以赛后回放不会干扰；回到 6/6 并保持 20 秒（其他回升保持一分钟）算新的一局，报告里的局数也按这个划分。卡图放大、横幅、解说台镜头会读不出来，直接跳过；被它们挡住时，变化时间写成一个区间，击倒就发生在区间里。一局的最后一张常因直播切走而漏读，看局分变化。新一局刚开始时插播的上一局回放（画面上方有 REPLAY 标记，两侧选手还可能对调）会被当成这一局的拿奖，要对照画面。`--prizes off` 关掉。小球位置是在 2026 Frankfurt 区域赛直播上量的（1280x720 画面）。
4. **Claude 看图**（需要 API key；不想用 API 就加 `--no-llm`，见下面"不用 API key"）：每 60 秒一个窗口，把关键帧、同时段解说、提到的卡名和上一窗口的局面一起交给 Claude，返回结构化 JSON：双方前场（含剩余 HP）、后备、剩余奖赏卡、场地卡、这段发生了什么。官方直播有数据面板时，Claude 直接读面板上的数字。
5. **对局报告**：再用一次 Claude，把整条时间线写成中文复盘：双方卡组、每局走势和转折点、关键决策、对选卡和这个对局的启示。时间戳可点击跳回视频。

## 用法

```bash
cd video
python3 -m pip install -r requirements.txt   # 另需系统里有 ffmpeg

# 看一个直播有哪些章节（通常一局一个章节）
python3 -m ptcg_video chapters "https://www.youtube.com/watch?v=VIDEO_ID"

# 分析其中一局（官方直播用 --hash-regions sides）
export ANTHROPIC_API_KEY=...
python3 -m ptcg_video analyze "https://www.youtube.com/watch?v=VIDEO_ID" \
    --chapter 3 --hash-regions sides

# 只用字幕、不下载视频、不调用 Claude（最快、免费）
python3 -m ptcg_video analyze VIDEO_ID --captions-only --no-llm

# 本地文件
python3 -m ptcg_video analyze match.mp4 --captions match.en.vtt --start 12:00 --end 48:30
```

### 不用 API key

加 `--no-llm` 时不调用 Claude API，但只要有视频，就会多写一个 `review_pack.md`：按窗口（`--window` 秒）列出关键帧图片路径（每窗口 `--frames-per-window` 张）、同时段解说、提到的卡名和解说明确喊出的击倒/拿奖。在 Claude Code（或 Claude 桌面版）里打开这个文件，让 Claude 按顺序看图写复盘，用的是订阅额度，不按 API 计费。看一局约 30 分钟的比赛，`--window 90 --frames-per-window 2` 大约 40 张图。

```bash
python3 -m ptcg_video analyze match.mp4 --captions match.en.vtt --start 0:21 --end 28:36 \
    --hash-regions sides --no-llm --window 90 --frames-per-window 2
```

输出在 `out/<视频 id>/`：

| 文件 | 内容 |
|---|---|
| `report.md` | 给人看的报告：Claude 复盘、局面时间线、解说提到的卡、关键时刻 |
| `timeline.json` | 每个窗口的局面（前场、后备、奖赏卡、动作） |
| `caption_events.json` | 字幕里的卡名和动作，带时间戳 |
| `transcript.json` | 清理后的字幕 |
| `frames/`、`frames.json` | 抽出的帧和哪些是关键帧；读得出奖赏卡时每帧带 `prizes`（左、右剩几张） |
| `prizes.json` | 奖赏卡时间线：每次变化的时间、左右各剩几张、第几局 |
| `review_pack.md` | `--no-llm` 时：给人或 Claude 会话逐窗口看图用的素材清单 |

## 卡名来源

本目录不自带卡牌数据库，卡名来自仓库的 `data/`（环境与卡池数据）：

- 默认（`--cards auto`）：读 `data/formats/standard_rotations.json`，按视频上传日期找到当时的 Standard 环境，只用 `data/formats/<环境>/card_pool.csv` 里当时合法的卡名。这样旧卡（比如把 "Dragapult ex" 认成 "Dragapult V"）基本不会误配。
- `--format 2026-27` 手动指定环境（比赛在换季前举办、换季后才上传时用）；`--live` 表示 TCG Live 视频，按 Live 的换季日期（比线下早两周左右）。
- `--data-dir` 指定 `data/` 的位置（默认从当前目录往上找）。在本仓库里运行时会自动找到仓库根目录的 `data/`。找不到或读不了时只跳过卡名识别，其余照常。
- 环境变量 `PTCG_CARD_NAMES` 可以指定默认卡表文件；给了 `--format` 或 `--data-dir` 时以它们为准。
- `--cards 文件` 也可以直接给卡表：`.txt`（一行一个）、`.json`（名字列表，或带 `name` 字段的对象列表）或 `.csv`（`name` 列）；`--cards none` 关闭卡名识别。

judge、grant、switch 这类同时是普通英文单词的卡名，在有大小写的字幕里只有首字母大写时才算卡名。

## 费用控制

- 先用 `--no-llm` 跑一遍，看字幕和关键帧是否合理，再开 Claude。
- `--max-windows N` 限制看图调用次数；`--window`、`--frames-per-window` 调整每次发多少帧。
- 看图默认 `--effort low`，最后的总结用 high。默认模型 `claude-opus-5-5`。

## 已知限制

- 画面识别依赖直播的画面布局；`sides` 预设按 2026 Worlds 的布局（两侧各约 21% 宽）设定，别的布局可以用 `--hash-regions x,y,w,h;...`（画面比例）自己指定，`--change-threshold` 调灵敏度（区域里变化的像素比例，`full` 默认 0.05，`sides` 和自定义区域默认 0.02），`--dead-band` 调像素要变多少才算变（`full` 默认 8，`sides` 默认 30；这组默认值是在 2026 世界赛决赛上校准的，一局 28 分钟大约 130 张关键帧）。`frames.json` 里每帧的 `change` 是它和上一关键帧的最大变化比例，可以照着它定阈值。读不出来的数值会是 null。
- 字幕里 KO/拿奖的"是否真的发生"是按语气判断的，会有漏判和误判；以 Claude 看画面得到的时间线为准。
- 自动字幕对卡名错误较多，模糊匹配需要装 rapidfuzz。实际直播里听错的卡名（比如 "Fessentipity" → Fezandipiti ex）记在 `lexicon.py` 的 `CAPTION_ALIASES`，只在听错的词本身不是当季卡名时生效。选手的口语简称（"pult" → Dragapult ex、"monkey dory" → Munkidori）也在这个表里，但 "hammer"、"stamp" 这类普通英文单词不收。
- 官方直播面板上名字旁边的大数字是这场已赢局数，奖赏卡是旁边那一列 6 个小标记。
- 解说说"game"不一定是在说对局结束，字幕切分的对局边界是参考：有章节时不会跨章节，选手自己的复盘视频（边看边聊别的局）基本切不准，看完画面后用 `--games 43:40-53:20,53:40-1:04:20` 直接指定。

## 测试

```bash
python3 -m pytest -q tests
```

测试用 ffmpeg 生成的合成视频和手写的 YouTube 滚动字幕样例，Claude 调用用假客户端代替，不需要网络和 API key。
