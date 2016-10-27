import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import OperationSystemApp from './containers/OperationSystemApp'
import OwnerApp from './containers/OwnerApp'
import RepoApp from './containers/RepoApp'

export default (
    <Route path="/" component={OperationSystemApp}>
        <Route path=":owner" component={OwnerApp} />
        <Route path=":owner/:repo" component={RepoApp} />
    </Route>
)