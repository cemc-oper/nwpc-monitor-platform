import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

export default class OrgWarningApp extends Component{
    componentDidMount(){
    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        return (
            <div>
                <div className="col-md-12">
                    <h2>报警</h2>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(OrgWarningApp)