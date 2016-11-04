import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import HpcApp from './containers/HpcApp'
import HpcDiskUsageApp from './containers/HpcDiskUsageApp'
import HpcLoadlevelerStatusApp from './containers/HpcLoadlevelerStatusApp'

export default (
    <Route path="/hpc" component={HpcApp}>
        <Route path=":user/disk/usage" component={HpcDiskUsageApp} />
        <Route path=":user/loadleveler/status" component={HpcLoadlevelerStatusApp} />
    </Route>
)