import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import WatchingPanel from '../../../repo/components/warning/WatchingPanel'
import WatcherSettingPanel from '../../../repo/components/warning/WatcherSettingPanel'
import WarnPolicyPanel from '../../../repo/components/warning/WarnPolicyPanel'

import {
    fetchDingTalkWarningWatchUsers,
    fetchDingTalkWarningSuggestedUsers,
    fetchDingTalkWarningWatcherUser,
    fetchDeleteDingTalkWarningWatcherUser
} from '../../actions/warn'


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
        let repo = '@all';
        this.updateWatcher(owner)
    }

    updateWatcher(owner){
        const { dispatch, params } = this.props;
        dispatch(fetchDingTalkWarningWatchUsers(owner));
        dispatch(fetchDingTalkWarningSuggestedUsers(owner));
    }

    handleWatchClick(owner, users) {
        const { dispatch } = this.props;
        users.forEach(function(item, index, array){
            let user = item;
            dispatch(fetchDingTalkWarningWatcherUser(owner, user));
            console.log('handleWatchClick', owner, user);
        });

        this.updateWatcher(owner);
    }

    handleUnWatchClick(owner, users) {
        const { dispatch } = this.props;
        users.forEach(function(item, index, array){
            let user = item;
            dispatch(fetchDeleteDingTalkWarningWatcherUser(owner, user));
            console.log('handleUnWatchClick', owner, user);
        });

        this.updateWatcher(owner);
    }

    render() {
        let owner = this.props.params.owner;
        let repo = "@all";
        const { watching_user_list, suggested_user_list } = this.props;
        return (
            <div>
                <h3>钉钉</h3>
                <div>
                    <h4 id="warn_ding_talk_overview">概览</h4>
                    <div className="row">
                        <div className="col-md-6">
                            <p>欢迎扫码加入我们的钉钉团队</p>
                            <img src="/static/image/ding_talk_invite.png" />
                        </div>
                        <div className="col-md-6">
                            <p>或者通过点击下面的链接加入团队</p>
                            <a href="https://t.dingtalk.com/invite/index?code=76b2940f32">
                                https://t.dingtalk.com/invite/index?code=76b2940f32
                            </a>
                        </div>
                    </div>
                </div>
                <WatchingPanel
                    id="warn_ding_talk_warn_watching_panel"
                    owner={ owner }
                    repo={ repo }
                    type="dingtalk"
                    watching_user_list={ watching_user_list }
                    watch_click_handler={ this.handleWatchClick }
                    unwatch_click_handler={ this.handleUnWatchClick }
                />
                <WatcherSettingPanel
                    id="warn_ding_talk_warn_setting_panel"
                    owner={ owner }
                    repo={ repo }
                    type="dingtalk"
                    suggested_user_list={ suggested_user_list }
                    watch_click_handler={ this.handleWatchClick }
                    unwatch_click_handler={ this.handleUnWatchClick }
                />
                <WarnPolicyPanel
                    id="warn_ding_talk_warn_policy_panel"
                    owner={owner}
                    repo={repo}
                    type="dingtalk"
                />
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
        watching_user_list: state.warning.ding_talk.watching_user.watching_user_list,
        suggested_user_list: state.warning.ding_talk.suggested_user.suggested_user_list
    }
}

export default connect(mapStateToProps)(DingTalkWarningApp)