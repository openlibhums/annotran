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

widgetcontroller =  require('../../../../h/h/static/scripts/widget-controller.coffee')


class WidgetControllerExt extends widgetcontroller
  this.$inject = [
    '$scope', 'annotationUI', 'crossframe', 'annotationMapper', 'drafts', 'groups', 'languages'
    'streamer', 'streamFilter', 'store', 'threading'
  ]
  constructor:   (
     $scope,   annotationUI,   crossframe,   annotationMapper,  drafts,    groups, languages,
     streamer,   streamFilter,   store,   threading
  ) ->
    $scope.threadRoot = threading.root
    $scope.sortOptions = ['Newest', 'Oldest', 'Location']

    this.crossframe = crossframe

    @chunkSize = 200
    loaded = []

    _resetAnnotations = ->
      # Unload all the annotations
      annotationMapper.unloadAnnotations(threading.annotationList())
      # Reload all the drafts
      threading.thread(drafts.unsaved())

    _loadAnnotationsFrom = (query, offset, crossframe) =>
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

        loadUsers(results.rows)
        userAnnotations = []

        ##1. show users
        ##2. on user focus event
            ##a) eliminate from userAnnotations annotations that do not belong to the current user
        user = results.rows[0].user #TODO - fill the user with the selected user!
        for annot in results.rows when annot.user == user
          userAnnotations.push annot
        
            ##b) call two lines below only on user focus event

        crossframe.call "passAnnotations", results.rows
        annotationMapper.loadAnnotations(results.rows, results.replies)
    
    loadUsers = (annotations) ->      
      userList = []
      for annot in annotations when annot.group == groups.focused().id and annot.language == languages.focused().id
        userList = new Set()
        userList.add annot.user

    loadAnnotations = (frames) ->
      for f in frames
        if f.uri in loaded
          continue
        loaded.push(f.uri)
        _loadAnnotationsFrom({uri: f.uri}, 0, crossframe)

      if loaded.length > 0
        streamFilter.resetFilter().addClause('/uri', 'one_of', loaded)
        streamer.setConfig('filter', {filter: streamFilter.getFilter()})


    $scope.$on events.GROUP_FOCUSED, ->
      _resetAnnotations(annotationMapper, drafts, threading)
      loaded = []
      loadAnnotations crossframe.frames

    $scope.$on eventsa.LANGUAGE_FOCUSED, ->
      _resetAnnotations(annotationMapper, drafts, threading)
      loaded = []
      loadAnnotations crossframe.frames

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

