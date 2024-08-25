# dormantracker

## Set up

### Create python environment

```
python3 -m venv dormenv
echo 'alias dormenv="source dormenv/bin/activate"' >> ~/.zshrc
dormenv
python3 -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### Postgress Database

You need to set up these environment variables in order to connect to the database

Copy the `.env_example` into a file named `.env` in the main directory and add your credentials.

If you don't have access to the production database you can run the following SQL in `DDL.sql` to create the same tables on your own database.


#### Running The database locally
install postgres on Mac
```
brew install postgresql
```

start the postgres database installed by brew
```
brew services start postgresql
```

create the database
```
createdb dormantrackerdb
```
and then run the `DDL.sql` file to create the tables.

Connect to the database
```
psql dormantrackerdb
```

list all tables
```
\dt
```
