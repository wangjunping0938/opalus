/**
 * 左侧菜单点击事件
 */
$('.memMenuTitle').click(function(){
    var s = $(this).attr('tabindex');
    var r = $(this).data('rel');
    if(s==-1){
        $('#'+r).show();
        $(this).attr('title', '收起');
        $(this).attr('tabindex', '1');
    }else{
        $('#'+r).hide();
        $(this).attr('tabindex', '-1');
        $(this).attr('title', '展开');
    }
});

/**
 * 左侧菜单点初始化
 */
$('.memMenuTitle.active').each(function(){
    var s = $(this).attr('tabindex');
    var r = $(this).data('rel');
    $('#'+r).show();
    $(this).attr('title', '收起');
    $(this).attr('tabindex', '1');
})

/**
 * 全选/返选
 */
$("#check-all").click( 
  function(){ 
    if(this.checked){ 
        $("input[name='check-item']").prop('checked', true);
    }else{ 
        $("input[name='check-item']").prop('checked', false);
    } 
  } 
);


