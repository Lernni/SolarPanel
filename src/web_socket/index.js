const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);

const { Server } = require('socket.io');
const io = new Server(server);

const views = require('./view');

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('navigate', function(data) {
    console.log("change view to: " + data);
    views.changeView(data, io);
  });

  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

server.listen(4000, 'web_socket', () => {
  console.log('listening on port 4000');
});