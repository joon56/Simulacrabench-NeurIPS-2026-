# E062 실제 DEV 결과 — UNRESOLVED

2026-10-08 KST 사후 문서 기록. **기존 사전 동점 arm 적용; E041 incumbent/E025 fallback,
E062 parked 유지.** 읽을 수 있는 새 best가 없으며, 정확한 효과와 예측 변화는 미해결이다.

## 사용자 제공 사실과 출처

현재 사용자가 붙여넣은 JSON fragment를 [텍스트](user-supplied-api-fragment.txt)로 보존했다.
필드나 score 문자열을 생략하지 않고 바깥 객체 괄호만 보완한
[JSON](user-supplied-api.json)도 저장했다. 보존 hash는 이 채팅 텍스트 사본의 식별이며,
원래 API 응답 transport bytes나 독립 플랫폼 인증을 뜻하지 않는다.

- E062 **ID/pk969351**, `Finished`, `Development`, phase29772.
- filename `2026-10-08-E062.zip`, task35494 `Survey Completion — Development`.
- `created_when`: **2026-10-08T13:37:12.926748Z**,
  KST **2026-10-08 22:37:12.926748 +09:00**.
- API 공개 Grand **0.6433333333**, UNICEF **0.5200000000**,
  WB **0.4900000000**, UNHCR **0.9200000000**. 각 precision2.
- `status_details:null`, `on_leaderboard:false`, `leaderboard:null`.
  독립 best-update 이벤트 자료·완료 시각·hosted runtime·실제 선택 경로/hash는 미제공이다.
- 제공 scoring_program `f3015fb3-26ec-44c2-97fa-6b5fd501f596`.

`created_when`은 제공된 플랫폼 생성 메타데이터다. ZIP 준비일·정확한 upload 시작 시각·
Finished 완료 시각으로 혼용하지 않는다. leaderboard membership 필드는 해당 제공 snapshot의
상태이며 역사적 best-update 이벤트를 직접 증명하지 않는다. task의 `validated:false`를
제출 실패로 바꾸지 않는다. 제출 status는 제공대로 Finished다.

## E041 비교와 사전 arm

E041 ID933094의 기존 사용자 API extract
[2026-09-27 장부](../../../../../submissions/hosted-scores/2026-09-27.json)와
[E041 API supplement](../../../../../submissions/2026-09-19-E041/SCORES.md)를 확인했다.
E041은 Finished, Development/phase29772, filename E041.zip이다.
2026-09-19T08:10:46.209685Z 생성 메타데이터와 아래 공개 문자열이 기록되어 있다.

| 관측 | Grand API | UNICEF API | WB API | UNHCR API |
| --- | --- | --- | --- | --- |
| E041 ID933094 | 0.6433333333 | 0.5200000000 | 0.4900000000 | 0.9200000000 |
| E062 ID969351 | 0.6433333333 | 0.5200000000 | 0.4900000000 | 0.9200000000 |

네 공개 값의 문자열이 모두 같다. 화면 Grand .64를 근거로 축약한 동점 판정이 아니다.
[원래 SCORES](../../../../../submissions/2026-10-08-E062/SCORES.md)의
**“WB and Grand equal: Unresolved; E041 retained/E062 parked; no exact-zero claim”**을 적용한다.
유리/하락/mixed/실패 arm으로 변경하거나 새 사후 기준을 만들지 않는다.
[기계 판독 비교](comparison.json).

비교 범위는 등록된 comparator에 대한 사용자 제공 Finished Development/phase29772의
공개 API 관측이다. E062 filename은 준비본 basename과 일치하고, 제공 출처 사이에 기록된
phase/ID/filename/score 모순은 없다. 두 출처 모두 독립 인증하지 않았다. E041의 역사 extract는
task/scoring_program을 제외했으므로 원격 scorer의 동일 버전까지 새로 확인한 것은 아니다.
이 한계를 함께 기록하며 사용자가 지정한 사전 UNRESOLVED arm을 따른다.

phase1의 privacy/noise/rounding과 precision2를 고려한다. Grand의 추가 소수 자릿수는
숨은 기관 정밀도를 복원하지 않는다. **공개 값 동점은 정확한 효과0·실제 예측 동일·활성
section 동일·전체 가설 반증을 뜻하지 않는다.** Grand로 숨겨진 기관/대상16/raw 값이나
가설 효과를 역산하지 않는다. 공개 점수상 더 좋은 결과는 읽히지 않았고, best-update
이벤트 자체는 별도 제공되지 않았다.

## 로컬 파일·원격 bytes와 기술 기록

원래 release manifest의 로컬 식별을 승계한다:
`submissions/2026-10-08-E062.zip`, 16,879 bytes,
SHA256 `83087eaa081e3973cf4c5b4ae48923f61d33a440c989c7d2a6652c069e90eee4`.
이번 사후 작업은 ZIP을 열거나 재해시·변경하지 않았다. filename 일치만으로 실제
업로드된 bytes가 이 파일과 같다고 인증하지 않는다. 원격 ZIP hash/bytes·실제 선택 경로는 미확정.

이전 source/assembly/extracted parity·ZIP checker·official all3·회귀/자원 PASS는
이전 로컬 release 근거로 보존한다. 재실행0이며 현재 hosted 개선 증거로 바꾸지 않는다.
S1 whole WB synthetic +.0002723772와 대상16 log score−.0007987550,
other60+.0009093584, 대상 Not answered−.0044084735도 그대로 승계한다.
이번 공개 동점이 그 synthetic 결과를 무효화하거나 정확한 실제 WB 효과를 확정하지 않는다.

## 판정과 인계

DEV: E041 incumbent/E025 fallback 유지, E062 parked. 동일정책 자동 재제출·
seed/head/threshold 구제 없음. TEST: 이번 관측으로 자동 선택·shortlist 승격 없음;
A018 사용자 미확정, S3 중단 유지. 다음 연구 우선순위는
[S0 사후 인계](../post-result-handoff.ko.md)에서 문서 판단만 요청한다.

원래 사전 arm·S1/S2/S0 검증/manifest·registration·실험 본문·source·snapshot·tree는 보존했다.
candidate/central SCORES에는 사후 supplement만, status/log에는 새 결과만 추가했다.
기존 manifest가 가리키는 SCORES/status/log 역사 hash와 새 문서 hash의 차이는
사후 verification에 명시한다. 기존 manifest를 다시 만들거나 소급 수정하지 않는다.
제공 JSON·비교·문서 보존 확인 외에 모델/검증/score/ZIP/플랫폼/commit/push 실행 없음.

E057/E060/E061/E062 parked. E058 STOP/E059 STOP_SELECTION, A023/A024 empirical HOLD,
A039/A040와 모든 기존 STOP/HOLD, A_half 비승격 보존. 누적17999명/12339SSUID·집계 노출,
A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130 및 보호
audit2074/1177·calibration1866 이력·경계 보존. 보호 응답/키·Parquet·NPZ·cache 접근·재해시0.
