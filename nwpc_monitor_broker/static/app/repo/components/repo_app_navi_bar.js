import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router'

export default class RepoAppNaviBar extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        let owner = this.props.owner;
        let repo = this.props.repo;

        let { router } = this.context;

        let settings_is_active = router.isActive({ pathname:'/' + owner + '/' + repo + '/settings'} );
        let warning_is_active = router.isActive({ pathname:'/' + owner + '/' + repo + '/warning'} );

        let sub_page_active_flag = false;
        if (settings_is_active || warning_is_active) {
            sub_page_active_flag = true;
        }

        let status_is_active = true;
        if (sub_page_active_flag) {
            status_is_active = false;
        }

        return (
            <section className="row" className="app-navi-bar">
                <ul className="nav nav-tabs">
                    <li  role="presentation"  className={ status_is_active?'active':'' } >
                        <Link to={{ pathname:'/' + owner + '/' + repo + '/' }} >状态</Link>
                    </li>
                    <li  role="presentation"  className={ warning_is_active?'active':'' } >
                        <Link to={{ pathname:'/' + owner + '/' + repo + '/warning' }} >报警</Link>
                    </li>
                    <li  role="presentation" className={ settings_is_active?'active':'' } >
                        <Link to={{ pathname:'/' + owner + '/' + repo + '/settings' }} >设置</Link>
                    </li>
                </ul>
            </section>
        );
    }
}

RepoAppNaviBar.propTypes = {
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired
};

RepoAppNaviBar.contextTypes = {
    router: PropTypes.object.isRequired
};
