import React, { Component, PropTypes } from 'react';

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faUser from '@fortawesome/fontawesome-free-solid/faUser'

export default class OrgMemberList extends Component{
  constructor(props) {
    super(props);
  }
  render() {
    //console.log('member_list', this.props.member_list);
    return (
      <ui className="list-group">
        {this.props.member_list.map((member, index) =>
          <li className="list-group-item" key={member.id}>
            <FontAwesomeIcon icon={faUser} size="1x"/>
            <a href={ '/' + member.name }>{member.name}</a>
          </li>
        )}
      </ui>
    );
  }
}

OrgMemberList.propTypes = {
  member_list: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired
  }).isRequired).isRequired,

  owner: PropTypes.string.isRequired
};


