import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchAddHpcUserDiskUsage,
    clearHpcDiskUsageUsers
} from '../actions/disk_usage';

import LoadingToast from '../../base/components/LoadingToast'

import { Util } from '../../base/util/util'

class HpcDiskUsageApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;

        dispatch(clearHpcDiskUsageUsers());
        dispatch(fetchAddHpcUserDiskUsage("nwp"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_qu"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_pd"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_xp"));
    }

    render() {
        const { params, disk_usage } = this.props;
        console.log(disk_usage);

        return (
            <div>
                <h1 className="page_title">hpc/disk_usage</h1>
                <LoadingToast shown={ disk_usage.status.is_fetching } />
            </div>
        );
    }
}

HpcDiskUsageApp.propTypes = {

};

function mapStateToProps(state){
    return {
        disk_usage: state.hpc.disk_usage
    }
}

export default connect(mapStateToProps)(HpcDiskUsageApp)