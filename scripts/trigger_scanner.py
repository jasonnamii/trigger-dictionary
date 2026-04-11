#!/usr/bin/env python3
"""
trigger_scanner.py — 트리거 사전 자동 스캐너

두 가지 기능:
1. trigger_scan(text) — 입력 텍스트에서 25개 트리거 + 8개 콤보 발동 조건 매칭 (모순기술→triz 스킬 리다이렉트)
2. submission_clean_scan(filepath) — 제출청소 13축 grep 패턴 일괄 실행 + 13행 테이블 생성

표준 라이브러리만 사용 (re, json, pathlib, sys).
"""

import re
import json
import sys
from pathlib import Path
from typing import NamedTuple


# ============================================================
# §1. 트리거 발동 조건 정의
# ============================================================

# P1 키워드 → 트리거 매핑 (정확 매칭 + 변형)
TRIGGER_KEYWORDS: dict[str, list[str]] = {
    # 분석 7 (모순기술→triz 스킬로 이관)
    "홈즈": ["홈즈"],
    "오컴": ["오컴"],
    "제1원리": ["제1원리", "제일원리", "첫번째원리"],
    "베이지안": ["베이지안", "베이즈"],
    "엄브렐러": ["엄브렐러"],
    "아날로지": ["아날로지"],
    "연역수렴": ["연역수렴"],
    # 구조 7
    "외과적": ["외과적"],
    "수정4": ["수정4", "수정레벨", "수정 레벨", "EDIT4"],
    "백본": ["백본"],
    "스켈레톤": ["스켈레톤"],
    "SHE": ["SHE"],
    "엘베피치": ["엘베피치"],
    "타임스톤": ["타임스톤"],
    # 실행 5
    "맥가이버": ["맥가이버"],
    "넛지": ["넛지"],
    "제출청소": ["제출청소"],
    "이쁘니": ["이쁘니"],
    "작업설계자": ["작업설계자"],
    # 판단 2
    "프리모르템": ["프리모르템"],
    "트리아지": ["트리아지"],
    # 관점 2
    "줌": ["줌"],
    "절대자": ["절대자"],
    # 전환 2
    "부작업": ["부작업"],
    "주작업": ["주작업"],
}

# P2 구문 패턴 (자연어 호출)
TRIGGER_PHRASES: dict[str, list[str]] = {
    "홈즈": [r"홈즈로\s*분석"],
    "백본": [r"백본\s*잡아"],
    "트리아지": [r"트리아지\s*해"],
    "제1원리": [r"제1원리로"],
    "프리모르템": [r"프리모르템\s*돌려"],
    "엘베피치": [r"엘베피치로"],
    "스켈레톤": [r"스켈레톤\s*뽑아"],
    "제출청소": [r"제출청소\s*해"],
    "이쁘니": [r"이쁘니\s*해"],
    "작업설계자": [r"작업설계자"],
    "수정4": [r"수정4로", r"수정\s*레벨\s*판정"],
    "부작업": [r"부작업\s*할게"],
    "주작업": [r"주작업\s*복귀"],
}

