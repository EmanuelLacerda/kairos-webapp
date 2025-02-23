<script setup>
defineOptions({
  name: 'FormRegister'
})
const prop = defineProps({
  allFieldsValue: {
    type: Array,
    default: null
  }
})

import { computed } from 'vue';

const areAnyFieldsNotFilledIn = computed(() => !(prop.allFieldsValue === null || prop.allFieldsValue.length === 0) && prop.allFieldsValue.some(field => field === ""))
</script>

<template>
  <q-btn
    :disable="areAnyFieldsNotFilledIn"
  >
    <slot></slot>
  </q-btn>
</template>

<style lang="scss">
</style>
