'use strict';
var persona = require('../../../../../h/h/static/scripts/filter/persona.js');
var events = require('../../../../../h/h/static/scripts/events.js');
var eventsa =  require('../events');

// @ngInject
function Controller($scope, settings, languages, crossframe) {

  this.serviceUrl = settings.serviceUrl;
  $scope.sentenceMode = "on";


  if ($scope.model == null) {
    $scope.model = {};
  }

  $scope.hideUserList = function () {
    $scope.$root.userListvisible = false;
  };

  $scope.setUserForReset = function () {
    this.$root.selectedUser = undefined;
    this.$root.editOnly = false;

    $scope.$root.$broadcast(eventsa.LANGUAGE_FOCUSED, languages.focused().id);

  };

  $scope.setUserForEdit = function () {
    this.$root.selectedUser = "self";
    this.$root.editOnly = true;

    $scope.$root.$broadcast(eventsa.LANGUAGE_FOCUSED, languages.focused().id);

  };

  $scope.setUser = function (id) {
    var selectedUser = "acct:" + id.username + "@" + id.provider;

    if (selectedUser == this.$root.currentUser) {
      this.$root.selectedUser = "self";
      this.$root.editOnly = true;
    } else {
      this.$root.selectedUser = id;
      this.$root.editOnly = false;
    }

    $scope.$root.$broadcast(eventsa.LANGUAGE_FOCUSED, languages.focused().id);

  };

  $scope.toggleSentence = function () {
    if($scope.sentenceMode == "on")
    {
      $scope.sentenceMode = "off";
    } else {
      $scope.sentenceMode = "on";
    }

    crossframe.call("toggleSentenceSelection");
  };

  $scope.userList = function () {
    return $scope.$root.updateUserList()
  };

  // for some reason we have to use an array here as NG repeat won't handle it properly otherwise
  $scope.list_of_users = $scope.$root.list_of_users;
  $scope.$root.updateUserList();
  
}

function userList () {
  return {
    controller: Controller,
    bindToController: true,
    controllerAs: 'vm',
    restrict: 'E',
    scope: {
      auth: '=',
      session: '=',
      onClose: '&',
      showUserList: '='
    },
    templateUrl: 'user_list.html'
  };
  }

module.exports = {
  directive: userList,
  Controller: Controller
};
