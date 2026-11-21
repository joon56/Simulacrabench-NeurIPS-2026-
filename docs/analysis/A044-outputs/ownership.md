# A044 — shared checkout 쓰기 담당

작성만으로 다른 채팅을 시작하지 않는다. 아래는 제안된 순서다.

1. **S0 A044**: 이번 운영 문서/인계 작성 담당. 종료 verification에 named jobs,
   HEAD/dirty 보존과 release를 남긴 뒤 대기한다. 이후 executor 중 S0도 파일을 수정하지 않는다.
2. **별도 S3-PREP-A044**: 사용자가 S3 인계를 실행하라고 전달한 뒤 단독 인수.
   `docs/analysis/A044-outputs/s3-prep/entry.json`과 status에 수락 시각/읽은 개정/범위 기록.
   종료 시 `closeout.md`에 jobs/산출물/해제를 남긴다. 준비 범위를 넘어 TEST 선택하지 않는다.
3. **별도 EXEC-B01-E064**: S3 해제 뒤 사용자 배치 지시를 받고 단독 인수.
   `docs/analysis/E064-outputs/s2/batch-entry.json`과 status에 인수 기록.
   완료 또는 hard stop 시 과거 실패를 보존하고 closeout/jobs/해제를 남긴 뒤 S0로 반환.
4. **S0 결과 검토**: 실행 세션 해제 확인 뒤 문서 판단만 재개한다.

각 인계는 소유 경로·미완료 작업·진행 중 PID/로그 또는 관측된 none을 포함한다.
status의 owner 문자열은 파일 잠금이 아니다. 다른 사용자 세션이 쓰는 중이면 기다리고,
그 세션의 종료를 임의로 선언하거나 프로세스를 종료하지 않는다. named Python jobs0은
모든 앱/다른 채팅/원격 작업이 없다는 증명으로 쓰지 않는다.

## S3 새 채팅에 붙여 넣을 지시

```text
이 별도 S3 세션에서 C:\Users\USER\Desktop\SimulacraBench\docs\analysis\A044-outputs\s3-test-preparation.ko.md를 읽고, 문서·공개 규칙·기존 검증 유효성 검토 범위와 신규 gross90분/비용0을 승인해 실행해줘. S0의 쓰기 해제를 확인하고 단독 인수해줘. 모델 실행·패키징·최종 TEST 선택·업로드·commit/push는 제외한다.
```

## S3 해제 후 별도 실행 채팅에 붙여 넣을 지시

```text
이 별도 실행 세션에서 C:\Users\USER\Desktop\SimulacraBench\docs\analysis\A044-outputs\batch-01-e064-release.ko.md의 B01을 승인해 실행해줘. 후보는 E064 하나이며 완료된 S1은 반복하지 말고 S3 문서 준비의 인계·쓰기 해제와 진입 조건을 확인한 뒤 남은 S2부터 진행해줘. 신규 gross180분/계산3600초/각 all3 900초/최대4 all3 시작/비용0 및 문서의 세부 상한을 승인한다. 업로드·새 유료 자원·새 가설·S3·서브에이전트·commit/push는 제외한다.
```

문구를 사용자가 해당 별도 세션에 전달하는 것이 실행 지시다. S0가 이 파일을
작성하거나 executor가 과거 파일에서 발견했다는 이유만으로 실행하지 않는다.
