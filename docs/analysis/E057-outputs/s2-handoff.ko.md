# E057 S2 검증 인계 — 제출 후보 채택 아님

S1 E057 완료. 사전 등록592da4c, 실행 코드e51b29f,
입력 HEAD9284bf4d277e339a9ae4a334d6cf7ee7bde2c6ba.
현재 브랜치work/e050-submission. 시작 전 최신 HEAD·dirty files·active jobs 확인.
사용자 소유 `.gitignore`, `.claude/skills/paper-session/SKILL.md`,
`.claude/settings.local.json`, `trip/` 보존. S1 종료 시 실행 중인 작업 없음.

사용자 결정이 우선한다. E041은 DEV incumbent, E025는 fallback.
S3 중단 상태이며 A018의 TEST selected/frozen 문구는 미확정 검토안이다.
S2가 TEST 선택이나 S3 재개를 승인받은 것으로 해석하지 않는다.
기존 E046/E050/E051/E053/E055 STOP과 E056 산출물 보존.

## 이번에 확인된 것

- UNHCR schema의 모든145 gated leaf 고정; max14 answer classes.
  실제 asked fit 수는 schema만으로 알 수 없다.
- 고정 seed5701, visible TRAIN8279를 fit5879/selection1200/validation1200으로
  분리. base와 tree 모두 나머지 PREDICT block을 전부 마스킹한 동일 입력 사용.
  GIVEN-only tree, asked 여부는 fit 행 선정에만 사용.
- 선택3개 leaf; whole-policy 검증 delta+.000021745421, SE.000011123476.
  사전2SE 기준 미달. 전체 가중치0 동결 후 all-visible refit. 기준 변경 없음.
- 모든145개 대상으로 eligibility 확인; shadow124+refit124개 실제 학습.
  자연 출력은 all3 총189649 vectors exact E041. 강제 활성 fixture는
  점수 없이124 heads/77004 vectors에서 구조 확인. 나머지21 heads fallback.
- 집중 테스트13개, 동결 해시·마스킹·순서·출력 재구성 검증 PASS.
  raw sentinel exact; 강제 경로 mass 최대4.44e-16, floor sentinel2.22e-16.
- import+all3+shadow+선택·검증+전체 refit+비교 포함564.661591초,
  보수적 fit544.353257초. worker·launcher·harness 합산 RSS lifetime peak
  1,828,978,688 bytes(~1.703GiB). CPU2 threads, 900s/1200s/8GiB 통과.
- clean E025 absolute.002: UNICEF0/WB0/UNHCR-.000486144847 모두 PASS.
  E041 delta는 모두0. 검증된 기존 cache만 사용; 새 E025 fit 없음.

이는 노출된 synthetic phase1의 절차·실행 가능성 근거다. 실제 UNHCR 이득,
실제 TRAIN에서의 활성 여부, refit 후 효과, hosted runtime은 미확정이다.
가중치0은 목표 데이터의 불가능을 뜻하지 않는다. 강제 양성 fixture는
성능 근거가 아니다. E056 oracle/selection/audit도 이미 개발 근거다.
E056 재실행·미선택 audit arm·calibration·추가 SIPP 튜닝 금지.

## S2에서 남은 검증과 판정

1. 새 모듈의 **default predict 경로와 최종 single-file assembly parity**.
   S1 전체 실행은 immutable E041 snapshot을 주입했다. 기존 source-default
   parity는56개 원본 source 해시 일치로 계승했지만, 새 wrapper의 shadow 및
   최종 refit까지 포함한 default/assembly parity는 아직 새로 검증하지 않았다.
   자연 inactive 경로만으로 active branch parity를 대신하지 않는다.
2. 같은 입력·코드·분할·config·cell 해시의 기존 cache만 사용한다.
   새 assembly의 부모/비말단/UNICEF/WB exact E041, alpha0, sparse fallback,
   sentinel·총질량·공식 floor·schema 순서·전체 벡터 검증. active fixture는
   점수 선택과 계속 분리한다. 실패는 STOP; seed/head/grid 탐색 금지.
3. **ZIP checker, official score.py all3, 제출 assembly의 shared runtime·memory**.
   S1은 ZIP과 method를 만들지 않았고 official CLI를 실행하지 않았다.
   기존 E041 checker/official PASS는 새 E057 archive의 PASS가 아니다.
   E025 절대.002 및 E041 비교를 새 제출 출력 기준으로 다시 결속한다.
4. **SCORES.md 판독표를 업로드 전에 고정**. 아직 E057 scorecard는 없다.
   유리: 비교 가능한 hosted 개선이면 목표 채널 지지 증거로 기록하되,
   노이즈/반올림/개별 instrument 분해 한계와 별개로 채택을 검토한다.
   불리: 읽을 수 있는 악화면 E041 유지, 실제 관측 범위에서만 중단한다.
   미해결: Grand 동일/비교 불가/개별 점수 없음은 inactive·작은 효과·노이즈를
   구분하지 못한다. hidden 활성 여부를 추정하거나 통계를 점수에 인코딩하지 않는다.
   실패: checker/parity/runtime/공식 실행 오류는 기술 실패이며 성능 결론 없음.
   수치 기준은 업로드 전 당시 허용된 관측과 비교 대상을 명시해 고정한다.
5. 날짜·slot·공식 환경/규칙은 release 시점에 확인한다. S1의 로컬 Windows
   CPU 시간은 hosted 환경 보증이 아니다. 새 runtime cap/검증 예산도 실행 전 고정.
   실제 TRAIN 선택·검증·refit은 hosted 내부에서만 수행하고 상세 통계는
   외부로 내보내지 않는다. 사용자 업로드 권한은 별도이며 이 인계가 승인하지 않는다.

다음 행동은 **S2 release 검증 여부 판단 및 필요한 검증 실행**이다.
E057은 연구 후보로 parked; 자동 제출 추천·새 DEV incumbent·TEST 채택 없음.
E056의 구조적 근거와 이번 정직한 절차 때문에 후속 검증 가치는 있으나,
synthetic 양성 또는 비활성만으로 후보를 채택하지 않는다.

## 파일과 재현

- [E057 전체 기록](../../experiments/E057-unhcr-conditional-content.md)
- [사전 등록 원본](registration.md), [schema 대상](schema-audit.json)
- [source/data/cache 해시](preflight.json), [동결 검증](frozen-verification.json)
- [실행 단계](unhcr-execution.json), [점수](result.json), [전체 시간](runtime.json),
  [합산 메모리](aggregate-memory.json)
- [노출 장부](exposure-ledger.md), [재현 명령·제한](reproduction.md)
- 구현 `src/models/conditional_leaf_content.py`, 실행 `scripts/check_e057.py`,
  동결 검증 `scripts/verify_e057.py`, 테스트 `tests/test_e057_conditional_content.py`.
- 행 단위 자료는 ignored `external/e057/`; Git에는 코드·집계·해시만 포함.

기존 자동 승인 검토가 origin으로의 push를 거부한 이력이 있다.
목적지 `https://github.com/joon56/Simulacrabench-NeurIPS-2026-.git`의
소유·비공개 여부와 외부 전송 승인이 확인되지 않았다는 사유다.
후속 사용자 메시지에서 해당 origin으로의 push를 명시적으로 승인했다.
이 승인으로 push를 진행하며 원격 HEAD를 확인한다. S2에서 같은 목적지의
이번 E057 커밋 전송 승인을 다시 요청할 필요는 없다. 업로드 승인은 별개다.
