import React, { Component, PropTypes } from 'react';

export default class WatcherList extends Component{
    constructor(props) {
        super(props);
    }

    handleUnWatchClick(owner, repo, users, event) {
        this.props.unwatch_click_handler(owner, repo, users)
    }

    handleWatchClick(owner, repo, users, event) {
        this.props.watch_click_handler(owner, repo, users)
    }

    handleAllCheckClick() {

    }

    handleAllUnCheckClick() {

    }

    handleCheckboxChange(user, event) {
        console.log(event.target);
    }


    render() {
        const {owner, repo} = this.props;
        let watcher_list = this.props.watcher_list;

        return (
            <div>
                <ui className="list-group">
                    {watcher_list.map((an_user, index) =>
                        <li className="list-group-item" key={an_user.owner_name}>
                            <label>
                                <input type="checkbox" value={an_user.owner_name}
                                       onchange={this.handleCheckboxChange.bind(this, an_user.owner_name)} />
                                &nbsp;
                                <a href={ '/' + an_user.owner_name }>{an_user.owner_name}</a>
                            </label>
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
                    <li className="list-group-item">
                        <button type="button" className="btn btn-default btn-xs">全选</button>
                        <button type="button" className="btn btn-default btn-xs">取消全选</button>
                        <button className="btn btn-default btn-xs pull-right" onClick={this.handleAllUnCheckClick.bind(this)}>
                                取消
                        </button>
                        <button className="btn btn-default btn-xs pull-right" onClick={this.handleAllCheckClick.bind(this)}>
                                关注
                        </button>
                    </li>
                </ui>
            </div>
        );
    }
}

WatcherList.propTypes = {
    type: PropTypes.string.isRequired,
    watcher_list: PropTypes.arrayOf(PropTypes.shape({
        owner_name: PropTypes.string.isRequired,
        is_watching:PropTypes.bool.isRequired,
        warn_watch: PropTypes.shape({
            start_date_time: PropTypes.string,
            end_date_time: PropTypes.string
        })
    })).isRequired,
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired,
    unwatch_click_handler: PropTypes.func.isRequired,
    watch_click_handler: PropTypes.func.isRequired
};