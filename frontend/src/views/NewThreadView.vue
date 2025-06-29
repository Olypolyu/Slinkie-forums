<script type="module" setup lang="ts">
    import { MdEditor } from 'md-editor-v3';
    import 'md-editor-v3/lib/style.css';

    import ToggleSwitch from "../components/ToggleSwitch.vue"
    import { fetchCategories, makeThread } from "../Api.ts"
    import { useRoute, useRouter } from "vue-router";
    import { ref } from "vue";

    const route = useRoute();
    const router = useRouter();
    
    const categoryID = Number(route.params.id);

    const category = ref(null);
    (fetchCategories()).then( cats => {category.value = cats.find(cat => cat.id == categoryID)});

    function cancel() {
        router.back();
    }

    const title = ref("");
    const text = ref("");
    const allowReply = ref(true);

    function post() {
        console.log(allowReply.value);
        console.log(text.value);
        console.log(title.value);

        const thread = makeThread(
            title.value,
            categoryID,
            text.value,
            "text/markdown",
            allowReply.value
        )
        
        thread.then( r => router.push(`/thread/${r.id}`))
    }

    const editorToolbar = [
        'bold', 'underline', 'italic',
        '-',
        'title', 'strikeThrough', 'sub', 'sup', 'quote', 'unorderedList', 'orderedList', 'task',
        '-',
        'codeRow', 'code', 'link', 'image', 'table', 'mermaid', 'katex',
        '-',
        'revoke', 'next', 'save',
        '=',
        'pageFullscreen', 'preview', 'previewOnly',
    ];
</script>

<script lang="ts">

</script>

<template>
    <div class="content card" style="padding: 0px;">
        <h3 v-if="category" class="text-subtle" style="margin: 12px; align-self: flex-start;">/{{ category.title }}</h3>
        <div style="display: flex; flex-direction: column; margin: 12px;">
            <input type="text" v-model="title" placeholder="Title" style="margin: 0px; margin-bottom: 12px;">
            <MdEditor v-model="text" theme="dark" :toolbars=editorToolbar />
        </div>

        <div style="align-self: self-start; margin: 6px;">
            <div style="display: grid; grid-template-columns: auto 1fr; margin-bottom: 6px;">
                <ToggleSwitch v-model="allowReply"/> <p style="margin: 0px; align-self: center;">Allow Replies</p>
            </div>

            <div style="display: grid; grid-template-columns: 6em 6em;">
                <button 
                    @click="post"
                    :disabled="title.length < 1 || text.length < 1"
                >Post</button>
                <button class="outline" @click="cancel">Cancel</button>
            </div>
        </div>
    </div>
        
</template>