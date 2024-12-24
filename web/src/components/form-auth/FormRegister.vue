<script setup>
defineOptions({
  name: 'FormRegister'
})
defineModel()

import { ref } from 'vue';
import { useQuasar } from 'quasar'

import FormAuthBase from 'src/components/form-auth/FormAuthBase.vue';
import InputAuthEmail from 'src/components/form-auth/InputAuthEmail.vue';
import InputAuthPassword from 'src/components/form-auth/InputAuthPassword.vue';
import InputAuthName from './InputAuthName.vue';
import InputAuthConfirmPassword from './InputAuthConfirmPassword.vue';

import { useAuthStore } from 'src/stores/auth';
import authService from 'src/services/auth'

const { validatePassword } = authService();


const authStore = useAuthStore()

const notifyWarningConfigObj = {
  type: "warning",
  timeout: "800",
  closeBtn: true
}

const $q = useQuasar()

const enteredName = ref('')
const enteredEmail = ref('teste@gmail.com')
const enteredPassword = ref('')
const enteredConfirmPassword = ref('')

const errorMessageName = ref('')
const errorMessageEmail = ref('')
const errorMessagePassword = ref('')
const errorMessageConfirmPassword = ref('')

const removeErrorMessageName = () => {
  errorMessageName.value = "";
}

const removeErrorMessageEmail = () => {
    errorMessageEmail.value = "";
}

const removeErrorMessagePassword = () => {
    errorMessagePassword.value = "";
}

const removeErrorMessageConfirmPassword = () => {
  errorMessageConfirmPassword.value = "";
}

const accountCreateSuccessfully = ref(false);

const submitForm = async () => {
  if(enteredName.value && enteredEmail.value && enteredPassword.value && enteredConfirmPassword.value){
    const result = validatePassword(enteredPassword.value, enteredConfirmPassword.value);

    if(result.isPasswordInvalid){
        if(result.field === "password"){
          errorMessagePassword.value = result.errorMessage;
        } else if(result.field === "confirm password"){
          errorMessageConfirmPassword.value = result.errorMessage;
        }
    } else{
      const resultRegister = await authStore.register({
        "name": enteredName.value,
        "email": enteredEmail.value,
        "password": enteredPassword.value,
        "confirm_password": enteredConfirmPassword.value
      })

      if(resultRegister.wasRegisterSuccessfully){
        $q.notify({
          message: "Conta criada com sucesso",
          type: "positive",
          timeout: "500",
          closeBtn: true
        })

        accountCreateSuccessfully.value = true;
      }else{
        if(typeof resultRegister.error_message === "string"){
            notifyWarningConfigObj.message = resultRegister.error_message;
            $q.notify(notifyWarningConfigObj);
        } else if(typeof resultRegister.error_message === "object"){
          if (resultRegister.error_message.name){
                errorMessageName.value = resultRegister.error_message.name[0];
          } else if (resultRegister.error_message.email){
              errorMessageEmail.value = resultRegister.error_message.email[0];
          } else if(resultRegister.error_message.password){
              errorMessagePassword.value = resultRegister.error_message.password[0];
          } else if(resultRegister.error_message.confirm_password){
              errorMessageConfirmPassword.value = resultRegister.error_message.confirm_password[0];
          }
        }
      }
    }
  }
}
</script>

<template>
    <FormAuthBase @submit-form="submitForm" class="form-login" v-if="!accountCreateSuccessfully">
      <InputAuthName v-model="enteredName" :error-message="errorMessageName" @remove-message-error="removeErrorMessageName"  :autofocus="true"></InputAuthName>
      <InputAuthEmail v-model="enteredEmail" :error-message="errorMessageEmail" @remove-message-error="removeErrorMessageEmail"></InputAuthEmail>
      <InputAuthPassword v-model="enteredPassword" :error-message="errorMessagePassword" @remove-message-error="removeErrorMessagePassword"></InputAuthPassword>
      <InputAuthConfirmPassword v-model="enteredConfirmPassword" :error-message="errorMessageConfirmPassword" @remove-message-error="removeErrorMessageConfirmPassword" class="mb-0"></InputAuthConfirmPassword>
      
      <q-btn
        label="login"
        type="submit"
        class="bg-white"
        :outline="false"
        :disable="!enteredEmail || !enteredPassword"
      >

      </q-btn>
    </FormAuthBase>
    <section class="box-verify-email-message" v-else>
      <h1>Verifique sua caixa de mensagens</h1>
      <p>Enviamos um código para <strong>{{enteredEmail}}</strong>. Clique no botão abaixo e insira esse código na página que será aberta para verificar seu e-mail.</p>
      <q-btn label="Verificar e-mail" to="/auth/verificar-email/" size="20px" :rounded="true"></q-btn>
    </section>
</template>

<style lang="scss">
  section{
    form.form-login{
      label.q-field{
        margin-bottom: 20px;
      }

      button.q-btn{
        width: 100%;
        height: 45px;
        color: $custom-blue-1;
        margin-top: 23px;
        font-family: "Montserrat", serif;
        font-weight: 600;
        font-size: 20px;
      }
    }
  }

  .box-verify-email-message{
    background-color: $custom-bg-white;
    width: 100%;
    min-width: 420px;
    height: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: start;

    padding: 60px 40px;

    border-radius: 20px;

    *{
      margin: 0;
    }

    h1{
      font-size: 32px;
      font-weight: 700;
      color: $custom-orange-1;
    }

    p{
      width:60%;

      text-align: center;
      font-size: 19px;
    }

    .q-btn{
      margin-top: 100px;

      background-color: $custom-bg-redirect-button;
      color:$custom-text-color-redirect-button;
    }
  }
</style>