const { default: axios } = require('axios');

module.exports = {

  init: (io, socket) => {
    socket.on("browserRequest", (range, units, interval) => {
      axios.get("http://solar_module:5001/db/records", {
        params: {
          range: range,
          units: units,
          interval: interval
        }
      })
      .then((response) => {
        socket.emit("DB_RECORDS", response.data)
      })
      .catch((error) => {
        console.log(error)
      })
    })
  },
  
  open: (io, socket) => {
    dbEntitiesRange(socket)
  },
}

const dbEntitiesRange = (socket) => {
  axios.get("http://solar_module:5001/db/entities/simple")
  .then((response) => {
    socket.emit("DB_ENTITIES_SIMPLE", response.data)
  })
  .catch((error) => {
    console.log(error)
  })
}