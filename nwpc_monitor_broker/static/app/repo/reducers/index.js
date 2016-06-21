import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import {
    REQUEST_DING_TALK_WARNING_WATCH_USERS,
    RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS,
    RECEIVE_DING_TALK_WARNING_WATCH_USERS_FAILURE
} from '../actions'


function repo(state={
    warning: {
        ding_talk:{
            owner: null,
            repo: repo,
            watching_user_list: []
        }
    }
}, action){
    switch(action.type){
        case RECEIVE_DING_TALK_WARNING_WATCH_USERS_SUCCESS:
            return Object.assign({}, state, {
                warning: {
                    ding_talk: {
                        owner: action.response.data.data.owner,
                        repo: action.response.data.data.repo,
                        watching_user_list: action.response.data.data.warning.watching_user_list
                    }
                }
            });
        default:
            return state;
    }
}



const repoAppReducer = combineReducers({
    repo,
    routing
});

export default repoAppReducer;