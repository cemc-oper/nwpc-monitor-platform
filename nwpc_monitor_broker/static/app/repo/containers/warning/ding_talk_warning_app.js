import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import WatchingUserList from '../../components/warning/WatchingUserList'
import WatcherSettingPanel from '../../components/warning/WatcherSettingPanel'

import {
    fetchDingTalkWarningWatchUsers,
    fetchDingTalkWarningSuggestedUsers
} from '../../actions'

import {
    fetchDingTalkWarningWatcherUser,
    fetchDeleteDingTalkWarningWatcherUser
} from '../../actions/watcher'

export default class DingTalkWarningApp extends Component{
    constructor(props) {
        super(props);
        this.handleWatchClick = this.handleWatchClick.bind(this);
        this.handleUnWatchClick = this.handleUnWatchClick.bind(this);
        this.updateWatcher = this.updateWatcher.bind(this)
    }

    componentDidMount(){
        const { params } = this.props;
        let owner = params.owner;
        let repo = params.repo;
        this.updateWatcher(owner, repo)
    }

    updateWatcher(owner, repo){
        const { dispatch, params } = this.props;
        dispatch(fetchDingTalkWarningWatchUsers(owner,repo));
        dispatch(fetchDingTalkWarningSuggestedUsers(owner, repo));
    }

    handleWatchClick(owner, repo, user) {
        const { dispatch } = this.props;
        dispatch(fetchDingTalkWarningWatcherUser(owner, repo, user));
        console.log('handleWatchClick', owner, repo, user);

        this.updateWatcher(owner, repo);
    }

    handleUnWatchClick(owner, repo, user) {
        const { dispatch } = this.props;
        dispatch(fetchDeleteDingTalkWarningWatcherUser(owner, repo, user));
        console.log('handleUnWatchClick', owner, repo, user);

        this.updateWatcher(owner, repo);
    }

    render() {
        let owner = this.props.params.owner;
        let repo = this.props.params.repo;
        const { watching_user_list, suggested_user_list } = this.props;
        return (
            <div>
                <h3>钉钉</h3>
                <div>
                    <h4>概览</h4>
                    <p>建设中</p>
                </div>
                <WatchingUserList owner={ owner }
                                  repo={ repo }
                                  type="dingtalk"
                                  watching_user_list={ watching_user_list }
                                  unwatch_click_handler={ this.handleUnWatchClick }
                />
                <WatcherSettingPanel owner={ owner }
                                     repo={ repo }
                                     type="dingtalk"
                                     suggested_user_list={ suggested_user_list }
                                     watch_click_handler={ this.handleWatchClick }
                                     unwatch_click_handler={ this.handleUnWatchClick }
                />
                <div>
                    <h4>报警策略设置</h4>
                    <p>建设中</p>
                </div>
            </div>
        );
    }
}

DingTalkWarningApp.propTypes = {
    dispatch: PropTypes.func.isRequired
};

function mapStateToProps(state){
    return {
        type: 'dingtalk',
        watching_user_list: state.repo.warning.ding_talk.watching_user.watching_user_list,
        suggested_user_list: state.repo.warning.ding_talk.suggested_user.suggested_user_list
    }
}

export default connect(mapStateToProps)(DingTalkWarningApp)