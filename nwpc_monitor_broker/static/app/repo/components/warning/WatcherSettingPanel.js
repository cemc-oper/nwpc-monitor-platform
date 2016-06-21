import React, { Component, PropTypes } from 'react';

export default class WatcherSettingPanel extends Component{
    constructor(props) {
        super(props);
    }

    handleUnWatchClick(owner, repo, user, event) {
        this.props.unwatch_click_handler(owner, repo, user)
    }

    handleWatchClick(owner, repo, user, event) {
        this.props.watch_click_handler(owner, repo, user)
    }

    render() {
        const { owner, repo, suggested_user_list } = this.props;
        return (
            <div>
                <h4>人员设置</h4>
                <p>{owner}小组成员</p>
                <ui className="list-group">
                    {suggested_user_list.map((an_user, index) =>
                        <li className="list-group-item" key={an_user.owner_name}>
                            <a href={ '/' + an_user.owner_name }>{an_user.owner_name}</a>
                            {
                                an_user.is_watching?
                                    (<button className="btn btn-danger btn-xs active pull-right"
                                             onClick={this.handleUnWatchClick.bind(this, owner, repo, an_user.owner_name)}>
                                        取消
                                    </button>) :
                                    (<button className="btn btn-primary btn-xs pull-right"
                                             onClick={this.handleWatchClick.bind(this, owner, repo, an_user.owner_name)}>
                                        关注
                                    </button>)
                            }
                        </li>
                    )}
                </ui>
                <div>
                    <h5>其他用户</h5>
                    <p>建设中</p>
                </div>
            </div>
        );
    }
}

WatcherSettingPanel.propTypes = {
    type: PropTypes.string.isRequired,
    suggested_user_list: PropTypes.arrayOf(PropTypes.shape({
        owner_name: PropTypes.string.isRequired,
        is_watching: PropTypes.bool.isRequired
    })).isRequired,
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired,
    watch_click_handler: PropTypes.func.isRequired,
    unwatch_click_handler: PropTypes.func.isRequired
};