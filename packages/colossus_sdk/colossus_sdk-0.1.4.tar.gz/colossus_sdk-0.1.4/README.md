# Colossus Staking Python SDK

Welcome to the Colossus Staking Python SDK - your definitive toolkit for staking and delegation. This SDK provides a streamlined experience for initiating staking flows, handling delegation, and managing signed transactions, ensuring seamless and secure integration to the POS networks.

- [Colossus Staking Python SDK](#colossus-staking-python-sdk)
  - [Build the Colossus SDK Application](#build-the-colossus-sdk-application)
    - [Prerequisites for Colossus SDK](#prerequisites-for-colossus-sdk)
    - [Installing Colossus SDK Dependencies](#installing-colossus-sdk-dependencies)
  - [Running the Colossus SDK Application](#running-the-colossus-sdk-application)
    - [Starting the Colossus API Server](#starting-the-colossus-api-server)
    - [Running SDK `Testing` Tool](#running-sdk-testing-tool)
    - [Understanding SDK Output Data](#understanding-sdk-output-data)
  - [SDK Testing Procedures](#sdk-testing-procedures)
    - [Testing Colossus SDK Server with `curl` Commands](#testing-colossus-sdk-server-with-curl-commands)
    - [Executing Automated Tests for the SDK](#executing-automated-tests-for-the-sdk)
      - [Running a Single Test File](#running-a-single-test-file)
    - [Performing Coverage Analysis for SDK Tests](#performing-coverage-analysis-for-sdk-tests)
    - [Generating Test Coverage Reports for the SDK](#generating-test-coverage-reports-for-the-sdk)
  - [MongoDB Command Reference for Staking Data Management](#mongodb-command-reference-for-staking-data-management)
    - [Accessing and Querying the **Staking Database**](#accessing-and-querying-the-staking-database)
- [Building and Deploying the Colossus SDK](#building-and-deploying-the-colossus-sdk)
  - [Configuring `pyproject.toml` for Colossus SDK](#configuring-pyprojecttoml-for-colossus-sdk)
  - [Building the Colossus SDK Package](#building-the-colossus-sdk-package)
  - [Publishing the Colossus SDK to PyPI](#publishing-the-colossus-sdk-to-pypi)
  - [Version Control Tagging for SDK Releases](#version-control-tagging-for-sdk-releases)
- [Using Poetry's Built-in Authentication:](#using-poetrys-built-in-authentication)
  - [Environment Variables:](#environment-variables)
  - [Keyring Support:](#keyring-support)

---

## Build the Colossus SDK Application

### Prerequisites for Colossus SDK

- **Python**: Version 3.11 or higher.
- **Poetry**: Dependency management tool for [Python](https://python-poetry.org/docs/).

### Installing Colossus SDK Dependencies

Before building the program, ensure you have the following prerequisites:

1. Navigate to the project directory:
   ```bash
   cd colossus_sdk
   ```

2. **Setup Environment**:

   Create a virtual environment and activate it:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```


3. Install the necessary dependencies using Poetry:
   ```bash
   poetry install
   ```

## Running the Colossus SDK Application
### Starting the Colossus API Server

To start the server and import validator keys using mnemonics, use the following command:

```bash
poetry run python colossus_sdk/endpoint_server.py
```

### Running SDK `Testing` Tool
```bash
poetry run python colossus_sdk/tester.py
```

### Understanding SDK Output Data
poetry run python colossus_sdk/tester.py
```bash
Flow ID: ['2d514903-2a09-41d6-938d-65965c0d7507']
Delegated State: delegated
Transaction State: broadcasted
```

## SDK Testing Procedures
### Testing Colossus SDK Server with `curl` Commands

To test the API endpoints, you can use the `curl` command-line tool. Here are some example commands:

1. **Test the Create Staking Flow Endpoint**:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"flow": {"network_code": "cosmos", "chain_code": "testnet", "operation": "staking"}}' \
     http://127.0.0.1:5000/api/v1/flows
   ```

2. **Test the Delegate Endpoint** (Replace `{flow_id}` with the actual flow ID):
   ```bash
   curl -X PUT -H "Content-Type: application/json" \
     -d '{"name": "create_delegate_tx", "inputs": {"delegator_address": "your_address", "validator_address": "validator_address", "amount": 100}}' \
     http://127.0.0.1:5000/api/v1/flows/{flow_id}/next
   ```

3. **Test the Signed Delegate Endpoint** (Replace `{flow_id}` with the actual flow ID):
   ```bash
   curl -X PUT -H "Content-Type: application/json" \
     -d '{"name": "sign_delegate_tx", "inputs": {"transaction_payload": "your_payload"}, "signatures": ["signature1", "signature2"]}' \
     http://127.0.0.1:5000/api/v1/flows/{flow_id}/next
   ```

Replace placeholders like `your_address`, `validator_address`, `your_payload`, etc., with actual values when executing the commands.

---

### Executing Automated Tests for the SDK
To execute your tests, you can use the following command:

```bash
poetry run pytest

# or

poetry run pytest tests/test_colossus_client.py
```

Or, if you are using unittest and your test files are named in the pattern test_*.py, you can use:

```bash
poetry run python -m unittest discover
```

#### Running a Single Test File

To run a specific test file, simply provide the path to the file. For example:

```bash
poetry run pytest tests/test_my_feature.py
```


### Performing Coverage Analysis for SDK Tests
Run tests with coverage using the following command:
```bash
poetry run pytest --cov=colossus_sdk/.
```
### Generating Test Coverage Reports for the SDK

**Terminal Report:**
```bash
poetry run pytest --cov=colossus_sdk/. --cov-report=term
```

**Create HTML Report:**
```bash
poetry run pytest --cov=colossus_sdk/. --cov-report=xml
```

**XML Report:**
```bash
poetry run pytest --cov=your_package_name --cov-report=xml
```

---
## MongoDB Command Reference for Staking Data Management

This section outlines the MongoDB commands used for querying the `staking` database, specifically within the `flows` collection.

### Accessing and Querying the **Staking Database**

First, Start mongo cli:
```bash
./mongosh
```

Switch to the `staking` database:

```bash
use staking
```

**Retrieve and Display All Documents in flows Collection**

This command fetches all documents from the flows collection and displays them in a formatted manner.


```bash
db.flows.find().pretty()
```

**Find a Specific Document by Flow ID**

Replace your_flow_id with the actual ID of the flow you want to query.

```bash
db.flows.find({"flow_id": "your_flow_id"}).pretty()
```

Example using a specific flow ID:
```bash
db.flows.find({"flow_id": "b2c4c9c9-a6ef-46f7-b1a4-e3aebd9ba84b"}).pretty()
```

**Drop the Collection**

Example to drop the flows collection:
```bash
db.flows.drop()
```


---

# Building and Deploying the Colossus SDK
## Configuring `pyproject.toml` for Colossus SDK

Ensure your pyproject.toml file is correctly set up with all necessary information. This includes the package name, version, description, dependencies, and any other relevant metadata. Here's an example template:

```bash
[tool.poetry]
name = "colossus-sdk"
version = "0.1.0"
description = "A Python SDK for interacting with the Colossus API"
authors = ["Your Name <youremail@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"

[tool.poetry.dev-dependencies]
pytest = "^7.4.3"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

## Building the Colossus SDK Package

To build the package, execute the following command:

```bash
poetry build
```

This command will generate a .tar.gz archive and a .whl file in the dist directory.

## Publishing the Colossus SDK to PyPI

To publish your package to PyPI (Python Package Index), create a account on PyPI.

Once the account is created, publish your package using:

```bash
poetry publish
```
This command will prompt you for your PyPI username and password. If you are using a CI/CD pipeline, you can also automate this step using API tokens.

## Version Control Tagging for SDK Releases

After deploying your package, tag the commit and push the tag to your remote repository:

```bash
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```

---

# Using Poetry's Built-in Authentication:

Run `poetry config http-basic.pypi username password` in your terminal.

This command stores your credentials securely in Poetry's configuration.

Replace username and password with your actual PyPI credentials. If you're using a token, your username will be __token__, and your password will be the token value.

## Environment Variables:

You can also set your credentials as environment variables.
For example, `set POETRY_PYPI_TOKEN_PYPI` to your PyPI token.
This is a secure way to handle credentials, especially in CI/CD pipelines.

## Keyring Support:

Poetry can integrate with the system's keyring to store credentials securely.
First, install a keyring backend if you don't have one (like keyring package in Python).
Store your credentials in the keyring, and Poetry will automatically use them when needed.

