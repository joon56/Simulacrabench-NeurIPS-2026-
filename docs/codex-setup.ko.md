# Codex / Windows 작업 안내

2026-09-27 전환 점검. 이 문서는 환경 안내이며 연구 실행 허가가 아니다.
현재 판단은 [status](status.md), 역할·평가 경계는 [workflow](workflow.md),
구체적 허용 작업은 사용자의 현재 지시와 해당 인계문을 따른다.

## 새 세션과 기존 세션

1. 프로젝트 루트 `C:\Users\USER\Desktop\SimulacraBench`를 작업 폴더로 연다.
2. [AGENTS.md](../AGENTS.md)가 Codex 진입점이다. `CLAUDE.md`, status,
   log 최신 3개, workflow, 현재 인계문 순서로 읽는다.
3. 실제 읽은 개정·역할·허용 작업·종료 조건을 보고한다. HEAD뿐 아니라
   현재 dirty files와 해당 작업 manifest를 확인한다.
4. 기존 채팅은 바뀐 지침을 명시적으로 다시 읽는다. 파일 존재나 점검 PASS로
   모든 채팅의 로딩·준수를 확인했다고 보고하지 않는다.

공용 규칙을 Codex 전용 파일에 복제하지 않는다. `CLAUDE.md` 파일명은
유지하며 AGENTS에서 읽도록 연결했다. 별도 모델·권한·MCP 설정이 필요한
근거가 없어 `.codex/config.toml`, 자동 실행 hook, 전역 설정은 추가하지 않았다.
`.claude/settings.local.json`은 해당 도구의 개인 설정이며 Codex 권한이 아니다.

## 논문 세션 스킬

Codex 진입: [.agents/skills/paper-session/SKILL.md](../.agents/skills/paper-session/SKILL.md).
공유 본문: [.claude/skills/paper-session/SKILL.md](../.claude/skills/paper-session/SKILL.md).
사용 예: `$paper-session`과 논문명 또는 학습 가이드 번호를 지정한다.
스킬 목록에 안 보이면 새 세션에서 확인하거나 이 경로를 직접 읽게 한다.
본문을 두 벌로 복제하지 않으므로 Claude의 기존 학습 방식도 함께 유지된다.

