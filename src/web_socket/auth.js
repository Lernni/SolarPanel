module.exports = {
  isAuthenticated(socket) {
    if (getDevice(socket == "Internal")) return true
    return (socket.handshake.headers["token"] == "adf7g8sdtfgi")
  },
  
  getDevice(socket) {
    var address = socket.handshake.headers["x-real-ip"]
    return (address == "127.0.0.1") ? "Internal" : "External"
  }
}
