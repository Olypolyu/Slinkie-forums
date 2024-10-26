<script setup>
import ThreadHeader from "../components/Category.vue"
import {Category} from "../Api.js"

const categories = [
  new Category("1", "something"),
  new Category("1", "weirdos"),
  new Category("1", "fumos"),
];

</script>

<template>
  <div>
    <div v-for="category in categories" class="content card">
      <ThreadHeader :key="category" :category="category" />
    </div>
  </div>
</template>

