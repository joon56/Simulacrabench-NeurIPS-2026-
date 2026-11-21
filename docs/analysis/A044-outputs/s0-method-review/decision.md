# S0 — E041/E025 방법 검토본 수용

2026-10-23 KST. **REVIEW_DRAFTS_ACCEPTED / FINAL_DELIVERY_NOT_APPROVED.**
S0 문서 내용·완료 증거 검토다. 원래 S3 결과와 산출물을 변경하지 않는다.

## 수용한 결과

E041/E025 영문 방법 문서와 각각4쪽 PDF를 검토용 산출물로 수용한다.
두 Markdown 본문, 근거표, 식별표, 미결정표 및 종료 증거를 읽었다.
14개 지정 S3 문서/PDF와3개 공유 문서의 현재 SHA256이 S3 기록과 일치했다.
main/ZIP 식별값은 문서에서 승계했으며 이번 S0가 모델/ZIP을 재해시하지 않았다.

두 모델의 차이, E025 새442425 raw 연결, E041 frozen 결과 재사용, synthetic 비교와
실제 TEST 효용의 구별, 옛 drift/환경/provenance 한계가 문서에 반영돼 있다.
E064 실제 DEV 결과를 만들어 쓰지 않았고, 라이선스 제안을 유효한 grant로 쓰지 않았다.
내용 검토에서 확인한 최종화 전 문구 보완은 아래 한 곳이다.

4쪽/각6개 링크/텍스트 경계/8페이지 시각 검토는 S3 검사 기록을 수용했다.
S0는 PDF를 다시 렌더·추출하거나 모든 PNG를 새로 육안 검사하지 않았다.
현재 PDF hash 확인과 S3의 시각 검사 증거는 구별한다.
S3 비용은125.5812167/300초, gross1441.187559/3600초, PDF1회씩/실패0.
성공한 문서 작업·모델 검증을 반복할 근거가 없다. 미사용 예산은 이어 쓰지 않는다.

- [E041 검토 PDF](../s3-method-drafts/E041-review.pdf)
- [E025 검토 PDF](../s3-method-drafts/E025-review.pdf)
- [원래 S3 검증](../s3-method-drafts/verification.json)
- [문서·소스 연결표](../s3-method-drafts/document-pairing.json)

## 최종화 때 적용할 문구 보완 — 즉시 재렌더 과제 아님

E025-review.md §3의 `practical UNHCR resolution, about 0.015-0.03`은 원래
2026-09-25 방법 문서의 Grand 차이 역산 설명을 승계했다. 현재 문장에는 그 과거
관측 방식의 범위가 충분히 드러나지 않는다. 기관별 API 값이 제공되는 현재 방식의
일반적 검출 한계나 고정된 최소 효과로 읽으면 안 된다. 직접 기관별 공개 값에도
privacy rounding/noise가 남으므로 raw 정밀도나 유의성 보장으로 대체하지 않는다.

다음에 E025를 최종 문서로 갱신할 때 해당 숫자 문장을 다음으로 교체할 것을 제안한다:

> These historical probes were interpreted using rounded, noised released scores and, where needed, Grand differences under unchanged controls. Their differences do not provide precise effect estimates. Current directly reported per-instrument API values remain privacy-rounded; they are not unrounded raw scores or a universal detection threshold.

역사적 .015-.03 문장을 원본에서 삭제하거나 결과를 소급 변경하지 않는다.
현재 review PDF의 완성/시각 검사 사실도 취소하지 않는다. 최종 선택·Terms·라이선스에
따른 문서 갱신과 함께 처리한다. 이 한 문장만을 위한 새 S1/S3 실행 인계를 만들지 않는다.

## 새 사용자 입력과 남은 결정

이번 채팅에서 사용자는 E041/E025 **팀 자체 작성 코드에 대해 본인 단독 권리자로
확인했다**고 답했다. 권리자 정보는 사용자 확인으로 기록한다. 법적 독립 검증,
제3자 권리 소멸, 전체 저장소 소유권, 라이선스 부여나 공개 승인으로 확대하지 않는다.
원래 S3 open-decisions의 미확정 기록은 당시 상태로 보존하고, 현재 변화는 이 문서에 둔다.

남은 사용자 결정은 적용할 정확한 팀 코드 라이선스 문구·대상 파일과 최종 TEST 모델이다.
기존 [라이선스 범위 제안](../s3-prep/license-inventory.md)을 검토할 수 있으며 새로운
라이선스 후보를 만들거나 MIT 제안을 자동 발효하지 않는다. 원래 notice는 보존한다.
최종 모델은 E041 잠정 기준/E025 대안 유지. E064 DEV 판독은 아직 없다.

현재 Terms/방법 의무와 Final의 정확한 timestamps/timezone, 실제 계정/slot/전달은
별도 확인 대상이다. 사용자 보고 Codabench 장애의 현재 상태는 이번에 조회하지 않았다.
라이선스 선택과 실제 전달 의무 충족은 별개이며, 날짜-only 기록을 마감 시각으로 바꾸지 않는다.

## 다음 행동과 재개 조건

오프라인 준비의 두 명시된 과제(E025 provenance, 두 방법 검토본)는 완료됐다.
같은 검사를 다시 하거나 제출 개수를 채우는 새 가설을 만들지 않는다.

1. 사용자: 두 PDF 내용 검토와 팀 코드 라이선스 범위/문구 결정. 이것이 모델 선택이나
   업로드 승인까지 포함하지 않음을 명시한다. 이미 답한 권리자 확인은 다시 요청하지 않는다.
2. 플랫폼 사용이 가능해지면: 기존 E064 고정 ZIP의 사용자 DEV 제출·기존 사전 arm 판독.
   신규 후보/재학습/자동 업로드 없이, 실제 결과가 오면 지정된 결과 기록 절차를 사용한다.
3. 최종 모델·라이선스·적용 Terms/정확한 시간이 확보되면: 선택한 방법만 새 최종본으로
   갱신하며 위 문구 보완·제출 시점 사실·선택 표시를 함께 반영한다. 별도 승인된 문서
   범위가 필요하며, 변경 없는 모델을 다시 학습하는 단계는 기본으로 포함하지 않는다.

그 전 새 정보 없이 동일 HOLD 검토나 문서 렌더를 자동 반복하지 않는다.
새 연구 배치를 요청받으면 별도 S0 문제 선정으로 다루며 이번 문서 수용과 혼합하지 않는다.

## 보존·소유권

Outgoing S3 해제17:50:01.187559 KST 확인 후 S0가18:54:38.550197 KST 인수했다.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, branch work/e050-submission.
S0의 git untracked-normal 목록125개와 S3 untracked-all2557개는 집계 방식이 다르다.
진입 Python/pythonw/uv 이름 census0; 모든 다른 채팅/원격 자원 부재 주장은 아니다.
이번 쓰기는 새 s0-method-review 폴더 및 status/log/phase2 현재 안내뿐이다.

E041 incumbent/잠정 TEST 기준·E025 대안, E057/E060/E061/E062/E063/E064 parked, 모든 기존 STOP/HOLD,
17999명/12339SSUID·집계·A022 원래 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866, A_half 비승격/A018 사용자 미확정 유지.
모델/과학검사/보호 데이터/ZIP/렌더/네트워크/설치/서브에이전트/업로드/commit/push0.
최종 [verification](verification.json)에 쓰기 해제와 보존을 기록하고 대기한다.
