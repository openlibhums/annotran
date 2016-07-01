
appcontroller =  require('../../../../../h/h/static/scripts/app-controller.coffee');

class AppControllerExt extends appcontroller
   constructor: (
     $controller,   $document,   $location,   $rootScope,   $route,   $scope,
     $window,   annotationUI,   auth,   drafts,   features,   groups,
     identity,   session
   ) ->
    super    
    $scope.userList = visible: false


module.exports = AppControllerExt

