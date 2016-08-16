
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

module.exports = AppControllerExt

