import io from 'socket.io-client';

const web_socket_url = (process.env.NODE_ENV == 'production') ? "" : "ws://localhost:4000"

export default io(web_socket_url, {
  auth: {
    token: localStorage.getItem('token')
  }
})