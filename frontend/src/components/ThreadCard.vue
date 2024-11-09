<script setup>
import {computed, ref} from 'vue'
import { fetchContent, Thread } from '../Api';
import { useRouter } from 'vue-router';

const props = defineProps([
    'post'
])

/**  @type Thread
*/
const post = ref(props.post);
const router = useRouter();

console.log(post.value)
function pushToThread() {router.push({path: `/thread/${post.value.bodyID}`})};

const description = computed(
    async () => {
        const result = await (await fetchContent(post.value.bodyID)).text();
        console.log(result);
        return result;
    }
);

</script>

<template>
    <div class="thread-card-wrapper" @click="pushToThread">
        <div class="thread-card" tabindex="0" @click="console.log('hi')" @keyup='function (event) {if (event.key == "Enter") event.target.click()}' role="button">
            <img :key="src" :src="post.icon" class="icon" />
            <div style="padding: var(--section-gap);">
                <h4 style="color: var(--minecraft-green)">{{ post.title }}</h4>
                <p class="text-subtle text-dense">{{ description }}</p>
            </div>
            <div class="text-subtle text-dense thread-card-text-center">
                <p>3012<span class="text-subtler">/week</span></p>
            </div>
            <div class="text-subtle text-dense thread-card-text-center">
                <p>45056<span class="text-subtler">/week</span></p>
            </div>
            <div class="text-subtle text-dense thread-card-text-center">
                <p><b>&lt;Joe Shmoe&gt;: </b>WOW! i couldn't believe he could do such a thing........... </p>
                <p>it is trully horrifying psychos like this are allowed to develop our minecraft mods!</p>
            </div>
        </div>
    </div>
</template>

<style scoped>

.icon {
    width:  4em;
    height: 4em;
    margin: 0.5rem;
    place-self: center;
}

.text-subtler { white-space: nowrap;}

.thread-card {
    cursor: pointer;
    display: grid;
    row-gap: 0;
    grid-template-areas: "icon debrief post replies";
    grid-template-columns: auto .60fr 0.12fr 0.12fr .55fr;
}

.thread-card:hover, .thread-card:focus {
    background-color: var(--background-grey-lighter);
}

.thread-card p, .thread-card h4 {margin: 0.5em;}

.thread-card-text-center {
    align-content: center;
    justify-content: center;
    padding: var(--section-gap);
}

.thread-card-wrapper {
    width: 100%;
}

.thread-card-wrapper #title {
    color: var(--minecraft-green-light);
}

.thread-card-wrapper + .thread-card-wrapper:not(:first-child){
    &::before {
        display: block;
        content: '';

        width: 60%;
        border-bottom: 2px solid var(--text-subtle);
        border-spacing: var(--section-gap);
        margin:  calc(var(--section-gap) * 1.5);
        margin-left: auto;
        margin-right: auto;
    }
}

@media screen and (max-width: 750px) {
    .thread-card {
        grid-template-areas: 
            "icon debrief"
            "post replies";

        grid-template-columns: 0.1fr .9fr;
        grid-template-rows: 6em;
    }

    .thread-card *:nth-child(3), .thread-card *:nth-child(4) {
        width: fit-content;
    }

    .thread-card *:nth-child(3)::before, .thread-card *:nth-child(4)::before {
        display: inline-block;
        width: 100%;
        font-weight: 800;
        text-align: center;
    }

    .thread-card *:nth-child(3)::before { content: "Replies:"; }
    .thread-card *:nth-child(4)::before { content: "Posts:"; }

    .thread-card *:nth-child(5) {
        visibility: hidden;
        height: 0;
        width: 0;
        margin: -100000em; /* IDK either, it just works:tm: */
    }
}

</style>