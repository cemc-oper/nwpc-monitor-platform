import React from 'react'
import { Route } from 'react-router'

import RepoApp from './containers/RepoApp'

export default (
    <Route path="/:owner/:repo" component={RepoApp} />
)
