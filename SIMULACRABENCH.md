# SimulacraBench (NeurIPS 2026) — 작업 폴더 브리핑

> 작성: 2026-08-09 · 출처: situatedevals.org/simulacrabench (공식) + IT RADAR + career-tracker seed v5
> 공식: <http://situatedevals.org/simulacrabench> · 문의: h4upt@stanford.edu

## 0. 한 줄 요약

미공개 UN 마이크로데이터(21개국 ~6.1만 명, ~150문항)로 서베이 응답 행렬을 **확률적으로 완성**하는 대회. 평가지표는 mean test log-loss(strictly proper, calibration 민감). Docker 코드 제출, 폐쇄 샌드박스 채점. **트랙별 top-3 = NeurIPS 프로시딩 논문 공저.**

## 1. 핵심 일정 (전부 2026)

| 날짜 | 내용 |
|---|---|
| **8/10 (월)** | 퍼블릭 런칭 + 등록 오픈 (Google Form) — **즉시 등록** |
| 8/10 – 10/31 | 개발 페이즈. 팀당 **하루 1회** 리더보드 제출 (매일 새로운 10% 샤드) |
| 11/1 – 11/14 | 테스트 페이즈. **최종 제출 1회**, 리더보드 동결 |
| 12월 | NeurIPS 시드니 Competition Track 세션 — 결과 발표 + 상위팀 발표 |
| 2027 Q1 | 프로시딩 논문 (트랙별 top-3 공저 초청) |

등록 폼: <https://docs.google.com/forms/d/1zx5P0XxUHGQcHgEnSH3eU-APnImDOXeL5u6_FLaE8hI/viewform>

## 2. 태스크

응답자 × 문항 행렬 완성 — 각 셀에 대해 응답 확률분포 예측.

- 문항 유형: binary, nominal, ordered Likert, multi-select, binned continuous. **skip-logic 게이팅이 별도 응답 레벨**로 취급됨 (중요 — 전처리에서 놓치면 손해).
- **Track A** — within-respondent imputation: 훈련 응답자마다 MCAR로 일부 문항 마스킹.
- **Track B** — cross-respondent generalization: held-out 응답자의 비인구통계 문항 전부 마스킹 (사회인구학 변수만 주어짐).
- 두 트랙 모두 참가 가능. Track B가 "AI가 도달 어려운 인구집단을 대표할 수 있나" 본질 질문에 가까움.

### 데이터 (전부 미공개 — 사전학습 코퍼스에 없음)

| 데이터셋 | 기관 | 국가 | 응답자 | 문항/웨이브 |
|---|---|---|---|---|
| CRA 2.0 | UNICEF | 6 | 20,229 | 72 |
| Faith & Immunisation | UNICEF | 10 | 19,847 | 26 |
| SkillCraft | World Bank | 남아공 1 | 7,000 | 58 |
| ERPIS 2025 | UNHCR | 시리아 난민 4개국 | 13,821 | 110 |

## 3. 평가·제출 규정

- **지표: mean test log-loss.** Accuracy 아님 — **캘리브레이션이 곧 점수.** 모달 클래스 때려맞추기 전략은 손해.
- 제출: Docker 이미지 또는 Python 스크립트+환경파일. 지정 API 구현. 주최측이 샌드박스에서 실행, **아웃바운드 네트워크 차단.**
- 마스킹 안 된 행렬 부분으로 제출 코드 내 학습 허용.
- 컴퓨트: **A100 1장.** 개발 페이즈 wall-clock **10분**/제출, 테스트 페이즈 **100분**/제출.
- 외부 사전학습 가중치: 공개 다운로드 가능 + 커밋 해시 지정 시 허용. **테스트 페이즈 전 사전 신고 필수.**
- 제출마다 **4페이지 method description** 첨부.
- top-3는 소스코드 비상업 연구 라이선스 공개 의무.
- 데이터 유출(exfiltration) 시도 = 실격. 동점은 paired-bootstrap 유의성 내 공동 인정.

## 4. 스타터 킷 (MIT 라이선스)

- Per-item marginal (트리비얼 베이스라인)
- **2PL IRT** (categorical-logistic likelihood)
- Low-rank ALS 행렬 완성
- **TabDDPM** (tabular diffusion)
- 스키마 명세 + 합성 샌드박스 (파이프라인 디버깅용)

