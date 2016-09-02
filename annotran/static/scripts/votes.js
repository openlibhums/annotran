
/**
 * @ngdoc service
 * @name  languages
 *
 * @description Provides access to the list of languages for available translations.
 *
 *              The list of languages is initialized from the session state
 *              and can then later be updated using the add() method.
 */
'use strict';


// @ngInject
function votes(settings, session, $rootScope, $http) {


  function addVote(userId, languageId, score) {

    var pageId = $rootScope.pageid;
    var groupPubid = $rootScope.groupPubid;
    var response = $http({
      method: 'POST',
      url: settings.serviceUrl + 'votes/' + userId + '/' + groupPubid + '/' + languageId + '/' + pageId + '/' + score + '/' + 'addVote',
    });

    //$scope.$root.$broadcast(eventsa.USER_VOTED, languages.focused().id);

    return response;
   };

  function showVotes() {
    console.log(session.state.votes);
  }


  return {
    addVote: addVote,
    showVotes: showVotes,
  };
};

module.exports = votes;