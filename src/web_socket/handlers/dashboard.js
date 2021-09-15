const { default: axios } = require('axios');
const auth = require('../auth')

class DashboardHandler {
  constructor() {
    this.timer = null
  }

  init(socket, io) {
    this.socket = socket
    this.io = io
  }

  open() {
    if (auth.isAuthenticated(this.socket)) {
      this.getLatestRecords()
      this.setRefreshInterval()
      console.log("dashboard active")
    } else {
      this.socket.disconnect()
    }
  }

  close() {
    clearInterval(this.timer)
    this.timer = null
  }


  getLatestRecords() {
    axios.get("http://solar_module:5001/latest/60")
    .then((response) => {
        console.log(response.data);
        this.socket.emit("SPARKLINE_RECORDS", response.data);
    })
    .catch((error) => {
        console.log(error);
    });
  }

  setRefreshInterval() {
    this.timer = setInterval(() => {
      axios.get("http://solar_module:5001/latest")
      .then((response) => {
          console.log(response.data);
          this.socket.emit("SPARKLINE_UPDATE", response.data);
      })
      .catch((error) => {
          console.log(error);
      });
    }, 1000)
  }
}

module.exports = DashboardHandler