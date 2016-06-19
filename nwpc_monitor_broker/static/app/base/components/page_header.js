import React, { Component, PropTypes } from 'react';

export default class PageHeader extends Component{
    constructor(props) {
        super(props);
    }
    render() {
        let index_page_url = this.props.url.index_page; // {{ url_for('get_index_page') }}
        return (
            <nav className="navbar navbar-default">
                <div className="container-fluid">
                    <!-- Brand and toggle get grouped for better mobile display -->
                    <div className="navbar-header">
                        <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#monitor-broker-navbar-collapse" aria-expanded="false">
                            <span className="sr-only">Toggle navigation</span>
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                        </button>
                        <a className="navbar-brand" href={ index_page_url }>NWPC业务监控平台</a>
                    </div>

                    <!-- Collect the nav links, forms, and other content for toggling -->
                    <div className="collapse navbar-collapse" id="monitor-broker-navbar-collapse">
                        <form className="navbar-form navbar-left" role="search">
                            <div className="form-group">
                                <input type="text" className="form-control" placeholder="Search Monitor" />
                            </div>
                        </form>
                        <ul className="nav navbar-nav">
                            <li><a href={ index_page_url }>首页 <span className="sr-only">(current)</span></a></li>
                            <li><a href="#">功能</a></li>
                        </ul>
                        <ul className="nav navbar-nav navbar-right">
                            <li><a href="#">帮助</a></li>
                            <li className="dropdown">
                                <a href="#" className="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">用户 <span className="caret"></span></a>
                                <ul className="dropdown-menu">
                                    <li><a href="#">主页</a></li>
                                    <li><a href="#">帮助</a></li>
                                    <li role="separator" className="divider"></li>
                                    <li><a href="#">设置</a></li>
                                    <li><a href="#">注销</a></li>
                                </ul>
                            </li>
                        </ul>
                    </div><!-- /.navbar-collapse -->
                </div><!-- /.container-fluid -->
            </nav>
        );
    }
}


PageHeader.propTypes = {
    url: PropTypes.objectOf(PropTypes.string).isRequired
};


