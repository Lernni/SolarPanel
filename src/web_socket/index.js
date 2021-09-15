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

const auth = require('./auth');

// event handlers
const DashboardHandler = require('./handlers/dashboard');
const BrowserHandler = require('./handlers/browser');
const LoginHandler = require('./handlers/login');

const handlers = {
  dashboard: new DashboardHandler(),
  browser: new BrowserHandler(),
  login: new LoginHandler()
}


// init handlers on connection and on navigation
var currentView = {}

io.on('connection', (socket) => {
  console.log("user " + socket.id + " connected")

  socket.emit("DEVICE_DEFINITION", {device: auth.getDevice(socket)})
  
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