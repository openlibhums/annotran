
/**
 * @ngdoc service
 * @name  pages
 *
 * @description Adds a page for which at least one language has been added previously.
 *
 */
'use strict';

var eventsa =  require('./events');

// @ngInject
function pages(settings, session, $rootScope, $http, translations) {

    function addPage(languageName) {
        var response = $http({
            method: 'POST',
            url: settings.serviceUrl + 'pages/' + languageName + '/' +  $rootScope.pageUri  + '/' + $rootScope.groupPubid + '/addPage',
        }).then(function successCallback(response) {
            $rootScope.$broadcast(eventsa.PAGE_ADDED, languageName);
        });;
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