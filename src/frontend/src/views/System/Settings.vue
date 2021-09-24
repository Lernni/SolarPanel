<template>
  <div class="settings">
    <b-modal disabled v-model="showShutdownModal" title="System herunterfahren" header-bg-variant="danger" header-text-variant="light">
      Soll das System jetzt heruntergefahren werden? Ein Fernzugriff ist dann nicht mehr möglich.

      <template #modal-footer>
        <b-button variant="secondary" @click="showShutdownModal = false">Abbrechen</b-button>
        <b-button variant="danger" @click="shutdownEvent()">
          <b-icon icon="power"></b-icon> Jetzt Herunterfahren
        </b-button>
      </template>
    </b-modal>

    <b-modal disabled v-model="showRestartModal" title="System neustarten" header-bg-variant="danger" header-text-variant="light">
      Soll das System jetzt neugestartet werden? Ein Fernzugriff ist vorrübergehend nicht möglich.

      <template #modal-footer>
        <b-button variant="secondary" @click="showRestartModal = false">Abbrechen</b-button>
        <b-button variant="danger" @click="restartEvent()">
          <b-icon icon="arrow-clockwise"></b-icon> Jetzt Neustarten
        </b-button>
      </template>
    </b-modal>

    <b-row>
      <b-col>
        <b-row class="content justify-content-center">
          <b-col cols="12" lg="10" xl="9">
            <div class="view-anchor" id="recording"><a name="recording"></a></div>
            <h2>Messung</h2>
            <!-- Aufnahme der Messwerte -->
            <b-form-group>
              <b-row align-v="center">
                <b-col>
                  <b-form-checkbox v-model="form.recording" name="check-button" switch size="lg">
                    <h4>Aufnahme der Messwerte</h4>
                  </b-form-checkbox>
                </b-col>
                <b-col cols="12" sm="auto">
                  <h4 class="text-right">
                    <b-badge v-if="settings.recording" variant="danger">
                      <b-icon
                        icon="circle-fill"
                        animation="fade"
                        scale="0.8"
                      ></b-icon>
                      Aktiv
                    </b-badge>
                    <b-badge v-else variant="secondary">
                      Inaktiv
                    </b-badge>
                  </h4>
                </b-col>
              </b-row>
              <p class="text-justify text-muted">
                Regelt die kontinuierliche Erfassung von Messwerten und Berechnung der Kapazität. Bei Pausieren der Aufnahme kann der Ladezustand und die Kapazität nicht
                weiter bestimmt werden. Bleibt die Aufnahme über längeren Nutzungszeitraum inaktiv, sind die errechneten Werte für Ladezustand und Kapazität nicht mehr
                repräsentativ und sollten zurückgesetzt werden.
              </p>
              <b-alert :show="showPauseWarning" variant="warning">
                Durch das Pausieren der Aufnahme werden errechneter Ladezustand und Kapazität weniger repräsentativ!
              </b-alert>
            </b-form-group>

            <hr>
            <div class="view-anchor" id="shunts"><a name="shunts"></a></div>

            <h2>Kalibrierung der Messmodule</h2>

            <!-- Kalibierung der Messwiderstände -->
            <h4>Messwiderstände (Shuntwerte)</h4>
            <p class="text-justify">
              Die beiden Messwiderstände (Shuntwerte) für Eingangs- und Ausgangsstrom können automatisch durch eine Kalibrierung ermittelt oder manuell angepasst werden. 
            </p>

            <b-row>
              <b-col cols="12" sm="6">
                <b-form-group label="Eingangswiderstand">
                  <b-input-group>
                    <b-form-input type="number" v-model="form.input_shunt" :step="form.input_shunt"></b-form-input>

                    <template #append>
                      <b-input-group-text>
                        <katex-element expression="\mu\Omega"/>
                      </b-input-group-text>
                    </template>
                  </b-input-group>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="Ausgangswiderstand">
                  <b-input-group>
                    <b-form-input type="number" v-model="form.output_shunt" :step="form.output_shunt"></b-form-input>

                    <template #append>
                      <b-input-group-text>
                        <katex-element expression="\mu\Omega"/>
                      </b-input-group-text>
                    </template>
                  </b-input-group>
                </b-form-group>
              </b-col>
            </b-row>

            <!-- Kalibierung der maximal zu erwartenden Ströme -->
            <div class="view-anchor" id="max_current"><a name="max_current"></a></div>

            <h4>Maximalströme</h4>
            <p class="text-justify">
              Das Maximum der zu erwartenden Eingangs- bzw. Ausgangsströme hat Einfluss auf die Einrichtung der Messmodule und kann die Genauigkeit der Messung erhöhen. 
            </p>

            <b-row>
              <b-col cols="12" sm="6">
                <b-form-group label="Maximaler Eingangsstrom">
                  <b-input-group>
                    <b-form-input type="number" v-model="form.max_input_current"></b-form-input>

                    <template #append>
                      <b-input-group-text>
                        <katex-element expression="A"/>
                      </b-input-group-text>
                    </template>
                  </b-input-group>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="Maximaler Ausgangsstrom">
                  <b-input-group>
                    <b-form-input type="number" v-model="form.max_output_current"></b-form-input>

                    <template #append>
                      <b-input-group-text>
                        <katex-element expression="A"/>
                      </b-input-group-text>
                    </template>
                  </b-input-group>
                </b-form-group>
              </b-col>
            </b-row>

            <hr>
            <div class="view-anchor" id="system_options"><a name="system_options"></a></div>

            <h2>System</h2>
            <div class="text-center">
              <b-button class="system-button" variant="danger" @click="showShutdownModal = true">
                <b-icon icon="power"></b-icon> Herunterfahren
              </b-button>
              <b-button class="system-button" variant="danger" @click="showRestartModal = true">
                <b-icon icon="arrow-clockwise"></b-icon> Neustarten
              </b-button>
            </div>
            <hr>
          </b-col>
        </b-row>
      </b-col>
      <b-col cols="1" class="scrollbar-box">
        <div class="scrollbar">
          <b-button-group vertical>
            <b-button @click="setAnchor(-1)">
              <b-icon icon="arrow-up"></b-icon>
            </b-button>
            <b-button @click="setAnchor(1)">
              <b-icon icon="arrow-down"></b-icon>
            </b-button>
          </b-button-group>
        </div>
      </b-col>
    </b-row>

    <b-card v-show="showConfirmBox" class="float-bottom">
      <b-button @click="cancelChanges">Abbrechen</b-button>
      <b-button @click="applyChanges" :disabled="submitLoader" class="ml-3" variant="primary">
        <b-spinner v-show="submitLoader" type="grow" small></b-spinner>
        Übernehmen
      </b-button>
    </b-card>
  </div>
