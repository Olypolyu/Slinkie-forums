<script setup>
    const model = defineModel()
</script>

<template>
    <div class="outer">
        <input type="checkbox" v-model="model">
    </div>
</template>

<style lang="css" scoped>
    .outer {
        width: 40px;
        height: 22px;
        border-radius: 1em;

        margin: 6px;
        overflow: hidden;

        input[type=checkbox]{
            position: relative;
            bottom: 18px;

            height: 100%;
            width: 100%;
            margin: 0px;
            opacity: 0;
            cursor: pointer;
        }

        transition: background-color 200ms;
        background-color: var(--background-grey-dark);
        outline: solid 1px var(--background-grey-mild);

        &:has(> input[type=checkbox]:checked) {
            background-color: var(--minecraft-green-dark);
        }

        &::before {
            pointer-events: none;
            transition: left 200ms, width 200ms;

            display: block;
            content: " ";
            width: 18px;
            height: 18px;
            border-radius: 2em;

            position: relative;
            top: 2px;
            left: 2px;

            background-color: var(--text-subtle);
        }

        &:active::before {
            width: 22px;
        }

        &:has(> input[type=checkbox]:checked) {
            &::before {
                left: 20px;
                background-color: var(--minecraft-green-light);
                box-shadow: 0px 0px 12px 1px rgba(0, 0, 0, 0.664);
            }
            
            &:active::before {
                width: 22px;
                left: 16px;
            }
        }
    }
</style>