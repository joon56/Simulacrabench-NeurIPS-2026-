# S0 — E025 phase2 provenance 수용과 다음 문서 작업

2026-10-23 KST. **ACCEPT_LOCAL_E025_PROVENANCE / TEST_CHOICE_OPEN.**
역할 S0, workflow 2026-10-22-r6. 실행이나 최종 선택 승인이 아니다.

## 수용한 범위

S3의 `LOCAL_E025_PHASE2_PROVENANCE_COMPLETE_FOR_S0`를 수용한다.
미변경 E025 modular source와 보존 ZIP의 local phase2 연결 공백은 해소됐다.
442425개 raw exact, official all3 PASS, 기관별 E041 절댓값 .002 비교,
각 all3 shared900초 및 관측 메모리 한도 통과가 종료 기록에 연결돼 있다.
E041 frozen raw 재사용 gate가 모델 전에 완료됐고 E041 재학습은 없었다.

S0는 핵심 S3 문서 9개와 공유 문서 3개의 현재 SHA256을 S3 verification과
대조했다. 모두 일치했다. raw/입력/모델/ZIP은 열거나 재해시하지 않았다.
이는 완료 증거의 문서 검토이며 S0가 과학 검증을 다시 실행했다는 뜻이 아니다.
[진입·식별](entry.json), [S3 종료](../s3-e025-provenance/closeout.md),
[비교](../s3-e025-provenance/comparison.json).

실측 source429.9301762초/official450.2767931초, 계산 charge1030.9642052/2700초.
정상 all3 두 번, 과학 수리 재실행0. 미사용 예산은 종료됐다. 추가 모델 검증이나
동일 checker 재실행을 권고하지 않는다. 새 경계 무효화가 생기면 그 부분만 별도 판단한다.

## 후보 판단과 남은 한계

E041은 DEV incumbent 및 잠정 TEST 기준, E025는 보존된 대안이다.
E025의 synthetic UNHCR +.0005084489956005411은 실제 TEST 우위·승률 근거가 아니다.
UNICEF/WB 차이는0. 이번 기술 공백 해소로 E025를 최종 선택하거나 E041을 폐기하지 않는다.

A012 사후 provenance, 옛 환경의 미기록 항목, 더 오래된 E025 U/WB drift 원인,
private hosted 환경·숨은 응답의 실행시간·효용은 여전히 미확정이다.
표본 process-tree peak는 미관측 순간 최대값의 보장이 아니다.
S3 공식 evaluator의 기존 truth 순서와 별도 source 출력 동결 후 평가를 구분한다.

E064는 고정 DEV 준비본으로 대기한다. Codabench 장애는 사용자 보고이며 이번 S0에서
현재 상태·복구 시각·slot을 조회하지 않았다. 복구 시 기존 한 번의 사용자 DEV 제출
권고와 사전 SCORES를 사용한다. 자동 업로드·동일 정책 반복은 없다.

## 다음 한 가지 권고

**별도 S3에서 E041/E025 검토용 방법 문서와 4쪽 PDF를 각각 완성한다.**
기존 초안의 E025 미완료 문구를 최신 완료 증거로 교체하고, 두 모델의 실제 차이와
노출·refit·평가 한계를 정확히 전달한다. 최종 선택 뒤 문서를 급하게 만드는 위험을 줄인다.
점수 개선 실험이나 TEST 우위 증명으로 설명하지 않는다.

현재 초안의 E025 provenance 미완료 설명은 작성 당시에는 맞았으나 현재 설명으로는
낡았다. 과거 초안을 고치지 않고 새 버전에 S3 결과와 남은 한계를 함께 반영한다.
기존 문서 환경의 경로 존재만 확인했다. 실제 렌더 가능성은 실행하지 않았다.

이는 기존 `s3-prep/revalidation-plan.md`의 **최종 문서 확정**과 구별되는
**검토용 초안 제작** 제안이다. 미확정 Terms와 코드 라이선스는 명시적으로 남긴다.
그 두 입력이 없다는 이유로 편집·렌더·시각 검토까지 미룰 필요는 없다.
반대로 초안 완료를 라이선스 부여·최신 Terms 충족·업로드 승인으로 읽어서는 안 된다.

신규 제안 한도: gross60분(마지막10분 종료 기록), 문서 실행합300초,
PDF 후보당 최대3회/총6회, CPU2/GPU0/동시 작업1/관측 메모리2GiB,
설치·유료·모델 실행0. 이전 S3/B01 잔여량을 재사용하지 않는다.
수정은 새 문서/문서 전용 renderer 복사본과 영향받은 페이지에 한정한다.
[별도 S3 인계](s3-method-review-drafts.ko.md)는 사용자 실행 지시 전까지 대기다.

최종 모델 선택, 팀 원본 코드의 권리자·라이선스 범위, 최신 Terms/정확한 Final 시각,
계정·slot·실제 전달은 이후 별도 결정이다. 현재 시각을 임의로 대회 마감에 대입하지 않는다.

## 보존과 소유권

S3 release 17:01:07.378603 KST 확인 후 S0가 17:12:04.890044 KST 단독 쓰기를 인수했다.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, git 경로목록125개 dirty 유지.
이는 directory-collapsed 목록이며 모든 파일 바이트의 전수 보존 검사 주장은 아니다.
진입 Python/pythonw/uv 이름 census0; 다른 채팅·원격 자원 전체 census는 아니다.
쓰기 범위는 이 새 폴더와 status/log/phase2 현재 안내뿐이다.

E057/E060/E061/E062/E063/E064 parked, E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD/A039/A040 및 모든 기존 STOP/HOLD 유지.
17999명/12339SSUID·집계·A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 보존. A_half 비승격, A018 사용자 미확정.
S3 승인된 준비는 완료됐으나 최종 TEST 선택/업로드는 미실행이다.

모델/데이터/ZIP/검증 재실행/렌더/설치/플랫폼/서브에이전트/commit/push0.
원래 기록은 소급 수정하지 않는다. 최종 [verification](verification.json)의 명시적
쓰기 해제 이후 owner 없음. 다음 사용자가 승인한 S3가 인수하며 S0는 대기한다.
