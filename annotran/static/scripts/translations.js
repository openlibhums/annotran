
/**
 * @ngdoc service
 * @name  translations
 *
 * @description Adds a unique translation record for a page and selected group and language.
 *
 */
'use strict';

var eventsa =  require('./events');

// @ngInject
function translations(settings, session, $rootScope, $http) {

    function addTranslation(languageName) {
        var response = $http({
            method: 'POST',
            url: settings.serviceUrl + 'translations/' + languageName + '/' + $rootScope.groupPubid + '/' + $rootScope.pageUri + '/addTranslation',
        });
        return response;
    };

    $rootScope.$on(eventsa.PAGE_ADDED, function (event, languageName) {
        addTranslation(languageName);
        session.reload(languageName);
    });

  return {
    addTranslation: addTranslation,
  };
};

module.exports = translations;