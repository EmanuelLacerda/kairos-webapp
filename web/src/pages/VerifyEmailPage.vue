<script setup>
defineOptions({
  name: 'VerifyEmailPage'
})


import { ref, computed } from 'vue';

import FormAuthBase from 'src/components/auth/FormAuthBase.vue';
import InputAuthEmail from 'src/components/auth/InputAuthEmail.vue';
import InputAuthBase from 'src/components/auth/InputAuthBase.vue';
import ButtonAuth from 'src/components/auth/ButtonAuth.vue';
import RedirectButton from 'src/components/RedirectButton.vue';

import { useAuthStore } from 'src/stores/auth';
import { useToast } from 'src/composables/UseToast';


const authStore = useAuthStore()
const { ToastSuccess, noStandardToastMixinInfo, positionToastSuccessAuth } = useToast()


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

    noStandardToastMixinInfo.title = "Verificação de e-mail";

    const resultEmailVerification = await
    authStore.verifyEmail({
      "code": enteredCode.value
    })

    if(resultEmailVerification.wasEmailVerify){
      noStandardToastMixinInfo.text = "E-mail verificado com sucesso!"

      ToastSuccess.fire({
        ...noStandardToastMixinInfo,
        position: positionToastSuccessAuth.value
      })

      wasEmailVerified.value = true;
    }else{
      errorMessageCode.value = resultEmailVerification.error_message;
    }
  }

  isVerificationProcessRunning.value = false;
}


const title = computed(() => `Digite abaixo ${wasEmailSubmit.value ? "o código que você recebeu" : "o e-mail que você quer verificar"}`);

const emailWasNotProvided = computed(() => !wasEmailVerified.value && !wasEmailSubmit.value);

const emailWasNotVerified = computed(() => !wasEmailVerified.value && wasEmailSubmit.value);
</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <section class="section-parent-verify-email flex items-center justify-center">
      <p class="title" v-if="!wasEmailVerified">{{ title }}</p>
      <FormAuthBase v-if="emailWasNotProvided" class="form-verify-email  flex column no-wrap" @submit-form="submitEmailForm">
        <template #formbody>
          <InputAuthEmail v-model="enteredEmail" :autofocus="true"></InputAuthEmail>
        </template>
        <template #formfooter>
          <ButtonAuth label="Continuar" :allFieldsValue="[ enteredEmail ]"></ButtonAuth>
        </template>
      </FormAuthBase>

      <FormAuthBase v-else-if="emailWasNotVerified" class="form-verify-email" @submit-form="submitCodeForm">
        <template #formbody>
          <InputAuthBase
            type="text"
            name="code"
            placeholder="Código de verificação"
            v-model="enteredCode"
            :error-message="errorMessageCode"
            @remove-message-error="removeErrorMessageCode"
          >
          </InputAuthBase>
        </template>
        <template #formfooter>
          <ButtonAuth label="Verificar" :allFieldsValue="[ enteredCode ]" :loading="isVerificationProcessRunning"></ButtonAuth>
        </template>
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
  width: 100%;
  height: 500px;
  max-width: 800px;
  background-color: $custom-bg-orange-1;
  border-radius: 12px;

  flex-direction: column;

  .form-verify-email{
    width: 60%;
    min-width: 300px;
    margin-bottom: 0;

    *{
      margin: 0;
    }

    label.q-field{
      width: 100%;
    }

    .error-text-message{
      color: $custom-text-danger-2;
    }

    .invalidInput{
      .q-field__control::before{
          border-color: $custom-border-color-error-2 !important;
      }

      .q-icon, input{
          color: $custom-text-danger-2 !important;
      }
  }
  }

  p.title{
    font-size: 24px;
    width: 90%;
    margin-bottom: 43px;
    color: $custom-full-white;
    text-align: center;
  }

  .container-email-successfully-verification-message{
    h1{
      color: $custom-green-3;
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

@media (min-width: 375px) {
  section.section-parent-verify-email{
      .form-verify-email{
        min-width: 350px;
    }
  }
}

@media (min-width: 400px) {
  section.section-parent-verify-email{
      .form-verify-email{
        min-width: 380px;
    }
  }
}

@media (min-width: 768px) {
  section.section-parent-verify-email{
    width: 75%;

    .form-verify-email{
        width: 80%;
    }
  }
}
</style>
