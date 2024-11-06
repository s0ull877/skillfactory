# Витруальная стажировка backend skillfactory
### Создание REST API для Федерации Спортивного Туризма России

## Оглавление:
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Описание работы](#описание-работы)
- [Удаление](#удаление)

## Технологии
<details>
  <summary>Подробнее</summary>
    <p><strong>Языки программирования:</strong> python</p>
    <p><strong>Фреймворк и модули:</strong> Django, djangorestframework</p>
    <p><strong>Базы данных и инструменты работы с ними:</strong> PostgreSQL, SQLite</p>
    <p><strong>Документрирование:</strong>drf-yasg, swagger</p>  
    <p><strong>CI/CD:</strong> Docker Hub, Docker Compose, Gunicorn, Nginx</p>  
</details>

## Установка и запуск

<details>
  <summary>Предварительные условия</summary>
  <p>Предполагается, что пользователь:</p>
  
  - Создал аккаунт [DockerHub](https://hub.docker.com/).
  - Установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
    
  `docker --version && docker-compose --version`
  
</details>
<details>
  <summary>Запуск</summary>
  
  <p><strong>!!! Для пользователей Windows обязательно выполнить команду:</strong></p>
  
    `git config --global core.autocrlf false`
    
  <p>иначе файл start.sh при клонировании будет бракован</p>
  
  1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, некоторые можно оставить по типу DB*):
    
    git clone https://github.com/s0ull877/skillfactory.git && \
    cd skillfactory/app && \
    cp .env_example .env && \
    nano .env

  2. Из корневой директории проекта выполните команду:

    docker compose -f infra/docker-compose.yml up -d --build

  Проект будет развернут в трех docker-контейнерах (db, web, nginx) по адресу `http:/host_ip/`
  
  3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:

    docker compose -f infra/docker-compose.yml down
  
  Если также необходимо удалить тома базы данных, статики и медиа:

    docker compose -f infra/docker-compose.yml down -v

</details>

---

При первом запуске будут автоматически произведены следующие действия:

  - выполнены миграции

  - собрана статика

  - создан суперюзер с учетными данными:
    - username = 'root', password = 'root'
      
    - собственными данными, если внесете в .env переменные `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_USERNAME`
      
Документация к api представлена по адресу:

  - `http://127.0.0.1/redoc/ | http://127.0.0.1/swagger<format>/`
  - `http://localhost/redoc/ | http://localhost/swagger<format>/`
  - `http://<IP-адрес удаленного сервера>/redoc/ | http://<IP-адрес удаленного сервера>/swagger<format>/`
   
Вход в админ-зону осуществляется по адресу:

  - `http://127.0.0.1/admin/`
  - `http://localhost/admin/`
  - `http://<IP-адрес удаленного сервера>/admin/`

Запросы к api осуществляются через endpoint`ы:

  - `http://127.0.0.1:8000/api/v1/submitData/` 
  - `http://localhost/api/v1/submitData/` 
  - `http://<IP-адрес удаленного сервера>/api/v1/submitData/`

## Описание работы

В ходе реализации проекта были созданы 5 моделей: `UserProfile, Perevals, PerevalLevel(OneToOne), Coordinates(OneToOne), PerevalImages(ManyRelated)`.<br><br>При написании `PerevalSerializer` были переписаны методы `create, update, to_representation`. 
<br><br><br>API включает в себя 2 эндпоинта `submitData/` (POST, GET) и  `submitData/<pk>/` (GET, PATCH). 
<br><br>Метод `POST` принимает в теле запроса данные(пример в файле example.json) и после кастомной валидации возвращает status, message и id созданного обьекта, в противном случае id будет none.
<br><br>Метод `GET` у `submitData/` имеет обязательный query_param в `user__email` и возвращает все обьекты `Perevals` в perevals, созданные пользователем с email из user__email, в противном случае `perevals = None` и описание ошибки в `message`.
<br><br>Метод `GET` `submitData/<pk>/` возвращает Pereval обьект по его id, включая статус модерации и message, если запрос некоректный или элемент не найден.
<br><br>Метод `PATCH` `submitData/<pk>/`, обновляет данные элемента Pereval по его id. Обязательным условием является неизменяемость полей в ключе `user`. Если partial update успешный, метод возвращает `state: '1'`, иначе `state: '0'` и `message` с описанием ошибки.
<br><br><br>Все правила возвращения статус кодов соблюдены, так что можно отталкиваться и от них. Более подробная информация к содержанию request body описана в документации по адресу `http:/project_ip/(swagger<format>, swagger, redoc)/`
При написании документации были использованы `swagger_auto_schema` декораторы из `drf_yasg.utils` для каждого crud метода контроллера.
<br><br><br>API методы покрыты тестами в `rest_api\tests.py`

## Удаление
Для удаления проекта выполните следующие действия:

  `cd .. && rm -fr skillfactory && deactivate`

[Оглавление](#оглавление)

## <a id="#автор">Автор</a>
[Radmir Galiullin](https://github.com/s0ull877)
