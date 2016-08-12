'use strict';


// this assumes that h is stored in the same root directory as annotran
var events = require('../../../../h/h/static/scripts/events.js');
var eventsa =  require('./events');

// @ngInject
function pages(settings, session, $rootScope, $http) {

    var pageId = $rootScope.pageid;
    pageId = decodeURIComponent(pageId);
    pageId = encodeURIComponent(encodeURIComponent(getParameterByName("url", pageId)));

    function getParameterByName(name, url) {
        if (!url) url = pageid;
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return results[2];
        //return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    function addPage(languageName) {
        var response = $http({
            method: 'POST',
            url: settings.serviceUrl + 'pages/' + languageName + '/' + pageId + '/' + $rootScope.groupPubid + '/addPage',
        });
        return response;
    };

    $rootScope.$on(eventsa.LANGUAGE_ADDED, function (event, languageName) {
        addPage(languageName);
    });

  return {
    addPage: addPage,
  };
};

module.exports = pages;