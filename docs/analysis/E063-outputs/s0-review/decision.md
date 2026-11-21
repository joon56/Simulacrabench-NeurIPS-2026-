# E063 S0 — 고정 round metric의 release 검증 권고

2026-10-09 KST. **RECOMMEND_S2_RELEASE_VALIDATION**.
S1의 LOCAL_TECHNICAL_PASS_FOR_S0를 수용한다. 고정 E063 한 후보의 별도 S2 조립·검증을
권고하며, 실제 DEV 제출·incumbent·TEST 선택은 아직 결정하지 않는다.
[별도 S2 완성 프롬프트](s2-handoff.ko.md). 작성 자체는 실행 허가가 아니다.

## 진행할 이유와 반대 근거

새 개입이 실행됐음은 확인 가능하다. 합성 F/S의 두 round 지원 조건을 만족했고,
H 7/8 section이 자연 활성됐다. R와 활성 집합은 같으나 UNHCR46405개 raw vector와
37문항 lambda가 달라졌다. UNICEF/WB는 raw exact0이고 H all3는327.633190초였다.
이제 질문은 같은 동작을 실제 제출 파일로 보존할 수 있는지다.

반면 **합성 skill +0.0000175788678469를 실제 이득의 증거로 삼지 않는다**.
16개 section×wave 중8개 하락, selector/proxy mismatch, in-sample base/replay,
이미 노출된 synthetic이라는 한계가 남는다. 독립 audit·유의성·예상 Grand는 없다.
합성 효과 크기를 게시 점수의 반올림 단위와 직접 비교해 hosted 동점을 예측하지도 않는다.

권고 근거는 큰 개선의 입증이 아니라, 고정·활성·비무변경인 다른 정책이 기술 기준을
통과했고 추가 확인을 bounded CPU release 작업으로 한정할 수 있다는 점이다.
현재 입력으로 E062 구제·A040 crash 조사·VAF 의미 가정을 다시 여는 것보다 다음 판독이
구체적이다. 이미 쓴 비용이나 빈 제출 slot 자체는 근거가 아니다.
현재 검토한 경로 사이의 우선순위이며 전역 최선·우승확률을 주장하지 않는다.

향후 비교 가능한 hosted favorable은 전체 정책에 유리한 noisy evidence,
tie는 미해결이며 이 고정 정책의 추가 우선순위를 낮춤, decline은 해당 실행 adverse다.
어느 경우도 동일 정책 자동 재제출·seed/head/threshold 구제를 하지 않는다.
따라서 이 한 번의 경로는 실제 정책에 대한 판단을 바꿀 수 있지만 TEST 승격을 보장하지 않는다.

## 검토한 근거와 한계 처리

[등록](../registration.md), [종료](../closeout.md), [검증](../verification.json),
[비교](../attempts/score-01/comparison.json), [동결](../freeze-01.json),
[구현](../implementation-contract.md), [노출](../exposure-ledger.md)와 생산 소스를 대조했다.
고정 objective/두 wave dispatch/F-only metric slice/원래 fallback·controls 연결에
등록과의 모순을 찾지 못했다. 이번 S0가 테스트·예측·채점을 재실행한 것은 아니다.

- R/H 각각 fresh all3,6pipeline/18neural/16metric, 재시작0. 전체 computational
  754.551699초/1800, RSS1.3000/private1.4232GiB. 실패 검사 포함, 중첩 시간을 합산하지 않았다.
- 비교 파일의 PENDING_RESOURCE_RECEIPT는 당시 단계 판정이다. 후속 resources/ledger/
  verification/final-receipt가 완료와 한도 내 결과를 기록하므로 최종 기술 판정과 충돌하지 않는다.
- 최초 RED와 observer 인자 수정은 보존됐다. diff는 관측기 위치 수정이며 모델·정책 변경이 아니다.
- 0.1초 polling과 peak 합산 기록은 있으나 최대 실제 scheduler gap은 미기록이다.
  관측된 peak를 연속 시간의 절대 메모리 상한 증명으로 쓰지 않는다. 이를 새 성공 suite
  재실행 사유로 만들지 않고, S2 새 측정에서 실제 gap/시작·종료·계수 경계를 기록한다.
- 빈 package marker3개의 사후 보충은 최초 freeze에 없었다는 한계를 남긴다.
  현재도 empty SHA와 일치한다. 이를 사전 기록으로 소급 수정하지 않는다.
  새 S2 manifest에서는 import 경계에 포함한다.
