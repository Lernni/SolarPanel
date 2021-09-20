<template>
  <b-tab :active="active" :disabled="disabled" :title-item-class="done ? 'variant-success' : ''">
    <template #title>
      <b-row>
        <b-col cols="auto" class="pr-0 d-flex align-items-center">
          <b-icon-check-circle v-show="done"></b-icon-check-circle>
          <b-icon-circle v-show="!done"></b-icon-circle>
        </b-col>
        <b-col>
          <div class="text-center">
            <h5>{{ caption }}</h5>
            <slot name="tab-content"></slot>
          </div>
        </b-col>
      </b-row>
    </template>
    <b-card-text>
      <slot></slot>
    </b-card-text>
  </b-tab>
</template>

<script>
export default {
  name: 'PillTab',
  props: ["caption", "active", "disabled", "done"]
}
</script>

<style scoped>
  .variant-success > .active {
    background-color: var(--success) !important;
    color: white;
  }

  .variant-success > :not(.active) {
    color: var(--success) !important;
  }
</style>