# E063 실제 DEV 결과 — UNRESOLVED

2026-10-10 KST, 기존 E063 S2 결과 문서화만 수행했다.
**E041 incumbent/E025 fallback/E063 parked 유지**. 읽을 수 있는 개선이 없다.
정확한 효과0·예측 동일·전체 가설 반증은 결론이 아니다.

## 제공 사실과 원문

출처는 이번 사용자가 채팅에 붙인 API 형태의 결과 fragment다.
[원문](user-message.txt)은 마지막 My request 본문의 결과와 실행 지시를 함께
보존한다. HTML entity, 줄 끝 Markdown backslash, escaped fence/list marker는
원문에서 정리하지 않았다. IDE 자동 문맥은 보존 범위에서 제외했다.
UTF-8/LF 문서 전사이며 플랫폼 HTTP 원본바이트 확보·직접 인증은 아니다.

[별도 JSON](user-supplied-api.json)은 결과 fragment72줄에서 &#x20;71개를
공백으로 풀고 줄 끝 backslash71개를 제거한 뒤 없는 바깥 중괄호를 추가했다.
점수 문자열·precision·나머지 필드 값은 바꾸지 않았다. 뒤의 실행 지시는
JSON에 넣지 않았다. [정리 내역](normalization.json), [비교 기록](comparison.json).
기존 post-result 경로 및 두 SCORES의 ID972597 기록은 없었고 덮어쓰지 않았다.

| 항목 | 사용자 제공 값 / 범위 |
| --- | --- |
| id / pk | 972597 / 972597 |
| status / status_details | Finished / null |
| phase_name / phase | Development / 29772 |
| filename | 2026-10-09-E063.zip |
| created_when UTC | 2026-10-09T15:29:35.752090Z |
| KST 변환 | 2026-10-10 00:29:35.752090 +09:00 |
| owner | minjoonyoo — 제공 소유명이며 권한/현재 계정 확인은 아님 |
| leaderboard / on_leaderboard | null / false — 제공 snapshot membership |
| best-update 이벤트 | 별도 미제공·독립 미확인 |

created_when은 제공 플랫폼 생성 메타데이터다. 독립 관측한 업로드 시작/완료나
Finished 전환 시각이 아니다. ZIP 파일명10월9일과 생성 KST10월10일을 구분한다.
membership은 과거 best-update 이벤트·현재 slot·계정 권한을 입증하지 않는다.

제공 task는 ID35494, Survey Completion — Development, 설명은 dev survey slice
(privacy-rounded)다. key e89c93af-8c06-4ef0-b091-926c51e2cc4b,
ingestion_program71372c7e-a051-4a39-aea6-62da1d0bb021,
scoring_program f3015fb3-26ec-44c2-97fa-6b5fd501f596가 제공됐다.
task.created_when2026-08-13T15:41:15.656304Z는 task 메타데이터이며 이번 제출
시각이 아니다. task.validated:false만으로 Finished를 실패로 바꾸지 않는다.
전체 필드·score ID/index/is_primary는 별도 JSON에 보존했다.

## 원래 arm과 E041 비교

E041 ID933094의 [2026-09-27 사용자 API extract](../../../../../submissions/hosted-scores/2026-09-27.json)와
[전역 SCORES](../../../../../submissions/SCORES.md)를 기준으로 사용했다.
기준도 Finished/Development/phase29772이며 precision은 모두2다.
E041 extract에는 task/scoring_program 버전 필드가 없다. E063이 제공한 GUID는
원격 scorer 내용·버전 동일성 증명이 아니다. 같은 원격 scorer 버전은 미입증이며,
필드 부재 자체를 모순으로 처리하지 않는다. 비교 범위는 제공된 같은 phase의
released API 값이다. 플랫폼을 조회하거나 인증하지 않았다.

