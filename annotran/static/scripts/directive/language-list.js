'use strict';

var events = require('../../../../../h/h/static/scripts/events.js');
var eventsa =  require('../events');
var Annotator = require('annotator');
var $ = Annotator.$;

var mouseUpPrevent = true;
var clickPrevent = true;

// @ngInject
function LanguageListController($scope, $window, languages, groups, pages) {
  $scope.addLanguage = function (language) {
    clickPrevent = false;
    mouseUpPrevent = false;

    // this will fire when the user selects the top entry in the list ("Add a new translation")
    if(language == null){ return; }

    if (languages.hasLanguageAlready(language.name) == false) {
      var message = 'Are you sure you want to add new translations for the language "' +
        language.name + '"?';
      if ($window.confirm(message)) {
        languages.addLanguage(language.name);
      }
    } else {
      var message = 'Language "' +
        language.name + '" has already been added.';
      alert(message);
      languages.focusByName(language.name);
    }
    $("#zeroIndex").prop('selected', true);
  };
 
  $scope.focusLanguage = function (languageId) {
    $scope.$root.setMode('view');
    $scope.$root.selectedUser = undefined;
    languages.focus(languageId);
  };


  $scope.showUserList = function () {
    $scope.$root.userListvisible = true;
    $scope.$root.updateUserList(0);
  }

  $scope.handleSubmenuMU = function (event) {
    if (mouseUpPrevent == true) {
      event.stopPropagation();
      event.preventDefault();
    }
    else{
      mouseUpPrevent = true;
    }
  };

  $scope.handleSubmenuClick = function (event) {
    if (clickPrevent == true) {
      event.stopPropagation();
      event.preventDefault();
    }
    else{
      clickPrevent = true;
    }
  };
  
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
