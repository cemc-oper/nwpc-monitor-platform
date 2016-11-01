import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import MonitorWebAppTab from '../../base/components/MonitorWebAppTab'

class OperationSystemApp extends Component{
    constructor(props) {
        super(props);
        this.state = {
            owner: ''
        }
    }

    onChange(e) {
        this.setState({owner: e.target.value});
    }

    handleClick(e) {
        e.preventDefault();
        console.log(this.state.owner);
        window.location.href='/'+this.state.owner;
    }

    render() {
        const { params } = this.props;
        let tab_bar_item_name = "operation-system";

        return (
            <div className="container">
                <div className="weui-tab">
                    <div className="weui-tab__panel">
                        {this.props.children}
                    </div>

                    <MonitorWebAppTab active_item={ tab_bar_item_name }/>
                </div>
            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(OperationSystemApp)
