'use strict';

var events = require('../../../../../h/h/static/scripts/events.js');

// @ngInject
function LanguageListController($scope, $window, languages) {
  $scope.addLanguage = function (language) {
    var message = 'Are you sure you want to add new translations for the language "' +
      language.name + '"?';
    if ($window.confirm(message)) {
      languages.addLanguage(language.name);
    }
  }
 
  $scope.focusLanguage = function (languageId) {
    languages.focus(languageId);
  }

  $scope.showUserList = function () {
    $scope.$parent.userList.visible = true;
    $scope.$root.updateUserList();
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
    },
    restrict: 'E',
    scope: {
      auth: '=',
      userList: '=',
      showUserList: '='
    },
    templateUrl: 'language_list.html'
  };
};

module.exports = {
  directive: languageList,
  Controller: LanguageListController
};
