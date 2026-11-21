# A044 — 승인된 실행 배치와 별도 TEST 준비

2026-10-22 KST · S0 · DOCUMENTS_COMPLETE / EXECUTION_NOT_STARTED.
사용자의 이번 요청은 운영 문서 개정과 인계 작성이다. 이 기록은 실행 승인이 아니다.
기준 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; 실제 dirty work 보존.
진입/허용 텍스트 해시 확인은 [entry.json](entry.json), 종료 확인은 [verification.json](verification.json).

## 실제 완료 상태와 첫 배치 판단

A043 구현 인계는 **E064로 이미 실행 완료**됐다. 과거 인계문은 기록으로 남기고
다시 전달하지 않는다. E064의 S1 ten-check PASS, fresh R/H all3 각각 한 번,
6 pipeline/18 neural/16 metric과 계산 877.3776708초는 이미 소비된 역사다.
기존 1800초에서 남은 양을 새 작업에 부여하지 않는다.

고정 H는 독립 asked-only head를 학습시키되 conditional CE의 trunk 직접 gradient만
차단한다. 단순 E061 head tying 재실행이 아니다. 초기 state/forward/CE parity와
학습 후 결과 parity를 혼동하지 않는다. Metric/activity/donor/replay 경계 불변은
관측됐고 lambda 12쌍과 최종 epoch 110→121, UNHCR 132225 vectors는 달라졌다.

**추천: B01은 E064 하나의 남은 S2 release 작업만 포함.** S1 재실행 없음.

| 근거 | 반대 근거/한계 | 이번 결정에 주는 의미 |
|---|---|---|
| 고정 개입, 열 개 영향 검사, controls raw exact, 등록 기술 하한 통과 | 합성 UNHCR delta −0.00008435360179303028; 개선 없음 | 구현 불확실성을 다시 조사할 필요는 적음; 효능 채택은 불가 |
| R/H 전체 379.994/376.841초, 메모리 약 1.42GiB 이하 | local CPU 결과이며 hosted 보장 아님 | 남은 release 비용을 한정할 근거가 있음 |
| 실제 UNHCR에서 whole-policy 차이를 읽는 사전 arm 가능 | noisy/rounded DEV, 독립 audit 없음; tie 가능; E012 공동학습 이점/E061 adverse 반대 근거 | 한 고정 후보의 탐색 준비 가치는 있으나 승률/예상 점수는 제시 못함 |
| E062/E063 release 절차/완료 baseline 기록 재사용 가능 | 현재 공식 kit 및 옛 source/array provenance 확인 필요 | 무효화된 경계만 새로 검증; 동점 점수만으로 재사용 불가 |

새 가설을 추가하지 않는다. A040 cloud/종료 crash, A039 linkage 등은 이 배치 밖이다.
예비 작업은 실패·누락 조건 closeout뿐. E064 parked/E041 incumbent/E025 fallback 유지.

## 산출물 식별 검토

E064 freeze SHA256 `5e8bd2eb84b73957e10f4ca21de858c8a5743290527364c45b09beeafb42245e`.
Verification SHA256 `46a3fc310a2e8177f7465bcf23e1d3ddd06eba9aa26ca83a76656ad29376e2e6`.
`src/models/conditional_gradient.py` SHA256
`19cd35b7d0069e3244a6a89b9baec6a61e702cc80b6e3f91f1a5689926e40927`.
S0는 freeze의 허용 문서/소스 53항목을 현재 바이트와 대조했고 모두 일치했다.
그 뒤 r6 운영 문서를 의도적으로 개정한다. 새 운영 해시와 옛 과학 freeze를 구분한다.
배열/Parquet/모델 cache/ZIP은 열거나 재해시하지 않았다. 출력 hash는 원래 JSON의
기록을 승계한 것이며, executor의 제한된 입력 identity 확인을 대체하지 않는다.

## 일정·TEST 준비 우선순위

[새 공식 문서 관측](official-rules-snapshot.md)은 옛 A018 일정과 다르다.
따라서 쓰기 순서는 **S0 해제 → 별도 승인 S3 문서 준비 → B01 실행 → S0 결과 판단**.
S3의 공통 kit/계약 호환성 표를 B01이 재사용한다. 문서·일정 변화만으로 성공한
S1을 다시 돌리지 않는다. 실제 입력/출력/점수 계약 변화가 있으면 영향 범위를
특정해 S0로 반환한다. 적합성을 확인할 수 있는 동안 문서 작업은 계속한다.

- [S3 준비 인계](s3-test-preparation.ko.md): 신규 gross 90분, 모델 실행 0, 비용 0.
  현재 규칙/일정, 옛 phase2 유효성, E041/E025 비교, method/license 초안을 완성한다.
- [B01 실행 인계](batch-01-e064-release.ko.md): 신규 gross 180분, 계산 3600초,
  각 all3 900초, 최대 네 all3 시작(정상 둘 + 조건부 E025 하나 + invalid-arm 수리 하나).
  CPU2/GPU0/heavy1, RSS/private 각8GiB, 비용0. 클라우드/설치/업로드 없음.
  E063 S2 약1215초, E064 H 약377초를 근거로 여유를 둔 새 상한이지 완료 보장이 아니다.

S3는 준비/비교만; 최종 모델 선택은 사용자 소관. A018의 selected는 당시 S3 기록이며
사용자의 최종 확정이 아니다. 기존 ZIP/PDF/license proposal을 자동 제출·발효하지 않는다.
S3 실행 지시 전까지 중단 상태이며, 배치 파일 전달만으로 S3가 시작되지 않는다.

## 운영 변경과 보존

Workflow r6는 S0의 배치/예산/판독 책임, 별도 executor의 사전 승인 S1→S2 전환,
별도 S3, 단일 writer, ordinary repair/영향 검사, 범위 밖 S0 반환을 명시한다.
AGENTS/CLAUDE/templates도 연결한다. 과거 등록/성공/실패/manifest는 소급 수정하지 않는다.
이번에 누락된 주장이나 운영 기준을 채우려고 E064 성공 검사를 재실행하지 않았다.

모든 STOP/HOLD, A_half 비승격, A018 미확정, 기존 노출17999명/12339SSUID·집계·A022 역할,
E059 소비 oracle1918/1124·selection2007/1130 및 보호 audit2074/1177·calibration1866 유지.
E057/E060/E061/E062/E063/E064 parked, E062/E063 UNRESOLVED 유지.
소유권과 사용자에게 전달할 시작 문구는 [ownership.md](ownership.md)에 있다.

사용자 결정: 두 별도 범위/신규 상한을 승인해 각 세션에 지시할지 여부.
최종 TEST 모델·실제 업로드·자체 코드 라이선스 부여는 이번 결정 대상이 아니며
나중에 근거가 준비된 상태에서 따로 확정한다. 이미 해결한 설치/주최측 runtime
학습 허용을 다시 묻지 않는다.
