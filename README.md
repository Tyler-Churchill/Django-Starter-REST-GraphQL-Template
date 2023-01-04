# Headless Django Server Application

A starter project for a headless REST/GraphQL API powered by Django

## Technologies

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Local Development

## Requirements
1. Editor of choice (VSCode, Pycharm)
2. Docker for Desktop (With appropriate licence)


# VSCode

1. Clone project
2. Open project in VSCode, you should be prompted to install the recommened VSCode extensions automatically
3. You will be prompted that this project is setup for "Dev Containers"
4. Click Open Dev Container from the prompt
5. After a short while, you will have a terminal and the full project running locally
6. You will have to apply migations to your database, run `migrate` in the terminal
7. run `start` in your terminal to start the backend service or use the editor built in run configuration for debugging
8. Navigate to `http://127.0.0.1:8000/api/schema/redoc/` or `http://127.0.0.1:8000/api/schema/swagger-ui/` to view API docs


# Unix/Linux/Windows - Any Code Editor

1. `make start` Starts the full project and related services in docker
2. In a new terminal/side by side, `make shell` will give you a shell dev environment for running commands against the running application
3. Inside the shell created by `make shell`, run `migrate` to ensure your database is up to date.


# Troubleshooting
1. WARNING: `You have X unapplied migration(s).`
*  Run `migrate` in the development shell

# Workflow Guides

While in the local development shell (run `make shell`)

1. **Adding New Dependencies**
   * `add DEPNAME`
   * `add --help`
   *  alias for `poetry add`*
2. **Generating Migration Files**
   * `poetry run python manage.py makemigrations`
3. **Applying Migrations**
   * `migrate` 
    * *alias for `poetry run python manage.py migrate`*


# Testing


## Philosophy
> Write tests. Not too many. Mostly integration.
> https://kentcdodds.com/blog/write-tests

Use the `GIVEN-WHEN-THEN` style of representing tests in order to 
encourage [behavior-driven development][givenwhenthen importance].

TDD/BDD can be used but specific python toolings for gherkin/cucumber have been omitted for you to add if needed.

## Testing Structure
* Tests are added in the `/tests/*` root folder
* Add your test to the specific app folder and organize them by `integration/` or `unit/` 

## Factories

[FactoryBoy][factoryboy] is used to [simplify testing][factory method benefits].


## Writing a Test

### Naming
Test cases should follow the following pattern:
 
`test_[given]__[when]__[then]`

*Examples:*
```
test_product_has_been_purchased__delete_product__rejected
```

### Structure
Just like good code, good tests should be self-documenting.
Tests should have easy-to-read sections of setup (GIVEN), action (WHEN), expected result (THEN)

```
# GIVEN
...

# WHEN
...

# THEN
...
```

## Running Tests
`poetry run pytest`

### Running Tests in Parallel
`poetry run pytest -n auto`


# Future Considerations
* update `settings.py` file structure for `common_settings.py`, `testing_settings.py`, so on
* Rework dockerfile to be multi-stage dev/prod
* Add Redis to dev image/update django cache backend
* add pre-commit linting for commit messages
* use `bumpversion` for version managment if desired
* add specific CI config for running tests

[givenwhenthen importance]: https://solidsoft.wordpress.com/2017/05/16/importance-of-given-when-then-in-unit-tests-and-tdd/
[factoryboy]: http://factoryboy.readthedocs.io/en/latest/orms.html
[factory method benefits]: http://defragdev.com/blog/?p=726