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
      console.log(response.data)
      this.socket.emit("DB_ENTITIES_SIMPLE", response.data);
    })
    .catch((error) => {
      console.log(error);
    });
  }

}

// from frontend -> to websocket

const browserRequest = function (range, units) {
  const socket = this

  axios.get("http://solar_module:5001/db/records", {
    params: {
      range: range,
      units: units
    }
  })
  .then((response) => {
    console.log(response.data)
    socket.emit("DB_RECORDS", response.data);
  })
  .catch((error) => {
    console.log(error);
  });
}

module.exports = BrowserHandler