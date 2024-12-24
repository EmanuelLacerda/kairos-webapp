<script setup>
import InputAuthBase from './InputAuthBase.vue';

defineOptions({
  name: "InputAuthEmail",
});

defineProps({
    autofocus: {
        type: Boolean,
        required: true
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
        type="email"
        name="email"
        placeholder="E-mail"
        :autofocus="autofocus"
        @remove-message-error="removeMessageError"
    >
        <q-icon class="bi bi-person" size="25px"></q-icon>
    </InputAuthBase>
</template>