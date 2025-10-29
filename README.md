[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)


# Ridez

> [!IMPORTANT]
> Not to be used for commercial/public use. As of now, this is only used for personal/business related and will be privated once finished.

## Deploying

TBD

## Developers

### Development environment

1. Create and activate a virtual environment of a supported python version with your tool of choice (e.g pyenv, virtualenv).
2. Install the project dependencies:

    ```sh
    make install-dev
    ```

### Updating requirements

1. If needed, add new optional dependency group/s in `pyproject.toml` (e.g. `optional-dependencies.{group}`)
2. Update/introduce dependencies in `requirements/{group}.in`.
3. Generate new pinned requirements files:

    ```sh
    make update-reqs
    ```

4. Sync dependencies:

    ```sh
    make install-dev
    ```

5. Commit changes.
