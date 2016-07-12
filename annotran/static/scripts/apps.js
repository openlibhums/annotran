
'use strict'

// this assumes that h is stored in the same root directory as annotran
require('../../../../h/h/static/scripts/app.coffee');

var AnnotationController = require('./directive/annotation.js');
require('./directive/language-list.js');

var app = angular.module("h");


app.controller('AppController', require('./app-controller'))
    .directive('languageList', require('./directive/language-list').directive)
    .directive('userList', require('./directive/user-list').directive)


.service('languages', require('./languages'))
.service('groups', require('./groups'))


app.factory('langListFactory', require('./directive/language-service').factory)


app.controller("languageController", ['$scope', 'langListFactory',
    function ($scope, langListFactory) {
    $scope.languages = langListFactory.getLanguages();
    $scope.language = null;
}]);

//this is to override the annotation directive from h
//the directive overriding code is in ../scripts/directive/annotation.js
//this approach detects if there are multiple directives loaded and selects the desired one!
app.decorator(
            "annotationDirective",
            function annotationDirectiveDecorator( $delegate ) {
                console.log( "There are %s matching directives.", $delegate.length );
                return( [ $delegate[0] ] );
            }
        );

/*
app.controller('AppController', ['$scope', '$controller', function ( $controller, $document, $location, $rootScope, $route, $scope,
     $window, annotationUI, auth, drafts, features, groups, identity, session) {
    // Initialize the super class and extend it.
    angular.extend(this, $controller('AppController', { $controller: $controller, $document: $document, $location: $location, $rootScope: $rootScope, $route: $route, $scope: $scope,
        $window: $window, annotationUI: annotationUI, auth: auth, drafts: drafts,features: features, groups: groups,
        identity: identity, session: session}));
    console.log($scope.shareDialog);
}]);
*/