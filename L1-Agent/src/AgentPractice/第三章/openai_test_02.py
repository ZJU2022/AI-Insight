from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import config

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="3D动漫古风美女，身穿汉服，手拿扇子，站在樱花树下,身材玲珑有致，妩媚动人",
    n=1,
    size="1024x1024",
    quality="standard"
)

image_url = response.data[0].url
print(f"生成的图片URL: {image_url}")

# 如果你想下载图片，可以使用以下代码
import requests
response = requests.get(image_url)
if response.status_code == 200:
    with open("generated_image.png", "wb") as f:
        f.write(response.content)
    print("图片已保存为 generated_image.png")