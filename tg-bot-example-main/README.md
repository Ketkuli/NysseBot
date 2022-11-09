# Telegram bot example

Python-based template for TG bots

## Development

1. Copy `.env.sample`. rename it to just `.env` and paste your Telegram bot API token there (obtained from https://t.me/BotFather)

2. Install the packages in Pipfile manually or via pipenv (https://pipenv.pypa.io/en/latest/install/) if you have it:
    - Manual install:
        ```bash
        pip install python-dotenv python-telegram-bot requests
        ```

    - pipenv:
        ```bash
        pipenv install --dev
        pipenv shell
        python bot.py
        ```

3. Edit `bot.py`, save changes and restart the process to update.
    - You can automate this with the `jurigged` package:

        ```bash
        pipenv install jurigged
        python -m jurigged -v bot.py
        ```

## Production

You can run the python script as is if your production server has the right python version and pipenv installed, use `pipenv ci` to install the necessary packages. Background running can be done with `nohup`.

Alternatively, create a Docker container from the script and run that.

Create a file called `Dockerfile` and paste the contents:
```Dockerfile
# Image setup
FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN pip install pipenv

WORKDIR /src

# Install python dependencies
COPY Pipfile /src
COPY Pipfile.lock /src
RUN pipenv install --system --deploy

# Copy code
COPY ./* /src

# Entry point
CMD ["python", "bot.py"]
```

Build the container based on Dockerfile, tag it with a name and run it. `-d` = detached mode, container will keep running after terminal is closed. `--restart on-failure:5` = restart container after failure, maximum 5 times before stopping.
```bash
docker build -t example-bot .
docker run -d --restart on-failure:5 example-bot
```

If you want to use Docker and need to add a database, it's time to start looking into docker-compose.

## Docs

- https://docs.python-telegram-bot.org/en/latest/index.html
- https://core.telegram.org/bots/api