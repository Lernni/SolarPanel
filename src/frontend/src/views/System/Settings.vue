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

    <b-row class="justify-content-center">
      <b-col cols="12" lg="10" xl="9">
        <h2>Messung</h2>
        <!-- Aufnahme der Messwerte -->
        <b-form-group>
          <b-row align-v="center">
            <b-col>
              <b-form-checkbox v-model="form.recording" name="check-button" switch size="lg">
                <h4>Aufnahme der Messwerte</h4>
              </b-form-checkbox>
            </b-col>
            <b-col cols="auto">
              <h4>
                <b-badge v-if="settings.recording" variant="danger" class="text-right">
                  <b-icon
                    icon="circle-fill"
                    animation="fade"
                    scale="0.8"
                  ></b-icon>
                  Aktiv
                </b-badge>
                <b-badge v-else variant="secondary" class="text-right">
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

        <h2>Kalibrierung der Messmodule</h2>

        <!-- Kalibierung der Messwiderstände -->
        <h4>Messwiderstände (Shuntwerte)</h4>
        <p class="text-justify">
          Die beiden Messwiderstände (Shuntwerte) für Eingangs- und Ausgangsstrom können automatisch durch eine Kalibrierung ermittelt oder manuell angepasst werden. 
        </p>

        <b-row>
          <b-col>
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
        <h4>Maximalströme</h4>
        <p class="text-justify">
          Das Maximum der zu erwartenden Eingangs- bzw. Ausgangsströme hat Einfluss auf die Einrichtung der Messmodule und kann die Genauigkeit der Messung erhöhen. 
        </p>

        <b-row>
          <b-col>
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

        <h2>System</h2>
        <div class="text-center">
          <b-button variant="danger" @click="showShutdownModal = true">
            <b-icon icon="power"></b-icon> Herunterfahren
          </b-button>
          <b-button class="ml-3" variant="danger" @click="showRestartModal = true">
            <b-icon icon="arrow-clockwise"></b-icon> Neustarten
          </b-button>
        </div>
        <hr>
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
    }
  },

  mounted() {
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
    }
  }

}
</script>

<style scoped>
.settings {
  margin-bottom: 100px;
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
</style>