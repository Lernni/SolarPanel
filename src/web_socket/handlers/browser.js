const { default: axios } = require('axios');

module.exports = (io, socket) => {
  socket.on("browserRequest", ({start_time, end_time, units}, callback) => {
    axios.get("/db/records", {
      headers: {
        "Content-Type": "application/json"
      },
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
}