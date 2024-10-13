<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'

const router = useRouter()
const loggedIn = ref(false);

onMounted(
  () => {
    loggedIn.value = Math.floor(Math.random() * 100 ) % 2 === 1;
    console.log(loggedIn);
  }
);

</script>

<template>
  <header>
    <div class="card" style="margin-bottom: 1em;">
      <nav v-if="loggedIn == true">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">about</RouterLink>
      </nav>

      <nav v-else>
        <p>You're not logged in <span class="text-subtle">- You must log in or sign in before posting.</span></p>
        <button v-if="$route.name !== 'login'" @click="router.push('/login')">Login / Signup</button>
      </nav>
    </div>

  </header>

  <RouterView />
  
</template>

<style scoped>

header {
  line-height: 1.5;
  max-height: 100vh;
}

nav {
  width: 100%;
  text-align: center;
  place-items: center;
}

nav a.router-link-exact-active {
  color: var(--minecraft-green);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
}

nav a:first-of-type {
  border: 0;
}

</style>
