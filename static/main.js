function myTimeToLocal(timestamp) {
    var date = new Date(timestamp);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
    var D = date.getDate() + ' ';
    var h = date.getHours() + ':';
    var m = date.getMinutes() + ':';
    var s = date.getSeconds();
    return Y + M + D + h + m + s;

}//时间格式转换
function create_button_range(pro_name, type) {
    let div_id = '#off_' + pro_name;
    if (type === 'on') div_id = '#on_' + pro_name;
    // 图表名称
    let div = '<span class="btn-group"><button class="btn btn-primary dropdown-toggle" data-toggle="dropdown">'
        + '取值范围</button><div class="dropdown-menu range" name="the_ranges"' + 'onclick=event.stopPropagation()>';
    // 按钮容器
    let title = '<h5></h5><h4>最小值</h4><h4>最大值</h4>';
    let body = '';
    // let the_range = mychart[pro_name][type]["range"];
    let the_range =ranges[type];
    for (let i = 0; i < the_range.length; i++) {
        let min_value = '["' + pro_name + '","' + type + '","' + i + '",this.value,"min"]';
        let max_value = '["' + pro_name + '","' + type + '","' + i + '",this.value,"max"]';
        body += '<h5>' + the_range[i]['meaning'] + '</h5>' +   //字段名称
            '<input type="number" value =' + the_range[i]['min'] +
            ' onchange=change_page_range(' + min_value + ')>' +  //最小值
            '<input type="number" value =' + the_range[i]['max'] +
            ' onchange=change_page_range(' + max_value + ')>'; //最大值
    }
    // console.log(div + title + body + '</div></span>');
    console.log(div + title + body);
    $(div_id).after(div + title + body + '</div></span>');
}// 创建子取值范围按钮
function change_page_range([pro_name, graph_type, index, value, field_type]) {
    mychart[pro_name][graph_type]["range"][index][field_type] = Number(value);
    // mychart[pro_name][graph_type].chart.series[index].update();
}//输入 [项目名，类型，范围索引，改变值，"min"/"max"] 改变子页面范围
function create_button(pro_name, type) {
    let div_id = "#" + type + '_' + pro_name;
    let options = '';
    let div = '<span class="btn-group"><button class="btn btn-primary dropdown-toggle" data-toggle="dropdown">' +
        '图表样式</button><div class="dropdown-menu" style="width: 500px;height: 100px;float:left" ' +
        'onclick=event.stopPropagation()>';
    for (let h = 0; h < mychart[pro_name][type].chart.series.length; h++) {
        options += '<option>' + mychart[pro_name][type].chart.series[h].options.name + '</option>';
    }
    let field = '<span class="style_span"><h5>字段</h5><select id="' + pro_name + '_fields" ' +
        'onchange=change_field_name("' + pro_name + '","' + type + '")>' + options + '</select></span>';
    //字段
    let color = '<span class="style_span"><h5>颜色</h5><input id="' + pro_name + '_color" type="color" ' +
        'onchange=change("' + pro_name + '","color","' + type + '")></span>';
    //颜色
    let width = '<span class="style_span"><h5>线宽</h5><input  id="' + pro_name + '_width" type="number"' +
        ' onchange=change("' + pro_name + '","width","' + type + '")></span>';
    //线宽
    let dashs = '';
    for (let h = 0; h < dashStyles.length; h++) {
        dashs += '<option>' + dashStyles[h] + '</option>';
    }
    let dashStyle = '<span class="style_span"><h5>线型</h5><select id="' + pro_name + '_dash" onchange=change("'
        + pro_name + '","dashStyle","' + type + '")>' + dashs + '</select></span>';
    //线型
    console.log(div);
    console.log(field);
    console.log(color);
    console.log(width);
    console.log(dashStyle);
    $(div_id).after(div + field + color + width + dashStyle + '</div></span>');
    //输出按钮
    change_field_name(pro_name, type); //样式初始化
}//输入容器名，图表名称,创建图例按钮
function change_field_name(pro_name, type) {
    let index = $('#' + pro_name + '_fields').get(0).selectedIndex;
    $('#' + pro_name + '_color').val(mychart[pro_name][type].chart.series[index].color);
    $('#' + pro_name + '_width').val(mychart[pro_name][type].chart.series[index].options.lineWidth);
    $('#' + pro_name + '_dash').val(mychart[pro_name][type].chart.series[index].options.dashStyle);
}//图例字段选择
function display_mode(div_id, pro_name, in_index = 0, the_type, t = 60) {
    let option = '<option>分</option><option>时</option>';
    if (t === 3600) option = '<option>时</option><option>分</option>';
    let times = '<span class="btn-group"><span class="style_span" style="width:50%;margin:0">' +
        '<h6 style="margin:0;text-align: center;">显示方式</h6><select name="time_length" style="height:60%;" ' +
        'onchange=time_interval("' + pro_name + '",' + in_index + ',"' + the_type + '",this)>' + option + '</select></span></span>';
    $(div_id).after(times);
}//显示方式
function time_interval(pro_name, in_index, the_type, the_this) {
    console.log(the_this.value);
    let gap = 60;
    if (the_this.value === '时') gap = 3600;
    update_data(pro_name, in_index, the_type, gap)
} // 改变显示方式
function change(pro_name, style_type, type) {
    let index = $('#' + pro_name + '_fields').get(0).selectedIndex;
    console.log(mychart[pro_name][type].chart.series[index]);
    switch (style_type) {
        case 'color':
            mychart[pro_name][type].chart.series[index].update(
                {color: $('#' + pro_name + '_color').val()}
            );
            break;
        case 'width':
            mychart[pro_name][type].chart.series[index].update(
                {lineWidth: Number($('#' + pro_name + '_width').val())}
            );
            break;
        case 'dashStyle':
            mychart[pro_name][type].chart.series[index].update(
                {dashStyle: $('#' + pro_name + '_dash').val()}
            );
            break;
    }
}// 图例样式选择
function db_range_change(new_range, db_type = 'on') {
    $.ajax({
        type: 'POST',
        url: '/db_range/',
        data: {new_range: new_range, db_type: db_type},
        success: function () {
            $.growl.warning({message: '修改成功'});
        }
    })
}//数据范围更改
function all_range(div_id) {
    let on_span = '<span><h5>在线参数范围</h5><table><thead><tr><th></th><th><h5>最小值</h5>' +
        '</th><th><h5>最大值</h5></th></tr></thead><tbody>';
    for (let i = 0; i < ons.length; i++) {
        on_span += '<tr><td><b>' + ons[i]['meaning'] + '<b></td><td><input type="number" value=' + ons[i]['min']
            + ' onchange=db_range_change(["' + ons[i]['chars'] + '","min",Number(this.value)],"on")>' +
            '</td><td><input type="number" value=' + ons[i]['max'] +
            ' onchange=db_range_change(["' + ons[i]['chars'] + '","max",Number(this.value)],"on")></td></tr>';
    }//在线
    on_span += '</tbody></table><button>提交</button></span><span><h5>离线参数范围</h5>' +
        '<table><thead><tr><th></th><th><h5>最小值</h5></th><th><h5>最大值</h5></th></tr></thead><tbody>';
    for (let i = 0; i < offs.length; i++) {
        on_span += '<tr><td><b>' + offs[i]['meaning'] + '<b></td><td><input type="number" value=' + offs[i]['min']
            + ' onchange=db_range_change(["' + offs[i]['chars'] + '","min",Number(this.value)],"off")>' +
            '</td><td><input type="number" value=' + offs[i]['max'] + ' ' +
            'onchange=db_range_change(["' + offs[i]['chars'] + '","max",Number(this.value)],"off")></td></tr>';
    }//离线
    on_span += '</tbody></table><button>提交</button>';
    $(div_id).html(on_span);
}//创建范围数据库更改
function today() {
    let dates = document.getElementsByName('date');
    for (let i = 0; i < dates.length; i++) {
        dates[i].value = (new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate());
        console.log((new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()));
        console.log(dates[i].value);
    }
}

