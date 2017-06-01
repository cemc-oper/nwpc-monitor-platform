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

    render() {
        const { params, loadleveler_status } = this.props;

        let user = params.user;

        return (
            <div>
                <h1 className="page_title">LoadLeveler队列</h1>
                <p>更新时间：{ Util.getDelayTime(Util.parseUTCTimeString(collect_time), Util.getNow())} </p>
                <LoadlevelerJobList job_list={jobs}/>
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