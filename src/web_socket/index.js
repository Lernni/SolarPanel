const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { instrument } = require("@socket.io/admin-ui")
const fs = require('fs');
const { default: axios } = require('axios');
require("console-stamp")(console)

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: ["http://localhost:3000", "http://localhost:8080", "https://admin.socket.io/"]
  }
});

if (process.env.NODE_ENV == 'production') {
  axios.defaults.baseURL = "http://solar_module:5001"
} else {
  axios.defaults.baseURL = "http://localhost:5001"
}

// init admin ui panel
instrument(io, { auth: false })

// login credential paths
const LOGIN_CREDENTIALS_APP_PATH = '/data/config/login_credentials.json'
const LOGIN_CREDENTIALS_TEMPLATE_PATH = './login_credentials.template.json'
const HOST_NAME = (process.env.NODE_ENV == 'production') ? 'web_socket' : 'localhost'

// login credentials

if (process.env.NODE_ENV == 'production') {
  try {
    if (!fs.existsSync(LOGIN_CREDENTIALS_APP_PATH)) {
      fs.copyFile(LOGIN_CREDENTIALS_TEMPLATE_PATH, LOGIN_CREDENTIALS_APP_PATH, (error) => {
        if (error) throw error;
      })
    }
  } catch(error) {
    console.log(error)
  }
}

const systemCredentials = require((process.env.NODE_ENV == 'production') ? LOGIN_CREDENTIALS_APP_PATH : LOGIN_CREDENTIALS_TEMPLATE_PATH)

// event handlers
const dashboard = require('./handlers/dashboard')
const browser = require('./handlers/browser')
const settings = require('./handlers/settings')

const handlers =  {
  dashboard, browser, settings
}

io.use((socket, next) => {
  var clientIp = socket.handshake.headers['x-forwarded-for']
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
      var clientIp = socket.handshake.headers['x-forwarded-for']
      var token = socket.handshake.auth.token
      console.log(clientIp + " tries to make a request")

      // disable authorization
      next()

      // if ((clientIp == '127.0.0.1') || (token == systemCredentials.token)) {
      //   next()
      // } else {
      //   console.log(clientIp + " with id " + socket.id + " is not unauthorized")
      //   next(new Error('unauthorized'))
      // }
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

server.listen(4000, HOST_NAME, () => {
  console.log('listening on port 4000');
});