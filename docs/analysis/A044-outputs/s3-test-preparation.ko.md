# S3-PREP-A044 — TEST 준비·후보 비교·현재 계약 감사

상태: **PROPOSED / SEPARATE_USER_INSTRUCTION_REQUIRED**.
S0 작성은 S3 재개가 아니다. 사용자가 이 별도 S3 채팅에 범위 실행을 지시할 때만 시작한다.
작업 폴더 `C:\Users\USER\Desktop\SimulacraBench`.
기준 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; 현재 dirty는 보존한다.

## 목적과 권한

E041 잠정 기준 후보/E025 대안을 바탕으로 **지금 TEST 준비에서 무엇을 재사용하고
무엇을 보완해야 하는지** 확정한다. 최종 모델 확정·업로드는 제외한다.
A018의 selected, frozen selection 문구는 과거 세션 기록이다. 사용자 최종 확정이 아니다.
E064는 completed S1/parked이며 TEST 비교군에 자동 추가하지 않는다.

이번 S3는 문서·공개 규칙·정적 source·기존 증거/산출물 식별 점검만 수행한다.
신규 gross90분, 마지막15분 closeout. 새 지출/credits0, 모델/fit/predict/score/fixture/
checker/phase2 재실행0. 새 패키징·PDF 렌더·설치·remote compute·subagents·commit/push0.
Phase2 재검증이 필요하면 이번 작업에서 정확한 실행 목록/새 예산안을 산출하고 S0로 반환한다.
모든 과거 성공 검증을 습관적으로 다시 돌리지 않는다.

AGENTS → CLAUDE → status → log 최신3개 → workflow r6 → 이 문서를 읽고 receipt를 남긴다.
S0 A044 verification/ownership release 확인 후 writer를 단독 인수한다. 이전 owner가
작업 중이면 쓰지 않는다. 현재 HEAD/branch/dirty/named jobs를 기록한다.
최종 해제 후 B01 실행 세션이 writer를 인수하도록 안내한다. 같은 checkout 동시 수정 금지.

## 읽을 기록·허용 입력

- A044 decision/entry/official-rules-snapshot 및 ownership.
- docs/phase2-preparation.md, docs/method-4p.md,
  docs/analysis/A012-phase2-baseline-and-calibration-gate.md,
  docs/analysis/A013-probe-resolution-and-method.md,
  docs/analysis/A018-test-selection.md.
- docs/analysis/A012-outputs/, A013-outputs/, A018-outputs/의 **문서·JSON manifest·
  resource/checker/official 로그·실행 source 텍스트**. Raw arrays는 제외.
- submissions/phase2-E041-preparation/, phase2-E025-preparation/의 SCORES/verification/
  provenance/방법 Markdown·PDF. 원래 PDF의 읽기/시각 검토는 가능, 생성·수정은 하지 않는다.
- submissions/2026-09-25-E041/ 및 2026-09-25-E025/의 main.py/notice/method PDF·문서,
  두 동명 ZIP의 **읽기 전용 bytes/hash/목록/main·notice 식별**. 실행/변경/재압축 없음.
  ZIP의 그 외 model/cache member는 로드하지 않는다. 역사 hash는 A018 freeze-manifest를 따른다.
- E041/E025 직접 의존 source, 현재 로컬 kit 공개 README/config/score/schema/checker/
  requirements/license와 git metadata. 외부 checkout 업데이트/환경 설치는 하지 않는다.
- E062/E063 post-result 및 E064 closeout/verification/freeze/score 비교 JSON,
  submissions/SCORES.md의 기존 공개 값. 새 후보 평가나 새 점수 계산 없음.

모든 response/Parquet/NPZ/key/모델cache/VAF 접근·재해시·역직렬화 금지.
Manifest는 그런 파일을 여는 허가가 아니다. Phase2 input/raw hash를 이번에 다시
확인하지 않았다면 **역사 증거 승계**로 표시하며 현재 complete parity라고 주장하지 않는다.

## 작업 1 — 현재 공식 규칙·일정·kit 영향

공식 공개 위치만 조회한다. 로그인/계정/신청/연락/업로드 없음.

- https://simulacrabench.org/
- https://www.codabench.org/competitions/17822/ 및 공개 competition API/Terms
- https://github.com/SituatedEvals/public 의 README/config/score/schema/checker/license,
  관련 공개 history/diff와 고정 commit.

최대30개 고유 공식 문서/metadata 경로, 총25분을 이 조회에 배정한다. 예산은90분에 포함.
문서 취득은 작은 text/JSON만 새 s3-prep에 보존하며 dataset/모델/실행파일 취득은 없다.
인증이 필요한 항목은 공개 확인 실패로 남기고 나머지 준비를 계속한다. 반복 검색/자동 문의 없음.

2026-10-22 S0 관측은 DEV Nov13 / Final Nov14–18,900/3600초다. 옛 A018 Nov1–14와
다르며 현재 Terms와 정확한 플랫폼 timestamp/timezone은 아직 확인하지 못했다.
출처·조회시각·적용 phase·정확한 원문 날짜·UTC/KST 변환 근거를 구분한다. 날짜만 있으면
임의 00:00/end-of-day로 바꾸지 않는다. 과거 Nov12 cutoff/Nov13 upload 목표도 현재
등록된 일정으로 자동 적용하지 말고, 확인한 공식 종료보다 앞선 내부 마감안을 제안한다.

현재 website의 winning-team method 요약과 옛 Terms의 every TEST entry 의무를 대조한다.
현재 약관 미확보면 의무 확정은 보류하되 method 초안 작업은 계속한다.
주최측 visible-row runtime fitting 허용이 이미 해소된 이력은 보존한다.

