"""
Z.AI (Zhipu AI) GLM-4.7-Flash API 사용 예제

이 파일은 Z.AI의 GLM-4.7-Flash 모델을 사용하는 다양한 방법을 보여줍니다.
주로 공식 Python SDK (zai-sdk)를 사용하며, OpenAI SDK 호환 방식도 지원합니다.

공식 문서: https://docs.z.ai/api-reference/introduction
SDK 설치: pip install zai-sdk
"""

import os
import json
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API Key 설정
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

# =============================================================================
# 공식 Python SDK (zai-sdk) 사용법
# =============================================================================
# 설치: pip install zai-sdk
# 검증: python -c "import zai; print(zai.__version__)"
# =============================================================================

def example_basic():
    """기본 사용 예제"""
    from zai import ZaiClient

    # 클라이언트 초기화
    client = ZaiClient(api_key=ZHIPU_API_KEY)

    # 채팅 완료 요청 생성
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {
                "role": "system",
                "content": "당신은 친절한 AI 코딩 도우미입니다."
            },
            {
                "role": "user",
                "content": "Python으로 피보나치 수열을 계산하는 함수를 작성해주세요."
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )

    # 응답 출력
    print("=== 기본 응답 ===")
    print(response.choices[0].message.content)


def example_streaming():
    """스트리밍 응답 예제"""
    from zai import ZaiClient

    client = ZaiClient(api_key=ZHIPU_API_KEY)

    print("=== 스트리밍 응답 ===")

    stream = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {
                "role": "system",
                "content": "당신은 친절한 AI 코딩 도우미입니다."
            },
            {
                "role": "user",
                "content": "FastAPI로 REST API 서버를 구현하는 코드를 작성해주세요."
            }
        ],
        stream=True
    )

    # 실시간 응답 출력
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print()


def example_multi_turn_conversation():
    """멀티턴 대화 예제"""
    from zai import ZaiClient

    client = ZaiClient(api_key=ZHIPU_API_KEY)

    # 대화 기록
    messages = [
        {
            "role": "system",
            "content": "당신은 친절한 AI 코딩 도우미입니다."
        }
    ]

    print("=== 멀티턴 대화 ===")

    # 첫 번째 질문
    messages.append({
        "role": "user",
        "content": "Python에서 리스트 컴프리헨션이란 무엇인가요?"
    })

    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=messages
    )

    assistant_message = response.choices[0].message.content
    print(f"AI: {assistant_message}\n")

    # 대화 기록에 추가
    messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    # 두 번째 질문 (이전 대화 맥락 유지)
    messages.append({
        "role": "user",
        "content": "그럼 예제 코드를 보여주세요."
    })

    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=messages
    )

    assistant_message = response.choices[0].message.content
    print(f"AI: {assistant_message}\n")


def example_json_mode():
    """JSON 출력 모드 예제"""
    from zai import ZaiClient

    client = ZaiClient(api_key=ZHIPU_API_KEY)

    print("=== JSON 출력 모드 ===")

    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {
                "role": "system",
                "content": "당신은 JSON 형식으로만 응답하는 AI 도우미입니다."
            },
            {
                "role": "user",
                "content": "Python, JavaScript, Go 언어의 특징을 각각 설명하고 JSON 형식으로 반환해주세요."
            }
        ],
        response_format={"type": "json_object"}
    )

    print(response.choices[0].message.content)


