<script setup>
defineOptions({
  name: 'IndexPage'
})

import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore();
</script>

<template>
  <q-page padding>
    <h1>Hi, {{ authStore.user.name }}!</h1>
  </q-page>
</template>