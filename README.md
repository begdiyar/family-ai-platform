# Oila AI

Платформа поддержки семей для хакимиятов — помогает парам улучшать отношения через AI-консультации, диагностику и практики.

## Стек

- **Backend:** Django 5 + Django REST Framework + PostgreSQL + Celery + Redis
- **Frontend:** React 18 + TypeScript + Vite + Tailwind CSS
- **AI:** OpenAI API (GPT)
- **Хранилище:** MinIO (S3-совместимое)
- **Деплой:** Docker Compose + Nginx + Gunicorn

## Быстрый старт (локальная разработка)

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd diplom-work
```

### 2. Настроить переменные окружения

```bash
cp backend/.env.example.txt backend/.env
```

Заполнить `backend/.env`:

| Переменная | Описание |
|-----------|----------|
| `SECRET_KEY` | Секретный ключ Django. Сгенерировать: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `OPENAI_API_KEY` | Ключ OpenAI API |
| `DATABASE_URL` | URL PostgreSQL (по умолчанию работает с docker-compose) |
| `REDIS_URL` | URL Redis (по умолчанию работает с docker-compose) |

### 3. Запустить через Docker Compose

```bash
docker compose up -d
```

Сервисы:
- Backend API: http://localhost:8001
- MinIO Console: http://localhost:9001
- PostgreSQL: localhost:5433

### 4. Запустить фронтенд

```bash
cd frontend
npm install
npm run dev
```

Приложение: http://localhost:5173

## Деплой на продакшн (VPS)

### Подготовка сервера

```bash
# Установить Docker
curl -fsSL https://get.docker.com | sh

# Клонировать проект
git clone <repo-url> /opt/oila-ai
cd /opt/oila-ai
```

### Настроить окружение

```bash
cp backend/.env.example.txt backend/.env
# Заполнить backend/.env реальными значениями:
# - DEBUG=False
# - SECRET_KEY=<сгенерированный ключ>
# - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# - OPENAI_API_KEY=<ключ>
# - EMAIL_* настройки
```

### Собрать фронтенд

```bash
cd frontend
npm install
npm run build
# dist/ папка появится в frontend/dist/
```

### Запустить

```bash
docker compose up -d
```

## Архитектура

```
Nginx (80/443)
├── / → frontend/dist/ (статические файлы React)
└── /api/v1/ → Django (Gunicorn, порт 8000)
                ├── PostgreSQL
                ├── Redis → Celery workers
                └── MinIO (медиафайлы)
```

## Модули

| Модуль | Описание |
|--------|----------|
| `users` | Регистрация, аутентификация, профиль |
| `couples` | Создание пары, приглашения |
| `diagnostics` | Тесты и диагностика отношений |
| `ai_consultant` | AI-чат, коуч, медиатор |
| `practices` | Ежедневные практики для пар |
| `analytics` | Аналитика и индексы отношений |
| `reports` | PDF-отчёты (генерируются через Celery) |
| `mediation` | Сессии медиации |
| `constitution` | Семейная конституция |
| `academy` | Статьи и обучающие материалы |
| `admin_panel` | Панель администратора хакимията |

## API

После запуска документация доступна на: `http://localhost:8001/api/v1/`

Аутентификация: JWT Bearer Token.

```
POST /api/v1/auth/register/    — регистрация
POST /api/v1/auth/login/       — вход
POST /api/v1/auth/refresh/     — обновить токен
```
