<template>
  <div class="wrapper h-100">
    <NavBar title="SolarPanel"/>
    <div class="row no-gutters h-100">
      <div class="col-lg-auto order-lg-1 order-sm-2">
        <SideBar/>
      </div>
      <div class="content col-lg order-lg-2 order-sm-1">
        <button @click="sendMessage()">Ping Server</button>
        <router-view/>
      </div>
    </div>
  </div>
</template>

<script>
import SideBar from './components/SideBar.vue'
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  data () {
    return {
      message: 'testtesttest',
      logs: [],
      status: 'disconnected'
    }
  },
  components : {
    SideBar,
    NavBar
  },
  created() {
    this.connect()
  },
  methods: {
    connect() {
      this.socket = new WebSocket('ws://localhost:4000')
      this.socket.onopen = () => {
        this.status = 'connected'
        console.log('WebSocket connected to:', this.socket.url)
        this.logs.push({event: 'WebSocket Connected', data: this.socket.url})
        this.socket.onmessage = ({data}) => {
          this.logs.push({event: 'Recieved message', data})
          console.log('Received:', data)
        }
      }
    },
    disconnect () {
      this.socket.close()
      this.status = 'disconnected'
      this.logs = []
      console.log('WebSocket disconnected')
    },
    sendMessage() {
      // Send message to Websocket echo service
      this.socket.send(this.message)
      this.logs.push({ event: 'Sent message', data: this.message })

      // Log to console and clear input field
      console.log('Sent:', this.message)
      this.message = ''
    }
  }
}
</script>

<style lang="scss">
  html, body, #app {
    height: 100%;
    user-select: none;
  }

  .content {
    height: 90%;
    padding: 15px !important;
  }

  .nav-link {
    font-size: 25px;
  }

  .tab-title {
    display: inline;
    padding-left: 5px;
    vertical-align: middle;
  }

  @media (min-width: 992px) {
    html, body, #app {
      user-select: auto;
    }

    .content {
      height: 100%
    }
  }

</style>
