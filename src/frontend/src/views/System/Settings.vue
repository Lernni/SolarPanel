<template>
  <div>
    <b-row class="justify-content-center">
      <b-col cols="6">
        <h2>Messung</h2>
        <!-- Aufnahme der Messwerte -->
        <b-form-group>
          <b-row align-v="center">
            <b-col>
              <b-form-checkbox v-model="checked" name="check-button" switch size="lg">
                <h4>Aufnahme der Messwerte</h4>
              </b-form-checkbox>
            </b-col>
            <b-col cols="auto">
              <h4>
                <b-badge variant="danger" class="text-right">
                  <b-icon
                    icon="circle-fill"
                    animation="fade"
                  ></b-icon>
                  Aktiv
                </b-badge>
              </h4>
            </b-col>
          </b-row>
          <p class="text-justify text-muted">
            Regelt die kontinuierliche Erfassung von Messwerten und Berechnung der Kapazität. Bei Pausieren der Aufnahme kann der Ladezustand und die Kapazität nicht
            weiter bestimmt werden. Bleibt die Aufnahme über längeren Nutzungszeitraum inaktiv, sind die errechneten Werte für Ladezustand und Kapazität nicht mehr
            repräsentativ und sollten zurückgesetzt werden.
          </p>
          <b-alert show variant="warning">
            Durch das Pausieren der Aufnahme werden errechnete Ladezustand und Kapazität weniger repräsentativ!
          </b-alert>
        </b-form-group>

        <h2>Messwiderstände</h2>
        <p class="text-justify">
          Die beiden Messwiderstände (Shuntwerte) für Eingangs- und Ausgangsstrom können automatisch durch eine Kalibrierung ermittelt oder manuell angepasst werden. 
        </p>

        <!-- Kalibierung der Messwiderstände -->
        <h4>Widerstandswerte</h4>
        <b-row>
          <b-col>
            <b-form-group label="Eingangswiderstand">
              <b-input-group>
                <b-form-input type="number"></b-form-input>

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
                <b-form-input tyope="number"></b-form-input>

                <template #append>
                  <b-input-group-text>
                    <katex-element expression="\mu\Omega"/>
                  </b-input-group-text>
                </template>
              </b-input-group>
            </b-form-group>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>