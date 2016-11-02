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

    renderChartDom(){
        const { data } = this.props;
        console.log(data);
        let { label, usage, total } = data;
        let echarts_instance = this.getEchartsInstance();

        echarts_instance.setOption({
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
                                    color: "rgb(47, 234, 73)"
                                }
                            }
                        },
                        {
                            value: total-usage,
                            name: '空闲',
                            itemStyle: {
                                normal: {
                                    color: "rgb(210, 251, 214)"
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
            height: 100
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
    })
};

FileSystemUsagePieChart.defaultProps = {

};