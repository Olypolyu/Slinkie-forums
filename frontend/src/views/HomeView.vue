<script setup>
import ThreadHeader from "../components/Category.vue"
import { fetchCategories } from "../Api.js"
import { ref, onMounted } from "vue";

const categories = ref([]);

onMounted(async () => {
  categories.value = await fetchCategories();
})

</script>

<template>
  <div>
      <div v-for="category in categories" :key="category">
      <ThreadHeader :category="category" />
    </div>
  </div>
</template>