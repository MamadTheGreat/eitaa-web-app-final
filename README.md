# 🏥 سامانه آموزش و پیگیری سلامت - Modular Version 3.0

یک وب‌اپلیکیشن فارسی برای آموزش بیماران و پیگیری علائم سلامتی با معماری Modular و استفاده از React و FastAPI.

## 📋 فهرست مطالب

- [ویژگی‌ها](#-ویژگی‌ها)
- [معماری پروژه](#-معماری-پروژه)
- [تکنولوژی‌ها](#-تکنولوژی‌ها)
- [نصب و راه‌اندازی](#-نصب-و-راه‌اندازی)
- [ساختار پروژه](#-ساختار-پروژه)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [تغییرات نسبت به نسخه قبل](#-تغییرات-نسبت-به-نسخه-قبل)

## ✨ ویژگی‌ها

### 📚 آموزش بیمار
- دسترسی به ویدیوهای آموزشی برای بیماری‌های مختلف
- پشتیبانی از فایل‌های PDF
- Cache برای بهبود عملکرد

### 📊 ثبت علائم
- ثبت و پیگیری قند خون (ناشتا و بعد از غذا)
- ثبت و پیگیری فشار خون
- ثبت و پیگیری وزن
- Validation کامل در Frontend و Backend

### 📈 تاریخچه
- مشاهده تاریخچه علائم ثبت شده
- تاریخ شمسی و ساعت ایران

### 💬 پشتیبانی
- ارتباط با کارشناسان از طریق ایتا
- اطلاعات تماس کامل

### 🔒 امنیت
- Validation کامل داده‌ها
- Rate Limiting
- CORS محدود شده
- Logging کامل

## 🏗 معماری پروژه

این نسخه با معماری **Modular** طراحی شده است:

### Backend (FastAPI)
```
backend/
├── main.py                 # Entry point و setup
├── config.py              # تنظیمات centralized
├── models.py              # Pydantic models
├── services/              # Business logic
│   ├── google_drive.py   # سرویس Google Drive
│   ├── google_sheets.py  # سرویس Google Sheets
│   └── cache.py          # Cache management
├── routers/               # API endpoints
│   ├── education.py      # Endpoints آموزش
│   ├── symptoms.py       # Endpoints علائم
│   └── contact.py        # Endpoints تماس
├── middleware/            # Middleware components
│   └── rate_limit.py     # Rate limiting
└── utils/                 # Utility functions
    ├── validators.py     # Validation logic
    └── logger.py         # Logging setup
```

### Frontend (React)
```
frontend/
├── index.html             # Main HTML template
├── js/
│   ├── app.js            # Main app component
│   ├── config.js         # Configuration
│   ├── components/       # React components
│   │   ├── HomePage.js
│   │   ├── EducationPage.js
│   │   ├── SymptomsPage.js
│   │   └── ContactPage.js
│   └── utils/            # Utility functions
│       ├── api.js        # API calls
│       ├── validators.js # Frontend validation
│       └── icons.js      # SVG icons
└── css/
    └── styles.css        # Custom styles
```

## 🛠 تکنولوژی‌ها

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Google Drive API** - ذخیره ویدیوها
- **Google Sheets API** - ذخیره داده‌های کاربر
- **jdatetime** - تاریخ شمسی
- **uvicorn/gunicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Tailwind CSS** - Styling
- **Vazirmatn Font** - فونت فارسی

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **pytest** - Testing

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- حساب Google Cloud با:
  - Google Drive API فعال
  - Google Sheets API فعال
  - Service Account ایجاد شده

### 1. کلون کردن پروژه

```bash
git clone https://github.com/MamadTheGreat/Web-app-eitaa.git
cd Web-app-eitaa
```

### 2. نصب Backend

```bash
# ایجاد virtual environment
python -m venv venv

# فعال‌سازی virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# نصب dependencies
pip install -r requirements.txt
```

### 3. تنظیم Environment Variables

```bash
# کپی فایل .env.example
cp .env.example .env

# ویرایش .env و اضافه کردن اطلاعات خود
nano .env
```

### 4. اجرای Backend

```bash
# Development mode
python backend/main.py

# یا با uvicorn
uvicorn backend.main:app --reload

# Production mode
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 5. اجرای Frontend

Frontend یک فایل HTML ساده است که می‌توانید با هر web server اجرا کنید:

```bash
# با Python
cd frontend
python -m http.server 3000

# یا با Node.js
npx serve
```

## 📁 ساختار کامل پروژه

```
web-app-eitaa/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── google_drive.py
│   │   ├── google_sheets.py
│   │   └── cache.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── education.py
│   │   ├── symptoms.py
│   │   └── contact.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── rate_limit.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── logger.py
├── frontend/
│   ├── index.html
│   ├── js/
│   │   ├── config.js
│   │   ├── components/
│   │   │   ├── HomePage.js
│   │   │   ├── EducationPage.js
│   │   │   ├── SymptomsPage.js
│   │   │   └── ContactPage.js
│   │   └── utils/
│   │       ├── api.js
│   │       ├── validators.js
│   │       └── icons.js
│   └── css/
│       └── styles.css
├── tests/
│   ├── test_backend.py
│   └── test_validators.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       └── deploy.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 📚 API Documentation

### Health Check
```
GET /
GET /api/health
```

### Education Endpoints
```
GET /api/videos/{disease}
GET /api/diseases
```

### Symptoms Endpoints
```
POST /api/symptoms
POST /api/symptoms/history
GET /api/symptoms/types
```

### Contact Endpoints
```
GET /api/contact
GET /api/support
```

### Example Requests

#### Save Symptom
```bash
curl -X POST "http://localhost:8000/api/symptoms" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123456",
    "symptom_type": "قند ناشتا",
    "value": "120"
  }'
```

#### Get History
```bash
curl -X POST "http://localhost:8000/api/symptoms/history" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123456",
    "symptom_filter": null
  }'
```

## 🧪 Testing

### اجرای تست‌ها

```bash
# اجرای تمام تست‌ها
pytest tests/ -v

# اجرای تست‌های خاص
pytest tests/test_backend.py -v
pytest tests/test_validators.py -v

# Coverage report
pytest tests/ --cov=backend --cov-report=html
```

### نوشتن تست جدید

```python
# tests/test_new_feature.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_new_feature():
    response = client.get("/api/new-endpoint")
    assert response.status_code == 200
```

## 🐳 Docker Deployment

### Build & Run با Docker

```bash
# Build image
docker build -f docker/Dockerfile -t patient-education-api .

# Run container
docker run -p 8000:8000 \
  -e GOOGLE_CREDENTIALS_JSON='...' \
  -e MAIN_FOLDER_ID='...' \
  -e GOOGLE_SHEET_ID='...' \
  patient-education-api
```

### استفاده از Docker Compose

```bash
# Start services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

## 🚀 Deployment

### Render.com (Backend)

1. در Render.com یک Web Service جدید بسازید
2. Repository GitHub را متصل کنید
3. Environment Variables را تنظیم کنید
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Netlify (Frontend)

1. فولدر `frontend` را به Netlify deploy کنید
2. یا از GitHub Pages استفاده کنید

### Environment Variables for Render

```
GOOGLE_CREDENTIALS_JSON=...
MAIN_FOLDER_ID=...
GOOGLE_SHEET_ID=...
ALLOWED_ORIGINS=https://your-frontend.netlify.app
MAX_REQUESTS_PER_MINUTE=60
LOG_LEVEL=INFO
```

## 🔄 تغییرات نسبت به نسخه قبل

### ✅ بهبودها

#### Backend:
- ✅ **Modular Architecture**: کد به ماژول‌های مستقل تقسیم شد
- ✅ **Separation of Concerns**: هر بخش مسئولیت خاص خود را دارد
- ✅ **Services Layer**: Business logic جدا از routing
- ✅ **Configuration Management**: تنظیمات centralized
- ✅ **Better Error Handling**: مدیریت خطای بهتر
- ✅ **Logging System**: سیستم logging کامل
- ✅ **Testing Framework**: تست‌های جامع

#### Frontend:
- ✅ **Component-Based**: Component های جداگانه
- ✅ **Configuration File**: تنظیمات centralized
- ✅ **API Abstraction**: API calls جدا از components
- ✅ **Reusable Utilities**: توابع کمکی قابل استفاده مجدد

#### DevOps:
- ✅ **Docker Support**: Containerization کامل
- ✅ **CI/CD Pipeline**: GitHub Actions
- ✅ **Automated Testing**: تست خودکار در CI

### 🆕 ویژگی‌های جدید

- API endpoints جدید (`/api/diseases`, `/api/symptoms/types`)
- Health check بهبود یافته
- Cache management بهتر
- Rate limiting پیشرفته‌تر

## 📝 License

این پروژه تحت لایسنس MIT منتشر شده است.

## 📞 پشتیبانی

- **ایتا**: [کانال پشتیبانی](https://eitaa.com/joinchat/6055926614C5ed07fc3f6)
- **GitHub Issues**: [مشکلات و پیشنهادات](https://github.com/MamadTheGreat/Web-app-eitaa/issues)

## 🙏 تشکر

از تیم‌های FastAPI، React و Google Cloud برای ابزارهای عالی

---

**نکته مهم**: این پروژه برای استفاده آموزشی طراحی شده است. برای استفاده بالینی واقعی، باید مجوزهای پزشکی لازم اخذ شود.
