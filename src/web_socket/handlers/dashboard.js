const { default: axios } = require('axios');

var timer = []

module.exports = {
  open: (io, socket) => {
    timer[socket.id] = null
    getLatestRecords(socket)
    setRefreshInterval(socket)
  },

  close: (io, socket) => {
    console.log(timer)
    clearInterval(timer[socket.id])
    delete timer[socket.id]
  },
}

const getLatestRecords = (socket) => {
  axios.get("http://solar_module:5001/latest/60")
  .then((response) => {
    console.log(response.data)
    socket.emit("SPARKLINE_RECORDS", response.data)
  })
  .catch((error) => {
    console.log(error)
  })
}

const setRefreshInterval = (socket) => {
  timer[socket.id] = setInterval(() => {
    axios.get("http://solar_module:5001/latest")
    .then((response) => {
      console.log(response.data);
      socket.emit("SPARKLINE_UPDATE", response.data)
    })
    .catch((error) => {
      console.log(error)
    })
  }, 1000)
}