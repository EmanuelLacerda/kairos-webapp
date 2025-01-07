<script setup>
defineOptions({
  name: 'IndexPage'
})

import CalendarEvents from 'src/components/events/CalendarEvents.vue';
</script>

<template>
  <q-page padding>
    <section class="flex justify-center">
      <h1 style="margin-top: 30px; font-weight: 600; color: #333;">Minha Agenda</h1>
    </section>
    <CalendarEvents></CalendarEvents>
  </q-page>
</template>