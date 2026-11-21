# Codabench — 최고점 외 제출의 기관별 점수 확인

확인일2026-09-27. 결론: **일반 UI에서는 제한이 맞음. 본인 페이지가 받은
점수 목록 응답에 세부 값이 있으면 확인 가능성이 있음. 실제 계정에서는 미검증.**

## 이 대회의 실제 공개 설정

[대회 공개 API](https://www.codabench.org/api/competitions/17822/)에 익명 GET으로
접근해200 응답을 저장했다. 일반 웹 도구가 대회 페이지에서 반환한 무관한
본문은 증거에서 제외했다. 사용자의 계정·제출 기록에는 접근하지 않았다.

- SimulacraBench, competition17822, Development phase29772.
- leaderboard `submission_rule=Force_Best`.
- `enable_detailed_results=false`.
- `show_detailed_results_in_submission_panel=false`.
- `show_detailed_results_in_leaderboard=false`.
- DEV `hide_output=true`, `hide_prediction_output=true`, `hide_score_output=true`.
- 공개 열은 `skill`, `skill_unicef`, `skill_world_bank`, `skill_unhcr`; precision2.
- `can_participants_make_submissions_public=false`.

따라서 상세 HTML, 점수 출력 ZIP, 로그 다운로드 또는 다른 제출을 리더보드에
수동 교체하는 버튼을 해결책으로 안내하면 부정확하다. Force_Best는 최고점을
표시하는 정책이고, 사용자가 그 정책을 바꾸는 작업은 허용되지 않는다.
익명 응답의 used_submissions=0은 사용자의 잔여 제출 횟수가 아니다.
[정리된 설정](competition-settings.json), [원본 응답](competition-public.json).

## 공식 소스에서 찾은 별도 경로

공식 upstream commit `6ffd3f48ec3ae13bd6e671d4119f5cfe5fa276a6` 확인:

- [submission_manager.tag](https://github.com/codalab/codabench/blob/6ffd3f48ec3ae13bd6e671d4119f5cfe5fa276a6/src/static/riot/competitions/detail/submission_manager.tag):
  `get_score()`는 `submission.scores`에서 대표 점수 하나만 표시한다.
- [SubmissionSerializer](https://github.com/codalab/codabench/blob/6ffd3f48ec3ae13bd6e671d4119f5cfe5fa276a6/src/apps/api/serializers/submissions.py):
  제출 목록/단건 응답에는 `scores` 배열이 있다.
- [SubmissionScoreSerializer](https://github.com/codalab/codabench/blob/6ffd3f48ec3ae13bd6e671d4119f5cfe5fa276a6/src/apps/api/serializers/submission_leaderboard.py):
  각 점수는 `column_key`, `score`, `precision`, `is_primary`를 포함한다.
- [SubmissionViewSet](https://github.com/codalab/codabench/blob/6ffd3f48ec3ae13bd6e671d4119f5cfe5fa276a6/src/apps/api/views/submissions.py):
  일반 제출 GET은 인증 및 본인/운영자 범위로 제한한다. 로그·출력의
  `get_details`는 별도로 hide_output을 검사한다.
- [공식 client](https://github.com/codalab/codabench/blob/6ffd3f48ec3ae13bd6e671d4119f5cfe5fa276a6/src/static/js/ours/client.js):
  페이지의 목록 조회는 GET `/api/submissions/`와 phase 필터를 사용한다.

**추론:** 이 버전과 같은 동작이면, 화면에 Grand만 보이더라도 서버가 이미
본인 페이지에 내려준 `scores`에 기관별 값이 있을 수 있다. 운영 서버의 실제
배포 버전·사용자 응답은 확인하지 않았으므로 성공을 보장하지 않는다.
hide_score_output은 출력 파일 제약이며, 점수 배열까지 반드시 비운다는 뜻으로
확대하지 않는다. 반대로 배열 존재만으로 모든 점수가 반환된다고 보장하지 않는다.

## 사용자 확인 절차 — 읽기만

1. 로그인 상태에서 대회 **My Submissions**의 **Development**를 연다.
2. **F12** 또는 **Ctrl+Shift+I**로 개발자 도구를 열고 **Network**를 선택한다.
3. **Fetch/XHR** 필터를 선택한 뒤 페이지를 새로고침한다.
4. 요청 목록에서 `submissions`를 검색한다. 정상 페이지가 보낸
   `/api/submissions/?phase=29772...` 형태의 **GET** 응답을 선택한다.
5. **Preview/Response**에서 본인의 E060 제출 ID 또는 filename을 찾는다.
   페이지에 따라 최상위 배열 또는 `results` 배열 안에 있다. 다른 제출과
   혼동하지 않도록 ID·파일명·생성 시각을 함께 확인한다.
6. 그 항목의 `scores`에서 아래 `column_key`를 찾고 대응 `score`만 기록한다.

| column_key | 의미 |
|---|---|
| skill | Grand |
| skill_unicef | UNICEF |
| skill_world_bank | World Bank |
| skill_unhcr | UNHCR |

그 요청이 이미 화면으로 보낸 본인 점수를 읽는 절차다. 콘솔 코드 실행,
관리자 권한 요청, 다른 사용자의 ID 탐색, 리더보드 변경, 재제출은 필요 없다.
비공개 출력 파일·로그 URL을 찾아 열지 않는다. HAR·쿠키·Authorization 헤더·
전체 계정 JSON을 공유할 필요 없음. **제출 ID와 위 점수 값만** 전달하면 된다.

응답이401/403이거나 해당 항목에 Grand만 있으면 종료한다. 권한 우회나
다른 endpoint 탐색으로 이어가지 않는다. 세부 값이 없다는 관측을 기록하고
Grand-only 판독을 유지한다. 다른 페이지의 최고점 값을 E060 값으로 섞지 않는다.

기관별 값이 있어도 공식 제공 정밀도·개인정보 보호 노이즈가 적용된 제출
관측이다. 응답의 소수 자릿수를 이용해 원래 숨겨진 정확도를 복원했다고
주장하지 않는다. S0/S2는 원래 사전 판독 기준과 노출 이력을 유지한다.

## 없을 때 담당자에게 물을 문장 — 미발송

```text
For SimulacraBench competition 17822, My Submissions shows the Grand score
for my non-best submissions, while the leaderboard shows instrument scores
for my best submission. Is there a supported participant-facing way to view
the officially released UNICEF, World Bank and UNHCR scores for each of my
own submissions? If not, could you confirm that only the Grand score is
available for non-best submissions? I am not requesting hidden diagnostics,
unrounded scores, private logs or respondent-level information.
```

문의는 선택사항이며 이번 작업에서는 보내지 않았다. 기관별 값이 없더라도
새로 등록한 DEV 탐색의 Grand-only 결과 판독은 가능하다.
