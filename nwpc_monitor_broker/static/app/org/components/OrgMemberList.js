import React, { Component, PropTypes } from 'react';

export default class OrgMemberList extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        //console.log('member_list', this.props.member_list);
        return (
            <div>
                {this.props.member_list.map((member, index) =>
                    <p key={member.name}>{member.name}</p>
                )}
            </div>
        );
    }
}

OrgMemberList.propTypes = {
    member_list: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired
    }).isRequired).isRequired
};


