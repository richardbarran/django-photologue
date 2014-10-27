$(document).ready(function() {
	// Highlight in the navigation bar the active menu item.
	var path = window.location['pathname'];
	if (path == '/') {
		$('ul.navbar-nav li.home').addClass('active');
	} else if (path.substring(0, 19) == '/photologue/gallery') {
		$('ul.navbar-nav li.galleries').addClass('active');
	} else if (path.substring(0, 17) == '/photologue/photo') {
		$('ul.navbar-nav li.photos').addClass('active');
	}
})