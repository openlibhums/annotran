var $ = require('jquery')
annotator = require('annotator');
$ = annotator.$
var substitution1 = require('./substitution/SubstituteAnnotation.js');
var substitution2 = require('./substitution/substitution');
var cycle = require('../libs/cycle');


var tags = require('../libs/plugins/tags.coffee');

var css = require('../css/annotran.css');

OpenAnnotate = ("OpenAnnotate" in window) ? OpenAnnotate : {}

OpenAnnotate.Annotator = function (element) {
    var $ = jQuery, self = this

    this.annotator = $(element).annotator().data('annotator')
    this.currentUser = null

    this.options = {
        user: {}

    }

    $(element).annotator().annotator('addPlugin', 'Substitutions', 'bbk:english');
    $(element).annotator().annotator('addPlugin', 'Tags');

    return this
}








