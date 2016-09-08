
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

var eventsa =  require('./events');


// @ngInject
function votes(settings, session, $rootScope, $http) {

  $rootScope.$on(eventsa.SESSION_RELOADED, function (event, languageName) {
    if (languageName == "") {
      $rootScope.allVotes = {};
      $rootScope.updateUserList();
    }
  });


  function addVote(userId, languageId, score) {

    var pageId = $rootScope.pageid;
    var groupPubid = $rootScope.groupPubid;
    var response = $http({
      method: 'POST',
      url: settings.serviceUrl + 'votes/' + userId + '/' + groupPubid + '/' + languageId + '/' + pageId + '/' + score + '/' + 'addVote',
    });

    session.reload("");

    return response;
   };

  function showVote(author, score) {
    //console.log(session.state.votes);
  };


  return {
    addVote: addVote,
    showVote: showVote,
  };
};

module.exports = votes;