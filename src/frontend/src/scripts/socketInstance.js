import io from 'socket.io-client';

export default io(process.env.VUE_APP_WEB_SOCKET_URL, {
  auth: {
    token: localStorage.getItem('token')
  }
})