/**
 * 
 */
$(function() {
	$("#executeAll").click(function() {
		if (confirm('你确定要执行测试吗?')) {
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

	$("#execute").click(function() {
		if ($("input[name=serverid]:checked").length == 0) {
			alert("请至少选择一个服务器！");
		} else if ($("input[name=interid]:checked").length == 0) {
			alert("请至少选择一个接口！");
		} else {
			var serverids = [];
			var interids = [];
			$("input[name=serverid]:checked").each(function(i, server) {
				serverids.push($(this).val())
			});
			$("input[name=interid]:checked").each(function(i, inter) {
				interids.push($(inter).val())
			});
			$.ajax({
				cache : false,
				async : true,
				type : "POST",
				url : "/execute.do",
				dataType : "json",
				data : $.param({
					"serverid" : JSON.stringify(serverids),
					"interid" : JSON.stringify(interids)
				}),
				beforeSend : function() {
					$("#execute").attr("src", "/static/images/running.png");
				},
				error : function() {
					$("#execute").attr("src", "/static/images/run.png");
					alert('执行出错');
				},
				success : function(data, textStatus) {
					$("#execute").attr("src", "/static/images/run.png");
					alert('执行成功，请查看测试结果');
				}
			});
		}
	});
});

function addServer(){
	if(document.getElementById("edittext")==null){
		$("#tb-servers").append("<tr><td><input type='checkbox' name='serverid'></td><td><input type='text' id='edittext'></td><td><img src='/static/images/filesave.png' class='img-btn' title='保存' onclick='saveServer()'></td></tr>");
	} else{
		alert("请保存后再次添加！")
	}
}
function saveServer(){
	var value=$("#edittext").val().trim();
	if(value.length>0){
		$.ajax({
			cache : false,
			async : true,
			type : "POST",
			url : "/saveServer.do",
			dataType : "json",
			data : {"name" : value},
			error : function() {
				alert('执行出错');
			},
			success : function(data, textStatus) {
				location.href="/lsinters.do"
			}
		});
	}
}
/**
 * 复选框 全选功能
 * @param obj 当前标签对象
 * @param itemName 需要影响的组件name
 */
function checkAll(obj,itemName) {
	if (obj.checked) {
		$("input[name="+itemName+"]").each(function() {
			this.checked = true;
			$(obj).attr("title", "全不选")
		});
	} else {
		$("input[name="+itemName+"]").each(function() {
			this.checked = false;
			$(obj).attr("title", "全选")
		});
	}
}

function add(tag){
	if(tag=='server'){
		
	}else if(tag='inter'){
		
	}
}

/*function edit(tag,id){
	alert(1);
	if(tag=='server'){
		
	}else if(tag='inter'){
		$.ajax({
			cache : false,
			async : true,
			type : "POST",
			url : "/editinter.do",
			dataType : "json",
			data :{"id":id},
			error : function() {
				alert('编辑失败');
			},
			success : function(data, textStatus) {
				
			}
		});
	}
}*/
/**
 * 删除
 * @param tag
 * @param id
 */
function del(tag,id){
	if(confirm("你确定要删除吗？")){
		$.ajax({
			cache : false,
			async : true,
			type : "POST",
			url : "/delete.do",
			dataType : "json",
			data :{"tag":tag,"id":id},
			error : function() {
				alert('删除失败');
			},
			success : function(data, textStatus) {
				if(data.code==200){
					location.href="/lsinters.do";
				}else{
					alert(data.msg)
				}
			}
		});
	}
}
/**
 * 批量上传
 * @param tag
 * @param itemName
 */
function batchdel(tag,itemName){
	if(confirm("你确定要执行批量删除吗？")){
		var ids=[]
		if(tag=='result'){
			$("input[name="+itemName+"]:checked").each(function(){
				ids.push($(this).val())
			});
			if(ids.length>0){
				$.ajax({
					cache : false,
					async : true,
					type : "POST",
					url : "/batchdel.do",
					dataType : "json",
					data :{"tag":tag,"ids":JSON.stringify(ids)},
					error : function() {
						alert('删除失败');
					},
					success : function(data, textStatus) {
						if(data.code==200){
							location.href="/lsresults.do";
						}else{
							alert(data.msg)
						}
					}
				});
			}else{
				alert("请选择你要删除的条目！")
			}
		}
	}
}

