/**
 * In this file should be declared all classes destined to be rendered as content and wrappers around the JSON api.
 * Documentation about the API is preffered to be in the backend as this should just be glue code interfacing the HTTP/json requests with JS.
 */

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
            new Post("i am"),
            new Post("trying"),
            new Post("cheese cake yummy"),
            new Post("but society"),
            new Post("won't allow"),
        ]
    };
};

export class Post {
    constructor(title) {
        this.title = title
    }

    authorID = "";
    title = "";
    datePosted = 0;

    /**
     * returns image src for the little icon.
     * @returns {string}
     */
    get icon() {
        return '/src/assets/talk.png';
    };

    get iconAltText() {
        return "a beutiful conversation";
    };

    get metrics()  {return null};
    get lastReply() {return null};
}

/**
 * Returns if the user is currently logged in. Used for the nav.
 * The way it's supposed to work is simple: 
 *  1. check the cookies for a login token, if none, we are not logged in.
 *  2. check expiry date on the token, if past, we are not logged in.
 *  - 2.1. if not past expiry date, and if the it expires in 4 days or less, tell the server to refresh the token.
 *  - 2.2. if we successfully refreshed the token, save that to localStorage.
 *  3. return whether the current token is valid.
 *
 * @returns {boolean}
 */
export function isLoggedIn() {return false};

export function getUserData(id) {
    return null;
};
