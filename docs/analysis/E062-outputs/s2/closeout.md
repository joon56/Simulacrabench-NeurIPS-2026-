# E062 S2 종료 — RELEASE_QUALIFIED_FOR_USER_REVIEW

2026-10-08 KST, 사용자 전달 고정 S2 범위 완료. E062는 parked,
E041 incumbent/E025 fallback 유지. DEV 채택·실제 업로드·TEST 선택 판정이 아니다.
준비일은 업로드일이 아니다. 업로드 ID·시각·원격 bytes·계정·slot은 미확정이다.

## 고정 파일과 검증

ZIP: `submissions/2026-10-08-E062.zip`, **16,879 bytes**.

SHA256: `83087eaa081e3973cf4c5b4ae48923f61d33a440c989c7d2a6652c069e90eee4`

main.py SHA256: `6d602380d8cfde1039faa758e43bc0be48834e41ae1c5f01873567833e3501f5`.
ZIP 루트에는 main.py·NOTICE.txt만 있다. snapshot·archive entry·실제 추출 bytes 일치.
NOTICE는 원래 starter-kit MIT license 그대로다. [Manifest](source-archive-manifest.json).

사용자 지정 source `wb_ordinal_heads.py`·E041 control·의존 source·공식 schema/config/
score·입력·환경 identity를 대조했다. S1 아홉 clean 확률 reference는 동일성 확인 후
재사용했다. baseline/source의 성공 fit 또는 기존 성공 suite를 반복하지 않았다.
새 조립 경계 테스트4 PASS; 첫 missing-assembler RED와 비용은 보존했다.
원래 nominal network 상속·isolated globals·control dispatch·WB factory 연결을 확인했다.

조립 all3와 실제 ZIP 추출본의 원래 `score.py` phase1 CLI all3를 각각 한 번 수행했다.
각 all3 UNICEF17,856/WB39,520/UNHCR132,273, 총189,649 vectors를 확인했다.
source→assembly→extracted raw 최대 차이0, 순서·shape·finite·nonnegative·positive
mass PASS. 최대 raw 합 오차2.7508940547704697e-7 ≤1e-6.
UNICEF·UNHCR는 E041과도 exact0. WB 변화35,613 vectors 유지.
정식 ZIP checker PASS; tiny generated smoke predict1은 별도 계수, fit0.

| 기관 | 공식 synthetic skill | E025 대비 | E041 대비 |
| --- | --- | --- | --- |
| UNICEF | .5006484230707156 | 0 | 0 |
| WB | .4549896845143664 | +.0002723771513838402 | +.0002723771513838402 |
| UNHCR | .5624627288576414 | -.0004861448473750807 | 0 |

공식 floor .001과 원래 계산 사용. 기관마다 candidate−E025≥−.002 **그리고**
candidate−E041≥−.002 PASS. baseline은 source/input/role/environment 동일성을 확인한
S1 fresh clean 결과다. 단순 화면 Grand 반올림이나 이전 source PASS로 대체하지 않았다.
[Verification](verification.json), [assembly](assembly.json), [official](official.json),
[checker](zip-check.log), [preflight](preflight.json), [source review](source-review.md).

## 자원·노출·수리

조립 all3 전체482.851370초/900초. 추출본 공식 all3 전체695.631058초/900초;
세 CLI startup/import/predict/score/exit 합684.848584초와 wrapper overhead10.782474초를
포함한다. 중첩 span을 다시 합산하지 않았다. CPU numerical threads2/GPU0/heavy1.
owned controller+descendant RSS2.284397GiB/private commitment2.457088GiB <8GiB 각각,
.1초 관측. 보수적인 per-process peak 합 방식이다.

새 computational children6개 합1,257.288989초/2,400초. 예상 RED45.309152초,
GREEN6.782856초, preflight21.871430초, assembly482.851370초,
package/checker4.843124초, official695.631058초를 모두 포함했다.
S2 pipeline6/neural18/metric16, target-role checks24. 추가 all3·수리 예비량 사용0,
강제 중단0. 진입 시 shell 시작/JSON truncation/PowerShell 구문 오류는 gross에 포함했고
해당 기록을 보존했다. [비용](resource-summary.json), [호출](call-summary.json),
[수리·실패 이력](error-repair-history.md).

