import { reactive, ref } from 'vue'
import { isLoggedIn } from './Api'

/**
 *  Global state goes here. This is *not* saved when the page closes.
 * For anything meaningful, please save to localStorage instead.
 */
export const store = reactive({
    loggedIn: ref(await isLoggedIn())
})