'use strict';

//TODO - resolve this path
var events = require('/home/marija/h/h/static/scripts/events.js');

// @ngInject
function LanguageListController($scope, $window, languages) {
  $scope.leaveLanguage = function (languageId) {
    var languageName = languages.get(languageId).name;
    var message = 'Are you sure you want to change the language "' +
      languageName + '"?';
    if ($window.confirm(message)) {
      languages.leave(languageId);
    }
  }

  $scope.focusLanguage = function (languageId) {
    languages.focus(languageId);
  }
}

/**
 * @ngdoc directive
 * @name languageList
 * @restrict AE
 * @description Displays a list of available languages
 */
// @ngInject
function languageList( $window, languages, settings) {
  return {
    controller: LanguageListController,
    link: function ($scope, elem, attrs) {
      $scope.languages = languages;

      $scope.createNewLanguage = function() {
        $window.open(settings.serviceUrl + 'languages/new', '_blank');
      }
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