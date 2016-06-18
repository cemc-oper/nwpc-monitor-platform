import React, { Component, PropTypes } from 'react';

export default class OrgMemberList extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        //console.log('member_list', this.props.member_list);
        return (
            <ui className="list-group">
                {this.props.member_list.map((member, index) =>
                    <li className="list-group-item" key={member.id}>{member.name}</li>
                )}
            </ui>
        );
    }
}

OrgMemberList.propTypes = {
    member_list: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired
    }).isRequired).isRequired
};


