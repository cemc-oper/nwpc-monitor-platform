import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import RepoAppSettingsTab from '../components/repo_app_settings_tab'

class RepoSettingsApp extends Component{
    componentDidMount(){

    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        let repo = params.repo;

        return (
            <RepoAppSettingsTab owner={owner} repo={repo} />
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(RepoSettingsApp)