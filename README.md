# fastapi-example

[![container](https://github.com/darioblanco/fastapi-example/actions/workflows/container.yaml/badge.svg)](https://github.com/darioblanco/fastapi-example/actions/workflows/container.yaml)
[![json](https://github.com/darioblanco/fastapi-example/actions/workflows/json.yaml/badge.svg)](https://github.com/darioblanco/fastapi-example/actions/workflows/json.yaml)
[![test](https://github.com/darioblanco/fastapi-example/actions/workflows/test.yaml/badge.svg)](https://github.com/darioblanco/fastapi-example/actions/workflows/test.yaml)
[![validate](https://github.com/darioblanco/fastapi-example/actions/workflows/validate.yaml/badge.svg)](https://github.com/darioblanco/fastapi-example/actions/workflows/validate.yaml)
[![yaml](https://github.com/darioblanco/fastapi-example/actions/workflows/yaml.yaml/badge.svg)](https://github.com/darioblanco/fastapi-example/actions/workflows/yaml.yaml)

This repository is a template to bootstrap a FastAPI service using PostgreSQL.
You can use this repository as an example of how to structure a Standalone API service
implemented with FastAPI and PostgreSQL.

To understand the example data see [DATA.md](./DATA.md).

## Tooling choices

The following development tooling has been chosen:

- `pytest`, `pytest-asyncio` and `pytest-cov` to run tests.
- `isort` and `black` to lint and format code.
- `poetry` to ease dependency management.
- `Containerfile` to build the app either with `podman` or `docker`.
- `docker-compose.yml` to run the app locally with other systems (e.g. postgresql).
- `SQLAlchemy` to perform database queries, and async drivers for `Postgres` and `SQLite`.
- `alembic` for database migrations.
- `prettier` to enforce style in other non-python files, like YAML and JSON.
- GitHub Action `workflows` to run CI tests, reused from [darioblanco/github-workflows](https://github.com/darioblanco/github-workflows).
- `sphinx` and `sphinx-autodoc-typehints` for automatic code documentation.
- [Renovate](https://docs.renovatebot.com/) for automated dependency updates.
- [Kustomize](https://kustomize.io/) for Kubernetes deployments.

## Directory structure

- `.github/`: folder that Github will use to provide its functionality, like CI/CD with its Github actions.
- `app/`: different composable apps to structure our REST application.
- `container/`: files to run the app in containers either with `docker` or `podman`.
- `deploy/`: `kustomize` files and overlays for deploying to `staging` and `production` environments.
- `fixtures/`: fixture data to be loaded to the database.
- `migrations/`: history of database migrations with `alembic`.
- `tests/`: unit and integration tests.
- `.editorconfig`: maintain consistent coding styles with [EditorConfig](https://editorconfig.org/)
- `.gitignore`: specifies intentionally untracked files to ignore in git. See [gitignore](https://git-scm.com/docs/gitignore).
- `.pre-commit-config.yaml`: configuration file to be loaded by [pre-commit](https://pre-commit.com/) for performing checks after every commit.
- `alembic.ini`:
- `Makefile`: helps to install dependencies, run tests, lint files...
- `pyproject.toml`
- `README.md`: this README.
- `renovate.json`: [configuration options](https://docs.renovatebot.com/configuration-options/) for [Renovate](https://docs.renovatebot.com/).
- `server.py`: runs the uvicorn server.

## Install

Before installing this project, you need the following requirements:

- Python 3.11 or superior: e.g. `brew install python3`
- Poetry: e.g. `brew install poetry`
- Prettier: e.g. `brew install prettier`
- Docker Compose (or Podman Compose): alternatively `podman` or `docker`

These essential dependencies are verified by `make init`.

Then you can perform the following commands:

```sh
    # Clone the repository
    git clone git@github.com:darioblanco/fastapi-example.git
    # Change current directory to the cloned repository
    cd fastapi-example
    # Do not forget to configure the local environment variables
    cp .envrc.example .envrc
    # Install production and development requirements (dependencies)
    make install
    # See available make commands
    make help
```

### Dependencies

Dependencies are managed with [poetry](https://github.com/python-poetry/poetry), and are defined
in `pyproject.toml`.

To update a dependency, edit it in `pyproject.toml` or add it via `poetry add mydependency`.

## Code style

The `Makefile` sets two specific targets to lint and format the code:

- `make lint` will check whether the code complies with the coding standards.
- `make format` will reformat the code to make it compliant.

The code compliance rules are defined in the `pyproject.toml` file and they are the standard rules
you can find in many other well maintained open sourced Python projects.

The idea is to write code that is as standard and widely-adopted as possible, so other developers
can get up to speed quickly because they will be already familiarized with that style.

### Pre-commit hooks

Enforcing code standards is something that should always be done at CI level. Nonetheless,
to prevent pushing to the repository and trigger unnecessary CI runs, it is recommended to
do some enforcement at local level.
A way to do that is via [Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

Thankfully, the Python ecosystem has the [pre-commit](https://pre-commit.com/) package
that makes Git hooks trivial.

Run `pre-commit install` to install the project's pre-commit hooks, based on the content
of the file `.pre-commit-config.yaml`.
These hooks use `isort` and `black` to check the code syntax, which is also used by the `Makefile`.

### Relax rules

Sometimes, relaxing rules for a given block of code might be the best way of action, for instance,
when there are long strings or regular literal expressions that may take much more than 80 characters.
Rather than disabling all the rules at once because the code might look ugly in certain isolated cases,
it is better to enclose the code between `#fmt off` and `#fmt on` lines when that happens.

## Environment variables

The application will take environment variables to define its configuration,
and are needed both for running and testing the project.

In a containerized environment (like Kubernetes), the environment variables are passed at deployment
time, usually by a CI/CD pipeline. With this approach, secrets can be loaded universally from any kind
of secret storage solution.

To run the application locally and configure its environment variables (even secrets),
you can copy the `.envrc.example` into an `.envrc` file. This `.envrc` file can contain some secrets but
it must never be pushed to the repo (it is in fact gitignored).

It is recommended to use [direnv](https://direnv.net/) to let it handle loading and unloading
environment variables depending on your `cwd`.

```sh
  # If direnv is installed (e.g. `brew install direnv` in MacOS and `eval "$(direnv hook bash)"` in your bash/zsh profile)
  direnv allow
  # If direnv is not installed
  source .env
```

## Run

To run the server locally:

```sh
  # Run the application (all dependencies are installed and env variables configured)
  make run
```

This will run the postgresql database (if not running already) from its container and
directly start the server in the host with the `server.py` script.
The server script will reload changes in the source files automatically.

To run the server from a container read [Run in a container](#run-in-a-container).

Now the API service should be up and running.
Visit <http://localhost:8100/docs> to get access to the Swagger interface provided with FastAPI.

### Launch directly with uvicorn

You can use `uvicorn` directly in the command line to run the backend with the flag `--reload`,
so that changes in the sources are automatically loaded:

```sh
    uvicorn app.main:app --host localhost --port 8100 --log-level info --reload
```

### Run in a container

Use the `container/docker-compose.yml` file to run the whole project.
It builds the image containing the API service and launches the two docker instances,
one with PostgreSQL and the other with the API service.

The Makefile can build the docker image and run the compose commands:

```sh
    make app-run
```

## Database

To set-up a local PostgreSQL database:

```sh
  # Database that is used when running `make run`
  make db-run
  # Tests use a different database that is automatically created and destroyed
  make db-test-run
```

PostgreSQL will run in the port 5432 and load all the SQL files from `container/dbscripts/*` at creation time.

You can attach to the PostgreSQL database:

```sh
  # Database that is used when running `make run`
  make db-attach
  # Tests use a different database that is automatically created and destroyed
  make db-test-attach
```

This allows to perform further commands in the `psql` interactive client directly in the desired database.

To apply the DB migrations to create the tables, regardless of which database is used:

```sh
    make migrate
```

To populate the target database with some data:

```sh
    make load-fixtures
```

### Bootstrap migrations

This step is not needed, because the `migrations/` directory is already provided.
Only applying the migrations from this repo is required.

The process to set up migrations for scratch is the following:

- Run `alembic init migrations`
- Adapt `alembic.ini` (look for `sqlalchemy.url` and `[post_write_hooks]`). Make them look like the copy in this repository.
- Adapt the file `migrations/env.py` so that it looks like our copy here.
- Create **initial** migration with `alembic revision -m "Empty Init"`. This will add a new file in `migrations/versions/`.
- Apply the initial migration: `alembic upgrade head` (it will create the `alembic_version` table)

### Add a new migration

New migrations are required when new database models (or changes to the current ones) are performed.
Once the new models and tables to the code are added into `models.py` and `dbrel.py`:

- Create the DB migration that will define those changes in the DB: `alembic revision --autogenerate -m "New model."`
- If you use `sqlalchemy_utils` (i.e.: to add `UUID4` field type), then you have to `import sqlalchemy_utils` within the migration python module, otherwise it will fail when upgrading the DB.
- Apply the new migration: `alembic upgrade head` .

## Tests

To run the tests:

```sh
  make test
```

If the environment is not a CI (the `CI` environment variable is not set), the Makefile will
automatically create the test database, run the tests with coverage,
and destroy the test database at the end.

Alternatively, `pytest` can be invoked directly for quick verification of your code. Make sure
that the test database is running when you do.

## Kubernetes

This template offers means to configure Kubernetes readiness and liveness probes:

- **Readiness probe**: exposed by creating a file `/tmp/fastapi-example` at start up time. Only if the file exists the service is ready.
- **Liveness probe**: exposed through the API `/health` route. The service can be considered alive if the end point returns `200` HTTP responses.

## Docs

The `./docs` folder has documentation generated by Sphinx as complementary to the
API documentation that FastAPI automatically generates via Swagger UI or ReDoc.

Whereas the API documentation focuses on the endpoints exposed to users and their
expected inputs/outputs, the code documentation gives developers insight into the
inner workings of the application.

The documentation from the `./docs` folder is bootstrapped in this way
(this is not needed, as it is done already):

```sh
mkdir docs
cd docs
poetry run sphinx-quickstart
```

To update and view the sphinx documentation:

```sh
make docs
open docs/_build/index.html
```

The `.github/workflows/docs.yaml` will automatically generate the documentation and push it
into the `gh-pages` branch. This branch is picked by Github Pages to expose the documentation
to <https://darioblanco.com/fastapi-example/>.

## Secrets

Secrets encryption is done with `Mozilla SOPS` and `age` as its backend, at client level:

- [Using SOPS with age and git like a pro](https://devops.datenkollektiv.de/using-sops-with-age-and-git-like-a-pro.html)
- [Encrypted GitOps secrets with flux and age](https://major.io/p/encrypted-gitops-secrets-with-flux-and-age/)

To be able to decrypt secrets, you need to have a private file per cluster. The private file
has to be stored in `./cluster/{clusterName}/sops.agekey`.

### Generate a private key

Each environment folder in `./deploy/` should have a git ignored `sops.agekey` file,
whose public key is listed in `./.sops.yaml` with a path_regex that involves files
that only belong to that cluster.

In addition, the key used to encrypt that secret should be provisioned in the target Kubernetes
cluster. See the [gitops repository](https://github.com/darioblanco/gitops).

You should have a file there with a format like this:

```sh
$ cat sops.agekey
# created: 2023-07-17T14:07:50+02:00
# public key: age1qvesyd4zyqs5p40n8gr2ngjvsg6surf9e37h3xv7rm7m5lsgz5jsetg3ql
AGE-SECRET-KEY-THIS_IS_A_SECRET_FOR_STAGING_THAT_SHOULD_NEVER_BE_PUSHED
$ cat sops.agekey
# created: 2023-07-17T14:07:50+02:00
# public key: age1g2wjea9r33l6w0kr6g49yh2tgz3mx6l6dt9a8umaf6fzdkgfsemqmrzxxg
AGE-SECRET-KEY-THIS_IS_A_SECRET_FOR_PRODUCTION_THAT_SHOULD_NEVER_BE_PUSHED
```

Normally, you would need to put an `AGE-SECRET-*` value that is shared within your team. The
`sops.agekey` file will never be pushed to the repo as it is git ignored.

### Encrypt secrets

The encrypt command with `sops` is easy because the `.sops.yaml` configuration file already
points to the age public key based on the path of the target file. As the files to be encrypted
are always divided by environment, `sops` know which public key to use thanks to that config.

In addition, the `sops` configuration defines an `encrypted_regex` so it will only encrypt the
`data` and `stringData` attributes, that are only found in Kubernetes secrets. This can be extended
to other secret types if desired.

Therefore, to encrypt a secret resource so it can be pushed to the repo:

```sh
sops -e secret.yaml > secret.enc.yaml
```

Always make sure that the secrets you push to the repo are encrypted!

It is safe to run this command because `secret-values.yaml` are always git ignored.

NOTE: make format has to be run because SOPS create yaml files that do not follow the .editorconfig standard.
You can run it manually or the git hook will.

Alternatively, you can achieve the same (encryption + formatting) through the `encrypt.sh` script:

```sh
$ ./scripts/encrypt.sh secret.yaml
secret.enc.yaml 20ms
✅ Encrypted file saved to secret.enc.yaml
```

### Decrypt Kubernetes secrets

With the environment variables loaded (`source .envrc`), you can decrypt specific attributes from the YAML:

```sh
$ sops -d --extract '["data"]' secret.yaml
foo: ValueThatWasEncrypted
```

Alternatively, you can decrypt and store the decrypted files with this script:

```sh
$ ./scripts/decrypt.sh secret.enc.yaml
✅ Decrypted file saved to secret.yaml
```

### Docker registry credentials

To be able to pull the image from the Github docker registry, a `docker-registry` secret type
has to be created in Kubernetes and linked to the deployment.

The `docker-secret.enc.yaml` is created and encrypted like:

```sh
kubectl create secret docker-registry fastapi-example-docker \
 --dry-run \
 --docker-server=ghcr.io \
 --docker-username=myusername \
 --docker-password=mypassword \
 --namespace=fastapi-example -o yaml > deploy/staging/docker-secret.yaml
./scripts/encrypt.sh deploy/staging/docker-secret.yaml
```
