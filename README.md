# QRKot

## QRKot - это сервис для пожертвований в Благотворительный фонд поддержки котиков.

### Описание проекта

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

### Как развернуть проект на компьютере:

Клонировать репозиторий с GitHub

```
$ git clone https://github.com/vecha1337/cat_charity_fund.git
$ cd cat_charity_fund
```

Создать и активировать виртуальное огружение 

```
# Windows
$ python -m venv venv
$ source venv/Scripts/activate

# Linux
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости из requirements.txt

```
$ pip install -r requirements.txt
```

Создать файл .env с переменными окружения. Пример наполнения:

APP_TITLE=app_title
DESCRIPTION=description
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret

Создать базу данных 

```
$ alembic init --template async alembic
$ alembic upgrade head 
```

Запустить приложение

```
$ uvicorn app.main:app
```


Технологии использованные в прокете:

fastapi, sqlalchemy, alembic, googleapi

### Автор Попов Алексей Сергеевич

### Для связи [Telegram](https://t.me/Vecha1337)