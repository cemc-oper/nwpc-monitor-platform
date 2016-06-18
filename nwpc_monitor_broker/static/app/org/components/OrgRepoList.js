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
                    <div className="panel panel-default" key={repo.id}>
                        <div className="panel-body">
                            <a>{repo.name}</a>
                            <p>repo description</p>
                        </div>
                    </div>
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