# P3 유의어/간접 표현 패턴 (정규식, 트리거명 없이 개념을 표현하는 자연어)
# LLM 퍼지 매칭을 대체하기 위한 확장 — 매칭 시 "semantic" 타입으로 보고
TRIGGER_SEMANTIC: dict[str, list[str]] = {
    # === 분석 7 (모순기술→triz 스킬로 이관) ===
    "홈즈": [
        r"단서.*추론", r"추론.*단서", r"관찰.*추리", r"증거.*역추적",
        r"가설.*검증", r"역방향.*추론", r"원인.*역추적",
    ],
    "오컴": [
        r"불필요한\s*가정.*제거", r"가장\s*단순한\s*설명", r"단순.*우선",
        r"복잡.*제거", r"간결.*원칙", r"최소\s*가정",
    ],
    "제1원리": [
        r"근본부터\s*따", r"처음부터\s*다시\s*생각", r"기본\s*전제.*재검토",
        r"본질.*돌아가", r"원점.*재검토", r"공리.*출발",
        r"기존\s*프레임.*벗어나", r"전제.*해체",
    ],
    "베이지안": [
        r"사전\s*확률.*업데이트", r"새\s*정보.*확률.*조정",
        r"증거.*비추어.*확률", r"사후\s*확률", r"우도\s*비",
        r"신뢰도.*업데이트", r"가능성.*갱신",
    ],
    "엄브렐러": [
        r"상위\s*개념.*묶", r"공통\s*프레임", r"전체.*조망",
        r"메타.*관점", r"포괄.*프레임", r"우산.*아래",
    ],
    "아날로지": [
        r"비유.*적용", r"유사\s*사례.*참고", r"다른\s*분야.*빌려",
        r"메타포", r"유추.*통해", r"비슷한\s*패턴",
    ],
    "연역수렴": [
        r"가설.*수렴", r"다축.*교차.*검증", r"여러\s*증거.*수렴",
        r"삼각\s*검증", r"복수.*축.*일치", r"교차\s*확인",
    ],
    # === 구조 7 ===
    "외과적": [
        r"최소.*변경.*최대.*효과", r"정밀.*수정", r"부작용\s*없이.*수정",
        r"핀셋.*수정", r"외과.*수술.*하듯", r"surgical",
    ],
    "수정4": [
        r"수정.*영향\s*범위", r"수정.*레벨.*판단", r"변경.*파급",
        r"편집.*임팩트", r"고칠\s*때.*영향",
    ],
    "백본": [
        r"핵심\s*메시지.*뭐", r"한\s*문장.*요약", r"뼈대.*잡",
        r"핵심.*관통.*메시지", r"중심\s*논지", r"스파인.*뭐",
    ],
    "스켈레톤": [
        r"목차.*뽑", r"뼈대.*구조", r"아웃라인.*잡",
        r"큰\s*그림.*구조", r"골격.*설계", r"섹션.*나눠",
    ],
    "SHE": [
        r"Simple.*Hide.*Embody", r"단순.*숨김.*드러남",
        r"표면.*단순화.*숨김", r"타이밍.*설계.*노출",
        r"겉.*단순.*숨기.*드러나", r"애플.*인터랙션.*원칙",
    ],
    "엘베피치": [
        r"30초.*설명", r"엘리베이터.*피치", r"한\s*문장.*요약.*설득",
        r"핵심.*한마디", r"짧게.*설득",
    ],
    "타임스톤": [
        r"시간.*역행.*검증", r"미래.*시점.*회고", r"사후.*관점.*검토",
        r"시간.*돌려.*보면",
    ],
    # === 실행 5 ===
    "맥가이버": [
        r"제한.*자원.*해결", r"있는\s*것.*활용", r"대안.*찾",
        r"없으면.*만들", r"제약.*돌파", r"임기응변",
    ],
    "넛지": [
        r"살짝.*유도", r"부드럽게.*방향", r"자연스럽게.*이끌",
        r"선택\s*설계", r"행동.*유도",
    ],
    "제출청소": [
        r"제출\s*전.*정리", r"최종\s*검수", r"납품\s*전.*체크",
        r"내부.*흔적.*제거", r"클린업",
    ],
    "이쁘니": [
        r"예쁘게.*정리", r"가독성.*높", r"보기\s*좋게",
        r"포맷.*다듬", r"깔끔하게.*정리",
    ],
    "작업설계자": [
        r"작업.*분해.*설계", r"태스크.*구조화", r"일.*쪼개.*순서",
        r"작업\s*흐름.*설계",
    ],
    # === 판단 2 ===
    "프리모르템": [
        r"실패.*미리.*상상", r"잘못될\s*수\s*있는", r"리스크.*사전.*점검",
        r"실패.*원인.*미리", r"최악.*시나리오",
        r"망할\s*수\s*있는", r"뭐가\s*잘못",
    ],
    "트리아지": [
        r"우선순위.*긴급", r"먼저.*해야.*할\s*것", r"급한\s*것.*분류",
        r"중요도.*정렬", r"시급.*판단", r"뭐부터\s*해야",
    ],
    # === 관점 2 ===
    "줌": [
        r"줌\s*인.*줌\s*아웃", r"확대.*축소.*반복", r"디테일.*전체.*오가",
        r"미시.*거시", r"나무.*숲", r"스케일.*전환",
    ],
    "절대자": [
        r"형의\s*프레임", r"형\s*관점.*유지", r"의뢰인.*시각",
        r"최종\s*결정권자", r"오너.*관점",
    ],
    # === 전환 2 ===
    "부작업": [
        r"곁가지.*잠깐", r"사이드.*태스크", r"잠깐.*딴\s*거",
        r"먼저.*이것.*처리",
    ],
    "주작업": [
        r"본래.*작업.*복귀", r"원래.*하던.*돌아", r"메인.*태스크.*복귀",
    ],
}

