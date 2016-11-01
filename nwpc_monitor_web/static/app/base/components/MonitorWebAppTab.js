import React, { Component, PropTypes } from 'react';

export default class MonitorWebAppTab extends Component{
    constructor(props) {
        super(props);
    }

    render() {
        const { active_item, tab_items } = this.props;
        let links = [];

        tab_items.map(function(tab_item, index){
            let class_name = "weui-tabbar__item";
            if(tab_item.name == active_item) {
                class_name += " weui-bar__item_on";
            }
            links.push(
                <a href={ tab_item.link } className={ class_name } key={ index }>
                    <img src="/static/image/icon_tabbar.png" alt="" className="weui-tabbar__icon" />
                    <p className="weui-tabbar__label">{ tab_item.label }</p>
                </a>
            )

        });

        return (
            <div className="weui-tabbar">
                { links }
            </div>
        );
    }
}


MonitorWebAppTab.propTypes = {
    active_item: React.PropTypes.string.isRequired,
    tab_items: React.PropTypes.arrayOf(React.PropTypes.shape({
        name: React.PropTypes.string.isRequired,
        link: React.PropTypes.string.isRequired,
        label: React.PropTypes.string.isRequired
    }))
};

MonitorWebAppTab.defaultProps = {
    active_item: 'operation-system',
    tab_items: [
        {
            'name':'operation-system',
            'link': '/',
            'label': '系统'
        },
        {
            'name':'hpc/disk-usage',
            'link': '/',
            'label': '空间'
        },
        {
            'name':'hpc/loadleveler',
            'link': '/',
            'label': '队列'
        },
        {
            'name':'about',
            'link': '/',
            'label': '关于'
        },
    ]
};


