# A040 C6 — NOT_REPRODUCED / A040 HOLD 유지

2026-10-26 KST. 사용자 지정 S1-A040-C6 한 건 종료. 실제 FunctionCreate fixture
graph 생성과 설치된 FunctionInfo parser 소비 뒤 **Python 본체40428 및 launcher53860
모두 exit0**. Parser-return marker, assertion, native process receipt, 빈 stderr가 일치한다.
추가 측정·수리·C7·전체 lifecycle·모델·원격 실행을 시작하지 않는다.

## 관측과 해석

- C3의 image 정의-only 정상 exit0 기록을 재사용했다. C6도 실제 graph/parser 뒤
  정상 종료했다. 이번 조건에서는 이 추가 경로만의 crash 충분성을 지지하지 못했다.
- C4/C5 진단 변경이 들어간 최신 소스를 C3 기준으로 오인하지 않았다. C3 preflight의
  검사 코드와 전체 source manifest를 정확한 해시로 복원했고, C3의 endpoint/transport
  보존본을 새 폴더에서 사용했다. 과거 C1–C5 재실행0.
- Fixture trace의 외부 서비스 대역 호출은 WorkspaceNameLookup/AppGetOrCreate/AppStop
  세 개뿐이다. 실제 인증/RPC는0. 이름은 대역 프로토콜이며 원격 자원 조회/생성/종료가 아니다.
- 실제 Image.build/resolve·mount thread pool·installer body·출력 wrapper 실행0.
  C6 graph/parser 외 인과적 개입 없음; 진입 제한·경로·관측·감시 변경은 diff로 분리했다.
- Build/resolve 복합 경로의 종료 crash는 여전히 미해결. 단일 음성 관측이 간헐적 crash의
  부재, upstream protobuf 무결함 또는 전체 root cause를 증명하지 않는다.

## 오류·비용·한계

첫 감독 시도는 원래 진입 감시기가 자기 conhost를 예상 밖 자식으로 보아 **Python 시작 전**
중단했다. launcher_pid=null, parser0. 실패 receipt/source/freeze 보존 후 그 콘솔을
소유 tree 감시에 포함하고 종료 시 정리하도록 수정했다. 유효 측정 뒤의 재시도가 아니다.
첫 receipt의 boundary_observation_unknown=true는 launcher 없는 경우의 일반 필드였으며,
새 보충 freeze는 그 전진입 사실을 명시한다. 원본 receipt를 수정하지 않았다.

감독 시도2/3, 유효 C6 1/1, Python 호출1(venv launcher+본체2 OS processes).
외부 명령 관측0.8349515+2.7974121=**3.6323636/90초** 보수적 차감.
내부 outer stopwatch 합3.3144037초는 중복 합산하지 않는다. 각 시도30초 이내.
Python 강제종료0; 자기 감독자 conhost 정리2는 별도로 공개한다.
CPU affinity3/2논리CPU, GPU0, 모델0, 현금/원격0. 관측 tree RSS237060096bytes,
private175984640bytes 각각2GiB 이하;7표본, 최대 gap0.296771초. 연속 peak 증명은 아니다.
소유 자식 모두 회수. 종료 뒤 별도 AIMO 작업 Python들이 관측됐지만 접근/종료하지 않았다.

Python3.13.14/Modal1.6.0/synchronicity0.12.5/protobuf6.33.6/grpclib0.4.9와
venv 경로는 기존 기록과 일치한다. 현재 직접 환경20개 파일의 해시를 동결했다.
옛 C3에 전체 native/interpreter 해시가 없으므로 과거의 완전한 binary identity를
소급 증명하지 않는다. 실제 기록된 버전·소스 대응 범위의 비교다. 환경 교체/설치0.

## 반환

S0는 **이 graph/parser 단독 충분성 경로를 지지하지 않은 관측**을 수용하고 A040 HOLD를
유지한다. 다음에 다른 진단을 고려하려면 build/resolve 복합 경로를 구별할 새 원인 근거,
단일 비교·소스 대응·별도 예산이 필요하다. 지금 새 수리/환경/모델 실행을 자동 제안하지 않는다.
성공 lifecycle, H100900초, 실제 효능 또는 release/S2 PASS가 아니다.

기존 STOP/HOLD·평가 노출 보존. E041 incumbent/E025 fallback, E057/E060/E061/
E062/E063/E064 parked; E062/E063/E064 공개 tie UNRESOLVED. E058 STOP/E059
STOP_SELECTION/A023/A024 empirical HOLD/A039/A040 유지.17999/12339SSUID·집계/
A022 역할·E059 소비1918/1124·2007/1130 및 보호2074/1177·calibration1866 보존.
A_half 비승격/A018 사용자 미확정, 새 S3/TEST 선택 없음. ZIP/commit/push/서브에이전트0.

근거: registration.md, source-environment-freeze*.json, c3-to-c6.diff,
source.diff 및 supervisor*.diff, c6-02-process.json, attempts/c6-02/trace.jsonl,
cost-time-ledger.json. 보존·최종 jobs·쓰기 해제는 verification.json.


종료 보충: S0의 21:32:42 shared 문서 갱신을 최종 보존 확인에서 발견했다. S0 해제 receipt를 확인하고 최신 status/log에 C6 관측만 추가했다. 양 세션 기록이 시간상 겹쳤으며 단일 writer 준수를 소급 주장하지 않는다. 동결 C6 소스 변화는 없고 새 전략은 보존했다. 쓰기 해제 후 S0 검토 대기.