def example_function_calling():
    """함수 호출 (Function Calling) 예제"""
    from zai import ZaiClient

    client = ZaiClient(api_key=ZHIPU_API_KEY)

    print("=== 함수 호출 (Function Calling) ===")

    # 사용자 정의 함수 정의
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "현재 날씨 정보를 가져옵니다",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "도시 이름 (예: Seoul, Busan)"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_fibonacci",
                "description": "피보나치 수열의 n번째 항을 계산합니다",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "n": {
                            "type": "integer",
                            "description": "구하고자 하는 항의 위치 (1부터 시작)"
                        }
                    },
                    "required": ["n"]
                }
            }
        }
    ]

    # 함수 호출 요청
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {
                "role": "user",
                "content": "피보나치 수열의 10번째 항을 계산해주세요."
            }
        ],
        tools=tools
    )

    # 함수 호출 결과 처리
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        print(f"호출된 함수: {function_name}")
        print(f"함수 인자: {function_args}")

        # 실제 함수 실행
        def calculate_fibonacci(n):
            if n <= 0:
                return 0
            elif n == 1 or n == 2:
                return 1
            else:
                a, b = 1, 1
                for _ in range(3, n + 1):
                    a, b = b, a + b
                return b

        def get_weather(location):
            return f"{location}의 현재 날씨: 맑음, 15°C"

        # 함수 실행
        if function_name == "calculate_fibonacci":
            result = calculate_fibonacci(function_args["n"])
            print(f"계산 결과: 피보나치 수열의 {function_args['n']}번째 항 = {result}")

            # 함수 실행 결과를 AI에게 전달하여 최종 응답 생성
            second_response = client.chat.completions.create(
                model="glm-4.7-flash",
                messages=[
                    {"role": "user", "content": "피보나치 수열의 10번째 항을 계산해주세요."},
                    response.choices[0].message,  # 함수 호출 메시지
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps({"result": result})
                    }
                ]
            )
            print(f"AI 최종 응답: {second_response.choices[0].message.content}")

        elif function_name == "get_weather":
            result = get_weather(function_args["location"])
            print(result)
    else:
        print("함수가 호출되지 않았습니다.")
        print(response.choices[0].message.content)


def example_with_thinking():
    """Thinking 모드 (추론 과정 표시) 예제"""
    from zai import ZaiClient

    client = ZaiClient(api_key=ZHIPU_API_KEY)

    print("=== Thinking 모드 (추론 과정 표시) ===")

    # Thinking 모드로 스트리밍 요청
    stream = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {
                "role": "user",
                "content": "다음 문제를 단계별로 생각해서 풀어주세요: 1~100까지 숫자 중 3의 배수이면서 5의 배수인 숫자의 합을 구하세요."
            }
        ],
        stream=True,
        extra_body={
            "thinking": {
                "type": "enabled"
            }
        }
    )

    reasoning_started = False

    for chunk in stream:
        delta = chunk.choices[0].delta

        # 추론 과정(reasoning_content) 출력
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            if not reasoning_started:
                print("\n[추론 과정]")
                reasoning_started = True
            print(delta.reasoning_content, end="", flush=True)
        # 일반 응답(content) 출력
        elif delta.content is not None:
            if reasoning_started:
                print("\n\n[최종 답변]")
            print(delta.content, end="", flush=True)

    print()


def example_with_system_instructions():
    """시스템 프롬프트 예제 - 다양한 시스템 설정"""
    from zai import ZaiClient

    client = ZaiClient(api_key=ZHIPU_API_KEY)

    print("=== 시스템 프롬프트 예제 ===")

    system_prompts = {
        "coding_assistant": "당신은 전문 코딩 도우미입니다. 코드를 작성할 때 항상 주석과 문서화를 포함하세요.",
        "code_reviewer": "당신은 코드 리뷰어입니다. 코드의 잠재적 버그, 성능 문제, 개선 사항을 찾아내세요.",
        "teacher": "당신은 친절한 선생님입니다. 초보자도 이해할 수 있도록 쉽게 설명하세요."
    }

    # 코딩 도우미 모드
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {
                "role": "system",
                "content": system_prompts["coding_assistant"]
            },
            {
                "role": "user",
                "content": "파이썬으로 파일을 읽고 내용을 처리하는 함수를 작성해주세요."
            }
        ]
    )

    print(f"[코딩 도우미 모드]\n{response.choices[0].message.content}\n")


