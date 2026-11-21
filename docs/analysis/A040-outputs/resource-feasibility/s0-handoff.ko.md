# S0 인계 — A040 H100 자원 정보 조사 완료

S0에서 검토·판단만 수행한다. 이 인계는 임대·접속·설치·실행 허가가 아니다.

판정: **HOLD_SPECIFIC_INPUT / EXECUTION_NOT_AUTHORIZED**.
RESOURCE_OPTION_DOCUMENTED는 공개 선택지를 기록했다는 뜻이며 자원 확보나
H100900초 통과를 뜻하지 않는다. 공식 문서6개·옵션2개 안에서 조사 종료.

먼저 [closeout](closeout.md), [옵션](options.md),
[전체 비용·이식 범위](cost-and-porting.md), [검증](verification.json)을 읽는다.
HEAD는 a43f4379ec78dbc2de260463eef67bb1d567d7e1 그대로. 기존 dirty work 보존,
commit/push 없음. 새 정보 기록과 status/log만 추가했다.

남은 사용자 결정: 자원/지역 선택, 계정 또는 기관 사용 권한, **총지출 상한과
통화**, 유료 준비 시간 한도, 종료·과금 확인 책임자. 현재 모두 미확정이다.
공급사/권한 있는 계정 소유자가 재고·quota·전체 GPU 독점/MIG 조건·실제 견적을
확인해야 한다. 에이전트가 로그인·문의·구매하거나 예산을 대신 설정하지 않았다.

기본 Ubuntu/Python과 기존 Windows3.13.14 환경이 다르다. 이미지·driver/CUDA·
Linux 의존성 바이트, Windows watchdog 이식과16GB private commitment 정의,
CPU2·단일 GPU·네이티브 네트워크 차단은 후속 검증 조건이다. 공개 VM 문서나
Docker 지원만으로 이 조건을 PASS 처리하지 않는다.

사용자 결정 후에도 S0가 별도 범위를 정해야 한다. 후속 최소 실행안은 동일
모델/context/head/입력/선택·guard 유지, 새 target reference와 candidate 각1회,
각900초·전체 검증·첫 오류 STOP. 새 출력에서 시작하며 과거 부분상태 재개나
실패 기록 변경은 금지. 준비·설치·취득·검증·export·종료도 유료 비용에 포함.
공급사 Terminate 확인까지 책임을 정해야 하며 process 종료만으로 과금 종료가 아니다.

RTX3070 LOCAL_RESOURCE_LIMIT 유지.641.0873초는 expert predict 호출과 CUDA
동기화의 합으로 GPU 단독 시간이 아니다. H100 배속/완료시간/실제 효과 미확정.
가짜 S/E 수락과 부분 parity는 S2 자격이 아니다. 성공하더라도 S0 검토 전
S2로 넘기지 않는다. S2 assembly/source parity·ZIP checker·official all3·
E025/E041 비교·SCORES 판독/제출 바이트 확인은 모두 이번 범위 밖이다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 기존 STOP/HOLD와
17999명/12339SSUID·A022 역할/집계 노출·E059 소비 및 보호 경계 유지.
A039 HOLD 별개, A_half 비승격, A018 사용자 미확정/S3 중단/S2 후보 없음.
