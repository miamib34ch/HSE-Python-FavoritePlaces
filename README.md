# Favorite Places Service

Service for saving favorite places.

## Requirements:

Install the appropriate software:

1. [Docker Desktop](https://www.docker.com).
2. [Git](https://github.com/git-guides/install-git).
3. [PyCharm](https://www.jetbrains.com/ru-ru/pycharm/download) (optional).

## Installation

Clone the repository to your computer:
```bash
git clone https://github.com/mnv/python-course-favorite-places.git
```

1. To configure the application copy `.env.sample` into `.env` file:
    ```shell
    cp .env.sample .env
    ```
   
    This file contains environment variables that will share their values across the application.
    The sample file (`.env.sample`) contains a set of variables with default values. 
    So it can be configured depending on the environment.

2. Build the container using Docker Compose:
    ```shell
    docker compose build
    ```
    This command should be run from the root directory where `Dockerfile` is located.
    You also need to build the docker container again in case if you have updated `requirements.txt`.

3. To run application correctly set up the database.
   Apply migrations to create tables in the database:
    ```shell
    docker compose run favorite-places-app alembic upgrade head
    ```

4. Now it is possible to run the project inside the Docker container:
    ```shell
    docker compose up
    ```
   When containers are up server starts at [http://0.0.0.0:8010/docs](http://0.0.0.0:8010/docs). You can open it in your browser.

## Usage

### Migrations

To first initialize migration functionality run:
```bash
docker compose exec favorite-places-app alembic init -t async migrations
```
This command will create a directory with configuration files to set up asynchronous migrations' functionality.

To create new migrations that will update database tables according updated models run this command:
```bash
docker compose run favorite-places-app alembic revision --autogenerate  -m "your description"
```

To apply created migrations run:
```bash
docker compose run favorite-places-app alembic upgrade head
```

### Automation commands

The project contains a special `Makefile` that provides shortcuts for a set of commands:
1. Build the Docker container:
    ```shell
    make build
    ```

2. Generate Sphinx documentation run:
    ```shell
    make docs-html
    ```

3. Autoformat source code:
    ```shell
    make format
    ```

4. Static analysis (linters):
    ```shell
    make lint
    ```

5. Autotests:
    ```shell
    make test
    ```

    The test coverage report will be located at `src/htmlcov/index.html`. 
    So you can estimate the quality of automated test coverage.

6. Run autoformat, linters and tests in one command:
    ```shell
    make all
    ```

Run these commands from the source directory where `Makefile` is located.

## Documentation

The project integrated with the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation engine. 
It allows the creation of documentation from source code. 
So the source code should contain docstrings in [reStructuredText](https://docutils.sourceforge.io/rst.html) format.

To create HTML documentation run this command from the source directory where `Makefile` is located:
```shell
make docs-html
```

After generation documentation can be opened from a file `docs/build/html/index.html`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