| score key | E041 ID933094 문자열 | E063 ID972597 문자열 | 판독 |
| --- | --- | --- | --- |
| skill | 0.6433333333 | 0.6433333333 | 같음 |
| skill_unicef | 0.5200000000 | 0.5200000000 | 같음 |
| skill_world_bank | 0.4900000000 | 0.4900000000 | 같음 |
| skill_unhcr | 0.9200000000 | 0.9200000000 | 같음 |

원래 [SCORES](../../../../../submissions/2026-10-09-E063/SCORES.md)의
**UNHCR/Grand tie; UNICEF/WB unchanged → UNRESOLVED** arm에 해당한다.
화면 Grand .64만 비교한 판정이 아니다. 네 전체 API 문자열이 모두 같다.
필수 ID/status/phase/filename/score 필드는 제공됐고 현재 출처/phase 모순은
발견되지 않았다. 따라서 제공 공개 값의 동점 판독은 가능하다. 실제 업로드
바이트나 원격 scorer 버전까지 검증된 비교라는 뜻은 아니다.

공개 점수는 noise/privacy-rounding을 거친 값이다. 소수 자릿수가 숨은 원점수
정밀도를 복원하지 않는다. 정확한 실제 효과·예측 동일·전체 가설 반증·hidden
round/head 효과·실제 활성 여부를 알 수 없고 Grand에서 역산하지 않는다.
명시적 best-update 이벤트 보고는 없으며, 이번 값에서 읽을 수 있는 개선이
없다는 사실만 기록한다. 기술 PASS·합성 release PASS는 hosted 개선 증거와 별개다.

## 준비본·manifest·보존

기존 S2 기록상 준비본은 submissions/2026-10-09-E063.zip,15720bytes,
SHA256 5469b5374f6fb3745cabf64071183ed3de5bbe240ea4f18c034049d560d532d9,
제작2026-10-09 23:51:00.484781KST다. 이번 작업에서는 ZIP을 열거나 stat/재해시하지
않았다. 제공 filename 일치만으로 실제 선택한 로컬 path·업로드 bytes·hash를
확정하지 않는다. 이 미확정은 공개 값 동점 판독과 구분한다.

사전 SCORES와 local release 본문 전체를 유지하고 뒤에 결과만 추가한다.
기존 S1/S2 manifest/registration/실험본문/tree는 수정하지 않는다. 이전 S2
artifact-manifest가 기록한 snapshot SCORES 해시는
98cfc9bff6aa17bfe62dca9e1b0bfd2a64885129ae0f51c3338ad9f4b8346d40이며,
이는 이번 추가 전 문서와 일치했다. 사후 SCORES 해시 차이는 허용된 문서
추가분이다. 모델·ZIP 차이나 재검증으로 해석하거나 과거 manifest에 맞춰
복원하지 않는다. 전후 해시·추가분·원래 bytes 복원 확인은 [verification](verification.json).
원문/정리 JSON 및 새 문서 해시는 별도 [문서 manifest](document-manifest.json)에 기록한다.

E025 identity 확인의 과거 순서상 보완과 기존 local release 한계도 그대로 둔다.
이번 확인은 문서 무결성·추가분 확인이며 모델/ZIP 현재 bytes 인증이 아니다.

## 판정과 다음 행동

DEV incumbent E041/E025 fallback 유지, E063 parked. 고정 E063의 동일 정책
재제출·seed/head/threshold 구제·자동 채택 없음. 효과가 미해결인 이 관측을
S0의 다음 연구 우선순위 판단 입력으로 반환하며 새 실험을 시작하지 않는다.
TEST 후보 자동 승격·선택 없음, A018 사용자 미확정/S3 중단 유지.
[S0 사후 인계](post-result-handoff.ko.md)에 다음 판단 질문만 적었다.

모든 parked/STOP/HOLD 및 이전 노출·보호 역할은 [노출 장부](exposure-ledger.md)대로
승계한다. 새 response/Parquet/NPZ/key/cache/ZIP 접근·재해시, fit/predict/score/
fixture/checker/성공 검증 재실행, 모델 변경, 플랫폼/원격/설치/서브에이전트/
commit/push/S3/TEST 선택은 수행하지 않았다.
