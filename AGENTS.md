# worldcup-mystic-oracle

Use `skills/worldcup-mystic-oracle/SKILL.md` when the user asks for a football or World Cup pre-match mystic report, Qi Men/Bazi football prediction, or China Sports Lottery strategy.

Default execution stance:

- Produce Chinese output.
- Treat the report as entertainment-only, not betting or investment advice.
- Use official Sporttery/中国体彩 odds for all stake-return arithmetic.
- Use `skills/worldcup-mystic-oracle/scripts/collect_match_bundle.py` before a long manual search whenever the user asks for a concrete match.
- Use `skills/worldcup-mystic-oracle/scripts/optimize_strategy.py` when official odds and score scenarios are available.
- Prefer one compact strategy, not a menu of styles.
- Do not claim guaranteed profit.
