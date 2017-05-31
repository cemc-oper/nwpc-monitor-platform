import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import {
    REQUEST_ADD_HPC_USER_DISK_USAGE,
    ADD_HPC_USER_DISK_USAGE_SUCCESS,
    CLEAR_HPC_DISK_USAGE_USERS
} from '../actions/disk_usage'
import {
    REQUEST_HPC_USER_LOADLEVELER_STATUS,
    RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS,
    REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS,
    RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS
} from '../actions/loadleveler_status'

import {
    REQUEST_HPC_DISK_SPACE,
    RECEIVE_HPC_DISK_SPACE_SUCCESS
} from '../actions/disk_space'

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

function disk_space_reducer(state={
    status: {
        is_fetching: false,
        last_updated: null
    },
    file_systems: [],
    time: null
}, action) {
    switch (action.type) {
        case REQUEST_HPC_DISK_SPACE:
            return  new Object({
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                },
                file_systems: state.file_systems,
                time: state.time,
            });
        case RECEIVE_HPC_DISK_SPACE_SUCCESS:
            let file_systems = action.response.data.message.data.response.file_systems;

            file_systems.sort(function(a,b){
                let a_file_system = a.file_system.toUpperCase();
                let b_file_system = b.file_system.toUpperCase();
                if( a_file_system < b_file_system){
                    return -1;
                } else if(a_file_system > b_file_system){
                    return 1;
                } else {
                    return 0;
                }
            });

            return new Object({
                status: {
                    is_fetching: false,
                    last_updated: Date.now()
                },
                file_systems: file_systems,
                time: action.response.data.message.time,
            });
        default:
            return state;
    }
}

function loadleveler_status_reducer(state={
    loadleveler_status: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        user: null,
        collect_time: null,
        jobs: [],
        abnormal_jobs: {
            update_time: null,
            abnormal_jobs_id: null,
            plugin_name: null,
            abnormal_job_list: []
        }
    }
}, action) {
    switch(action.type){
        case REQUEST_HPC_USER_LOADLEVELER_STATUS:
        case REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS:
            return new Object({
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                },
                user: state.user,
                collect_time: state.collect_time,
                jobs: state.jobs,
                abnormal_jobs: state.abnormal_jobs
            });
        case RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS:
            let data = action.response.data;
            let message = data['message'];
            let collect_time = message['time'];
            let user = data['user'];
            let jobs = message['data']['response']['items'];
            return new Object({
                status: {
                    is_fetching: false,
                    last_updated: Date.now()
                },
                user: user,
                collect_time: collect_time,
                jobs: jobs,
                abnormal_jobs: state.abnormal_jobs
            });
        case RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS:
            data = action.response.data;
            let abnormal_jobs = {
                update_time: data['update_time'],
                plugin_name: data['plugin_name'],
                abnormal_jobs_id: data['abnormal_jobs_id'],
                abnormal_job_list: data['abnormal_job_list']
            };
            return new Object({
                status: {
                    is_fetching: false,
                    last_updated: Date.now()
                },
                user: state.user,
                collect_time: state.collect_time,
                jobs: state.jobs,
                abnormal_jobs: abnormal_jobs
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
    },
    disk_space: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        file_systems: [],
        time: null
    },
    loadleveler_status: {
        status: {
            is_fetching: false,
            last_updated: null
        },
        user: null,
        collect_time: null,
        jobs: [],
        abnormal_jobs: {
            update_time: null,
            abnormal_jobs_id: null,
            plugin_name: null,
            abnormal_job_list: []
        }
    }
}, action) {
    switch (action.type) {
        case REQUEST_ADD_HPC_USER_DISK_USAGE:
        case ADD_HPC_USER_DISK_USAGE_SUCCESS:
        case CLEAR_HPC_DISK_USAGE_USERS:
            return new Object({
                disk_usage: disk_usage_reducer(state.disk_usage, action),
                disk_space: state.disk_space,
                loadleveler_status: state.loadleveler_status
            });
        case REQUEST_HPC_USER_LOADLEVELER_STATUS:
        case RECEIVE_HPC_USER_LOADLEVELER_STATUS_SUCCESS:
        case REQUEST_HPC_USER_LOADLEVELER_ABNORMAL_JOBS:
        case RECEIVE_HPC_USER_LOADLEVELER_ABNORMAL_JOBS_SUCCESS:
            return new Object({
                disk_usage: state.disk_usage,
                disk_space: state.disk_space,
                loadleveler_status: loadleveler_status_reducer(state.loadleveler_status, action)
            });
        case REQUEST_HPC_DISK_SPACE:
        case RECEIVE_HPC_DISK_SPACE_SUCCESS:
            return new Object({
                disk_usage: state.disk_usage,
                disk_space: disk_space_reducer(state.disk_space, action),
                loadleveler_status: state.loadleveler_status
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