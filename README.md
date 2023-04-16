# Connector
**Основной сервер запущен на https://connector.pythonanywhere.com**

## Использовано
- Python
- Flask 
- SQLite
- Flask-SQLalchemy 
- Flask-Login 

## Кратко по серверу
Реализована система аккаунтов, постов и комментариев.
Пользователь имеет три типа аккаунта - Пользователь[0], Модератор[1], Администратор[2]
Где цифры - ID роли.
Администратором автоматически становится первый зарегистрированный пользователь.

Для администрации существует админ-панель.
Людям с первым уровнем (модераторам) доступен небольшой функционал:
- Блокировка / разблокировка аккаунтов
- Очистка недоступных публикаций

А людям со вторым уровнем (администраторам) доступен полный функционал:
- Очистка всех комментариев
- Удаление забаненных аккаунтов
- Разбан всех аккаунтов
- Удаление конкретного аккаунта/поста
- Выдача уровня администратора

# Установка
```bash
pip install -r requirements.py
flask run
```
Первой командой устанавливаются необходимые модули, второй - производится запуск сервера.