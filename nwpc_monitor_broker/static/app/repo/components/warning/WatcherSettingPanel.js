import React, { Component, PropTypes } from 'react';

export default class WatcherSettingPanel extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let suggested_user_list = this.props.suggested_user_list;
        return (
            <div>
                <h4>人员设置</h4>
                <ui className="list-group">
                    {suggested_user_list.map((an_user, index) =>
                        <li className="list-group-item" key={an_user.owner_name}>
                            <a href={ '/' + an_user.owner_name }>{an_user.owner_name}</a>
                        </li>
                    )}
                </ui>
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
    repo: PropTypes.string.isRequired
};