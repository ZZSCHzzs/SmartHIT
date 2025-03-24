<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from "@/components/navbar.vue";
import Header from "@/components/header.vue";
import Bubble from "@/components/chatbubble.vue"

</script>

<template>
  <div id="app">
      <Navbar />
      <Header v-if="$route.name === 'index' || $route.name === 'default'"/>
      <Bubble />
      <router-view></router-view>

  </div>
</template>

<style scoped>

</style>