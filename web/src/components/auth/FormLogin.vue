<script setup>
defineOptions({
  name: 'FormLogin'
})
defineModel()

import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import FormAuthBase from 'src/components/auth/FormAuthBase.vue';
import InputAuthEmail from 'src/components/auth/InputAuthEmail.vue';
import InputAuthPassword from 'src/components/auth/InputAuthPassword.vue';
import ButtonAuth from './ButtonAuth.vue';

import { useAuthStore } from 'src/stores/auth';
import { useToast } from 'src/composables/UseToast';


const authStore = useAuthStore()
const { ToastSuccess, ToastError, noStandardToastMixinInfo, positionToastSuccessAuth, positionToastError } = useToast()

const route = useRoute()
const router = useRouter()

const enteredEmail = ref('')
const enteredPassword = ref('')

const errorMessageEmail = ref('')
const errorMessagePassword = ref('')

const isLoginRequestRunning = ref(false)

const removeErrorMessageEmail = () => {
    errorMessageEmail.value = "";
}

const removeErrorMessagePassword = () => {
    errorMessagePassword.value = "";
}

const submitForm = async () => {
  if(enteredEmail.value && enteredPassword.value){
    isLoginRequestRunning.value = true;

    noStandardToastMixinInfo.title = "Login"

    const resultLogin = await authStore.login({
      "email": enteredEmail.value,
      "password": enteredPassword.value
    })
    
    if(resultLogin.wasLoginSuccessfully){
      noStandardToastMixinInfo.text = "Login efetuado com sucesso!"

      ToastSuccess.fire({
        ...noStandardToastMixinInfo,
        position: positionToastSuccessAuth.value
      })

      const toPath = route.query.to || '/';
      setTimeout(() => {
        router.push(toPath);
      }, 600)
    }else{
      if(typeof resultLogin.error_message === "string"){
          noStandardToastMixinInfo.text = resultLogin.error_message;

          ToastError.fire({
            ...noStandardToastMixinInfo,
            position: positionToastError.value

          })
      } else if(typeof resultLogin.error_message === "object"){
          if(resultLogin.error_message.password){
              errorMessagePassword.value = resultLogin.error_message.password[0];
          } else if (resultLogin.error_message.email){
              errorMessageEmail.value = resultLogin.error_message.email[0];
          }
      }
    }

    isLoginRequestRunning.value = false;
  }
}
</script>

<template>
    <section class="section-parent-form-login flex justify-center items-center">
        <FormAuthBase @submit-form="submitForm" class="form-login">
            <InputAuthEmail v-model="enteredEmail" :autofocus="true" :error-message="errorMessageEmail" @remove-message-error="removeErrorMessageEmail"></InputAuthEmail>
            <InputAuthPassword v-model="enteredPassword" :error-message="errorMessagePassword" @remove-message-error="removeErrorMessagePassword"></InputAuthPassword>
            <ButtonAuth button-label="Login" :is-disabled="!enteredEmail || !enteredPassword" :is-process-running="isLoginRequestRunning"></ButtonAuth>
        </FormAuthBase>
        <section class="container-create-account-redirect-link">
            <q-btn flat label="Não tenho conta" to="/auth/criar-conta/" />
        </section>
    </section>
</template>

<style lang="scss">
  section.section-parent-form-login{
    width: 30%;
    
    form.form-login{
        label.q-field:first-child{
            margin-bottom: 20px;
        }
    }

    .container-create-account-redirect-link{
        width: 100%;
        margin-top: 10px;

        display: flex;
        justify-items: start;

        .q-btn{
            color: $custom_full_white;
        }

        .q-btn:hover{
            background-color: $custom-bg-redirect-button;
        }
    }
  }
</style>