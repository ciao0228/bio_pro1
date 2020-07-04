 onmessage=function(event){
    // console.log(event);
     //获取数据
    let data=event.data;
    //所要输出的数据
    let series={};
    //每条数据长度
    let one_length=data.data[0].length;
    //数据列长度
    let range_length=data.range.length;
    // console.log(range_length);
    //  console.log("这是分线程");
    for(let j=0;j<range_length;j++){
        series[data.range[j].chars]=[];
        //判断数据是否处理，判断依据：差值是否大于0
        if(data.sub[j]<=0){
            // console.log(1);
            for(let i=0;i<data.data.length;i++){
                series[data.range[j].chars].push([data.data[i][one_length-1]*1000,data.data[i][j+6]])
            }
            // console.log(series[data.range[j].chars]);
        }else{
            // console.log(data.range[j].chars);
            for(let i=0;i<data.data.length;i++){
                series[data.range[j].chars].push([data.data[i][one_length-1]*1000,(data.data[i][j+6]-data.range[j].min)/data.sub[j]])
            }
        }
    }
    // console.log(series);
    postMessage(series);

    // console.log(1);
}