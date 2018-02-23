import React, { Component, PropTypes } from 'react';

export default class RepoAppTitle extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let owner = this.props.owner;
        let repo = this.props.repo;
        return (
            <section className="row">
                    <h1>
                        <span className="glyphicon glyphicon-book" aria-hidden="true" />
                        <a href={ '/' + owner }>{ owner }</a>/<a href={ '/' + owner + '/' + repo }>{ repo }</a>
                    </h1>
            </section>
        );
    }
}

RepoAppTitle.propTypes = {
    owner: PropTypes.string.isRequired,
    repo: PropTypes.string.isRequired
};
