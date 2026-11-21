# A043 S1 closeout

2026-10-11 KST. **CONTRACT_READY_FOR_S0_REVIEW.**
사용자가 전달한 A043 정보·설계 검토만 수행했다. S1의 실행 권한은 문서/정적 source
검토와 새 문서4개·status/log 결과 추가까지다. 모델·실험·S2 권한이 아니다.

확정한 계약은 [contract.md](contract.md). 독립 conditional heads와 초기화/forward/
pooled CE/denominator를 보존하고 conditional 입력 representation에만 stop-gradient를 둔다.
Conditional head parameter는 계속 학습한다. 기존 tune hook으로 config2와 final refit을
연결한다. 학습 가능성은 chain rule·소스에 근거한 설계이며 autograd 실측이 아니다.

새로 분명해진 사항:

- Conditional CE의 직접 trunk gradient만 제거한다. Denominator, inner stop, outer
  config, final epoch/config, w 선택 및 replay lambda에 간접 영향은 남는다.
- E041 metric fit/section activity/donor/replay 자격은 neural 출력 인자를 받지 않아
  동일 input/runtime에서 기대 불변이다. Lambda 활성·최종 출력은 달라질 수 있다.
  S0의 포괄적 영향 목록을 이렇게 구체화했으며 S0 원본은 수정하지 않았다.
- W 선택 때 net은 inner train checkpoint다. 별도 outer-fit 재학습은 없다.
  W=0이어도 정상 final refit 비용은 발생한다.
- Forward loss는 같고 derivative만 달라지므로 전체 CE finite difference는 H gradient
  검증 기준이 아니다. 분기별 gradient·conditional head 갱신 검사가 필요하다.
- 정상 R/H는6pipeline/18neural/16metric. Fresh E025와 assembly·official all3까지
  계획하면 정상 합15/45/32. 작은 검사·fallback·실패·검증 비용은 별도 계수하고
  총시간에 포함한다. 이는 정적 호출 계획이며 새 시간/메모리 실측이 아니다.

E012의 공동 학습 이득과 E061 hosted adverse를 반대 근거로 유지한다. H는 E061의
head 제거/tying, E060 metric loss, E062 ordinal output, E063 round metric과 다르다.
차이 자체가 개선 근거는 아니다. 단일 경로의 잘못된 연결/NO_OP/비용을 반박할 수 있고,
장래 한 정책의 favorable/adverse/unresolved 관측이 다음 우선순위를 바꿀 수 있어
제한된 구현 검토에 넘길 계약 가치는 있다고 판단했다.

미확정: 실제 gradient 충돌/손해, 현재 E041 손실 지도, 새 후보 효과·runtime·peak,
모델/assembly parity, clean E025/S2 release, 향후 hosted 결과. 유효한 새 numerical
oracle 없음. Synthetic은 노출된 공학 채널이며 실제 UNHCR gain의 상·하한이 아니다.
공개 동점으로 미세 효과를 복원하지 않는다. 같은 정책 재제출/seed·head·계수 구제 없음.

진입 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1 / work/e050-submission,
dirty116, named python/pythonw/uv jobs0. Workflow2026-10-05-r5를 실제 읽었고
SHA256 a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
AGENTS/CLAUDE/status/latest3log/workflow 순서 및 허용 source 본문 읽기 근거·해시·
시작/종료와 보존 검사는 [verification.json](verification.json)에 기록한다.
S0 pre-write manifest와 비교한21개 중19개 일치, status/log2개는 S0 후속 기록 차이.
현재 바이트를 기준으로 보존하며 과거 해시로 되돌리지 않았다.

이번 scientific/model/import/autograd/fit/predict/score/fixture/test0,
새 응답·키·Parquet/NPZ/cache/checkpoint/ZIP 접근·재해시0, 새 웹/원격/현금0.
현재 설치 Torch optimizer 파일은 필요한 텍스트만 읽었다. Import/설치/환경 변경 없음.
문서 처리 중 Git ownership/ignore 경고, JSON 출력/배열 처리, UTF-8 표시와 출력 절단을
같은 범위에서 고쳤다. 실제 데이터/모델 실행 실패나 재시도가 아니다.
전체40분(마지막10분 기록) 상한을 초기화하지 않았다. 정확한 gross는 verification 기준.

다음 행동은 [S0 인계](s0-handoff.ko.md) 검토뿐이다. 새 구현/실험 등록·S2·ZIP·업로드·
commit/push·S3/TEST 선택으로 전환하지 않았다. E041 incumbent/E025 fallback,
E057/E060/E061/E062/E063 parked/E063 UNRESOLVED, E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD/A039/A040 및 모든 STOP/HOLD 유지.
17999명/12339SSUID·집계·A022 원래 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격/A018 미확정/S3 중단/S2 후보 없음.
