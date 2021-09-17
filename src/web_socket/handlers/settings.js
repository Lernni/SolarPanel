const { default: axios } = require('axios');

module.exports = {
  init: (io, socket) => {
    socket.on("restart", () => {
      axios.post("http://solar_module:5001/system/restart")
    })

    socket.on("shutdown", () => {
      axios.post("http://solar_module:5001/system/shutdown")
    })

    socket.on("newSettings", (settings, callback) => {
      axios.post("http://solar_module:5001/system/settings", settings)
      .then(() => {
        callback()
      })
      .catch((error) => {
        console.log(error)
        callback()
      })
    })
  },

  open: (io, socket) => {
    getSettings(socket)
  }
}

const getSettings = (socket) => {
  axios.get("http://solar_module:5001/system/settings")
  .then((response) => {
    socket.emit("SETTINGS_UPDATE", response.data)
  })
  .catch((error) => {
    console.log(error)
  })
}