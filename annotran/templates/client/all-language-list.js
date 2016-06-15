'use strict';

//TODO - resolve this path
var events = require('/home/marija/h/h/static/scripts/events.js');

// @ngInject
function AllLanguageListController($scope, $window, languages) {
  
}

/**
 * @ngdoc directive
 * @name allLanguageList
 * @restrict AE
 * @description Displays a list of available languages
 */
// @ngInject
function allLanguageList( $window, languages, settings) {
  return {
    controller: AllLanguageListController,
    restrict: 'E',
    scope: {
      auth: '='
    },
    templateUrl: 'all_language_list.html'
  };
};

module.exports = {
  directive: allLanguageList,
  Controller: AllLanguageListController
};