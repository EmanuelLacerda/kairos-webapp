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
  min-width: 320px;
  height: 30%;

  .form-body, .form-footer{
    padding: 0;
  }
}

@media (min-width: 360px) {
  form.form-auth-base{
    min-width: 340px;
  }
}

@media (min-width: 430px) {
  form.form-auth-base{
    min-width: 405px;
  }
}

@media (min-width: 768px) {
  form.form-auth-base{
    width: 100%;
  }
}
</style>
