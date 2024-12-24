<script setup>
defineOptions({
  name: 'RegisterUserPage'
})

import FormRegister from 'src/components/form-auth/FormRegister.vue';
</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <section class="flex justify-center items-center">
      <FormRegister></FormRegister>
    </section>
  </q-page>
</template>