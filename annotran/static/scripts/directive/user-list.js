'use strict';

// @ngInject
function Controller($scope, flash, session, formRespond, settings) {

  this.serviceUrl = settings.serviceUrl;

  if ($scope.model == null) {
    $scope.model = {};
  }

  $scope.hideUserList = function () {
    $scope.$parent.userList.visible = false;
  }

  $scope.setUser = function (id) {
    this.$root.selectedUser = id;
  }
  
}

module.exports = {
  directive: function () {
    return {
      bindToController: true,
      controller: Controller,
      controllerAs: 'userListController',
      restrict: 'E',
      scope: {
        auth: '=',
        onClose: '&',
        showUserList: '='
      },
      templateUrl: 'user_list.html',
    };
  },
  Controller: Controller,
};
