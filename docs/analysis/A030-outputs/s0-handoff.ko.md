# S0 인계 — A030 Jordan VAF 공개 문서 조사

판정: **정보 과제 완료 / MISSING_METADATA / EMPIRICAL_HOLD 유지**.
인계의 세 번째 종료 분기다. 자료 부적합·UNHCR 전체 불가능 판정은 아니다.
S2 후보 없음. 실제 데이터 접근·학습·패키징을 허가하지 않는다.

## 이번에 확보한 것

- catalog1030 정확한 release `UNHCR_JOR_2023_VAF_HOST_v2.1` 확인.
  제목2024, 실제 조사2023-09-05~11-05, Jordan host communities/캠프 제외.
- 공식 목록의 해당 release는 Licensed data files. 일반 약관은 신청·승인을
  전제. 개별 계약의 허용 목적·계정 절차·파생물 조건은 아직 확인되지 않았다.
- 공식 보고서 PDF 확보. 층화 표본과 case/family/household/sharing group/
  individual 구분, 공개 규모 확인. skip logic DQA 실시를 확인했지만 실제
  routing 오류율이나 근사 gate 증거는 확보하지 못했다.
- questionnaire의 문항 번호·section 간 parent/child 분기, never-asked/refusal/
  DK/일반 결측/imputation 구분은 미확정. 조건부 문항 이름만으로 입증 불가.

근거: [A030 본문](../A030-vaf-channel-metadata-review.md),
[출처·접근 장부](source-register.md), [노출 장부](exposure-ledger.md),
[검증·해시](verification.json), [진입 기록](entry.json).
공식 PDF·텍스트 추출본은 같은 폴더에 저장. 공개 집계 노출은 비영(非零),
행 단위 응답 접근·모델 실행·테스트·ZIP·commit/push는0.

## S0가 결정할 것

동일 검색을 자동 반복하지 않는다. 재개 조건은 **새 문서 또는 식별 가능한
새 공식 공개 위치**다. 필요한 입력:

1. release-matched questionnaire/codebook, 문항 번호·section·분기 조건·각
   결측 코드. 응답·키 값은 포함하지 않는다.
2. 편집/imputation/routing 오류 처리 명세와 해당 release의 연결 단위·key
   정의·wave 연결 여부. DQA 실시만으로 실제 오류를 추정하지 않는다.
3. release-specific 접근/이용 계약. 공개 문서가 부족하면 별도 권한을 받은
   소유자가 제공 가능 여부를 판단한다. 이번 세션은 연락·신청하지 않았다.

새 입력이 생기면 S0가 한정된 문서 확인 과제를 정한다. 입력이 없으면 이
경로는 문서 미충족 상태로 닫아 둔다. 다른 모델 실험이나 다른 자료 탐색은
자동 예비 작업이 아니다. 문서가 충분해져도 응답 접근 권한, 독립 역할,
정밀도·다중 후보와 D-P/D-R 비교 처리, adapter parity·전체 비용은 별도 조건.

## 읽기·작업 증거

S1/정보 확보, workflow2026-09-27-r3.
SHA256 `987b4549dbb6c701bab48df5969e4aa1ed8bf69cc3a851842f55853ca69a84ba`.
이 세션의 도구 읽기: AGENTS.md, CLAUDE.md, status.md, log 최신 A029/A028/A027,
workflow.md, A027 완성 인계 순서. 이어 codex-setup/A029 verification 및 관련
A008/A024/A026/A027 구절 확인. 해시는 식별자이며 읽기 증거 자체가 아니다.
A029 입력76개/산출물17개 해시 일치. 기존 dirty 파일은 현재본으로 유지했다.
HEAD `1d223340d4e1fa3993b411dc5daafab9cb37d0cd`. 실제 시작10:14:36UTC,
60분 한도/자료1개/핵심12개. 최종 시각·jobs·보존 검증은 verification.json.
다른 세션이 이 규칙을 읽었다고 주장하지 않는다.

E041 incumbent/E025 fallback, E057/E060 parked, E058 STOP/E059 STOP_SELECTION,
기존 모든 STOP/HOLD, A_half 비승격 유지. 누적17999/12339와 원래 A022 역할,
E059 소비 oracle/selection·보호 audit/calibration 유지. A018 TEST 사용자
미확정, S3 중단, S2 후보 없음. 다음 주체는 S0 검토이며 자동 실행 없음.
