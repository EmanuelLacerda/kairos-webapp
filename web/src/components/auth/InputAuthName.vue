<script setup>
import InputAuthBase from './InputAuthBase.vue';

defineOptions({
  name: "InputAuthName",
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

const removeMessageError = () => {
    emit('removeMessageError');
}
</script>

<template>
    <InputAuthBase
        type="text"
        name="name"
        placeholder="Nome"
        max_length="255"
        :autofocus="autofocus"
        @remove-message-error="removeMessageError"
    >
        <q-icon class="bi bi-person" size="25px"></q-icon>
    </InputAuthBase>
</template>