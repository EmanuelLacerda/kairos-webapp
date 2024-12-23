<script setup>
import { ref } from 'vue';

defineOptions({
  name: 'IndexPage'
})

const emailEntered = ref('')
const passwordEntered = ref('')
</script>

<template>
  <q-page padding class="flex items-center justify-center">
    <section class="flex justify-center items-center">
      <q-form class="form-login" method="post">
        <q-input
          type="email"
          v-model="emailEntered"
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
          v-model="passwordEntered"
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