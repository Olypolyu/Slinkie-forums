<script setup>
import ThreadHeader from "../components/Category.vue"
import { fetchCategories } from "../Api.ts"
import { ref, onMounted } from "vue";

const categories = ref([]);

onMounted(async () => {
  categories.value = await fetchCategories();
})

</script>

<template>
    <div>
        <div style="margin: auto; width: fit-content; text-align: center; margin-bottom: 6em; margin-top: 3em;">
            <h2>Welcome!</h2>
            <input type="search" placeholder="search">
        </div>

        <div v-for="category in categories" :key="category">
            <ThreadHeader :category="category" />
        </div>
    </div>
</template>