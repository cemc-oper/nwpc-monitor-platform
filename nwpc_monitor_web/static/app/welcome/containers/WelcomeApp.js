import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

class WelcomeApp extends Component{
    componentDidMount(){

    }

    render() {
        const { params } = this.props;

        return (
            <div>
                <h1>Welcome</h1>
                {this.props.children}

            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(WelcomeApp)
