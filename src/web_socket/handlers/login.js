class LoginHandler {
  constructor() {

  }

  init(socket, io) {
    this.socket = socket
    this.io = io

    socket.on("login", login)
  }
  
  open() {
    console.log("login active")
  }

  close() {

  }
}

const login = function (credentials) {
  if (credentials.username === "admin" && credentials.password === "admin") {
    return {
      token: "adf7g8sdtfgi"
    }
  }
}


module.exports = LoginHandler