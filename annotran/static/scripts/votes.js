
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
      $rootScope.updateUserList(0);
    }
  });


  function addVote(username, languageId, score) {

    var pageUri = $rootScope.pageUri;
    var groupPubid = $rootScope.groupPubid;
    var response = $http({
      method: 'POST',
      url: settings.serviceUrl + 'votes/' + username + '/' + groupPubid + '/' + languageId + '/' + pageUri + '/' + score + '/' + 'addVote',
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