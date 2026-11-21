# E061 실제 결과 — S2에서 S0로 인계 (2026-09-29 KST)

**Comparable Grand decline arm 적용. 해당 실행의 adverse operational reading.**
E041 incumbent/E025 fallback, E057/E060/E061 parked 유지.
화면 Grand .64가 같아도 API 값은 하락했다.

| 사용자 제공 공개/API 값 | E041 ID933094 | E061 ID949956 | 차이 |
| --- | ---: | ---: | ---: |
| Grand | .6433333333 | .6400000000 | -.0033333333 |
| UNICEF | .52 | .52 | .00 |
| World Bank | .49 | .49 | .00 |
| UNHCR | .92 | .91 | -.01 |

E061: Finished, Development/phase29772, 파일명2026-09-28-E061.zip.
플랫폼 생성 시각2026-09-28T13:57:41.742034Z,
KST2026-09-28 22:57:41.742034. 사용자의22:57:41 보고와 일치한다.
별도 best-update 이벤트는 미제공. E041 대비 공개 값 개선 없음.
on_leaderboard=false/leaderboard=null만으로 갱신 이력을 단정하지 않았다.

## 출처와 비교 범위

[사용자 제공 JSON](user-reported-949956.json)을 별도 파일로 보존했다.
붙여넣기의 HTML 공백·Markdown 밑줄 이스케이프와 마지막 쉼표만 정리한
JSON 객체이며 HTTP 원문 바이트를 확보했다고 주장하지 않는다.
[상세 결과/receipt](post-result.json), [SCORES](../../../../submissions/2026-09-28-E061/SCORES.md),
[실험 결과 추가](../../../experiments/E061-tied-content-heads.md).

E041 비교값은 기존 사용자 제공
[API ledger](../../../../submissions/hosted-scores/2026-09-27.json)의 ID933094.
양쪽 Development/phase29772, Finished, 네 score key와 precision2가 일치한다.
제공된 공개 값/phase 메타데이터 수준에서 비교 가능하며 모순은 확인되지 않았다.
독립 플랫폼 조회·인증은 하지 않았다. E041 정리본에 task/scoring-program ID가
없어 동일 hosted scorer 버전까지 확인한 것은 아니다.

파일명은 준비본과 일치한다. 아래는 기존 S2 검증 기록의 로컬 식별값이다:
submissions/2026-09-28-E061.zip,16508bytes,
SHA2564b89e619987d568034bf8a70a7ffda190af483c083ad5921eec9f5a8d843f8c6.
이번에는 ZIP/모델/Parquet/NPZ/캐시를 열거나 재해시하지 않았다.
실제 업로드 바이트·원격 해시·선택한 로컬 경로는 미확정.
계정 소유명은 제공 JSON에 있으나 권한/현재 slot 확인으로 확대하지 않는다.

## 판독과 다음 판단

Grand-.0033333333/UNHCR-.01은 공개된 값의 차이다. 정확한 비노이즈 효과,
인과적 손실 크기, tying만의 원인, 실제 예측 동일성·활성 여부를 뜻하지 않는다.
UNHCR.91은 직접 보고된 값이며 Grand 역산이 아니다.
전체 가설 반증·효과0으로 확대하지 않는다.

DEV: 해당 고정 정책에 불리한 관측. E041 유지/E061 parked.
TEST: 개선·승격 근거 없음. 자동 제외/선택이나 S3 재개도 하지 않는다.
A018은 사용자 미확정. 기술·합성 release PASS는 역사적 사실로 보존하며,
이번 hosted 개선 부재와 구분한다.

S0의 다음 질문: 이 adverse 관측을 반영해 고정 E061의 우선순위를 어떻게
정리할 것인가? 이후 작업을 검토한다면 기존 STOP/HOLD와 구별되는 새 입력·
기전·판독 가치가 있는가? 이번 인계는 새 후보나 실험 실행 지시가 아니다.
동일 정책 재제출·seed/head/threshold 구제는 권고하지 않는다.

## 보존과 작업 범위

사전 SCORES/기존 결과 본문은 보존하고 실제 결과만 뒤에 추가했다.
실험 문서도 기존 본문 뒤에 추가; parked header 불변. status/log는 현재 기록 갱신.
기존 manifest/verification/registration/tree 수정 없음.
S2 manifest와 현재 SCORES/실험/status/log의 차이는 사후 결과 기록이며,
status/log에는 이번 이전 A035 추가도 있었다.
[사후 문서 검증](post-result-verification.json)이 전후 해시/원문 prefix를 구분한다.

누적17999명/12339SSUID·집계 노출·A022 원래 역할,
E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866을 유지한다.
E058 STOP/E059 STOP_SELECTION, A023/A024 empirical HOLD와 모든 STOP/HOLD,
A_half 비승격 보존. 새 fit/predict/score/성공검증 재실행0회.
모델/ZIP 변경·보호 데이터 접근·로그인/업로드·commit/push 없음.
HEADa43f4379ec78dbc2de260463eef67bb1d567d7e1 유지.

## S0 붙여넣기용

```text
SimulacraBench / HSCC S0 — E061 실제 결과 문서 검토.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench

AGENTS → CLAUDE → status → log 최신3개 → workflow.md를 실제 읽고,
docs/analysis/E061-outputs/s2/post-result-handoff.ko.md,
user-reported-949956.json·post-result.json·post-result-verification.json,
submissions/2026-09-28-E061/SCORES.md의 사전 arm과 실제 결과를 검토한다.

E061 ID949956 Finished,2026-09-28 22:57:41.742034KST.
Grand API.6400000000/UNICEF.52/WB.49/UNHCR.91.
E041.6433333333/.52/.49/.92 대비 comparable Grand decline.
화면.64 동일을 API tie로 기록하지 않는다.
사용자 제공 API 기록 수준 비교이며 원격 업로드 bytes는 미확정이다.

해당 고정 실행의 adverse reading. 정확한 실제 효과·전체 가설 반증 아님.
E041 incumbent/E025 fallback, E057/E060/E061 parked 유지.
DEV와 TEST 판단을 분리하고 S0 문서 검토/다음 권고만 기록한다.
새 실험·재학습·동일정책 재제출·seed/head/threshold 구제·모델/ZIP 수정,
보호 데이터/캐시 접근·재해시·성공검증 재실행·플랫폼 조회/업로드,
commit/push·S3 재개·TEST 자동 선택은 하지 않는다.
모든 STOP/HOLD·노출/보호 역할·A_half 비승격·A018 사용자 미확정을 보존한다.
```
