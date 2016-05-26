'use strict';

//TODO - resolve this path
var events = require('/home/marija/h/h/static/scripts/events.js');

// @ngInject
function LanguageListController($scope, $window) {

}

/**
 * @ngdoc directive
 * @name languageList
 * @restrict AE
 * @description Displays a list of availabel languages
 */
// @ngInject
function languageList( $window, groups, settings) {
  return {
    controller: LanguageListController,
    link: function ($scope, elem, attrs) {
    },
    restrict: 'E',
    scope: {
      auth: '='
    },
    templateUrl: 'language_list.html'
  };
};

module.exports = {
  directive: languageList,
  Controller: LanguageListController
};


