<script setup>
defineOptions({
  name: 'LoginPage'
})

import FormLogin from 'src/components/form-auth/FormLogin.vue';
</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <section class="flex justify-center items-center">
      <FormLogin></FormLogin>
    </section>
  </q-page>
</template>