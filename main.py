import os
import math
import random
import string
from datetime import datetime
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import uvicorn

app = FastAPI()

# ✅ Fix lỗi "Invalid Host header" khi deploy Render
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

mcp = FastMCP("demo-tools")

# ─────────────────────────────────────────
# 🔢 MATH
# ─────────────────────────────────────────

@mcp.tool()
def sum_numbers(a: float, b: float) -> float:
    """Tính tổng hai số"""
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Tính hiệu hai số"""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Nhân hai số"""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Chia hai số"""
    if b == 0:
        raise ValueError("Không thể chia cho 0")
    return a / b

@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Tính lũy thừa"""
    return base ** exponent

@mcp.tool()
def square_root(n: float) -> float:
    """Tính căn bậc hai"""
    if n < 0:
        raise ValueError("Không thể tính căn bậc hai của số âm")
    return math.sqrt(n)

@mcp.tool()
def percentage(value: float, total: float) -> float:
    """Tính phần trăm"""
    if total == 0:
        raise ValueError("Total không được bằng 0")
    return round((value / total) * 100, 2)

@mcp.tool()
def bmi_calculator(weight_kg: float, height_m: float) -> dict:
    """Tính BMI và phân loại sức khỏe"""
    bmi = round(weight_kg / (height_m ** 2), 2)
    if bmi < 18.5:
        category = "Thiếu cân"
    elif bmi < 25:
        category = "Bình thường"
    elif bmi < 30:
        category = "Thừa cân"
    else:
        category = "Béo phì"
    return {"bmi": bmi, "category": category}

# ─────────────────────────────────────────
# 📅 DATE & TIME
# ─────────────────────────────────────────

@mcp.tool()
def get_current_datetime() -> dict:
    """Lấy ngày giờ hiện tại"""
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
        "timestamp": int(now.timestamp())
    }

@mcp.tool()
def days_between_dates(date1: str, date2: str) -> int:
    """Tính số ngày giữa 2 ngày. Format: YYYY-MM-DD"""
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    return abs((d2 - d1).days)

@mcp.tool()
def age_calculator(birthdate: str) -> dict:
    """Tính tuổi từ ngày sinh. Format: YYYY-MM-DD"""
    birth = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return {"age": age, "birthdate": birthdate}

# ─────────────────────────────────────────
# 📝 STRING
# ─────────────────────────────────────────

@mcp.tool()
def word_count(text: str) -> dict:
    """Đếm số từ, ký tự, câu trong đoạn văn"""
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?')
    return {
        "characters": len(text),
        "characters_no_space": len(text.replace(" ", "")),
        "words": len(words),
        "sentences": sentences
    }

@mcp.tool()
def reverse_text(text: str) -> str:
    """Đảo ngược chuỗi văn bản"""
    return text[::-1]

@mcp.tool()
def to_uppercase(text: str) -> str:
    """Chuyển văn bản thành chữ HOA"""
    return text.upper()

@mcp.tool()
def to_lowercase(text: str) -> str:
    """Chuyển văn bản thành chữ thường"""
    return text.lower()

@mcp.tool()
def generate_random_password(length: int = 16) -> str:
    """Tạo mật khẩu ngẫu nhiên"""
    if length < 4:
        raise ValueError("Độ dài tối thiểu là 4")
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

# ─────────────────────────────────────────
# 💰 FINANCE
# ─────────────────────────────────────────

@mcp.tool()
def compound_interest(principal: float, rate: float, years: int, n: int = 12) -> dict:
    """Tính lãi kép. rate là lãi suất năm (0.07 = 7%)"""
    amount = principal * (1 + rate / n) ** (n * years)
    interest = amount - principal
    return {
        "principal": round(principal, 2),
        "final_amount": round(amount, 2),
        "interest_earned": round(interest, 2),
        "years": years
    }

@mcp.tool()
def currency_converter(amount: float, from_currency: str, to_currency: str) -> dict:
    """Chuyển đổi tiền tệ. Hỗ trợ: USD, VND, EUR, JPY, GBP"""
    rates_to_usd = {
        "USD": 1.0, "VND": 25000.0,
        "EUR": 0.92, "JPY": 149.5, "GBP": 0.79
    }
    from_c = from_currency.upper()
    to_c = to_currency.upper()
    if from_c not in rates_to_usd or to_c not in rates_to_usd:
        raise ValueError(f"Không hỗ trợ: {from_currency} hoặc {to_currency}")
    result = (amount / rates_to_usd[from_c]) * rates_to_usd[to_c]
    return {"from": f"{amount} {from_c}", "to": f"{round(result, 2)} {to_c}"}

# ─────────────────────────────────────────
# 🎲 UTILITY
# ─────────────────────────────────────────

@mcp.tool()
def roll_dice(sides: int = 6) -> int:
    """Tung xúc xắc"""
    return random.randint(1, sides)

@mcp.tool()
def random_number(min_val: int, max_val: int) -> int:
    """Tạo số ngẫu nhiên trong khoảng min đến max"""
    return random.randint(min_val, max_val)

@mcp.tool()
def unit_converter(value: float, from_unit: str, to_unit: str) -> dict:
    """Chuyển đổi đơn vị: km/miles, kg/lbs, celsius/fahrenheit"""
    conversions = {
        ("km", "miles"): lambda x: x * 0.621371,
        ("miles", "km"): lambda x: x * 1.60934,
        ("kg", "lbs"): lambda x: x * 2.20462,
        ("lbs", "kg"): lambda x: x / 2.20462,
        ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key not in conversions:
        raise ValueError(f"Không hỗ trợ: {from_unit} → {to_unit}")
    result = conversions[key](value)
    return {"from": f"{value} {from_unit}", "to": f"{round(result, 4)} {to_unit}"}

# ─────────────────────────────────────────
# 🚀 APP
# ─────────────────────────────────────────

app.mount("/mcp", mcp.sse_app())

@app.get("/")
def root():
    return {"status": "running", "total_tools": 21}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8999))
    uvicorn.run(app, host="0.0.0.0", port=port)