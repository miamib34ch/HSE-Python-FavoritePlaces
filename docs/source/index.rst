Любимые места
=============

Сервис для сохранения информации о любимых местах.

Зависимости
===========

Install the appropriate software:

1. [Docker Desktop](https://www.docker.com).
2. [Git](https://github.com/git-guides/install-git).
3. [PyCharm](https://www.jetbrains.com/ru-ru/pycharm/download) (optional).


Установка
=========

Clone the repository to your computer:

.. code-block::console

    git clone https://github.com/mnv/python-course-favorite-places.git

1. To configure the application copy `.env.sample` into `.env` file:

    .. code-block::console

        cp .env.sample .env

    This file contains environment variables that will share their values across the application.
    The sample file (`.env.sample`) contains a set of variables with default values.
    So it can be configured depending on the environment.

2. Build the container using Docker Compose:

    .. code-block::console

     docker compose build

    This command should be run from the root directory where `Dockerfile` is located.
    You also need to build the docker container again in case if you have updated `requirements.txt`.

3. To run application correctly set up the database.
   Apply migrations to create tables in the database:

    .. code-block::console

        docker compose run favorite-places-app alembic upgrade head

4. Now it is possible to run the project inside the Docker container:

    .. code-block::console

        docker compose up

   When containers are up server starts at [http://0.0.0.0:8010/docs](http://0.0.0.0:8010/docs). You can open it in your browser.

Использование
=============

Работа с базой данных
---------------------

To first initialize migration functionality run:

    .. code-block::console

        docker compose exec favorite-places-app alembic init -t async migrations

This command will create a directory with configuration files to set up asynchronous migrations' functionality.

To create new migrations that will update database tables according updated models run this command:

    .. code-block::console

        docker compose run favorite-places-app alembic revision --autogenerate  -m "your description"

To apply created migrations run:

    .. code-block::console

        docker compose run favorite-places-app alembic upgrade head


Автоматизация
=============

The project contains a special `Makefile` that provides shortcuts for a set of commands:

1. Build the Docker container:

.. code-block::console

    make build

2. Generate Sphinx documentation run:

    .. code-block::console

        make docs-html

3. Autoformat source code:

    .. code-block::console

        make format

4. Static analysis (linters):

    .. code-block::console

        make lint

5. Autotests:

    .. code-block::console

        make test

    The test coverage report will be located at `src/htmlcov/index.html`.
    So you can estimate the quality of automated test coverage.

6. Run autoformat, linters and tests in one command:

    .. code-block::console

        make all

    Run these commands from the source directory where `Makefile` is located.

Тестирование
============

To run tests use the following command:

    .. code-block::console

        make all


Документация
============

Клиенты
=======

Базовый
--------
.. automodule:: clients.base.base
    :members:

Geo
---
.. automodule:: clients.geo
    :members:

Schemas
-------
.. automodule:: clients.base.base
    :members:


Integrations
============

Database
--------
.. automodule:: integrations.db.session
    :members:

Events
------
.. automodule:: integrations.events.events
    :members:
.. automodule:: integrations.events.schemas
    :members:

Models
======
.. automodule:: models.mixins
    :members:
.. automodule:: models.places
    :members:

Repositories
============
.. automodule:: repositories.base_repository
    :members:
.. automodule:: repositories.places_repository
    :members:

Settings
========
.. automodule:: settings
    :members:

Schemas
=======
.. automodule:: schemas.base
    :members:
.. automodule:: schemas.places
    :members:
.. automodule:: schemas.routes
    :members:

Services
========
.. automodule:: services.places_service
    :members:

Transport
=========
.. automodule:: transport.handlers.places
    :members: