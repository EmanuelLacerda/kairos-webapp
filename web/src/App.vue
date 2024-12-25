<template>
  <router-view />
</template>

<script setup>
defineOptions({
  name: "App",
});

import "bootstrap-icons/font/bootstrap-icons.css";
import { onBeforeMount } from "vue";
import { useAuthStore } from "./stores/auth";
import { api } from "./boot/axios";

const authStore = useAuthStore();

onBeforeMount(() => {
  authStore.init();

  if(authStore.token){
    api.defaults.headers.common.Authorization = `Bearer ${authStore.token.value}`;
  } else{
    api.defaults.headers.common.Authorization = "";
  }
})
</script>
