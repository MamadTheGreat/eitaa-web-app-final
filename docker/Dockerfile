# استفاده از Python 3.11 slim برای کم‌کردن حجم
FROM python:3.11-slim

# تنظیم working directory
WORKDIR /app

# کپی فایل requirements
COPY requirements.txt .

# نصب dependencies
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# تنظیم environment variable برای Python
ENV PYTHONUNBUFFERED=1

# Expose کردن پورت
EXPOSE 80

# دستور اجرای اپلیکیشن
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
