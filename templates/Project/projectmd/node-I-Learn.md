## Node.js 

**1. What is Node?**

Node.js is a runtime environment that lets you run JavaScript code *outside* of a web browser.  Think of it as a way to use JavaScript on your server, allowing you to build back-end applications, command-line tools, and more.  Key features:

*   **JavaScript Everywhere:** Uses the same language for both front-end (browser) and back-end (server).
*   **Asynchronous & Non-Blocking:**  Handles multiple tasks efficiently without waiting for one to finish before starting another. This makes it fast.
*   **Event-Driven:**  Reacts to events (like a user clicking a button) to trigger actions.
*   **NPM (Node Package Manager):** Access to a vast library of pre-built modules to add functionality to your projects.

**2. How do you install Node?**

Simple steps:

*   **Download:** Go to the official Node.js website ([https://nodejs.org/](https://nodejs.org/)) and download the installer for your operating system (Windows, macOS, Linux).  Choose the LTS (Long Term Support) version for stability.
*   **Run the Installer:**  Follow the on-screen instructions in the installer.  Make sure to accept the default options, which usually include adding Node.js to your system's PATH.
*   **Verify Installation:** Open your terminal or command prompt and type `node -v`. This should display the version of Node.js that you installed.  Also, type `npm -v` to check the version of npm.

**3. Hello World**

The classic first program:

```javascript
console.log("Hello, World!");
```

To run this:

1.  Save the code above as a file named `hello.js`.
2.  Open your terminal/command prompt.
3.  Navigate to the directory where you saved `hello.js` (using the `cd` command).
4.  Type `node hello.js` and press Enter.  You should see "Hello, World!" printed on your terminal.

**4. Know the Runtime**

Node.js provides a global object called `process` that gives information about the current Node.js process and how it's running. You can use it to:

* Access environment variables (settings specific to your system).
* Control the process execution (exit, handle errors).
* Get information about memory usage.

Example:

```javascript
console.log(process.version); // Shows the Node.js version
console.log(process.platform); // Shows the operating system (e.g., 'win32', 'darwin', 'linux')
```

**5. Events**

Node.js is built around events. An *event* is something that happens in your application (e.g., a file being read, a connection being established).  The `EventEmitter` class is used to create and manage events.

```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const myEmitter = new MyEmitter();

// Attach a listener to the 'event'
myEmitter.on('event', () => {
  console.log('An event occurred!');
});

// Emit the 'event'
myEmitter.emit('event');
```

**6. File System**

The `fs` module allows you to interact with the file system (read, write, create, delete files).

```javascript
const fs = require('fs');

// Read a file asynchronously
fs.readFile('my_file.txt', 'utf8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(data);
});

// Write to a file asynchronously
fs.writeFile('new_file.txt', 'Hello, Node.js!', (err) => {
  if (err) {
    console.error(err);
  } else {
    console.log('File written successfully!');
  }
});
```

**7. Modules**

Modules are reusable blocks of code.  Node.js has built-in modules (like `fs`, `http`) and you can create your own.  NPM packages are also modules.

*   **`require()`:** Used to import modules into your code.
*   **`module.exports`:**  Used to export functions, objects, or variables from a module so they can be used in other files.

Example:

```javascript
// my_module.js
module.exports = {
  greet: (name) => {
    return `Hello, ${name}!`;
  }
};

// app.js
const myModule = require('./my_module'); // relative path to the file

console.log(myModule.greet('Alice')); // Output: Hello, Alice!
```

**8. Build & Deploy**

Building and deploying a Node.js application typically involves:

*   **Bundling (Optional):** Using tools like Webpack or Parcel to combine your JavaScript files and optimize them for production.
*   **Choosing a Deployment Platform:** Common platforms include:
    *   **Cloud Providers:** AWS (Amazon Web Services), Google Cloud Platform (GCP), Azure.
    *   **PaaS (Platform as a Service):** Heroku, DigitalOcean.
    *   **Docker:** Containerize your application for consistent deployment.
*   **Setting up a Process Manager:** Tools like PM2 keep your Node.js application running in the background and automatically restart it if it crashes.

Basic Deployment Steps (example using a platform like Heroku):

1.  **Create a `package.json` file:** Defines your project's dependencies.
2.  **Create a `Procfile`:**  Specifies the command to start your application (e.g., `web: node index.js`).
3.  **Push your code to the platform's repository.**
4.  **Configure the platform (if needed):** Set environment variables, etc.

This is a very high-level overview.  Building and deployment can be quite complex depending on your application's needs.
```

**9. HTTP and Creating a Web Server**

Node.js excels at building web servers. The `http` module provides the functionality to create servers and handle HTTP requests.

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' }); // Set response headers
  res.end('Hello, World from Node.js!\n'); // Send the response
});

const port = 3000; // Choose a port number
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
```

Explanation:

*   `require('http')`: Imports the HTTP module.
*   `http.createServer((req, res) => { ... })`: Creates a new HTTP server.  The function passed to `createServer` is executed for each incoming request.
    *   `req`:  Represents the incoming request (headers, URL, etc.).
    *   `res`: Represents the outgoing response (headers, body).
*   `res.writeHead(200, { 'Content-Type': 'text/plain' })`: Sets the response headers.  `200` is the HTTP status code for "OK".  `Content-Type` tells the client (e.g., browser) what type of data is being sent.
*   `res.end('Hello, World from Node.js!\n')`: Sends the response body and signals the end of the response. The `\n` adds a newline character.
*   `server.listen(port, () => { ... })`: Starts the server and listens for incoming connections on the specified `port`.  The function passed to `listen` is called when the server is ready.

To run this:

1.  Save the code above as `server.js`.
2.  Open your terminal/command prompt.
3.  Navigate to the directory where you saved `server.js`.
4.  Type `node server.js` and press Enter.
5.  Open your web browser and go to `http://localhost:3000/` (or the port you specified).  You should see "Hello, World from Node.js!" displayed in your browser.
```