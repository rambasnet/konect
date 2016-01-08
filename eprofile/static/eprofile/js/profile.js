


// Javascript to enable link to tab
$(document).ready(function () {

    var hash = document.location.hash;
    if (hash) {
        $('nav-tabs a[href=#' + hash +']').tab('show');
    }
    // console.log(hash);
     //console.log(prefix);
// Change hash for page-reload
    $('.nav-tabs a').on('shown.bs.tab', function (e) {
        window.location.hash = e.target.hash;
    });
});
