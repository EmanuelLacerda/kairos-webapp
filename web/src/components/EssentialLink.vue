<script setup>
defineOptions({
  name: "EssentialLink",
});

const props = defineProps({
  title: {
    type: String,
    required: true,
  },

  caption: {
    type: String,
    default: "",
  },

  route: {
    type: Object,
    default: null,
  },

  icon: {
    type: String,
    default: "",
  },
});
</script>
<template>
  <q-item clickable :to="props.route" exact class="q-mx-sm row flex-center">
    <q-item-section class="q-pr-xs" v-if="props.icon" avatar>
      <i :class="props.icon" style="font-size: 24px" class="text-pink-800"></i>
    </q-item-section>

    <q-item-section>
      <q-item-label
        class="text-weight-bold"
        style="font-size: 18px"
        >{{ props.title }}</q-item-label
      >
    </q-item-section>
  </q-item>
</template>
<style lang="scss">
.q-router-link--exact-active,
.q-router-link--active {
  background-color: $custom-bg-primary;
  color: $custom-full-white !important;
  border-radius: 12px;
}

.q-router-link--exact-active .q-item__section--avatar > i,
.q-router-link--active .q-item__section--avatar > i {
  color: $custom-full-white !important;
}
</style>
