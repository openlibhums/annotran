
appcontroller =  require('../../../../h/h/static/scripts/app-controller.coffee');
persona = require('../../../../h/h/static/scripts/filter/persona.js')

class AppControllerExt extends appcontroller
   constructor: (
     $controller,   $document,   $location,   $rootScope,   $route,   $scope,
     $window,   annotationUI,   auth,   drafts,   features, groups, languages,
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
      # get all users using annot list
      getUsers()

      # clear the array
      $scope.$root.list_of_users.length = 0

      dupeCheck = []

      if $scope.$root.allPageAnnotations.length > 0
        if (session.state.votes != undefined && session.state.votes.length != 0)
          for i in [0 .. (session.state.votes.length-1)]
            if (groups.focused().id == session.state.votes[i].group_id &&
                languages.focused().id == session.state.votes[i].language_id)
              score = session.state.votes[i].avg_score
              author = setUserWithScore(session.state.votes[i].author_id)
              auth_obj = {}
              auth_obj["score"] = score
              auth_obj["author"] = author
              $scope.$root.list_of_users.push auth_obj

        #push unvoted users
        keys = Object.keys($scope.$root.users_no_scores)
        for i in [0 .. (Object.keys($scope.$root.users_no_scores).length-1)]
          auth_obj = {}
          auth_obj["score"] = 0
          auth_obj["author"] = $scope.$root.users_no_scores[keys[i]]
          $scope.$root.list_of_users.push auth_obj

      return $scope.$root.list_of_users

    $scope.$root.users_no_scores = {}
    getUsers = () ->
      for entry in $scope.$root.allPageAnnotations
        parsed = persona.parseAccountID(entry.user)
        if Object.keys($scope.$root.users_no_scores).length != 0 && $scope.$root.users_no_scores[parsed.username] != undefined
          continue
        else
          $scope.$root.users_no_scores[parsed.username] = parsed

    $scope.$root.users_with_scores = {}
    setUserWithScore = (authorusername) ->
      user_info = $scope.$root.users_no_scores[authorusername]
      $scope.$root.users_with_scores[authorusername] = user_info
      delete $scope.$root.users_no_scores[authorusername]
      return user_info

    $scope.$root.allVotes = {}
    getAuthorTotalScore = (authorusername) ->
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