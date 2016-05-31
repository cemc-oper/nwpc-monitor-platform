import React, { Component } from 'react';

/* component */
export class OrgRepoList extends Component {
    constructor(props) {
        super(props);
        this.state = {repo_list: props.repo_list};
    }
    componentDidMount() {
        var component = this;
        component.setState({
            repo_list: [
            {name: 'nwpc_op'},
            {name: 'nwpc_qu'},
            {name: 'eps_nwpc_qu'}
        ]});
    }
    render() {
        var rows = [];
        this.state.repo_list.forEach(function (element, index, array) {
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



export class OrgMemberList extends Component{
    constructor(props) {
        super(props);
        this.state = {member_list: props.member_list};
    }

    componentDidMount() {
        var component = this;
        component.setState({
            member_list:[
                {name: 'wangdp'},
                {name: 'cuiyj'},
                {name: 'wangyt'},
                {name: 'jiaxzh'}
            ]
        })
    }

    render() {
        var rows = [];
        this.state.member_list.forEach(function (element, index, array) {
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

OrgMemberList.propType = { member_list: React.PropTypes.array };
OrgMemberList.defaultProps = {member_list: []};

