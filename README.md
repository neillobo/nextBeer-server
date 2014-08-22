# Next Beer

> The first beer recommendation app with a fun interface.

## Team

  - __Product Owner__: Neil Lobo
  - __Scrum Master__: Boris Verkhovskiy
  - __Development Team Members__: Caly Moss, DH Lee

## Requirements

  - Python 2.6+
  - pip
  - Postgres 9.3.4
  - See [requirements.txt](requirements.txt) for required python packages

### Installing Dependencies


We use virtualenv to manage dependencies.

To install all dependencies,

```sh
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

To start and reload the database,

```sh
pg_ctl start
psql -c 'create database test_nextbeer;' -U postgres
psql -a -U postgres -d test_nextbeer -f resetTables.sql
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
