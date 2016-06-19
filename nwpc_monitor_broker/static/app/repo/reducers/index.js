import { combineReducers } from 'redux'
import { routerReducer as routing } from 'react-router-redux'

const repoAppReducer = combineReducers({
    routing
});

export default repoAppReducer;