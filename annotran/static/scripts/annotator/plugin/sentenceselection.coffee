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

    this.operational = false
    this.currentIndex = 0
    this.storedEvent = null

    null

  destroy: ->
    $(document).unbind({
      "click": @makeSentenceSelection,
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

    if tagName = $(target).prop("tagName") == undefined
      console.log("We appear to have reached the end of the document.")
      window.getSelection().removeAllRanges()
      return

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

    this.storedEvent = event

    this.currentIndex = 0
    this.selectSentence event.target

    selection = Annotator.Util.getGlobal().getSelection()
    ranges = for i in [0...selection.rangeCount]
      r = selection.getRangeAt(0)
      if r.collapsed then continue else r

    if ranges.length
      event.ranges = ranges
      @annotator.onSuccessfulSelection event
      @annotator.createAnnotation()

    return null


  moveToNextSentence: (event) ->
    if this.operational == false
      # we are not in sentence selection mode
      return

    this.currentIndex = this.currentIndex + 1
    currentSelection = window.getSelection()

    this.selectSentence(currentSelection.anchorNode.parentElement)

    selection = Annotator.Util.getGlobal().getSelection()
    ranges = for i in [0...selection.rangeCount]
      r = selection.getRangeAt(0)
      if r.collapsed then continue else r

    if event == undefined
      # load the initial click event and use this as the default "base" event
      # this is needed so that the range is accurately described
      event = this.storedEvent

    if ranges.length
      event.ranges = ranges
      @annotator.onSuccessfulSelection event
      @annotator.createAnnotation()

    return null