def example_temperature_control():
    """온도 제어 예제 - 창의성 vs 정확성"""
    from zai import ZaiClient

    client = ZaiClient(api_key=ZHIPU_API_KEY)

    print("=== 온도 제어 예제 ===")

    user_prompt = "인공지능의 미래에 대해 설명해주세요."

    # 낮은 온도 (정확하고 일관된 응답)
    print("\n[낮은 온도 (0.2) - 정확성]")
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.2
    )
    print(response.choices[0].message.content[:200] + "...")

    # 높은 온도 (창의적이고 다양한 응답)
    print("\n[높은 온도 (1.0) - 창의성]")
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[{"role": "user", "content": user_prompt}],
        temperature=1.0
    )
    print(response.choices[0].message.content[:200] + "...")


# =============================================================================
# OpenAI SDK 호환 방식 (대안)
# =============================================================================
# 설치: pip install openai>=1.0
# =============================================================================

def example_openai_sdk():
    """OpenAI SDK 호환 방식 예제"""
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=ZHIPU_API_KEY,
            base_url="https://api.z.ai/api/paas/v4/"
        )

        response = client.chat.completions.create(
            model="glm-4.7-flash",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 친절한 AI 코딩 도우미입니다."
                },
                {
                    "role": "user",
                    "content": "Python으로 피보나치 수열을 계산하는 함수를 작성해주세요."
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        print("=== OpenAI SDK 호환 방식 ===")
        print(response.choices[0].message.content)

    except ImportError:
        print("OpenAI SDK가 설치되지 않았습니다. pip install openai를 실행하세요.")


# =============================================================================
# 메인 실행 함수
# =============================================================================

def main():
    """메인 실행 함수 - 원하는 예제를 선택하여 실행"""

    print("Z.AI GLM-4.7-Flash API 예제 (공식 SDK)")
    print("=" * 60)

    # API Key 확인
    if not ZHIPU_API_KEY:
        print("경고: ZHIPU_API_KEY가 .env 파일에 설정되지 않았습니다.")
        print("https://open.bigmodel.cn/에서 API Key를 발급받으세요.")
        return

    # SDK 설치 확인
    try:
        import zai
        print(f"zai-sdk 버전: {zai.__version__}")
    except ImportError:
        print("경고: 공식 SDK가 설치되지 않았습니다.")
        print("pip install zai-sdk를 실행하세요.")
        return

    print("\n1. 기본 사용 예제")
    print("2. 스트리밍 응답 예제")
    print("3. 멀티턴 대화 예제")
    print("4. JSON 출력 모드 예제")
    print("5. 함수 호출 (Function Calling) 예제")
    print("6. Thinking 모드 (추론 과정 표시) 예제")
    print("7. 시스템 프롬프트 예제")
    print("8. 온도 제어 예제")
    print("9. OpenAI SDK 호환 방식 (대안)")
    print("0. 전체 실행")

    choice = input("\n실행할 예제를 선택하세요 (0-9): ").strip()

    if choice == "1":
        example_basic()
    elif choice == "2":
        example_streaming()
    elif choice == "3":
        example_multi_turn_conversation()
    elif choice == "4":
        example_json_mode()
    elif choice == "5":
        example_function_calling()
    elif choice == "6":
        example_with_thinking()
    elif choice == "7":
        example_with_system_instructions()
    elif choice == "8":
        example_temperature_control()
    elif choice == "9":
        example_openai_sdk()
    elif choice == "0":
        print("\n" + "=" * 60)
        example_basic()
        print("\n" + "=" * 60)
        example_streaming()
        print("\n" + "=" * 60)
        example_multi_turn_conversation()
        print("\n" + "=" * 60)
        example_function_calling()
        print("\n" + "=" * 60)
        example_with_thinking()
    else:
        print("잘못된 선택입니다.")


if __name__ == "__main__":
    main()
