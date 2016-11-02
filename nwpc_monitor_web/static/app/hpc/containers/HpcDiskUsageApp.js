import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {
    fetchAddHpcUserDiskUsage,
    clearHpcDiskUsageUsers
} from '../actions/disk_usage';

import LoadingToast from '../../base/components/LoadingToast'
import FileSystemUsagePieChart from '../../base/components/FileSystemUsagePieChart'

import { Util } from '../../base/util/util'

class HpcDiskUsageApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let user = params.user;

        // dispatch(clearHpcDiskUsageUsers());
        dispatch(fetchAddHpcUserDiskUsage("nwp"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_qu"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_pd"));
        dispatch(fetchAddHpcUserDiskUsage("nwp_xp"));
    }

    render() {
        const { params, disk_usage } = this.props;

        let disk_usage_list = [];
        disk_usage.users.map(function(a_disk_usage, index){
            let file_systems = a_disk_usage.file_systems;
            let file_systems_node = [];
            file_systems.map(function(a_file_system, file_index){
                file_systems_node.push(
                    <div className="weui-flex" key={file_index}>
                        <div className="weui-flex__item">
                            <FileSystemUsagePieChart data={
                                {
                                    label: a_file_system.file_system,
                                    usage: a_file_system.block_limits.current,
                                    total: a_file_system.block_limits.quota
                                }
                            }/>
                        </div>
                        <div className="weui-flex__item">
                            <p>文件系统：{a_file_system.file_system}</p>
                            {/*<p>已用空间：{a_file_system.block_limits.Scurrent}</p>*/}
                            {/*<p>分配限额：{a_file_system.block_limits.quota}</p>*/}
                            {/*<p>最大限制：{a_file_system.block_limits.limit}</p>*/}
                        </div>


                    </div>
                )
            });

            disk_usage_list.push(
                <div key={index}>
                    <h2>{ a_disk_usage.user }</h2>
                    <p>更新时间：{ a_disk_usage.time } UTC</p>
                    { file_systems_node }
                </div>
            )
        });

        return (
            <div>
                <h1 className="page_title">HPC磁盘空间</h1>
                { disk_usage_list }
                <LoadingToast shown={ disk_usage.status.is_fetching } />
            </div>
        );
    }
}

HpcDiskUsageApp.propTypes = {
    disk_usage: PropTypes.object
};

function mapStateToProps(state){
    return {
        disk_usage: state.hpc.disk_usage
    }
}

export default connect(mapStateToProps)(HpcDiskUsageApp)