import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import OrgApp from './containers/OrgApp'
import OrgReposApp from './containers/OrgReposApp'

export default (
    <Route path="/:owner" component={OrgApp}>
        <IndexRoute component={OrgReposApp} />
        <Route path="repos" component={OrgReposApp} />
    </Route>
)