module.exports = {
  root: true,
  parser: 'vue-eslint-parser',
  env: {
    es6: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:import/recommended',
    'plugin:vue/vue3-recommended',
    'plugin:tailwindcss/recommended',
    'plugin:prettier/recommended',
  ],
  globals: {
    defineProps: 'readonly',
  },
  rules: {
    'tailwindcss/no-custom-classname': 'off',
    'vue/multi-word-component-names': 'off',
    'no-multiple-empty-lines': [2, { max: 3 }],
  },
  settings: {
    'import/resolver': {
      alias: {
        map: [['@', './src']],
      },
    },
  },
}
