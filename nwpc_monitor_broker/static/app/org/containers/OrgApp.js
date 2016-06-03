import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import {fetchOrgRepos, fetchOrgMembers} from '../actions'

import OrgRepoList from '../components/OrgRepoList'
import OrgMemberList from '../components/OrgMemberList'

class OrgApp extends Component{
    componentDidMount(){
        const { dispatch, params } = this.props;
        let owner = params.owner;
        console.log('OrgApp:', owner);
        dispatch(fetchOrgRepos(owner));
        dispatch(fetchOrgMembers(owner))
    }

    render() {
        const { repo_list, member_list } = this.props;
        return (
            <div>
                <div className="col-md-8">
                    <h2>项目</h2>
                    <OrgRepoList repo_list={repo_list} />
                </div>
                <div className="col-md-4">
                    <h2>人员</h2>
                    <OrgMemberList member_list={member_list} />
                </div>
            </div>
        );
    }
}

OrgApp.propTypes = {
    repo_list: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired
    }).isRequired).isRequired,
    member_list: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired
    }).isRequired).isRequired
};

function mapStateToProps(state){
    return {
        repo_list: state.orgRepos.repos,
        member_list: state.orgMembers.members
    }
}

export default connect(mapStateToProps)(OrgApp)