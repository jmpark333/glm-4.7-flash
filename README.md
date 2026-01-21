# GLM-4.7-Flash API Examples

Z.AI (Zhipu AI) GLM-4.7-Flash 모델을 사용하는 다양한 Python 예제 모음입니다.

## 프로젝트 개요

이 프로젝트는 Z.AI의 GLM-4.7-Flash 모델을 사용하는 방법을 보여주는 예제 코드입니다. 주로 공식 Python SDK (`zai-sdk`)를 사용하며, OpenAI SDK 호환 방식도 지원합니다.

## 설치

```bash
# 가상환경 생성 (선택사항)
python -m venv myenv
source myenv/bin/activate

# 공식 SDK 설치
pip install zai-sdk

# 또는 OpenAI SDK 호환 (대안)
pip install openai>=1.0

# 환경 변수 설정
echo "ZHIPU_API_KEY=your_api_key_here" > .env
```

API Key 발급: https://open.bigmodel.cn/

## 사용 예제

### 1. 기본 사용 (app1.py)

```bash
python app1.py
```

### 2. 간단한 테스트 (test.py)

```bash
python test.py
```

## 예제 기능

app1.py에서 제공하는 예제:

- **기본 사용**: 기본적인 채팅 완료 요청
- **스트리밍 응답**: 실시간 응답 수신
- **멀티턴 대화**: 대화 맥락 유지
- **JSON 출력 모드**: 구조화된 JSON 응답
- **함수 호출 (Function Calling)**: 사용자 정의 함수 실행
- **Thinking 모드**: 추론 과정 표시
- **시스템 프롬프트**: 다양한 시스템 설정
- **온도 제어**: 창의성 vs 정확성 조절
- **OpenAI SDK 호환**: OpenAI SDK로 GLM-4.7-Flash 사용

## 파일 구조

```
.
├── app1.py          # 종합 예제 (모든 기능 포함)
├── test.py          # 간단한 테스트 코드
├── .env.example     # 환경 변수 예시
└── README.md        # 프로젝트 문서
```

## 공식 문서

- Z.AI API 문서: https://docs.z.ai/api-reference/introduction
- SDK 설치 확인: `python -c "import zai; print(zai.__version__)"`

## 라이선스

MIT License
