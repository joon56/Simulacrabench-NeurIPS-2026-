# S0 인계 — A042 round 조건부 metric 계약 조사 완료

**CONTRACT_READY_FOR_S0_REVIEW.** 정보·수식·정적 소스 조사만 완료했다.
효과·local model·release PASS 및 후속 실행 권한을 뜻하지 않는다.
[계약](contract.md), [종료 기록](closeout.md), [읽기·해시·보존 검증](verification.json).

S0가 판단할 것은 **이 계약 한 개의 제한된 로컬 구현·기술 검증을 별도로 허용할지**다.
S2 이관이나 실제 응답 접근으로 바로 넘어가지 않는다.

- 후보 H: original K32를 유지하고 query wave1/2에 따라17개 가중치를 달리한다.
  두 벡터는0..12, 공유 share는원래범위. 공통 평균의 기존 penalty와 두 round
  차이의 .001 penalty를 고정했다. 총35좌표; grid·새 expert·lambda 분할 없음.
- C는 원래18좌표 E041/R 그 자체다. C/R를 별도 학습·독립 비교 두 개로 세지 않는다.
  H와 C 중 승자를 다시 고르는 selector도 없다. 각 arm의 원래 .003/2SE 대
  first10-of-K32 proxy 선택을 유지한다. S 재사용과8section 다중 선택의 한계가 남는다.
- 새 사전 지원 조건: F/S 각각 round당30행 및 원래K32 폭, 전체 입력의 지원된
  wave값. 미달/one-round/unknown은 전체 기관 exact E041 경로. 이30은
  공학상 eligibility이며 통계적 정밀도나 lambda minimum30의 증명이 아니다.
- 가중치가 같다는 수식만으로 exact E041을 주장하지 않는다. 원래 optimizer,
  activity, replay/lambda, renderer 상태를 재사용하는 common endpoint가 필요하다.
  H는 activity·replay 자격·lambda·부모/자식 출력을 바꿀 수 있다.
- 전체 all3 정상 호출은3pipeline/9neural/8metric. 새 R/H 비교는6/18/16.
  neural final refit은 이미 포함, 추가 refit0. 시간·RSS/commitment는 미측정이다.
  기존 CPU 환경의 별도 실행 제안은 각 all3≤900초/CPU2/worker1/GPU0/8GiB이며
  이번 조사에서 실행하거나 이 한도를 충족했다고 주장하지 않았다.

공개 schema의 round별 코딩 차이와 수식상 순위 역전 가능성은 확인했다.
실제 donor 보완성·학습 가능성·효과는 미확정이다. base와 wave-match가 이미
wave를 쓴다. donor-constant 항은 softmax에서 사라지며, binary wave-match의
차이 항 일부는 donor-round preference와 동치라는 한계도 계약에 명시했다.

미래 기술 검증은 common parity/gradient·정보 흐름·지원 fallback·강제 활성
공학 경로부터 시작할 수 있다. 전체 PREDICT 마스킹, UNICEF/WB exact controls,
all213 recursive 출력과 비용을 확인해야 한다. 실제 TRAIN 선택은 hosted 내부만;
독립 audit이나 A021 D-P/D-R 검증이라고 부를 수 없다. 새 oracle 없음.
현재 synthetic은 노출된 공학 채널이며 긍정/비활성이 실제 UNHCR 증거가 아니다.

S2 잔여: clean E025 absolute .002/기관, E041 전체 비교, source/assembly parity,
ZIP checker, official all3/shared900s·메모리, SCORES 사전 판독표. 모두 미실행.
적합한 실제 관측 채널이 필요하면 소유자·권한·round/단위/코딩·노출·정밀도
설계를 먼저 특정해야 한다. A022 또는 E059 보호 역할을 가져다 채우지 않는다.

HEAD a43f4379 유지. 모델·연구 원본·snapshot·tree와 기존 dirty 작업 보존.
새 문서4개 및 status/log 결과 추가만 수행. 모델/응답/cache/test/원격/E/ZIP/
commit/push/subagent0. 기존 E041/E025, E057/E060/E061/E062 parked, 모든
STOP/HOLD/A039/A040/A023/A024/E058/E059 유지. 17999/12339SSUID·집계·A022
역할·E059 소비oracle1918/1124 및selection2007/1130, 보호audit2074/1177·
calibration1866 그대로다. A_half 비승격/A018 미확정/S3 중단/S2 새 후보 없음.
