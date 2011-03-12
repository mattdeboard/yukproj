google.load("search", "1");
google.load("jquery", "1.5.0");
google.load("jqueryui", "1.8.9");
google.setOnLoadCallback(function() {
	$(function () { 
	    	
	    // Javascript for form submission
	    $("a#submit").live("click", function () {
		$("form").submit();
	    });
	    
	    // Below here is the javascript for the Delete/Are you sure dialogue
	    $("a.confirm#del_conf_false").live("click",function () {
		$("span.hconf").replaceWith(
		    $("<a class='delete' id="+$(this).attr('u')+
		      " href='#'>delete</a>"));
		 return false;
		});
				
	    $("a.confirm#del_conf_true").live("click", function () {
		$("li#"+$(this).attr("u")).hide();			
		$.post("/u:"+$("span.username").text()+"/delete/", 
		       { url_id:$("#del_conf_false").attr("u"), 
			 uname:$("span.username").text()}
		      );
		return false;
	    });
			
	    $("a.delete").live("click", function () {
		var id = $(this).attr("id");
		$(this).replaceWith(confirm_string(id));
		return false;
		});
		
	    function confirm_string(id) {
		var conf = "<span class='hconf' style>Are you sure? <a class='confirm' u='" + id + "' id='del_conf_true' href='#'>yes</a> | <a class='confirm' u='" + id + "' id='del_conf_false' href='#'>no</a></span>";
		return conf;
	    }
	});
});
