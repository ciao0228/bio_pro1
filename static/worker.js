 onmessage=function(event){
    // console.log(event);
     //��ȡ����
    let data=event.data;
    //��Ҫ���������
    let series={};
    //ÿ�����ݳ���
    let one_length=data.data[0].length;
    //�����г���
    let range_length=data.range.length;
    // console.log(range_length);
    //  console.log("���Ƿ��߳�");
    for(let j=0;j<range_length;j++){
        series[data.range[j].chars]=[];
        //�ж������Ƿ����ж����ݣ���ֵ�Ƿ����0
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