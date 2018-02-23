import React from 'react'
import { render } from 'react-dom'

import Root from './containers/Root'

import {store, history} from './store'

render(
    <Root store={store} history={history} />,
    document.getElementById('repo-app')
);