import { combineReducers } from 'redux'
import { createStore } from 'redux';

/* action */
export const QUERY_ORG_REPOS = 'QUERY_ORG_REPOS';
export const QUERY_ORG_MEMBERS = 'QUERY_ORG_MEMBERS';

/* action create function */
export function queryOrgRepos(owner){
    return {
        type: QUERY_ORG_REPOS,
        owner
    }
}

export function queryOrgMembers(owner){
    return {
        type: QUERY_ORG_MEMBERS,
        owner
    }
}