# 콤보 정의 (콤보명 → [1차, 2차+])
COMBOS: dict[str, list[str]] = {
    "미궁": ["백본", "제1원리"],
    "마비": ["트리아지", "홈즈"],
    "시야": ["줌", "절대자", "엄브렐러"],
    "벽": ["→triz", "오컴"],  # 모순기술→triz 스킬
    "카드없음": ["맥가이버", "→triz"],  # 모순기술→triz 스킬
    "장밋빛폭주": ["프리모르템", "홈즈"],
    "제출직전": ["스켈레톤", "제출청소"],
    "복잡계": ["연역수렴", "줌"],
}

# 트리거 계열 분류
TRIGGER_CATEGORY: dict[str, str] = {
    "홈즈": "분석", "오컴": "분석", "제1원리": "분석", "베이지안": "분석",
    "엄브렐러": "분석", "아날로지": "분석", "연역수렴": "분석",
    "→triz": "분석",  # 모순기술→triz 스킬 리다이렉트
    "외과적": "구조", "수정4": "구조", "백본": "구조", "스켈레톤": "구조",
    "SHE": "구조", "엘베피치": "구조", "타임스톤": "구조",
    "맥가이버": "실행", "넛지": "실행", "제출청소": "실행",
    "이쁘니": "실행", "작업설계자": "실행",
    "프리모르템": "판단", "트리아지": "판단",
    "줌": "관점", "절대자": "관점",
    "부작업": "전환", "주작업": "전환",
}

# 복합 실행 순서: 관점→분석→구조→판단→실행→전환
CATEGORY_ORDER = {"관점": 0, "분석": 1, "구조": 2, "판단": 3, "실행": 4, "전환": 5}

# "줌" false positive 방지 — 일반 용어 문맥
ZOOM_FP_PATTERNS = [
    r"줌\s*미팅", r"줌\s*회의", r"줌\s*콜", r"Zoom\s*(meeting|call|link|url)",
    r"줌\s*링크", r"줌\s*접속",
]


class TriggerMatch(NamedTuple):
    trigger: str
    category: str
    match_type: str  # "keyword" | "phrase" | "semantic" | "combo"
    matched_text: str
    position: int  # char offset


