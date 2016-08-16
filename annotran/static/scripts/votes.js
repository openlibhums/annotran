
'use strict';


// @ngInject
function votes(settings, $rootScope, $http) {

    function addVote(userId, languageId, score) {

     var pageId = $rootScope.pageid;
     var response = $http({
       method: 'POST',
       url: settings.serviceUrl + 'votes/' + userId + '/' + languageId + '/' + pageId + '/' + score + '/' + 'addVote',
     });

    //$scope.$root.$broadcast(eventsa.USER_VOTED, languages.focused().id);

     return response;
  };


  return {
    addVote: addVote,
  };
};

module.exports = votes;