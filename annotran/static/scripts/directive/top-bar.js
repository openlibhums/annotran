'use strict';

module.exports = {
    directive: function () {
      return {
        restrict: 'E',
        priority: 0,
        scope: {
          auth: '=',
          isSidebar: '=',
          onLogin: '&',
          onLogout: '&',
          searchController: '=',
          accountDialog: '=',
          shareDialog: '=',
          sortBy: '=',
          sortOptions: '=',
          userList: '=',
          onChangeSortBy: '&',
          showUserList: '&'
        },
      templateUrl: 'top_bar.html',
      };
    }
};
