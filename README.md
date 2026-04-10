# trigger-dictionary

**25 thinking tool protocols in one skill — say the tool name, execute the full protocol.**

## Goal

Complex problems demand different thinking approaches. Trigger Dictionary eliminates the friction between knowing which tool you need and actually executing its full protocol. Rather than manually assembling methodology steps, you invoke a tool by name and get the complete, pre-engineered thinking framework.

## When & How to Use

Use this skill whenever you encounter a problem that requires a specific thinking methodology. Say the tool name — Holmes, Occam, First Principles, Bayesian, Pre-mortem, Analogy, Surgical, etc. — and Claude executes the full protocol with all steps, gates, and output structures. Tools are organized into 6 categories (Analysis, Structure, Execution, Judgment, Perspective, Transition), making it easy to find the right approach for your situation. Input → tool name → structured output.

## Use Cases

| Scenario | Prompt | What Happens |
|---|---|---|
| Need rigorous elimination logic | `"Holmes on this decision"` | Observe→Hypothesize→Eliminate protocol; constraints identified; alternatives narrowed |
| Simplify overcomplicated solution | `"Occam this problem"` | Fewest assumptions identified; redundancies removed; simplest explanation surfaced |
| Build from fundamentals | `"First Principles on our approach"` | Assumptions broken down; axioms identified; solution rebuilt from core truths |
| Evaluate under uncertainty | `"Bayesian on this market assumption"` | Prior probability→evidence strength→posterior reasoning; confidence intervals calculated |
| Identify hidden failure modes | `"Pre-mortem on this launch"` | Future failure scenarios mapped; failure causes diagnosed; mitigation plans drafted |

## Key Features

- 25 thinking protocols across 6 categories: Analysis (Holmes, Occam, First Principles, Bayesian, Dimensional, Socratic, Ladder), Structure (Pre-mortem, Analogy, Surgical, Backbone, Skeleton, SHE, Elevator Pitch), Execution (Timestone, MacGyver, Nudge, Triage, Zoom), Judgment (Reversal, Antidote), Perspective (Thesis, Antithesis), Transition (Stepwise, Ratchet)
- One-word invocation — just name the tool, get the full methodology
- Pre-engineered protocols with clear steps and validation gates
- Protocols pair diagnostic reasoning with actionable output
- Works across domains: strategy, product, hiring, partnerships, operations

## Works With

- **[planning-skill](https://github.com/jasonnamii/planning-skill)** — planning-skill orchestrates phases; trigger-dictionary provides the thinking tools within each phase
- **[research-frame](https://github.com/jasonnamii/research-frame)** — research-frame structures multi-axis investigation; trigger-dictionary tools power individual axis analysis
- **[deliverable-engine](https://github.com/jasonnamii/deliverable-engine)** — deliverable-engine packages outputs; trigger-dictionary generates rigorous content

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

This is one of 25+ custom skills. See the full catalog: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## License

MIT License — feel free to use, modify, and share.
