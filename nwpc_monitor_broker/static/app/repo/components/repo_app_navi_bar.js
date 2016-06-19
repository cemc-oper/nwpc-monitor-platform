import React, { Component, PropTypes } from 'react';

export default class RepoAppNaviBar extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let owner = this.props.owner;
        let repo = this.props.repo;
        return (
            <section className="row">
                    <ul className="nav nav-tabs">
                        <li role="presentation" className="active"><a href="#">状态</a></li>
                        <li role="presentation"><a href="#">设置</a></li>
                    </ul>
                </section>
        );
    }
}

RepoAppNaviBar.propTypes = {
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired
};
