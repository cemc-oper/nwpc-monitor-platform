import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

class UserApp extends Component{
    componentDidMount(){

    }

    render() {
        const { params } = this.props;
        let user = params.user;

        return (
            <div>
                <h1>User</h1>
                <h2>{user}</h2>

                {this.props.children}

            </div>
        );
    }
}


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(UserApp)