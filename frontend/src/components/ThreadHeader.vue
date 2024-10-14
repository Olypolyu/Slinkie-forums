<script setup>
import {ref} from 'vue'
import {Category, Post} from "../Api.js"
import ThreadCard from "./ThreadCard.vue"

const props = defineProps(['category']);

/**
 * @type {Category}
 */
const category = props.category;
const posts = ref(category.topPosts)

</script>

<template>
        <div class="card-header" style="display: flex; flex-direction: row;">
            <p style="width:50%">
                {{category.name}}
            </p>
            <p style="width:10%;">Posts </p>
            <p style="width:10%;">Replies</p>
            <p style="width:25%; text-align: end;">Last Reply</p>
        </div>
    
    <span style="margin: 0.75rem;" />
    <div style="width: 95%; padding: 0.5rem;">
        <ThreadCard v-for="post in posts" :key="post" :post="post"/>
    </div>
</template>