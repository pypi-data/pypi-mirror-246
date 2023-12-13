# db4me

Basic sqlalchemy helpers

## Installation

```bash
python -m pip install db4me
```

## Usage

Include the database settings into your model and, at application
start-up time, create the connection based on these settings.

```python
from pydantic_settings import BaseSettings
from db4me import AllDatabaseSettings, get_engine


class AppSettings(BaseSettings):
    # ...
    database: AllDatabaseSettings = Field(
        description="Database settings.",
    )
    # ...


settings = AppSettings()
engine = get_engine(settings.database)
```

## Development

Start by creating a virtual environment and installing the dependencies.
If you have a `make` command available, you can run `make init` after
the virtual environment is created and activated. Otherwise, you can run
the following commands:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

On Windows, to be able to serve the documentation, you may also need to
install the `cairo2` package:

```bash
pip install pipwin
pipwin install cairocffi
```
