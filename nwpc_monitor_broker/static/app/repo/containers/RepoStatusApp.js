import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import RepoAppStatusTab from '../components/repo_app_status_tab'

class RepoStatusApp extends Component{
    componentDidMount(){

    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        let repo = params.repo;

        return (
            <RepoAppStatusTab owner={owner} repo={repo} />
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(RepoStatusApp)