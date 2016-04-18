define(function (require, exports, module) {
    var $ = require('$');
    var ajax = require('../../lib/util/ajax');
    var DateX = require('../../lib/util/date');
    var highcharts = require('highcharts');
    var json = require('../../lib/util/json');
    var Tip = require('./tip');

    var helper = {
        // 基地址
        /**
         * JSON字符串化
         */
        stringify: function (obj) {
            return json.stringify(obj);
        },
        showLineChart: function (node, category, data, textY, unit) {
            /*var step = 1;
             if (category.length > 10) {
             var len = category.length;
             var step = Math.floor(len / 9);
             }*/
            var params = {
                chart: {
                    borderColor: '#FFFFFF',
                    borderRadius: 0,
                    borderWidth: 0,
                    type: 'line',
                    marginBottom: 50
                },
                title: {
                    text: '',
                    x: -20 //center
                },
                legend: {
                    enabled: false
                },
                colors: ['#84cdff', '#f18f6c', '#a4cf88'],
                xAxis: {
                    categories: category,
                    labels: {
                        style: {
                            color: '#9b9b9b'
                        }
                    }
                },
                yAxis: {
                    title: {
                        text: ''
                    },
                    labels: {
                        style: {
                            color: '#9b9b9b'
                        }
                    },
                    plotLines: [
                        {
                            value: 0,
                            width: 1,
                            color: '#84cdff'
                        }
                    ]
                },
                tooltip: {
                    valueSuffix: unit || '个'
                },
                series: data
            };
            if (category.length > 10) {
                params.xAxis = {
                    type: 'datetime',
                    dateTimeLabelFormats: { // 输出格式
                        week: '%Y-%m-%d'
                        //month: '%Y-%m-%d'
                    },
                    labels: {
                        formatter: function () {
                            // console.log(this.value);
                            return highcharts.highcharts.dateFormat('%m-%d', this.value);
                        },
                        style: {
                            color: '#9b9b9b'
                        }
                    }
                };
                var pointStart = category[0].split('-');
                params['plotOptions'] = {
                    line: {
                        pointStart: Date.UTC(+pointStart[0], +pointStart[1] - 1, +pointStart[2]), // 起始日期
                        pointInterval: 24 * 3600 * 1000 // 时间间隔，按天算
                    }
                };
                params['tooltip'] = {
                    formatter: function () {
                        return highcharts.highcharts.dateFormat('%Y-%m-%d', this.x) + ' ' + this.series.name + ' : ' + this.y + ( unit || '元' );
                    }
                };
            }
            node.highcharts(params);
        },
        showColumnChart: function (node, category, data, textY, unit) {
            /*var step = 1;
             if (category.length > 10) {
             var len = category.length;
             var step = Math.floor(len / 9);
             }*/
            var params = {
                chart: {
                    type: 'column'
                },
                title: {
                    text: '',
                    x: -20 //center
                },
                xAxis: {
                    categories: category
                },
                yAxis: {
                    title: {
                        text: textY || ''
                    },
                    plotLines: [
                        {
                            value: 0,
                            width: 1,
                            color: '#808080'
                        }
                    ]
                },
                tooltip: {
                    valueSuffix: unit || '个'
                },
                series: data
            };
            if (category.length > 10) {
                params.xAxis = {
                    type: 'datetime',
                    dateTimeLabelFormats: { // 输出格式
                        week: '%Y-%m-%d'
                        //month: '%Y-%m-%d'
                    },
                    labels: {
                        formatter: function () {
                            return highcharts.highcharts.dateFormat('%m-%d', this.value);
                        }
                    }
                };
                var pointStart = category[0].split('-');
                params['plotOptions'] = {
                    line: {
                        pointStart: Date.UTC(+pointStart[0], +pointStart[1] - 1, +pointStart[2]), // 起始日期
                        pointInterval: 24 * 3600 * 1000 // 时间间隔，按天算
                    }
                };
                params['tooltip'] = {
                    formatter: function () {
                        return highcharts.highcharts.dateFormat('%Y-%m-%d', this.x) + ' ' + this.series.name + ' : ' + this.y + ( unit || '元' );
                    }
                };
            }
            node.highcharts(params);
        },
        showColumnPercentageChart: function (node, category, data, textY, unit) {
            var step = 1;
            if (category.length > 10) {
                var len = category.length;
                step = Math.floor(len / 9);
            }
            // console.log(step);
            // console.log(category);
            // console.log(data);
            var params = {
                chart: {
                    type: 'column'
                },
                title: {
                    text: '',
                    x: -20 //center
                },
                colors: ['#96c8ea', '#f18f6c', '#a4cf88', '#738ecc', '#6ab7e3', '#f18940'],
                xAxis: {
                    categories: category
                    // type: 'datetime',
                    // dateTimeLabelFormats: { // 输出格式
                    //     week: '%Y-%m-%d'
                    //     //month: '%Y-%m-%d'
                    // },
                    // labels: {
                    //     rotation: 270,
                    //     formatter: function() {
                    //         console.log(this.value);
                    //         console.log(new Date(Date.parse(this.value.replace(/-/g,   "/"))).getTime());
                    //         return highcharts.highcharts.dateFormat('%m-%d', new Date(Date.parse(this.value.replace(/-/g,   "/"))).getTime());
                    //     }
                    // }
                },
                yAxis: {
                    title: {
                        text: ''
                    },
                    plotLines: [
                        {
                            value: 0,
                            width: 1,
                            color: '#808080'
                        }
                    ]
                },
                tooltip: {
                    valueSuffix: unit || '个'
                },
                plotOptions: {
                    column: {
                        stacking: 'percent'
                    }
                },
                series: data
            };
            if (category.length > 10) {
                params.xAxis = {
                    categories: category,
                    type: 'datetime',
                    dateTimeLabelFormats: { // 输出格式
                        week: '%Y-%m-%d'
                        //month: '%Y-%m-%d'
                    },
                    labels: {
                        formatter: function () {
                            // console.log(this.value);
                            var date = DateX.stringToDate(this.value);
                            return DateX.format(date, 'MM-dd');
                        },
                        step: step
                    }
                };
                // var pointStart = category[0].split('-');
                // params['plotOptions'] = {
                //     line: {
                //         pointStart: Date.UTC(+pointStart[0], +pointStart[1] - 1, +pointStart[2]), // 起始日期
                //         pointInterval: 24 * 3600 * 1000 // 时间间隔，按天算
                //     }
                // };
                // params['tooltip'] = {
                //     formatter: function () {
                //         return highcharts.highcharts.dateFormat('%Y-%m-%d', this.x) + ' ' + this.series.name + ' : ' + this.y + ( unit || '元' );
                //     }
                // };
            }
            node.highcharts(params);
        },
        showPieChart: function (node, category, data, textY, unit) {
            /*var step = 1;
             if (category.length > 10) {
             var len = category.length;
             var step = Math.floor(len / 9);
             }*/
            var params = {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false
                },
                title: {
                    text: '',
                    x: -20 //center
                },
                xAxis: {
                    categories: category
                },
                yAxis: {
                    title: {
                        text: textY || ''
                    },
                    plotLines: [
                        {
                            value: 0,
                            width: 1,
                            color: '#808080'
                        }
                    ]
                },
                tooltip: {
                    valueSuffix: unit || '个'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            distance: -100,
                            enabled: true,
                            color: '#fff',
                            connectorColor: '#000000',
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                        }
                    }
                },
                series: [{
                    type: 'pie',
                    name: '在线来源',
                    data: data
                }]
            };
            node.highcharts(params);
        },
        strToTimestamp: function (datestr) {
            //转换为UNIX时间戳
            var new_str = datestr.replace(/:/g, "-");
            new_str = new_str.replace(/ /g, "-");
            var arr = new_str.split("-");
            var datum = new Date(Date.UTC(arr[0], arr[1] - 1, arr[2], arr[3], arr[4], arr[5]));
            return (datum.getTime() / 1000);  //为PHP所用
        },
        timestampToStr: function (timestamp) {
            //UNIX时间戳转换为字符串
//            var unixTimestamp = new Date(timestamp * 1000);
            var d = new Date(timestamp * 1000);
            var fix0 = function (v) {
                return (v < 10 ? '0' + v : v);
            };
            return (d.getFullYear()) + "-" + fix0(d.getMonth() + 1) + "-" + fix0(d.getDate()) + " " + fix0(d.getHours()) + ":" + fix0(d.getMinutes()) + ":" + fix0(d.getSeconds());
        },
        decode: function(s) {
            return unescape(s.replace(/\\(u[0-9a-fA-F]{4})/gm, '%$1'));
        }

    };

    $(function () {
        //顶部bar以及左侧导航的事件定义
        $('.show-dropdown').on('mouseenter', function () {
            $(this).find('.dropdown-menu').eq(0).show();
        }).on('mouseleave', function () {
            $(this).find('.dropdown-menu').eq(0).hide();
        });
        $('.dropdown-menu').on('mouseleave', function () {
            $(this).hide();
            $('.show-dropdown').on('mouseover', function () {
                $(this).find('.dropdown-menu').eq(0).show();
            });
        });
        $('.clock-list .btn-part').on('mouseenter', function () {
            $(this).siblings('.float-site-clock').eq(0).show();
        }).on('mouseleave', function () {
            $(this).siblings('.float-site-clock').eq(0).hide();
        });
        $('.float-site-clock').on('mouseenter', function () {
            $(this).show();
        }).on('mouseleave', function () {
            $(this).hide();
        });
        $('.subtitle').on('click', function () {
            var node = $(this).closest('li');
            if (node.hasClass('expanded')) {
                node.removeClass('expanded').find('.caret-down').eq(0).show();
                node.find('.caret-up').eq(0).hide();
            } else {
                node.addClass('expanded').find('.caret-down').eq(0).hide();
                node.find('.caret-up').eq(0).show();
            }
        });

        //右侧顶部栏的效果
        $('.tb-filter').on('mouseenter', function () {
            $(this).find('.s-row').eq(0).slideDown();
        }).on('mouseleave', function () {
            $(this).find('.s-row').eq(0).slideUp();
        });
        $('.sidebar').delegate('li', 'mouseenter', function() {
            if (!$(this).hasClass('submenu')) {
                $(this).addClass('hover');
            }
        }).delegate('li', 'mouseleave', function() {
            $(this).removeClass('hover');
        });
    });

    module.exports = helper;
});
