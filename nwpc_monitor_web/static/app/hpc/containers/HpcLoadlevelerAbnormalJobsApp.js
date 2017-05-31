import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import LoadingToast from '../../base/components/LoadingToast'
import { Util } from '../../base/util/util'

import { fetchHpcUserLoadlevelerAbnormalJobs} from '../actions/loadleveler_status';

import { HpcLoadlevelerStatusApp } from './HpcLoadlevelerStatusApp'

class HpcLoadlevelerAbnormalJobsApp extends Component{
    constructor(props){
        super(props);
        this.state = {
            sort_label: null,
            is_asc_order: true
        }
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

    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;
        let abnormal_jobs_id = params.abnormal_jobs_id;

        dispatch(fetchHpcUserLoadlevelerAbnormalJobs(user, abnormal_jobs_id));
    }

    render() {
        const { params, abnormal_jobs, status } = this.props;
        if(abnormal_jobs===null)
        {
            return (
                <div>
                    <p>不存在</p>
                    <LoadingToast shown={ status.is_fetching } />
                </div>
            )
        }

        let user = params.user;
        let abnormal_jobs_id = params.abnormal_jobs_id;

        let last_update_time = '未知';
        let cur_time = new Date();
        if(abnormal_jobs['update_time']!==null) {
            last_update_time = Util.getDelayTime(
                Util.parseUTCTimeString(abnormal_jobs['update_time']), Util.parseDate(cur_time));
        }

        let local_jobs = abnormal_jobs['abnormal_job_list'].concat();
        local_jobs = HpcLoadlevelerStatusApp.sortJobs(local_jobs, this.state.sort_label, this.state.is_asc_order);

        let jobs_nodes = local_jobs.map(function(a_job, index){
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
                <h1 className="page_title">Loadleveler异常任务</h1>
                <p>更新时间：{ last_update_time } </p>
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
                    { jobs_nodes }
                </div>
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

HpcLoadlevelerAbnormalJobsApp.propTypes = {
    abnormal_jobs: PropTypes.shape({
        update_time: PropTypes.string,
        abnormal_jobs_id: PropTypes.number,
        abnormal_job_list: PropTypes.arrayOf(PropTypes.shape({
            props: PropTypes.array
        })),
        plugin_name: PropTypes.string
    }),
    status: PropTypes.shape({
        is_fetching: PropTypes.bool,
        last_updated: PropTypes.oneOfType([
            PropTypes.null,
            PropTypes.number
        ])
    })
};

function mapStateToProps(state){
    return {
        abnormal_jobs: state.hpc.loadleveler_status.abnormal_jobs,
        status: state.hpc.loadleveler_status.status
    }
}

export default connect(mapStateToProps)(HpcLoadlevelerAbnormalJobsApp)