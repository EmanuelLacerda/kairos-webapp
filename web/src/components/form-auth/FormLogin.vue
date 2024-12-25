<script setup>
defineOptions({
  name: 'FormLogin'
})
defineModel()

import { ref } from 'vue';
import { useQuasar } from 'quasar'
import { useRoute, useRouter } from 'vue-router';

import FormAuthBase from 'src/components/form-auth/FormAuthBase.vue';
import InputAuthEmail from 'src/components/form-auth/InputAuthEmail.vue';
import InputAuthPassword from 'src/components/form-auth/InputAuthPassword.vue';
import ButtonAuth from './ButtonAuth.vue';

import { useAuthStore } from 'src/stores/auth';


const authStore = useAuthStore()

const notifyWarningConfigObj = {
  type: "warning",
  timeout: "800",
  closeBtn: true
}

const $q = useQuasar()
const route = useRoute()
const router = useRouter()

const enteredEmail = ref('')
const enteredPassword = ref('')

const errorMessageEmail = ref('')
const errorMessagePassword = ref('')

const removeErrorMessageEmail = () => {
    errorMessageEmail.value = "";
}

const removeErrorMessagePassword = () => {
    errorMessagePassword.value = "";
}

const validatePassword = (password) => {
    const lowerCaseLetters = /[a-z]/g;
    if(!password.match(lowerCaseLetters)) {
      return {
        "isPasswordInvalid": true,
        "error_message": "A senha deve conter ao menos uma letra minúscula!"
      }
    }

    const upperCaseLetters = /[A-Z]/g;
    if(!password.match(upperCaseLetters)) {
      return {
        "isPasswordInvalid": true,
        "error_message": "A senha deve conter ao menos uma letra maiúscula!"
      }
    }

    const numbers = /[0-9]/g;
    if(!password.match(numbers)) {
      return {
        "isPasswordInvalid": true,
        "error_message": "A senha deve conter ao menos um número!"
      }
    }

    if(!(password.length >= 8)) {
      return {
        "isPasswordInvalid": true,
        "error_message": "A senha deve conter ao menos 8 caracteres!"
      }
    }

    return {
      "isPasswordInvalid": false
    }
}

const submitForm = async () => {
  if(enteredEmail.value && enteredPassword.value){
    const result = validatePassword(enteredPassword.value);

    if(result.isPasswordInvalid){
        errorMessagePassword.value = result.error_message;
    } else{
      const resultLogin = await authStore.login({
        "email": enteredEmail.value,
        "password": enteredPassword.value
      })

      if(resultLogin.wasLoginSuccessfully){
        $q.notify({
          message: "Login efetuado com sucesso",
          type: "positive",
          timeout: "500",
          closeBtn: true
        })

        const toPath = route.query.to || '/';
        setTimeout(() => {
          router.push(toPath);
        }, 600)
      }else{
        if(typeof resultLogin.error_message === "string"){
            notifyWarningConfigObj.message = resultLogin.error_message;
            $q.notify(notifyWarningConfigObj);
        } else if(typeof resultLogin.error_message === "object"){
            if(resultLogin.error_message.password){
                errorMessagePassword.value = resultLogin.error_message.password[0];
            } else if (resultLogin.error_message.email){
                errorMessageEmail.value = resultLogin.error_message.email[0];
            }
        }
      }
    }
  }
}
</script>

<template>
    <section class="section-parent-form-login flex justify-center items-center">
        <FormAuthBase @submit-form="submitForm" class="form-login">
            <InputAuthEmail v-model="enteredEmail" :autofocus="true" :error-message="errorMessageEmail" @remove-message-error="removeErrorMessageEmail"></InputAuthEmail>
            <InputAuthPassword v-model="enteredPassword" :error-message="errorMessagePassword" @remove-message-error="removeErrorMessagePassword"></InputAuthPassword>
            <ButtonAuth button-label="Login" :is-disabled="!enteredEmail || !enteredPassword"></ButtonAuth>
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