Kit의 옛 commit/로컬 현재/공식 현재 pinned revision과 변경을 비교한다. B01에도 필요한
공통 비교표: schema item/options/order/gate/split, mask/roles, runtime schema 정규화,
floor/normalization/pooled denominator, API/requirements, shared clock/CPU/RAM/offline.
README/date/새 generator 기본값 변경과 모델/평가 의미 변경을 구분한다. 생성기 변경만으로
과거 고정 synthetic 검증이 없었던 일이 되지는 않으며 자동 재생성하지 않는다.
확인 못한 source parity는 unknown으로 남긴다. Latest README 열람만으로 hash equality라고 쓰지 않는다.

## 작업 2 — A012/A018 phase2 유효성 표

모델별 source/snapshot/archive/PDF/input/scorer/환경/실행 로그/자원/순서 parity 항목마다
다음 중 하나를 기재한다: 현재 identity 확인, 역사 증거 재사용 가능, 계약 변경으로 무효,
현재 확인 불가. 현재 byte 확인과 과거 metadata를 별도 열로 둔다.

역사 근거:
- E041: A012 442425 raw parity, A018 최종ZIP phase2 공식 약359.45초/포함364.34초,
  shared-process rehearsal336.55초. 이는 기존 CPU/fixture 결과로 hosted 보장이 아니다.
- E025: A018 rehearsal332.78초/assembly-to-frozen-assembly equality. 옛 official은
  raw/scorer/data provenance가 약하며 fresh official raw-parity 자격으로 확대하지 않는다.
- A012의 평가 전 raw 동결 미흡/나중 provenance, A018 동시작업 중단·post-run guard
  보완을 숨기지 않는다. 옛 성공/실패·한도·source를 바꾸지 않는다.

새 실행 필요 여부는 변경된 경계에 연결한다. 시간이 지났다는 이유만으로 재학습하지 않는다.
E025 provenance 부족도 정확한 gap으로 기술한다. 단지 이미 문서에 알려진 gap을 반복
발견했다고 새로운 실패로 세지 않는다. 다음 실행이 필요하면 후보·입력·stage·재사용/
새 all3 횟수·shared3600초/전체자원·비교 기준·no tuning 범위의 계획을 작성한다.
이번 S3에는 그 실행 예산이 없다. A018 소진 예산을 되살리지 않는다.

## 작업 3 — 후보 비교·방법·라이선스 초안

E041/E025만 비교한다. DEV 공개값, 독립 실증 한계, phase2 TRAIN+DEV refit의 역할/
bank/선택/replay 변화, calibration 낙관성, activation/fallback, 비용/의존성,
실제 TEST 근거 없음과 장애 시 대안을 표로 만든다. DEV 최고점만으로 확정하지 않는다.
E062/E063 tie는 효과0가 아니며 E064 기술 PASS도 TEST 승격 사유가 아니다.

새 s3-prep/method-e041-draft.md, method-e025-notes.md를 작성한다. 원래 method/PDF는 보존.
주요 수정: selected→provisional, 현재 일정/공개 API 정밀도·출처, E060~E064 개발 이력의
필요한 공개, proxy/real-data/실제predictor 포함 여부, runtime fitting, native/H100 한계,
과거 retired-account disclosure와 미해결 상태. 네 페이지 구성안을 제시하되 렌더되지 않은
초안을 four-page PDF PASS라고 부르지 않는다. Snapshot에 없는 기능을 넣지 않는다.

License inventory: starter MIT notice, 두 predictor 자체 코드의 소유자 선택 대기,
runtime dependency별 upstream license, 외부 proxy/TabPFN/TabICL/VAF의 개발 사용과
실제 제출 포함 여부를 구분한다. E041/E025에 외부 응답/weight를 추가하지 않는다.
VAF 이용약관을 알아보려고 보호 응답을 열지 않는다. 기존 문서와 공식 license만 사용한다.
Scoped MIT 등 선택안과 적용 파일 범위는 초안으로 남기고 사용자의 grant를 대신하지 않는다.
현재 의무의 확인과 법률적 보장/새 재배포 허용은 구분한다.

## 산출물·종료

쓰기: docs/analysis/A044-outputs/s3-prep/ 아래 entry, rules-and-schedule,
kit-compatibility, phase2-validity, candidate-comparison, method 초안, license-inventory,
필요 시 revalidation-plan, exposure/preservation/verification/closeout.
Status/log 및 docs/phase2-preparation.md의 **현재 상태 안내**만 갱신 가능하다.
Historical A018/A012/manifest·model/source·oldsnapshot/PDF/ZIP·tree·method-4p.md는 변경 금지.

판독:
- 문서/계약 비교 완료: DOCUMENT_PREPARATION_COMPLETE. B01 release 계약의 호환/비호환/
  미확정을 명시한다. 전체 phase2 current PASS나 TEST 최종 선택을 뜻하지 않는다.
- 새 실행 필요: 정확한 revalidation 범위와 신규 예산을 제안하고 S0 반환.
- 공개 근거 일부 미확보: 확보한 초안·유효성 표까지 완료하고 특정 누락 입력만 남긴다.
  사용자의 계정 화면 정보가 꼭 필요한 경우에만 항목을 좁힌다. 메일을 자동 필수화하지 않는다.
- 일반 문서 도구 오류는 같은90분 안에서 수정하고 관련 출력만 확인한다.

마지막에 소유 경로·작업/PID·미완료 항목·시간·writer 해제를 기록한다. B01은 그 인계를
읽은 뒤 별도 사용자 실행 지시로 시작한다. 자동 실행/최종 모델 확정/업로드 없음.
E041/E025, 모든 parked/STOP/HOLD·A_half 비승격·A018 미확정·노출17999/12339·집계·A022,
E059 소비1918/1124·2007/1130·보호2074/1177·calibration1866 유지.
