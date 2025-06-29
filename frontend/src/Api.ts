import { store } from './store';
import { b64EncodeUnicode } from './util';

/**
 * In this file should be declared all classes destined to be rendered as content and wrappers around the JSON api.
 * Documentation about the API is preffered to be in the backend as this should just be glue code interfacing the HTTP/json requests with JS.
 */

export const serverIP = "http://127.0.0.1:8000";

export type Category = {
    id: number;
    title: string;
    description: number;
    icon: string;
}

export type Thread = {
    id: number
    title: string
    date: number
    body: number
}

export type ContentShard = {
    id: number;
    author: number;
    date: number;
    content_type: string;
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

        try {
            if (JSON.parse(token).header.expiry < new Date().getTime()/1000) {
                return false;
            }
        }
        catch {return false};

        try {
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
        catch {return false};
    }
    return false;
}

export async function logIn(username = null, password, userID = null) {
    try {
        const response = await fetch(
            `${serverIP}/token/acquire`,
            {
                method:"POST",
                headers: { "Content-Type": "application/json", mode: 'no-cors'},
                body: JSON.stringify({
                    username:String(username),
                    password:String(password),
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
    return response;
}

export async function fetchContentData(id): Promise<Response>  {
    const response = await fetch(
        `${serverIP}/content/${id}`,
        {
            method: "GET",
            headers: {
                mode: 'no-cors',
                token: localStorage.getItem('token')
            }
        }
    );

    return response
}

export async function fetchContentInfo(id): Promise<ContentShard>  {
    const response = await fetch(
        `${serverIP}/content/${id}/info`,
        {
            method: "GET",
            headers: {
                mode: 'no-cors',
                token: localStorage.getItem('token')
            }
        }
    ).then(r => r.json());

    return response
}

export async function fetchRemoteDescription(id): Promise<string> {
    return ""
}

export async function fetchPostsFromCat(categoryID): Promise<Thread[]> {
    const response = await (
        await fetch(
            `${serverIP}/category/${categoryID}`,
            {
                method: "GET",
                headers: {
                    mode: 'no-cors',
                    token: localStorage.getItem('token')
                }
            }
        )
    ).json();

    return response;
}

export async function fetchThread(threadID) {
    const response = await fetch(
        `${serverIP}/thread/${threadID}`,
        {
            method:"GET",
            headers: { 
                "Content-Type": "application/json",
                mode: 'no-cors',
                token: localStorage.getItem('token')
            },
        }
    ).then(r => r.json());

    return response;
}

export async function makeThread(
    title: string,
    category: number,
    body_content: string,
    body_mime_type: string,
    allow_replies: boolean,
) {
    const response = await fetch(
        `${serverIP}/thread`,
        {
            method:"POST",
            headers: { 
                "Content-Type": "application/json",
                mode: 'no-cors',
                token: localStorage.getItem('token')
            },

            body: JSON.stringify({
                title:          title,
                category:       category,
                body_content:   b64EncodeUnicode(body_content),
                body_mime_type: body_mime_type,
                allow_replies:  allow_replies,
                attachments: []
            }),
        }
    );

    return response.json();
}