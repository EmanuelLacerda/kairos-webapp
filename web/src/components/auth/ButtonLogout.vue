<script setup>
defineOptions({
  name: 'ButtonLogout'
})

import { ref } from 'vue'
import { useRouter } from 'vue-router';

import ButtonBase from '../base/ButtonBase.vue';

import { useAuthStore } from 'src/stores/auth';
import { useDialog } from 'src/composables/UseDialog';
import { useToast } from 'src/composables/UseToast';


const router = useRouter()

const authStore = useAuthStore()
const { confirmLogoutDialog } = useDialog()
const { ToastSuccess, ToastError, noStandardToastMixinInfo, positionToastSuccessAuth, positionToastError } = useToast()


const isLogoutRunning = ref(false);


async function logout(){
  isLogoutRunning.value = true;

  const result = await confirmLogoutDialog.fire();

  noStandardToastMixinInfo.title = "Logout"

  if(result.isConfirmed){
    isLogoutRunning.value = false;

    const resultLogout = await authStore.logout();

    if(resultLogout.wasLogoutSuccessfully){
      noStandardToastMixinInfo.text = "Saída com sucesso!"

      ToastSuccess.fire({
        ...noStandardToastMixinInfo,
        position: positionToastSuccessAuth.value
      })

      router.push("/auth/login/");
    } else{
      console.log(resultLogout.error_message);
      noStandardToastMixinInfo.text = "Não foi possível sair! Entre em contato com o suporte ou tente novamente."

      ToastError.fire({
        ...noStandardToastMixinInfo,
        position: positionToastError.value
      })
    }
  } else{
    isLogoutRunning.value = false;
  }
}
</script>

<template>
    <ButtonBase
      class="logout-btn"
      :loading="isLogoutRunning"
      @click="logout"
    >
      <i class="bi bi-box-arrow-left"></i> <span>Sair</span>
    </ButtonBase>
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
