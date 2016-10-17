###

Copyright (c) 2013-2014 Hypothes.is Project and contributors

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
###


###
 * This module extends the h's widget-controller.coffee
###
angular = require('angular')

eventsa = require('./events')
events = require('../../../../h/h/static/scripts/events.js')

substitution = require('./annotator/plugin/substitution')
sidebar = require('./annotator/sidebar.coffee')

widgetcontroller =  require('../../../../h/h/static/scripts/widget-controller.coffee')


class WidgetControllerExt extends widgetcontroller
  this.$inject = [
    '$scope', 'annotationUI', 'crossframe', 'annotationMapper', 'drafts', 'groups', 'languages', 'session',
    'streamer', 'streamFilter', 'store', 'threading', '$http', 'settings'
  ]
  constructor:   (
     $scope,   annotationUI,  crossframe,   annotationMapper,  drafts, groups, languages, session,
     streamer,   streamFilter,   store,   threading, $http, settings
  ) ->
    $scope.threadRoot = threading.root
    $scope.sortOptions = ['Newest', 'Oldest', 'Location']
    $scope.$root.currentUser = session.state.userid
    $scope.session = session

    # this fires on first page load and is designed to catch instances where the user has been logged out
    # sadly, we can't use a hook to on USER_CHANGED here since the session is reloaded before angular is fully up
    # and running
    if $scope.$root.currentUser == null
        groups.focus("__world__")

    this.crossframe = crossframe

    @chunkSize = 200
    loaded = []

    _resetAnnotations = ->
      # Unload all the annotations
      annotationMapper.unloadAnnotations(threading.annotationList())
      # Reload all the drafts
      threading.thread(drafts.unsaved())

    _loadAnnotationsFrom = (query, offset, crossframe) =>
      if languages.focused() == undefined
        return

      queryCore =
        limit: @chunkSize
        offset: offset
        sort: 'created'
        order: 'asc'
        group: groups.focused().id
        language: languages.focused().id
      q = angular.extend(queryCore, query)
      q._separate_replies = true

      store.SearchResource.get q, (results) ->
        total = results.total
        offset += results.rows.length
        if offset < total
          _loadAnnotationsFrom query, offset, crossframe

        userList = loadUsers(results.rows)

        # note: selectedUser is set in user-list.js directive
        if $scope.$root == undefined or $scope.$root == null or $scope.$root.selectedUser == undefined
          selectedUser = undefined
        else
          selectedUser = $scope.$root.selectedUser

        if selectedUser == "self"
          selectedUser = $scope.$root.currentUser
        else if selectedUser != undefined
          selectedUser = "acct:" + selectedUser.username + "@" + selectedUser.provider

        userAnnotations = []
        allPageAnnotations = []

        if selectedUser != undefined
          for annot in results.rows when annot.user == selectedUser
            userAnnotations.push annot
        else
          userAnnotations = results.rows

        allPageAnnotations = results.rows

        if $scope.$root != undefined and $scope.$root != null
          $scope.$root.userAnnotations = userAnnotations
          $scope.$root.allPageAnnotations = allPageAnnotations
          $scope.$root.updateUserList(0)

        crossframe.call "resetDOM"

        if $scope.$root != null and $scope.$root.mode == "view"
          crossframe.call "hideAdder"

        if selectedUser != undefined
          if !$scope.$root.editOnly
            crossframe.call "stashAnnotations", []
            $scope.$root.cleanDOM = false
            crossframe.call "passAnnotations", userAnnotations
          else
            crossframe.call "stashAnnotations", userAnnotations
            if $scope.$root != undefined and $scope.$root != null
              $scope.$root.cleanDOM = true
            annotationMapper.loadAnnotations(userAnnotations, null)


    loadUsers = (annotations) ->      
      userList = []

      if groups.focused() == undefined or languages.focused() == undefined
        return userList

      for annot in annotations when annot.group == groups.focused().id and annot.language == languages.focused().id
        userList = new Set()
        userList.add annot.user

      return userList

    loadAnnotations = (frames) ->
      for f in frames
        if f.uri in loaded
          continue
        loaded.push(f.uri)
        _loadAnnotationsFrom({uri: f.uri}, 0, crossframe)

      if loaded.length > 0
        streamFilter.resetFilter().addClause('/uri', 'one_of', loaded)
        streamer.setConfig('filter', {filter: streamFilter.getFilter()})

    $scope.$root.addAnnotation = (annot) ->

      $scope.$root.allPageAnnotations.push annot

      crossframe.call("pushAnnotation", annot)

      # now update the interface
      $scope.$root.updateUserList($scope.$root.direction)

    $scope.$on events.USER_CHANGED, ->
      $scope.$root.selectedUser = undefined
      _resetAnnotations(annotationMapper, drafts, threading)
      loaded = []
      loadAnnotations crossframe.frames
      if $scope.session.state.groups.length == 1
        # move focus to world when the user can only see the public group
        groups.focus("__world__")

    $scope.$on events.GROUP_FOCUSED, ->
      $scope.$root.selectedUser = undefined
      _resetAnnotations(annotationMapper, drafts, threading)
      loaded = []
      loadAnnotations crossframe.frames

    $scope.$on eventsa.LANGUAGE_FOCUSED, ->
      _resetAnnotations(annotationMapper, drafts, threading)
      loaded = []
      loadAnnotations crossframe.frames

    $scope.$on eventsa.ROOTSCOPE_LISTS_UPDATED, (event, args) ->
      userId = session.state.userid
      i = 0
      lastAnnotationDeleted = true
      allAnnotations = $scope.$root.allPageAnnotations.length

      while i < allAnnotations
        if userId == $scope.$root.allPageAnnotations[i].user
          lastAnnotationDeleted = false;
          break;
        i++

      if lastAnnotationDeleted
        deleteAuthorVotes userId

      return true

    deleteAuthorVotes = (authorId) ->
      pageUri = $scope.$root.pageUri
      response = $http({
       method: 'POST',
       url: settings.serviceUrl + 'votes/' + groups.focused().id + '/' + languages.focused().id + '/' + pageUri + '/' + 'deleteVote',
      })
      return response



    $scope.$on eventsa.USER_DELETED_ANNOTATION, (event, deleted) ->
      array = (annot for annot in $scope.$root.userAnnotations when annot.id != deleted.id)
      $scope.$root.userAnnotations = array

      crossframe.call("updateAnnotationList", array)

      array = (annot for annot in $scope.$root.allPageAnnotations when annot.id != deleted.id)
      $scope.$root.allPageAnnotations = array

      # now update the interface
      $scope.$root.updateUserList($scope.$root.direction)

      # now fire an event that can be hooked since we've updated the lists in the background
      $scope.$broadcast(eventsa.ROOTSCOPE_LISTS_UPDATED, $scope.$root.allPageAnnotations);

      return true

    $scope.$watchCollection (-> crossframe.frames), loadAnnotations

    $scope.focus = (annotation) ->
      if angular.isObject annotation
        highlights = [annotation.$$tag]
      else
        highlights = []
      crossframe.call('focusAnnotations', highlights)

    $scope.scrollTo = (annotation) ->
      if angular.isObject annotation
        crossframe.call('scrollToAnnotation', annotation.$$tag)

    $scope.hasFocus = (annotation) ->
      !!($scope.focusedAnnotations ? {})[annotation?.$$tag]


module.exports = WidgetControllerExt

