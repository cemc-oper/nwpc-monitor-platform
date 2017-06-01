import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchHpcUserLoadlevelerStatus,
} from '../actions/loadleveler_status';

import LoadingToast from '../../base/components/LoadingToast'

import { Util } from '../../base/util/util'
import LoadlevelerJobList from '../components/LoadlevelerJobList'

export class HpcLoadlevelerStatusApp extends Component{
    constructor(props){
        super(props);
        this.state = {
            sort_label: null,
            is_asc_order: true
        }
    }

    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;

        dispatch(fetchHpcUserLoadlevelerStatus(user));
    }

    render() {
        const { params, job_queue, status } = this.props;

        let user = params.user;

        return (
            <div>
                <h1 className="page_title">LoadLeveler队列</h1>
                <p>更新时间：{ Util.getDelayTime(Util.parseUTCTimeString(collect_time), Util.getNow())} </p>
                <LoadlevelerJobList job_list={job_queue.jobs}/>
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

HpcLoadlevelerStatusApp.propTypes = {
    loadleveler_status: PropTypes.object
};

function mapStateToProps(state){
    return {
        job_queue: state.hpc.loadleveler_status.job_queue,
        status: state.hpc.loadleveler_status.status
    }
}

export default connect(
    mapStateToProps
)(HpcLoadlevelerStatusApp)