'use strict';
var persona = require('../../../../../h/h/static/scripts/filter/persona.js');
var events = require('../../../../../h/h/static/scripts/events.js');
var eventsa =  require('../events');

// @ngInject
function Controller($scope, $window, settings, languages, votes, crossframe) {

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

    if (languages.focused().id == undefined) {
      var message = 'Select language.';
      $window.confirm(message);
    } else {
      $scope.$root.$broadcast(eventsa.LANGUAGE_FOCUSED, languages.focused().id);
    }
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
      $scope.setUserForEdit();
    } else {
      $scope.sentenceMode = "on";
      $scope.setUserForReset();
    }

    crossframe.call("toggleSentenceSelection");
  };

  $scope.vote = function(author) {
    if (author != this.$root.currentUser) {
      $scope.author = author;
    }
  };

  $scope.addVote = function(author, score) {
    $scope.author=author;

    var voteRet = votes.addVote(author.username, languages.focused().id, score);

    // set scope.author to an empty dictionary in order to hide the box once the user has voted.
    $scope.author={};

    return voteRet;
  };

  $scope.showVote = function(author, score) {

    votes.showVote(author, score);

  };

  $scope.voteAuthor = function(user) {
    return function(score) {
      if ($scope.author == undefined ||  user == undefined)
        return false;
      if ($scope.author ==  user)
        return true;
      else
        return false;
    }
  };

  $scope.userList = function () {
    return $scope.$root.updateUserList()
  };

  // for some reason we have to use an array here as NG repeat won't handle it properly otherwise
  $scope.list_of_users = $scope.$root.list_of_users;
  $scope.$root.updateUserList();

}

// @ngInject
function userList (languages) {
  return {
    controller: Controller,
    bindToController: true,
    controllerAs: 'vm',
    restrict: 'E',
    link: function ($scope, elem, attrs) {
      $scope.languages = languages;
    },
    scope: {
      auth: '=',
      session: '=',
      onClose: '&',
      showUserList: '=',
      languages: '&',
    },
    templateUrl: 'user_list.html'
  };
}

module.exports = {
  directive: userList,
  Controller: Controller
};
