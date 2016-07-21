Annotator = require('annotator')
$ = Annotator.$

# This plugin modifies the host page's CSS according to crossframe calls
module.exports = class CSSModify extends Annotator.Plugin

  pluginInit: ->
  # Register the event handlers required for creating a selection
    super
    null

  hideAdder: () ->
    $(".annotator-adder").css({"visibility": "hidden"});

  showAdder: () ->
    $(".annotator-adder").css({"visibility": "visible"});