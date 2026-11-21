# S3-E025-PROVENANCE-A044 — 별도 실행 제안

**PROPOSED / USER_EXECUTION_INSTRUCTION_REQUIRED.** 문서 작성은 실행 허가가 아니다.
사용자가 이 범위를 별도 S3 채팅에 실행 지시하면 아래 유한한 기술 작업을 수행한다.
S0/B01의 연장이나 최종 TEST 선택이 아니다. 서버 복구를 기다릴 필요는 없다.

## 진입과 목적

작업 폴더 `C:\Users\USER\Desktop\SimulacraBench`.
기준 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`. Dirty 원본 보존.
AGENTS/CLAUDE/status/log 최신3개/workflow r6를 읽고 역할·읽기·범위 receipt를 남긴다.
다음 문서를 읽는다:

- 이 폴더 decision.md, verification.json, proposed-input-identities.json.
- A044-outputs/s3-prep/{closeout,phase2-validity,kit-compatibility,revalidation-plan}.md.
- docs/analysis/A012-phase2-baseline-and-calibration-gate.md 및
  docs/analysis/A012-outputs/{README,final-review}.md.
- submissions/phase2-E041-preparation/{verification,supplemental-verification}.json.
- docs/analysis/A018-outputs/{freeze-manifest,preflight}.json 및 관련 기존 결과 요약.

실제 사용자 실행 지시, 현재 HEAD·dirty·named jobs·이전 writer 해제를 확인한 뒤
**S3-E025-PROVENANCE-A044**로 단독 인수한다. 소유권 충돌 시 타 세션을 종료하지 않는다.
현재 모델과 결과 파일을 과거 manifest에 맞춰 되돌리지 않는다.

문제: A018 E025 fresh parity는 assembly 대 frozen assembly이고, 옛 official 결과에는
raw/scorer/data 결합과 작은 UNICEF/WB drift의 설명이 부족하다. **미변경 E025 modular
source 대 보존 archive의 phase2 전체 raw 연결**을 새로 확인한다. E041 전체 학습이나
이미 통과한 S1/phase1 검증 반복은 하지 않는다. 합성 TEST는 과거 노출된 공학 자료이며
실제 비공개 TEST와 다르다. 이 작업으로 새 독립 audit이나 효과를 주장하지 않는다.

## 허용 자료·변경 범위

정적 source: src/models/hh_cap.py 및 실제로 추적한 직접 의존 closure, 해당 package
marker, 원래 official make_sandbox/config/schema/scorer/checker. 먼저 closure를 파일
목록으로 고정한다. 옛 manifest의 전체 src 목록을 읽기/해시 허가로 사용하지 않는다.

기준 E025 main은 submissions/2026-09-25-E025/main.py:
`00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9`.
같은 날짜 E025.zip은11240bytes:
`142921c3ea843c653821cf06a8b3fab89e8e6c96592581590f7e970064d90c6f`.
이 ZIP과 직접 member는 읽기·새 임시 경로 추출만 허용한다. 변경/재압축하지 않는다.
E041 main.py의 정적 identity 확인은 허용하되 E041 ZIP/모델 실행은 하지 않는다.

수치 입력은 **proposed-input-identities.json의 정확한9개**만 허용한다:

- 기존 synthetic respondents.parquet3개.
- A012 E041 {unicef,world_bank,unhcr}-source.json3개와
  E041 {unicef,world_bank,unhcr}-official-predictions.json3개.

입력 목록 basis SHA256:
`5208da8abaf5a37496f382f57b814a6101296c723b41a4877095c333f9aa9775`.
이는 supplementary 문서 해시다. 이 S0는9개 실제 입력 바이트를 확인하지 않았다.
실행자는 exact allowlist를 동결하고 historical hash/current identity·완료 provenance를
대조한 뒤 접근한다. 다른 E025 old raw/E064/NPZ/cache/VAF/Adult/SIPP/원천 키는 제외한다.

이번 명시적 S3 범위에서만 synthetic phase2 TRAIN+DEV visible 및 TEST GIVEN/order
읽기를 허용한다. Model entry 전에 모든 TEST PREDICT를 mask한다. Source 비교 평가의
synthetic TEST truth는 source all3 raw/source/input/order 동결 뒤 전용 evaluator만
읽는다. Stock official scorer는 원래 순서대로 truth를 소유하되 predictor에는 masked
frame만 전달한다. 그 내부 scoring 순서를 바꾸거나 official 실행 전체를 truth 미열람으로
표현하지 않는다. Official raw 회수·동결 뒤에 외부 parity/비교를 수행한다. 새 synthetic 생성 금지.

새 코드·검사·출력은 docs/analysis/A044-outputs/s3-e025-provenance/와
tmp/a044-e025-phase2/에만 작성한다. 기존 source/snapshot/manifest/방법/PDF/ZIP/tree를
수정하지 않는다. 상태·종료 후속 기록은 소유 기간의 status/log/phase2-preparation 안내에
추가 가능하다. 새 E번호·새 제출물 없음.

## 실행 순서와 진입 gate

1. 외부 조회 없이 기존 pinned kit compatibility를 재사용한다. 현재 schema/config/
   masking/order/floor·직접 source·환경·역할·completed raw receipt를 확인한다.
   E041 raw의 exact reuse 근거가 부족하면 **모델 시작 전에** missing-input closeout.
   환경 미기록을 임의 복원하거나 E041 fresh run으로 구제하지 않는다. 사후 수집된
   A012 provenance를 사전 동결이었다고 쓰지 않는다. 날짜/docstring 차이만으로 차단하지 않는다.
2. 새 driver/observer의 필요한 경계만 검사한다. 기존 성공 suite 재실행 없음. 실행 전
   source/data/scorer/order/environment·예산·시도 latch를 동결한다. 원래 science 정책을
   변경하지 않는 adapter/관측기 수리는 같은 세션에서 수행한다.
3. **E025 modular source phase2 all3 한 번**. 같은 원래 parameters/seed/refit/선택/
   lambda 유지. 모든 raw를 먼저 저장·동결하며 subgroup/head 진단은 하지 않는다.
4. **보존 E025 archive 추출본 stock official phase2 all3 한 번**. 삼기관 합계 shared
   900초. 이 출력으로 source/archive parity·전체 비용도 확인한다. 별도 parity fit 없음.
   동일 archive member equality와 기존 stock checker PASS의 byte/source 근거를
   이번 certificate에 연결한다. 동일 ZIP·checker의 성공 검사는 반복하지 않는다.
   그 certificate에 실제 무효화가 확인되면 이유를 기록하고 checker 최대1회만 허용한다.
5. 442425 ordered vectors(41676/92112/308637), shape/finite/nonnegative/positive sum,
   raw exact source/archive, official all3, 자원 기준을 확인한다. Qualified frozen E041
   raw와 같은 truth/order/floor.001로 기관별 absolute skill 차이<=.002를 평가한다.
   단순 aggregate 일치로 raw/provenance 적격성을 대신하지 않는다.

PASS는 **LOCAL_E025_PHASE2_PROVENANCE_COMPLETE_FOR_S0**다. 실제 TEST 우위·선택·
현재 private hosted image 동등성은 아니다. Parity/경계/자원 실패는 해당 certificate를
막는다. 유효한 불리한 결과를 반복하지 않는다. 비교값 부재는 INCOMPLETE로 남긴다.
역사 E025 fallback 기록을 지우거나 자동 E041/E025 선택하지 않는다.

## 신규 예산·수리·종료

- Gross120분, 마지막15분 종료/기록. 이전 B01/A018/S3 소비 예산과 별개다.
- 계산2700초 합계: 준비/검사/checker/평가/실패/수리 포함. Nested 시간 중복 합산 없음.
- 정상 all3 시작2회, 무효 arm의 일반 구현 수리 재시도 최대1회, 전체3회 이내.
  각 all3 공유900초(import·삼기관·출력/driver 포함), 한도 초기화 금지.
- 새 영향 검사/수리 최대3cycle·계산120초, 위2700초에도 포함. 성공 suite 반복 없음.
- CPU numerical2/가능한 affinity2, GPU0/heavy1, 소유 tree RSS/private 각각8GiB.
  실행 전부터 monitor, 최종 sample 포함 판정, 실제 sample gap/peak 의미 기록.
  초과하면 소유 tree만 종료하고 잔여 PID 확인. 대기/기록 시간을 숨기지 않는다.
- 현금/credit0. 기존 로컬 환경만. 설치/클라우드/H100/모델 취득/원격은 금지한다.

역사 E025/E041 shared rehearsal 약333/337초를 참고한 한도이며 완료시간 보장이 아니다.
Ordinary helper 오류는 고정 범위·한도 안에서 원인 수리 후 영향 검사만 수행한다. 원래
모델 정책 불일치·새 자료/기준/예산 필요·cap 소진이면 S0 반환한다. 예비 작업은 구체적
missing-input/failure closeout뿐이다. 정상 종료를 위해 기준을 낮추지 않는다.

산출물: entry/권한·소유권, input/source/env freeze, baseline reuse 표, 새 output
hashes, source/archive parity, official/E041 비교, 자원·호출·시도·수리 장부,
노출·보존·closeout·S0 인계·jobs/쓰기 해제. 기존 성공은 역사로 유지한다.
자동 제출/TEST 선택/새 후보/서브에이전트/commit/push·사이트 폴링은 하지 않는다.

E041 incumbent/잠정 TEST 기준, E025 대안, E064 DEV 대기/parked 및 모든 parked/STOP/HOLD,
17999명/12339SSUID·집계/A022 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866, A_half 비승격/A018 사용자 미확정 유지.
