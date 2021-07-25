const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);

const { Server } = require('socket.io');
const io = new Server(server);

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('testEvent', function(data) {
    console.log('received: %s', JSON.stringify(data));
    io.emit('updateTest', data);
  });

  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

server.listen(4000, 'web_socket', () => {
  console.log('listening on port 4000');
});