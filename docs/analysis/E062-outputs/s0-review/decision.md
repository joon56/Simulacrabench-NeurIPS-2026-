# E062 S0 — 고정 후보의 S2 release 검증 권고

2026-10-08 KST. **RECOMMEND_S2_RELEASE_VALIDATION**.
S1의 EXPLORATORY_SOURCE_QUALIFIED를 수용한다. E062는 parked 유지; release/실제 WB 효과/TEST 채택은 미확정이다. 이번 S0는 문서·허용 소스 검토와 기록·인계만 수행한다.

## 결정과 이유

주력은 **현재 E062 바이트를 고정한 별도 S2 조립·release 검증**이다. 사용자가 [새 S2 프롬프트](s2-handoff.ko.md)를 전달한 세션에서만 실행한다. 예비 작업은 같은 범위의 조립/검증 오류 수리와 한도 내 closeout이다. 새 모델·seed·head 탐색이나 A040 수리를 병행하지 않는다.

승리 목표에서 이번 작업의 가치는 새로운 WB 전체 절차를 실제 DEV에서 판독할 수 있는 제출 후보로 만드는 데 있다. 대상16의 합성 손실 때문에 기전의 효과 확신은 낮아졌다. 그러나 사전 기술·통제·회귀·자원 기준을 모두 충족했고, 모델이 실제로 바뀌었으며, 현재 별도의 인프라·데이터 취득 없이 남은 release 검증을 구체화할 수 있다. 합성에서 대상16 상승을 사후 필수 조건으로 추가하지 않는다. 반대로 전체 WB의 작은 상승을 순서형 head 효과로 승격하지도 않는다.

| 선택 | 판단에 주는 정보 | 비용·한계 | 결정 |
| --- | --- | --- | --- |
| 고정 E062 S2 검증 | 실제 배포 바이트가 연구 source와 같은지, 전체 공식 경로가 한도 내 끝나는지 확인; 이후 한 DEV 관측 가능 | 로컬 조립/공식 검증 필요, 실제 효과 미확정 | 주력 |
| 대상16 하락을 보고 초기화/비응답/head를 조정 | 새 후보를 만들 수 있으나 현재 자료에 대한 적응이며 원인 분리도 안 됨 | 추가 연구 등록/학습·노출; 현재 범위 아님 | 이번에 하지 않음 |
| A040 인프라 수리 재개 | E062 효과 판단과 무관 | 기존 실패 비용과 해소되지 않은 원인 | 보류 유지 |
| 즉시 채택/TEST 선택 | 뒷받침할 새 실제 결과 없음 | 기술 PASS와 효과 혼동 | 하지 않음 |

## 기록으로 확인한 사실

- [사전 등록](../registration.md)의 게이트와 [최종 검증](../verification.json)이 일치한다. comparison.json의 `PENDING_FINAL_RESOURCE_RECEIPT`는 평가기 중간 상태다. resource-summary 및 closeout-receipt가 이후 종료/자원 조건을 충족하며 최종 판정을 뒷받침한다. 중간 파일은 고치지 않는다.
- 새 검사13 PASS, clean E025/E041/candidate fresh all3 각1회, pipeline9/neural27/metric16. 아홉 출력 동결 후 공식 in-process 채점9회. 소스에서 freeze-before-truth와 TRAIN/DEV projection 경로를 확인했다. S0에서 재실행하거나 배열을 재검증한 것은 아니다.
- UNICEF/UNHCR는 E041과 raw 차이0. WB35613/39520 vectors 변화, max차이 .16004160046577454. NO_OP가 아니다.
- WB skill 차이 +.0002723771513838402; UNHCR-E025 −.0004861448473750807. 모든 기관에서 E025/E041 각각 대비 −.002 기준 통과. 이 수치는 기존 노출 synthetic에 한정한다.
- 대상16 mean log-score 차이 −.0007987550486939816, 나머지60 +.0009093584055200603. 대상 Not answered −.004408473492304696, substantive −.00039821078021481184. 대상16에 대한 부정적 관측을 보존한다.
- WB config/w는 같고 refit epoch는 E041193/E062184. 초기화·비응답 분리·trunk·선택/refit·λ를 포함한 전체 절차 비교다. 나머지60의 상승 원인을 공유 trunk 또는 epoch 중 하나로 확정할 수 없다.
- 후보357.522443초, computational children1123.1965955초, gross3540.7424854초로 등록 한도 내. RSS1.3085GiB/private1.4520GiB. 로컬 CPU2/GPU0 실측이며 hosted/H100 시간 보증이 아니다.

실제 WB 개선 확률·효과 크기·Grand 예상값·검정력은 미확정이다. 대상16 하락은 해당 합성 채널의 반대 근거이며 전체 순서형 모델 계열의 반증이 아니다. 관측 채널의 한계를 이유로 반대 근거를 무시하지 않는다.

## S2 범위와 반복을 줄이는 방법

