import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import { fetchOperationSystemOwnerRepos } from '../actions/owner';

import { Util } from '../../base/util/util'

class OwnerApp extends Component{

    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        dispatch(fetchOperationSystemOwnerRepos(owner));
    }

    render() {
        const { params, repos_status } = this.props;
        let owner = params.owner;
        let cur_time = new Date();

        let repos = repos_status.map(function(element,i){
            let repo_status = "unk";
            if(element['status']!=null)
                repo_status = element['status'];

            let repo_last_update_time = '未知';
            if(element['last_updated_time']!=null) {
                let last_updated_time = new Date(element['last_updated_time']);
                repo_last_update_time = Util.getDelayTime(last_updated_time, cur_time)
            }

            const image_style = {
                width: '40px',
                marginRight: '5px',
                display: 'block',
            };

            return (
                <a className="weui-cell" key={i} href={ "/" + owner + "/" + repo_status['repo'] }>
                    <div className="weui-cell__hd">
                        <img src={Util.getStatusBackgroundImage(repo_status)}
                             alt="icon" style={image_style} />
                    </div>
                    <div className="weui-cell__bd weui-cell_primary">
                        <p>{ element['repo'] }</p>
                    </div>
                    <div className="weui-cell__ft">
                        { repo_last_update_time}
                    </div>
                </a>
            )
        });

        return (
            <div>
                <h1 className="page_title"><a href={ "/" + owner } >{ owner }</a></h1>
                <div className="weui-cells weui-cells_access">
                    { repos }
                </div>
            </div>
        );
    }
}

OwnerApp.propTypes = {
    repos_status: PropTypes.arrayOf(PropTypes.shape({
        last_updated_time: PropTypes.string,
        owner: PropTypes.string,
        repo: PropTypes.string,
    }))
};

function mapStateToProps(state){
    return {
        repos_status: state.operation_system.owner.repos_status
    }
}

export default connect(mapStateToProps)(OwnerApp)