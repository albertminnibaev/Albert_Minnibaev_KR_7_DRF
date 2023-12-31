# Курсовая работа №7 DRF
В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. Заказчик прочитал книгу, впечатлился и обратился к вам с запросом реализовать трекер полезных привычек.

В рамках данного учебного курсового проекта реализум бэкенд-часть SPA веб-приложения.

## Модели:
В книге Джеймса Клира «Атомные привычки» хороший пример привычки описывается как конкретное действие, которое можно уложить в одно предложение:

я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

За каждую полезную привычку необходимо себя вознаграждать или сразу после делать приятную привычку. Но при этом привычка не должна расходовать на выполнение больше 2 минут. Исходя из этого получаем первую модель — Привычка.

### Привычка(Habit):
- Пользователь — создатель привычки.
- Место — место, в котором необходимо выполнять привычку.
- Время — время, когда необходимо выполнять привычку.
- Действие — действие, которое представляет из себя привычка.
- Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
- Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.
- Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания.
- Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
- Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
- Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.

### Валидаторы
- Исключен одновременный выбор связанной привычки и указания вознаграждения.
- Время выполнения должно быть не больше 120 секунд.
- В связанные привычки могут попадать только привычки с признаком приятной привычки.
- У приятной привычки не может быть вознаграждения или связанной привычки.
- Нельзя выполнять привычку реже, чем 1 раз в 7 дней.

### Пагинация
- Для вывода списка привычек реализована пагинацию с выводом по 5 привычек на страницу.

### Права доступа
- Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD.
- Пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять.

### Эндпоинты
- Регистрация
- Авторизация
- Список привычек текущего пользователя с пагинацией
- Список публичных привычек
- Создание привычки
- Редактирование привычки
- Удаление привычки

### Интеграция
- Реализована работа с отложенными задачами для напоминания о том, в какое время какие привычки необходимо выполнять.
Для этого произведена интеграция сервиса с мессенджером Telegram, который заниматься рассылкой уведомлений.

### Безопасность
- Для проекта настроена CORS, чтобы фронтенд мог подключаться к проекту на развернутом сервере.

### Документация
- Для реализации экранов силами фронтенд-разработчиков настроен вывод документации.

### Данный проект настроен для запуска с помощью Docker Compose, оформлены файлы Dockerfile и docker-compose.yaml.

Для запуска проекта в Docker нужно:
- создать файл .env
- указать значения переменных окружения в файле .env (набор необходимых перменных указан в файле .env.sample)
- собрать образы командой docker-compose build
- запустить контейнеры командой docker-compose up
