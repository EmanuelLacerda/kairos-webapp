<script setup>
defineOptions({
  name: 'LoginPage'
})

import FormLogin from 'src/components/auth/FormLogin.vue';
</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <FormLogin></FormLogin>
  </q-page>
</template>