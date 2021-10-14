const { default: axios } = require('axios');

module.exports = (io, socket) => {
  socket.on("browserRequest", (range, units, interval, callback) => {
    axios.get("/db/records", {
      params: {
        range: range,
        units: units,
        interval: interval
      }
    })
    .then((response) => {
      callback({
        data: response.data
      })
    })
    .catch((error) => {
      console.log(error)
    })
  })
  
  socket.on("getDBEntities", (callback) => {
    axios.get("/db/entities/simple")
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