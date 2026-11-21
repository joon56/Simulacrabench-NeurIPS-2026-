# A044 — 2026-10-22 공개 규칙 읽기

S0의 공개 문서 관측. 로그인/계정/slot/제출/kit 업데이트/데이터 다운로드 없음.
웹 도구로 본 현재 공개 내용이며, 원격 bytes의 독립 hash/실행 증명은 아니다.

| 근거 | 관측 | 후속 처리 |
|---|---|---|
| [공식 사이트](https://simulacrabench.org/) | DEV Nov13; Final Nov14–18; shared900/3600초; DEV 일1회/Final1회; visible-row training 허용 | 옛 A018 Nov1–14 일정을 현재 일정으로 쓰지 않음 |
| [공식 config](https://raw.githubusercontent.com/SituatedEvals/public/main/config.yml) | phases1.ends2026-11-13; phases2.starts2026-11-14/ends2026-11-18; floor.001; H100/CPU8/RAM16GB | 날짜만으로 timezone/정확한 마감 시각을 생성하지 않음 |
| [공식 README](https://github.com/SituatedEvals/public/blob/main/README.md) | 같은 새 날짜, TRAIN→DEV / TRAIN+DEV→TEST, shared compute, config를 phase 계약 출처로 명시 | pinned revision·핵심 source/schema 차이는 S3가 확인 |
| Codabench competition/API 직접 공개 조회 | 도구 fetch 실패 | 현재 Terms, phase timestamp, method 의무의 적용 범위 미확정 |
| GitHub main commit API | 도구 접근 실패 | 최신 commit SHA를 추정하지 않음; S3에서 공식 pinned revision 확보 |

사이트는 winning teams의 method/source 제공을 요약한다. A018의 9월 보존 Terms는
모든 TEST entry에 네 페이지 method를 요구한 것으로 기록돼 있다. 이번 S0에서
최신 Terms를 확보하지 못했으므로 충돌을 해소하거나 의무가 사라졌다고 단정하지 않는다.
둘 중 어느 경우에도 method 초안을 준비할 가치는 있다. 법적 라이선스를 새로 부여하지 않는다.

현재 config에는 sandbox trait_scale2.0 등 생성 설정도 보인다. 기존 허용 synthetic와
동일하다고 확인한 것은 아니다. 생성기/문서 날짜 변경과 scorer/schema/model 계약의
변경을 분리한다. 새 synthetic를 자동 생성하거나 기존 input freeze를 교체하지 않는다.
기존 완료 검증은 그 바이트/계약에 대한 역사로 남는다.

S3는 정확한 규칙/일정/표본계약의 현재 근거를 표로 남기고 B01과 공유한다. 공개
자료로 해결되지 않는 계정 권한/잔여 slot만 사용자 확인 대상으로 남긴다. 자동 문의 없음.
