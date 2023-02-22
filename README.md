# Проект YaMDb
### Описание проекта:
Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять **комментарии** к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Пользовательские роли и права доступа
-   **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
-   **Аутентифицированный пользователь (**`user`**)** — может читать всё, как и **Аноним**, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
-   **Модератор (**`moderator`**)** — те же права, что и у **Аутентифицированного пользователя**, плюс право удалять и редактировать **любые** отзывы и комментарии.
-   **Администратор (**`admin`**)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
-   **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Технологии:
Python, Django, Django REST Framework, JWT, SQLite3.

### Как запустить проект:
1. Клонировать репозиторий:
```git clone https://github.com/vinni-pushinka/api_yamdb.git```
2. Перейти в него в командной строке:
```cd api_yamdb```
3. Cоздать и активировать виртуальное окружение:
```python -m venv venv```
```venv/Scripts/activate```
4. Установить зависимости из файла requirements.txt:
```python -m pip install --upgrade pip```
```pip install -r requirements.txt```
5. Выполнить миграции:
```python manage.py makemigrations```
```python manage.py migrate```
6. Запустить проект:
```python manage.py runserver```

### Документация:
Документация API доступна по адресу `http://127.0.0.1:8000/redoc/`.

### Примеры запросов:
 - **Регистрация пользователя в системе:**
POST (c параметрами `email` и `username`)
`/api/v1/auth/signup/`
В ответ сервис **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на указанный адрес `email`.
- **Получение пользователем токена:**
POST (с параметрами `username` и `confirmation_code`)
 `/api/v1/auth/token/`
В ответе на запрос пользователю приходит `token` (JWT-токен).
- **Получение списка жанров:**
GET `/api/v1/genres/`
- **Получение списка произведений:**
GET `/api/v1/titles/`
- **Получение списка отзывов:**
GET `/api/v1/titles/{title_id}/reviews/`
- **Получение списка комментариев к отзыву:**
GET `/api/v1/ /titles/{title_id}/reviews/{review_id}/comments/`

### Команда проекта:
[Andrei Bodrov](https://github.com/awesky): отзывы, комментарии, рейтинг произведений;
[Dmitriy Mayorov](https://github.com/dmay92): произведения,   категории,  жанры, работа с базой;
[Valeria Goran](https://github.com/vinni-pushinka): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail.

> Written with [StackEdit](https://stackedit.io/).