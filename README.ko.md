# 사고도구 프로토콜 사전

**하나의 스킬에 25개 사고도구 프로토콜 — 도구 이름을 말하면 전체 프로토콜 실행.**

> 🇺🇸 [English README](./README.md)

## 사전 요구사항

- **Obsidian Vault** — 프로토콜 산출물 (정리, 정렬)은 Obsidian 호환 기본값
- **Claude Cowork 또는 Claude Code** 환경

## 목적

복잡한 문제는 서로 다른 사고 접근을 요구합니다. Trigger Dictionary는 어떤 도구가 필요한지 아는 것과 실제로 전체 프로토콜을 실행하는 사이의 마찰을 제거합니다. 방법론 단계를 수동으로 조합하는 대신, 도구 이름을 호출하면 모든 단계, 게이트, 산출물 구조가 포함된 완전한 사고 프레임워크를 얻습니다.

## 사용 시점 및 방법

특정 사고 방법론이 필요한 문제에 직면할 때마다 이 스킬을 사용하세요. 도구 이름을 말하세요 — Holmes, Occam, First Principles, Bayesian, Pre-mortem, Analogy, Surgical 등 — Claude가 모든 단계와 함께 전체 프로토콜을 실행합니다. 도구는 6개 카테고리로 정리됩니다 (분석, 구조, 실행, 판단, 관점, 전환), 상황에 맞는 올바른 접근을 쉽게 찾을 수 있습니다. 입력 → 도구명 → 구조화된 산출.

## 사용 예시

| 상황 | 프롬프트 | 결과 |
|---|---|---|
| 엄밀한 제거 논리 필요 | `"이 결정에 Holmes 적용"` | 관찰→가설→제거 프로토콜; 제약 식별; 대안 축소 |
| 복잡한 해결안 단순화 | `"이 문제에 Occam 적용"` | 최소 가정 식별; 중복 제거; 가장 단순한 설명 도출 |
| 기본 원리부터 구축 | `"우리 접근에 First Principles 적용"` | 가정 분해; 공리 식별; 핵심 진리로부터 해결안 재구축 |
| 불확실성 하의 평가 | `"이 시장 가정에 Bayesian 적용"` | 사전 확률→증거 강도→사후 추론; 신뢰 구간 계산 |
| 숨겨진 실패 모드 식별 | `"이 출시에 Pre-mortem 적용"` | 미래 실패 시나리오 매핑; 실패 원인 진단; 완화 계획 초안 |

## 핵심 기능

- 6개 카테고리 25개 사고 프로토콜: 분석 (Holmes, Occam, First Principles, Bayesian, Dimensional, Socratic, Ladder), 구조 (Pre-mortem, Analogy, Surgical, Backbone, Skeleton, SHE, Elevator Pitch), 실행 (Timestone, MacGyver, Nudge, Triage, Zoom), 판단 (Reversal, Antidote), 관점 (Thesis, Antithesis), 전환 (Stepwise, Ratchet)
- 한 단어 호출 — 도구 이름만 말하면, 전체 방법론 실행
- 명확한 단계와 검증 게이트가 포함된 사전 엔지니어링된 프로토콜
- 진단 추론과 실행 가능한 산출을 결합한 프로토콜
- 도메인 무관: 전략, 제품, 채용, 파트너십, 운영

## 연관 스킬

- **[planning-skill](https://github.com/jasonnamii/planning-skill)** — planning-skill이 단계 조율; trigger-dictionary가 각 단계 내 사고 도구 제공
- **[research-frame](https://github.com/jasonnamii/research-frame)** — research-frame이 다축 조사 구조화; trigger-dictionary 도구가 개별 축 분석 담당
- **[deliverable-engine](https://github.com/jasonnamii/deliverable-engine)** — deliverable-engine이 산출 패키징; trigger-dictionary가 엄밀한 콘텐츠 생성
## 설치

```bash
git clone https://github.com/jasonnamii/trigger-dictionary.git ~/.claude/skills/trigger-dictionary
```

## 업데이트

```bash
cd ~/.claude/skills/trigger-dictionary && git pull
```

`~/.claude/skills/`에 배치된 스킬은 Claude Code 및 Cowork 세션에서 자동으로 사용할 수 있습니다.

## Cowork 스킬 생태계

25개 이상의 커스텀 스킬 중 하나입니다. 전체 카탈로그: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## 라이선스

MIT 라이선스 — 자유롭게 사용, 수정, 공유하세요.
