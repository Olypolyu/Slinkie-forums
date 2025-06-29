<script setup>
import { useRoute } from 'vue-router'
import ReplyCard from '../components/ReplyCard.vue';
import {fetchContentData, fetchContentInfo, fetchThread} from "../Api"
import {computed, ref, watch } from 'vue';
import {marked} from 'marked';
import dompurify from 'dompurify';

const route = useRoute()
const threadID = route.params.id;

const thread = ref(null);
const body = ref(null);

fetchThread(threadID).then(r => {thread.value = r});

watch(thread, 
    async () => {
        const metadata = await fetchContentInfo(thread.value.body);
        const resource = await fetchContentData(thread.value.body);

        if (resource.status != 200) throw new Error("Failed to acquire content.");
        
        if (metadata.content_type == "text/markdown") {
            body.value = dompurify.sanitize(marked.parse(await resource.text()))
        }

        else if (metadata.content_type == "text/plain") {
            body.value = resource.text()
        }

        console.log(metadata)
        console.log(body.value)
    }
)

</script>

<template>

    <div class="content card" id="post">
        <div v-if="thread" style="width: 100%;">
            <div style=" width: 95%; margin: auto;">
                <div class="header-grid">
                    <div>
                        <p>Author(s): 
                            <span class="text-subtler" v-for="author in thread.authors"> {{ author }}</span>
                        </p>

                        <p v-if="thread.last_edited">Last Edited:
                            <span class="text-subtler">{{ thread.last_edited }}</span>
                        </p>

                        <p v-if="thread.date">Posted on: 
                            <span class="text-subtler">{{ new Date(thread.date * 1000).toLocaleString() }}</span>
                        </p>
                    </div>

                    <div>
                        <button>share</button>
                        <button>tools</button>
                    </div>
                </div>

                <h1 class="card-header" style="margin-top: 2rem;">{{ thread.title }}</h1>
            </div>

            <div id="content" v-html="body">
            </div>
        </div>

        <div v-else>
            HEHEHEHEH
        </div>

        <span style="margin: 0.75rem;" />
    </div>

    <div class="content card" id="comments">
        <h2 class="card-header">Comments</h2>
        <span style="margin: 0.75rem;" />
        <div style="width: 100%;">
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