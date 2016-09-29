/**
 * 
 */
$(function(){
	$("#executeAll").click(function(){
		if(confirm('你确定要执行测试吗?')){
			$.ajax({
				cache : false,
				async : true,
				url : "/executeAll.do",
				error : function() {
					alert('执行出错');
				},
				success : function(data, textStatus) {
					alert('执行成功，请查看测试结果');
				}
			});
		}
	});
	
	$("#execute").click(function(){
		if($("input[name=serverid]:checked").length==0){
			alert("请至少选择一个服务器！");
		}else if($("input[name=interid]:checked").length==0){
			alert("请至少选择一个接口！");
		}else{
			var serverids=[];
			var interids=[];
			$("input[name=serverid]:checked").each(function(i,server){
				serverids.push($(this).val())
			});
			$("input[name=interid]:checked").each(function(i,inter){
				interids.push($(inter).val())
			});
			$.ajax({
				cache : false,
				async : true,
				type:"POST",
				url : "/execute.do",
				dataType:"json",
				data:$.param({"serverid":JSON.stringify(serverids),"interid":JSON.stringify(interids)}),
				beforeSend:function() {
					$("#execute").attr("src","/static/images/running.png");
				},
				error:function() {
					$("#execute").attr("src","/static/images/run.png");
					alert('执行出错');
				},
				success : function(data, textStatus) {
					$("#execute").attr("src","/static/images/run.png");
					alert('执行成功，请查看测试结果');
				}
			});
		}
	});
	
	$("#selectserver").click(function(){
		if(this.checked){
			$("input[name=serverid]").each(function(){
				this.checked=true;
				$("#selectserver").attr("title","全不选")
			});
		}else{
			$("input[name=serverid]").each(function(){
				this.checked=false;
				$("#selectserver").attr("title","全选")
			});
		}
	});
	
	$("#selectinter").click(function(){
		if(this.checked){
			$("input[name=interid]").each(function(){
				this.checked=true;
				$("#selectinter").attr("title","全不选")
			});
		}else{
			$("input[name=interid]").each(function(){
				this.checked=false;
				$("#selectinter").attr("title","全选")
			});
		}
	});
	
	$("#selectall").click(function(){
		if(this.checked){
			$("input[name=item]").each(function(){
				this.checked=true;
				$("#selectall").attr("title","全不选")
			});
		}else{
			$("input[name=item]").each(function(){
				this.checked=false;
				$("#selectall").attr("title","全选")
			});
		}
	});
	
});