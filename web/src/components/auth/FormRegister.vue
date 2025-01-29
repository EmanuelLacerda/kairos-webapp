<script setup>
defineOptions({
  name: 'FormRegister'
})
defineModel()

import { ref } from 'vue';

import FormAuthBase from 'src/components/auth/FormAuthBase.vue';
import InputAuthEmail from 'src/components/auth/InputAuthEmail.vue';
import InputAuthPassword from 'src/components/auth/InputAuthPassword.vue';
import InputAuthName from './InputAuthName.vue';
import InputAuthConfirmPassword from './InputAuthConfirmPassword.vue';
import ButtonAuth from './ButtonAuth.vue';
import RedirectButton from '../RedirectButton.vue';

import { useAuthStore } from 'src/stores/auth';
import authService from 'src/services/auth'
import { useToast } from 'src/composables/UseToast';


const authStore = useAuthStore()
const { validatePassword } = authService();
const { ToastSuccess, ToastError, noStandardToastMixinInfo, positionToastSuccessAuth, positionToastError } = useToast()


const enteredName = ref('')
const enteredEmail = ref('teste@gmail.com')
const enteredPassword = ref('')
const enteredConfirmPassword = ref('')

const errorMessageName = ref('')
const errorMessageEmail = ref('')
const errorMessagePassword = ref('')
const errorMessageConfirmPassword = ref('')

const isRegisterProcessRunning = ref(false)
const accountCreateSuccessfully = ref(false);


function removeErrorMessageName(){
  errorMessageName.value = "";
}

function removeErrorMessageEmail(){
    errorMessageEmail.value = "";
}

function removeErrorMessagePassword(){
    errorMessagePassword.value = "";
}

function removeErrorMessageConfirmPassword(){
  errorMessageConfirmPassword.value = "";
}

async function submitForm(){
  if(enteredName.value && enteredEmail.value && enteredPassword.value && enteredConfirmPassword.value){
    isRegisterProcessRunning.value = true;

    noStandardToastMixinInfo.title = "Criação de conta"

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
        noStandardToastMixinInfo.text = "Conta criada com sucesso!"

        ToastSuccess.fire({
          ...noStandardToastMixinInfo,
          position: positionToastSuccessAuth.value
        })

        accountCreateSuccessfully.value = true;
      }else{
        if(typeof resultRegister.error_message === "string"){
            noStandardToastMixinInfo.text = resultRegister.error_message;

            ToastError.fire({
              ...noStandardToastMixinInfo,
              position: positionToastError.value

            });
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

    isRegisterProcessRunning.value = false;
  }
}
</script>

<template>
    <section class="section-parent-form-register flex justify-center items-center">
      <FormAuthBase @submit-form="submitForm" class="form-login" v-if="!accountCreateSuccessfully">
        <InputAuthName v-model="enteredName" :error-message="errorMessageName" @remove-message-error="removeErrorMessageName"  :autofocus="true"></InputAuthName>
        <InputAuthEmail v-model="enteredEmail" :error-message="errorMessageEmail" @remove-message-error="removeErrorMessageEmail"></InputAuthEmail>
        <InputAuthPassword v-model="enteredPassword" :error-message="errorMessagePassword" @remove-message-error="removeErrorMessagePassword"></InputAuthPassword>
        <InputAuthConfirmPassword v-model="enteredConfirmPassword" :error-message="errorMessageConfirmPassword" @remove-message-error="removeErrorMessageConfirmPassword" class="mb-0"></InputAuthConfirmPassword>
        <ButtonAuth button-label="Criar conta" :is-disabled="!enteredName || !enteredEmail || !enteredPassword || !enteredConfirmPassword" :is-process-running="isRegisterProcessRunning"></ButtonAuth>
      </FormAuthBase>
      <section class="box-verify-email-message" v-else>
        <h1>Verifique sua caixa de mensagens</h1>
        <p>Enviamos um código para <strong>{{enteredEmail}}</strong>. Clique no botão abaixo e insira esse código na página que será aberta para verificar seu e-mail.</p>
        <RedirectButton button-label="Verificar e-mail" redirect-link="/auth/verificar-email/"></RedirectButton>
      </section>
    </section>
</template>

<style lang="scss">
  section.section-parent-form-register{
    width: 50%;

    form.form-login{
      label.q-field{
        margin-bottom: 20px;
      }

      button.q-btn{
        width: 100%;
        height: 45px;
        color: $custom-text-primary;
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
      line-height: 38px;
      text-align: center;
      margin-bottom: 20px;
    }

    p{
      width:60%;

      text-align: center;
      font-size: 19px;
    }
  }
</style>
