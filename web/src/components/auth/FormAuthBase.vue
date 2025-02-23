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
      <q-card-section class="form-body">
        <slot name="formbody"></slot>
      </q-card-section>
      <q-card-section class="form-footer">
        <slot name="formfooter"></slot>
      </q-card-section>
  </q-form>
</template>

<style lang="scss">
form.form-auth-base{
  width: 100%;
  min-width: 369px;
  height: 6%;

  .form-body, .form-footer{
    padding: 0;
  }
}
</style>
