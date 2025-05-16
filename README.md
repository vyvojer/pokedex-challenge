# Pokedex Challenge

A Django-based web application for exploring PokeAPI data. The frontend is based on HTMX, PokeAPI integration is based on Celery, and the API is based on Django REST Framework.

## Getting started

### Clone the project

```bash
git clone https://github.com/vyvojer/pokedex-challenge.git
cd pokedex-challenge
```

### Create environment files

Create the following environment files in the `.envs` directory:

1. `.envs/.app`:
```
SECRET_KEY=<your_secret_key>
DEBUG=True
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=http://localhost
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

2. `.envs/.postgres`:
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=pokedex
POSTGRES_USER=pokedex
POSTGRES_PASSWORD=pokedex
```

3. `.envs/.redis`:
```
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/1
```

4. `.envs/.nginx`:
```
DOMAIN=localhost
```

### Run the project using Docker Compose

```bash
docker compose up -d
```

This will start all the services defined in the `docker-compose.yml` file:
- app: The main Django application
- celery-worker: Celery worker for background tasks
- postgres: PostgreSQL database
- redis: Redis for Celery and caching
- flower: Flower for monitoring Celery tasks
- nginx: Nginx web server

### Add a superuser

```bash
docker compose exec app python manage.py createsuperuser
```

Follow the prompts to create a superuser account.

### Run command for adding periodic tasks

```bash
docker compose exec app python manage.py create_periodic_tasks
```

This command creates periodic tasks for data synchronization from PokeAPI.

### Run periodic tasks via admin


- navigate to "Periodic tasks" in the admin http://localhost/admin/django_celery_beat/periodictask/
- select all tasks
- select the actions "Run selected tasks" and click the "Go" button to start the tasks

### Control process of data loading via Flower

You can monitor Celery tasks using Flower at http://localhost:5555

## Frontend Screens

The application has the following screens, accessible from the sidebar menu:

### Pokémons

Displays a list of Pokémons with their basic information. You can:
- Filter Pokémons by name, types, abilities
- Click on the "Detail" button to view its details
- Order the list by clicking on column headers

### Types

Displays a list of Pokémon types. You can:
- Filter Types by name
- Click on the "Detail" button to view its details
- Order the list by clicking on column headers

### Abilities

Displays a list of Pokémon abilities. You can:
- Filter Abilities by name
- Click on the "Detail" button to view its details
- Order the list by clicking on column headers

### Pokémon comparison

Allows you to compare multiple Pokémons side by side.


## API

The API is documented using Swagger UI, which is available at:

http://localhost/api/v1/schema/swagger-ui/

## Environment variables

### Required environment variables

