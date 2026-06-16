# Kit Colour Query

Use kit colours as a verified factual input, not as a guess. Classify every colour claim by confidence.

## Source Priority

1. Official competition match-colour designation.
   - FIFA World Cup pages may link to `Fwc2026 Match Colours Designation` or a similar Digital Hub collection.
   - When the official PDF or image is hard to parse, look for reputable mirrors that embed the official pages, then cite both the official collection and the mirror.
   - For the 2026 World Cup example, Footy Headlines embedded screenshots from FIFA's official `Match Team Colours` PDF and linked the FIFA Digital Hub source.
2. Official match centre, team sheet, or pre-match coordination note.
3. Team official dressing-room photos, starting-XI graphics, kit-announcement posts, or matchday posts.
4. Reputable kit specialists or match previews that explicitly cite the official designation.
5. Normal home/away kit inference. Use this only when no better source exists.

## Confidence Labels

- `official-designation`: official competition colour designation, PDF, match centre, or team sheet.
- `official-pre-match`: team or competition social post showing the dressing room, lineup graphic, or "today's kit".
- `reputable-secondary`: a reliable mirror or specialist site that cites the official document.
- `probable`: regular home/away kit inferred from the fixture order.
- `unknown`: no reliable source.

Always state the label. If the label is not `official-designation` or `official-pre-match`, call the Five Elements reading provisional.

## FIFA World Cup Lookup Pattern

1. Search for:
   - `FIFA World Cup match colour designations [teams]`.
   - `Fwc2026 Match Colours Designation`.
   - `[Team A] [Team B] kit colours FIFA match team colours`.
2. Open the FIFA Digital Hub or FIFA article when available.
3. If the Digital Hub page exposes a collection but not the PDF content:
   - Find the public media id in the URL, often `mediaId=...`.
   - Search that title or media id on specialist kit sites.
   - Use embedded official screenshots only when they visibly show the match number and team names.
4. Match by official match number, group, date, and team names. Do not rely on image filename numbering alone because article image indices may represent PDF pages, not match numbers.
5. Extract:
   - Team A player shirt, shorts, socks.
   - Team A goalkeeper shirt, shorts, socks.
   - Team A substitute bib.
   - Referee colour.
   - Ball kid colour if present.
   - Team B player shirt, shorts, socks.
   - Team B goalkeeper shirt, shorts, socks.
   - Team B substitute bib.
6. Save the source link and the exact text visible in the chart.

## Example: Sweden vs Tunisia, 2026 World Cup

The official chart screenshot for Match No. 12, Group F shows:

- Sweden player: shirt `yellow / blue`, shorts `blue / white`, socks `yellow / blue`.
- Sweden goalkeeper: shirt `green / black`, shorts `green / black`, socks `green`.
- Sweden bib: `purple`.
- Referee: `black`.
- Ball kid: `dark grey`.
- Tunisia player: shirt `red`, shorts `red`, socks `red`.
- Tunisia goalkeeper: shirt `turquoise`, shorts `turquoise`, socks `turquoise`.
- Tunisia bib: `olive green`.

Use this as `official-designation` if the visible chart is sourced to FIFA's `Match Team Colours` document. Still re-check within 24 hours and within 2 hours before kickoff when making a live report, because late coordination changes can occur.

## Five Elements Mapping

- Wood: green, cyan, teal, turquoise.
- Fire: red, crimson, purple, bright pink.
- Earth: yellow, ochre, tan, brown.
- Metal: white, silver, gold, grey.
- Water: blue, navy, black.

Use kit colours as one input to the Qi Men and bazi judgement:

- Player outfield colours describe the team's visible match qi.
- Goalkeeper colours describe the gate-keeping and defensive qi.
- Bib and referee colours are secondary context only.
