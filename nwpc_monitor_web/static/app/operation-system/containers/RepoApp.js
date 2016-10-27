import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

class RepoApp extends Component{
    componentDidMount(){
    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        let repo = params.repo;

        return (
            <div>
                <h1>Repo App</h1>
                <p>{owner}/{repo}</p>
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(RepoApp)