- S1 read receipt는 도구 chunk가 있는 session-reported 근거이며, 이번 S0 실제 읽기와 구별한다.
  S0에서 기존 허용 소스/문서/marker63개 해시와 S1 산출 문서16개를 대조해 모두 일치했다.
  NPZ/Parquet/ZIP/cache는 열거나 해시하지 않았다.

## 중복 학습을 줄이는 release 설계

현재 문서상 E062 clean E025/E041의 phase1 frame/schema/order/mask/role 메타데이터와
E063의 해당 메타데이터는 세 기관 모두 일치한다. E063 R의 기록된 세 NPZ SHA도
E062 clean E041의 기록된 SHA와 같다. 실제 바이트·배열 parity는 S2에서 확인해야 한다.

환경 기록은 형태/시점이 다르다. E062는 모델 import 후 추가 scipy/sklearn threadpool을,
E063 freeze는 그 전 상태를 기록한다. 공통 Python/numpy/pandas/torch/CPU 설정은 같지만
전체 environment JSON이 같다고 주장하지 않는다. S2가 같은 import 단계에서 비교하고
기록된 필드의 대응·미기록 범위를 명시해야 한다. 추정으로 빈 필드를 채우지 않는다.

우선 고정 clean E025/E041의 기존 결과를 정확히 식별해 재사용한다. 원본 E063 R/H와
새 assembly/extracted raw parity, E041 snapshot reference와의 연결을 확인한다.
baseline의 과거 환경/완료/identity가 충분히 확인되지 않거나 reference가 없을 때에만,
**동일한 E063 입력·현재 동결 환경에서 그 baseline의 원래 snapshot을 fresh all3 한 번**
실행하는 조건부 범위를 미리 둔다. 후보 재탐색이나 무변경 성공 arm 반복 예산이 아니다.
입력/원본 모델 hash 자체 불일치, R-source와 clean E041 불일치는 HOLD이며 구제하지 않는다.

S2 정상은 assembly와 extracted official의2 all3:6pipeline/18neural/16metric.
조건부 baseline 최대2 all3와 실제 구현 결함 수리용 최대1 all3 상당량을 포함해
상한15pipeline/45neural/32metric, 전체 computational3600초/각 all3 900초,
gross120분/마지막10분 기록, CPU2/GPU0/heavy1/RSS·private8GiB로 제한한다.
이는 최악 범위의 STOP cap이며 실행시간 예측이 아니다. 재사용 성립 시 baseline fit0.

고정 정책·원래 E041 함수들의 global binding을 보존하는 조립이 핵심이다.
새 H와 original에 metric_objective/fit_sections/_replace_evidence/LAST_DIAGNOSTICS
등 같은 이름이 있어 단순 덮어쓰기는 fallback을 바꿀 수 있다. 별도 namespace/명시 binding과
작은 조립 경계 검사, 실제189649 raw parity로 확인한다. 생산 원본은 수정하지 않는다.

## 이후 결정과 보존

모든 release 조건을 통과하면 RELEASE_QUALIFIED_FOR_USER_REVIEW로 S0 반환한다.
그때 동일 ZIP의 사용자 DEV 제출 여부를 판단한다. clean E025 및 E041 기관별-.002,
ZIP checker·official all3·parity·SCORES·bytes provenance를 생략하지 않는다.
기술 실패면 허용된 ordinary repair만 같은 S2에서 진행, 과학적 하한/자원/정책 실패는
그대로 closeout. 예비 작업은 정확한 미완료 조건과 보존 기록뿐이다.

E063 parked. E041 incumbent/E025 fallback; E057/E060/E061/E062 parked,
E062 tie UNRESOLVED. E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/
A039/A040 및 모든 STOP/HOLD,17999명/12339SSUID·집계·A022 역할,
E059 소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177·calibration1866 유지.
A_half 비승격/A018 사용자 미확정/S3 중단. 현재 release-qualified 후보/새 ZIP 없음.

이번 변경은 이 S0 폴더와 status/log 추가뿐. HEAD a43f4379/기존 dirty109 보존.
모델·응답·raw cache·검사·ZIP·원격·commit/push·서브에이전트 실행0.
[읽기·보존 verification](verification.json).

