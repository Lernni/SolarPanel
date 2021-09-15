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
  if (credentials.username === "admin" && credentials.password === "admin1234") {
    return {
      success: true,
      token: "adf7g8sdtfgi"
    }
  } else {
    return {
      success: false
    }
  }
}


module.exports = LoginHandler