<script setup>
defineOptions({
  name: 'ButtonLogout'
})

import { ref } from 'vue'

import { useAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router';
import { useDialog } from 'src/composables/UseDialog';
import { useToast } from 'src/composables/UseToast';

const authStore = useAuthStore()

const { confirmLogoutDialog } = useDialog()
const { ToastSuccess, noStandardToastMixinInfo, positionToastSuccessAuth } = useToast()

const router = useRouter()

const isLogoutRunning = ref(false);

async function logout(){
  isLogoutRunning.value = true;

  const result = await confirmLogoutDialog.fire();

  noStandardToastMixinInfo.title = "Logout"

  if(result.isConfirmed){
    const resultLogout = await authStore.logout();

    isLogoutRunning.value = false;

    if(resultLogout.wasLogoutSuccessfully){
      noStandardToastMixinInfo.text = "Saída com sucesso!"

      ToastSuccess.fire({
        ...noStandardToastMixinInfo,
        position: positionToastSuccessAuth.value
      })
      
    router.push("/auth/login/");
    } else{
      console.log(resultLogout.error_message);
    }
  } else{
    isLogoutRunning.value = false;
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