import React from 'react'
import { render } from 'react-dom'
import { createStore } from 'redux'
import { Provider } from 'react-redux'

import orgApp from './reducers/index'
import OrgApp from './containers/OrgApp'

let store = createStore(orgApp);

let rootElement = document.getElementById('org-repo-app');

render(
    <Provider store={store}>
        <OrgApp />
    </Provider>,
    rootElement
);
