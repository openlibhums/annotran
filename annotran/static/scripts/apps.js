'use strict'

//TODO - resolve this path

require('/home/marija/h/h/static/scripts/app.coffee');


require('./directive/language-list.js');

var app = angular.module("h");


app.directive('languageList', require('./directive/language-list').directive)
    .directive('allLanguageList', require('./directive/all-language-list').directive)

.service('languages', require('./languages'))


app.factory('langListFactory', require('./directive/language-service').factory)


app.controller("languageController", ['$scope', 'langListFactory',
    function ($scope, langListFactory) {
    $scope.languages = langListFactory.getLanguages();
    $scope.language = null;
}]);

