Annotator = require('annotator')
$ = Annotator.$
xpathRange = Annotator.Range
Util = Annotator.Util

# This plugin implements the UI code for selecting sentences by clicking
module.exports = class SentenceSelection extends Annotator.Plugin

  pluginInit: ->
    # Register the event handlers required for creating a selection
    $(document).bind({
      "click": @makeSentenceSelection,
      "keypress": @keyPressHandler
    })

    this.operational = false
    this.currentIndex = 0

    null

  destroy: ->
    $(document).unbind({
      "click": @makeSentenceSelection,
      "keypress": @keyPressHandler
    })
    super

  toggleOperation: () ->
    this.operational = not this.operational

  prepareData: (target) ->
    desiredText = $(target).text()
    desiredText = desiredText.split('.')

    offset_to_use = 0
    counter = 0

    if desiredText.length == 1
      console.log("Current selection does not contain a full stop. Cannot split by sentence.")
      desiredText = []
      desiredText.push $(target).text()

    for sentence in desiredText
      if counter == this.currentIndex
        break
      offset_to_use = offset_to_use + sentence.length
      counter = counter + 1

    if desiredText.length == 1
      desiredText = $(target).text()
    else
      desiredText = desiredText[this.currentIndex]

    full_xpath = Util.xpathFromNode($(target), document)

    data = {
      start: full_xpath
      startOffset: offset_to_use + this.currentIndex
      end: full_xpath
      endOffset: offset_to_use + desiredText.length + this.currentIndex + 1
    }

    console.log(data)

    return data

  secondaryJump: (target) ->
    console.log("Trying secondary jump")
    this.currentIndex = 0
    nextSibling = $(target).next()

    if nextSibling != undefined and nextSibling.length != 0
      console.log("Using next sibling for jump")
      this.selectSentence nextSibling
    else
      nextSibling = $($(target).parent()).next()
      console.log("Using parent next sibling for jump")
      this.selectSentence nextSibling

  selectSentence: (target) ->
     # Get the currently selected ranges.
    tagName = $(target).prop("tagName").toLowerCase()

    # this loop checks that we are not within a formatting cell and that we should recurse upwards through parent elements
    while tagName is "i" or tagName is "strong" or tagName is "em" or tagName is "b" or tagName is "mark" or tagName is "small" or tagName is "del" or tagName is "ins" or tagName is "sub" or tagName is "sup"
      target = $(target).parent()
      tagName = $(target).prop("tagName").toLowerCase()

    data = this.prepareData target

    try
      anchor = new xpathRange.SerializedRange(data).normalize(document)

      window.getSelection().removeAllRanges()
      window.getSelection().addRange(anchor.toRange())
    catch error
      console.log("Jumping siblings")
      # if we get here the most likely thing is that the next sentence is beyond the range, so we can just pass a call
      # to the first sentence selection function with the target set to the next element
      this.currentIndex = 0
      nextSibling = $(window.getSelection().focusNode.parentElement).next()

      # now try again
      data = this.prepareData nextSibling

      if data.start.length == 0
        this.secondaryJump(target)
        return

      try
        anchor = new xpathRange.SerializedRange(data).normalize(document)

        window.getSelection().removeAllRanges()
        window.getSelection().addRange(anchor.toRange())
      catch error
        this.secondaryJump(target)

    return null


  # This is called when the mouse is clicked on a DOM element.
  # Checks to see if there is a sentence that we can select, if so
  # calls Annotator's onSuccessfulSelection method.
  #
  # event - The event triggered this. Usually it's a click Event
  #
  # Returns nothing.
  makeSentenceSelection: (event = {}) =>

    if this.operational == false
      # we are not in sentence selection mode
      return

    this.currentIndex = 0
    this.selectSentence event.target

  moveToNextSentence: () ->
    this.currentIndex = this.currentIndex + 1
    currentSelection = window.getSelection()

    this.selectSentence(currentSelection.baseNode.parentElement)

    return null

  keyPressHandler: (event = {}) =>
    if this.operational == false
      # we are not in sentence selection mode
      return

    if event.which == 13
      # handle the enter key
      this.moveToNextSentence()