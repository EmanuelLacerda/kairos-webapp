<script setup>
defineOptions({
  name: "InputAuthPassword",
});

defineProps({
    autofocus: {
        type: Boolean,
        default: false
    },
})


import { computed, ref } from 'vue';

const emit = defineEmits([
  'removeMessageError'
])


import InputAuthBase from './InputAuthBase.vue';


function removeMessageError(){
    emit('removeMessageError');
}

const shouldShowPassword = ref(false)

function changeThePasswordVisibility(){
  shouldShowPassword.value = !shouldShowPassword.value
}

const passwordFieldType = computed(() => {
  return shouldShowPassword.value ? "text" : "password"
})

const passwordFieldClasses = computed(() => {
  return {'bi': true, 'bi-eye-fill': !shouldShowPassword.value, 'bi-eye-slash-fill': shouldShowPassword.value }
})
</script>

<template>
    <InputAuthBase
        :type="passwordFieldType"
        name="password"
        :autofocus="autofocus"
        @remove-message-error="removeMessageError"
    >
      <template #prepend>
        <q-icon class="bi bi-shield-lock" size="20px"></q-icon>
      </template>

      <template #append>
        <q-icon :class="passwordFieldClasses" size="20px" id="passwordVisibleButton" @click="changeThePasswordVisibility" />
      </template>
    </InputAuthBase>
</template>

<style lang="scss">
form.form-auth-base{
  label.q-field{
    .q-field__inner{
      .q-field__append{
        #passwordVisibleButton:hover{
          cursor: pointer;
        }
      }
    }
  }
}
</style>