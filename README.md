<a id="anchor"></a>
# Bеб-приложение для сбора данных


[ссылка на веб-сайт: ![link1](https://user-images.githubusercontent.com/97599612/173827421-7652c275-57c8-4cd6-a664-4e199fafc890.png)](http://victorious.pythonanywhere.com/)


<img width="1440" alt="screen1" src="https://user-images.githubusercontent.com/97599612/173827435-07d1b4f8-f6b1-4fde-baa0-1dd787db0d99.png">

___
:sparkle: Содержание:
* [Фронтенд](#front)
* [Бэкенд](#back)
* [1. Создание виртуального окружения](#virtual)
* [2. Захват пользовательского ввода](#capture)
* [3. Создание таблицы в базе данных PostGreSQL](#postgre)
* [4. Хранение пользовательских данных в базе](#storing)
* [5. Отправка емэйла пользователю](#email)
* [6. Отправка пользователю статистических данных](#statistic)
* [7. Развертывание сайта на pythonanywhere.com](#deploy)
___


Веб-сайт для сбора данных о росте пользователей. Пользователям оставившим данные о себе (рост и адрес почты), будет отправлен _email_ примерного содержания:
**"Приветствую, Ваш рост _187_ см. Средний рост всех пользователей _183.0_ см - рассчитано на основе данных _15_ человек."**


** Приложение создано на фреймворке _Flask_. Работает с базой данных _PostGreSQL_.

** Фронтенд - _HTML_ и _CSS_. Бэкенд - _Python_.

Приложение принимает адрес электронной почты и рост (см) у посетителей сайта. Данные сохраняются в базу на сервере. Расчитывается средний рост всех людей в базе. Информация о росте пользователей и величине выборки отправляется на _email_, оставленный посетителем.


<a id="front"></a>

## Фронтенд приложения

### 1. Создание html страницы.
** см. файл: _templates/index.html_;  _templates/success.html_.

### 2. Работа над внешним видом страинц - создание CSS файла.
** см. файл: _static/main.css_.


<a id="back"></a>

## Бэкенд приложения


<a id="virtual"></a>

### 1. Создание виртуального окружения.

Виртуальное окружение создается в начале, чтобы иметь доступ к версии _Python_ без библиотек, 
модулей и всего, что не понадобится в работе над проектом.

> pip install virtualenv

> python3 -m venv virtual

** Установка _Flask_ в виртуальном окружении:

> virtual/bin/pip3 install flask (для mac)

** Запуск веб-сайта в виртуальном окружении:

> virtual/bin/python3 app.py


<a id="capture"></a>

### 2. Захват пользовательского ввода.

Импортируем класс _Flask_ фреймфорка _Flask_ в файле _app.py_:

> from flask import Flask, render_template, request

** _render_template_ - метод для отображения _html_-шаблонов.
** _request_ - метод для доступа к _http_-запросу, отправляемому браузером и его чтения.


Создаем переменную _app_ для хранения экземляра объекта:

> app = Flask(__name__)

** name - специальная переменная, в качестве значения принимающая название _Python_ скрипта.


Используем декоратор _@app.route('/')_ для создания Домашней страницы.

_URL_ по которому виден вебсайт (/ - Домашняя страница)

Создадим функцию, определяющую функционал веб-страницы:

```
@app.route("/")
def index():
    return render_template("index.html")
```

** С помощью данной функции, _Python_ имеет доступ к _templates/index.html_, и отображает файл _index.html_ по адресу домашней страницы.



Используем новый декоратор и новую функцию, для создания страницы _'success'_:

```
@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"] # Убедимся в получении POST запроса, так как пользователь может перейти на данный URL и другими способами.
        height = request.form["height_name"]
        print(email, height)
        return render_template("success.html")
```

** При создании декоратора, по умолчанию используется метод _GET_. Во избежание ошибки _'Method Not Allowed'_, укажем нужный метод: methods=['POST']. Метод _'POST'_ нужен для передачи емэйла и роста пользователей на сервер.


Далее:

if __name__ == "__main__":
    app.debug=True
    app.run()

** При запуске _Python_ файла, _Python_ присваивает файлу имя _main_. При импорте данного скрипта в другой файл, данному скрипту будет присвоено имя _app.py_, соответсвенно приложение запускается только из данного файла.


<a id="postgre"></a>

### 3. Создание таблицы в базе данных PostGreSQL.

> pip install psycopg2

> pip install Flask-SQLAlchemy


> from flask_sqlalchemy import SQLAlchemy


Создание модели базы данных - таблица с колонками.

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://*******:********@localhost/height_collector'
db = SQLAlchemy(app)
```

```
class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_
```

Команды в терминале:
> python
> from app import db
> db.create_all()


<a id="storing"></a>

### 4. Хранение пользовательских данных в базе данных.

В функции _def success()_:

```
    if db.session.query(Data).filter(Data.email_==email).count() == 0:
        data = Data(email, height) # создание экземпляра объекта класса Data с двумя параметрами email_, height_
        db.session.add(data) # для добавления строк в таблицу с помощью SQLAlchemy, обратимся к объекту SQLAlchemy (db)
        db.session.commit() # метод commit класса session фиксирует изменения в базе данных
        return render_template("success.html")
return render_template("index.html", text="Seems like we've got something from that email address already!")
```

<a id="email"></a>

### 5. Отправка емэйла пользователю.
** см. файл _send_email.py_.

```
import smtplib
from email.mime.text import MIMEText


def send_email(email, height):
    from_email = "********@google.com"
    from_password = "***********"
    to_email = email
   
    subject = "Height data"
    message = "Hey there, your height is <strong>%s</strong>." % height

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    server = smtplib.SMTP('smtp.google.com', 587)
    server.ehlo()
    server.starttls()
    server.login(from_email, from_password)
    server.send_message(msg)
```

<a id="statistic"></a>

### 6. Отправка пользователю статистических данных (средний рост и величина выборки).

> from sqlalchemy.sql import func  # average function

```
average_height = db.session.query(func.avg(Data.height_)).scalar()
average_height = round(average_height, 1)
count = db.session.query(Data.height_).count()
send_email(email, height, average_height)
```

```
def send_email(email, height, average_height):
    message = "Hey there, your height is <strong>%s</strong>. Average height of all is <strong>%s</strong> and that is calculated out <strong>%s</strong> of people." % (height, average_height, count)
```

<a id="deploy"></a>

### 7. Развертывание сайта на [pythonanywhere.com](https://www.pythonanywhere.com):

_Pythonanywhere_ как и _Heroku_ позволяет бесплатно развертывать _Flask_-приложения.

Важно:
```
if __name__ == "__main__":
    app.run(debug=True)
```

** При развертывании сайта, в файле _app.py_, __True__ заменим на __False__, чтобы не показывать посетителям ошибки _Python_, так как это может привести к уязвимости сайта.

[Вверх](#anchor)
