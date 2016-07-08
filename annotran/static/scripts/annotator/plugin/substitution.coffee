Annotator = require('annotator')
$ = Annotator.$
xpathRange = Annotator.Range
Util = Annotator.Util
original_document = ''

# This plugin implements the UI code for selecting sentences by clicking
module.exports = class Substitution extends Annotator.Plugin

  pluginInit: ->
  # Register the event handlers required for creating a selection

    $(document).bind({
      "click": @startSubstitution
    })

    this.original_document = ""

    null

  destroy: ->
    $(document).unbind({
      "click": @startSubstitution
    })
    super


  startSubstitution: (event = {}) =>
    if this.original_document == ""
      this.original_document = `$("body").html()`

    if this.original_document != `$("body").html()`
      `
      $("body").html(this.original_document);
      `
      return null
    else
      this.makeSubstitution(event)



# This is called when the mouse is clicked on a DOM element.
# Checks to see if there is a sentence that we can select, if so
# calls Annotator's onSuccessfulSelection method.
#
# event - The event triggered this. Usually it's a click Event
#
# Returns nothing.
  makeSubstitution: (event = {}) =>

    start_xpath = "/html[1]/body[1]/div[2]/h2[1]"
    end_xpath = "/html[1]/body[1]/div[2]/div[5]/p[2]"

    data = {
      start: start_xpath
      startOffset: 0
      end: end_xpath
      endOffset: 2428
    }

    this.singleSubstitution(data, "This is a replacement")
    return


  singleSubstitution: (data = {}, substituteText = '') =>
    # resolve the passed xpath
    full_range = new xpathRange.SerializedRange(data).normalize(document)

    # map the start and end points
    start = full_range.start
    end = full_range.end

    removeArray = []

    start.textContent = substituteText

    if start != end
      nextElement = start.nextSibling

      if this.checkChildren(nextElement, end, data, removeArray) == false
        this.cleanUp(removeArray)
        return

      while nextElement != end
        if this.checkChildren(nextElement, end, data, removeArray) == false
          this.cleanUp(removeArray)
          return

        if nextElement == null
          nextElement = start.parentNode
          start = nextElement

        if nextElement.nextSibling != null
          nextElement = nextElement.nextSibling
        else
          nextElement = nextElement.parentNode.nextSibling
    else
      this.cleanUp(removeArray)
      return

    this.cleanUp(removeArray)
    return

  cleanUp: (removeArray) =>
    for ele in removeArray
      ele.remove()

  checkChildren: (nextElement = null, end, data, removeArray) =>

    # make sure we don't hit any null instances
    if nextElement is null
      return true

    # if this is a text element, we will empty it
    if nextElement.nodeType == 3
      if nextElement == end
        # here we replace up to the offset
        nextElement.textContent = nextElement.textContent[data.endOffset..]
        return false
      else
        result = this.checkChildren(childNode, end, data, removeArray)
        nextElement.textContent = ""

        if nextElement.parentNode.nodeType == 1 and nextElement.parentNode.textContent.trim() == ""
          removeArray.push nextElement.parentNode

        if result == false
          return false

    if nextElement.nodeName == "BR"
      removeArray.push nextElement

    if nextElement.childElementCount == 0
      for childNode in nextElement.childNodes
        if childNode == end
          childNode.textContent = childNode.textContent[data.endOffset..]
          return false
        else
          return this.checkChildren(childNode, end, data, removeArray)

      return true
    else
      for childNode in nextElement.childNodes
        if childNode == end
          return false
        else
          result = this.checkChildren(childNode, end, data, removeArray)

          if !result
            return false

      return true


