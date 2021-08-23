const { default: axios } = require('axios');

class BrowserHandler {
  constructor() {

  }

  init(socket, io) {
    this.socket = socket
    this.io = io
  }

  open() {
    this.dbEntitiesRange()

    console.log("browser active")
  }

  close() {

  }


  dbEntitiesRange() {
    console.log("getDBEntitiesRange")
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

module.exports = BrowserHandler