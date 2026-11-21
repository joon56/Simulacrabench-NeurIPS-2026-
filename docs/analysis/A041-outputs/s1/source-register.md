# A041 S1 — source register

조회일 2026-10-07 KST/UTC. 새 primary 문서 **2/3**. 같은 문서의 method/supplement 재열람은 중복 논문으로 세지 않는다. 제3 cumulative-link 문서는 결정에 필요하지 않아 열지 않았다. 이 표는 읽은 범위와 근거를 구분한다.

| 원전 | 실제 읽은 범위 | 이 설계에 필요한 사실/한계 |
| --- | --- | --- |
| Cao, Mirjalili, Raschka, CORAL, arXiv1901.07884v7 (2020-11-13), [full text](https://arxiv.org/html/1901.07884v7) | §3.1–3.2.3, 식1–7 및 rank-consistency theorem, 실험 목적/지표 | 공통 weight와 threshold bias, threshold label/BCE, 최적 bias 순서. 유한 early-stop/HSCC 범주 calibration 증명 아님 |
| Shi, Cao, Raschka, CORN, arXiv2111.08851v5, [full text](https://arxiv.org/html/2111.08851v5) | §3.2–3.6 식2–6, §8.1 likelihood, §5 결과/ablation | 조건부 risk set, chain product, risk-set 총크기 분모, 안정 log-sigmoid. 원 논문 MAE/RMSE 결과를 HSCC log-score 효능으로 옮기지 않음 |

Not answered 분리, 일곱 범주 NLL 유도, 기존 pooled denominator 유지, 초기 parameter 복사, WB 귀속/비용/관측 설계는 A041의 자체 적용 제안이다. 논문이 이 HSCC 계약을 검증했다고 쓰지 않는다. 원문 인용 대신 필요한 내용만 요약했다.

## 로컬 자료 및 소스

19개 허용 입력의 expected/현재 SHA와 비교는 [entry.json](entry.json). 실제 source/schema/S0 문서 보존 기준은 [preservation-before.json](preservation-before.json). 해시 계산과 본문 읽기는 구분한다.

- 순서대로 읽음: AGENTS → CLAUDE → status → log 최신3 → workflow r5 → A041 review/inputs 및 saved handoff. 읽기 evidence/tool chunk는 entry에 기록. workflow SHA `a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23`.
- A041 S0 review/inputs/verification/handoff: 고정16개와 과거 읽기·STOP 요약 재사용. 기존 inventory 재생성 없음. 공개 WB schema는 metadata 부분을 읽고 지정 bytes만 hash 확인. 실제 분포/표본 통계 접근 없음.
- E041 snapshot: `_layout`/`_complete_rows`/GIVEN encoding, ladder selection, pooled loss, network/train/config/w/refit, gate agreement, donor/λ, E025 및 E041 최종 dispatch를 읽음. 핵심 line anchors는 cost-accounting에 기록. 현재 production wrapper의 WB 경로를 snapshot과 대조.
- `src/models/shared_trunk.py`, `hh_cap.py`, `supervised_retrieval.py` 본문 읽음. `cond_agree.py` 관련 앞부분, `external/starter-kit/score.py` 공식 floor/score, `src/eval/logloss.py` 읽음. 전부 텍스트 읽기만, import0.
- E011/E030/E061 실험 문서 본문 읽음. E017/E026/E029/E012/A004는 S0 review의 요약을 승계하고 허용 hash를 확인. 이 세션에서 그 전부를 재검증했다고 주장하지 않는다. E011 대상 제외/과거 null을 새 결과로 바꾸지 않는다.
- E061 과거 비용은 실험 문서의 기록만 사용. 출력 경로의 파일명 목록을 찾던 읽기 전용 `rg --files`가 과거 official-work 임시 디렉터리3곳에서 Access denied를 반환했다. 재시도/권한 확대/파일 내용 접근 없음. 비용 사실은 이미 읽은 E061 문서로 충분하여 조사 중단.

S0 inputs19개 중17개 동일. status/log 두 개는 S0 작성 전 hash와 다르지만 A041 S0 verification의 작성 후 hash와 일치한다. HEAD는 기준과 동일. 현재 파일을 과거 hash로 되돌리지 않았다. 세션 시작 dirty91; 기존 변경 수가 S0 entry89보다 큰 이유는 당시 추가된 A041 문서/경로가 현재 포함되기 때문이다. 숫자만으로 작성자/수정 부재를 보증하지 않는다. 최종 보존 비교는 verification을 따른다.

초기 일부 PowerShell 기본 디코딩 재열람 출력이 깨져 관련 문서는 `-Encoding UTF8`로 다시 읽었다. 파일 바이트 변경 없음. 보고서 인용/판독은 UTF8 본문 기준이다.
