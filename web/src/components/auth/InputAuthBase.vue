<script setup>
defineOptions({
  name: "InputAuthBase",
});
const prop = defineProps({
    autofocus: {
        type: Boolean,
        default: false
    },
    errorMessage: String
})
const emit = defineEmits([
  'removeMessageError'
])


import { computed } from 'vue';

import FormFieldErrorMessage from '../base/FormFieldErrorMessage.vue';


function removeMessageError(){
    emit('removeMessageError');
}


const inputClasses = computed(() => {
  return { 'invalidInput': prop.errorMessage }
})
</script>

<template>
    <q-input :outlined="true" :autofocus="autofocus" :class="inputClasses" @focus="removeMessageError" v-bind="$attrs">
        <slot></slot>
    </q-input>
    <FormFieldErrorMessage :error-message="errorMessage"></FormFieldErrorMessage>
</template>

<style lang="scss">
form.form-auth-base{
    label.q-field{
        margin-bottom: 20px;

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
            border-color: $custom-full-white;
        }

        .q-field__native, .q-icon{
            color: $custom-full-white;
            font-family: "Montserrat", serif;
            font-weight: 300;
            font-size: 18px;
        }
    }
}

@media (min-width: 1280px) {
  form.form-auth-base{
    label.q-field{
        .q-field__control{
            height: 55px !important;
        }
      }
    }
}
</style>
