import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

export default class WeixinWarningApp extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let owner = this.props.params.owner;
        let repo = this.props.params.repo;
        return (
            <div>Weixin</div>
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(WeixinWarningApp)