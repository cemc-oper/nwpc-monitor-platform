import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import MonitorWebAppTab from '../../base/components/MonitorWebAppTab'

class AboutApp extends Component{
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


function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(AboutApp)
