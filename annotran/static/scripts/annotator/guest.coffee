Guest =  require('../../../../../h/h/static/scripts/annotator/guest.coffee');
extend = require('extend')
Annotator = require('annotator')
$ = Annotator.$

class GuestExt extends Guest
    constructor: (element, options) ->
      super

    html: extend {}, Annotator::html,
      adder: '''
        <div class="annotator-adder">
          <button class="h-icon-insert-comment" data-action="comment" title="New Translation"></button>
        </div>
      '''

    anchor: (annotation) ->
      # disable anchoring pip display in sidebar
      null

    _connectAnnotationSync: (crossframe) ->
      this.subscribe 'annotationsLoaded', (annotations) =>
        for annotation in annotations
          # annotations are structured like this:
          # startContainer: annotation.target[0].selector[1].startContainer
          # startOffset: annotation.target[0].selector[1].startOffset
          # endContainer: annotation.target[0].selector[1].endContainer
          # endOffset: annotation.target[0].selector[1].endOffset
          alert(annotation.target[0].selector[1].startContainer)

module.exports = GuestExt