//用ajax渲染首页右上角登录状态(检查用户登录状态)
function check_session(){
	// 使用jquery向后台发送异步请求
	// $.get(url,data,callback,datatype),data用来接受后端返回的数据
    $.get('/index/check_session',function(data){
        var html = ''
		//{loginStage:0} 未登录
		//此处后端返回的是json串，到这儿就变成了js对象
        if (data.loginStage == 0){
            html = "<a href='/index/login'>[登录]</a>,";
            html = html + "<a href='/index/register'>[注册，有惊喜]</a>";
        }else{
			//{'loginStage':1,'username':'session_username'}
            html += "欢迎：" + data.username;
			html += "<a href='/index/logout'>退出</a>"
        }
		// $('xxx'):选择器
		// xxx.html():设置或读取标签内容，可识别标签
        $('#login').html(html)
    },'json');
}


//Ajax渲染前端goods显示
function loadGoods(){
    $.get('/index/load_goods',function(data){
        //[{'type':{'title':xxx},'goods':[{'title':xx,}] }, ... ]
        var show = ''
        $.each(data, function(i, obj){
            show += '<div class="title">';
                show += '<h3 class="fl">' + obj.type.title + '</h3>'
                show += '<div class="fr">更多</div>';
                show += '<div class="cb"></div>';
            show += '</div>';

            show += '<ul>'
            $.each(obj.goods, function(ix,gobj){
                //循环商品 生成 li 区域
                show += '<li class="fl">';
                    show += '<div class="box">';
                        show += '<figure>'
                        show += '<img src="/' + gobj.picture + '">'
                        show += '</figure>';
                        show += '<div class="tip">';
                            show += '<div class="fl">';
                                show += '<h4>' + gobj.title + '</h4>';
                                show += '<p>$' + gobj.price + '/' + gobj.spec + '</p>';
                            show += '</div>';
                            show += '<div class="fr">';
                                show += '<figure>';
                                    show += '<img src="/static/imgs/cart.png">';
                                show += '</figure>';
                            show += '</div>';
                            show += '<div class="cb"></div>'
                        show += '</div>';
                    show += '</div>';
                show += '</li>';

            })
            show += '</ul>';
        });
       $('#main').html(show);
    },'json');
}


$(function(){
    //1 check_session
    check_session();
    //2 load goods
    loadGoods();
})
