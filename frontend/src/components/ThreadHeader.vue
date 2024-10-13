<script setup>
import {Category, Post} from "../Api.js"

const props = defineProps(['category']);

/**
 * @type {Category}
 */
const category = props.category;

category.g

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


</template>