import { io } from 'socket.io-client'

export const useSocketIO = () => {
  const webSocketURL = process.env.NODE_ENV == 'production' ? '' : 'ws://localhost:4000'
  const socket = io(webSocketURL)

  socket.on('connect', () => {
    console.log('user ' + socket.id + ' connected')
  })

  socket.on('disconnect', () => {
    console.log('user ' + socket.id + ' disconnected')
  })

  return socket
}
