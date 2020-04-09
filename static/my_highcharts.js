            function on_highchart(pro_on_data,div_id) {
                for (let x=0;x<pro_on_data.length;x++) {
                    let graph_name = pro_on_data[x][0][0];
                    $(div_id).append('<div id=' + graph_name + ' style="max-width:800px;height:400px"></div>');
                    $(div_id).append("<div><select></select></div><div><select></select></div>")
                    ;(function (x) {
                        $(function () {
                            let s = [];
                            for (let i = 2, pro_on_data_length = pro_on_data[x].length; i < pro_on_data_length; i++) {
                                let k = {};
                                k['name'] = pro_on_data[x][i][0];
                                k['data'] = pro_on_data[x][i][1];
                                k['dashStyle'] = 'Solid';
                                s.push(k)
                            }
                            let s1 = pro_on_data[x][0][0];
                            let plot_Lines = [];
                            for (let p = 0, l_length = parseInt(Number(pro_on_data[x][1][1].length / 10)); p < l_length; p++) {
                                let plot = {};
                                plot['color'] = 'red';
                                plot['dashStyle'] = 'longdashdot';
                                plot['value'] = p * 10;
                                plot['width'] = 1;
                                plot['id'] = p * 10;
                                plot_Lines.push(plot)
                            }
                            on_charts[x] = Highcharts.chart(s1, {
                                title: {
                                    text: pro_on_data[x][0][0]
                                },
                                chart: {
                                    zoomType: 'x'
                                },
                                xAxis: {
                                    categories: pro_on_data[x][1][1],
                                    plotLines: plot_Lines,
                                    crosshair: {
                                        width: 2,
                                        color: 'green',
                                        dashStyle: 'shortdot'
                                    },
                                    scrollbar: {
                                        enabled: true
                                    }

                                },
                                yAxis: {
                                    title: {
                                        text: '参数值'
                                    },
                                    crosshair: {
                                        width: 2,
                                        color: 'green',
                                        dashStyle: 'shortdot'
                                    }
                                },
                                legend: {
                                    layout: 'vertical',
                                    align: 'right',
                                    verticalAlign: 'middle'
                                },
                                plotOptions: {
                                    series: {
                                        label: {
                                            connectorAllowed: false
                                        }
                                    }
                                },
                                series: s,
                                responsive: {
                                    rules: [{
                                        condition: {
                                            maxWidth: 500
                                        },
                                        chartOptions: {
                                            legend: {
                                                layout: 'horizontal',
                                                align: 'center',
                                                verticalAlign: 'bottom'
                                            }
                                        }
                                    }]
                                }
                            });
                        })
                    })(x);
                }
            }
            function off_highchart(pro_off_data,div_id) {
                for (let x=0;pro_off_data.length;x++) {
                    let graph_name = 'off' + pro_off_data[x][0][0];
                    $(div_id).append('<div id=' + graph_name + ' style="max-width:800px;height:400px"></div>');
                    (function (x) {
                        $(function () {
                            let s = [];
                            for (let i = 2, pro_off_data_length = pro_off_data[x].length; i < pro_off_data_length; i++) {
                                let k = {};
                                k['name'] = pro_off_data[x][i][0];
                                k['data'] = pro_off_data[x][i][1];
                                k['dashStyle'] = 'Solid';
                                s.push(k)
                            }
                            let s1 = 'off' + pro_off_data[x][0][0];
                            let plot_Lines = [];
                            for (let p = 0, l_length = parseInt(Number(pro_off_data[x][1][1].length / 10)); p < l_length; p++) {
                                let plot = {};
                                plot['color'] = 'red';
                                plot['dashStyle'] = 'longdashdot';
                                plot['value'] = p * 10;
                                plot['width'] = 1;
                                plot['id'] = p * 10;
                                plot_Lines.push(plot)
                            }
                            off_charts[x] = Highcharts.chart(s1, {
                                title: {
                                    text: pro_off_data[x][0][0]
                                },
                                chart: {
                                    zoomType: 'x'
                                },
                                xAxis: {
                                    categories: pro_off_data[x][1][1],
                                    plotLines: plot_Lines,
                                    crosshair: {
                                        width: 2,
                                        color: 'green',
                                        dashStyle: 'shortdot'
                                    },
                                    scrollbar: {
                                        enabled: true
                                    }

                                },
                                yAxis: {
                                    title: {
                                        text: '参数值'
                                    },
                                    crosshair: {
                                        width: 2,
                                        color: 'green',
                                        dashStyle: 'shortdot'
                                    }
                                },
                                legend: {
                                    layout: 'vertical',
                                    align: 'right',
                                    verticalAlign: 'middle'
                                },
                                plotOptions: {
                                    series: {
                                        label: {
                                            connectorAllowed: false
                                        }
                                    }
                                },
                                series: s,
                                responsive: {
                                    rules: [{
                                        condition: {
                                            maxWidth: 500
                                        },
                                        chartOptions: {
                                            legend: {
                                                layout: 'horizontal',
                                                align: 'center',
                                                verticalAlign: 'bottom'
                                            }
                                        }
                                    }]
                                }
                            });
                        })
                    })(x)
                }
            }