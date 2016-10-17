Annotator = require('annotator')
$ = Annotator.$
xpathRange = Annotator.Range
Util = Annotator.Util

# This plugin implements the UI code for selecting sentences by clicking
module.exports = class SentenceSelection extends Annotator.Plugin

  pluginInit: ->
    # Register the event handlers required for creating a selection
    $(document).bind({
      "click": @findASentence
    })

    this.operational = false
    this.currentIndex = 0
    this.currentSentence = 0
    this.storedEvent = null
    this.extentElement = null
    this.savedOffset = 0

    null

  destroy: ->
    $(document).unbind({
      "click": @findASentence
    })
    super

  toggleOperationOn: () ->
    this.operational = true
    Annotator._instances[0].plugins.CSSModify.hideAdder()

  toggleOperationOff: () ->
    this.operational = false
    Annotator._instances[0].plugins.CSSModify.showAdder()

  anchorToPage: (data) ->
    anchor = new xpathRange.SerializedRange(data).normalize(document)

    window.getSelection().removeAllRanges()
    window.getSelection().addRange(anchor.toRange())

    return null

  normalizeStyleTags: (target) ->

    # Get the currently selected ranges.
    tagName = $(target).prop("tagName").toLowerCase()

    # this loop checks that we are not within a formatting cell and that we should recurse upwards through parent elements
    while tagName is "i" or tagName is "strong" or tagName is "em" or tagName is "b" or tagName is "mark" or tagName is "small" or tagName is "del" or tagName is "ins" or tagName is "sub" or tagName is "sup"
      target = $(target).parent()
      tagName = $(target).prop("tagName").toLowerCase()

    return target

  packageData: (initialTarget, endTarget, endIndex, startIndexOffset = 0) ->
    full_xpath = Util.xpathFromNode($(initialTarget), document)
    end_xpath = Util.xpathFromNode($(endTarget), document)

    data = {
      start: full_xpath
      startOffset: startIndexOffset + this.savedOffset
      end: end_xpath
      endOffset: endIndex + 1
    }

    this.savedOffset = 0
    return data

  returnNext: (currentTarget) ->
    nextSibling = $(currentTarget).next()

    if nextSibling != undefined and nextSibling.length != 0 and nextSibling.prop("tagName").toLowerCase() != "figure" and nextSibling.prop("tagName").toLowerCase() != "img" and nextSibling.prop("tagName").toLowerCase() != "applet"  and nextSibling.prop("tagName").toLowerCase() != "audio"  and nextSibling.prop("tagName").toLowerCase() != "embed"  and nextSibling.prop("tagName").toLowerCase() != "object"  and nextSibling.prop("tagName").toLowerCase() != "video"
      return nextSibling
    else
      if nextSibling != undefined and nextSibling.length != 0
        return this.returnNext(nextSibling)
      else
        return this.findNextJumpNode(currentTarget)

  scanForNextSibling: (initialTarget, currentTarget, offset_to_use, endIndex) ->
    # here want to test:
    # 1. is there a sibling element?
    # 2. is there a parent element with a next sibling?
    this.currentIndex = 0
    this.currentSentence = 0

    nextSibling = this.returnNext(currentTarget)

    if offset_to_use == endIndex + 1
      initialTarget = nextSibling

    if offset_to_use == endIndex + 1
      initialTarget = nextSibling

    if nextSibling != undefined and nextSibling.length != 0
      this.selectSentence initialTarget, nextSibling
    else
      # this needs to gracefully fall through
      this.selectSentence initialTarget, nextSibling

  selectSentence: (initialTarget, currentTarget = undefined, force = false) ->

    if currentTarget == undefined
        currentTarget = initialTarget

    desiredText = $(currentTarget).text()
    match = /[.!?][\b\s]/.test(desiredText)
    desiredText = desiredText.split(/[.!?]\s/)

    finalCount = desiredText.length - 1

    matchEnd = desiredText[this.currentSentence] == ""

    offset_to_use = 0
    counter = 0

    if desiredText.length == 1
      desiredText = []
      desiredText.push $(currentTarget).text()

    for sentence in desiredText
      if counter == this.currentSentence
        break
      offset_to_use = offset_to_use + sentence.length + 2
      counter = counter + 1

    if desiredText.length == 1
      desiredText = $(currentTarget).text()
    else
      desiredText = desiredText[this.currentSentence]

    console.log(desiredText)

    if (desiredText != undefined and desiredText.endsWith(".")) or (desiredText != undefined and desiredText.endsWith("?")) or (desiredText != undefined and desiredText.endsWith("!"))
      # this means that we have reached a line break that ends with a sentence
      match = false

    if desiredText != undefined
      endIndex = offset_to_use + desiredText.length + 1

    if endIndex > $(currentTarget).text().length - 1
      endIndex = $(currentTarget).text().length - 1

    if (this.currentSentence == finalCount) and (matchEnd == false) and (desiredText.endsWith(".") == false)
      # if this is the case then we are starting mid-element and need to jump
      match = false
      if this.savedOffset == 0
        this.savedOffset = offset_to_use

    # test if we have found a sentence marker or if we are forcing this through anyway
    if (match or force) and (offset_to_use < endIndex)
      data = this.packageData(initialTarget, currentTarget, endIndex, offset_to_use)
      this.anchorToPage(data)
    else
      tagName = $(currentTarget).prop('tagName').toLowerCase()

      if tagName == 'tr'
        this.selectSentence initialTarget, currentTarget.find(">:first-child")
      if tagName == 'td' or tagName == 'th'
        length = $(currentTarget).text().length - 1
        data = this.packageData(initialTarget, currentTarget, length, 0)
        this.anchorToPage(data)
      else
        if desiredText == undefined
          console.log("HERE")
          nextSibling = this.returnNext(currentTarget)
          this.currentIndex = 0
          this.currentSentence = 0
          this.selectSentence nextSibling
        else if desiredText.endsWith(".") or desiredText.endsWith("!") or desiredText.endsWith("?")
          console.log("Sentence condition")
          this.selectSentence initialTarget, currentTarget, true
        else
          this.scanForNextSibling initialTarget, currentTarget, offset_to_use, endIndex

  findASentence: (event = {}) =>
    if this.operational == false
      # we are not in sentence selection mode
      return

    this.storedEvent = event

    this.currentIndex = 0
    this.currentSentence = 0

    event.target = this.normalizeStyleTags event.target

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

  findNextJumpNode: (target) ->
    parent = $(target).parent()

    nextSibling = $(parent).next()

    if nextSibling == undefined
      return this.findNextJumpNode parent

    else if nextSibling.length == 0

      tagName = $(nextSibling).prop("tagName")

      if tagName != undefined
        tagName = tagName.toLowerCase()

        if tagName != "figure" and tagName != "img"
          if tagName == 'body' or tagName == 'html'
            return nextSibling
          else
            return this.findNextJumpNode parent
        else
          if tagName == 'body' or tagName == 'html'
            return nextSibling
          else
            return this.findNextJumpNode nextSibling
      else
        return this.findNextJumpNode parent

    return nextSibling

  moveToNextSentence: (event) ->
    if this.operational == false
      # we are not in sentence selection mode
      return

    currentSelection = window.getSelection()

    this.currentIndex = currentSelection.extentOffset
    this.currentSentence = this.currentSentence + 1

    elementToUse = currentSelection.extentNode.parentElement
    tagName = $(elementToUse).prop('tagName').toLowerCase()

    if elementToUse.textContent.length <= (this.currentIndex)
      nextSibling = $(elementToUse).next()

      this.currentIndex = 0
      this.currentSentence = 0

      # algorithm here is:
      # 1. check if there is a sibling
      # 2. if there is no sibling, check the parent
      # 3. if the parent has a sibling, use that
      # 4. if the parent has no sibling, pass parent as element to 2

      if nextSibling == undefined or nextSibling.length == 0
        nextSibling = this.findNextJumpNode(elementToUse)

      elementToUse = nextSibling

    this.selectSentence elementToUse

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
