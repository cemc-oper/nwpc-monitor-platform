import React, { Component, PropTypes } from 'react';

export default class WatchingUserList extends Component{
    constructor(props) {
        super(props);
    }

    handleUnWatchClick(owner, repo, user, event) {
        this.props.unwatch_click_handler(owner, repo, user)
    }

    render() {
        const {owner, repo} = this.props;
        let watching_user_list = this.props.watching_user_list;

        return (
            <div>
                <h4>推送列表</h4>
                <ui className="list-group">
                    {watching_user_list.map((an_user, index) =>
                        <li className="list-group-item" key={an_user.owner_name}>
                            <label>
                                <input type="checkbox" /> <a href={ '/' + an_user.owner_name }>{an_user.owner_name}</a>
                            </label>
                            <button className="btn btn-danger btn-xs active pull-right"
                                    onClick={this.handleUnWatchClick.bind(this, owner, repo, an_user.owner_name)} >
                                取消
                            </button>
                        </li>
                    )}
                    <li className="list-group-item">
                        <button type="button" className="btn btn-default btn-xs">全选</button>
                        <button type="button" className="btn btn-default btn-xs">取消全选</button>
                        <button className="btn btn-default btn-xs pull-right" >
                                取消
                        </button>
                    </li>
                </ui>
            </div>
        );
    }
}

WatchingUserList.propTypes = {
    type: PropTypes.string.isRequired,
    watching_user_list: PropTypes.arrayOf(PropTypes.shape({
        owner_name: PropTypes.string.isRequired,
        warn_watch: PropTypes.shape({
            start_date_time: PropTypes.string,
            end_date_time: PropTypes.string
        }).isRequired
    })).isRequired,
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired,
    unwatch_click_handler: PropTypes.func.isRequired
};