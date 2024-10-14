<script setup>
import {ref} from 'vue'

const props = defineProps([
    'post'
])

const post = ref(props.post);

</script>

<template>
    <div class="thread-card">
        <div class="thread-card-grid">
            <img :key="src" :src="post.icon" class="icon" />
            <h3 id="title">{{ post.title }}</h3>
        </div>
    </div>
</template>

<style scoped>

.icon {
    width:  4em;
    height: 4em;
    margin: 0.25rem;
}

.thread-card-grid {
    display: grid;
    grid-template-columns: 0.1fr .45fr 0.115fr 0.115fr 0.32fr;
}

.thread-card-grid:hover {
    background-color: var(--background-grey-lighter);
}

.thread-card {
    width: 100%;
}

.thread-card #title {
    color: var(--minecraft-green-light);
}

.thread-card + .thread-card:not(:first-child){
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