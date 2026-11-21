# S0 인계 — A040 Modal 재개2, 첫 준비 오류 STOP

**BLOCKED_SPECIFIC_INPUT / LOCAL_BUILD_LOGGING_FAIL**.
비용 계약 변경은 적용했고 원격 이미지 준비1회를 시작했다. 과거 엄밀한
USD1/5 보장 문제로 다시 차단하지 않았다. 이번 중단은 로컬 실행기 결함이다.

필수 기록: closeout.md, build-result.json, cost-policy.md, cost-ledger.json,
app-terminal.json, termination-receipt.json, verification.json, entry.json.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1 유지. 기존 dirty/기록 보존.

사실:
- SDK1.6.0·인증 재사용. 사용자 credits30/spend0/usage30 보고 승계.
  예산 API 재조회·재로그인·재설치·한도 변경·공급사 문의 없음.
- 단일 이미지 recipe 요청 뒤 Modal 진행 로그 U+2022를 cp949로 출력하다
  UnicodeEncodeError. 코드 수정·재빌드 없이 첫 오류 STOP.
- App `ap-CJkQ7byYW3D872nirY6KRM`: 00:48:37KST 생성,00:48:40 종료.
  정상 CLI와 별도 API로 stopped/잔여 task0 확인. 처음 cleanup 호출은
  task-context 경고와 로컬 대기 문제가 있어 별도 확인이 필요했다.
  해당 로컬 controller 두 PID만 종료; unrelated job 종료 없음.
- Base image `im-eWgRNij0VH6mzozlOzEyxy`: 원격 SUCCESS 확인.
  전체 dependency 이미지 성공이 아니다. Linux pins/이식/경계/H100/
  reference/candidate 모두 미완료 또는 NOT_RUN. 단일 과학 allowance 미사용.
- 최신 요약 metered0/billed0, 세부 Deployed Apps0.00001152USD.
  게시 지연·귀속·cache 잔여 비용 미확정. 최종 청구액0 보장 안 함.
- 빌드 recipe metadata 전송은 있었음. 기존112 staging 파일/응답/checkpoint
  전송·재해시·역직렬화는 없음. 원본/기존 성공 suite/실험 정책 변경 없음.

다음 S0 판단:
재개한다면 모델 없는 Windows UTF-8 출력 및 cleanup 계약 수정만 먼저
별도 지정해야 한다. `-X utf8`/stdout·stderr 설정과 리다이렉션 하 Unicode
로그 회귀, 단일 async SDK 경로·bounded cleanup/terminal 확인을 검토한다.
이번에는 해당 수정·회귀·추가 원격 요청을 하지 않았다. base image 재사용도
별도 허용과 identity 확인 후 판단. 남은 시간을 자동으로 새 시도에 부여하지 말 것.

원래 reference/candidate 각1회900s, H1001개2400s, CPU/메모리/offline/
중복 방지·데이터 정책 그대로. 비용USD1/5는 계획, 현금0·설정 불변.
기존 STOP/HOLD·보호 audit/calibration·E041/E025·parked 유지.
S2 후보 없음, S3 중단/A018 미확정. S0 검토 전 S2로 넘기지 않음.
