import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import {
    REQUEST_ADD_HPC_USER_DISK_USAGE,
    ADD_HPC_USER_DISK_USAGE_SUCCESS,
    CLEAR_HPC_DISK_USAGE_USERS
} from '../actions/disk_usage'


function disk_usage_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    users: []
}, action){
    switch(action.type){
        case REQUEST_ADD_HPC_USER_DISK_USAGE:
            return  new Object({
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                },
                users: state.users,
            });
            break;
        case ADD_HPC_USER_DISK_USAGE_SUCCESS:
            let new_user = new Object({
                user: state.user,
                file_systems: state.file_systems,
                time: state.time
            });

            let disk_usage_data = action.response.data['message']['data'];
            new_user.user = disk_usage_data['response']['user'];
            new_user.file_systems = disk_usage_data['response']['file_systems'];
            new_user.time = action.response.data['message']['time'];

            return  new Object({
                status: {
                    is_fetching: false,
                    last_updated: new Date()
                },
                users: [
                    new_user,
                    ...state.users
                ]
            });
        case CLEAR_HPC_DISK_USAGE_USERS:
            return  new Object({
                status: {
                    is_fetching: false,
                    last_updated: state.status.last_updated
                },
                users: []
            });
        default:
            return state;
    }
}

function hpc_reducer(state={
    disk_usage: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        users: []
    }
}, action) {
    switch (action.type) {
        case ADD_HPC_USER_DISK_USAGE_SUCCESS:
        case CLEAR_HPC_DISK_USAGE_USERS:
            return new Object({
                disk_usage: disk_usage_reducer(state.disk_usage, action)
            });
        default:
            return state;
    }
}

const hpcAppReducer = combineReducers({
    hpc: hpc_reducer,
    routing
});

export default hpcAppReducer;