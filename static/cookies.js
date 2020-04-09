function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
    }
    return "";
} //获取cookie

function delCookie(name) {
    let exp = new Date();
    exp.setTime(exp.getTime() - 1);
    let cval = getCookie(name);
    if (cval != null)
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}
//删除cookie

function checkbox_save(Dom_id, inline_tagname, cookie_name) {
    let chosen_dom = document.getElementById(Dom_id), dom_tagname = chosen_dom.getElementsByTagName(inline_tagname);
    chosen_dom.onclick = function (e) {
        e = e || window.event;
        let o = e.target || e.srcElement;
        if (o.type === 'checkbox') {
            let cookie_str = '';
            for (let i = 0; i < dom_tagname.length; i++)
                if (dom_tagname[i].checked) cookie_str += ',' + dom_tagname[i].value;
            document.cookie = cookie_name + '=' + cookie_str.substring(1);//存储选中的checkbook的值
        }
    };
    let the_cookie = getCookie(cookie_name);
    if (the_cookie) {//cookie中有值，初始化勾选状态
        let cookie_list = the_cookie.split(',');
        for (let j = 0; j < cookie_list.length; j++)
            for (let i = 0; i < dom_tagname.length; i++)
                if (dom_tagname[i].value === cookie_list[j]) {
                    dom_tagname[i].checked = true;
                    break;
                }
    }
}
//复选框储存cookie