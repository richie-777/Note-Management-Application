# Note Management API

This is a Flask-based API for managing notes and users in a simple note-taking application. It provides endpoints for user registration, login, note creation, updating notes, sharing notes with other users, retrieving note version history, and deleting notes.

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/richie-777/Note-Taking-Application/blob/main/app.py
    ```

2. Navigate to the project directory:
    ```bash
    cd Note Management Application
    ```

3. Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    python app.py
    ```

The application should now be running on `http://localhost:5000`.

## Usage

1. Use a tool like Postman to interact with the API endpoints.
2. Register a new user using the `/signup` endpoint.
3. Log in with the registered user credentials using the `/login` endpoint to obtain a user token.
4. Use the obtained token for authentication in subsequent requests by including it in the Authorization header.
5. Use the provided endpoints to create, update, share, retrieve, and delete notes as needed.

## API Endpoints

- `/signup` (POST): Register a new user.
- `/login` (POST): Log in with existing user credentials.
- `/notes/create` (POST): Create a new note.
- `/notes/<id>` (PUT): Update an existing note.
- `/notes/<id>` (GET): Retrieve a specific note.
- `/notes/share` (POST): Share a note with other users.
- `/notes/version-history/<id>` (GET): Get the version history of a note.
- `/notes/<id>` (DELETE): Delete a note.

Refer to the API documentation or source code comments for detailed usage instructions and endpoint specifications.


## Unit Testing

The project includes unit tests to ensure the correctness of API endpoints. The unit_testing.py file contains test cases for each endpoint. To run the unit tests:

```bash
python -m unittest unit_test.py
```

The unit tests use the unittest library in Python and simulate HTTP requests to each endpoint. The tests cover various scenarios, including positive cases, error handling, and edge cases.

## Deployment

This project is deployed here. click on the link to check this.
https://richie777.pythonanywhere.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
