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

This is the override of the directive from h - for the purpose of "via annotran" link usage.
###



###*
# @ngdoc directive
# @name share-dialog
# @restrict A
# @description This dialog generates a via link to the page h is currently
# loaded on.
###
module.exports = ['crossframe', (crossframe) ->
  link: (scope, elem, attrs, ctrl) ->
    scope.viaPageLink = ''

    # Watch scope.shareDialog.visible: when it changes to true, focus input
    # and selection.
    scope.$watch (-> scope.shareDialog?.visible), (visible) ->
      if visible
        scope.$evalAsync(-> elem.find('#via').focus().select())

    scope.$watchCollection (-> crossframe.frames), (frames) ->
      if not frames.length
        return
      # Check to see if we are on a via page. If so, we just return the URI.
      re = /https:\/\/via\.annotran\.??/
      if re.test(frames[0].uri)
        scope.viaPageLink = frames[0].uri
      else
        scope.viaPageLink = 'https://via.annotran.??/' + frames[0].uri

  restrict: 'E'
  templateUrl: 'share_dialog.html'
]
