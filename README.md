# DjangoTestProject
* Тестовый проект, задача подробно описана в файле [Python-Test](Python-Test.pdf)
* Все шаги и команды необходимые для оценки результата описаны в этом файле

### Установка и запуск проекта
1. Клонируйте репозиторий с проектом на локальную машину через Git(должен быть предварительно установлен)
2. Запустите проект в Docker(должен быть предварительно установлен)
3. Проверьте работу логики проекта

### Клонирование репозитория
```shell
git clone <путь к репозиторию>
```
### Запуск проекта в Docker
```shell
docker compose -f docker-compose.yml up -d --build
```

### Проверка работы логики проекта
#### Загрузите данные логов из удалённого файла командой
```shell
docker exec -d django-test-project-app-1 python manage.py parse https://drive.google.com/file/d/18Ss9afYL8xTeyVd0ZTfFX9dqja4pBGVp/view?usp=sharing
```
#### Проверьте наличие данных в БД и работу CRUD операций, фильтрации, поиска и сортировки в двух интерфейсах
* REST API http://127.0.0.1:8000/api/logs/
* Django Admin http://127.0.0.1:8000/admin  <login: admin password: admin>

#### Остановка проекта с полным удалением данных и Docker контейнера
```shell
docker compose -f docker-compose.yml down
```

#### Проверка чистоты кода линтерами
```shell
flake8 && mypy . && pylint *
```

#### Недоработки
* для упрощения запуска проекта .env файл намерено был загружен в репозиторий в связи с отсутствием необходимости сокрытия данных
* не выполнено тестирование проекта