
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
          author = persona.parseAccountID(entry.user)
          parsed = {}
          parsed["author"] = author
          parsed["score"] = getAuthorTotalScore(author)
          if dupeCheck.indexOf(entry.user) == -1
            $scope.$root.list_of_users.push parsed
            dupeCheck.push entry.user

      return $scope.$root.list_of_users

    $scope.$root.allVotes = {}
    getAuthorTotalScore = (author) ->
      author_score = 0.0
      if (session.state.votes != undefined && session.state.votes.length != 0)
        if Object.keys($scope.$root.allVotes).length == 0
          for i in [0 .. (session.state.votes.length-1)]
            $scope.$root.allVotes[session.state.votes[i].author_id] = session.state.votes[i]
            if session.state.votes[i].author_id == author.username
              author_score = session.state.votes[i].avg_score
        else
          auth_obj = $scope.$root.allVotes[author.username]
          if (auth_obj)
            author_score = auth_obj.avg_score
      return author_score

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

