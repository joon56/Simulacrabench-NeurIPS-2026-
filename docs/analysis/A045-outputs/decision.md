# A045 — S0 조정·하위 에이전트 실행 운영

2026-10-26. **운영 전환 승인 / 새로운 모델 실행 배치 미승인.**

사용자 지시: “이전처럼 다른 세션에게 인계문을 넘기면서 진행하지 않고 … 각 세션이
하던 업무를 서브 에이전트로 만들어서 자동화 … 내가 손을 대지 않아도 빠르게”.
이 지시로 수동 전달을 제거한다. S0 본체가 모델 연구를 직접 수행하는 전환은 아니다.
각 작업의 데이터·과학 정책·예산 권한은 별도로 식별하며, 승인된 범위는 반복해서 묻지 않는다.

## 운영

| 담당 | 업무 | 다음 단계 |
|---|---|---|
| Root S0 | 우선순위·고정 계약·예산·배정·산출물 검토·판독 | 승인된 다음 단계를 직접 배정 |
| S1 executor | 정보 조사·구현·한정된 검증/실험 | 사전 허용된 S2 gate를 충족하면 같은 child에서 계속 |
| S2 역할 | 고정 후보 조립·release·ZIP 또는 실제 결과 기록 | 검증된 산출물과 사용량을 S0에 반환; 업로드는 별도 |
| Reviewer | 동결 계약/소스/결과의 읽기 전용 독립 검토 | 사실·결함·미확정 조건만 반환 |
| S3 executor | 별도 승인된 TEST 비교·준비 | 최종 모델 선택·라이선스 부여·업로드 자동 수행 없음 |

필요한 역할만 활성화한다. 현재 도구의 root 포함4개 slot을 넘지 않으며, heavy job1,
전체 checkout writer1이다. 읽기 전용 조사/리뷰는 병렬 가능하지만 서로 다른 파일도
동시 쓰지 않는다. Root가 executor에 쓰기를 넘긴 동안 root 역시 읽기 전용이다.
Child의 추가 child 생성은 금지한다. Root가 실제 artifacts/출처/해시/사용량/종료를
확인하며, reviewer 동의나 메시지만으로 PASS·독립 실증을 주장하지 않는다.

인계 MD는 내부 실행 계약과 기록으로 남는다. 사용자가 복사해 전달할 필요는 없다.
작은 인자·경로·로그·구현 오류는 같은 executor가 승인된 예산 안에서 영향 검사만
수리·재실행한다. 과학적 STOP을 해제하거나 새 가설/응답 역할/기준/예산을 만들지 않는다.
범위 변경만 root로 반환하고, 추가 사용자 권한이 필요한 변경은 구체안을 한 번에 묻는다.
새 프로세스·agent·날짜로 사용량을 초기화하지 않는다. 무제한 재시도나 비활성 runtime
밖의 계속 실행을 보장하는 scheduler는 만들지 않았다.

## 실제 cutover와 소유권 결함

두 읽기 전용 child `workflow_review`, `wb_batch_readiness`를 사용자 지시 아래 실행했다.
둘 모두 쓰기·Python/모델 실행·응답/weight 접근이 없었다고 보고했다. 해당 보고는
parent의 개별 모델 실행 검증이 아니다. 현재 scope가 문서/정적 검토임을 구별한다.

기존 외부 S1-A040-C6가 실행 중인 사실을 발견해 이번 root는 파일 쓰기를 기다렸다.
사용자는 처음 대기 중이라고 답한 뒤 S1 작업 중으로 정정했다. C6 verification의
명시적 release **21:51:55.2818025 KST**, named/owned jobs0과 문서3개 해시 일치를
확인한 뒤 root가 **21:53:49.9307535 KST**에 인수했다. [entry](entry.json).

앞선 C6 인수21:28:13.1257813과 이전 S0 인수21:28:53.660791–21:32:42.770216이
겹쳤다. 이전 S0의 인수 확인이 부족했던 실제 운영 결함이다. 기존 receipt를 지워
정상 단독 운영으로 소급하지 않는다. C6가 최신 공유 문서 해시를 다시 확인하고 추가
기록을 보존했다는 결과는 승계하되, overlap이 없었던 것으로 주장하지 않는다.

이후 [orchestration-state.json](orchestration-state.json)의 현재 epoch/task ID와 root
배정으로만 child가 쓰기를 인수한다. 오래된 release/hash 일치만으로 새 소유권을
얻지 않는다. 별도 옛 채팅을 다시 시작하려면 현재 root 배정과 유효한 실행 범위를
확인한다. 상태 파일은 협조하는 에이전트의 조정 기록이며 원자적 OS lock이 아니다.
불명확한 다른 writer가 나타나면 새 쓰기/실행 배정을 멈추고 확인한다.

