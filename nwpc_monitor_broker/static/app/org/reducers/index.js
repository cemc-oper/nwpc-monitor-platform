import { combineReducers } from 'redux'
import {QUERY_ORG_REPOS, QUERY_ORG_MEMBERS} from '../actions/index'

/* reducer */

//const initialState = {
//    org_repo_list: []
//};

function orgRepos(state = [], action){
    switch(action.type){
        case QUERY_ORG_REPOS:
            console.log(action.owner);
            return [
                {name: 'nwpc_op'},
                {name: 'nwpc_qu'},
                {name: 'eps_nwpc_qu'}
            ];
        default:
            return state;
    }
}

function orgMembers(state = [], action){
    switch(action.type){
        case QUERY_ORG_MEMBERS:
            console.log(action.owner);
            return [
                {name: 'cuiyj'},
                {name: 'wangyt'},
                {name: 'wangdp'},
                {name: 'jiaxzh'}
            ];
        default:
            return state;
    }
}


const orgApp = combineReducers({
    orgRepos,
    orgMembers
});

export default orgApp;