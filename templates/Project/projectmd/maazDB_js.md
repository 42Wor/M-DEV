# maazDB_js
# test.js - JavaScript WebSocket Client Testing Script

This `test.js` file is a JavaScript script designed to test a WebSocket client by interacting with a WebSocket server. It uses the `WebSocketClient` class (defined in `client.js`) to connect to a server, send queries, and receive responses.

## Prerequisites

Before running this script, ensure that you have the following prerequisites installed:

*   **Node.js:** You need Node.js to run JavaScript files. You can download it from [https://nodejs.org/](https://nodejs.org/).
*   **ws Library:** This script uses the `ws` library for WebSocket communication. You can install it using npm:

    ```bash
    npm install 
    ```

*   **WebSocket Server:** You need a running WebSocket server that is compatible with the queries sent by this script. Make sure your server is running and listening on the correct port (default: `8080`). The script expects the server to respond with JSON-formatted messages.

## Files

*   **`test.js`:** This file contains the main testing script.
*   **`client.js`:** This file contains the `WebSocketClient` class, which handles the WebSocket connection and communication logic.

## Usage

1.  **Clone or Download:**  Obtain the `test.js` and `client.js` files.
2.  **Install Dependencies:** Navigate to the directory containing the files in your terminal and run:

    ```bash
    npm install
    ```

3.  **Start the Server:**  Ensure that your WebSocket server is running. This script is configured to connect to `ws://localhost:8080` by default.
4.  **Run the Test Script:**  In your terminal, execute the following command:

    ```bash
    node test.js
    ```

## Configuration

*   **WebSocket URI:** The WebSocket URI is defined in the `test.js` file. You can modify this to point to your server's address:

    ```javascript
    const client = new WebSocketClient('ws://localhost:8080'); // Modify this URI
    ```

*   **Database Name:** The database name is passed to the `selectData` and `insertData` methods. Modify this value in `test.js` according to your server's requirements.

    ```javascript
    const dbName = 'mydatabase.db';  // Modify this database name
    ```

## Output

The script will print the following output to the console:

*   `Connected to WebSocket server.` - Indicates a successful connection to the server.
*   `SELECT result: [ ... ]` - The results of the SELECT query, formatted as a JSON array.
*   `INSERT result: { ... }` - The result of the INSERT query, formatted as a JSON object. The response should contain details about the success or failure of the query.

If any errors occur during the process, they will be printed to the console with descriptive error messages.

## Error Handling

The script includes basic error handling to catch common problems, such as:

*   `WebSocket is not a constructor`: This indicates an issue with the `require` statement or the `ws` library.
*   `WebSocket connection is now open. Proceeding with queries.`: Shows if the connection is established.
*   Errors received from the server: The server might send error messages in JSON format if there are issues with the query (e.g., SQL syntax errors, database connection problems).  The client will print these errors to the console.

## Important Notes

*   **Server-Side Implementation:**  This script assumes that the server is implemented correctly and follows a specific protocol for handling queries and returning results in JSON format.
*   **Database Setup:** The database and the `users` table with the correct schema are presumed to exist on the server-side.
*   **Security:** For production environments, ensure that the WebSocket communication is secured using WSS (WebSocket Secure) and that appropriate authentication and authorization mechanisms are in place on the server-side.