- `SECRET_KEY`: Django secret key
- `POSTGRES_DB`: PostgreSQL database name
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_HOST`: PostgreSQL host
- `POSTGRES_PORT`: PostgreSQL port
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port

### Optional environment variables

- `DEBUG`: Enable debug mode (default: False)
- `ENVIRONMENT`: Environment name (default: production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted origins for CSRF
- `LOG_LEVEL`: Logging level (default: INFO)
- `PAGE_SIZE`: Number of items per page (default: 10)
- `COMPARISON_MAX_POKEMON_NUMBER`: Maximum number of Pokémons that can be compared (default: 6)
- `SENTRY_DSN`: Sentry DSN for error tracking
- `SENTRY_ENABLE_TRACING`: Enable Sentry tracing (default: False)
- `SENTRY_ENVIRONMENT`: Sentry environment name (default: production)

## Testing

To run tests using Docker Compose:

```bash
docker compose run --rm  app python manage.py test
```

This will run the Django test suite.

## Continuous integration

The project includes a GitHub Actions workflow that runs on push to any branch except master. The workflow is defined in `.github/workflows/push.yml` and includes the following jobs:

1. **build**: Builds a Docker image for the application
2. **tests**: Runs the Django test suite
3. **isort**: Checks Python import sorting using isort
4. **black**: Checks Python code formatting using Black

## Docker services

The project includes the following Docker services:

- **app**: The main Django application
  - Built from the Dockerfile in `dockerfiles/development/Dockerfile`
  - Depends on the postgres service
  - Uses environment variables from `.envs/.app`, `.envs/.postgres`, and `.envs/.redis`
  - Mounts the project directory to `/app` in the container
  - Runs the `scripts/start.sh` script

- **celery-worker**: Celery worker for background tasks
  - Uses the same image as the app service
  - Depends on the postgres and redis services
  - Uses environment variables from `.envs/.app`, `.envs/.postgres`, and `.envs/.redis`
  - Mounts the project directory to `/app` in the container
  - Runs the `scripts/start_worker.sh` script

- **postgres**: PostgreSQL database
  - Uses the postgres:15 image
  - Stores data in the `_postgres_data` directory
  - Uses environment variables from `.envs/.postgres`

- **redis**: Redis for Celery and caching
  - Uses the redis:8-alpine image

- **flower**: Flower for monitoring Celery tasks
  - Uses the mher/flower image
  - Depends on the redis service
  - Uses environment variables from `.envs/.redis`
  - Exposes port 5555

- **nginx**: Nginx web server
  - Uses the nginx image
  - Mounts the nginx configuration from `nginx_config/default.conf`
  - Mounts the static and media directories
  - Uses environment variables from `.envs/.nginx`
  - Depends on the app service
  - Exposes port 80

## Integration with PokeAPI

The application integrates with the [PokeAPI](https://pokeapi.co/) to fetch Pokemon data. The integration is implemented using a modular architecture with the following components:

### Page Loaders

Page loaders are responsible for loading paginated data from an API. The default implementation is `core.integrations.loaders.DefaultPageLoader`, which:
- Makes HTTP requests to the API
- Parses the response to extract entity URLs and pagination information
- Returns a tuple of entity URLs and the URL for the next page

### Entity Loaders

Entity loaders are responsible for loading individual entity data from an API. The default implementation is `core.integrations.loaders.DefaultEntityLoader`, which:
- Makes HTTP requests to a specific entity URL
- Returns the raw JSON response

### Transformers

Transformers are responsible for converting raw data from the an API into a format suitable for the application's data model. The transformers must extend the `core.integrations.BaseTransformer` The application includes:
- `pokemons.integrations.transformers.PokemonTransformer`: Transforms Pokemon data
- `pokemons.integrations.transformers.AbilityTransformer`: Transforms Ability data

### Updaters

Updaters are responsible for creating or updating entities in the database. The application includes:
- `pokemons.integrations.updaters.PokemonUpdater`: Creates or updates Pokemon entities and their relationships
- `core.integrations.updaters.DefaultUpdater`: A generic updater that can be used for simple entities

### Dependency Injection

The integration uses a form of dependency injection, where the concrete implementations of the integration components are specified in the configuration rather than hardcoded in the code. The factory for this is `core.integrations.factories.DataSourceFactory`, which creates the appropriate loaders, transformers, and updaters based on the configuration in `settings.DATA_SOURCES`.

### DATA_SOURCES Format

The `settings.DATA_SOURCES` configuration is a dictionary where:
- Keys are source identifiers (e.g., "pokemon", "ability")
- Values are dictionaries with the following keys:
  - `page_loader`: Configuration for the page loader
    - `class`: The fully qualified class name of the page loader
    - `kwargs`: Additional arguments for the page loader (e.g., the URL)
  - `entity_loader`: Configuration for the entity loader
    - `class`: The fully qualified class name of the entity loader
    - `kwargs`: Additional arguments for the entity loader
  - `transformer`: Configuration for the transformer
    - `class`: The fully qualified class name of the transformer
    - `kwargs`: Additional arguments for the transformer
  - `updater`: Configuration for the updater
    - `class`: The fully qualified class name of the updater
    - `kwargs`: Additional arguments for the updater (e.g., the model name)

### Adding a New Data Source

To add a new data source:

1. Overload or use an existing page loader
2. Overload or use an existing entity loader
3. Create a new transformer by extending `core.integrations.transformers.BaseTransformer`
4. Overload or use an existing updater
5. Add a new record to `settings.DATA_SOURCES` with the appropriate configuration
6. Run the command `python manage.py create_periodic_tasks` to create periodic tasks for the new data source
