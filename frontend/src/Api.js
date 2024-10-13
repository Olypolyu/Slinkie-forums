export class Category {
    constructor(id, name) {
        this.id = id;
        this.name = name;
    }

    id = "";
    name = "";
    description = "some text";

    get lastPost() {return null};
    
    /**
     * Returns the 5 most recent posts.
     * @returns {[Post]}
     */
    get topPosts() {
        return [
            new Post()
        ]
    };
};

export class Post {
    constructor(title) {
        self.title = title
    }

    authorID = "";
    title = "";
    datePosted = 0;

    get metrics()  {return null};
    get lastReply() {return null};
}

