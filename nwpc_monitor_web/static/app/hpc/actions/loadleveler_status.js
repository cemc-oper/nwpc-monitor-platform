export const REQUEST_HPC_USER_LOADLEVELER_STATUS = 'REQUEST_HPC_USER_LOADLEVELER_STATUS';

export function requestHpcUserLoadlevelerStatus(user){
    return {
        type: REQUEST_HPC_USER_LOADLEVELER_STATUS,
        user
    }
}

export const RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS = 'RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS';

export function receiveHpcUserLoadlevelerStatusSuccess(response){
    return {
        type: RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}

export const RECEIVE_HPC_USER_LOADLEVELER_STATUS_FAILURE = 'RECEIVE_HPC_USER_LOADLEVELER_STATUS_FAILURE';

export function receiveHpcUserLoadlevelerStatusFailure(error){
    return {
        type: RECEIVE_HPC_USER_LOADLEVELER_STATUS_FAILURE,
        error
    }
}

export function fetchHpcUserLoadlevelerStatus(user){
    return function (dispatch) {
        dispatch(requestHpcUserLoadlevelerStatus(user));

        return $.getJSON('/api/v1/hpc/users/' + user + '/loadleveler/status', {} ,function(data){
            dispatch(
                receiveHpcUserLoadlevelerStatusSuccess({
                    data: data
                })
            );
        });
    };
}