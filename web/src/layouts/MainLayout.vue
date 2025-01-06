<template>
  <q-layout view="hHh Lpr lFf">
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

        <div class="welcome-message">Hi, {{ authStore.user.name }}</div>
        <q-btn @click="logout" class="logout-btn" v-if="authStore.isAuthenticated" :loading="isLogoutRunning">Sair</q-btn>
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

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router';

const $q = useQuasar()
const router = useRouter()

const authStore = useAuthStore()

const linksList = [
  {
    title: 'Minha Agenda',
    icon: 'bi bi-calendar-date',
    route: { name: "home" },
  }
]

const isLogoutRunning = ref(false);

const leftDrawerOpen = ref(false)

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

async function logout(){
  isLogoutRunning.value=true;

  const resultLogout = await authStore.logout();

  isLogoutRunning.value = false;

  if(resultLogout.wasLogoutSuccessfully){
    $q.notify({
      message: "Saída com sucesso!",
      type: "positive",
      timeout: "500",
      closeBtn: true
    })
    router.push("/auth/login/");
  } else{
    console.log(resultLogout.error_message);
  }
}
</script>

<style lang="scss">
  .q-header{
    background-color: rgb(44,62,80);

    .welcome-message{
      margin-right: 10px;
    }

    .logout-btn{
      background-color: rgb(71 104 137);;
    }
  }
</style>