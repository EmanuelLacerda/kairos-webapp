<script setup>
defineOptions({
  name: 'VerifyEmailPage'
})

import { ref } from 'vue';
import { useQuasar } from 'quasar'

import FormAuthBase from 'src/components/form-auth/FormAuthBase.vue';
import InputAuthEmail from 'src/components/form-auth/InputAuthEmail.vue';
import InputAuthBase from 'src/components/form-auth/InputAuthBase.vue';
import ButtonAuth from 'src/components/form-auth/ButtonAuth.vue';
import RedirectButton from 'src/components/RedirectButton.vue';

import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore()

const $q = useQuasar()

const enteredEmail = ref('');
const enteredCode = ref('');
const wasEmailSubmit = ref(false)
const wasEmailVerified = ref(false)

const errorMessageCode = ref('')

const isVerificationProcessRunning = ref(false)

const removeErrorMessageCode = () => {
  errorMessageCode.value = "";
}

const submitEmailForm = () => {
  if(enteredEmail.value){
    wasEmailSubmit.value = true;
  }
}

const submitCodeForm = async () => {
  if(enteredCode.value){
    isVerificationProcessRunning.value = true;

    const resultEmailVerification = await 
    authStore.verifyEmail({
      "code": enteredCode.value
    })

    if(resultEmailVerification.wasEmailVerify){
        $q.notify({
          message: "O e-mail foi verificado com sucesso",
          type: "positive",
          timeout: "500",
          closeBtn: true
        })

        wasEmailVerified.value = true;
      }else{
        errorMessageCode.value = resultEmailVerification.error_message;
      }
  }

  isVerificationProcessRunning.value = false;
}
</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <section class="section-parent-verify-email flex items-center justify-center">
      <p class="title" v-if="!wasEmailVerified">Digite abaixo {{ wasEmailSubmit ? "o código que você recebeu" : "o e-mail que você quer verificar" }}</p>
      <FormAuthBase v-if="!wasEmailVerified && !wasEmailSubmit" class="form-verify-email flex items-center justify-center" @submit-form="submitEmailForm">
        <InputAuthEmail v-model="enteredEmail" :autofocus="true"></InputAuthEmail>
        <ButtonAuth button-label="Continuar" :is-disabled="!enteredEmail"></ButtonAuth>
      </FormAuthBase>
      <FormAuthBase v-else-if="!wasEmailVerified && wasEmailSubmit" class="form-verify-email" @submit-form="submitCodeForm">
        <InputAuthBase
          type="text"
          name="code"
          placeholder="Código de verificação"
          v-model="enteredCode"
          :error-message="errorMessageCode"
          @remove-message-error="removeErrorMessageCode"
        >
        </InputAuthBase>
        <ButtonAuth button-label="Verificar" :is-disabled="!enteredCode" :is-process-running="isVerificationProcessRunning"></ButtonAuth>
      </FormAuthBase>
      <section class="container-email-successfully-verification-message flex justify-center items-center" v-else>
        <h1>Parabéns, seu e-mail foi verificado com sucesso!</h1>
        <p>Agora, você pode agendar quantos eventos quiser no nosso sistema!</p>
        <RedirectButton button-label="Quero fazer login" redirect-link="/auth/login/"></RedirectButton>
      </section>
    </section>
  </q-page>
</template>

<style lang="scss">
section.section-parent-verify-email{
  width: 40%;
  height: 500px;
  background-color: $custom-bg-orange-1;
  border-radius: 12px;

  flex-direction: column;

  .form-verify-email{
    width: 30%;
    margin-bottom: 18%;

    *{
      margin: 0;
    }

    label.q-field{
      width: 100%;
    }

    .error-text-message{
      color: $custom-text-color-error-2;
    }

    .invalidInput{
      .q-field__control::before{
          border-color: $custom-border-color-error-2 !important;
      }

      .q-icon, input{
          color: $custom-text-color-error-2 !important;
      }
  }
  }

  p.title{
    font-size: 24px;
    width: 50%;
    margin-bottom: 50px;
    color: $custom-full-white;
  }

  .container-email-successfully-verification-message{
    h1{
      color: #388E3C;
      font-size: 30px;
      font-weight: 600;
      text-align: center;
      margin: 0 20px;
      line-height: 30px;
    }

    p{
      font-size: 17px;
      margin: 0 30px;
      margin-top: 28px;
      margin-bottom: 28px;
      text-align: center;
    }
  }
}
</style>