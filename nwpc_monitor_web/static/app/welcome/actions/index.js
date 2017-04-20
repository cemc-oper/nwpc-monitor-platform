export const REQUEST_USER_INFO = "REQUEST_USER_INFO";

export function requestUserInfo(code){
    return {
        type: REQUEST_USER_INFO,
        code
    }
}

export const RECEIVE_USER_INFO = "RECEIVE_USER_INFO";

export function receiveUserInfo(response){
    return {
        type: RECEIVE_USER_INFO,
        response,
        receive_time: Date.now()
    }
}

export function fetchUserInfo(code){
    return function (dispatch){
        dispatch(requestUserInfo(code));
        return $.getJSON(
            '/api/v1/user/info?code=' + code,
            {},
            function(data){
                dispatch(receiveUserInfo({
                    data: data
                }))
            }
        )
    };
}
