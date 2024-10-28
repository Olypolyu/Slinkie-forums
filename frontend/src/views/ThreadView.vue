<script setup>
import { useRoute } from 'vue-router'
import ReplyCard from '../components/ReplyCard.vue';
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
            <h1 class="card-header" style="margin-top: 2rem;">A awesome thread</h1>
        </div>

        <div id="content">
            <h1>Heading 1</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
            <h2>Heading 2</h2>
            <img src="https://www.gamepur.com/wp-content/uploads/wp-content/uploads/2018/06/01150810/additional-structures-850x478.jpg">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>
        <span style="margin: 0.75rem;" />
    </div>

    <div class="content card" id="comments">
        <h2 class="card-header">Comments</h2>
        <span style="margin: 0.75rem;" />
        <div style="width: 85%;">
            <ReplyCard />
            <ReplyCard />
            <ReplyCard />
        </div>
    </div>

</template>

<style scoped>

#content {
    padding: 1rem;
}

#content > p {
    line-height: 1.5rem;
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