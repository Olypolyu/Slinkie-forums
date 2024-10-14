<script setup>
import {ref} from 'vue'
import { RouterLink, } from 'vue-router'

const props = defineProps([
    'post'
])

const post = ref(props.post);

</script>

<template>
    <div class="thread-card-wrapper">
        <div class="thread-card">
            <img :key="src" :src="post.icon" class="icon" />
            <div style="padding: var(--section-gap);">
                <h4 style="color: var(--minecraft-green);">{{ post.title }}</h4>
                <p class="text-subtle text-dense">I really know i should not tell you this, but in truth, mak is not allowed within the EU anymore because h-</p>
            </div>
            <div class="text-subtle text-dense" style="align-content: center; justify-content: center;">
                <p><b>3012</b> posts p/ week</p>
            </div>
            <div class="text-subtle text-dense" style="align-content: center; justify-content: center;">
                <p><b>45056</b> replies p/ week</p>
            </div>
            <div class="text-subtle text-dense" style="text-align: center;">
                <p><b>&lt;Joe Shmoe&gt;: </b>WOW! i couldn't believe he could do such a thing........... </p>
                <p>it is trully horrifying psychos like this are allowed to develop our minecraft mods!</p>
            </div>
        </div>
    </div>
</template>

<style scoped>

.icon {
    width:  4em;
    height: 4em;
    margin: 0.25rem;
    place-self: center;
}

.thread-card {
    cursor: pointer;
    display: grid;
    grid-template-columns: 0.1fr .45fr 0.115fr 0.115fr 0.32fr;
}

.thread-card:hover {
    background-color: var(--background-grey-lighter);
}

.thread-card-wrapper {
    width: 100%;
}

.thread-card-wrapper #title {
    color: var(--minecraft-green-light);
}

.thread-card-wrapper + .thread-card-wrapper:not(:first-child){
    &::before {
        display: block;
        content: '';

        width: 60%;
        border-bottom: 2px solid var(--text-subtle);
        border-spacing: var(--section-gap);
        margin:  calc(var(--section-gap) * 1.5);
        margin-left: auto;
        margin-right: auto;
    }
}

</style>