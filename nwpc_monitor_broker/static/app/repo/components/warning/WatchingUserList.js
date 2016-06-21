import React, { Component, PropTypes } from 'react';

export default class WatchingUserList extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let watching_user_list = this.props.watching_user_list;
        return (
            <div>
                <h4>推送列表</h4>
                <ui className="list-group">
                    {watching_user_list.map((an_user, index) =>
                        <li className="list-group-item" key={an_user.owner_name}>
                            <a href={ '/' + an_user.owner_name }>{an_user.owner_name}</a>
                        </li>
                    )}
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
    repo: PropTypes.string.isRequired
};