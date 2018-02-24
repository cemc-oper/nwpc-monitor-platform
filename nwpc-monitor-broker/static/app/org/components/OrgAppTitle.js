import React, { Component, PropTypes } from 'react';

const octicons = require("octicons");

export default class OrgAppTitle extends Component{
  constructor(props) {
    super(props);
  }
  render() {
    let owner = this.props.owner;
    const org_icon_node = octicons.organization.toSVG({ "width": 30 });
    return (
      <section className="row">
        <h1>
          <span dangerouslySetInnerHTML={{__html: org_icon_node}} />
          <a href={ '/' + owner }>{ owner }</a>
        </h1>
      </section>
    );
  }
}

OrgAppTitle.propTypes = {
  owner: PropTypes.string.isRequired
};
