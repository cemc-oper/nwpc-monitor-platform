import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import { NodeStatusImage } from '../../base/components/NodeStatusImage'
import LoadingToast from '../../base/components/LoadingToast'

import { fetchOperationSystemRepoTaskCheckUnfitNodes } from '../actions/repo';
import { Util } from '../../base/util/util'

class RepoTaskCheckUnfitNodesApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        let repo = params.repo;
        let unfit_nodes_id = params.unfit_nodes_id;

        dispatch(fetchOperationSystemRepoTaskCheckUnfitNodes(owner, repo, unfit_nodes_id));
    }

    render() {
        const { params, unfit_nodes, status } = this.props;
        if(unfit_nodes===null)
        {
            return (
                <div>
                    <p>不存在</p>
                    <LoadingToast shown={ status.is_fetching } />
                </div>
            )
        }

        let owner = params.owner;
        let repo = params.repo;
        let unfit_nodes_id = params.unfit_nodes_id;

        let repo_last_update_time = '未知';
        let cur_time = new Date();
        if(unfit_nodes['update_time']!==null) {
            repo_last_update_time = Util.getDelayTime(
                Util.parseUTCTimeString(unfit_nodes['update_time']), Util.parseDate(cur_time));
        }

        let task_nodes = unfit_nodes['unfit_node_list'].map(function(a_node, i){
            return (
                <p className="unfit-node-path-row" key={i} >
                    <span className="node-path">
                        { a_node['node_path'] }
                    </span>
                </p>
            )
        });

        return (
            <div>
                <p>更新时间：{ repo_last_update_time }</p>

                <article className="weui-article">
                    <section>
                        <h1>异常节点</h1>
                        { task_nodes }
                    </section>
                </article>

                <div className="weui-cells__title">链接</div>
                <div className="weui-cells weui-cells_access">
                    <a className="weui-cell" href={ "/" +  owner  + "/" +  repo }>
                        <div className="weui-cell__bd weui-cell_primary">
                            <p>最新状态</p>
                        </div>
                        <div className="weui-cell__ft">
                        </div>
                    </a>
                </div>
                <LoadingToast shown={ status.is_fetching } />
            </div>
        );
    }
}

RepoTaskCheckUnfitNodesApp.propTypes = {
    unfit_nodes: PropTypes.shape({
        collected_time: PropTypes.string,
        status_blob_id: PropTypes.number,
        unfit_node_list: PropTypes.arrayOf(PropTypes.shape({
            node_path: PropTypes.string,
            unfit_node_list: PropTypes.array
        })),
        name: PropTypes.string,
        trigger: PropTypes.array,
        update_time: PropTypes.string
    })
};

function mapStateToProps(state){
    return {
        unfit_nodes: state.operation_system.repo.task_check.unfit_nodes,
        status: state.operation_system.repo.status
    }
}

export default connect(mapStateToProps)(RepoTaskCheckUnfitNodesApp)