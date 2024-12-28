<script setup>
defineOptions({
  name: 'IndexPage'
})

import CalendarEvents from 'src/components/events/CalendarEvents.vue';

import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore();
</script>

<template>
  <q-page padding>
    <h1>Hi, {{ authStore.user.name }}!</h1>
    <CalendarEvents></CalendarEvents>
  </q-page>
</template>