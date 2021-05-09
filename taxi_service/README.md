
## Installation

To start, clone the repo to your local computer and change into the proper directory.

```
$ git clone https://github.com/Vadym-Hub/taxi_service.git
$ cd taxi_service
```

### Pipenv

```
$ pip install pipenv
$ pipenv shell
(taxi_service) $ pipenv install
(taxi_service) $ python manage.py migrate
(taxi_service) $ python manage.py createsuperuser
(taxi_service) $ python manage.py runserver
# Load the homepage of site at http://127.0.0.1:8000
```

### Docker

```
$ docker build .
$ docker-compose up -d
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
# Load the homepage of site at 0.0.0.0:8000
```

----

## Description

Тестовое задание

Написать сервис заказа такси.
Для клиента:
1. Форма создания заказа - имя клиента, телефон, адрес заказа, адрес следования, желаемое время. Учесть валидацию полей, имя - только кириллица, телефон - соответствовать формату +380(ХХ)ХХХ-ХХ-ХХ. Все поля формы обязательны.

Для диспетчера(должен быть авторизованным):
1. Просмотр списка всех заказов(имя клиента, адрес вызова авто) с пагинацией и с переходом на детализацию по отельному заказу.
2. Просмотр информации по заказу. Выводить всю информацию по заказу.

Дополнительно:
1. При создании заказа проверять наличие свободных авто, если авто свободно то закреплять его за клиентом и фиксировать в БД флаг что авто занято. После чего показать клиенту номер заказа и марку авто.
2. Если при заказе все авто заняты показать клиенту сообщение, что свободных авто нет.
3. Реализовать метод, который будет отвечать за возврат авто в пул свободных.

Использовать Django любой версии, PostgreSQL или SQLite.
Плюсом будет (но не обязательно) если приложение можно будет запустить в docker.
----
