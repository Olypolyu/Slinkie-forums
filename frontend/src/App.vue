<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { store } from './store';
import { logOut } from './Api';

const router = useRouter()
</script>

<script>
    window.onmousemove = function (e) {
        let x = e.clientX;
        let y = e.clientY;

        const docRect = document.body.getBoundingClientRect();

        document.body.querySelectorAll(".tooltip").forEach(
            tooltip => {
                if (Number(window.getComputedStyle(tooltip).getPropertyValue("opacity")) > 0) {
                    const tooltipRect = tooltip.getBoundingClientRect();

                    tooltip.style.top  = ((y + tooltipRect.height < docRect.height) ? (y + 5) : (docRect.height -tooltipRect.height)) + 'px';
                    tooltip.style.left = ((x + tooltipRect.width < docRect.width) ? (x + 5) : (docRect.width - tooltipRect.width)) + 'px';
                }
            }
        );
    };
</script>

<template>
    <header style="position: sticky; top: 0; z-index: 1;">
        <div class="card" >
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
        max-height: 100vh;
        border-bottom: 2px solid var(--background-grey-dark);
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
