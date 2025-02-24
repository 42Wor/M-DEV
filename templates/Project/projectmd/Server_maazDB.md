# Server_maazDB: Flask SQLite Database Manager and WebSocket Query Server

This project provides two components for interacting with SQLite databases:

1.  **Flask-based Web Application:** A user-friendly web interface for managing SQLite databases, allowing browsing, creation, modification, and data manipulation.
2.  **WebSocket Query Server:** A server that accepts SQL queries over WebSockets, enabling programmatic database interaction.

## Contents

*   [Prerequisites](#prerequisites)
*   [Installation](#installation)
*   [Configuration](#configuration)
    *   [Flask Web Application](#flask-web-application)
    *   [WebSocket Query Server](#websocket-query-server)
*   [Usage](#usage)
    *   [Flask Web Application](#usage-flask-web-application)
    *   [WebSocket Query Server](#usage-websocket-query-server)
    *   [WebSocket Query Server (Improved Version)](#usage-websocket-query-server-improved-version)
*   [Application Routes (Flask)](#application-routes-flask)
*   [Functionality (Flask)](#functionality-flask)
*   [WebSocket Message Format](#websocket-message-format)
    *   [Database Client Interaction Flow](#database-client-interaction-flow)
*   [Error Handling](#error-handling)
*   [Security Considerations](#security-considerations)
*   [Important Notes](#important-notes)
*   [Contributing](#contributing)
*   [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python:** Python 3.7 or higher is recommended.
*   **pip:** The Python package installer (should come with Python).

## Installation

1.  **Clone or Download:** Clone this repository to your local machine.

    ```bash
    git clone <repository_url>
    cd Server_maazDB  # Or the name of your repository directory
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt 
    ```

## Configuration

### Flask Web Application

*   **Database Directory:** The application stores SQLite databases in the directory specified by the `DATABASE_DIR` variable in `app.py`. The default is `databases` within the project directory. **Important:** Ensure this directory exists and is accessible, or modify `DATABASE_DIR` in `app.py` to your desired path.

### WebSocket Query Server

*   **Database Directory:** Similar to the Flask application, the `DATABASE_DIR` variable in your WebSocket server script (`WebSocket_s.py` or `WS_s-v2.py`) specifies the directory containing the SQLite databases. The default is `databases` within the project directory.  Modify `DATABASE_DIR` in the server script if needed.
*   **Port:** Both WebSocket servers listen on port `8080` by default. You can change the `PORT` variable in `WebSocket_s.py` or `WS_s-v2.py`.

## Usage

### Flask Web Application

1.  **Run the Application:**

    ```bash
    python app.py
    ```

2.  **Access the Application:** Open your web browser and navigate to the URL provided by the Flask development server (usually `http://127.0.0.1:5000/`).

3.  **Login:** Log in using a valid API key. You can manage API keys directly in the `auth.db` SQLite database (initially, you might need to add an API key directly to the `api_keys` table using a SQLite browser).

4.  **Manage Databases:** Use the web interface to browse databases, manage tables, insert, edit, and delete data, and execute custom SQL queries.

### WebSocket Query Server

1.  **Run the Server:**

    ```bash
    python WebSocket_s.py 
    ```

2.  **Connect with a WebSocket Client:** Use a WebSocket client to connect to the server at `ws://localhost:8080`.

3.  **Send JSON Messages:** Follow the [WebSocket Message Format](#websocket-message-format) to interact with the database server.

### WebSocket Query Server (Improved Version)

1.  **Run the Improved Server:**

    ```bash
    python WS_s-v2.py
    ```

2.  **Connect with a WebSocket Client:** Use a WebSocket client to connect to the server at `ws://localhost:8080`.

3.  **Authentication and Authorization:**
    *   The improved version uses `permission.db` for user authentication and authorization.
    *   **Before running for the first time:**
        *   Install `bcrypt`: `pip install bcrypt`
        *   Run `WS_s-v2.py` once to create `permission.db` and the `permissions` table if they don't exist.
        *   Populate `permission.db` using a SQLite browser (like DB Browser for SQLite):
            *   Add users to the `permissions` table.
            *   **Important:** Hash passwords using bcrypt before inserting them into the database. You can use a Python script or online bcrypt hash generator.
            *   Define allowed operations (`select`, `insert`, `update`, `delete`) for each user.

4.  **Send Authenticated JSON Messages:** When connecting with a WebSocket client, you'll need to include authentication details (username and password) in your initial JSON messages, as described in the [WebSocket Message Format](#websocket-message-format) documentation (currently not detailed in this README, refer to the code comments in `WS_s-v2.py`).

## Application Routes (Flask)

*   `/`: Databases - Lists available databases.
*   `/login`: Login - Login page for API key authentication.
*   `/logout`: Logout - Logs out the current user.
*   `/database/<db_name>`: Database Home - Displays tables in a database.
*   `/table/<db_name>/<table_name>`: Table Data - Displays data in a table, with options to edit and delete rows.
*   `/create_table/<db_name>`: Create Table - Form to create a new table.
*   `/insert_data/<db_name>/<table_name>`: Insert Data - Form to insert new data into a table.
*   `/update_data/<db_name>/<table_name>`: Update Data - Form to edit existing data in a table (row identified by all column values).
*   `/delete_data/<db_name>/<table_name>`: Delete Data - Handles deletion of a row (identified by all column values).
*   `/create_database`: Create Database - Form to create a new database.
*   `/delete_database/<db_name>`: Delete Database - Handles database deletion.
*   `/delete_table/<db_name>/<table_name>`: Delete Table - Handles table deletion.
*   `/execute_sql/<db_name>`: Execute SQL - Page to execute custom SQL queries directly.

## Functionality (Flask)

*   **Browse Databases:** Lists `.db` files from `DATABASE_DIR`.
*   **View Tables:** `SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';`
*   **View Table Data:** `SELECT * FROM '{table_name}';` and `PRAGMA table_info('{table_name}');`
*   **Create Tables:** `CREATE TABLE '{table_name}' ({column_defs});`
*   **Insert Data:** `INSERT INTO '{table_name}' ({column_names}) VALUES ({placeholders});`
*   **Update Data:** `UPDATE '{table_name}' SET {column_names} WHERE ...` (dynamically generated WHERE clause based on row values)
*   **Delete Data:** `DELETE FROM '{table_name}' WHERE ...` (dynamically generated WHERE clause based on row values)
*   **Create Database:** Creates a new `.db` file.
*   **Execute SQL:** Allows execution of arbitrary SQL queries against the database.

## WebSocket Message Format

### Database Client Interaction Flow

This section describes the communication protocol for interacting with the WebSocket Query Server. The client communicates with the server using JSON messages over the WebSocket connection.

**Step 1: Database Name Transmission**

*   The client initiates communication by sending a JSON message containing the database name to connect to.

    ```json
    {
      "db_name": "example.db"
    }
    ```

**Step 2: Database Existence Check**

*   The server checks if the database exists and responds with a JSON message indicating the status:

    *   **Successful Connection:**

        ```json
        {
          "status": "success",
          "message": "Connected to database example.db"
        }
        ```

    *   **Database Not Found:**

        ```json
        {
          "error": "Database example.db does not exist"
        }
        ```

**Step 3: Query Transmission and Processing (Conditional)**

*   This step is **conditional** and occurs only after successful database connection.
*   The client sends queries as JSON messages, specifying `query_type` ("SELECT", "INSERT", "UPDATE", "DELETE") and the `query` itself. For `INSERT` and `UPDATE`, include `data` as a dictionary of column-value pairs.

    *   **Example SELECT Query:**

        ```json
        {
          "query_type": "SELECT",
          "query": "SELECT * FROM users WHERE name = :name",
          "data": {
            "name": "John Doe"
          }
        }
        ```

    *   **Example INSERT Query:**

        ```json
        {
          "query_type": "INSERT",
          "query": "INSERT INTO users (name, email) VALUES (:name, :email)",
          "data": {
            "name": "Jane Doe",
            "email": "jane.doe@example.com"
          }
        }
        ```

    *   **Example UPDATE Query:**

        ```json
        {
          "query_type": "UPDATE",
          "query": "UPDATE users SET email = :email WHERE name = :name",
          "data": {
            "name": "Jane Doe",
            "email": "jane.newemail@example.com"
          }
        }
        ```

    *   **Example DELETE Query:**

        ```json
        {
          "query_type": "DELETE",
          "query": "DELETE FROM users WHERE name = :name",
          "data": {
            "name": "John Doe"
          }
        }
        ```

*   The server processes the query and sends a JSON response back to the client. The response format may vary based on the `query_type` (e.g., `SELECT` queries will return results as an array of dictionaries).

## Error Handling

*   **Flask:** Error messages are displayed using flash messages in the web interface. Detailed error information is logged. HTTP status codes (e.g., 400, 500) are used to indicate client and server errors.
*   **WebSocket:** The server sends JSON error responses to the client with an `"error"` key. 
    *   Example: `{"error": "Database 'non_existent_db.db' does not exist"}`
    *   Example: `{"error": "Table 'non_existent_table' does not exist in database 'example.db'"}`
    *   Example: `{"error": "Invalid SQL query: near 'FROMM': syntax error", "query": "SELECT * FROMM users"}`
    *   The WebSocket server performs basic SQL syntax validation but relies on SQLite's error reporting for detailed SQL errors.

## Security Considerations

*   **SQL Injection:** 
    *   **Mitigation:** Both the Flask application and WebSocket servers use parameterized queries (with SQLAlchemy in Flask and directly in the WebSocket server code) to prevent SQL injection. User-provided data is passed as parameters, not directly embedded into SQL query strings. This is a **critical** security measure.
    *   **Note:** While parameterized queries greatly reduce SQL injection risk, ensure that you are not constructing any part of the SQL query itself (like table or column names) directly from user input without careful validation.
*   **API Key Authentication (Flask):** The Flask web application uses API key-based authentication to protect access. API keys are stored (hashed - *currently not hashed in the provided code, but should be in a production environment*) in the `auth.db` database.
*   **User Authentication and Authorization (Improved WebSocket Server - `WS_s-v2.py`):** The improved WebSocket server version implements username/password authentication and operation-based authorization using the `permission.db` database and bcrypt for password hashing.
*   **Data Validation:** Input data validation is performed in both components to ensure data integrity and prevent unexpected issues. However, more comprehensive validation may be needed depending on your specific use case.
*   **HTTPS (Flask - Production):** If deploying the Flask application in a production environment, **always use HTTPS** to encrypt communication between the client and server.
*   **WebSocket Security (Production):** For production WebSocket deployments, consider secure WebSocket (WSS) and carefully evaluate network security and access control.

## Important Notes

*   **File Paths:** Double-check database file paths and ensure the Flask application and WebSocket servers have the necessary read/write permissions to the database directory.
*   **Concurrency:** SQLite is file-based and has concurrency limitations, especially for write operations. For high-concurrency applications, consider using a different database system.
*   **Dependencies:** Ensure all dependencies listed in `requirements.txt` are installed in your virtual environment.
*   **API Keys and Passwords:** 
    *   **Security Best Practices:** In a real-world production environment, API keys and especially user passwords should be handled with robust security practices, including proper hashing (bcrypt is used for WebSocket server passwords), secure storage, and potentially more advanced authentication and authorization mechanisms. The current implementation provides basic security but might need enhancement for sensitive deployments.
    *   **Hashing Passwords (WebSocket Server):** Remember to hash passwords using bcrypt *before* storing them in the `permission.db`.  The provided code includes bcrypt hashing for password verification but not for initial password storage in the database.

## Contributing

Contributions are welcome! Please feel free to submit pull requests for bug fixes, improvements, or new features. For major changes, it's recommended to open an issue for discussion first.

## License

[Specify your project license here, e.g., MIT License, Apache 2.0, etc.] 
(If you do not specify a license, the default copyright laws apply.)