import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import RepoApp from './containers/RepoApp'
import RepoStatusApp from './containers/RepoStatusApp'
import RepoSettingsApp from './containers/RepoSettingsApp'
import RepoWarningApp from './containers/RepoWarningApp'

export default (
    <Route path="/:owner/:repo" component={RepoApp}>
        <IndexRoute component={RepoStatusApp} />
        <Route path="status" component={RepoStatusApp} />
        <Route path="warning" component={RepoWarningApp} >
        </Route>
        <Route path="settings" component={RepoSettingsApp} />
    </Route>
)
