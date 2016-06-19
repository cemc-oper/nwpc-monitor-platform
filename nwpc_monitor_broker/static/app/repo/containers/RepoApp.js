import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import PageHeader from '../../base/components/page_header'

class RepoApp extends Component{
    componentDidMount(){
    }

    render() {
        let url = {
            index_page: '/'
        };

        return (
            <div>
            <PageHeader url={ url }/>
                <section className="row">
                    <h1><span className="glyphicon glyphicon-book" aria-hidden="true" /> owner/repo </h1>
                </section>

                <section className="row">
                    <ul className="nav nav-tabs">
                        <li role="presentation" className="active"><a href="#">项目</a></li>
                        <li role="presentation"><a href="#">设置</a></li>
                    </ul>
                </section>

                <section className="row">
                </section>
            </div>
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(RepoApp)