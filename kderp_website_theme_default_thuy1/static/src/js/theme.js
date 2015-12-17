$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
});
//Khi click vao thi anh duoc phong to trong Certificate
$('.pop').on('click', function() {
	$('.imagepreview').attr('src', $(this).find('img').attr('src'));
	$('#imagemodal').modal('show');
});
