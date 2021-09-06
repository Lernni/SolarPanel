const { default: axios } = require('axios');

class BrowserHandler {
  constructor() {

  }

  init(io, socket) {
    this.socket = socket
    this.io = io

    socket.on("browserRequest", browserRequest)
  }

  open() {
    this.dbEntitiesRange()

    console.log("browser active")
  }

  close() {

  }

  // from websocket -> to frontend

  dbEntitiesRange() {
    axios.get("http://solar_module:5001/db/entities/simple")
    .then((response) => {
      this.socket.emit("DB_ENTITIES_SIMPLE", response.data);
    })
    .catch((error) => {
      console.log(error);
    });
  }

}

// from frontend -> to websocket

const browserRequest = function (range, units, interval) {
  const socket = this

  axios.get("http://solar_module:5001/db/records", {
    params: {
      range: range,
      units: units,
      interval: interval
    }
  })
  .then((response) => {
    socket.emit("DB_RECORDS", response.data);
  })
  .catch((error) => {
    console.log(error);
  });
}

module.exports = BrowserHandler