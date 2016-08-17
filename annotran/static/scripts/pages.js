'use strict';


// this assumes that h is stored in the same root directory as annotran
var events = require('../../../../h/h/static/scripts/events.js');
var eventsa =  require('./events');

// @ngInject
function pages(settings, session, $rootScope, $http) {

    function addPage(languageName) {
        var response = $http({
            method: 'POST',
            url: settings.serviceUrl + 'pages/' + languageName + '/' +  $rootScope.pageid  + '/' + $rootScope.groupPubid + '/addPage',
        });
        return response;
    };

    $rootScope.$on(eventsa.LANGUAGE_ADDED, function (event, languageName) {
        addPage(languageName);
        session.reload(languageName);
    });

  return {
    addPage: addPage,
  };
};

module.exports = pages;