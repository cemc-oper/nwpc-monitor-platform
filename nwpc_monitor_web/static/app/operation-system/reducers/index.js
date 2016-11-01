import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import {
    REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS,
    REQUEST_OPERATION_SYSTEM_REPO_STATUS_SUCCESS
} from '../actions/owner'

import {
    REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS,
} from '../actions/repo'

function owner_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    repos_status: []
}, action){
    switch(action.type){
        case REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS:
            // return Object.assign({}, state, {
            //     repos_status: action.response.data
            // });
            return new Object({
                status: state.status,
                repos_status: action.response.data
            });
        default:
            return state;
    }
}

function repo_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    node_status: null,
    aborted_tasks: null
}, action){
    switch(action.type){
        case REQUEST_OPERATION_SYSTEM_REPO_STATUS_SUCCESS:
            // return Object.assign({}, state, {
            //     node_status: action.response.data.data.node_status
            // });
            return  new Object({
                status: state.status,
                node_status: action.response.data.data.node_status,
                aborted_tasks: status.aborted_tasks
            });
        case REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS:
            return  new Object({
                status: state.status,
                node_status: status.node_status,
                aborted_tasks: action.response.data
            });
        default:
            return state;
    }
}


function operation_system_reducer(state={
    owner: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        repos_status: []
    },
    repo: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        node_status: null,
        aborted_tasks: null
    }
}, action){
    switch(action.type){
        case REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS:
            // return Object.assign({}, state, {
            //     owner: owner_reducer(state.owner, action)
            // });
            return  new Object({
                owner: owner_reducer(state.owner, action),
                repo: state.repo
            });
        case REQUEST_OPERATION_SYSTEM_REPO_STATUS_SUCCESS:
        case REQUEST_OPERATION_SYSTEM_REPO_ABORTED_TASKS_SUCCESS:
            // return Object.assign({}, state, {
            //     repo: repo_reducer(state.repo, action)
            // });
            return  new Object({
                owner: state.owner,
                repo: repo_reducer(state.repo, action)
            });
        default:
            return state;
    }
}

const operationSystemAppReducer = combineReducers({
    operation_system: operation_system_reducer,
    routing
});

export default operationSystemAppReducer;