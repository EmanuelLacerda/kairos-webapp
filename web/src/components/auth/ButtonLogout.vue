<script setup>
defineOptions({
  name: 'ButtonLogout'
})

import { ref } from 'vue'

import { useAuthStore } from 'src/stores/auth';
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router';

const authStore = useAuthStore()

const $q = useQuasar()
const router = useRouter()

const isLogoutRunning = ref(false);

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

<template>
    <q-btn @click="logout" class="logout-btn" :loading="isLogoutRunning">
        <i class="bi bi-box-arrow-left"></i> <span>Sair</span>
    </q-btn>
</template>

<style lang="scss">
.logout-btn{
    background-color: $custom-blue-2;

    .q-btn__content{
        display: flex;
        gap: 8px;
        justify-content: center;
        align-items: center;
    }
}
</style>