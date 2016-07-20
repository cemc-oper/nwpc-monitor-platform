import React, { Component, PropTypes } from 'react';

export default class WarnPolicyPanel extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { owner, repo } = this.props;
        return (
            <div>
                <h4 id="warn_ding_talk_warn_policy_panel">报警策略设置</h4>
                <p>有新的任务出错就会发送报警信息</p>
            </div>
        );
    }
}

WarnPolicyPanel.propTypes = {
    type: PropTypes.string.isRequired,
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired
};