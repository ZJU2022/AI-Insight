from openai import OpenAI
import config

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "您是一个帮助用户了解鲜花信息的智能助手，并能够输出JSON格式的内容"},
        {"role": "user", "content": "生日送什么花最好?"},
        {"role": "assistant", "content": "玫瑰花是生日礼物的热门选择"},
        {"role": "user", "content": "送货需要多长时间？"},
    ]
)

#打印后换行
print(response)

#只打印相应中的消息内容
print(response.choices[0].message.content)