import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import { REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS } from '../actions/owner'

function owner_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    repos_status: []
}, action){
    switch(action.type){
        case REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS:
            return Object.assign({}, state, {
                repos_status: action.response.data
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
    }
}, action){
    switch(action.type){
        case REQUEST_OPERATION_SYSTEM_OWNER_REPOS_SUCCESS:
            return Object.assign({}, state, {
                owner: owner_reducer(state.owner, action)
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