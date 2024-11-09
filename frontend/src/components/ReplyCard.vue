<template>

<div>
    <div class="reply-card">
        <div class="profile-picture-container text-dense text-subtle">
            <img style="width: 5rem; height: 5rem;" src="https://i.pinimg.com/736x/d2/77/2e/d2772eb4b802b536e1ad4bcab5876787.jpg"/>
            <span class="role">Admin</span>
            <p>Author: <span class="text-subtler">Belizarius cawl</span></p>
            <p>Last Edited: <span class="text-subtler">26/10/24 2:04am</span></p>
        </div>
        <div class="content">
            <p> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
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

<style scoped>

.role {
    background-color: brown;
    color: white;
    font-weight: bolder;
    margin: 0.25rem;
    padding: 4px;
    border-radius: 6px;
}

.content {
    margin: 0.5rem;

    > p:first-child {
        margin-top: 0;
    }

    > p::first-letter {
        margin-left: 2rem;
    }
}

.quote {
    margin-left: 2rem;
    margin-right: 2rem;
    margin-bottom: 1rem;
    padding: 1rem;
    min-height: 3rem;

    background-color: rgba(5, 98, 37, 0.25);
    border: 2px dashed var(--minecraft-green-light);
    border-radius: 6px;
}

.reply-card {
    display: flex;
    gap: var(--section-gap);

    padding: 1rem;
}

div:has(> .reply-card) {
    background-color: var(--background-grey-mild);
    margin-bottom: 2rem;
}

.profile-picture-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 6px;
    width: 5.5rem;

    p {
        margin-bottom: 0;
    }

}

</style>

