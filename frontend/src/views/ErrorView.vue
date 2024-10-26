<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()


</script>

<template>
    <div style="display: flex; flex-direction: column; align-items: center;">
        <h1 class="text-hero">...Oops!</h1>
        <h1 class="text-hero-sub">({{ route.params.status }})</h1>
        <p class="description-large">It seems that something went wrong...</p>
    </div>
</template>

<style scoped>
.text-hero {
    color: var(--minecraft-green-light);
    font-size: 6rem;
}

.text-hero-sub {
    margin-top: -4rem;
    font-size: 3.5rem;
    margin-bottom: 2rem;
}

.description-large {
    font-weight: bold;
    font-size: x-large;
}

</style>