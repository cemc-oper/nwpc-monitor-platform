import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';


class RepoWarningApp extends Component{
    componentDidMount(){

    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        let repo = params.repo;

        return (
            <section className="row">
                <div className="col-md-2">
                    <div className="list-group">
                        <a href="#" className="list-group-item active">
                            <span className="glyphicon glyphicon-fire" /> 钉钉
                        </a>
                        <a href="#" className="list-group-item">
                            <span className="glyphicon glyphicon-fire" /> 微信
                        </a>
                    </div>
                </div>
                <div className="col-md-10">
                    Warning Tab
                </div>
            </section>
        );
    }
}

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(RepoWarningApp)