def trigger_scan(text: str) -> dict:
    """입력 텍스트에서 트리거 발동 조건을 스캔하고 결과를 반환한다.

    Returns:
        {
            "matches": [TriggerMatch, ...],
            "combos_detected": [{"name": str, "triggers": [str]}],
            "execution_order": [str],  # 복합 순서 정렬된 트리거 목록
            "false_positives": [{"trigger": str, "reason": str, "text": str}],
        }
    """
    matches: list[TriggerMatch] = []
    false_positives: list[dict] = []

    # --- P1: 키워드 매칭 ---
    for trigger, keywords in TRIGGER_KEYWORDS.items():
        for kw in keywords:
            # SHE는 대소문자 구분 (소문자 she 등 오탐 방지)
            if trigger == "SHE":
                pattern = re.compile(re.escape(kw))
            else:
                pattern = re.compile(re.escape(kw), re.IGNORECASE)

            for m in pattern.finditer(text):
                # "줌" false positive 체크
                if trigger == "줌":
                    context = text[max(0, m.start() - 5):m.end() + 10]
                    if any(re.search(fp, context, re.IGNORECASE) for fp in ZOOM_FP_PATTERNS):
                        false_positives.append({
                            "trigger": "줌",
                            "reason": "일반 용어 문맥 (Zoom 미팅 등)",
                            "text": context.strip(),
                        })
                        continue

                matches.append(TriggerMatch(
                    trigger=trigger,
                    category=TRIGGER_CATEGORY[trigger],
                    match_type="keyword",
                    matched_text=m.group(),
                    position=m.start(),
                ))

    # --- P2: 구문 패턴 매칭 ---
    for trigger, patterns in TRIGGER_PHRASES.items():
        for pat in patterns:
            for m in re.finditer(pat, text):
                # 키워드와 중복 위치면 스킵 (phrase가 keyword를 포함하므로)
                if not any(
                    em.trigger == trigger
                    and abs(em.position - m.start()) < len(m.group()) + 3
                    for em in matches
                ):
                    matches.append(TriggerMatch(
                        trigger=trigger,
                        category=TRIGGER_CATEGORY[trigger],
                        match_type="phrase",
                        matched_text=m.group(),
                        position=m.start(),
                    ))

    # --- P3: 시맨틱(유의어/간접 표현) 매칭 ---
    for trigger, patterns in TRIGGER_SEMANTIC.items():
        for pat in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                # P1/P2와 중복 위치면 스킵
                if not any(
                    em.trigger == trigger
                    and abs(em.position - m.start()) < max(len(m.group()), len(em.matched_text)) + 5
                    for em in matches
                ):
                    matches.append(TriggerMatch(
                        trigger=trigger,
                        category=TRIGGER_CATEGORY[trigger],
                        match_type="semantic",
                        matched_text=m.group(),
                        position=m.start(),
                    ))

    # --- 콤보 감지 ---
    matched_triggers = {m.trigger for m in matches}
    combos_detected: list[dict] = []

    # 직접 콤보명 호출 체크
    for combo_name, triggers in COMBOS.items():
        if combo_name in text:
            combos_detected.append({"name": combo_name, "triggers": triggers})
            for t in triggers:
                if t not in matched_triggers:
                    matches.append(TriggerMatch(
                        trigger=t,
                        category=TRIGGER_CATEGORY[t],
                        match_type="combo",
                        matched_text=combo_name,
                        position=text.index(combo_name),
                    ))
                    matched_triggers.add(t)

    # 개별 트리거 조합으로 콤보 패턴 감지
    for combo_name, triggers in COMBOS.items():
        if combo_name not in [c["name"] for c in combos_detected]:
            if all(t in matched_triggers for t in triggers):
                combos_detected.append({
                    "name": combo_name,
                    "triggers": triggers,
                    "note": "개별 트리거 조합으로 감지",
                })

    # --- 복합 순서 정렬 ---
    unique_triggers = sorted(
        {m.trigger for m in matches},
        key=lambda t: (CATEGORY_ORDER.get(TRIGGER_CATEGORY.get(t, "실행"), 99), t),
    )

    # --- 중복 제거 (동일 트리거 + 동일 위치) ---
    seen = set()
    deduped: list[TriggerMatch] = []
    for m in matches:
        key = (m.trigger, m.position)
        if key not in seen:
            seen.add(key)
            deduped.append(m)

    return {
        "matches": [m._asdict() for m in deduped],
        "combos_detected": combos_detected,
        "execution_order": unique_triggers,
        "false_positives": false_positives,
        "summary": f"{len(deduped)}건 매칭, {len(combos_detected)}개 콤보, "
                   f"{len(false_positives)}건 오탐 제외",
    }


# ============================================================
# §2. 제출청소 13축 grep 스캐너
# ============================================================

