//An hien menu trai trong cac trang Project
if( $("#xs-check").is(":visible") )
    $("#kdvn-collapse").removeClass("in");
    
if( $("#xs-check").is(":visible") )
    $("#kdvn-collapse-comp").removeClass("in");

//Cho slice trong trang Project
jQuery(function() {
	jQuery('#allinone_carousel_charming').allinone_carousel({
		skin: 'charming',
		width: 850,
		height: 454,
		responsive:true,
		autoPlay: 3,
		resizeImages:true,
		autoHideBottomNav:false,
		showElementTitle:false,
		verticalAdjustment:50,
		showPreviewThumbs:false,
		//easing:'easeOutBounce',
		numberOfVisibleItems:3,
		nextPrevMarginTop:23,
		playMovieMarginTop:0,
		bottomNavMarginBottom:-10
	});		
});