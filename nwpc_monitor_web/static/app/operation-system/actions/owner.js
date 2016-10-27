export const REQUEST_OPERATION_SYSTEM_OWNER_REPOS = 'REQUEST_OPERATION_SYSTEM_OWNER_REPOS';

export function requestOperationSystemOwnerRepos(owner){
    return {
        type: REQUEST_OPERATION_SYSTEM_OWNER_REPOS,
        owner
    }
}

export function fetchOperationSystemOwnerRepos(owner) {
    return function (dispatch) {
        dispatch(requestOperationSystemOwnerRepos(owner));
        return fetch('/api/v1/operation-systems/owners/' + owner + '/repos')
            .then(response => response.json())
            .then(data => dispatch(receiveOperationSystemOwnerReposSuccess({
                    data: data
            })))
    };
}


export const REQUEST_OPERATION_SYSTEM_OWNER_REPOS_FAILURE = 'REQUEST_OPERATION_SYSTEM_OWNER_REPOS_FAILURE';
export function receiveOperationSystemOwnerReposFailure(error){
    return {
        type: REQUEST_OPERATION_SYSTEM_OWNER_REPOS_FAILURE,
        error
    }
}


export const REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS = 'REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveOperationSystemOwnerReposSuccess(response) {
    return {
        type: REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}