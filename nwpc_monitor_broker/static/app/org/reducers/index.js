import { combineReducers } from 'redux'
import { QUERY_ORG_MEMBERS, REQUEST_ORG_REPOS, RECEIVE_ORG_REPOS_SUCCESS, fetchOrgRepos } from '../actions'

/* reducer */

//const initialState = {
//    org_repo_list: []
//};

/**
 *
 * @param state
 *      state of orgRepos:
 *      {
 *          status: {
 *              is_fetching: boolean,
 *              last_updated: number // Date()
 *          }
 *          owner: string
 *          repos: array of repo object
 *              [
 *                  { id: number, name: string },
 *                  ...
 *              ]
 *
 *      }
 * @param action
 * @returns {*}
 */

function orgRepos(state = {
    status:{
        is_fetching: false,
        last_updated: null
    },
    owner: 'nwp_xp',
    repos: []
}, action){
    switch(action.type){
        case REQUEST_ORG_REPOS:
            console.log(action.owner);
            var new_state = Object.assign({}, state, {
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                }
            });
            return new_state;
        case RECEIVE_ORG_REPOS_SUCCESS:
            return Object.assign({}, state, {
                repos: action.response.data.repos,
                status: {
                    is_fetching: false,
                    last_updated: action.receive_time
                }
            });
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