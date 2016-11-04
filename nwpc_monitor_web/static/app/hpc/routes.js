import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import HpcApp from './containers/HpcApp'
import HpcDiskUsageApp from './containers/HpcDiskUsageApp'

export default (
    <Route path="/hpc" component={HpcApp}>
        <Route path=":user/disk/usage" component={HpcDiskUsageApp} />
    </Route>
)