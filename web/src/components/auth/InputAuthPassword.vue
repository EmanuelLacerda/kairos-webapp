<script setup>
import InputAuthBase from './InputAuthBase.vue';

defineOptions({
  name: "InputAuthPassword",
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
        type="password"
        name="password"
        placeholder="Senha"
        :autofocus="autofocus"
        @remove-message-error="removeMessageError"
    >
        <q-icon class="bi bi-shield-lock" size="20px"></q-icon>
    </InputAuthBase>
</template>