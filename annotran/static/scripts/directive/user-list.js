'use strict';

// @ngInject
function Controller($scope) {
  
}

module.exports = {
  directive: function () {
    return {
      restrict: 'E',
      scope: {
        onClose: '&',
      },
      templateUrl: 'user_list.html',
    };
  },
  Controller: Controller,
};
