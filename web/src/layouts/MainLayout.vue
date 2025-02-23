<script setup>
import { ref } from 'vue'

import EssentialLink from 'components/EssentialLink.vue'
import ButtonLogout from 'src/components/auth/ButtonLogout.vue';

import { useAuthStore } from 'src/stores/auth';


const authStore = useAuthStore()


const linksList = [
  {
    title: 'Minha Agenda',
    icon: 'bi bi-calendar-date',
    route: { name: "home" },
  }
]

const leftDrawerOpen = ref(false)


function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>

<template>
  <q-layout view="hHh Lpr lFf" class="main-layout">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Kairos WebApp
        </q-toolbar-title>

        <div class="welcome-message">Oi, {{ authStore.user.name }}</div>
        <ButtonLogout v-if="authStore.isAuthenticated"></ButtonLogout>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container class="page-background">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style lang="scss">
  .main-layout{
    .q-header{
      background-color: $custom-blue-3;

      .welcome-message{
        margin-right: 10px;
      }
    }
    .q-drawer{
      background-color: $custom-blue-3;
      padding-top: 20px;
    }
    .q-page{
      background-color: $custom-bg-page;
    }
  }
</style>
