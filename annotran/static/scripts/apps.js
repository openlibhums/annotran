'use strict'

//TODO - resolve this path

require('/home/marija/h/h/static/scripts/app.coffee');


require('./directive/language-list.js');

var app = angular.module("h");


app.directive('languageList', require('./directive/language-list').directive)


