Annotator = require('annotator')
$ = Annotator.$
xpathRange = Annotator.Range
Util = Annotator.Util
original_document = ''

# This plugin implements the UI code for selecting sentences by clicking
module.exports = class Substitution extends Annotator.Plugin

  pluginInit: ->
  # Register the event handlers required for creating a selection

    ###
    $(document).bind({
      "click": @makeSubstitution
    })
    ###


    this.original_document = ""
    this.continue_action = ""
    this.continue_data = null

    # here we setup a DOM Mutation Observer to allow continued execution after we modify the body tag
    `
    var target = document.body;

    var observer = new MutationObserver(this.handle_state_continuity);
    var config = { attributes: true, childList: true, characterData: true };

    observer.observe(target, config);
    `

    null

  ###
  destroy: ->
    $(document).unbind({
      "click": @makeSubstitution
    })
    super
  ###
  handle_state_continuity: (mutation = null) =>
    if this.continue_action == "multipleSubstitution"
      console.log("Annotran: Starting substitution via state machine.")
      this.multipleSubstitution(null)
    this.continue_action = ""

  clearDOM: (event = {}) =>
    if this.original_document == ""
      this.original_document = `$("body").html()`

    if this.original_document != `$("body").html()`
      console.log("Annotran: Restoring DOM to original state.")
      `
      $("body").html(this.original_document);
      `
      return null


# This is called when the mouse is clicked on a DOM element.
# It sets up a dummy annotation and fires it
#
# event - The event triggered this. Usually it's a click Event
#
# Returns nothing.
  makeSubstitution: (event = {}) =>

    annotations = []

    first_package = {}

    start_xpath = "/html[1]/body[1]/div[2]/h2[1]"
    end_xpath = "/html[1]/body[1]/div[2]/div[5]/p[2]"

    data = {
      start: start_xpath
      startOffset: 0
      end: end_xpath
      endOffset: 2428
    }

    first_package.data = data
    first_package.substituteText = "This is a replacement"

    second_package = {}

    start_xpath = "/html[1]/body[1]/div[2]/div[5]/p[2]"
    end_xpath = "/html[1]/body[1]/div[2]/div[5]/p[2]"

    second_data = {
      start: start_xpath
      startOffset: 2430
      end: end_xpath
      endOffset: 2432
    }

    second_package.data = second_data
    second_package.substituteText = "Another replacement"

    annotations.push(first_package)
    annotations.push(second_package)

    this.continue_action = "multiple_substitute"
    this.continue_data = annotations

    # clear the DOM back to its original state
    # NB this may mean that the state machine will re-call this function via the DOM Mutation Observer
    this.clearDOM()

    this.multipleSubstitution(annotations)

    return

  multipleSubstitution: (annotations = []) =>
    # reset state machine variables if this script is executing
    this.continue_action = ""
    this.continue_data = null

    # iterate over the annotations _in reverse order_ so that all the XPATHs still work
    # in other words, this function takes a list of annotations in top to bottom order and works from the end upwards
    for data in annotations.reverse()
      this.singleSubstitution(data.target[0].selector[1], data.text)

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


