import React, { Component, PropTypes } from 'react';

/* component */
export default class OrgRepoList extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        //console.log('repo_list', this.props.repo_list);
        return (
            <div>
                {this.props.repo_list.map((repo, index) =>
                    <p key={repo.name}>{repo.name}</p>
                )}
            </div>
        );
    }
}

OrgRepoList.propTypes = {
    repo_list: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired
    }).isRequired).isRequired
};