S1 역사1,123.1965955000032초/pipeline9/neural27/metric16을 별도 승계.
S1+S2 합2,380.485584500004초/15/45/32. S2 한도와 S1 한도를 혼동하지 않는다.
Gross는09:37Z부터11:37Z, 계산 cutoff11:27Z로 사전에 고정; 마지막 영수증의 실제
경과시간은 [보존·종료 확인](final-preservation.json)에 있다. 문서·hash·오류도 gross에 포함.

이번 S2만 허용된 기존 synthetic Parquet3·numeric NPZ9 및 새 staging/output에 접근했다.
원래 Parquet TRAIN/DEV 필터·projection, TEST 행 요청0. 모델은 TRAIN generated·DEV
GIVEN만 받고 DEV PREDICT는 missing, EXCLUDE 제거. 평가 truth는 evaluator만 접근했다.
정식 CLI staging은 TRAIN/DEV만 포함하며 schema/role/masked-frame round-trip PASS.
NPZ는 allow_pickle=False flat/offsets만 읽었다. 성공 branch상 projected query24,
NPZ loads27이며 OS 파일 접근 감사 수치라고 부르지 않는다. 보호 응답·키·모델 cache·
다른 Parquet/NPZ 접근·재해시 없음. 독립 audit이나 신규 평가 표본이 아니다.
[노출 장부](exposure-ledger.md), [의존성·오프라인·hosted 한계](disclosure.md).

## 과학적 판독·다음 행동

WB 전체 skill 소폭 상승은 원래 절차 전체의 exposed synthetic 결과다. S1 대상16
mean log score−.0007987550486939816, other60+.0009093584055200603,
대상 Not answered−.004408473492304696를 그대로 승계했다. 새 subgroup 계산·선별 없음.
이는 순서형 대상 개선 증거가 아니다. 초기화·비응답·trunk·선택·refit·lambda 등
전체 절차가 함께 바뀌므로 isolated ordinal 효과·실제 WB 효과·유의성·Grand 예상은 주장하지 않는다.

[SCORES](../../../../submissions/2026-10-08-E062/SCORES.md)의 사전 hosted arm은 불변이다.
초기 scorecard hash `11d13920be8e5fa386cbf1d7a6155504f3f4d9e459ba00ba46a3044fdb1b2d6a`,
[초기 bytes](scorecard-prerun.md)·freeze 보존. 마지막 공식 검증 후 release 근거만 추가했고
[append 영수증](scorecard-finalization.json)에 prefix 동일성과 최종 hash를 남겼다.
Local PASS와 hosted 개선 증거는 별개다. 공개 Grand 전체 API·WB·통제 점수 및 비교 가능한
출처를 먼저 확인한다. WB/Grand 상승+통제 공개값 동일은 whole candidate의 noisy favorable,
동점 unresolved, 어느 쪽 하락 adverse, 반대 방향/통제 변화는 mixed·귀속 미해결도 기록한다.
실패는 technical, 필수 값 부재·출처 모순은 판단 보류. 어느 arm도 자동 재제출·구제를 허용하지 않는다.

다음은 [S0 문서 검토 인계](s0-handoff.ko.md)뿐이다. 새로운 실험을 시작하지 않는다.
원본 source·S1 본문/registration/manifest·실험 본문·기존 snapshot·tree 불변.
status/log에 새 S2 결과만 추가; S1 공유 문서 역사 hash와 이후 S0/S2 추가는 별도 명시했다.
HEADa43f4379 불변, 기존 dirty 보존. commit/push·설치·원격·로그인·조회·업로드·
서브에이전트·S3 재개·TEST 선택 없음.

E041 incumbent/E025 fallback, E057/E060/E061/E062 parked. E058 STOP/E059 STOP_SELECTION,
A039/A040와 모든 STOP/HOLD, A_half 비승격, A018 사용자 미확정·S3 중단 유지.
누적17999명/12339SSUID·집계 노출·A022 원래 역할, E059 소비 oracle1918/1124·
selection2007/1130 및 보호 audit2074/1177·calibration1866 이력·경계 유지.