SUBMISSION_AXES: list[dict] = [
    {
        "num": 1, "name": "헤더메타",
        "pattern": r"changelog|변경이력|revision history|작성자:|author:|검토자:|승인자:|문서번호|doc.?id|draft|검토중|승인대기|내부용|대외비|confidential|internal.?only",
    },
    {
        "num": 2, "name": "체인지로그",
        "pattern": r"변경이력|변경사항|수정이력|수정내역|[Cc]hange.?[Ll]og|[Rr]evision|[Hh]istory|[Rr]elease.?[Nn]otes|이전\s*버전|기존안\s*대비|v\d+.*에서\s*(수정|변경|추가)",
    },
    {
        "num": 3, "name": "내부언어",
        "pattern": (
            # 트리거명·UP용어·스킬명·내부약어
            r"확신도|MECE|스파인|spine|트리아지|갭렌즈|절대자|C8C|DC\b|OK\b|UP\b|SHE\b"
            r"|엄브렐러|홈즈|오컴|제1원리|베이지안|모순기술|아날로지|연역수렴|외과적|백본|스켈레톤"
            r"|엘베피치|타임스톤|맥가이버|넛지|프리모르템|줌\b|부작업|주작업|제출청소|이쁘니|작업설계자"
            r"|모래시계|렌즈6|ceo-pipeline|policy-planning|bp-guide|financial-model"
            r"|UP\s*§|§[A-H]|샤워효과|TRIZ|트리즈"
            # 내부 작업 프로세스 용어
            r"|[0-9]+축|[0-9]+건\s*(수정|보강|채택|삭제|추가)|대조판정|교차검증"
            r"|독립\s*리서치|보강\s*리서치|팩트시트|팩트\s*베이스|Phase\s*[0-9]"
            r"|연역수렴\s*도출|제약\s*역전|자원\s*재조합"
            # 분석 구조 표기 (layer/층/N대 패턴 등)
            r"|[0-9]+층|[Ll]ayer\s*[0-9]|레이어\s*[0-9]"
            r"|[0-9]+[대개종]?\s*(패턴|원리|원칙|공식|렌즈|도메인|시나리오|메타원리|매트릭스)"
            r"|축별\s*(조사|분석|통찰)|L[0-4]\s*(교차|통찰|연역)|공식[①-⑥]"
            r"|스크리닝|게이트\s*(통과|판정)|폴백|스포크\s*(로드|로딩)|허브\s*스포크"
            r"|LIGHT\b|DEEP\b|낙관.?기본.?비관|도메인\s*(라우팅|어댑터|판별)"
        ),
    },
    {
        "num": 4, "name": "AI흔적",
        "pattern": r"Python검증|확신도\s*\d|Co-Authored|Claude|GPT|LLM|서브에이전트|sub-agent|Anthropic|Copilot|ChatGPT|OpenAI|AI\s*생성|generated.?by|AI.?assisted|검증\s*완료|QC\s*통과|도움이\s*되셨|추가\s*질문이",
    },
    {
        "num": 5, "name": "작업마커",
        "pattern": r"TODO|FIXME|TBD|WIP|⚠️|❓|\[ \]|HACK|PENDING|BLOCKED|미완|미정|확인\s*필요|검토\s*필요|보류|작성중|🚧|\[/\]|\[-\]",
    },
    {
        "num": 6, "name": "플레이스홀더",
        "pattern": r"\[여기에|\(추후|XXX|TBA|삽입\]|INSERT.?HERE|PLACEHOLDER|FILL.?IN|작성\s*예정|추가\s*예정|확인\s*후\s*기재|\{\{|\}\}|\[OO|lorem ipsum",
    },
    {
        "num": 7, "name": "톤/격식",
        "pattern": r"~해\b|~야\b|~거든|~잖아|ㅋㅋ|ㅎㅎ|근데\b|걍\b|도움이\s*되셨|우리가\b|내부적으로|FYI\b|BTW\b",
    },
    {
        "num": 8, "name": "코드주석",
        "pattern": r"<!--|-->|%%|console\.(log|warn|error|debug|info|table|dir)|alert\(|debugger\b|dataview|templater|<%|%>",
    },
    {
        "num": 9, "name": "프론트매터",
        "pattern": r"^---|tags:|aliases:",
    },
    {
        "num": 10, "name": "버전흔적",
        "pattern": r"_draft|_old|_backup|_사본|_검토용|_내부용|_temp|_test|_sample|Draft\s*\d|이전\s*버전\s*대비|기존안\s*대비",
    },
    {
        "num": 11, "name": "내부경로",
        "pattern": r"/Users/|/sessions/|/mnt/|C:\\\\|D:\\\\|/home/|/tmp/|localhost|127\.0\.0\.1|192\.168\.|10\.0\.|\\.internal\b",
    },
    {
        "num": 12, "name": "포맷정합",
        "pattern": None,  # 수동 대조
    },
    {
        "num": 13, "name": "숫자정합",
        "pattern": r"\d+[,.]?\d*\s*(원|만|억|조|달러|위안|RMB|USD|EUR|JPY|%)",
    },
]


class AxisResult(NamedTuple):
    num: int
    name: str
    grep_count: int
    matches: list[dict]  # [{"line": int, "text": str, "match": str}]


