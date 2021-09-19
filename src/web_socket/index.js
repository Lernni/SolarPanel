const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { instrument } = require("@socket.io/admin-ui")
const fs = require('fs');
require("console-stamp")(console)

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: ["https://admin.socket.io/"]
  }
});

// init admin ui panel
instrument(io, { auth: false })

// login credentials
try {
  if (!fs.existsSync('/data/config/login_credentials.json')) {
    fs.copyFile('./login_credentials.template.json', '/data/config/login_credentials.json', (error) => {
      if (error) throw error;
    })
  }
} catch(error) {
  console.log(error)
}

const systemCredentials = require('/data/config/login_credentials.json')

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

  console.log('user ' + socket.id + ' connected')

  socket.use(([event, ...args], next) => {
    console.log(`event: ${event}`, args)
    
    if (event == 'loginRequest') {
      next() 
    } else {
      var clientIp = socket.handshake.headers['x-real-ip']
      var token = socket.handshake.auth.token
      console.log(clientIp + " tries to make a request")

      if ((clientIp == '127.0.0.1') || (token == systemCredentials.token)) {
        next()
      } else {
        console.log(clientIp + " with id " + socket.id + " is not unauthorized")
        next(new Error('unauthorized'))
      }
    }
  })

  socket.on('loginRequest', (credentials, callback) => {
    if (credentials.username === systemCredentials.username
      && credentials.password === systemCredentials.password) {
      callback({
        success: true,
        token: systemCredentials.token
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