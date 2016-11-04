import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchHpcUserLoadlevelerStatus,
} from '../actions/loadleveler_status';

import LoadingToast from '../../base/components/LoadingToast'

import { Util } from '../../base/util/util'

class HpcLoadlevelerStatusApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;

        dispatch(fetchHpcUserLoadlevelerStatus(user));
    }

    render() {
        const { params, loadleveler_status } = this.props;
        console.log(loadleveler_status);

        return (
            <div>
                <h1 className="page_title">HPC磁盘空间</h1>
                <LoadingToast shown={ loadleveler_status.status.is_fetching } />
            </div>
        );
    }
}

HpcLoadlevelerStatusApp.propTypes = {
    loadleveler_status: PropTypes.object
};

function mapStateToProps(state){
    return {
        loadleveler_status: state.hpc.loadleveler_status
    }
}

export default connect(mapStateToProps)(HpcLoadlevelerStatusApp)