<script setup>
    import { onMounted } from 'vue'
    const props = defineProps(['name'])

    onMounted(
        function() {
            const modal = document.body.querySelector(".modal")
            const modalBackground = document.body.querySelector(".modal-background");
            modalBackground.style.paddingTop = `calc(50vh - ${modal.clientHeight/2}px)`;
            addEventListener("resize", 
                (event) => {
                    modalBackground.style.paddingTop = `calc(50vh - ${modal.clientHeight/2}px)`
                }
            );
        }
    );

</script>

<template>
    <div class="modal-background">
        <div class="modal">
            <div class="modal-header">
                <slot name=header />
            </div>
            <hr v-if="this.$slots.header">
            <div class="modal-content">
                <slot />
            </div>
            <hr v-if="this.$slots.footer">
            <div>
                <slot name=footer />
            </div>
        </div>
    </div>
</template>

<style>

.modal-background {
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal {
    margin: auto;
    padding: 0px;
    width: 40rem;
    height: 20rem;
    max-width: 80%;

    background-color: var(--background-grey-light);
    border: 2px solid var(--background-grey-lighter);
}

.modal-content {
    padding: var(--section-gap);
    text-align: center;
}

.modal-header {
    display: flex;
    flex-direction: row;
    padding: var(--section-gap);
    padding-bottom: 0;
}

</style>