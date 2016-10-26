import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import WelcomeApp from './containers/WelcomeApp'

export default (
    <Route path="/" component={WelcomeApp}>
    </Route>
)