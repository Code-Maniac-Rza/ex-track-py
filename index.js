const PythonShell = require('python-shell').PythonShell;
const static = require('node-static');
const http = require('http');
const fs = require('fs');
const socketIO = require('socket.io');

// Serve static files
const staticServe = new static.Server('./static');

// Create HTTP server
const server = http.createServer((req, res) => {
    staticServe.serve(req, res);
});

// Attach Socket.IO to the server
const io = socketIO(server);

// Listen for client connections
io.on('connection', (socket) => {
    console.log("Client connected via Socket.IO");

    let pyshell;

    // Function to run Python script
    function runPythonScript() {
        try {
            pyshell = new PythonShell('run.py');

            // Listen for incoming commands from the client
            socket.on('command_entered', (command) => {
                console.log("Received command from client:", command);
                try {
                    pyshell.send(command); // Send command to Python script
                } catch (e) {
                    console.error('Error sending command to Python process:', e);
                }
            });

            // Handle messages from Python script
            pyshell.on('message', (message) => {
                console.log('Python Output:', message);
                socket.emit('console_output', message); // Send Python output to the client
            });

            // Handle errors in the Python process
            pyshell.on('error', (err) => {
                console.error('Python Error:', err);
                socket.emit('console_output', `Error: ${err.traceback || err.message}`);
            });

            // Handle Python process termination
            pyshell.on('close', () => {
                console.log("Python process closed");
            });

        } catch (e) {
            console.error("Error starting Python process:", e);
            socket.emit('console_output', `Error: ${e.message}`);
        }
    }

    // Start the Python script when the client connects
    runPythonScript();

    // Handle client disconnection
    socket.on('disconnect', () => {
        console.log("Client disconnected");
        if (pyshell) {
            try {
                pyshell.kill();
            } catch (e) {
                console.error('Error killing Python process:', e);
            }
        }
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
