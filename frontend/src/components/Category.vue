<script setup>
import {ref} from 'vue'
import {Category} from "../Api.js"
import ThreadCard from "./ThreadCard.vue"

const props = defineProps(['category', 'startCollapsed']);

/**
 * @type {Category}
 */
const category = props.category;
const posts = ref(category.topPosts);
const collapsed = ref(props.startCollapsed !== undefined);
console.log(collapsed);

</script>

<template>
        <div class="card-header">
            <p>
                {{category.name}}
            </p>
            <p>Posts </p>
            <p>Replies</p>
            <p>Last Reply</p>
            <button class="thread-header-hide" :class="{ 'thread-header-hide-rot' : collapsed === false}" @click="collapsed = !collapsed" />
        </div>
    
    <div v-if="!collapsed">
        <span style="margin: 0.75rem;" />
        <div style="width: 95%; padding: 0.5rem;">
            <ThreadCard v-for="post in posts" :key="post" :post="post"/>
        </div>
    </div>
</template>

<style scoped>

.card-header {
    display: grid;
    width: calc(100% - 1em);
    height: 1.5em;
    grid-template-columns: .56fr 0.15fr 0.15fr 0.40fr 2em;
    text-align: center;
}

.thread-header-hide {
    color: white;
    background-color: none;
    border: none;
    margin: auto;
    padding: 0;
    height: 2em;
    width: 2em;
}

.thread-header-hide::after {
    transition: cubic-bezier(0.075, 0.82, 0.165, 1) 0.5s;
    display: inline-block;
    content: "▶";
    font-size: large;
    font-weight: bolder;
    text-shadow: none;
    text-align: center;
    vertical-align: middle;
}

.thread-header-hide-rot::after {
    transform: rotate(90deg);
}

@media screen and (max-width: 750px) {
    .card-header {
        grid-template-columns: calc(100% - 2em) 0px 0px 0px 0px 4em;
    }

    .card-header *:nth-child(1) {
        padding-left: 1.75em;
    }

    .card-header *:nth-child(2), .card-header *:nth-child(3), .card-header *:nth-child(4) {
        visibility: hidden;
        height: 0;
        width: 0;
    }
}

</style>