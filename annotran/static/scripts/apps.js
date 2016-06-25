'use strict'

// this assumes that h is stored in the same root directory as annotran
require('../../../../h/h/static/scripts/app.coffee');


require('./directive/language-list.js');

var app = angular.module("h");


app.directive('languageList', require('./directive/language-list').directive)

.service('languages', require('./languages'))


app.factory('langListFactory', require('./directive/language-service').factory)


app.controller("languageController", ['$scope', 'langListFactory',
    function ($scope, langListFactory) {
    $scope.languages = langListFactory.getLanguages();
    $scope.language = null;
}]);

