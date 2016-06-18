import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

import { REQUEST_ORG_REPOS, RECEIVE_ORG_REPOS_SUCCESS,
    REQUEST_ORG_MEMBERS, RECEIVE_ORG_MEMBERS_SUCCESS
} from '../actions'



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
            return Object.assign({}, state, {
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                }
            });
        case RECEIVE_ORG_REPOS_SUCCESS:
            return Object.assign({}, state, {
                repos: action.response.data.data.repos,
                status: {
                    is_fetching: false,
                    last_updated: action.receive_time
                }
            });
        default:
            return state;
    }
}


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
 *          members: array of member object
 *              [
 *                  { id: number, name: string },
 *                  ...
 *              ]
 *
 *      }
 * @param action
 * @returns {*}
 */
function orgMembers(state = {
    status:{
        is_fetching: false,
        last_updated: null
    },
    owner: 'nwp_xp',
    members: []
}, action){
    switch(action.type){
        case REQUEST_ORG_MEMBERS:
            console.log(action.owner);
            return Object.assign({}, state, {
                status: {
                    is_fetching: true,
                    last_updated: state.status.last_updated
                }
            });
        case RECEIVE_ORG_MEMBERS_SUCCESS:
            return Object.assign({}, state, {
                members: action.response.data.data.members,
                status: {
                    is_fetching: false,
                    last_updated: action.receive_time
                }
            });
        default:
            return state;
    }
}


const orgAppReducer = combineReducers({
    orgRepos,
    orgMembers,
    routing
});

export default orgAppReducer;