공식 문서상 Codex는 저장소 `.agents/skills`를 검색하며 변경 감지를 지원한다.
이 체크아웃의 새 세션에서 실제 선택·본문 로딩되는지는 아직 독립 검증하지
않았다. [공식 스킬 문서](https://learn.chatgpt.com/docs/build-skills).
[AGENTS 검색 규칙](https://learn.chatgpt.com/docs/agent-configuration/agents-md)도 참고한다.

## 환경 확인

PowerShell에서 UTF-8을 명시하고, 활성화 스크립트 대신 인터프리터를 직접 쓴다.
아래 점검은 설치·학습·평가 없이 운영 문서와 패키지 메타데이터만 읽는다.

```powershell
Get-Content -LiteralPath AGENTS.md -Encoding UTF8
& .\.venv\Scripts\python.exe -B scripts/check_workspace.py
git -c safe.directory=C:/Users/USER/Desktop/SimulacraBench --no-optional-locks status --short
Get-Process -Name python,pythonw,pytest,uv,wsl,bash -ErrorAction SilentlyContinue
```

`check_workspace.py`는 고정 운영 파일의 존재·SHA256, 진입 연결, workflow와
템플릿 개정 일치, Markdown 파일 링크, 스킬 진입, 패키지 버전을 JSON으로
출력한다. 파일을 쓰지 않으며 링크 대상은 존재만 확인한다. 문서 오류는
종료 코드 1, 문서 연결 정상은 0이다. 누락 패키지는 경고로 분리한다.
문서 PASS는 모델 실행·ABI 호환·제출 적합성·실제 지침 준수를 뜻하지 않는다.

현재 `.venv`는 Python 3.13.14의 절대 경로를 참조한다. A029에서 기본 sandbox는
해당 Python 경로 접근에 실패했지만, 허용된 읽기 전용 실행에서는 정상 동작했다.
같은 증상이면 설치 손상으로 단정하거나 가상환경을 삭제하지 않는다. 경로와
권한을 확인하고, 필요한 명령만 승인 절차를 거친다. 이 안내가 sandbox 우회나
전역 `safe.directory=*` 설정을 허용하지 않는다.

한국어 파일을 기본 인코딩으로 읽는 외부 Python 도구는 `-X utf8`을 사용한다.
예: `python -X utf8 -B ...`. 스킬 validator는 기본 cp949에서 실패했고,
이 옵션으로 두 SKILL.md 검증이 통과했다. 전역 로캘은 바꾸지 않았다.

## 의존성 범위

| 파일/구성 | 용도 |
| --- | --- |
| [requirements.txt](../requirements.txt) | 기존 기본 harness/test 의존성 |
| [requirements-models.txt](../requirements-models.txt) | 기본 목록 + SciPy, scikit-learn, threadpoolctl, PyTorch |
| E049 당시 환경·등록 | TabPFN의 별도 버전·라이선스·가중치 조건; 일반 설치에 섞지 않음 |
| 문서 렌더링 당시 환경 | reportlab 등 부가 도구; 문서 작성만으로 설치하지 않음 |

설치가 필요한 새 환경에서만 해당 범위를 선택한다. 기존 `.venv`는 이번에
재생성·설치·업그레이드하지 않았다. CPU/CUDA PyTorch 선택은 실행 환경에 맞춘다.
목록은 완전한 lockfile이 아니다. 재현은 해당 실험의 버전·manifest가 기준이다.
현재 메타데이터는 [A029 점검 결과](analysis/A029-outputs/workspace-check.json)에
기록했다. 이 목록을 제출 ZIP의 `requirements.txt`로 복사하지 않는다.

## 폴더별 사용법

| 위치 | 목적과 주의점 |
| --- | --- |
| `.agents/`, `.claude/` | Codex 진입 스킬 / 공유 논문 스킬·Claude 개인 설정 |
| `docs/` | 현재 운영 지침·상태·로그·도메인 학습 자료 |
| `docs/analysis/`, `docs/experiments/` | A/E 기록·노출 이력·등록과 결과; 과거 판정 보존 |
| `src/`, `scripts/`, `tests/` | 생산 코드·연구 실행기·테스트; 읽기와 실행을 구분 |
| `external/` | 공식 kit, 외부 자료와 연구 캐시; gitignored, 자동 재다운로드 금지 |
| `data/` | 로컬 데이터 자산 위치; 경로 존재는 응답 접근 권한이 아님 |
| `submissions/` | 동결 source·scorecard·ZIP; 기존 snapshot 수정 금지 |
| `output/` | 기존 렌더링·준비 산출물; 현재 권장 제출 위치는 submissions |
| `notebooks/` | 분석 소스; 노트북/스크립트 실행도 연구 범위 확인 |
| `docker/` | 현재 빈 예약 폴더; 필요 없는 Docker 설정을 만들어 넣지 않음 |
| `.venv/`, `tmp/`, `__pycache__/`, `.pytest_cache/` | 환경·임시 파일; 일괄 삭제/모델 캐시 읽기 금지 |
| `trip/` | 별도 사용자 자료; 전환 작업은 경로 조사만, 내용·구조 보존 |
| `.git/` | 저장소 관리 정보; 내부 객체 수집/설정 수정 없이 Git 조회 사용 |

이 표는 사용 안내다. 보호된 `docs/tree.md`를 재생성하지 않았다.

## 명령 이름만 보고 실행하지 않기

`scripts/check_e060.py`는 기존 Parquet 해시·캐시 역직렬화·학습·평가를 포함한다.
`src/eval/runner.py`는 sandbox 생성과 점수 계산을 할 수 있다. `pytest` 전체
실행도 모델 테스트를 수집한다. 이런 명령을 환경 확인 용도로 실행하지 않는다.
새 운영 도구 자체를 고칠 때 필요한 최소 검증은 다음과 같다.

```powershell
& .\.venv\Scripts\python.exe -B tests/test_workspace_check.py
```

이 테스트는 새 임시 문서만 쓴다. 성공한 연구 fixture나 이전 실험 재실행을
포함하지 않는다. 새 과학적 작업은 기존 역할·노출·STOP/HOLD를 승계한 별도
범위로 시작한다. 현 상태에서는 E041 incumbent/E025 fallback, E057/E060 parked,
S3 중단과 사용자 미확정 TEST 선택을 유지한다.

전체 조사 범위·보완 내역·미확인 사항: [A029](analysis/A029-codex-migration-audit.md).
