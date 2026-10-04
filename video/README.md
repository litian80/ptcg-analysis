# video：Pokémon TCG 对局视频分析

把一场 YouTube 上的对局（Worlds、国际赛、Regional 直播等）变成可以复盘的时间线和对局报告。

## 它做什么

1. **取素材**：用 yt-dlp 下载字幕（优先人工字幕，没有就用自动字幕）和视频（默认 ≤720p）。直播动辄几小时，可以用 `--start/--end` 或 `--chapter` 只下其中一局。也可以直接给本地视频文件和字幕文件。
2. **读字幕**（不花钱，总会跑）：清理 YouTube 自动字幕的滚动重复，按时间戳找出解说提到的卡名（容忍自动字幕的拼写错误，比如 "charizard x" → Charizard ex，"garde voir" → Gardevoir）和关键动作（击倒、拿奖、进化、换位、认输、"that's game"），据此切分每一局。
3. **抽帧**：每 N 秒抽一帧，用感知哈希只保留桌面有变化的关键帧，省掉大量重复画面。
4. **Claude 看图**（需要 API key，可用 `--no-llm` 关闭）：每 60 秒一个窗口，把关键帧、同时段解说、提到的卡名和上一窗口的局面一起交给 Claude，返回结构化 JSON：双方前场、后备、剩余奖赏卡、这段发生了什么。
5. **对局报告**：再用一次 Claude，把整条时间线写成中文复盘：双方卡组、每局走势和转折点、关键决策、对选卡和这个对局的启示。时间戳可点击跳回视频。

## 用法

```bash
cd video
python3 -m pip install -r requirements.txt   # 另需系统里有 ffmpeg

# 看一个直播有哪些章节（通常一局一个章节）
python3 -m ptcg_video chapters "https://www.youtube.com/watch?v=VIDEO_ID"

# 分析其中一局
export ANTHROPIC_API_KEY=...
python3 -m ptcg_video analyze "https://www.youtube.com/watch?v=VIDEO_ID" \
    --chapter 3 --cards ../path/to/card_names.json

# 只用字幕、不下载视频、不调用 Claude（最快、免费）
python3 -m ptcg_video analyze VIDEO_ID --captions-only --no-llm --cards cards.txt

# 本地文件
python3 -m ptcg_video analyze match.mp4 --captions match.en.vtt --start 12:00 --end 48:30
```

输出在 `out/<视频 id>/`：

| 文件 | 内容 |
|---|---|
| `report.md` | 给人看的报告：Claude 复盘、局面时间线、解说提到的卡、关键时刻 |
| `timeline.json` | 每个窗口的局面（前场、后备、奖赏卡、动作） |
| `caption_events.json` | 字幕里的卡名和动作，带时间戳 |
| `transcript.json` | 清理后的字幕 |
| `frames/`、`frames.json` | 抽出的帧和哪些是关键帧 |

## 卡名来源

本目录不自带卡牌数据库。`--cards`（或环境变量 `PTCG_CARD_NAMES`）接受 `.txt`（一行一个）、`.json`（名字列表，或带 `name` 字段的对象列表，pokemontcg.io / TCGdex 格式都行）或 `.csv`（`name` 列）。仓库里的环境与卡池数据做好后，直接把它的卡表路径传进来即可。不给卡表时仍会识别动作和切分对局，只是没有卡名统计。

## 费用控制

- 先用 `--no-llm` 跑一遍，看字幕和关键帧是否合理，再开 Claude。
- `--max-windows N` 限制看图调用次数；`--window`、`--frames-per-window` 调整每次发多少帧。
- 看图默认 `--effort low`，最后的总结用 high。默认模型 `claude-opus-5-5`。

## 已知限制

- 画面识别依赖直播的画面布局；不同赛事的 overlay 不同，奖赏卡数和手牌数读不出来时会是 null。
- 自动字幕对卡名错误较多，模糊匹配需要装 rapidfuzz。
- 解说说"game"不一定是在说对局结束，字幕切分的对局边界是参考，Claude 的时间线会再核对。

## 测试

```bash
python3 -m pytest -q tests
```

测试用 ffmpeg 生成的合成视频和手写的 YouTube 滚动字幕样例，Claude 调用用假客户端代替，不需要网络和 API key。