</template>

<script>
var _ = require('lodash');

export default {
  name: "Settings",
  data() {
    return {
      form: {},
      settings: {},
      showConfirmBox: false,
      showPauseWarning: false,
      showShutdownModal: false,
      showRestartModal: false,
      submitLoader: false,
      anchorIndex: 0,
      anchors: [],
    }
  },

  mounted() {
    var anchors = document.getElementsByClassName("view-anchor")
    for (var i = 0; i < anchors.length; i++) {
      this.anchors.push(anchors[i].id)
    }

    this.$socket.emit("getSettings", (response) => {
      this.settings = response.settings
      this.form = _.clone(this.settings)
      this.$watch("form", {
        handler() {
          this.showConfirmBox = true
        },
        deep: true
      })
    })
  },

  watch: {
    "form.recording"() {
      if (this.settings.recording && !this.form.recording) {
        this.showPauseWarning = true
      }
    }
  },
  
  methods: {
    restartEvent() {
      this.$socket.emit("restart")
      this.$store.dispatch("logout")
      this.$router.push("/login")
    },

    shutdownEvent() {
      this.$socket.emit("shutdown")
      this.$store.dispatch("logout")
      this.$router.push("/login")
    },

    cancelChanges() {
      this.$router.go()
    },
    
    applyChanges() {
      this.submitLoader = true

      this.$socket.emit("newSettings", this.form, () => {
        this.$router.go()
      })
    },

    setAnchor(nextIndex) {
      if (this.anchorIndex + nextIndex == -1) {
        this.anchorIndex = this.anchors.length - 1
      } else {
        this.anchorIndex = (this.anchorIndex + nextIndex) % this.anchors.length
      }
      location.hash = this.anchors[this.anchorIndex]
    }
  }

}
</script>

<style lang="scss">
.settings {
  margin-bottom: 100px;

  h2, p {
    display: none;
  }

  h4 {
    font-size: 1.3rem;
  }

  .system-button {
    display: block;
    width: 100%;
    margin-bottom: 10px;
  }

  .scrollbar-box {
    display: none;
  }
}

.float-bottom {
  position: sticky !important;
  bottom: 40px;
  left: 0;
  right: 0;
  margin: auto;
  width: 300px;
  text-align: center;
  border: none !important;
  background-color: rgba(255, 255, 255, 0.8) !important;
  z-index: 1000;
}

@media (min-width: 430px) {
  .settings {
    h2, p {
      display: block;
    }

    h4 {
      font-size: 1.5rem;
    }

    .system-button {
      display: inline-block;
      width: auto;
      margin-bottom: 0;

      &:nth-child(2) {
        margin-left: 10px;
      }
    }
  }
}

@media (min-width: 800px) and (max-width: 800px)
  and (min-height: 480px) and (max-height: 480px) {

  .settings {
    .content {
      overflow: hidden;
    }

    .scrollbar-box {
      display: block;
      
      .scrollbar {
        display: flex;
        position: fixed;
        right: 15px;
        height: 49vh;
        z-index: 1000;
      }
    }
  }
}
</style>