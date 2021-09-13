const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { instrument } = require("@socket.io/admin-ui")

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: ["https://admin.socket.io/"]
  }
});

// init admin ui panel
instrument(io, { auth: false })


// event handlers
const DashboardHandler = require('./handlers/dashboard');
const BrowserHandler = require('./handlers/browser');

const handlers = {
  dashboard: new DashboardHandler(),
  browser: new BrowserHandler(),
}


// init handlers on connection and on navigation
var currentView = {}

io.on('connection', (socket) => {
  console.log("user " + socket.id + " connected")
  var address = socket.handshake.headers["x-real-ip"];
  console.log('New connection from ' + address);

  var device = "External"
  if (address == "127.0.0.1") device = "Internal"

  socket.emit("DEVICE_DEFINITION", {device: device})

  currentView[socket.id] = null

  for (const [key, value] of Object.entries(handlers)) {
    value.init(io, socket)
  }
    

  socket.on('navigate', (view) => {
    if (currentView[socket.id] !== view) {
      console.log("change view for " + socket.id + " to: " + view)

      if (currentView[socket.id] !== null) currentView[socket.id].close()
      currentView[socket.id] = handlers[view]
      currentView[socket.id].open()
    }
  })

  socket.on('disconnect', () => {
    console.log("user " + socket.id + " disconnected")
    if (currentView[socket.id] !== null) currentView[socket.id].close()
    delete currentView[socket.id]
  })
});


server.listen(4000, 'web_socket', () => {
  console.log('listening on port 4000');
});