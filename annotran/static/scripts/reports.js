
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
function reports(settings, session, $rootScope, $http, $window) {


    function addReport(userId, languageId) {

        var pageId = $rootScope.pageUri;
        var groupPubid = $rootScope.groupPubid;

        var response = $http({
            method: 'POST',
            url: settings.serviceUrl + '/reports/' + userId + '/' + groupPubid + '/' + languageId + '/' + pageId + '/' + 'addReport'
        }).then(function successCallback(response) {
            var message = 'You reported ' +
                userId + '\'s translations as abusive.';
            alert(message);
        }, function errorCallback(response) {
            var message = 'You already reported this ' +
                userId + '\'s translations as abusive.';
            alert(message);
        });

        session.reload("");

        return response;
    }


    return {
        addReport: addReport
    };
}

module.exports = reports;