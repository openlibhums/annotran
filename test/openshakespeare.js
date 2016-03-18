OpenShakespeare = ("OpenShakespeare" in window) ? OpenShakespeare : {}

OpenShakespeare.Annotator = function (element) {
    var $ = jQuery, self = this

    this.annotator = $(element).annotator().data('annotator')
    this.currentUser = null

    this.options = {
        user: {}


    }
/*
    jQuery(function ($) {
        $('#text-to-annotate').annotator();
    });


    // Setup the annotator on the page.
    var content = $('#text-to-annotate').annotator();
*/
    $(element).annotator().annotator('addPlugin', 'Substitutions', 'bbk:english');
    $(element).annotator().annotator('addPlugin', 'Tags');



    jQuery(function ($) {
       $(element).annotator()
                .annotator('setupPlugins');
    });


    return this
}
