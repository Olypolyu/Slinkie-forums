<template>

<div class="content-card" style="background-color: var(--background-grey-mild);">
    <div class="comment-card">
        <div class="profile-picture-card text-dense text-subtle">
            <div style="background-color: red; width: 6rem; height: 6rem;"/>
            <p>Author: <span class="text-subtler">Belizarius cawl</span></p>
            <p>Last Edited: <span class="text-subtler">26/10/24 2:04am</span></p>
        </div>
        <hr>
        <div style="padding: 1rem;">
            I am content.
        </div>
    </div>
    <div class="quote">
        Sometimes... I dream about cheese.
    </div>
    <div style="margin: 0.5rem;">
        <button>Like</button>
        <button>Reply</button>
        <button>Share</button>
    </div>
</div>

</template>

<style> 

.quote {
    padding: 2rem;
    margin-left: 2rem;
    margin-right: 2rem;
    margin-bottom: 1rem;

    background-color: var(--background-grey-light);
    border: 1px solid var(--minecraft-green-light);
    border-radius: 6px;
}

.comment-card {
    display: flex;
    gap: var(--section-gap);

    width: 100%;
    padding: 2rem;
    margin: 0;
}

.profile-picture-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 6px;
    width: 15%;

    p {
        margin-bottom: 0;
    }

}

</style>

