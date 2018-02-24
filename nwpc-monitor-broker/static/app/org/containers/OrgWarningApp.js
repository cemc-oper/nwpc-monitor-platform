import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router'
import classNames from 'classnames'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import {faFire, faUser, faPlane} from '@fortawesome/fontawesome-free-solid'
import faChessKing from "@fortawesome/fontawesome-free-solid/faChessKing";

export class OrgWarningApp extends Component{
  componentDidMount(){
  }

  render() {
    const { params } = this.props;
    let owner = params.owner;

    let { router } = this.context;

    let weixin_is_active = router.isActive( {pathname: '/orgs/' + owner + '/warning/weixin'} );

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
          <h3 className="row">
            钉钉
          </h3>
          <div className="row list-group">
            <Link to={{ pathname: '/orgs/'+owner+'/warning/ding_talk', hash:'#warn_ding_talk_overview' }}
                  className={ classNames({
                    active: ding_talk_is_active,
                    'list-group-item': true
                  })} >
              <FontAwesomeIcon icon={faFire} size="1x" /> 概览
            </Link>
            <Link to={{ pathname: '/orgs/'+owner+'/warning/ding_talk', hash:'#warn_ding_talk_warn_watching_panel' }}
                  className="list-group-item">
              <FontAwesomeIcon icon={faUser} size="1x" /> 人员设置
            </Link>
            <Link to={{ pathname: '/orgs/'+owner+'/warning/ding_talk', hash:'#warn_ding_talk_warn_policy_panel' }}
                  className="list-group-item">
              <FontAwesomeIcon icon={faPlane} size="1x" /> 推送策略
            </Link>
          </div>
          <h3 className="row">
            微信
          </h3>
          <div className="row list-group">
            <Link to={{ pathname:'/orgs/'+owner+'/warning/weixin' }}
                  className={ classNames({
                    active: weixin_is_active,
                    'list-group-item': true
                  })} >
              <FontAwesomeIcon icon={faFire} size="1x" /> 概览
            </Link>
            <Link to={{ pathname:'/orgs/'+owner+'/warning/weixin' }}
                  className="list-group-item">
              <FontAwesomeIcon icon={faUser} size="1x" /> 人员设置
            </Link>
            <Link to={{ pathname:'/orgs/'+owner+'/warning/weixin' }}
                  className="list-group-item">
              <FontAwesomeIcon icon={faPlane} size="1x" />  推送策略
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

OrgWarningApp.contextTypes = {
  router: PropTypes.object.isRequired
};

function mapStateToProps(state){
  return {
  }
}

export default connect(mapStateToProps)(OrgWarningApp)