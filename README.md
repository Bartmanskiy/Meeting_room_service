# Meeting Room Service

REST API для керування переговорними кімнатами та бронюваннями.

Проєкт створений для практики backend-розробки на Python із використанням FastAPI, PostgreSQL, SQLAlchemy та Docker.

## Можливості

* перегляд доступних переговорних кімнат;
* створення бронювання;
* перевірка конфліктів між бронюваннями;
* перегляд усіх бронювань;
* фільтрація бронювань за кімнатою;
* фільтрація бронювань за датою;
* видалення бронювання;
* валідація часу бронювання;
* автоматичне створення таблиць бази даних;
* автоматичне додавання тестових переговорних кімнат;
* запуск API та PostgreSQL через Docker Compose;
* автоматичне тестування API.

## Технології

* Python 3.11
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* pytest
* Docker
* Docker Compose

## Архітектура

У проєкті використовується розділення відповідальності між окремими шарами:

```text
Клієнт
  ↓
FastAPI Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

### Router

Відповідає за HTTP-запити, параметри запитів та response models.

### Service

Містить бізнес-логіку застосунку.

Наприклад:

* перевіряє існування кімнати;
* перевіряє наявність конфлікту з іншим бронюванням;
* створює бронювання;
* видаляє бронювання.

### Repository

Відповідає за взаємодію з базою даних та виконання SQLAlchemy-запитів.

### Database

PostgreSQL використовується як основна база даних, а SQLAlchemy — як ORM для роботи з нею.

## Структура проєкту

```text
Meeting_room_service/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── bookings.py
│   │       └── rooms.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── repositories/
│   │   ├── booking_repository.py
│   │   └── room_repository.py
│   │
│   ├── schemas/
│   │   ├── booking.py
│   │   └── room.py
│   │
│   ├── services/
│   │   └── booking_service.py
│   │
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   └── test_bookings.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API

| Метод  | Endpoint                     | Опис                      |
| ------ | ---------------------------- | ------------------------- |
| GET    | `/api/rooms`                 | Отримати список кімнат    |
| POST   | `/api/bookings`              | Створити бронювання       |
| GET    | `/api/bookings`              | Отримати список бронювань |
| DELETE | `/api/bookings/{booking_id}` | Видалити бронювання       |

### Фільтрація бронювань

Отримати бронювання конкретної кімнати:

```text
GET /api/bookings?room_id=1
```

Отримати бронювання за конкретною датою:

```text
GET /api/bookings?date=2030-01-15
```

Можна використовувати обидва параметри одночасно:

```text
GET /api/bookings?room_id=1&date=2030-01-15
```

## Правила бронювання

### Час бронювання

`start_time`:

* не може бути в минулому.

`end_time`:

* повинен бути більшим за `start_time`.

Некоректні дані повертають:

```text
422 Unprocessable Entity
```

### Перетин бронювань

Два бронювання однієї кімнати не можуть перетинатися в часі.

Наприклад:

```text
10:00 ───────── 11:00
        10:30 ───────── 11:30
```

Друге бронювання буде відхилено:

```text
400 Bad Request
```

При цьому послідовні бронювання дозволені:

```text
10:00 ───────── 11:00
                  11:00 ───────── 12:00
```

Тобто бронювання, яке починається точно в момент завершення попереднього, не вважається конфліктним.

## Початкові кімнати

Якщо база даних не містить кімнат, застосунок автоматично створює три кімнати:

| Кімната         | Місткість |
| --------------- | --------: |
| Meeting Room 1  |         6 |
| Meeting Room 2  |        10 |
| Conference Room |        20 |

## Запуск локально

### 1. Клонування репозиторію

```bash
git clone https://github.com/Bartmanskiy/Meeting_room_service.git
cd Meeting_room_service
```

### 2. Створення віртуального середовища

Windows:

```bash
python -m venv .venv
```

Активація:

```bash
source .venv/Scripts/activate
```

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 4. Налаштування змінних середовища

Створіть файл `.env` на основі `.env.example`.

Приклад:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=meeting_rooms
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

PostgreSQL повинен бути запущений локально.

### 5. Запуск застосунку

```bash
uvicorn app.main:app --reload
```

API буде доступний за адресою:

```text
http://localhost:8000
```

Swagger-документація:

```text
http://localhost:8000/docs
```

## Запуск через Docker

Docker Compose запускає два сервіси:

* FastAPI застосунок;
* PostgreSQL базу даних.

Для запуску:

```bash
docker compose up -d --build
```

Перевірити стан контейнерів:

```bash
docker compose ps
```

Зупинити контейнери:

```bash
docker compose down
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

## Тестування

Запустити всі тести:

```bash
pytest
```

Тести перевіряють:

* створення бронювання;
* бронювання неіснуючої кімнати;
* конфліктуючі бронювання;
* послідовні бронювання;
* час початку в минулому;
* неправильний час завершення;
* отримання бронювань;
* фільтрацію за кімнатою;
* фільтрацію за датою;
* видалення бронювання;
* видалення неіснуючого бронювання;
* отримання списку кімнат.

На поточному етапі проєкт містить **13 тестів API**.

## Приклад створення бронювання

Запит:

```http
POST /api/bookings
Content-Type: application/json
```

```json
{
  "room_id": 1,
  "organizer_name": "Pavlo",
  "start_time": "2030-01-15T10:00:00",
  "end_time": "2030-01-15T11:00:00"
}
```

Успішна відповідь:

```json
{
  "id": 1,
  "room_id": 1,
  "organizer_name": "Pavlo",
  "start_time": "2030-01-15T10:00:00",
  "end_time": "2030-01-15T11:00:00"
}
```

## База даних

Для зберігання даних використовується PostgreSQL.

SQLAlchemy використовується як ORM.

Основні сутності:

```text
rooms
  │
  │ 1 : N
  ↓
bookings
```

Одна кімната може мати багато бронювань.

Кожне бронювання належить одній кімнаті.

## Змінні середовища

Конфіденційні змінні середовища не зберігаються в Git.

У репозиторії знаходиться:

```text
.env.example
```

Локальні файли з реальними даними:

```text
.env
.env.docker
```

додані до `.gitignore`.

## Призначення проєкту

Проєкт створений у навчальних цілях для практики:

* Python backend;
* FastAPI;
* REST API;
* PostgreSQL;
* SQLAlchemy;
* Repository/Service architecture;
* Dependency Injection через `Depends()`;
* тестування API;
* Docker та Docker Compose.
