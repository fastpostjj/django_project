## Учебный проект для работы с Django и базой данных PostgreSQL

В базе данных содержатся две таблицы:

*   Product
*   Category

Реализован CRUD для моделей Product и Category

Для корректного подключения к базе данных настройки для подключения должны находится в файле database.ini в корневом каталоге проекта. Файл дожен иметь следующую структуру:

    [postgresql]
    host=<имя хоста>
    user=<имя пользователя базы данных>
    password=<пароль>
    port=<порт>

В проекте реализованы следущие url:
*   /
  * index/
  * contact/
  * gallery/
  * about/
  * categories/

Реализованы команды:
*   save_category - сохранение данных из таблицы категории в файл save_category.json
* save_products - сохранение данных из таблицы продукты в файл save_data.jso
* load_data - восстановление данных из файлов