function chosen_on() {
    checkbox_save('collapse4', 'input', 'pro_off_fields');    //储存复选框选中的在线字段名
    let chosen_fields = getCookie('pro_on_fields').split(','); //获取选中的在线字段
    for (let i = 0, chosen_fields_length = chosen_fields.length; i < chosen_fields_length; i++) {
        let k = document.getElementsByName(chosen_fields[i]);
        for (let j = 0; j < k.length; j++)
            k[j].checked = true;
    }
}<!--表格中在线字段批量赋值true -->
function chosen_off() {
    checkbox_save('collapse3', 'input', 'pro_on_fields');    //储存复选框选中的离线字段名
    let chosen_off_fields = getCookie('pro_off_fields').split(','); //获取选中的离线字段
    for (let i = 0; i < chosen_off_fields.length; i++) {
        let x = document.getElementsByName(chosen_off_fields[i]);
        for (let j = 0; j < x.length; j++)
            x[j].checked = true;
    }
}<!-- 表格中离线字段批量赋值true-->
function draw_checkbox() {
    checkbox_save('collapse2', 'input', 'chosen_name');//储存复选框选中的项目名
    let chosen_name = getCookie('chosen_name').split(',');
    let tbody = '#tbody';
    $(tbody).empty();
    let tbody_str = '';
    for (let k = 0, chosen_name_length = chosen_name.length; k < chosen_name_length; k++) {
        tbody_str += '<tr><td>' + chosen_name[k] + '</td>';
        for (let i = 0, on_names_length = ons.length; i < on_names_length; i++) {
            tbody_str += '<td class="ons"><label><input type="checkbox" class="'
                + chosen_name[k] + '" name=' + ons[i]['chars'] + '></label></td>';
        }  <!-- 创建在线字段名-->
        for (let j = 0, off_names_length = offs.length; j < off_names_length; j++) {
            tbody_str += '<td class="offs"><label><input type="checkbox" class="'
                + chosen_name[k] + '" name=' + offs[j]['chars'] + '></label></td>';
        }<!-- 创建离线字段名-->
    }
    $(tbody).html(tbody_str);
    chosen_on();
    chosen_off();
}//绘制图表
function del_pro() {
    delCookie('chosen_name');
    // {#let chosen_name = getCookie('chosen_name').split(',');#}
    let all = document.getElementsByName('pro_name');
    for (let i = 0; i < all.length; i++)
        all[i].checked = false;
    draw_checkbox();
}//清空所选项目名
function del_field(the_type) {
    if (the_type === 'on') {
        delCookie('pro_on_fields');
        let chosen_dom = document.getElementsByName('on_fields');
        for (let i = 0; i < chosen_dom.length; i++)
            chosen_dom[i].checked = false;
    } else {
        delCookie('pro_off_fields');
        let chosen_dom = document.getElementsByName('off_fields');
        for (let i = 0; i < chosen_dom.length; i++)
            chosen_dom[i].checked = false;
    }
    draw_checkbox();
}//清除所选离/在字段
function del_all() {
    for (let i = 0; i < ons.length; i++) {
        let all = document.getElementsByName(ons[i]['chars']);
        for (let j = 0; j < all.length; j++)
            all[j].checked = false;
    }
    for (let i = 0; i < offs.length; i++) {
        let all = document.getElementsByName(offs[i]['chars']);
        for (let j = 0; j < all.length; j++)
            all[j].checked = false;
    }
}//清空所有字段
function draw_field(type = 'on', div_id) {
    let data = ons;
    if (type === 'off') data = offs;
    let txt = '';
    for (let i = 0; i < data.length; i++)
        txt += '<div><label><input type="checkbox" name="' + type + '_fields" value="' +
            data[i]["chars"] + '">' + data[i]["meaning"] + '</label></div>';
    $(div_id).append(txt);
}//参数list
function draw_pro(div_id) {
    let txt = '';
    for (let i = 0; i < pro_names.length; i++)
        txt += '<div><label><input type="checkbox" name="pro_name" value="' +
            pro_names[i] + '"</label>' + pro_names[i] + '</div>';
    $(div_id).append(txt);
}//项目list
function cr_table(div_id) {
    let txt = '<table class="table"><caption>生物参数</caption><thead style="position:relative"><tr><th>项目名称</th>';
    for (let i = 0; i < ons.length; i++) {
        txt += '<th class="ons">' + ons[i]['meaning'] + '</th>'
    }
    for (let i = 0; i < offs.length; i++) {
        txt += '<th class="offs">' + offs[i]['meaning'] + '</th>'
    }
    txt += '</tr> </thead> <tbody id="tbody"></tbody></table>';
    $(div_id).append(txt);
}//创建表头