## 5. 보상

- 종합 1위: NeurIPS 초청 발표 + 논문 저자
- 트랙 A/B 각 top-3: 10분 발표 + 프로시딩 공저
- LMIC·소외지역 팀 여비 지원
- UN Behavioural Science Group 공동 표창 (운영 후속검토 대상 접근법)

주최: Stanford HAI Digital Economy Lab · STAIR · UN BSG · UNICEF · UNHCR · World Bank. 컴퓨트 스폰서 Modal. 리드: Andreas Haupt (Stanford HAI).

## 6. 전략 메모 (개인 컨텍스트)

- **왜 이 대회인가**: 서베이 행렬 완성 = 산재 논문(서베이 데이터 방법론) 스킬 직결. NeurIPS 공저 = core ML PhD 내러티브에 최고 레버리지. 컴퓨트 10분 제약 = 대형 랩 대비 개인 불리함 없음.
- **깊이 1 + 넓이 3 원칙의 "넓이" 슬롯.** TMLR 재현 연구(9/30 마감)가 깊이 메인 — 9월 말 시간 배분 주의.
- log-loss 특성상 **캘리브레이션 좋은 단순 모델이 과적합된 복잡 모델을 이김.** IRT + 저랭크 + 스무딩 조합부터. LLM 기반 시뮬레이션(페르소나 프롬프팅)은 캘리브레이션 후처리 없이는 log-loss에서 불리 — 하이브리드 각도가 차별화 포인트.
- skip-logic 레벨 처리를 정확히 하는 것만으로 베이스라인 대비 공짜 점수 가능성.
- 하루 1회 제출 = 로컬 검증 셋 구축이 필수. 공개 샤드 10%가 매일 바뀌므로 리더보드 과적합 위험 낮지만 제출 낭비 금물.
- 개발 10분 vs 테스트 100분: 최종 제출은 10배 예산 — 개발 중엔 10분에 맞춘 경량 버전, 테스트용 확장 버전 별도 유지.

## 7. 초기 액션 체크리스트

- [ ] 8/10 등록 폼 제출 (팀명·구성 결정 — 개인 참가 가능)
- [ ] 스타터 킷 클론 + 합성 샌드박스에서 제출 파이프라인 end-to-end 확인
- [ ] 스키마 정독 — 문항 유형별 인코딩 + skip-logic 레벨 처리 설계
- [ ] 베이스라인 4종 로컬 재현 + 로컬 홀드아웃 log-loss 기준선 기록
- [ ] Docker 제출 템플릿 확정 (10분 wall-clock 프로파일링 포함)
- [ ] 첫 리더보드 제출 (marginal이라도 — 파이프라인 검증 목적)
- [ ] method description 4p 템플릿 초안
- [ ] 외부 가중치 쓸 계획이면 커밋 해시 목록 미리 관리

## 8. 권장 폴더 구조

```
simulacrabench/
├── README.md               ← 이 파일
├── data/                   # 스키마·합성 샌드박스 (실데이터는 폐쇄 환경에만 존재)
├── notebooks/              # EDA, 문항 유형 분석
├── src/
│   ├── preprocess/         # 인코딩, skip-logic 처리
│   ├── models/             # irt / lowrank / diffusion / hybrid
│   └── eval/               # 로컬 log-loss 하네스 (공식 지표 재현)
├── submissions/            # 날짜별 제출 스냅샷 + 리더보드 점수 로그
├── docker/                 # 제출 이미지 정의
└── docs/
    ├── method-4p.md        # 제출용 method description
    └── log.md              # 일일 실험 로그
```

## 9. 리스크·주의

- 데이터가 폐쇄 환경에만 있음 — **로컬에서는 합성 샌드박스 + 공개 샤드 통계로만 개발.** 실데이터 가정 하드코딩 금지.
- 11/1–14 테스트 페이즈가 SimulacraBench 최종 + Steerability 등록 마감(11/15)과 겹침 — 11월 초 일정 비워둘 것.
- 백업 플랜: 이 대회 무산 시 FAIR Universe (~10/11) 또는 Steerability.
