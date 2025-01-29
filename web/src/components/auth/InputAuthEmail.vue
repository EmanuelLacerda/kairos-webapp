<script setup>
defineOptions({
  name: "InputAuthEmail",
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
        type="email"
        name="email"
        placeholder="E-mail"
        :autofocus="autofocus"
        @remove-message-error="removeMessageError"
    >
        <q-icon class="bi bi-person" size="25px"></q-icon>
    </InputAuthBase>
</template>
