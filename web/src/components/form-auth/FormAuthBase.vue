<script setup>
defineOptions({
  name: 'FormAuthBase'
})

const emit = defineEmits([
  'submitForm'
])


function submitForm(){
  emit('submitForm');
}
</script>

<template>
    <q-form
      class="form-auth-base"
      method="post"
      @submit.prevent="submitForm"
    >
        <slot></slot>
    </q-form>
</template>

<style lang="scss">
form.form-auth-base{
  width: 24%;
  min-width: 369px;
  height: 6%;
}
</style>