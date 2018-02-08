/*
 * phenix base js 
 */

/**
 * 全局变量声明
 */

var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

var phenix = {
	    // 当前访问者用户信息
	    visitor: {},
		url : {},
		redirect: function(url,delay) {
	        setTimeout(function(){
				window.location = url;
			},delay);
	    },
	    show_error_note: function(msg,delay) {
			msg = '<div class="content">'+ msg +'</div>';
	    	phenix.show_notify_bar(msg,'error',delay);
	    },
	    show_ok_note:function(msg,delay) {
			msg = '<div class="content">'+ msg +'</div>';
	    	phenix.show_notify_bar(msg,'ok', delay);
	    },
	    show_notify_bar: function(msg,type,delay) {
            var class_name;
	        if(!type || type == 'ok'){
	        	type = 'ok';
				class_name = 'success';
	        }else{
				type = 'error';
				class_name = 'error';
	        }
			
			$.gritter.add({
				title: '',
				text: msg,
				time: delay,
				class_name: class_name,
			});
            // 让显示框可以显示在弹出层之上
            $('#gritter-notice-wrapper').css({'z-index':1000});
	    }
};

phenix.show_error_message = function(errors, ele) {
	var html = '<ul class="list">';
  	if ($.isArray(errors)) {
	  	$.each(errors, function(index, value) {
	    	html += '<li>' + value + '</li>';
	  	});
  	} else {
  		html += '<li>' + errors + '</li>';
  	}
  	html += '</ul>';
  	
	$('<div/>')
		.addClass('ui danger message')
		.html(html)
		.prependTo(ele);
};

/*
 * 初始化,设置常用的ajax hook
 */
phenix.initial = function(){
	/* 此类为确认后执行的ajax操作 */
	$('a.confirm-request').on('click', function(){
        if(confirm('确认执行这个操作吗?')){
            $.post($(this).attr('href'), {}, function(rs){
                if(rs.success){
                    if(rs.data.type==1){
                        arr = rs.data.ids.split(',');
                        for(var i=0;i<arr.length;i++){
                            $('#item-'+arr[i]).remove();
                        }
                    }
                }else{
                    alert(rs.message);
                }
            }, 'json');
        }
        return false;
	});	

	/* 此类为确认后执行的ajax操作 */
	$('a.ajax-batch-delete').on('click', function(){
        if(confirm('确认执行这个操作吗?')){
            var chk_value = Array();
            $("input[name='check-item']:checked").each(function(){ 
                chk_value.push($(this).val()); 
            });
            ids = chk_value.join(',');
            if(!ids){
                alert('请选择要删除的项目!');
                return false;
            }
            $.post($(this).attr('href'), {ids: ids}, function(rs){
                if(rs.success){
                    arr = rs.data.ids.split(',');
                    for(var i=0;i<arr.length;i++){
                        $('#item-'+arr[i]).remove();
                    }
                }else{
                    alert(rs.message);
                }
            }, 'json');
        }
        return false;
	});	
    
    /* 此类为ajax链接 */
	$('a.ajax').on('click', function(){
        var res_url = $(this).attr('href');
        // 所有ajax请求，验证是否登录
        if (!phenix.visitor.is_login){
            phenix.show_login_box(res_url);
            return false;
        }
        // 发送ajax请求
        $.get(res_url);
        
        return false;
	});
};


/**
 * 允许多附件上传
 */
phenix.record_asset_id = function(class_id, id){
    var ids = $('#'+class_id).val();
    if (ids.length == 0){
        ids = id;
    }else{
        if (ids.indexOf(id) == -1){
            ids += ','+id;
        }
    }
    $('#'+class_id).val(ids);
};

//移除附件id
phenix.remove_asset_id = function(class_id, id){
    var ids = $('#'+class_id).val();
    var ids_arr = ids.split(',');
    var is_index_key = phenix.in_array(ids_arr,id);
    ids_arr.splice(is_index_key,1);
    ids = ids_arr.join(',');
    $('#'+class_id).val(ids);
};

//查看字符串是否在数组中存在
phenix.in_array = function(arr, val) {
    var i;
    for (i = 0; i < arr.length; i++) {
        if (val === arr[i]) {
            return i;
        }
    }
    return -1;
}; // 返回-1表示没找到，返回其他值表示找到的索引

// Mustache render result
phenix.ajax_render = function(eid, data){
    var template = $(eid).html(), rendered = Mustache.render(template, data);
    //console.log(template);
    return rendered;
};
