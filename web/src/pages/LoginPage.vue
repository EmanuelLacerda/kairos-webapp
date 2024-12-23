<script setup>
import { ref } from 'vue';

defineOptions({
  name: 'IndexPage'
})

const emailEntered = ref('')
const passwordEntered = ref('')
</script>

<template>
  <q-page padding>
    <div>
      <q-form method="post">
        <q-input type="email" v-model="emailEntered" name="email" :autofocus="true" placeholder="E-mail">

        </q-input>
        <q-input type="password" v-model="passwordEntered" name="email" placeholder="Senha">

        </q-input>
        <q-btn label="login" type="submit">

        </q-btn>
      </q-form>
    </div>
  </q-page>
</template>