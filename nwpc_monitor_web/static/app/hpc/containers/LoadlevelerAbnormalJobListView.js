import React, {PropTypes } from 'react';
import { connect } from 'react-redux';

import LoadlevelerJobList from '../components/LoadlevelerJobList'
import { Util } from '../../base/util/util'


class LoadlevelerAbnormalJobListView extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        const { abnormal_jobs } = this.props;
        if(abnormal_jobs===null)
        {
            return (
                <div>
                    <p>不存在</p>
                </div>
            )
        }

        const { job_list, update_time} = abnormal_jobs;

        let last_update_time = '未知';
        let cur_time = new Date();
        if(abnormal_jobs.update_time!==null) {
            last_update_time = Util.getDelayTime(
                Util.parseUTCTimeString(update_time), Util.parseDate(cur_time));
        }

        return (
            <div>
                <p>更新时间：{ last_update_time } </p>
                <LoadlevelerJobList job_list={job_list}/>
            </div>
        )
    }
}

LoadlevelerAbnormalJobListView.propTypes = {
    abnormal_jobs: PropTypes.shape({
        update_time: PropTypes.string,
        abnormal_jobs_id: PropTypes.number,
        abnormal_job_list: PropTypes.arrayOf(PropTypes.shape({
            props: PropTypes.array
        })),
        plugin_name: PropTypes.string
    }),
};

function mapStateToProps(state){
    return {
        abnormal_jobs: state.hpc.loadleveler_status.abnormal_jobs
    }
}

export default connect(mapStateToProps)(LoadlevelerAbnormalJobListView)