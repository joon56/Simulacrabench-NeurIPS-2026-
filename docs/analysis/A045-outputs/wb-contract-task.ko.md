# S1-WB-CONTRACT-A045 — 내부 배정, 문서 계약만

Authority: 사용자의2026-10-26 하위 에이전트 운영 전환 지시. Root가 현재 task ID와
epoch를 전달하고 이전 writer release를 남겼을 때 시작한다. 별도 채팅 복사 불필요.
Root는 S0이고 이 child는 **S1 정보/정적 계약 작성자**다. 모델 실행 권한은 없다.

## 읽기·소유권

AGENTS→CLAUDE→status→log 최신3→workflow r7를 실제 읽고 receipt/hash를 남긴다.
현재 [state](orchestration-state.json), dispatch-wb-contract.json, [운영 결정](decision.md),
entry.json을 확인한다. Task S1-WB-CONTRACT-A045, epoch `2026-10-26-A045-01`.
명시적으로 root가 해제한 후 단독 인수한다. 아직 root가 writer면 쓰지 않는다.
완료 뒤 child가 해제하기 전 root는 status/log를 포함해 쓰지 않는다.

이미 완료된 본 child의 읽기 전용 준비도 검토를 재사용한다. 핵심 새 사실은 WB의
최대K26/19개 K>10, raw schema에 sentinel 없음, 기존 UNHCR dispatcher·호출/역할
고정이다. 전체 기존 조사를 재현하지 말고 필요한 부분만 채운다.

## 목적과 허용 입력

다음 새 모델 배치에서 사용자에게 한 번에 제시할 **고정 후보 하나의 실행 계약**을 완성한다.
Whole WB76 pretrained expert, E041 UNICEF/UNHCR controls. 기존 A040 UNHCR213
timeout의 축소 구제나 E062 ordinal16 재시도가 아니다. 현재 E번호 생성 금지.

허용: A040/s1의 contract/observation-plan/cost-accounting 및 로컬 tiny retry1,
full-path-resume1 closeout/manifest와 필요한 직접 adapter/orchestration/runner/schema
정적 source. E062/E064 release·baseline provenance 문서, E041/E025 snapshot main.py
정적 읽기, 공개 external/starter-kit/data/world_bank.json 및 직접 schema/config/scorer
정적 source. 모델 source는 읽기만; import 금지. 기존 노출/보호 역할 승계.
재사용 asset 후보: A040-outputs/full-path-resume1/adapter.py,
tmp/a040-local-technical/source/tabicl-0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src.
직접 필요한 설치 소스/기록 metadata만 허용; 환경 import/probe/install 금지.

금지: 실제·fake 응답 값, Parquet/NPZ/keys/cache/checkpoint 접근·해시·역직렬화,
모델/fixture/test/fit/predict/score·GPU/원격·추가 web/다운로드·환경 변경,
과거 C6/성공 suite 반복, 새 code/ZIP·S2/S3·업로드·commit/push·재위임.
weight/환경 identity는 기록상 값과 현재 재검증 미실시를 구별한다.

## 닫아야 할 계약

1. WB76 전체 출력·655 slots·K26·19개 many-class의 범주 정렬, singleton/빈 context,
   NaN/unknown/정상 fallback, config 주입 sentinel, query 순서·batch·정보 흐름.
2. F/S/E 역할·전체 masking·선택 후 평가·all-visible refit. A040의 S1000/E1000을
   자동 승계하지 말고 WB5195 TRAIN에 대해 근거와 약점을 명시한다. 공개 DEV는
   외부 숨은 평가이며 내부 E나 새 audit으로 부르지 않는다. 세 역할을 실제 열지 않는다.
3. 단일 기관 공통 alpha·동점·guard·불활성 시 exact E041. 복잡한 respondent/head
   router나 임의 grid를 만들지 않는다. 원래 A040 규칙을 읽고 수치/판독까지 고정하거나,
   고정 불가한 조건을 정확히 남긴다. 후보/정책을 결과 뒤 바꾸는 분기 금지.
4. Controls의 import/RNG 영향, complete WB final mixture와 한 번의 floor, gate 재렌더링
   금지, loader/shared weights와 head별 context 분리. 런타임 fitting 허용은 이미 해결됨.
5. Tiny K26의 새로운 영향 검사, 전체 최대 활성 경로, E041 controls/fallback,
   source/assembly/extracted raw parity, clean E025 abs.002/기관 및 E041 비교,
   공식 all3 shared900초, 메모리·배포 disclosure·SCORES 판독을 단계별로 연결한다.
6. full-shape 공학과 scored synthetic release 입력을 구별하고 미래 정확한 allowlist,
   재사용 조건·identity·환경·완료 provenance를 명시한다. manifest 속 모든 파일에
   포괄 접근을 주지 않는다. 수치 배열의 실재/해시 검증을 지금 주장하지 않는다.
7. 새 비용·시간·시도 상한과 정상/실패 최대 호출 수를 전체 절차에 대해 계산한다.
   과거900초 timeout, 많은K·TRAIN/query 크기 차이를 보존하고76/213 비율로 외삽하지 않는다.
   정보검토 제안값 S1 gross180분/children3000초, S2 gross240분/children6000초는
   초안이다. 근거·중복·재사용·수리 여유를 따져 유한한 새 배치 제안으로 확정한다.
   현재 승인된 실행 한도가 아니다. GPU/환경 한도를 낮추거나 cloud로 자동 구제 금지.

새 oracle 없음, synthetic은 engineering, 실제 이득 미측정이라는 한계를 유지한다.
E012 공동학습 이점·E048 standalone 부정 결과·E049 선택기 격차를 반대 근거로 남긴다.
동점은 효과0/비활성 증거 아님. 사용자 제공 선두 WB.50은 가능 이득이나 oracle이 아니다.

## 범위·종료·산출물

새 문서 작업 gross45분(마지막5분 closeout), 모델·테스트·과학0/cash0.
부모가 전달하는 dispatch 시각부터 계수하고 앞선 읽기 전용 준비 비용은 역사로 별도 남긴다.
이 한도는 미래 과학 예산을 새로 승인하지 않는다. 일반 문서/정적 계산 오류는 같은
child에서 수리하며, 입력·권한·과학 기준을 바꾸지 않는다. 실패 시 exact gap closeout만.

쓰기: `docs/analysis/A045-outputs/wb-contract/`와 이 task의 orchestration-state.json,
status/log의 현재 결과·소유권 추가만. 다른 운영 지침·과거 문서/source는 수정하지 않는다.
최소 산출물: contract.md, proposed-batch.ko.md, verification.json, closeout.md.
Entry/문서 해시·입력 읽기·비용 근거·노출/실행0·dirty/jobs·해제는 verification에 통합 가능.
Root가 직접 읽어 판단하므로 중복된 여러 인계 문서를 만들 필요 없다.

완료는 CONTRACT_READY_FOR_S0_REVIEW 또는 구체적 GAP/HOLD. 제안 배치는
**PROPOSED / MODEL_EXECUTION_NOT_AUTHORIZED**를 표시한다. S1 model 실행이나
조건부 S2 시작을 하지 않는다. 모든 STOP/HOLD/보호 역할/E041/E025/parked/A018 유지.
마지막에 소유 jobs와 artifact identities를 기록하고 명시적 writer release 후 root에 반환한다.
