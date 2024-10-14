<script setup>
import ThreadHeader from "../components/ThreadHeader.vue"
import {Category, Post} from "../Api.js"

const categories = [
  new Category("1", "something"),
  new Category("1", "weirdos"),
  new Category("1", "fumos"),
];

</script>

<template>
  <div v-for="category in categories" class="content card">
    <ThreadHeader :key="category" :category="category" />
  </div>
</template>

