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

    static findPropById(job, id){
        const { props } = job;
        let prop = null;
        props.forEach(function(a_prop, index){
            if(a_prop.id == id) {
                prop = a_prop
            }
        });
        return prop;
    }

    static getPropTextById(job, id){
        let text = null;
        let prop = HpcLoadlevelerStatusApp.findPropById(job,id);
        if(prop) text = prop.text;
        return text;
    }

    render() {
        const { params, loadleveler_status } = this.props;
        console.log(loadleveler_status);

        let { collect_time, jobs } = loadleveler_status;

        let jobs_node = jobs.map(function(a_job, index){
            let id = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.id");
            let owner = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.owner");
            let queue_date = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.queue_date");
            let status = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.status");
            // if(status.length==1){
            //     status += " ";
            // }
            let ll_class = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.class");
            let job_script = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.job_script");
            return (
                <div className="weui-cell" key={index}>
                    <div className="weui-cell__bd">
                        <p className="loadleveler-status-row">
                            <span className="loadleveler-status-cell-status">{status}</span>
                            <span className="loadleveler-status-cell-owner">{owner}</span>
                            <span className="loadleveler-status-cell-class">{ll_class}</span>
                            <span className="loadleveler-status-cell-queue-date">{queue_date}</span>
                        </p>
                    </div>
                </div>
            );
        });

        return (
            <div>
                <h1 className="page_title">HPC队列</h1>
                <p>更新时间：{ Util.getDelayTime(Util.parseUTCTimeString(collect_time), Util.getNow())} </p>
                <div className="weui-cells">
                    <div className="weui-cell">
                        <div className="weui-cell__bd">
                            <p className="loadleveler-status-row">
                                <span className="loadleveler-status-cell-status">ST</span>
                                <span className="loadleveler-status-cell-owner">Owner</span>
                                <span className="loadleveler-status-cell-class">Class</span>
                                <span className="loadleveler-status-cell-queue-date">Queue Date</span>
                            </p>
                        </div>
                    </div>
                    { jobs_node }
                </div>
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