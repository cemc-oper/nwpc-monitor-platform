import React, { Component, PropTypes } from 'react';

export default class MonitorWebAppTab extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="weui-tabbar">
                <a href="/" className="weui-tabbar__item weui-bar__item_on">
                    <img src="/static/images/icon_tabbar.png" alt="" className="weui-tabbar__icon" />
                    <p className="weui-tabbar__label">系统</p>
                </a>
                <a href="/hpc/disk-usage" className="weui-tabbar__item">
                    <img src="/static/images/icon_tabbar.png" alt="" className="weui-tabbar__icon" />
                    <p className="weui-tabbar__label">空间</p>
                </a>
                <a href="/hpc/loadleveler" className="weui-tabbar__item">
                    <img src="/static/images/icon_tabbar.png" alt="" className="weui-tabbar__icon" />
                    <p className="weui-tabbar__label">队列</p>
                </a>
                <a href="/about" className="weui-tabbar__item">
                    <img src="/static/images/icon_tabbar.png" alt="" className="weui-tabbar__icon" />
                    <p className="weui-tabbar__label">关于</p>
                </a>
            </div>
        );
    }
}


MonitorWebAppTab.propTypes = {
};


