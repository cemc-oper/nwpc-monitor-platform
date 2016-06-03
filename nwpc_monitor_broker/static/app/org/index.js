import thunkMiddleware from 'redux-thunk'

import React, {Component} from 'react'
import { render } from 'react-dom'

import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'

import { Router, Route, browserHistory } from 'react-router'

import orgApp from './reducers'
import { fetchOrgRepos } from './actions'
import OrgApp from './containers/OrgApp'

let store = createStore(orgApp,
    applyMiddleware(
        thunkMiddleware
    )
);


class Root extends Component {
    render () {
        return (
            <Router history={this.props.history}>
                <Route path="/:owner" component={OrgApp} />
            </Router>
        )
    }
}

let rootElement = document.getElementById('org-repo-app');

render(
    <Provider store={store}>
        <Root history={browserHistory}/>
    </Provider>,
    rootElement
);
