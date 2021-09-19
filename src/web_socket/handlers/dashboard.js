const { default: axios } = require('axios');

module.exports = (io, socket) => {
  socket.on("getLatestRecords", (callback) => {
    axios.get("http://solar_module:5001/latest/60")
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
    axios.get("http://solar_module:5001/latest")
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