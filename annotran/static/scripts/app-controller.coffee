
appcontroller =  require('../../../../h/h/static/scripts/app-controller.coffee');
persona = require('../../../../h/h/static/scripts/filter/persona.js')

class AppControllerExt extends appcontroller
   constructor: (
     $controller,   $document,   $location,   $rootScope,   $route,   $scope,
     $window,   annotationUI,   auth,   drafts,   features,   groups,
     identity,   session
   ) ->
    super    
    $scope.userList = visible: false
    $scope.$root.list_of_users = []
    $scope.$root.userAnnotations = []

    $scope.$root.updateUserList = ->
      # clear the array
      $scope.$root.list_of_users.length = 0

      if $scope.$root.userAnnotations.length > 0
        for entry in $scope.$root.userAnnotations
          parsed = persona.parseAccountID(entry.user)

          if $scope.$root.list_of_users.indexOf(parsed.username) == -1
            $scope.$root.list_of_users.push parsed.username

      return $scope.$root.list_of_users

module.exports = AppControllerExt

