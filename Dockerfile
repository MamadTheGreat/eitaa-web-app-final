# استفاده از Python 3.11
FROM python:3.11-slim

# تنظیم working directory
WORKDIR /app

# کپی و نصب dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# تنظیمات Python
ENV PYTHONUNBUFFERED=1

# پورت 80 برای ابرآروان
EXPOSE 80

# اجرای اپلیکیشن
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
