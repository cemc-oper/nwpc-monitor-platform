import React, { Component, PropTypes } from 'react';

export default class OrgAppTitle extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let owner = this.props.owner;
        return (
            <section className="row">
                <h1>
                    <span className="glyphicon glyphicon-king" aria-hidden="true" />
                    <a href={ '/' + owner }>{ owner }</a>
                </h1>
            </section>
        );
    }
}

OrgAppTitle.propTypes = {
    owner: PropTypes.string.isRequired
};
