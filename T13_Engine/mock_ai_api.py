from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/ai/analyze")
async def analyze_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    # نمونه پاسخ تستی: پیشنهادات ساده و بازنویسی ساختگی
    suggestions = [
        "کد شما نیاز به مستندسازی بیشتر دارد.",
        "برخی توابع طولانی هستند، تقسیم آن‌ها توصیه می‌شود."
    ]
    rewritten_code = code  # در حالت تست، همان کد را برمی‌گرداند
    return JSONResponse({
        "suggestions": suggestions,
        "rewritten_code": rewritten_code
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
