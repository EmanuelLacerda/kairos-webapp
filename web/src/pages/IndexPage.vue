<script setup>
defineOptions({
  name: 'IndexPage'
})

import CalendarEvents from 'src/components/events/CalendarEvents.vue';
</script>

<template>
  <q-page padding>
    <CalendarEvents></CalendarEvents>
  </q-page>
</template>