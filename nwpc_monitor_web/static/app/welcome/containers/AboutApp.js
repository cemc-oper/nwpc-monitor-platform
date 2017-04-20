import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import MonitorWebAppTab from '../../base/components/MonitorWebAppTab'
import {fetchUserInfo} from '../actions/index'

class AboutApp extends Component{
    constructor(props) {
        super(props);
        this.state = {
            owner: ''
        }
    }

    componentDidMount(){
        const { dispatch, params} = this.props;
        let location = this.props.location;
        let query = location.query;
        //console.log(location);
        //console.log(query);
        if(query.code){
            //console.log('has code');
            let code = query.code;
            dispatch(fetchUserInfo(code))
        }
    }

    onChange(e) {
        this.setState({owner: e.target.value});
    }

    handleClick(e) {
        e.preventDefault();
        //console.log(this.state.owner);
        window.location.href='/'+this.state.owner;
    }

    render() {
        const { params, user } = this.props;
        console.log(user);
        let user_info = (
                <p>未获取用户</p>
            );
        if(user.info.hasOwnProperty('UserId')){
            user_info = (
                <p>{user.info.UserId}</p>
            );
        }

        let tab_bar_item_name = "about";

        return (
            <div className="container">
                <div className="weui-tab">
                    <div className="weui-tab__panel">
                        <article className="weui-article">
                            <h1>关于</h1>
                            <section>
                                <h2 className="title">目标</h2>
                                <p>辅助业务系统运行维护。</p>
                            </section>
                            <section>
                                <h2 className="title">当前用户</h2>
                                <p>{user_info}</p>
                            </section>
                            <section>
                                <h2 className="title">维护</h2>
                                <p>***REMOVED***roc</p>
                            </section>
                        </article>
                    </div>

                    <MonitorWebAppTab active_item={ tab_bar_item_name }/>
                </div>
            </div>
        );
    }
}

AboutApp.propTypes = {
    user: (PropTypes.shape({
        info : PropTypes.object
    }))
};

AboutApp.defaultProps = {
    user: {
        info: {

        }
    }
};


function mapStateToProps(state){
    return {
        user: state.welcome.user
    }
}

export default connect(mapStateToProps)(AboutApp)
