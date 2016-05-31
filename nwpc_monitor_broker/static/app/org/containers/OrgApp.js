import React, { Component } from 'react';

import OrgRepoList from '../components/OrgRepoList'
import OrgMemberList from '../components/OrgMemberList'

export class OrgApp extends Component{
    render() {
        return (
            <div>
                <div className="col-md-8">
                    <h2>项目</h2>
                    <OrgRepoList />
                </div>
                <div className="col-md-4">
                    <h2>人员</h2>
                    <OrgMemberList />
                </div>
            </div>
        );
    }
}