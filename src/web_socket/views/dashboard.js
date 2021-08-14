const { default: axios } = require('axios');

class Dashboard {
    constructor() {
        this.state = false
        this.timer = null
    }

    set(state, io) {
        if (this.state != state) {
            this.state = state
            this.io = io
            this.setRefreshInterval(state)
            this.getLatestRecords()
        }
    }

    getLatestRecords() {
        axios.get("http://solar_module:5001/latest/60")
        .then((response) => {
            console.log(response.data);
            this.io.emit("SPARKLINE_RECORDS", response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    }

    setRefreshInterval(state) {
        if (state) {
            this.timer = setInterval(() => {
                axios.get("http://solar_module:5001/latest")
                .then((response) => {
                    console.log(response.data);
                    this.io.emit("SPARKLINE_UPDATE", response.data);
                })
                .catch((error) => {
                    console.log(error);
                });
            }, 1000)
        } else {
            clearInterval(this.timer)
            this.timer = null
        } 
    }
}

module.exports = Dashboard