<script setup>
import { ref } from 'vue';
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth';
import { useRoute, useRouter } from 'vue-router';

const authStore = useAuthStore()

const notifyWarningConfigObj = {
  type: "warning",
  timeout: "800",
  closeBtn: true
}


const $q = useQuasar()
const route = useRoute()
const router = useRouter()

defineOptions({
  name: 'IndexPage'
})

const enteredEmail = ref('')
const enteredPassword = ref('')

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
      notifyWarningConfigObj.message = result.error_message
      $q.notify(notifyWarningConfigObj)
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
        notifyWarningConfigObj.message = resultLogin.error_message;
        $q.notify(notifyWarningConfigObj);
      }
    }
  }
}
</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <section class="flex justify-center items-center">
      <q-form class="form-login" method="post" @submit.prevent="submitForm">
        <q-input
          type="email"
          v-model="enteredEmail"
          name="email"
          :autofocus="true"
          placeholder="E-mail"
          :outlined="true"
          class="border-white"
        >
          <q-icon class="bi bi-person" size="25px"></q-icon>
        </q-input>
        <q-input
          type="password"
          v-model="enteredPassword"
          name="email"
          placeholder="Senha"
          :outlined="true"
        >
          <q-icon class="bi bi-shield-lock" size="20px"></q-icon>
        </q-input>
        <q-btn
          label="login"
          type="submit"
          class="bg-white"
          :outline="false"
          :disable="!enteredEmail || !enteredPassword"
        >

        </q-btn>
      </q-form>
    </section>
  </q-page>
</template>

<style lang="scss">
  section{

    form.form-login{
      width: 24%;
      min-width: 369px;
      height: 6%;

      label.q-field:first-child{
        margin-bottom: 20px;
      }

      label.q-field{
        .q-field__control{
          height: 45px !important;

          .q-field__control-container{
            display: flex;
            flex-direction: row-reverse;
            align-items: center;
            gap: 15px;
          }
        }
  
        .q-field__control::before{
          border-color: $custom-full-white !important;
        }
  
        .q-field__native, .q-icon{
          color: $custom-full-white;
          font-family: "Montserrat", serif;
          font-weight: 300;
          font-size: 18px;
        }
      }

      button.q-btn{
        width: 100%;
        height: 45px;
        color: $custom-blue-1;
        margin-top: 43px;
        font-family: "Montserrat", serif;
        font-weight: 600;
        font-size: 20px;
      }
    }
  }
</style>