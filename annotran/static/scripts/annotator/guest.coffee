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
          <button class="h-icon-move" data-action="lockit" title="Sentence-by-Sentence Lock Mode"></button>
        </div>
      '''

    anchor: (annotation) ->
      # disable anchoring pip display in sidebar
      null

    _connectAnnotationSync: (crossframe) =>
      super

      crossframe.on 'toggleSentenceSelection', () =>
        Annotator = require('annotator')
        Annotator._instances[0].plugins.SentenceSelection.toggleOperation()

      crossframe.on 'moveToNextSentence', () =>
        Annotator = require('annotator')
        # TODO: this needs to pass a false event object so that the annotation is correctly created
        Annotator._instances[0].plugins.SentenceSelection.moveToNextSentence()

      crossframe.on 'resetDOM', () =>
        Annotator = require('annotator')
        Annotator._instances[0].plugins.Substitution.clearDOM()
        Annotator._instances[0].plugins.CSSModify.showAdder()

      crossframe.on 'passAnnotations', (annotations) =>
        Annotator = require('annotator')
        Annotator._instances[0].plugins.Substitution.clearDOM()
        Annotator._instances[0].plugins.CSSModify.hideAdder()

        if annotations.length > 0
          Annotator._instances[0].plugins.Substitution.multipleSubstitution(annotations)

    onAdderClick: (event) ->
      event.preventDefault?()
      event.stopPropagation?()
      @adder.hide()
      switch $(event.target).data('action')
        when 'lockit'
          this.plugins.SentenceSelection.toggleOperation()
        when 'comment'
          this.createAnnotation()
      Annotator.Util.getGlobal().getSelection().removeAllRanges()


module.exports = GuestExt