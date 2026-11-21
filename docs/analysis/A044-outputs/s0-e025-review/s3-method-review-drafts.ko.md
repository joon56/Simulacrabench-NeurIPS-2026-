# S3-METHOD-DRAFTS-A044 — E041/E025 검토용 방법 문서

**제안 인계문. 작성·열람만으로 실행되지 않는다.** 사용자가 이 파일을 별도 S3에
실행 지시로 전달한 경우에만 아래 신규 범위를 수행한다. S0를 실행 세션으로 바꾸지 않는다.
목표는 두 후보의 검토용 문서 완성이다. 최종 TEST 선택·라이선스 부여·제출 승인이 아니다.

## 진입과 소유권

작업 폴더 `C:\Users\USER\Desktop\SimulacraBench`.
기준 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`.
AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 → docs/workflow.md
순서로 실제 읽고 역할 S3/문서 작업·개정·허용 범위·workflow SHA256을 기록한다.
현재 HEAD/dirty/관련 jobs와 이 폴더 verification의 `exclusive_writer_released:true`를
확인한다. writer가 있으면 쓰지 않는다. Incoming은 `S3-METHOD-DRAFTS-A044`로 명시한다.
현재 파일을 과거 hash에 맞춰 되돌리지 않는다. 충돌이나 새 변경은 경위를 기록한다.

## 읽을 입력 — 문서와 정적 소스만

- 이 폴더 decision.md, entry.json, verification.json.
- `docs/analysis/A044-outputs/s3-prep/`의 method-e041-draft.md,
  method-e025-notes.md, license-inventory.md, rules-and-schedule.md,
  kit-compatibility.md, phase2-validity.md, revalidation-plan.md.
- `docs/analysis/A044-outputs/s3-e025-provenance/`의 closeout.md, protocol.md,
  comparison.json, baseline-reuse.json, budget-ledger.json, verification.json.
  이 문서의 raw/data/cache/ZIP 경로는 접근 허가가 아니다.
- `docs/phase2-preparation.md`, `docs/analysis/A018-test-selection.md`.
- 정확히 `submissions/2026-09-25-E041/`와 `submissions/2026-09-25-E025/`의
  method-4p.md, method-4p.pdf 및 main.py. main.py는 설명 확인용 정적 읽기만 허용한다.
  모델 import/실행 없음. ZIP은 접근·재해시하지 않는다.
- `scripts/render_method.py` 정적 읽기와 문서 전용 복사본 활용.
  기존 `.venv/Scripts/python.exe` + `tmp/pdf-deps` 문서 환경만 사용한다.
  PDF skill이 있으면 해당 지침을 읽고 적용한다. 모델 실행 지침으로 확대하지 않는다.

기존 자료의 직접 문서 인용은 위 기록이 제공하는 근거 범위에서만 사용한다.
새 웹 조사/로그인/다운로드/문의는 이번 작업에 포함하지 않는다.
정확한 Terms/시간을 확인하지 못한 상태를 숨기거나 날짜-only를 임의 시각으로 바꾸지 않는다.

## 작성할 내용

1. E041 잠정 기준과 E025 대안을 각각 설명하는 새 영문 Markdown과 **각4쪽 PDF**.
   제목/표지 영역에 `REVIEW DRAFT — NOT FINAL TEST SELECTION` 표시.
   E041 learned section metric을 E025에 잘못 포함하지 않는다.
2. E025 modular-source→preserved ZIP의442425 raw exact/official3 PASS,
   reuse gate·CPU2/각 shared900·sampled memory 근거를 반영한다.
   옛 drift·사후 A012 provenance·누락 환경·hosted 불확실성은 별도 보존한다.
   E041을 이번에 재실행했다고 쓰지 않는다.
3. E025−E041 synthetic UNHCR+.000508448996을 실제 TEST 우위나 최종 선택 근거로
   표현하지 않는다. 기관별 공개 DEV 점수는 privacy rounding/noise 범위와 출처를 명시한다.
   E064는 DEV 대기이며 실제 결과가 아직 없는 상태다.
4. Runtime fitting/refit/선택/replay 한계, 실제 외부 자료 사용과 배포 포함 여부,
   역사적 실패·개발/노출 한계·타사 notice를 보존한다. 원래 데이터 값/개별 응답은 넣지 않는다.
5. `open-decisions.md`에 팀 코드 권리자·라이선스 미결정, 최신 Terms/방법 의무와 정확한
   Final 시각 미확정, 사용자 최종 모델/계정·slot/업로드 결정을 분리한다.
   제안 MIT를 유효한 grant로 쓰거나 원본 LICENSE/notice를 수정하지 않는다.
6. 기록된 ZIP/main 식별값과 새 Markdown/PDF hash를 `document-pairing.json`에 연결한다.
   ZIP hash는 기존 완료 기록에서 승계했음을 표시한다. 원격 bytes나 업로드 인증으로 쓰지 않는다.

## 쓰기·검증 범위

새 출력 전용: `docs/analysis/A044-outputs/s3-method-drafts/`.
이미 존재하면 덮어쓰지 말고 소유권/진행 기록을 확인한다.
E041-review.md/pdf, E025-review.md/pdf, page PNG, 문서 전용 renderer 복사본,
open-decisions.md, document-pairing.json, entry.json, verification.json,
closeout.md, s0-handoff.ko.md 및 필요한 문서 작업 기록을 이 안에 둔다.
공유 쓰기는 docs/status.md·docs/log.md·docs/phase2-preparation.md 현재 안내만 허용한다.
원래 모델/문서/renderer/PDF/ZIP/A012/A018/S3 manifest/tree는 보존한다.

원본 renderer를 바로 실행하지 않는다. 출력 경로와 입력을 먼저 확인하고 새 폴더만
쓰는 복사본에서 렌더한다. 복사본은 문서 의존성만 import하며 모델/연구 도구 호출은 없다.
각 PDF의 실제4페이지 수·텍스트 추출·수식/글꼴·잘림/겹침·출처 링크·여백을 확인하고,
8페이지 모두 PNG로 렌더해 시각 검토한다. pagebreak3개만으로4쪽 PASS를 주장하지 않는다.
일반 편집/경로/레이아웃 오류는 같은 세션에서 수리하고 영향받은 문서만 다시 렌더한다.
실패본은 남기며 성공·미변경 문서를 근거 없이 반복하지 않는다.

## 신규 예산과 종료

이전 S3/B01 잔여 예산 사용0. **신규 제안** gross60분, 마지막10분은 기록·종료.
문서 subprocess 합300초(실패·추출·PDF/PNG 렌더 포함), PDF 제작 최대3회/후보·총6회.
CPU2/GPU0/동시 heavy1, 관측 tree RSS/private 각2GiB, 현금·credits0.
모델 fit/predict/score/checker/연구 tests/패키징0, 설치·원격·서브에이전트0.
제안 한도는 실측 비용 보장이 아니다. 진입 시 고정한 deadline/시도 수를 늘리지 않는다.
환경이 없거나 문서 의존성이 작동하지 않으면 설치 대신 작성한 초안과 정확한 누락을 반환한다.
범위 내 오류 수리는 유지하되 예산·새 데이터·모델·과학 기준 변경은 S0로 반환한다.

완료 조건: 두4쪽 검토용 PDF와 전체 시각검토·식별표·미결정표가 확보되면
`REVIEW_DRAFTS_COMPLETE / FINAL_DELIVERY_NOT_APPROVED`.
미완료이면 완성된 부분과 구체적 장애·소모량을 기록한다. 잔여 시간으로 다른 작업을 시작하지 않는다.
출력 문서의 비교·편집은 허용되지만 후보 점수 재계산·head/subgroup 진단·모델 최적화는 금지한다.

종료 시 dirty·owned jobs·보존 확인과 outgoing writer/해제시각/
`exclusive_writer_released:true`를 명시해 S0로 반환한다. 최종 선택·업로드·commit/push0.

E041 incumbent/잠정 TEST 기준, E025 대안, E057/E060/E061/E062/E063/E064 parked.
E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/A039/A040/all STOP/HOLD,
17999명/12339SSUID·집계·A022 원래 역할·E059 소비 oracle1918/1124/selection2007/1130,
보호 audit2074/1177/calibration1866 유지. A_half 비승격, A018 사용자 최종 확정 아님.
이 문서 작업은 과거 선택 표현을 현재 승인으로 만들지 않는다.
