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
*   [Application Routes (Flask)](#application-routes-flask)
*   [Functionality (Flask)](#functionality-flask)
*   [WebSocket Message Format](#websocket-message-format)
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
    pip install -r requirements.txt # Install from a requirements file (preferred)
    # OR
    pip install Flask SQLAlchemy websockets
    ```

    **Note:** Create a `requirements.txt` file in your project root directory. This file should list all the Python packages your project depends on, making it easy for others to install them.  Example content:

    ```
    Flask
    SQLAlchemy
    websockets
    ```

## Configuration

### Flask Web Application

*   **Database Directory:** The application stores SQLite databases in the directory specified by the `DATABASE_DIR` variable in your Python code (e.g., `app.py` or `main.py`). The default is `/home/mm/Desktop/maazDB-test_GO/DBMS_MAAZDB/sqlite_manager/databases`.  **Important:** Ensure this directory exists and is accessible.

### WebSocket Query Server

*   **Database Directory:** Similar to the Flask application, the `DATABASE_DIR` variable in your WebSocket server script specifies the directory containing the SQLite databases.  The default is `/home/mm/Desktop/maazDB-test_GO/DBMS_MAAZDB/sqlite_manager/databases`.
*   **Port:** The server listens on port `8080` by default. You can change this in your script.

## Usage

### Flask Web Application

1.  **Run the Application:**

    ```bash
    python app.py  # Replace with the actual name of your Python file (e.g., app.py)
    ```

2.  **Access the Application:** Open your web browser and navigate to the URL provided by the Flask development server (usually `http://127.0.0.1:5000/`).

3.  **Manage Databases:** Use the web interface to browse, create, and manage your SQLite databases and tables.

### WebSocket Query Server

1.  **Run the Server:**

    ```bash
    python WebSocket_s.py  # Replace with the actual name of your Python file (e.g., server.py)
    ```

2.  **Connect with a WebSocket Client:** Use a WebSocket client to connect to the server at `ws://localhost:8080`.

## Application Routes (Flask)

*   `/`: Displays a list of available databases.
*   `/database/<db_name>`: Displays the tables in the specified database.
*   `/table/<db_name>/<table_name>`: Displays the data in the specified table.
*   `/create_table/<db_name>`: Allows you to create a new table in the specified database.
*   `/insert_data/<db_name>/<table_name>`: Allows you to insert new data into the specified table.
*   `/update_data/<db_name>/<table_name>/<int:id_value>`: Allows you to update data in the specified table for a specific ID.
*   `/create_database`: Allows you to create a new SQLite database.

## Functionality (Flask)

*   **Browse Databases:** Lists `.db` files from `DATABASE_DIR`.
*   **View Tables:** `SELECT name FROM sqlite_master WHERE type='table';`
*   **View Table Data:** `SELECT * FROM '{table_name}';` and `PRAGMA table_info('{table_name}');`
*   **Create Tables:** `CREATE TABLE '{table_name}' ({column_defs});`
*   **Insert Data:** `INSERT INTO '{table_name}' ({column_names}) VALUES ({placeholders});`
*   **Update Data:** `UPDATE '{table_name}' SET {column_names} WHERE id = :id`
*   **Create Database:** Creates a new `.db` file.

## WebSocket Message Format

### Database Client Interaction Flow

This section describes the communication protocol for interacting with the WebSocket Query Server.  The client communicates with the server using JSON messages over the WebSocket connection.

**Step 1: Database Name Transmission**

*   The client initiates the communication by sending a JSON message containing the database name to check if the database exists.

    ```json
    {
      "db_name": "example.db"
    }
    ```

**Step 2: Database Existence Check**

*   The server receives the database name and checks if the database exists.
*   The server then responds with a JSON message indicating the status:

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

*   This step occurs **only if** the server successfully connects to the database (as indicated by the `"status": "success"` response in Step 2).
*   The client sends queries to the server as JSON messages. The `query_type` field specifies the type of query (e.g., "SELECT", "INSERT").

    *   **Example SELECT Query:**

        ```json
        {
          "query_type": "SELECT",
          "query": "SELECT * FROM users;"
        }
        ```

    *   **Example INSERT Query (with data):**

        ```json
        {
          "query_type": "INSERT",
          "query": "INSERT INTO users (name, email) VALUES (:name, :email)",
          "data": {
            "name": "John Doe",
            "email": "john.doe@example.com"
          }
        }
        ```

*   The server processes the query and returns an appropriate response (not explicitly defined here but would typically include success/failure indicators and potentially result data.  The exact format of the response will depend on the query).

**Summary**

1.  **Client Sends Database Name:** Client transmits the `db_name` to initiate the connection and database selection.
2.  **Server Checks Database:** Server verifies the existence of the database and responds with a success or error message.
3.  **Client Sends Queries:** If the database exists, the client can send `SELECT`, `INSERT`, or other SQL queries to the server for data manipulation. The server will process these queries.

## Error Handling

(Describe how errors are handled in both the Flask application and the WebSocket server.  Include examples of potential error messages and how to interpret them.)

For example:

*   **Flask:**  Error messages are displayed in the web interface.  HTTP status codes are used to indicate errors (e.g., 404 for "Not Found," 500 for "Internal Server Error").
*   **WebSocket:**  Error messages are sent back to the client as JSON payloads with an `"error"` key.  Example: `{"error": "Invalid SQL syntax"}`.  Include details of how the server validates the SQL syntax.

## Security Considerations

*   **SQL Injection:**  The WebSocket server must be carefully designed to prevent SQL injection vulnerabilities.  *Parameterized queries or prepared statements should always be used* when handling user-provided data in SQL queries.  Explain how you are mitigating SQL injection in your code.  This is *critical*.
*   **Access Control:** Consider implementing access controls to restrict which clients can connect to the WebSocket server and which databases they can access.
*   **Data Validation:**  Validate all input data to prevent unexpected behavior or security vulnerabilities.
*   **Flask Security:**  Use appropriate Flask security measures, such as HTTPS and proper authentication, if exposing the web application to a public network.

## Important Notes

*   **File Paths:**  Be mindful of file paths and permissions when working with SQLite databases.
*   **Concurrency:**  SQLite has limitations with concurrency.  Consider these limitations if your application requires high concurrency.
*   **Dependencies:** Ensure that all required dependencies are installed correctly.

## Contributing

(Explain how others can contribute to the project.)

## License

(Specify the license under which the project is released.)