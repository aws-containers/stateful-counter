# Counter app

An example app that stores state is postgres

Run it locally in a container with

```
docker build -t counter .

# Create postgres database
docker run -d --name postgres \
    -e POSTGRES_PASSWORD=supersecret \
    -v $PWD/init.sql:/docker-entrypoint-initdb.d/init.sql:ro \
    -p 5432:5432 \
    postgres
```

By default the app uses the following environment variables for configuration

```
export DB_USER=${postgres}
export DB_PASS=${supersecret}
export DB_HOST=${postgres}
export DB_PORT=${5432}
export DB_DB=${postgres}
```

```
# Run counter app and link it to postgres

docker run -it --rm \
    --name counter \
    -p 8000:8000 \
    --link postgres \
    counter
```

### Develop

To develop the application outside of a container you can

Create a database

```
# Create postgres database
docker run -d --name postgres \
    -e POSTGRES_PASSWORD=supersecret \
    -v $PWD/init.sql:/docker-entrypoint-initdb.d/init.sql:ro \
    -p 5432:5432 \
    postgres
```

```
pipenv install
pipenv shell
```

Source the environment file

```
source .env
DB_HOST=localhost
```

Run the application
```
python app.py
```