## 첫 자동 작업

**S1-WB-CONTRACT-A045: WB 전체76문항 TabICLv2 적용 계약 완성.**
이미 끝난 읽기 전용 준비도 검토를 반복하지 않고 구체적인 선택·역할·비용 계약으로
연결한다. 새 gross45분/모델·검사·과학0/cash0, 허용 문서·공개 schema·정적 source만.
이는 현재 사용자의 운영 자동화 요청 아래 수행하는 문서/정보 작업이며 새 E/fit 허가가 아니다.
[내부 작업 계약](wb-contract-task.ko.md). 완료 후 root가 결과를 직접 읽는다.

WB 공개 schema는9 GIVEN/76 PREDICT, scored gated30, 전체 확률 칸655,
최대K26·K>10문항19개다. 전체 gated40 중 EXCLUDE10을 scored 수에 합하지 않는다.
기존 A040 tiny K15 검증이나 UNHCR hardcoded orchestration만으로 WB PASS를 만들지 않는다.
기존 model/weight/환경 경로는 재사용 가능성만 확인했으며 현재 바이트·실행 적합성은 미검증이다.

미래 모델 배치는 명시된 입력/role, source/환경 identity, 새로운 누적 비용/시간/시도,
S1/S2 gate·판독표가 완성되면 이 채팅에서 한 번 검토한다. 이번 전환이 undefined
model implementation/fit/predict/score/ZIP·추가 설치/유료 자원을 승인한 것은 아니다.
현재는 신규 후보 없음. C6는 NOT_REPRODUCED로 종료됐으며 A040 HOLD, C7/원격 재개 없음.

## S0 결과 수용 — 내부 전달 완료

S1-WB-CONTRACT-A045의 문서4개 현재 해시와 명시적 해제
22:29:22.9883254 KST, owned/named jobs0을 확인하고 root가
22:30:47.2116287 KST에 문서 마감을 인수했다. 사용자 수동 전달은 없었다.
정보 작업은1398.721초/2700초, 모델·응답·weight·검사·ZIP·원격0이다.
[계약 closeout](wb-contract/closeout.md), [실제 receipt](wb-contract/verification.json).

**MODEL_BATCH_NOT_EXECUTION_READY / DEPLOYMENT_SPECIFIC_INPUT을 수용한다.**
WB76 정책과 신규 한도 제안은 구체화됐지만, 현재 install0 조건과 공식 scorer의
nonempty requirements 설치 경로가 충돌한다. 필수 hosted dependency/import closure도
미확정이다. 420분/9000초 제안을 지금 실행 승인 대상으로 권하지 않는다.
Root와 별도 읽기 전용 reviewer가 이 결함을 발견했고 child가 사전 gate를 수정했다.
이 gate 자체가 배포 가능성 증거가 되지는 않는다. 성공한 과학 작업을 반복하지 않았다.

다음 판단을 바꿀 최소 입력은 기존 자산만으로 성립하는 정확한 dependency/source/
license 전달 경로와 공식 실행 조건, 또는 이를 검증하는 별도 유한 격리 설치 범위다.
환경 준비에 필요한 권한·비용을 구체화하기 전 긴 fit부터 시작하지 않는다.
새 문의·유료 자원·Modal 수리·모델 배치를 자동 활성화하지 않았다. 이번 운영 변경은
완료이고 첫 연구 실행 준비는 별도 미완료다. 원격 bytes 미확정만으로 사용자 제공
공개 점수 판독을 모두 막지 않도록 기존 결과 기록의 근거 범위도 보존했다.

쓰기 해제 후 현재 writer는 없음. 다음 정보 작업은 root가 한정해 직접 배정할 수 있고,
새 모델/실행 예산은 완성된 구체 범위에 대해 이 채팅에서 한 번 확인한다. 승인된
gate·일반 수리마다 사용자에게 다시 인계문을 복사하도록 요구하지 않는다.

## 보존 결과

현행 AGENTS/CLAUDE/workflow/session-prompts를 r7로 연결하고 status/log를 추가한다.
과거 manifest/인계/실패/source/snapshot/tree는 변경하지 않는다. E041 incumbent/E025
fallback, E057/E060/E061/E062/E063/E064 parked, 모든 STOP/HOLD와17999/12339·집계·
A022 역할·E059 소비 oracle1918/1124·selection2007/1130 및 보호 audit2074/1177·
calibration1866, A_half 비승격/A018 미확정 유지. TEST·업로드·commit/push 자동 실행 없음.

운영 중에는 state와 각 dispatch/release를 따른다. 최종 검증·쓰기 해제는
[verification.json](verification.json). 파일 작성이나 agent 역할명은 실행 권한을 만들지 않는다.
