import React from 'react'
import { Route } from 'react-router'

import OrgApp from './containers/OrgApp'

export default (
    <Route path="/:owner" component={OrgApp} />
)
