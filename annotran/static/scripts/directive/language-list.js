'use strict';

var events = require('../../../../../h/h/static/scripts/events.js');
var eventsa =  require('../events');
var Annotator = require('annotator');
var $ = Annotator.$;

// @ngInject
function LanguageListController($scope, $window, languages, groups, pages) {
  $scope.addLanguage = function (language) {

    // this will fire when the user selects the top entry in the list ("Add a new translation")
    if(language == null){ return; }

    if (languages.hasLanguageAlready(language.name) == false)
    {
      var message = 'Are you sure you want to add new translations for the language "' +
        language.name + '"?';
      if ($window.confirm(message)) {
        languages.addLanguage(language.name);
        $scope.$root.$broadcast(eventsa.LANGUAGE_ADDED, language.name);
      } else {
        $("#zeroIndex").prop('selected', 'selected');
      }
    } else {
      $scope.$root.$broadcast(eventsa.LANGUAGE_ADDED, language.name);
    }
  };
 
  $scope.focusLanguage = function (languageId) {
    $scope.$root.selectedUser = undefined;
    languages.focus(languageId);
  };


  $scope.showUserList = function () {
    $scope.$root.userListvisible = true;
    $scope.$root.updateUserList(0);
  }
  
}

/**
 * @ngdoc directive
 * @name languageList
 * @restrict AE
 * @description Displays a list of available languages
 */
// @ngInject
function languageList($window, languages, settings) {
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
