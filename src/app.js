var $ = require('jquery')
annotator = require('annotator');
$ = annotator.$

//todo: write annotator extension code here

var findandreplacedomtext = require('findandreplacedomtext');

findandreplacedomtext(document.getElementsByClassName('test'), {
  find: 'text',
  replace: function(portion, match) {
    return '[[' + portion.index + ']]';
  }
});
