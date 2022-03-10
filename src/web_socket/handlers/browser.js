const { default: axios } = require('axios');

module.exports = (io, socket) => {
  socket.on("browserRequest", ({start_time, end_time, units}, callback) => {
    axios.get("/db/records", {
      params: {
        start_time, end_time, units
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
  
  socket.on("getDBSections", ({start_time, end_time}, callback) => {
    axios.get("/db/sections", {
      params: {
        start_time, end_time
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
}