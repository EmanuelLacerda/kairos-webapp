<script setup>
defineOptions({
  name: 'RegisterUserPage'
})

import FormRegister from 'src/components/auth/FormRegister.vue';

</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <FormRegister></FormRegister>
  </q-page>
</template>