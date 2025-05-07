<script setup>
defineOptions({
  name: "ErrorMessage",
});

defineProps({
    errorMessage: String
})
</script>

<template>
    <p class="error-text-message">{{errorMessage}}</p>
</template>

<style lang="scss">
form{
    .invalidInput{
        .q-field__control::before{
            border-color: $custom-border-color-error !important;
        }

        .q-icon, input{
            color: $custom-text-danger !important;
        }
    }

    .error-text-message{
        color: $custom-text-danger;
        margin-top: 12px;
        font-weight: 600;
        text-align: justify;
    }
}

@media (min-width: 768px) {
  form{
    .error-text-message{
      font-size: 1.1rem;
    }
  }
}

@media (min-width: 1280px) {
  form{
    .error-text-message{
      font-size: 1.2rem;
    }
  }
}
</style>
