# E064 ID1008932 — 실제 DEV 결과: UNRESOLVED

2026-10-26 KST. 사용자 제공 API 형식 fragment에 원래 사전 동점 arm 적용.
**E041 incumbent / E025 fallback / E064 parked 유지.** 읽을 수 있는 개선 없음.

| 항목 | E064 ID1008932 | E041 ID933094 | 공개값 차이 |
|---|---|---|---|
| Grand / skill | 0.6433333333 | 0.6433333333 | 0 |
| UNICEF / skill_unicef | 0.5200000000 | 0.5200000000 | 0 |
| World Bank / skill_world_bank | 0.4900000000 | 0.4900000000 | 0 |
| UNHCR / skill_unhcr | 0.9200000000 | 0.9200000000 | 0 |

두 보고 모두 Finished, Development / phase29772. 네 key와 전체 score 문자열,
precision2, primary를 대조했다. E064의 index0..3도 해당 key 순서와 일치한다.
Grand 화면 반올림값만 비교한 것이 아니다.
E064 filename은 `2026-10-23-E064.zip`, pk/id는 모두1008932다.
UNHCR·Grand 동점 및 두 통제의 공개값 동일: 원래 **UNRESOLVED**.
실제 효과0·예측 동일·hidden activation 동일·gradient 충돌 부재·함수족 전체 반증은 아니다.
동일 정책 추가 우선순위를 낮추며 자동 재제출/seed/head/threshold 구제·TEST 승격은 없다.

## 출처와 정리

- [user-message.txt](user-message.txt)는 이번 async 답변의 fragment를 UTF-8로
  옮긴 텍스트다. 마지막 쉼표를 보존했고 파일 끝 개행을 추가했다. HTTP 응답 원본 바이트,
  서버 서명 또는 독립 플랫폼 조회를 인증한 파일이 아니다.
- [user-supplied-api.json](user-supplied-api.json)은 끝 쉼표 하나를 제거해 단일
  JSON 객체로 파싱한 뒤 들여쓰기를 정리했다. 값/필드는 그대로, score는 문자열로 유지했다.
  owner/fact_sheet/task metadata도 원문에 보존했다. 전체 제출 목록은 아니다.
- Comparator는 고정된 `submissions/hosted-scores/2026-09-27.json`의 E041 ID933094.
  기존 사용자 제공 API 기록이며 이번에도 플랫폼에서 재조회하지 않았다.
- 로컬 준비 ZIP의 기록상 SHA256은
  `002028ce0c7fa7cb3549d198cef3e4c13060fdf9aa47ce7a7f7a773ee1c74f1c`,16305bytes.
  이는 이전 S2 문서에서 승계했으며 이번 ZIP 접근/재해시0. Filename 일치만으로
  실제 업로드 경로·바이트·해시 동일성을 확인했다고 하지 않는다.

`created_when=2026-10-26T11:07:15.519457Z` → **2026-10-26 20:07:15.519457 KST**.
이는 제공된 플랫폼 생성 metadata다. 독립 검증한 업로드 시작/완료·Finished 시각은 아니다.
`on_leaderboard=false`, `leaderboard=null`은 제공 스냅샷의 membership일 뿐이다.
Best-update 이벤트·계정 권한·slot 소비/잔여·실제 선택 로컬 경로는 확인되지 않았다.
E064 task35494 및 scoring_program/ingestion_program 식별자는 보존했지만,
E041 비교 기록에 해당 식별자가 없어 동일 scorer 버전/바이트 증명으로 쓰지 않는다.
`task.validated=false`는 task metadata이며 submission status Finished를 덮어쓰지 않는다.

## 범위별 판정과 다음 행동

기존 local technical/release PASS는 역사로 유지한다. 이번에는 문서 값/보존 확인만 했고
모델·과학 검증·scorer/checker·패키지 검증을 재실행하지 않았다. 공개 점수는 이미
노이즈/반올림을 거친 값이며 Grand의 추가 소수 자리는 숨은 기관별 정밀도를 복원하지 않는다.
S1의 작은 합성 UNHCR 하락은 그대로며 이번 공개 동점으로 실제 효능을 확정하지 않는다.

S0는 이 동점 결과와 기존 반대 근거로 후속 우선순위를 판단한다. 새 가설/모델/입력,
남은 B01 예산 재사용, 동일 정책 재제출은 시작하지 않는다. E041 provisional TEST
reference/E025 alternative는 최종 사용자 선택과 별개이며 방법 초안·license/Terms의
후속 판단도 이번 결과 기록에서 바꾸지 않는다.

E057/E060/E061/E062/E063/E064 parked, E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD/A039/A040 및 모든 기존 STOP/HOLD 보존.
17999명/12339SSUID·집계·A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격/A018 사용자 미확정 유지.
응답/키/Parquet/NPZ/cache/VAF 접근0, 모델/검증/ZIP/플랫폼/재제출/commit/push/S3/TEST 선택0.
쓰기 해제·문서 변경/보존 범위는 [verification.json](verification.json)에 기록한다.
