import React from 'react'
import { Route, IndexRedirect, IndexRoute } from 'react-router'

import HpcDiskApp from './containers/HpcDiskApp'
import HpcDiskUsageApp from './containers/HpcDiskUsageApp'
import HpcLoadlevelerApp from './containers/HpcLoadlevelerApp'
import HpcLoadlevelerStatusApp from './containers/HpcLoadlevelerStatusApp'

export default (
    <Route path="/hpc" >
        <Route path=":user/disk" component={HpcDiskApp}>
            <Route path="usage" component={HpcDiskUsageApp} />
        </Route>
        <Route path=":user/loadleveler" component={ HpcLoadlevelerApp } >
            <Route path="status" component={HpcLoadlevelerStatusApp} />
        </Route>
    </Route>
)