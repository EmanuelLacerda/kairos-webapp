<script setup>
defineOptions({
  name: 'FormLogin'
})
defineModel()

import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import FormAuthBase from 'src/components/auth/FormAuthBase.vue';
import InputAuthEmail from 'src/components/auth/InputAuthEmail.vue';
import InputAuthPassword from 'src/components/auth/InputAuthPassword.vue';
import ButtonAuth from './ButtonAuth.vue';

import { useAuthStore } from 'src/stores/auth';
import { useToast } from 'src/composables/UseToast';


const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()
const { ToastSuccess, ToastError, noStandardToastMixinInfo, positionToastSuccessAuth, positionToastError } = useToast()


const enteredEmail = ref('')
const enteredPassword = ref('')

const errorMessageEmail = ref('')
const errorMessagePassword = ref('')

const isLoginRequestRunning = ref(false)


function removeErrorMessageEmail(){
    errorMessageEmail.value = "";
}

function removeErrorMessagePassword(){
    errorMessagePassword.value = "";
}

async function submitForm(){
  if(enteredEmail.value && enteredPassword.value){
    noStandardToastMixinInfo.title = "Login"

    isLoginRequestRunning.value = true;

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
          } else{
            console.log(resultLogin.error_message);
            noStandardToastMixinInfo.text = "Não foi possível fazer login! Entre em contato com o suporte ou tente novamente."

            ToastError.fire({
              ...noStandardToastMixinInfo,
              position: positionToastError.value
            })
          }
      }
    }

    isLoginRequestRunning.value = false;
  }
}

const arrayOfFieldsValue = computed(() => [ enteredEmail.value, enteredPassword.value ])
</script>

<template>
    <section class="section-parent-form-login flex justify-center items-center">
        <FormAuthBase @submit-form="submitForm" class="form-login">
          <template #formbody>
            <InputAuthEmail v-model="enteredEmail" :autofocus="true" :error-message="errorMessageEmail" @remove-message-error="removeErrorMessageEmail"></InputAuthEmail>
            <InputAuthPassword v-model="enteredPassword" :error-message="errorMessagePassword" @remove-message-error="removeErrorMessagePassword"></InputAuthPassword>
          </template>
          <template #formfooter>
            <ButtonAuth label="Login" :allFieldsValue="arrayOfFieldsValue" :loading="isLoginRequestRunning"></ButtonAuth>
          </template>
        </FormAuthBase>
        <section class="container-create-account-redirect-link">
            <q-btn flat label="Não tenho conta" to="/auth/criar-conta/" />
        </section>
    </section>
</template>

<style lang="scss">
  section.section-parent-form-login{
    width: 40%;

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
