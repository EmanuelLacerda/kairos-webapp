<script setup>
defineOptions({
  name: "InputAuthConfirmPassword",
});

defineProps({
    autofocus: {
        type: Boolean,
        default: false
    },
})

const emit = defineEmits([
  'removeMessageError'
])


import InputAuthBase from './InputAuthBase.vue';


function removeMessageError(){
    emit('removeMessageError');
}
</script>

<template>
    <InputAuthBase
        type="password"
        name="password"
        placeholder="Confirmar senha"
        :autofocus="autofocus"
        @remove-message-error="removeMessageError"
    >
        <q-icon class="bi bi-shield-lock" size="20px"></q-icon>
    </InputAuthBase>
</template>
