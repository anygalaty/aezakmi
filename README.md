# AI Notifications Service

AI Notifications Service — это микросервис на базе FastAPI, предназначенный для создания, хранения и анализа уведомлений с использованием внешнего AI API. Проект использует асинхронную обработку с Celery, PostgreSQL в качестве базы данных и Redis для кэширования и очередей.

## Возможности

- Создание уведомлений через REST API
- Автоматическая асинхронная категоризация уведомлений с помощью AI API (info, warning, critical)
- Кэширование популярных запросов (список уведомлений)
- Отметка уведомлений как прочитанных
- Эндпоинт для проверки статуса обработки уведомления
- Поддержка контейнеризации через Docker и Docker Compose
- Простая структура и SOLID-архитектура
- Юнит- и интеграционные тесты

## API

Все эндпоинты находятся под префиксом `/api/v1/notifications`

### `POST /` — Создать уведомление
**Request Body:**
```json
{
  "user_id": "UUID",
  "title": "string",
  "text": "string"
}
```
**Response:** уведомление с полями `id`, `created_at`, `processing_status = "pending"`

### `GET /` — Получить список уведомлений
**Query params:** `skip`, `limit` (по умолчанию 0 и 10) — поддерживается кэширование
**Response:** список уведомлений

### `GET /{id}` — Получить уведомление по ID
**Response:** уведомление

### `POST /{id}/read` — Отметить уведомление как прочитанное
**Response:** уведомление с обновлённым `read_at`

### `GET /{id}/status` — Статус AI-обработки
**Response:** `{ "status": "pending" | "processing" | "completed" | "failed" }`

## Стек
- Python 3.11
- FastAPI
- SQLAlchemy 2 + Alembic
- PostgreSQL
- Redis
- Celery
- Docker & Compose
- Pytest

## Тестирование
- Юнит-тесты для сервисов
- Интеграционные тесты API
- Celery замокан для стабильности

## Запуск в Docker
```bash
docker-compose up --build
```
Проект будет доступен по адресу: http://localhost:8000

Документация Swagger доступна по адресу: http://localhost:8000/docs

## Структура проекта
```
app/
|-- api/          # Роуты
|-- core/         # Настройки, celery, redis
|-- db/           # Модели, сессия, Alembic
|-- schemas/      # Pydantic-схемы
|-- services/     # Бизнес-логика
|-- main.py       # Точка входа
|-- tasks.py      # Celery задачи
```
