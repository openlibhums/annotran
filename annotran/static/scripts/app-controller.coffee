
appcontroller =  require('../../../../h/h/static/scripts/app-controller.coffee');

class AppControllerExt extends appcontroller
   constructor: (
     $controller,   $document,   $location,   $rootScope,   $route,   $scope,
     $window,   annotationUI,   auth,   drafts,   features,   groups,
     identity,   session
   ) ->
    super    
    $scope.userList = visible: false

    # Start the user-list flow. This will present the user with the user-list.

    $scope.showUserList = ->
      alert("Running")
      $scope.userList.visible = true
      


module.exports = AppControllerExt

