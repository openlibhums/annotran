var $ = require('jquery')
annotator = require('annotator');
$ = annotator.$
var substitution = require('./substitution');


var jsonAnnotation = '{ "ranges" : [' +
'{ "start":"//div/p" , "end":"//div/p" },' +
'{ "startOffset":0 , "endOffset":5 }]}';

substitution.Substitution(jsonAnnotation, "this is a substitution text");




