export const REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS = 'REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS';

export function requestOperationSystemRepoAbortedTasks(owner, repo, id){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS,
        owner,
        repo,
        id
    }
}

export function fetchOperationSystemRepoAbortedTasks(owner, repo, id) {
    return function (dispatch) {
        dispatch(requestOperationSystemRepoAbortedTasks(owner, repo, id));
        
        return $.getJSON('/api/v1/operation-systems/repos/' + owner + '/' + repo + '/aborted_tasks/' + id, {} ,function(data){
            dispatch(receiveOperationSystemRepoAbortedTasksSuccess({
                data: data
            }));
        });
    };
}


export const REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_FAILURE = 'REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_FAILURE';
export function receiveOperationSystemRepoAbortedTasksFailure(error){
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_FAILURE,
        error
    }
}


export const REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS = 'REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS';
export function receiveOperationSystemRepoAbortedTasksSuccess(response) {
    return {
        type: REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}