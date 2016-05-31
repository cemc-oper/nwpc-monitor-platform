import React, { Component } from 'react';

/* component */
export default class OrgRepoList extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        var rows = [];
        this.props.repo_list.forEach(function (element, index, array) {
            rows.push(
                <p key={element.name}>{element.name}</p>
            )
        });
        return (
            <div>
                {rows}
            </div>
        );
    }
}

OrgRepoList.propType = { repo_list: React.PropTypes.array };
OrgRepoList.defaultProps = { repo_list: [] };
