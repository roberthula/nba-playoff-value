# NBA Playoff Value – Problem Statement

**Question**  
Which NBA players (seasons 2000-2024) improve or decline the most in the playoffs compared with the regular season?

**Stakeholders / Use Case**  
- Front-office cap analysts (identify playoff bargains)  
- Fans & media (evidence for debates)  
- My data-analyst portfolio (show end-to-end workflow)

**Metric Selection**  

| Metric | Unit | Playoff coverage | Keep? | Note |
|--------|------|------------------|-------|------|
| WS/48  | wins / 48 min | Yes (all yrs) | ✅ | Linear in wins, widely cited |
| BPM    | pts / 100 poss | Yes (all yrs) | ✅ | Adjusted for pace |
| RAPM   | pts / 100 poss | Spotty        | ❌ | Needs heavy play-by-play |
| PER    | index | Yes | ❌ | Not win-scaled |

*Chosen:* **WS/48** and **BPM** (transparent formulas, playoff availability).

**Project Constraints**  
- Seasons: 2000-2024  
- Player sample: ≥ 3 000 RS minutes *and* ≥ 500 PO minutes  
- Salary lens: 2024 salary as % of 2024 cap  
- Anything added after Day 2 goes to an Icebox list
