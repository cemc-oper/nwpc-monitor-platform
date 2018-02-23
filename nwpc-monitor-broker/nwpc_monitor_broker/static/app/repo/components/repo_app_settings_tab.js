import React, { Component, PropTypes } from 'react';

export default class RepoAppSettingsTab extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let owner = this.props.owner;
        let repo = this.props.repo;
        return (
            <section className="row">
                Settings Tab
            </section>
        );
    }
}

RepoAppSettingsTab.propTypes = {
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired
};
