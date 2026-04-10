# Trigger Dictionary

**25 thinking tool protocols in one skill.**

A protocol dictionary containing structured analysis tools — Holmes (observe→hypothesize→eliminate), Occam (competing hypotheses→select simplest), First Principles (decompose to axioms→rebuild), Bayesian (prior→evidence→posterior update), Pre-mortem (assume failure→trace causes→prevent), and 20 more. Each tool has a defined action sequence; just say the tool name and Claude executes the full protocol.

### Example Prompts

```
"Analyze this with Holmes" → observation→anomaly→hypotheses→evidence→elimination→conclusion
"First Principles on this problem" → strip analogies→decompose to axioms→reassemble
"Run a Pre-mortem" → assume failure→trace top 3 causes→build prevention plan
"Bayesian update" → state prior→weigh evidence→output posterior
```

### Included Tools (26 total)

- **Analysis (7):** Holmes, Occam, First Principles, Bayesian, Umbrella, Analogy, Deductive Convergence
- **Structure (7):** Surgical, Edit4, Backbone, Skeleton, SHE, Elevator Pitch, Timestone
- **Execution (5):** MacGyver, Nudge, Triage, Zoom, Absolute
- **Judgment (2):** Pre-mortem, Rose-tinted Runaway
- **Perspective (2):** Labyrinth, Paralysis/Wall/No-cards
- **Transition (2):** Main-task / Sub-task switching

## Installation

```bash
git clone https://github.com/jasonnamii/trigger-dictionary.git ~/.claude/skills/trigger-dictionary
```

## Update

```bash
cd ~/.claude/skills/trigger-dictionary && git pull
```

Skills placed in `~/.claude/skills/` are automatically available in Claude Code and Cowork sessions.

## Part of Cowork Skills

This is one of 25 custom skills. See the full catalog: [https://github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## License

MIT License — feel free to use, modify, and share.
