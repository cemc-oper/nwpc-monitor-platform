import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

function welcome_reducer(state={
}, action){
    switch(action.type){
        default:
            return state;
    }
}

const welcomeAppReducer = combineReducers({
    welcome:welcome_reducer,
    routing
});

export default welcomeAppReducer;