<template>
  <div class="not-found-page fullscreen text-white text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 30vh">
        404
      </div>

      <div class="text-h2" style="opacity:.4">
        Desculpe, não temos esta página.
      </div>

      <q-btn
        class="q-mt-xl"
        color="white"
        unelevated
        to="/"
        label="Voltar para home"
        no-caps
      />
    </div>
  </div>
</template>

<style lang="scss">
.not-found-page{
  background-color: $custom-text-primary;

  .q-btn{
    color: $custom-text-primary !important;
  }
}
</style>
