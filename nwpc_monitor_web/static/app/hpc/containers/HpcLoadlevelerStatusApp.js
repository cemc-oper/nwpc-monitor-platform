import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchHpcUserLoadlevelerStatus,
} from '../actions/loadleveler_status';

import LoadingToast from '../../base/components/LoadingToast'

import { Util } from '../../base/util/util'

class HpcLoadlevelerStatusApp extends Component{
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

    handleSortClick(sort_label){
        if(this.state.sort_label===null){
            this.setState({
                sort_label: sort_label,
                is_asc_order: true
            })
        } else if(this.state.sort_label === sort_label) {
            this.setState({
                is_asc_order: !this.state.is_asc_order
            });
        } else {
            this.setState({
                sort_label: sort_label
            })
        }
    }

    static findPropById(job, id){
        const { props } = job;
        let prop = null;
        props.forEach(function(a_prop, index){
            if(a_prop.id === id) {
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

    static compareString(a,b){
        if(a<b)
            return -1;
        else if(a>b)
            return 1;
        else
            return 0;

    }

    static compareJobStatus(a, b){
        return HpcLoadlevelerStatusApp.compareString(
            HpcLoadlevelerStatusApp.getPropTextById(a, "llq.status"),
            HpcLoadlevelerStatusApp.getPropTextById(b, "llq.status")
        );
    }

    static compareOwner(a, b){
        return HpcLoadlevelerStatusApp.compareString(
            HpcLoadlevelerStatusApp.getPropTextById(a, "llq.owner"),
            HpcLoadlevelerStatusApp.getPropTextById(b, "llq.owner")
        );
    }

    static compareQueueDate(a, b){
        return HpcLoadlevelerStatusApp.compareString(
            HpcLoadlevelerStatusApp.getPropTextById(a, "llq.queue_date"),
            HpcLoadlevelerStatusApp.getPropTextById(b, "llq.queue_date")
        );
    }

    static compareJobClass(a, b){
        return HpcLoadlevelerStatusApp.compareString(
            HpcLoadlevelerStatusApp.getPropTextById(a, "llq.class"),
            HpcLoadlevelerStatusApp.getPropTextById(b, "llq.class")
        );
    }

    render() {
        const { params, loadleveler_status } = this.props;

        let user = params.user;

        let { collect_time, jobs } = loadleveler_status;
        let local_jobs = jobs.concat();

        switch(this.state.sort_label){
            case "llq.owner":
                if(this.state.is_asc_order)
                    local_jobs.sort(HpcLoadlevelerStatusApp.compareOwner);
                else
                    local_jobs.sort((a,b)=>(-1)*HpcLoadlevelerStatusApp.compareOwner(a,b));
                break;
            case "llq.queue_date":
                if(this.state.is_asc_order)
                    local_jobs.sort(HpcLoadlevelerStatusApp.compareQueueDate);
                else
                    local_jobs.sort((a,b)=>(-1)*HpcLoadlevelerStatusApp.compareQueueDate(a,b));
                break;
            case "llq.status":
                if(this.state.is_asc_order)
                    local_jobs.sort(HpcLoadlevelerStatusApp.compareJobStatus);
                else
                    local_jobs.sort((a,b)=>(-1)*HpcLoadlevelerStatusApp.compareJobStatus(a,b));
                break;
            case "llq.class":
                if(this.state.is_asc_order)
                    local_jobs.sort(HpcLoadlevelerStatusApp.compareJobClass);
                else
                    local_jobs.sort((a,b)=>(-1)*HpcLoadlevelerStatusApp.compareJobClass(a,b));
                break;
            default:
                break;
        }

        let jobs_node = local_jobs.map(function(a_job, index){
            let id = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.id");
            let owner = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.owner");
            let queue_date = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.queue_date");
            let status = HpcLoadlevelerStatusApp.getPropTextById(a_job, "llq.status");
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
                <h1 className="page_title">LoadLeveler队列</h1>
                <p>更新时间：{ Util.getDelayTime(Util.parseUTCTimeString(collect_time), Util.getNow())} </p>
                <div className="weui-cells">
                    <div className="weui-cell">
                        <div className="weui-cell__bd">
                            <p className="loadleveler-status-row">
                                <span className="loadleveler-status-cell-status">
                                    <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.status")}
                                       className="loadleveler-status-header-button">ST</a>
                                </span>
                                <span className="loadleveler-status-cell-owner">
                                    <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.owner")}
                                       className="loadleveler-status-header-button">Owner</a>
                                </span>
                                <span className="loadleveler-status-cell-class">
                                    <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.class")}
                                       className="loadleveler-status-header-button">Class</a>
                                </span>
                                <span className="loadleveler-status-cell-queue-date">
                                    <a href="javascript:;" onClick={this.handleSortClick.bind(this, "llq.queue_date")}
                                       className="loadleveler-status-header-button">Queue Date</a>
                                </span>
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