class Settings {
    constructor() {
        this.state = false
    }

    set(state, io) {
        if (this.state != state) {
            console.log("settings active")
        }
    }
}

module.exports = Settings