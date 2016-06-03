import { combineReducers } from 'redux'
import fetch from 'isomorphic-fetch'

// 用于用户操作的 action

export const QUERY_ORG_REPOS = 'QUERY_ORG_REPOS';
export const QUERY_ORG_MEMBERS = 'QUERY_ORG_MEMBERS';

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

// 与网络请求相关的 action

export const REQUEST_ORG_REPOS = 'REQUEST_ORG_REPOS';
export function requestOrgRepos(owner){
    return {
        type: REQUEST_ORG_REPOS,
        owner
    }
}

export function fetchOrgRepos(owner) {
    return function (dispatch) {
        dispatch(requestOrgRepos(owner));
        return fetch('/api/v2/orgs/nwp_xp/repos')
            .then(response => response.json())
            .then(data => dispatch(receiveOrgReposSuccess({
                    data: data
            })))
    };
}


export const RECEIVE_ORG_REPOS_FAILURE = 'RECEIVE_ORG_REPOS_FAILURE';
export function receiveOrgReposFailure(error){
    return {
        type: RECEIVE_ORG_REPOS_FAILURE,
        error
    }
}


export const RECEIVE_ORG_REPOS_SUCCESS = 'RECEIVE_ORG_REPOS_SUCCESS';
/**
 *
 * @param response
 *      {
 *          data:[]
 *      }
 * @returns {{type: string, response: *, receive_time: number}}
 */
export function receiveOrgReposSuccess(response) {
    return {
        type: RECEIVE_ORG_REPOS_SUCCESS,
        response,
        receive_time: Date.now()
    }
}
