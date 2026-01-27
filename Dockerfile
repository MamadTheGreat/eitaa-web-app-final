# استفاده از Python 3.11 slim
FROM python:3.11-slim

# تنظیم working directory
WORKDIR /app

# کپی requirements و نصب dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# تنظیمات Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# پورت 80 برای ابرآروان
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:80/api/health')" || exit 1

# اجرای اپلیکیشن
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-80}"]
