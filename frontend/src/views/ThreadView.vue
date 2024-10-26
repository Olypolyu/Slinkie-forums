<script setup>
import { useRoute } from 'vue-router'
import CommentCard from '../components/CommentCard.vue';
const route = useRoute()

</script>

<template>
    <div class="content card" id="post">
        <div style=" width: 95%;">
            <div class="header-grid">
                <div>
                    <p>Author(s): <span class="text-subtler">Kheprep, Kheppie, Khepster</span></p>
                    <p>Last Edited: <span class="text-subtler">26/10/24 2:04am</span></p>
                </div>
                <div>
                    <button>share</button>
                    <button>tools</button>
                </div>
            </div>
            <h2 class="card-header" style="margin-top: 2rem;">Tittle</h2>
        </div>

        <span style="margin: 0.75rem;" />
        <div name="content">
            <p>well, i am writing this so i have some boiler plate to view this as</p>
        </div>
        <span style="margin: 0.75rem;" />
    </div>

    <div class="content card" id="comments">
        <h2 class="card-header">Comments</h2>
        <span style="margin: 0.75rem;" />
        <div style="width: 85%;">
            <CommentCard />
        </div>
    </div>

</template>

<style scoped>
h2 {
    margin: 0.25rem;
}

.header-grid {
    display: grid;
    justify-content: space-between;
    grid-template-columns: repeat(2, auto);
}

@media screen and (max-width: 750px) {
    .header-grid{
        grid-template-columns: auto;
    }
}

</style>