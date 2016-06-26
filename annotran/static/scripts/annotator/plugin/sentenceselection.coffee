Annotator = require('annotator')
$ = Annotator.$
xpathRange = Annotator.Range
Util = Annotator.Util

# This plugin implements the UI code for selecting sentences by clicking
module.exports = class SentenceSelection extends Annotator.Plugin

  pluginInit: ->
    # Register the event handlers required for creating a selection
    $(document).bind({
      "click": @makeSentenceSelection
    })

    null

  destroy: ->
    $(document).unbind({
      "click": @makeSentenceSelection
    })
    super

  # This is called when the mouse is clicked on a DOM element.
  # Checks to see if there is a sentence that we can select, if so
  # calls Annotator's onSuccessfulSelection method.
  #
  # event - The event triggered this. Usually it's a click Event
  #
  # Returns nothing.
  makeSentenceSelection: (event = {}) =>
    # Get the currently selected ranges.

    tagName = $(event.target).prop("tagName").toLowerCase()

    # this loop checks that we are not within a formatting cell and that we should recurse upwards through parent elements
    while tagName is "i" or tagName is "strong" or tagName is "em" or tagName is "b" or tagName is "mark" or tagName is "small" or tagName is "del" or tagName is "ins" or tagName is "sub" or tagName is "sup"
      event.target = $(event.target).parent()
      tagName = $(event.target).prop("tagName").toLowerCase()

    desiredText = $(event.target).text()
    desiredText = desiredText.split('.')[0]

    full_xpath = Util.xpathFromNode($(event.target), document)

    data = {
      start: full_xpath
      startOffset: 0
      end: full_xpath
      endOffset: desiredText.length
    }

    anchor = new xpathRange.SerializedRange(data).normalize(document)

    window.getSelection().removeAllRanges()
    window.getSelection().addRange(anchor.toRange())

