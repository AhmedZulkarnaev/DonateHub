# 📦 DonateHub

> Платформа для создания и управления денежными сборами с поддержкой платежей, авторизации, email-уведомлений и фоновыми задачами через Celery.

---

## 🚀 Технологии

- **Django 5** — backend-фреймворк
- **PostgreSQL** — база данных
- **Celery + Redis** — асинхронные задачи
- **DRF + drf-yasg** — API и документация Swagger
- **Docker** — контейнеризация проекта
- **JWT (SimpleJWT)** — аутентификация
- **SMTP** — email-уведомления

---

## 🐳 Быстрый старт (Docker)

```bash
git clone https://github.com/yourname/donatehub.git
cd donatehub
cp .env.example .env  # создай файл конфигурации
```

### 📦 Собрать и запустить
```bash
docker-compose up --build
```

### 🛠 Создать и применить миграции, создать суперпользователя
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🔑 Авторизация

JWT-токены:
- Получить токен: `POST /api/token/`
- Обновить токен: `POST /api/token/refresh/`

---

## 📬 Email-уведомления

- При создании сбора автор получает письмо ✅
- При платеже донатор получает письмо ✅
- Отправка писем через Celery + SMTP

---

## 📘 Документация API

Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  
ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## ⚙️ Пример `.env`

```dotenv
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=donatehub
DB_USER=donateuser
DB_PASSWORD=donatepass
DB_HOST=db
DB_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

---

## 🧪 Тестовые данные

```bash
docker-compose exec web python manage.py generate_mock_data --users=50 --collects=100 --payments=300
```

---

## 👤 Автор

> Made with by [Твоё Имя](https://github.com/AhmedZulkarnaev)

---

## 🪪 Лицензия

Проект распространяется под лицензией [MIT](LICENSE)
