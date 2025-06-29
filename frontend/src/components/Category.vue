<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import {Category, fetchContentData, fetchPostsFromCat} from "../Api.ts"
import ThreadCard from "./ThreadCard.vue"
import { useRouter } from 'vue-router'

const router = useRouter();
const props = defineProps(['category', 'startCollapsed']);

const category: Category = props.category;
const threads = ref([]);
const description = ref("");

const collapsed = ref(props.startCollapsed !== undefined);

onMounted(
    async () => {
        description.value = await fetchContentData(category.description)
        .then( async response => {
                const contentType = response.headers.get("content-type");
                console.log(contentType);

                const types = ["text/markdown", "text/html", "application/text"]
                for (let i = 0; i < types.length; i++) {
                    if (contentType.includes(types[i])) {
                        return await response.text();
                    }
                }
            }
        )
        .catch(
            (error) => {
                console.error(error);
                return 'Error fetching content';
            }
        );
        
        threads.value = await fetchPostsFromCat(category.id);
    }
);

</script>

<template >
    <div  class="content card">
        <div class="card-header">
            <p>{{ category.title }}</p>
            <p>Posts </p>
            <p>Replies</p>
            <p>Last Reply</p>
            <button class="thread-header-hide" :class="{ 'thread-header-hide-rot' : collapsed === false}" @click="collapsed = !collapsed" />
            <div class="tooltip">
                <span>{{ description }}</span>
            </div>
        </div>

        <div style="width: 100%; padding: 6px;" v-if="!collapsed" >

            <ThreadCard v-for="thread in threads" :key="post" :post="thread" style="margin-top: 6px; margin-bottom: 6px;" />

            <div v-if="threads.length < 1" style="display: flex; flex-direction: column;">
                <p class="text-subtler" style="text-align: center;"><b>Something has yet to be posted here...</b></p>
                <button style="margin: auto;" @click="router.push(`/category/${category.id}/newthread`)">Create a new Post</button>
            </div>
            
            <div v-else style="width: 100%; display: flex; justify-content: end;">
                <button
                    @click="router.push(`/category/${category.id}/newthread`)"
                >
                    Create a new Post
                </button>
            </div>
            

        </div>
    </div>
</template>

<style scoped>

.card-header {
    display: grid;
    width: calc(100% - 1em);
    height: 2.6em;
    padding: 0;
    align-content: center;
    text-align: center;

    grid-template-columns: .56fr 0.15fr 0.15fr 0.40fr 2em;
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

    .card-header *:nth-child(2), .card-header *:nth-child(3), .card-header *:nth-child(4) {
        visibility: hidden;
        height: 0;
        width: 0;
    }
}

</style>