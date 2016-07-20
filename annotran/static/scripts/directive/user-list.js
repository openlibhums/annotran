'use strict';

// @ngInject
function Controller($scope, flash, session, formRespond, settings) {

  this.serviceUrl = settings.serviceUrl;

  if ($scope.model == null) {
    $scope.model = {};
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
        onClose: '&',
        showUserList: '='
      },
      templateUrl: 'user_list.html',
    };
  },
  Controller: Controller,
};