def submission_clean_scan(filepath: str) -> dict:
    """제출청소 13축 grep 일괄 실행.

    Args:
        filepath: 스캔 대상 파일 경로

    Returns:
        {
            "file": str,
            "total_lines": int,
            "axes": [AxisResult as dict],
            "table_md": str,  # 13행 고정 마크다운 테이블
            "flagged_axes": [int],  # 1건+ 발견된 축 번호
        }
    """
    path = Path(filepath)
    if not path.exists():
        return {"error": f"파일 없음: {filepath}"}

    lines = path.read_text(encoding="utf-8").splitlines()
    results: list[dict] = []

    for axis in SUBMISSION_AXES:
        axis_num = axis["num"]
        axis_name = axis["name"]
        pattern = axis["pattern"]

        if pattern is None:
            results.append({
                "num": axis_num,
                "name": axis_name,
                "grep_count": 0,
                "matches": [],
                "note": "수동 대조 필요",
            })
            continue

        compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        axis_matches: list[dict] = []

        for i, line in enumerate(lines, 1):
            for m in compiled.finditer(line):
                axis_matches.append({
                    "line": i,
                    "text": line.strip()[:120],
                    "match": m.group(),
                })

        results.append({
            "num": axis_num,
            "name": axis_name,
            "grep_count": len(axis_matches),
            "matches": axis_matches,
        })

    # 13행 고정 테이블 생성
    table_lines = [
        "| # | 축 | 결과 | grep 건수 |",
        "|---|---|------|-----------|",
    ]
    flagged = []
    for r in results:
        count = r["grep_count"]
        note = r.get("note", "")
        if note:
            status = f"📋 {note}"
        elif count == 0:
            status = "✅ 0건"
        else:
            status = f"⚠️ {count}건"
            flagged.append(r["num"])
        table_lines.append(f"| {r['num']} | {r['name']} | {status} | {count} |")

    return {
        "file": str(filepath),
        "total_lines": len(lines),
        "axes": results,
        "table_md": "\n".join(table_lines),
        "flagged_axes": flagged,
        "summary": f"{len(flagged)}/13축 발견, 총 {sum(r['grep_count'] for r in results)}건",
    }


# ============================================================
# §3. CLI 인터페이스
# ============================================================

def _print_trigger_result(result: dict) -> None:
    """트리거 스캔 결과를 읽기 좋게 출력."""
    print(f"\n{'='*60}")
    print(f"트리거 스캔 결과: {result['summary']}")
    print(f"{'='*60}")

    if result["matches"]:
        print(f"\n{'─'*40}")
        print("매칭 목록:")
        for m in result["matches"]:
            print(f"  [{m['category']}] {m['trigger']} — "
                  f"{m['match_type']}: \"{m['matched_text']}\" (pos:{m['position']})")

    if result["combos_detected"]:
        print(f"\n{'─'*40}")
        print("콤보 감지:")
        for c in result["combos_detected"]:
            note = c.get("note", "")
            print(f"  {c['name']} → {' → '.join(c['triggers'])}"
                  f"{' (' + note + ')' if note else ''}")

    if result["execution_order"]:
        print(f"\n{'─'*40}")
        print(f"실행 순서 (관점→분석→구조→판단→실행→전환):")
        print(f"  {' → '.join(result['execution_order'])}")

    if result["false_positives"]:
        print(f"\n{'─'*40}")
        print("오탐 제외:")
        for fp in result["false_positives"]:
            print(f"  {fp['trigger']}: {fp['reason']} — \"{fp['text']}\"")


def _print_submission_result(result: dict) -> None:
    """제출청소 스캔 결과를 읽기 좋게 출력."""
    if "error" in result:
        print(f"오류: {result['error']}")
        return

    print(f"\n{'='*60}")
    print(f"제출청소 스캔: {result['file']} ({result['total_lines']}줄)")
    print(f"결과: {result['summary']}")
    print(f"{'='*60}")
    print(f"\n{result['table_md']}")

    # 발견 건 상세
    for axis in result["axes"]:
        if axis["grep_count"] > 0:
            print(f"\n{'─'*40}")
            print(f"축{axis['num']} {axis['name']} — {axis['grep_count']}건:")
            for m in axis["matches"][:20]:  # 최대 20건만 표시
                print(f"  L{m['line']}: [{m['match']}] {m['text'][:80]}")
            if axis["grep_count"] > 20:
                print(f"  ... 외 {axis['grep_count'] - 20}건")


def main():
    """CLI: python trigger_scanner.py <command> [args]

    Commands:
        scan <text>       — 텍스트에서 트리거 발동 조건 스캔
        clean <filepath>  — 파일에 제출청소 13축 grep 실행
        json <command> [args] — JSON 출력 모드
    """
    if len(sys.argv) < 3:
        print(__doc__)
        print(main.__doc__)
        sys.exit(1)

    json_mode = sys.argv[1] == "json"
    cmd_idx = 2 if json_mode else 1
    command = sys.argv[cmd_idx]
    arg = " ".join(sys.argv[cmd_idx + 1:])

    if command == "scan":
        result = trigger_scan(arg)
        if json_mode:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_trigger_result(result)

    elif command == "clean":
        result = submission_clean_scan(arg)
        if json_mode:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            _print_submission_result(result)

    else:
        print(f"알 수 없는 명령: {command}")
        print(main.__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
