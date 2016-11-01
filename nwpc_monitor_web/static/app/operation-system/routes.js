import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import OperationSystemApp from './containers/OperationSystemApp'
import OwnerApp from './containers/OwnerApp'
import RepoApp from './containers/RepoApp'
import RepoStatusApp from './containers/RepoStatusApp'
import RepoAbortedTasksApp from './containers/RepoAbortedTasksApp'

export default (
    <Route path="/" component={OperationSystemApp}>
        <Route path=":owner" component={OwnerApp} />
        <Route path=":owner/:repo" component={RepoApp}>
            <IndexRoute component={RepoStatusApp} />
            <Route path="status/head/*" component={RepoStatusApp} />
            <Route path="aborted_tasks/:aborted_task_id" component={RepoAbortedTasksApp} />
        </Route>
    </Route>
)