from zai import ZaiClient

# API 클라이언트 초기화
client = ZaiClient(api_key="6e74659313a8456da1b4881d29dc098f.SgJrKDIG5qoTW9YO")

# GLM-4.7-Flash 모델 호출
response = client.chat.completions.create(
    model="glm-4.7-flash",
    messages=[
        {"role": "system", "content": "당신은 친절한 AI 도우미입니다."},
        {"role": "user", "content": "한국으로 여행갈 때 추천할 만한 계절과 활동을 알려주세요."}
    ]
)

# 응답 출력
print(response.choices[0].message.content)