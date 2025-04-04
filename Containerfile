FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install pipenv && \
    pipenv install --deploy --ignore-pipfile
ENTRYPOINT ["pipenv", "run", "python", "app.py"]