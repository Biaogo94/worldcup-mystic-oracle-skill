# Qi Men Engine

Use this file before charting a match. The goal is to avoid hand-built or HTML-fragile charts when a structured engine is available.

## Engine Priority

1. **Primary: qfdk/qimen local engine**
   - Source: `https://github.com/qfdk/qimen`
   - Method stated by project: 茅山派奇门遁甲, 转盘排法.
   - Provides: 地盘, 天盘, 八门, 九星, 八神, 暗干, 四柱, 局数, 旬首, 值符, 值使, 空亡, 马星, 格局/解断 fields.
   - Best use: deterministic JSON for the football scoring model.
2. **Secondary: another cited structured Qi Men library or official calculator**
   - Use only when it exposes enough palace data to audit.
3. **Fallback: saved calculator HTML parsed by `scripts/qimen_parse.py`**
   - Label as lower confidence if palace mapping or special patterns are incomplete.
4. **Last resort: 简化奇门象占**
   - Use only when no chart source is available; do not claim exact palace placements.

## qfdk/qimen Setup

Do not silently vendor third-party code. Either point to an existing local checkout or clone it into a known engine directory:

```bash
git clone https://github.com/qfdk/qimen.git ~/.qimen/qfdk-qimen
cd ~/.qimen/qfdk-qimen
npm install
```

Then run:

```bash
node scripts/qimen_qfdk.js --engine-dir ~/.qimen/qfdk-qimen --datetime 2026-06-14T12:00:00-05:00 --location "Houston" --pretty
```

Alternative:

```bash
export QIMEN_QFDK_PATH=~/.qimen/qfdk-qimen
node scripts/qimen_qfdk.js --datetime 2026-06-14T12:00:00-05:00 --pretty
```

Always pass the venue-local kickoff wall time with a UTC offset when possible. The wrapper preserves the wall time for qfdk because qfdk reads JavaScript `Date` values in the Node process local timezone. The offset is kept for audit/disclosure, not used to convert the chart to Beijing time. If the input has no offset, state the timezone assumption.

If the user asks for true solar time, adjust the wall time before running the wrapper and disclose the longitude correction.

## Disclosure

When qfdk/qimen is used, disclose:

- Engine and source URL.
- Method: 茅山派 / 转盘 / 时家 unless changed.
- Kickoff time and timezone used.
- Whether true solar time was used. Default remains official local time unless the user asks for true-solar rigor.
- License note if code is bundled: the repository README says MIT while `package.json` says ISC; both are permissive, but keep attribution.

## Boundaries

qfdk/qimen calculates the chart. It does not decide football markets. After getting JSON, read `qimen-scoring.md` and score:

- 主队/客队 anchors.
- Result qi.
- Handicap qi.
- Goal-channel qi.
- Tempo qi.
- Image/detail qi.

If qfdk output lacks a special-pattern row needed by the scoring model, mark that row `unknown` and cap confidence instead of guessing.
