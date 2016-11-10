import React, { Component, PropTypes } from 'react';
import echarts from 'echarts'

import elementResizeEvent from 'element-resize-event';

export default class FileSystemUsagePieChart extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){
        let echarts_instance = echarts.init(this.refs.chart_dom);
        this.renderChartDom();

        elementResizeEvent(this.refs.chart_dom, function() {
            echarts_instance.resize();
        });
    }

    componentDidUpdate(){
        this.renderChartDom();
    };

    componentWillUnmount(){
        echarts.dispose(this.refs.chart_dom);
    }

    getEchartsInstance(){
        return echarts.getInstanceByDom(this.refs.chart_dom);
    }

    getUsedColor(value){
        const { config } = this.props;
        if(config.warning.inRange(value)){
            return config.warning.used_color;
        } else {
            return config.normal.used_color;
        }
    }

    getFreeColor(value){
        const { config } = this.props;
        if(config.warning.inRange(value)){
            return config.warning.free_color;
        } else {
            return config.normal.free_color;
        }
    }

    renderChartDom(){
        const { data, config } = this.props;
        let { label, usage, total } = data;
        let echarts_instance = this.getEchartsInstance();

        echarts_instance.setOption({
            title:{
                text: label,
                top: 'center',
                left: 'center',
                textStyle: {
                    fontWeight: 'normal',
                    fontSize: 15
                }
            },
            series: [
                {
                    'name': '使用情况',
                    type: 'pie',
                    radius: [ '50%', '70%' ],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        }
                    },
                    data: [
                        {
                            value: usage,
                            name:'使用',
                            itemStyle: {
                                normal: {
                                    color: this.getUsedColor(usage/total)
                                }
                            }
                        },
                        {
                            value: total-usage,
                            name: '空闲',
                            itemStyle: {
                                normal: {
                                    color: this.getFreeColor(usage/total)
                                }
                            }

                        }
                    ]
                }
            ]
        });
        return echarts_instance;
    }

    render() {
        const { data } = this.props;
        let chart_style = {
            height: 150
        };

        return (
            <div ref="chart_dom" style={ chart_style }>

            </div>
        )
    }
}

FileSystemUsagePieChart.propTypes = {
    data: PropTypes.shape({
        label: PropTypes.string,
        usage: PropTypes.number,
        total: PropTypes.number
    }),
    config: PropTypes.object
};

FileSystemUsagePieChart.defaultProps = {
    config: {
        normal: {
            used_color: 'rgb(49,163,84)',
            free_color: 'rgb(247,252,185)',
            inRange: function(value){
                let min = 0;
                let max = 0.9;
                return value>=min && value<max
            }
        },
        warning: {
            used_color: 'rgb(240,59,32)',
            free_color: 'rgb(255,237,160)',
            inRange: function(value){
                let min = 0.9;
                let max = 1.0;
                return value>=min && value<=max
            }
        }
    },
};