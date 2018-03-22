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
					// $("#execute").attr("src", "/static/images/running.png");
					$("#execute").css({
						"background-color" : "red",
						"color" : "white"
					});
					$("#execute").val("执行中");
				},
				error : function() {
					// $("#execute").attr("src", "/static/images/run.png");
					$("#execute").css("background-color", "green");
					$("#execute").val("执行/测试");
					alert('执行出错');
				},
				success : function(data, textStatus) {
					// $("#execute").attr("src", "/static/images/run.png");
					$("#execute").css("background-color", "green");
					$("#execute").val("执行/测试");
					alert('执行成功，请查看测试结果');
				}
			});
		}
	});
});

function addServer() {
	if (document.getElementById("editname") == null) {
		$("#tb-servers")
				.append(
						"<tr><td><input type='checkbox' name='serverid'></td><td><input type='text' id='editname'></td><td><input type='text' id='editcomment' maxlength='20'></td><td><input type='button' value='保存' onclick='saveServer()'></td></tr>");
	} else {
		alert("请保存后再次添加！")
	}
}
function saveServer() {
	var name = $("#editname").val().trim();
	if (name.length > 0) {
		$.ajax({
			cache : false,
			async : true,
			type : "POST",
			url : "/saveServer.do",
			dataType : "json",
			data : {
				"name" : name,
				"comment":$("#editcomment").val().trim()
			},
			error : function() {
				alert('执行出错');
			},
			success : function(data, textStatus) {
				location.href = "/lsinters.do"
			}
		});
	}
}
/**
 * 当失去焦点时校验输入内容是否合法
 * @param obj 当前标签对象 固定传this
 * @param reg 正则表达式格式
 * @param tagid 提示位置的标签id
 */
function tip(obj, reg, tagid){
	if(obj!=null && obj!=undefined && reg!=null && reg!=undefined && tagid!=null && tagid!=undefined){
		if(typeof(reg)=="string"){
			if(reg.toLowerCase()=="json"){
				if(isJSON(obj.value)){
					showSuccessMsg(tagid);
				}else{
					showErrorMsg(tagid);
				}
			}else if(eval(reg).test(obj.value)){
				showSuccessMsg(tagid);
			}else{
				showErrorMsg(tagid);
			}
		}else if(reg instanceof RegExp){
			if(reg.test(obj.value)){
				showSuccessMsg(tagid);
			}else{
				showErrorMsg(tagid);
			}
		}
	}
	
}
function showSuccessMsg(tagid){
	$("#"+tagid).html("验证通过");
	$("#"+tagid).css("color","blue");
}
function showErrorMsg(tagid){
	$("#"+tagid).html("验证失败");
	$("#"+tagid).css("color","red");
}
/**
 * 验证制定输入项是否匹配正则表达式
 * @param inputid 待验证的input标签id
 * @param reg 验证规则
 * @returns {Boolean} 验证通过返回true，否则返回false
 */
function check(inputid, reg){
	var value=$("#"+inputid).val().trim();
	if(typeof(reg)=="string"){
		if(reg.toLowerCase()=="json"){
			if(isJSON(value)){
				return true;
			}
		}else if(eval(reg).test(value)){
			return true;
		}
	}else if(reg instanceof RegExp){
		if(reg.test(value)){
			return true;
		}
	}
	return false;
}
/**
 * 判断是否是json格式的字符串
 * @param value
 * @returns {Boolean}
 */
function isJSON(value){
	if(value!=null && $.trim(value).length>0){
		try {
			$.parseJSON($.trim(value));
			return true;
		} catch (e) {
			console.log(e.message);
		}
	}
	return false;
}
/**
 * 提交保存接口表单
 */
function saveInter(){
	if(check("service",/^\S*$/) && check("path", /^\S*$/)){
		if($("#enc").val()=="json"){
			if(isJSON($("#input").val().trim()) && isJSON($("#output").val().trim())){
				document.inter.submit();
			}else{
				alert("JSON格式不合法！");
			}
		}else{
			document.inter.submit();
		}
	}else{
		alert("服务或者路径不合法！");
	}
	
}
/**
 * 复选框 全选功能
 * 
 * @param obj
 *            当前标签对象
 * @param itemName
 *            需要影响的组件name
 */
function checkAll(obj, itemName) {
	if (obj.checked) {
		$("input[name=" + itemName + "]").each(function() {
			this.checked = true;
			$(obj).attr("title", "全不选")
		});
	} else {
		$("input[name=" + itemName + "]").each(function() {
			this.checked = false;
			$(obj).attr("title", "全选")
		});
	}
}

function add(tag) {
	if (tag == 'server') {

	} else if (tag = 'inter') {

	}
}

/*
 * function edit(tag,id){ alert(1); if(tag=='server'){
 * 
 * }else if(tag='inter'){ $.ajax({ cache : false, async : true, type : "POST",
 * url : "/editinter.do", dataType : "json", data :{"id":id}, error : function() {
 * alert('编辑失败'); }, success : function(data, textStatus) {
 *  } }); } }
 */
/**
 * 单个删除
 * 
 * @param tag
 * @param id
 */
function del(tag, id) {
	if (confirm("你确定要删除吗？")) {
		$.ajax({
			cache : false,
			async : true,
			type : "POST",
			url : "/delete.do",
			dataType : "json",
			data : {
				"tag" : tag,
				"id" : id
			},
			error : function() {
				alert('删除失败');
			},
			success : function(data, textStatus) {
				if (data.code == 200) {
					location.href = "/lsinters.do";
				} else {
					alert(data.msg)
				}
			}
		});
	}
}
/**
 * 批量删除
 * 
 * @param tag
 * @param itemName
 */
function batchdel(tag, itemName) {
	var ids = []
	if (tag == 'result') {
		$("input[name=" + itemName + "]:checked").each(function() {
			ids.push($(this).val())
		});
		if (ids.length > 0) {
			if (confirm("你确定要执行批量删除吗？")) {
				$.ajax({
					cache : false,
					async : true,
					type : "POST",
					url : "/batchdel.do",
					dataType : "json",
					data : {
						"tag" : tag,
						"ids" : JSON.stringify(ids)
					},
					error : function() {
						alert('删除失败');
					},
					success : function(data, textStatus) {
						if (data.code == 200) {
							location.href = "/lsresults.do";
						} else {
							alert(data.msg)
						}
					}
				});
			}
		} else {
			alert("请选择你要删除的条目！")
		}
	}
}
