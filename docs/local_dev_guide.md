# 로컬 웹 개발/테스트 가이드

이 문서는 TARE 프로젝트에서 프론트엔드(UI)와 연관된 백엔드(GraphQL API)를 로컬 환경에서 실행하고 테스트하는 방법을 안내합니다. 프로젝트에 익숙하지 않은 웹 개발자를 대상으로 하며, 기본 환경 세팅부터 테스트 실행까지 단계별로 설명합니다.

## 1. 필수 도구 준비

다음 도구가 설치되어 있어야 합니다.

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) 18 이상과 `npm`
- [Python](https://www.python.org/) 3.12 이상
- [uv](https://github.com/astral-sh/uv) — Python 패키지/런타임 매니저 (`pipx install uv` 권장)

## 2. 저장소 가져오기

```bash
git clone https://github.com/USER/tare.git
cd tare
```

## 3. 백엔드(GraphQL API) 실행

1. 의존성 설치:
   ```bash
   uv sync --package tare-graphql
   ```
2. 개발 서버 실행:
   ```bash
   uv run --package tare-graphql uvicorn tare_graphql.main:app --reload
   ```
   기본적으로 `http://localhost:8000/graphql` 에서 GraphQL API가 제공됩니다.
3. 백엔드 테스트 실행 (선택):
   ```bash
   uv run --package tare-graphql pytest python_modules/tare-graphql/tests -q
   ```

## 4. 프론트엔드(UI) 실행

1. 의존성 설치:
   ```bash
   npm install --prefix js_modules/tare-ui
   ```
2. 개발 서버 실행:
   ```bash
   npm run dev --prefix js_modules/tare-ui
   ```
   기본적으로 `http://localhost:5173` 에서 UI가 동작합니다. UI는 동일 출처의 `/graphql` 엔드포인트로 요청을 보냅니다. Vite 개발 서버는 `/graphql` 요청을 `http://localhost:8000/graphql` 로 프록시하도록 구성되어 있으므로, 앞서 백엔드 서버가 실행 중이어야 합니다.
3. 프론트엔드 테스트 실행 (현재는 템플릿만 존재):
   ```bash
   npm test --prefix js_modules/tare-ui
   ```

## 5. 전체 개발 흐름

1. **터미널 1**에서 백엔드 서버를 실행합니다.
2. **터미널 2**에서 프론트엔드 서버를 실행합니다.
3. 브라우저에서 `http://localhost:5173` 에 접속하여 UI가 백엔드와 정상적으로 통신하는지 확인합니다.

## 6. 문제 해결 팁

- 포트 충돌이 발생하면 `uvicorn`의 `--port` 옵션 또는 Vite의 `--port` 옵션으로 포트를 조정하세요.
- 네트워크 요청이 실패한다면 백엔드 서버가 실행 중인지와 `/graphql` 경로로의 프록시 설정을 확인하세요.
- 의존성 설치가 실패하면 Node.js 및 Python 버전이 요구 사항을 만족하는지 점검하세요.

이 가이드에 따라 로컬 환경에서 프론트엔드와 백엔드를 손쉽게 실행하고 테스트할 수 있습니다.
