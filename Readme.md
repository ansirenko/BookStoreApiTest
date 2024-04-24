# BookStore API Project

## Project Description
This is an API project for an online bookstore that includes functionality for user registration and authentication, book searching, cart management, and the checkout process.

## Project Structure

````
BookStore/
│
├── main.py              - Main API server file.
├── models.py            - Data models used throughout the project.
│
├── test/                - Tests for the API.
│   ├── mocks.py         - Mocks for API testing.
│   ├── test_main.py     - Tests for main API functionalities.
│   └── postman.json     - Postman collection for API testing.
│
├── requirements.txt     - Python requirements.
└── README.md            - Documentation for the project.
````

## Starting the Server
To start the server, run the following command:
```bash:
uvicorn main:app --reload
```

## Starting the Server from Mocks
To start the test server from mocks:
1. Navigate to the mocks directory:
```bash:
cd test
```
2. Start the mock server:
```bash:
uvicorn mocks:app --reload
```

## Running Tests
To run the tests, execute the following command:
```bash:
pytest test_main.py
```

## Running Tests in Postman
1. Import the `postman.json` file into Postman.
2. Before run the tests please start the mock server
3. Select the desired test collection and run it through the Runner.

## CI Integration
To integrate with a CI system (such as Jenkins, GitHub Actions, GitLab CI):
1. Set up steps to install dependencies:
```bash:
pip install -r requirements.txt
```
2. Add steps to run tests:```bash:
```bash:
pytest
```
3. Configure to run Postman tests using Newman:
```bash:
newman run postman.json
```

## Dependencies
To install dependencies, use the `requirements.txt` file, which should include:
- fastapi
- uvicorn
- pytest
- requests (for testing)
- other project-specific dependencies.

