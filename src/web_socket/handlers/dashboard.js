const { default: axios } = require('axios');

module.exports = (io, socket) => {
  socket.on("getLatestRecords", (callback) => {
    axios.get("/latest/180")
    .then((response) => {
      callback({
        records: response.data
      })
    })
    .catch((error) => {
      console.log(error)
    })
  })
  
  socket.on("getLatestRecord", (callback) => {
    axios.get("/latest")
    .then((response) => {
      callback({
        record: response.data
      })
    })
    .catch((error) => {
      console.log(error)
    })
  })
}