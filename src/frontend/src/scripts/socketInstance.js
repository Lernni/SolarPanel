import io from 'socket.io-client';

export default io({
  auth: {
    token: localStorage.getItem('token')
  }
})