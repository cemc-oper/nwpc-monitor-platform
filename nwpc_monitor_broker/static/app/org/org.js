import { combineReducers } from 'redux'
import { createStore } from 'redux';

/* action */
const QUERY_ORG_REPOS = 'QUERY_ORG_REPOS';

/* create action*/
function queryOrgRepos(owner){
    return {
        type: QUERY_ORG_REPOS,
        owner
    }
}

/* reducer */

const initialState = {
    org_repo_list: []
};

function orgRepo(state = [], action){
    switch(action.type){
        case QUERY_ORG_REPOS:
            return Object.assign({}, state, {
                org_repo_list:[
                    {name: 'nwpc_op'},
                    {name: 'nwpc_qu'},
                    {name: 'eps_nwpc_qu'}
                ]
            });
        default:
            return state;
    }
}


const orgApp = combineReducers({
    orgRepo
});

// export default orgApp;
let store = createStore(orgApp);

console.log(store.getState());

let unsubscribe = store.subscribe(() =>
    console.log(store.getState())
);

store.dispatch(queryOrgRepos('nwp_xp'));

unsubscribe();