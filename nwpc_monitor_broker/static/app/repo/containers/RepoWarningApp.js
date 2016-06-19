import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router'

class RepoWarningApp extends Component{
    componentDidMount(){

    }

    render() {
        const { params } = this.props;
        let owner = params.owner;
        let repo = params.repo;

        let { router } = this.context;

        let weixin_is_active = router.isActive( {pathname: '/' + owner + '/' + repo + '/warning/weixin'} );

        let sub_page_active_flag = false;
        if (weixin_is_active) {
            sub_page_active_flag = true;
        }

        let ding_talk_is_active = true;
        if (sub_page_active_flag) {
            ding_talk_is_active = false;
        }

        return (
            <section className="row">
                <div className="col-md-2">
                    <div className="list-group">
                        <Link to={{ pathname: '/'+owner+'/'+repo+'/warning' }} className={ ding_talk_is_active?'list-group-item active':'list-group-item'}  >
                            <span className="glyphicon glyphicon-fire" /> 钉钉
                        </Link>
                        <Link to={{ pathname:'/'+owner+'/'+repo+'/warning/weixin' }} className={ weixin_is_active?'list-group-item active':'list-group-item' }>
                            <span className="glyphicon glyphicon-fire" /> 微信
                        </Link>
                    </div>
                </div>
                <div className="col-md-10">
                    {this.props.children}
                </div>
            </section>
        );
    }
}

RepoWarningApp.contextTypes = {
    router: PropTypes.object.isRequired
};

function mapStateToProps(state){
    return {
    }
}

export default connect(mapStateToProps)(RepoWarningApp)