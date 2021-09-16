<template>
  <b-container fluid class="mb-3">
    <b-alert variant="danger" :show="loginState == false">
      Nutzername oder Passwort falsch!
    </b-alert>

    <b-row align-h="center">
      <b-col lg="4">
        <b-card class="login-box" title="Login">
          <b-form @submit="onSubmit" :novalidate="true">
            <b-form-group label="Nutzername" label-for="userInput">
              <b-form-input type="text" id="userInput" v-model.trim="$v.form.username.$model" :state="validateState('username')"></b-form-input>
            </b-form-group>
            <b-form-group label="Passwort" label-for="passwordInput">
              <b-form-input type="password" id="passwordInput" class="mb-2" v-model.trim="$v.form.password.$model" :state="validateState('password')"></b-form-input>
            </b-form-group>
            <b-button class="float-right" type="submit" variant="primary" :disabled="loginLoader">
              <b-spinner v-show="loginLoader" small></b-spinner>
              Anmelden
            </b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { formValidation } from '@/scripts/formValidation'
import { required } from 'vuelidate/lib/validators'

export default {
  name: "Login",
  mixins: [formValidation],
  data() {
    return {
      loginLoader: false,
      loginState: null,

      form: {
        username: null,
        password: null,
      }
    }
  },

  validations: {
    form: {
      username: {
        required
      },
      password: {
        required
      }
    }
  },

  computed: {
    device() {
      return this.$store.state.device
    }
  },

  watch: {
    device: function() {
      if (this.device == 'Internal') {
        this.$router.push('/')
      }
    }
  },

  methods: {
    onSubmit(event) {
      if (this.validateSubmit(event)) this.postLogin()
    },

    postLogin() {
      this.loginLoader = true

      var credentials = {
        username: this.form.username,
        password: this.form.password
      }

      this.$store.dispatch('login', credentials)
      .then(() => this.$router.push('/'))
      .catch(() => {
        this.loginState = false
        this.loginLoader = false
        this.$v.$reset()
      })
    }
  }
}
</script>