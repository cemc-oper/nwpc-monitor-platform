import React from 'react'
import { render } from 'react-dom'

import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'

import { browserHistory } from 'react-router'
import { syncHistoryWithStore } from 'react-router-redux'


import welcomeAppReducer from './reducers'

import Root from './containers/Root'

let store = createStore(welcomeAppReducer,
    applyMiddleware(
        thunkMiddleware
    )
);

const history = syncHistoryWithStore(browserHistory, store);

render(
    <Root store={store} history={history} />,
    document.getElementById('welcome-app')
);
