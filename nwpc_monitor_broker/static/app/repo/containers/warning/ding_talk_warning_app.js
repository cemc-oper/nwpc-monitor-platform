import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import WatchingUserList from '../../components/warning/WatchingUserList'

import {fetchDingTalkWarningWatchUsers} from '../../actions'

export default class DingTalkWarningApp extends Component{
    constructor(props) {
        super(props);
    }

    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        let repo = params.repo;
        dispatch(fetchDingTalkWarningWatchUsers(owner,repo))
    }

    render() {
        let owner = this.props.params.owner;
        let repo = this.props.params.repo;
        const { watching_user_list } = this.props;
        return (
            <div>
                <h3>钉钉</h3>
                <div>
                    <h4>概览</h4>
                </div>
                <WatchingUserList owner={ owner }
                                  repo={ repo }
                                  type="dingtalk"
                                  watching_user_list={ watching_user_list } />
                <div>
                    <h4>人员设置</h4>
                </div>
                <div>
                    <h4>报警策略设置</h4>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
        type: 'dingtalk',
        watching_user_list: state.repo.warning.ding_talk.watching_user.watching_user_list
    }
}

export default connect(mapStateToProps)(DingTalkWarningApp)