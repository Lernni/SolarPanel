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
const dashboard = require('./handlers/dashboard')
const browser = require('./handlers/browser')
const settings = require('./handlers/settings')

const handlers =  {
  dashboard, browser, settings
}

io.use((socket, next) => {
  var clientIp = socket.handshake.headers['x-real-ip']
  socket.emit('DEVICE_DEFINITION', {
    device: (clientIp == '127.0.0.1') ? "Internal" : "External"
  })
  next()
})


io.on('connection', (socket) => {
  for (const [key, value] of Object.entries(handlers)) {
    value(io, socket)
  }

  console.log('a user connected')

  socket.use(([event, ...args], next) => {
    console.log(`event: ${event}`, args)
    
    if (event == 'loginRequest') {
      next() 
    } else {
      var clientIp = socket.handshake.headers['x-real-ip']
      var token = socket.handshake.auth.token
      console.log(clientIp, token)

      if ((clientIp == '127.0.0.1') || (token == 'abcdefg')) {
        next()
      } else {
        console.log('unauthorized')
        next(new Error('unauthorized'))
      }
    }
  })

  socket.on('loginRequest', (credentials, callback) => {
    if (credentials.username === "admin" && credentials.password === "admin1234") {
      callback({
        success: true,
        token: "abcdefg"
      })
    } else {
      callback({
        success: false
      })
    }
  })

  socket.on('disconnect', () => {
    console.log("user " + socket.id + " disconnected")
  })
})

server.listen(4000, 'web_socket', () => {
  console.log('listening on port 4000');
});