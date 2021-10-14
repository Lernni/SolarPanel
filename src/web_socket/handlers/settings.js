const { default: axios } = require('axios');

module.exports = (io, socket) => {
  socket.on("restart", () => {
    axios.post("/system/restart")
  })

  socket.on("shutdown", () => {
    axios.post("/system/shutdown")
  })

  socket.on("newSettings", (settings, callback) => {
    axios.post("/system/settings", settings)
    .then(() => {
      callback()
    })
    .catch((error) => {
      console.log(error)
      callback()
    })
  })
  
  socket.on("getSettings", (callback) => {
    axios.get("/system/settings")
    .then((response) => {
      callback({
        settings: response.data
      })
    })
    .catch((error) => {
      console.log(error)
    })
  })
}