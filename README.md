
# Ласкаво прошу до захоплюючого завдання з проектування API!

## 📁 Структура проекту

```
contacts-api/
├── app/
│   ├── main.py                 # Головний файл додатку
│   ├── config.py              # Налаштування
│   ├── api/
│   │   ├── deps.py            # Залежності
│   │   └── v1/
│   │       ├── api.py         # API роутер v1
│   │       └── endpoints/
│   │           └── contacts.py # Ендпоінти контактів
│   ├── database/
│   │   ├── base.py            # Базовий клас моделей
│   │   └── connection.py      # З'єднання з БД
│   ├── models/
│   │   └── contacts.py        # SQLAlchemy моделі
│   ├── schemas/
│   │   └── contacts.py        # Pydantic схеми
│   └── crud/
│       └── contacts.py        # CRUD операції
├── .env                       # Змінні середовища
├── .gitignore                # Git ігнорування
├── docker-compose.yaml       # Docker композиція
├── init.sql                  # Ініціалізація БД (опціонально)
├── requirements.txt          # Python залежності
└── README.md                 # Цей файл
```

## 🚀 Інструкція по запуску

### Крок 1: Встановлення залежностей

```bash
# Клонуйте репозиторій
git clone <your-repo-url>
cd contacts-api

# Створіть віртуальне середовище
python -m venv venv

# Активуйте середовище
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Встановіть залежності
pip install -r requirements.txt
```

### Крок 2: Запуск бази даних

```bash
# Запустіть PostgreSQL та PgAdmin через Docker
docker-compose up -d

# Перевірте статус контейнерів
docker-compose ps

# Якщо треба подивитися логи
docker-compose logs db
```

### Крок 3: Запуск API

```bash
# З кореня проекту
python -m app.main

# Або через uvicorn з auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Крок 4: Перевірка роботи

🌐 **Веб-інтерфейси:**
- **API Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc  
- **PgAdmin:** http://localhost:8080 (admin@example.com / admin123)

🔧 **API тести:**
```bash
# Перевірка здоров'я
curl http://localhost:8000/health

# Список контактів
curl http://localhost:8000/api/v1/contacts/

# Створити контакт
curl -X POST "http://localhost:8000/api/v1/contacts/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Тест",
    "last_name": "Користувач", 
    "email": "test@example.com",
    "phone_number": "+380501234567",
    "birth_date": "1990-12-25",
    "additional_data": "Тестовий контакт"
  }'
```

## 📝 API Ендпоінти

| Метод | URL | Опис |
|-------|-----|------|
| GET | `/` | Головна сторінка |
| GET | `/health` | Перевірка здоров'я |
| POST | `/api/v1/contacts/` | Створити контакт |
| GET | `/api/v1/contacts/` | Список контактів |
| GET | `/api/v1/contacts/{id}` | Отримати контакт |
| PUT | `/api/v1/contacts/{id}` | Оновити контакт |
| DELETE | `/api/v1/contacts/{id}` | Видалити контакт |
| GET | `/api/v1/contacts/birthdays/` | Дні народження (7 днів) |

## 🔍 Параметри пошуку

```bash
# Пошук за іменем, прізвищем або email
GET /api/v1/contacts/?search=Іван

# Пагінація
GET /api/v1/contacts/?skip=0&limit=10

# Комбінований запит
GET /api/v1/contacts/?search=test&skip=0&limit=5
```

## 🗄️ Налаштування PgAdmin

1. Відкрийте http://localhost:8080
2. Введіть дані:
   - **Email:** admin@example.com
   - **Password:** admin123
3. Додайте сервер:
   - **Name:** Contacts DB
   - **Host:** db (назва Docker сервісу!)
   - **Port:** 5432
   - **Database:** contacts_db
   - **Username:** contacts_user
   - **Password:** contacts_password

## 🛠️ Корисні команди

```bash
# Зупинити контейнери
docker-compose down

# Зупинити та видалити дані
docker-compose down -v

# Перезапустити тільки базу
docker-compose restart db

# Подивитися логи
docker-compose logs -f db

# Підключитися до PostgreSQL
docker exec -it contacts_db psql -U contacts_user -d contacts_db
```

## 🐛 Розв'язання проблем

### Проблема: "Connection refused"
```bash
# Перевірте чи запущені контейнери
docker-compose ps

# Перезапустіть базу даних
docker-compose restart db
```

### Проблема: "Module not found"
```bash
# Переконайтеся що ви в правильній директорії
pwd

# Активуйте віртуальне середовище
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Встановіть залежності
pip install -r requirements.txt
```

### Проблема: "Table doesn't exist"
```bash
# SQLAlchemy створить таблиці автоматично
# Але якщо є проблеми, перезапустіть API
python -m app.main
```

## 📊 Приклад даних

Якщо ви використовуєте `init.sql`, в базі будуть тестові контакти:
- Іван Петренко (ivan.petrenko@example.com)
- Марія Коваленко (maria.kovalenko@example.com) 
- Олександр Сидоренко (alex.sydorenko@example.com)

## 🎯 Функціональність

✅ **CRUD операції** - Створення, читання, оновлення, видалення контактів  
✅ **Пошук** - За іменем, прізвищем або email  
✅ **Дні народження** - Контакти з ДН на найближчі 7 днів  
✅ **Валідація** - Email, номер телефону, обов'язкові поля  
✅ **Документація** - Автоматичний Swagger UI  
✅ **База даних** - PostgreSQL з PgAdmin  
✅ **Docker** - Готовий до розгортання  

## 📋 TODO

- [ ] Додати аутентифікацію  
- [ ] Додати тести  
- [ ] Додати логування  
- [ ] Додати rate limiting  

---

**Автор:** Андрій Григоров
**Версія:** 1.0.0  
**FastAPI:** 0.104.1