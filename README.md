# Это тестовое задание со слюдующей формулировкой:
# Стек обязательных используемых технологий:
* Python 3 (Latest stable);
* FastAPI (Latest stable);
* Postgresql 12 (Latest stable);
* virtualenv;
Тема задачи: Задача заключается в реализации сервиса-опросника для сбора отзывов, проведения голосований, реализации ab-тестирования и т.д.
# Базовый уровень:
Полноценный CRUD на работу с новым голосованием или опросом (далее по тексту Опрос), в
графическом интерфейсе.
* Страница с отображением всех заведенных Опросов;
* Создание/Редактирование/Удаление Опросов;
* Просмотр информации об Опросе;
* Просмотр результатов Опросов;
* 2 типа Опросов(Голосование - один вопрос, несколько вариантов ответа, Опрос - несколько
вопросов с вариантами или возможностью свободного ответа - текстовое поле).
# Средний уровень:
Требования базового уровня +
* Авторизация локальных пользователей;
* Настройка Опросов(кто может участвовать, кто может видеть результаты, возможность
множественного голосования для каждого вопроса в Опросе, возможность проходить Опросы повторно);
* Отображение для пользователя только его собственных Опросов(всегда должен быть создатель Опроса), либо Опросов, где он может участвовать;
* Блокирование возможности проходить Опросы повторно, если не настроено иное. Обработать редирект на просмотр: результатов(если есть доступ), иначе собственных ответов.
# Продвинутый уровень:
Требования среднего уровня +
* REST API для возможности пройти Опрос(увидеть вопросы, отправить ответы на сервер);
* Vue.js приложение для Frontend-части;
* Возможность выгрузить результаты Опроса для его создателя.
Срок выполнения - 3 дня.