export const REQUEST_USER_INFO = "REQUEST_USER_INFO";

export function requestUserInfo(code){
    return {
        type: REQUEST_USER_INFO,
        code
    }
}

export function fetchUserInfo(code){
    return {

    }
}
