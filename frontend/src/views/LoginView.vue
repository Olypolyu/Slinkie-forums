<script setup>
import {ref} from 'vue'
import { isLoggedIn, logIn } from '../Api';
import { watch } from 'vue';
import { store } from '../store';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref("");
const password = ref("");
const error = ref("")

async function doLogIn(event) {
    error.value = await logIn(username.value, password.value);
    if (store.loggedIn) router.replace({path: "/"});
};

</script>

<template>
    <div class="card content" style="max-width: 35rem;">
        <div class="card-header" style="text-align: center;">
            <h1>Welcome!</h1>
        </div>
            <span style="margin: 0.75rem;" />

        <div style="display: grid; grid-template-columns: repeat(2, auto); align-items: center; margin: 6px;">
            <label for="username">Username:</label>
            <div class="tooltip-parent">
                <input type="text" id="username" v-model="username">
                <div class="tooltip">
                    <p>Insert a valid username:</p>
                    <p>A valid username must be at least 8 letters long and <strong>unique to the user.</strong></p>
                    <p>Usernames <strong>may be changed once per month.</strong></p>
                </div>
            </div>

            <!--
            <label for="email">Email:</label>
            <div class="tooltip-parent">
                <input type="text" id="email">
                <div class="tooltip">
                    <p>Insert a valid email.</p>
                    <p>This email <strong>will be used for password resets</strong> and critical messaging like long website outages.</p>
                </div>
            </div>
            -->

            <label for="password">Password:</label>
            <div class="tooltip-parent">
                <input type="password" id="password" v-model="password">
                <div class="tooltip">
                    <p>Insert a valid password:</p>
                    <p>A valid password must be <strong>at least 16 letters long and contain letters (both cases), numbers and symbols.</strong></p>
                    <p>For example: pASSw0rd!!!1!11!</p>
                </div>
            </div>
        </div>
        <p class="error" id="error">{{ error }}</p>
        <button @click="doLogIn" style="width: 50%;">Login!</button>

        <span style="margin: 0.75rem;" />
        <hr style="width: 85%">
        <span style="margin: 0.75rem;" />
        <button style="width: 50%;">Login with Microsoft</button>
        <button style="width: 50%;" class="discord-btn">Login with Discord</button>
    </div>
</template>

<style>
    .error {
        color: salmon;
        font-style: italic;
    }

    .discord-btn {
        background-color: rgb(88, 101, 242);
        border-bottom: 3px solid rgb(44, 54, 170);
    }
    .discord-btn:hover {background-color: rgb(72, 84, 219);}
    .discord-btn:active {background-color: rgb(44, 54, 170);}
</style>