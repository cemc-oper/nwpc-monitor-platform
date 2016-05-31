import React, { Component } from 'react';

export default class OrgMemberList extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        var rows = [];
        this.props.member_list.forEach(function (element, index, array) {
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

