<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import modal from './components/Modal.vue';
import { store } from './store';
import { logOut } from './Api';

const router = useRouter()

</script>

<template>
  <header style="position: sticky; top: 0; z-index: 1;">
    <div class="card" style="margin-bottom: 1em">
      <nav v-if="store.loggedIn == true" style="display: flex; flex-direction: row; justify-content: space-between;">
        <div>
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/about">about</RouterLink>
        </div>
        <button @click="logOut">Log-out</button>
      </nav>

      <nav v-else>
        <p><span style="font-weight: bold;">You're not logged in</span> <span class="text-subtle">- You must log in or sign in before posting.</span></p>
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
