# Qi Men Engine

Use this file before charting a match. Prefer structured MCP output over hand-built charts or HTML parsing.

## Engine Priority

0. **Time preparation: true-solar-time MCP**
   - Source: `https://github.com/Biaogo94/true-solar-time-mcp`
   - Codex config name: `true_solar_time`
   - Use before charting when venue longitude is known.
   - Provides: civil time, true solar time, civil shichen, solar shichen, shichen crossing audit, and `qimen_datetime`.
1. **Primary: Biaogo94/qimen MCP**
   - Source: `https://github.com/Biaogo94/qimen`
   - Local default server: `~/.codex/mcp/qimen/mcp/server.mjs`
   - Codex config name: `qimen`
   - Method: 时家转盘, 拆补口径.
   - Provides: 四柱, 局数, 天盘, 地盘, 八门, 九星, 八神, 暗干, 值符, 值使, 空亡, 驿马, 格局, 九宫解断.
2. **Secondary: bundled MCP stdio client**
   - Use when the agent does not expose MCP tools directly but the local server path exists.
3. **Legacy fallback: `scripts/qimen_qfdk.js`**
   - Use only when MCP is unavailable and a compatible qfdk checkout is available.
4. **Last resort: 简化奇门象占**
   - Use only when no structured chart source is available; do not claim exact palace placements.

## Direct MCP Calls

First prepare time when longitude is known:

```text
qimen_time_prepare(datetime="2026-06-16T18:00:00-04:00", longitude=-71.059, latitude=42.360, location="Boston")
```

Then pass the returned `qimen_datetime` into the qimen engine if:

- `qimen_time_basis=true_solar_time`;
- `crosses_shichen=true`;
- `boundary_risk=high` or `critical`.

If the agent exposes MCP tools, call:

```text
qimen_supported_rules()
qimen_calculate(datetime="2026-06-16T18:00:00-04:00", location="Boston", purpose="综合")
qimen_detect_geju(datetime="2026-06-16T18:00:00-04:00", location="Boston")
qimen_explain_gong(datetime="2026-06-16T18:00:00-04:00", location="Boston", gong="9")
```

Use `qimen_calculate` for full scoring. Use `qimen_detect_geju` for a compact fact card. Use `qimen_explain_gong` only for the home/away/key-person palaces that the analysis needs.

## CLI Fallback Client

If MCP tools are not directly available, call the stdio server through the bundled client:

```bash
node scripts/qimen_mcp_client.mjs \
  --datetime 2026-06-16T18:00:00-04:00 \
  --location "Boston" \
  --pretty
```

Explicit server path:

```bash
node scripts/qimen_mcp_client.mjs \
  --server ~/.codex/mcp/qimen/mcp/server.mjs \
  --datetime 2026-06-16T18:00:00-04:00 \
  --location "Boston" \
  --tool qimen_detect_geju \
  --pretty
```

`collect_match_bundle.py` uses this MCP client automatically when `--kickoff-local` is provided. Pass `--qimen-mcp-server` only when the server lives outside the default path.

## Setup

Recommended local install:

```bash
git clone https://github.com/Biaogo94/qimen.git ~/.codex/mcp/qimen
cd ~/.codex/mcp/qimen
npm ci
npm test
```

Codex MCP config:

```toml
[mcp_servers.qimen]
command = "node"
args = ['C:\Users\Administrator\.codex\mcp\qimen\mcp\server.mjs']
```

For other CLI agents, register the same stdio server path.

## Time Rules

Always pass venue-local kickoff time with an explicit UTC offset when possible. Example: `2026-06-16T18:00:00-04:00`.

When the venue longitude is available, do not call `qimen_calculate` directly with civil time until true-solar-time audit is done. Use:

```text
civil kickoff + venue longitude -> qimen_time_prepare -> qimen_datetime -> qimen_calculate
```

The current qimen engine states:

- `location` is display-only and does not do true-solar-time conversion.
- It supports 时家 only.
- It does not support 日家, 月家, 年家, 置闰, or true solar time.

If true-solar-time MCP is unavailable:

- If kickoff is within 30 minutes of a shichen boundary, cap Qi Men confidence at `low-medium`.
- If longitude is unknown, state `真太阳时未校准`.
- If the match is not near a boundary, disclose that the chart uses civil venue time.

## Disclosure

When MCP is used, disclose:

- Engine: `Biaogo94/qimen` MCP.
- Method: 时家转盘 / 拆补.
- Kickoff time and timezone used.
- True solar time: civil time, true solar time, civil shichen, solar shichen, boundary risk, and whether true solar time was used.
- Limitations from `qimen_supported_rules`.

## Scoring Handoff

After getting JSON, read `qimen-scoring.md` and map:

- 主队/客队 anchors.
- Result qi.
- Handicap qi.
- Goal-channel qi.
- Tempo qi.
- Image/detail qi.

If MCP output lacks a field needed by the scoring model, mark that row `unknown` and cap confidence instead of guessing.