새 조립본 all3와 ZIP 추출본 공식 all3를 각1회 계획한다. source/assembly/extracted raw189649개 exact parity, unchanged UNICEF/UNHCR, 기관별 clean E025/E041 −.002, ZIP checker, 공식 phase1 all3 shared900초와 메모리, 배포 바이트 identity와 SCORES 사전 판독이 모두 필요하다.

S1 closeout의 미래 `fresh clean ... release comparisons` 표현은 새로운 학습을 의무화하는 확정 실행 계약이 아니다. 이번 S0는 **이미 fresh·clean으로 생성한 E062 S1의 아홉 raw 출력**을 재사용하는 검증 계획으로 구체화한다. S2가 source·입력·runtime schema·역할·환경 및 해당 출력 해시의 동일성을 먼저 확인하고, 새 조립/추출 출력과 exact parity를 입증한 경우에만 기존 clean E025/E041 비교를 release에 연결한다. 이는 깨끗한 비교 기준이나 −.002 기준 완화가 아니다. 출처/동일성이 불완전하면 PASS를 만들거나 자동 baseline 재학습하지 않고 S0로 반환한다.

다음 S2에는 그 아홉 synthetic probability NPZ의 읽기/해시만 명시적으로 허용한다. 모델 cache나 다른 실험 출력까지 허용하는 것은 아니다. 현재 S0는 NPZ/Parquet를 읽거나 재해시하지 않았다.

제안 한도: gross120분/마지막10분 기록, CPU2/GPU0/heavy1, owned RSS 및 private commitment 각각8GiB, computational child 합2400초. 정상 S2 pipeline6/neural18/metric16; S1 누적과 합치면15/45/32. 구체적인 조립/검증 구현 결함이 확인된 경우에만 같은 세션에서 최대 추가 all3 상당량3pipeline/9neural/8metric을 예비로 허용하는 프롬프트를 준비한다. 총 S2 cap9/27/24와2400초는 유지한다. 추가 성공 반복·정책 변경·시간 초과 구제에는 예비량을 쓰지 않는다. checker의 작은 no-fit 호출은 따로 계수한다.

## 이후 DEV 판독의 정보 가치

비교 기준은 기존 사용자 API 기록 E041 ID933094, Development, Grand .6433333333 / UNICEF .52 / WB .49 / UNHCR .92. 현 시점 플랫폼 독립 조회는 하지 않았다. 공개 수치가 noise/rounding을 거친 값이라는 한계를 유지한다.

- 비교 가능한 결과에서 WB와 Grand가 상승하고 통제 기관 공개값이 같으면 고정 전체 후보에 유리한 noisy evidence로 S0 검토한다. 순서형 대상16의 개선·유의성·TEST 승격 증거는 아니다.
- WB/Grand가 같으면 효과 미해결, E041 유지/E062 parked. 화면 .64만으로 API tie를 판단하지 않는다.
- WB 또는 Grand 하락은 해당 실행의 불리한 관측. 서로 다른 방향이나 통제 기관 변화는 mixed/귀속 미해결로 함께 기록한다. 통제 공개점수 변화만으로 소스 누수를 단정하지 않는다.
- 실패는 technical; phase/scorer/파일/ID 출처 모순이나 필요한 점수 부재는 판단 보류. Grand 역산으로 세부 점수를 만들지 않는다.

어느 결과도 자동 채택·동일정책 재제출·seed/head/threshold 구제·S3 재개를 만들지 않는다. S2 검증 성공 후에도 업로드는 사용자가 결정한다. 현재 slot/계정 권한/원격 bytes는 미확정이다.

## 읽기·identity·보존

S0 결과 검토. AGENTS → CLAUDE → status의 현재 결정 → log 최신3개 → workflow r5 → E062 인계/핵심 기록을 읽었다. 긴 status 출력의 생략된 과거 항목까지 전부 읽었다고 주장하지 않는다. workflow SHA256 `a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23`.

18:08 KST 관측 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`, branch work/e050-submission, dirty96, named Python/pythonw/uv jobs0. 원격/다른 채팅 부재의 증거는 아니다. S1 entry의 읽기/권한 증거는 **session-reported**로 분류하며 그 채팅 transcript를 직접 인증했다고 주장하지 않는다.

현재 허용 source35·문서 metadata37·실험 기록1, 총73해시가 S1 manifest와 일치했다. Parquet3/NPZ9는 명시적으로 제외했다. 새 S0 기록과 status/log 추가 외 기존 연구/source/snapshot/tree를 변경하지 않는다. 상세 보존은 verification.json에 기록한다.

E041 incumbent/E025 fallback; E057/E060/E061/E062 parked. 모든 STOP/HOLD, E058/E059/A039/A040 및17999/12339·집계·A022 역할·E059 소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177·calibration1866 보존. A_half 비승격/A018 사용자 미확정/S3 중단. S2 검증 대상은 권고됐지만 release-qualified 후보/ZIP은 아직 없다. S0 fit/predict/score/test/보호자료/원격/ZIP/commit/push/서브에이전트0.
