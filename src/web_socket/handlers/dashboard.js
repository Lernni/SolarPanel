const { default: axios } = require('axios');

module.exports = (io, socket) => {
  socket.on("getLatestRecords", (callback) => {
    axios.get("/latest/180")
    .then((response) => {
      callback({
        data: response.data
      })
    })
    .catch((error) => {
      console.log(error)
    })
  })
  
  socket.on("getDashboardUpdate", (callback) => {
    axios.get("/dashboard")
    .then((response) => {
      callback({
        data: response.data
      })
    })
    .catch((error) => {
      console.log(error)
    })
  })
}