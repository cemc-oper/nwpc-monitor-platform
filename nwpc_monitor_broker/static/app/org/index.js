import thunkMiddleware from 'redux-thunk'

import React from 'react'
import { render } from 'react-dom'

import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'

import orgApp from './reducers'
import { fetchOrgRepos } from './actions'
import OrgApp from './containers/OrgApp'

let store = createStore(orgApp,
    applyMiddleware(
        thunkMiddleware
    )
);

let rootElement = document.getElementById('org-repo-app');

render(
    <Provider store={store}>
        <OrgApp />
    </Provider>,
    rootElement
);
