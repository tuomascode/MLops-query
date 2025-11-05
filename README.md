# MLOps-Query
To run the project, follow these steps


Set up your timescale database
```sh
docker compose up timescaledb
uv run alembic upgrade head
```

Then, while this is running, start polling with the backend
```sh
docker compose up poller
```

Now, you should be able to access the output at port 8000 with

```sh
curl http://localhost:8000
```


# Initial plan

Docker compose

Multiple containers dealing with different responsibilities

1. api query container
    * return json with all relevant data
2. DB container
3. Dashboard container