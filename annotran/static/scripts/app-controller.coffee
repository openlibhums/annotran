
appcontroller =  require('../../../../h/h/static/scripts/app-controller.coffee');
persona = require('../../../../h/h/static/scripts/filter/persona.js')

class AppControllerExt extends appcontroller
   constructor: (
     $controller,   $document,   $location,   $rootScope,   $route,   $scope,
     $window,   annotationUI,   auth,   drafts,   features,   groups,
     identity,   session
   ) ->
    super
    $scope.$root.userListvisible = true
    $scope.$root.editOnly = false
    $scope.$root.list_of_users = []
    $scope.$root.userAnnotations = []
    $scope.$root.allPageAnnotations = []
    $scope.$root.pageid = window.location.href
    $scope.$root.pageid = decodeURIComponent($scope.$root.pageid);
    $scope.$root.pageid = encodeURIComponent(encodeURIComponent(getParameterByName("url", $scope.$root.pageid)));

    $scope.$root.updateUserList = ->
      # clear the array
      $scope.$root.list_of_users.length = 0

      dupeCheck = []

      if $scope.$root.allPageAnnotations.length > 0
        for entry in $scope.$root.allPageAnnotations
          parsed = persona.parseAccountID(entry.user)

          if dupeCheck.indexOf(entry.user) == -1
            $scope.$root.list_of_users.push parsed
            dupeCheck.push entry.user

      return $scope.$root.list_of_users

    `
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
    `

module.exports = AppControllerExt

