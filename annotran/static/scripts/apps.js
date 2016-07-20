
'use strict'

// this assumes that h is stored in the same root directory as annotran
require('../../../../h/h/static/scripts/app.coffee');

require('./directive/language-list.js');
require('./events.js');
var app = angular.module("h");

app.controller('AppController', require('./app-controller'))
    .controller('WidgetController', require('./widget-controller'))
    .directive('languageList', require('./directive/language-list').directive)
    .directive('userList', require('./directive/user-list').directive)
    .directive('annotation', require('./directive/annotation').directive)
    .directive('topBar', require('./directive/top-bar').directive)



.service('languages', require('./languages'))
.service('groups', require('./groups'))
.service('session', require('./session'))

app.factory('langListFactory', require('./directive/language-service').factory)


app.controller("languageController", ['$scope', 'langListFactory',
    function ($scope, langListFactory) {
    $scope.languages = langListFactory.getLanguages();
    $scope.language = null;
}]);


// these decorators override hypothes.is's decorators

app.decorator(
            "annotationDirective",
            function annotationDirectiveDecorator( $delegate ) {
                return( [ $delegate[1] ] );
            }
        );

app.decorator(
            "topBarDirective",
            function topBarDirectiveDecorator( $delegate ) {
                return( [ $delegate[1] ] );
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