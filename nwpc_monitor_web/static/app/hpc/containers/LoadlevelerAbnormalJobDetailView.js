import React, {Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import LoadlevelerJobUtil from '../util/LoadlevelerJobUtil'
import LoadlevelerJobDetail from '../components/LoadlevelerJobDetail'


class LoadlevelerAbnormalJobDetailView extends Component{
    render(){
        const { job_list, params } = this.props;
        const { job_id } = params;

        // find job in job_list
        let job = job_list.find(function(element, index, array){
            return LoadlevelerJobUtil.getPropTextById(element, "llq.id") === job_id;
        });
        let job_node = (
            <div>作业不存在：{job_id}</div>
        );
        if(job) {
            job_node = (
                <LoadlevelerJobDetail job={job} />
            )
        }

        return (
            <div>
                { job_node }
            </div>
        )
    }
}

LoadlevelerAbnormalJobDetailView.propTypes = {
    job_list: PropTypes.arrayOf(PropTypes.shape({
        props: PropTypes.array
    }))
};

function mapStateToProps(state, ownProps){
    return {
        job_list: state.hpc.loadleveler_status.abnormal_jobs.job_list
    }
}

export default connect(mapStateToProps)(LoadlevelerAbnormalJobDetailView)