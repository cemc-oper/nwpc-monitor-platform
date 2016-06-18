import React from 'react'
import { Route } from 'react-router'

import OrgReposApp from './containers/OrgReposApp'

export default (
    <Route path="/:owner" component={OrgReposApp} />
)
