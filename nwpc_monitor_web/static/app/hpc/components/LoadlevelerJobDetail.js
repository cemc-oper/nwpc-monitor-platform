import { Component, PropTypes } from 'react';

import LoadlevelerJobUtil from '../util/LoadlevelerJobUtil'


export default class LoadlevelerJobDetail extends Component{
    constructor(props){
        super(props);
    }

    render(){
        const {job} = this.props;
        let id = LoadlevelerJobUtil.getPropTextById(job, "llq.id");
        let owner = LoadlevelerJobUtil.getPropTextById(job, "llq.owner");
        let queue_date = LoadlevelerJobUtil.getPropTextById(job, "llq.queue_date");
        let status = LoadlevelerJobUtil.getPropTextById(job, "llq.status");
        let ll_class = LoadlevelerJobUtil.getPropTextById(job, "llq.class");
        let job_script = LoadlevelerJobUtil.getPropTextById(job, "llq.job_script");
        return (
            <div>
                <p>id: {id}</p>
                <p>owner: {owner}</p>
                <p>queue_date: {queue_date}</p>
                <p>status: {status}</p>
                <p>ll_class: {ll_class}</p>
                <p>job_script: {job_script}</p>
            </div>
        )
    }
};

LoadlevelerJobDetail.propTypes = {
    job: PropTypes.shape({
        props: PropTypes.array
    })
};

LoadlevelerJobDetail.defaultProps = {
    job: null
};