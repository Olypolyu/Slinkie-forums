import { store } from './store';

/**
 * In this file should be declared all classes destined to be rendered as content and wrappers around the JSON api.
 * Documentation about the API is preffered to be in the backend as this should just be glue code interfacing the HTTP/json requests with JS.
 */

export const serverIP = "http://127.0.0.1:8000";

export class Category {
    constructor(id, title, descriptionID, icon) {
        this.id = id;
        this.title = title;
        this.descriptionID = descriptionID;
        this.icon = icon;
    }
};

export class Thread {
    constructor() {}
    id;
    title;
    authorID;
    date;
    bodyID;
}

export class ContentShard {
    constructor() {}
    id;
    authorID;
    contentType;
    isDataZipped;
    data;
    date;
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
export async function isLoggedIn() {
    const token = localStorage.getItem('token');
    if (token && token != "null") {

        if (JSON.parse(token).header.expiry < new Date().getTime()/1000) {
            return false;
        }

        const response = await fetch(
            `${serverIP}/token/isvalid`, 
            {
                method:"GET",
                headers: {"token":token}
            }
        );

        if (response.status == 200) {
            console.log("Token present in local storage is valid.")
            return true
        }
    }
    return false;
}

export async function logIn(username, password) {
    try {
        const response = await fetch(
            `${serverIP}/token/acquire`,
            {
                method:"POST",
                body: JSON.stringify({
                    username:username,
                    password:password,
                }),
            }
        );

        const data = await response.json();
        if (response.status == 200) {
            console.log("User logged in.")
            localStorage.setItem('token', data.token);
            store.loggedIn = true
        }

        return data.error;
    }

    catch (error) {
        return error.message;
    }
}

export function logOut() {
    store.loggedIn = false;
    localStorage.setItem('token', null);
}

export async function fetchCategories() {
    const response = await (await fetch(`${serverIP}/category`)).json();

    const result = []
    response.forEach(
        cat => { result.push(new Category(cat.id, cat.title, cat.description, cat.icon)) }
    );

    return result;
}