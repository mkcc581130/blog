$(function(){

	var $_ta_len = 0;
	$('.main-aside').height($(window).height()-40);
	$('.dropdown').mouseenter(function(){
		$(this).addClass('open');
	});
	$('.dropdown').mouseleave(function(){
		$(this).removeClass('open');
	});
	$('.main-section .row').mouseenter(function(){
		$(this).find('.hover-edit').show();
	});
	$('.main-section .row').mouseleave(function(){
		$(this).find('.hover-edit').hide();
	});
	$(window).resize(function(){
		$('.main-aside').height($(window).height()-40);
	})
	$('.media-body textarea').on('input',function(){
		$_ta_len=$(this).val().length;
		$(this).next('p').text('还能输入' + (1000 - $_ta_len) + '个字符').removeClass('hide');
	});
	$('#popup-submit').click(function(){
		$.ajax({
			url:'login',
			type:"post",
			async:true,
			dataType:'json',
			data:$('#login-form').serializeArray(),
			success:function(data){
				if (!data.r) {
					alert('用户名或邮箱不存在，请重新输入！');
					$('#loginname').val('');
					$('#loginpass').val('');
				}else if(!data.passresult){
					alert('密码错误，请重新输入！');
					$('#loginpass').val('');
				}else{
					location.reload();
				}
			}
		});
    });
	$('#reg-submit').click(function(){
		var suc = 0;
		if($(this).prevAll().find('.right-img').length == 4){
			$.ajax({
				url:'reg',
				type:"post",
				async:false, //同步执行 不执行完 不执行下面语句
				dataType:'json',
				data:{
					remail:$('#regemail').val()
				},
				success:function(data){
					if (data.r){
						$.ajax({
							url:'reg',
							type:"post",
							async:true,
							dataType:'json',
							data:$('#reg-form').serializeArray(),
							success:function(data){
								if (data.r) {
									location.reload();
								}
							}
						});
					}else{
					   alert('邮箱已存在，请重新输入！');
					   $('#regemail').val('');
					}
				}
			});
			if(suc == 1){

			}
		}else{
			alert('不满足注册条件，请检查后重试！');
		}
    });
	$('.user-exit-a').click(function (){
		$.ajax({
			url:'logout',
			type:"post",
			async:true,
			dataType:'json',
			data:{logout:'permit',},
			success:function(data){
				if (data.r) location.reload();
			}
		});
    });
	$('#com-btn').click(function (){
		$.ajax({
			url:'comment',
			type:"post",
			async:true,
			dataType:'json',
			data:{
			    comcon:$('#com-txta').val(),
                dataid:''
            },
			success:function(data){
				if (data.r) location.reload();
			}
		});
    });
	$('.del-comment').click(function (){
		var dataid = $(this).attr('data-id');
		if(confirm('确定删除这条评论吗？')){
			if(!$(this).hasClass('del-sec')){
				$.ajax({
					url:'delcom',
					type:"post",
					async:true,
					dataType:'json',
					data:{
						dataid:dataid,
						com:'first'
					},
					success:function(data){
						if (data.r) location.reload();
					}
				});
			}else{
				$.ajax({
					url:'delcom',
					type:"post",
					async:true,
					dataType:'json',
					data:{
						dataid:dataid,
						com:'second'
					},
					success:function(data){
						if (data.r) location.reload();
					}
				});
			}
		}
    });
    $('.icon-huifu').click(function (){
        var $_s = $(this).parent('span').nextAll('.reply');
        if ($_s.hasClass('reply-active')) {
            $_s.removeClass('reply-active').animate({'height': '0px'}, 1000);
        } else {
            $_s.addClass('reply-active').animate({'height': '170px'}, 1000);
        }
    });
    $('.com-btn').click(function (){
        var $_v = $(this).prevAll('textarea').val();
        var dataid = $(this).attr('data-id');
        $.ajax({
			url:'comment',
			type:"post",
			async:true,
			dataType:'json',
			data:{
			    comcon:$_v,
                dataid:dataid
            },
			success:function(data){
				if (data.r) location.reload();
			}
		});
    });
    $('#c-save').click(function (){
        var $_e = $('#c-email').val();
        var $_yp = $('#c-pass').val();
        var $_p = $('#c-pass1').val();
        var $_i = $('#c-intr').val();
        var $_img = $('#c-img').val();
        if($_e){
            if(!(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test($_e))){
                alert('邮箱输入错误，请重新输入！');
            }else if($_e == $('#p-email').text().replace('邮箱： ','')){
                alert('邮箱无变化，请重新输入！');
            }else{
                $.ajax({
                    url:'change',
                    type:"post",
                    async:false,
                    dataType:'json',
                    data:{
                        cemail:$_e
                    },
                    success:function(data){
                        if (data.r){
                            $_e = '1';
                        }else{
                            alert('邮箱已存在，请重新输入！');
                        }
                    }
		        });
            }
        }
        if($_p){
            if(!(/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$/.test($_p))){
                alert('密码必须6位以上，包含数字与字母！');
                $('#c-pass').val('');
                $('#c-pass1').val('');
                $('#c-pass2').val('');
            }else if($_p != $('#c-pass2').val()){
                alert('两次密码不同，请重新输入！');
                $('#c-pass').val('');
                $('#c-pass1').val('');
                $('#c-pass2').val('');
            }else{
                $.ajax({
                    url:'change',
                    type:"post",
                    async:false, //同步执行 不执行完 不执行下面语句
                    dataType:'json',
                    data:{
                        cpass:$_yp
                    },
                    success:function(data){
                        if (data.r){
                           $_p = '1';
                        }else{
                           alert('原密码不正确，请重新输入！');
                           $('#c-pass').val('');
                           $('#c-pass1').val('');
                           $('#c-pass2').val('');
                        }
                    }
		        });
            }
        }
        if($_i){
            if($_i.length>30){
                alert('长度大于30,请重新输入！');
            }else{
                $_i = '1';
            }
        }
        if(($_e == '1') || ($_p == '1') || ($_i == '1') || $_img){
            $('#c-form').submit();
        }
    });
	$('.panel-img').click(function (){
		var dataid = $(this).attr('data-id');
		window.open('/m_'+dataid);
    })
});