//图表配置
let the_options = {
    chart: {
        events: {}
    },
    global: {
        useUTC: false
    },
    legend: {
        enabled: true,
        align: 'right',
        layout: 'vertical',
        verticalAlign: 'top',
        y: 100,
        shadow: true
    },
    noData: {
        style: {
            fontWeight: 'bold',
            fontSize: '15px',
            color: '#303030'
        }
    },
    plotOptions: {
        series: {
            // compare: 'percent',
            // {#showInNavigator: true#}
        }
        // showInNavigator: true
    },
    navigator: {
        // baseSeries: 2,
        adaptToUpdatedData: true,
        height: 70,
        series: {
            name: ''
        }
    },
    credits: {
        enabled: false
    },
    xAxis: {
        crosshair: {
            width: 2,
            color: 'green',
            dashStyle: 'shortdot'
        },
        minRange: 120,
        // {#minorTickInterval: 'auto',#}
        // {#startOnTick: true,#}
        // {#endOnTick: true#}
    },
    rangeSelector: {
        buttons: [{
            type: 'second',
            count: 1,
            text: '1秒'
        }, {
            type: "minute",
            count: 1,
            text: "1分钟"
        }, {
            type: "hour",
            count: 2,
            text: "2小时"
        }, {
            type: 'day',
            count: 1,
            text: '1天'
        }, {
            type: 'week',
            count: 1,
            text: '1周'
        }, {
            type: 'month',
            count: 1,
            text: '1个月'
        }, {
            type: 'month',
            count: 6,
            text: '6个月'
        }, {
            type: 'year',
            count: 1,
            text: '1年'
        }, {
            type: 'all',
            text: '全部'
        }],
        selected: 2
    },
    tooltip: {
        split: false,
        formatter: function () {

            //相对时间
            let relative = (this.x - Date.parse(mychart.begintime)) / 1000;
            let min = parseInt(relative / 60);
            let sec = relative % 60;
            let xIndex = this.point.index;
            let yIndex = this.series.index;
            //判断图表类型
            let type = this.series.chart.renderTo.id.split("_")[0];
            // {#console.log(yIndex);#}
            // {#mychart[type].chart.update({navigator:{baseSeries:4}});#}
            // {#console.log(this.series.index);#}
            return this.series.name + "<br>" + min + "分" + sec + '秒/' + myTimeToLocal(this.x) + "<br>" +
                this.y + "/" + mychart[type].series[xIndex][yIndex + 6];

        }
        // {#shared: true,#}
    },
};

