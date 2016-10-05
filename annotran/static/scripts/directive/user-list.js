'use strict';
var persona = require('../../../../../h/h/static/scripts/filter/persona.js');
var events = require('../../../../../h/h/static/scripts/events.js');
var eventsa =  require('../events');

// @ngInject
function Controller($scope, $window, session, settings, languages, votes, reports, crossframe) {

  this.serviceUrl = settings.serviceUrl;
  $scope.sentenceMode = "on";
  $scope.mode = "view";

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

  $scope.setMode = function(modeValue) {
    $scope.mode = modeValue;
    if ($scope.mode == 'view') {
      if ($scope.sentenceMode == "off") {
        $scope.toggleSentence();
      } else {
         $scope.setUser('self');
      }
    }
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

  $scope.enableSentence = function () {
    $scope.sentenceMode = "on";
    $scope.setUserForReset();
    this.$root.sentencebysentence = $scope.sentenceMode;

    crossframe.call("sentenceSelectionOn");
  };

  $scope.disableSentence = function () {
    $scope.sentenceMode = "off";
    this.$root.sentencebysentence = $scope.sentenceMode;

    crossframe.call("sentenceSelectionOff");
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

  $scope.addReport = function(author) {
    $scope.author=author;

    var message = 'Are you sure you want to report ' + author.username  + '\'s translations as abusive?';
      if ($window.confirm(message)) {
        var reportRet = reports.addReport(author.username, languages.focused().id);
        // set scope.author to an empty dictionary in order to hide the box once the user has voted.
        $scope.author={};
        return reportRet;
      }
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

  $scope.reverseUserList = function(direction) {
    $scope.$root.direction = direction;
    $scope.$root.updateUserList($scope.$root.direction);
  };

  $scope.userList = function () {
    return $scope.$root.updateUserList(0)
  };

  // for some reason we have to use an array here as NG repeat won't handle it properly otherwise
  $scope.list_of_users = $scope.$root.list_of_users;
  $scope.$root.updateUserList(0);

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
