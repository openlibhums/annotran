Annotator = require('annotator')
$ = Annotator.$
xpathRange = Annotator.Range

# This plugin implements the UI code for selecting sentences by clicking
module.exports = class Substitution extends Annotator.Plugin

  pluginInit: ->
  # Register the event handlers required for creating a selection
    this.original_document = ""
    this.state = "clean"
    super
    null

  clearDOM: (event = {}) =>

    annotatorComponents = []

    # save the DOM
    if this.original_document == ""
      this.original_document = $("body").clone()

    if this.state == "clean"
      return

    this.state = "clean"

    # blank the DOM
    if this.original_document != $("body")

      for ele in $("body").children()
        if ele.nodeName != undefined and ele.nodeName != "IFRAME" and ele.nodeName != "SCRIPT" and ele.nodeName != "DIV"
          ele.remove()
        else
          if $(ele).hasClass("annotator-notice") or $(ele).hasClass("annotator-frame") or $(ele).hasClass("annotator-adder")
            annotatorComponents.push ele
          else if ele.nodeName != "SCRIPT"
            ele.remove()

      for ele in $(this.original_document).children()
        if ele.nodeName != undefined and ele.nodeName != "IFRAME" and ele.nodeName != "SCRIPT" and ele.nodeName != "DIV"
          $(annotatorComponents[0]).before($(ele).clone())
        else
          if $(ele).hasClass("annotator-notice") or $(ele).hasClass("annotator-frame") or $(ele).hasClass("annotator-adder")
          else if ele.nodeName != "SCRIPT"
            $(annotatorComponents[0]).before($(ele).clone())

      this.annotator.adder.hide()

      return null

  multipleSubstitution: (annotations = []) =>
    # iterate over the annotations _in reverse order_ so that all the XPATHs still work
    # in other words, this function takes a list of annotations in top to bottom order and works from the end upwards
    this.state = "dirty"

    for data in annotations.reverse()

      if data.target[0].selector != undefined
        for target_selector in data.target[0].selector
          if target_selector.type == "RangeSelector"
            packager = {
              start: target_selector.startContainer
              startOffset: target_selector.startOffset
              end: target_selector.endContainer
              endOffset: target_selector.endOffset
            }

            this.singleSubstitution(packager, data.text)

  createSubstitutionElement: (originalText, substituteText, ele) ->

    # we don't preserve full formatting but we can at least put some paragraph breaks in
    originalText = originalText.replace(new RegExp('\n', 'g'), '<br/><br/>')
    substituteText = substituteText.replace(new RegExp('\n', 'g'), '<br/>')

    newEle = $('<span class="annotation-hover"></span>')
    newEle.html(substituteText)

    newEle.css({
      "background-color" : "#F5F5F5",
      "color" : "#000000"
    })

    ele.before(newEle)

    newEle.mouseover (event) ->
      newEle.html(originalText)

    newEle.mouseleave (event) ->
      newEle.html(substituteText)

    return newEle

  singleSubstitution: (data = {}, substituteText = '') =>

    div = document.createElement('div')
    div.appendChild(document.createTextNode(substituteText))
    substituteText = div.innerHTML

    full_range = null

    try
      # resolve the passed xpath
      full_range = new xpathRange.SerializedRange(data).normalize(document.body)
    catch
      full_range = null

    if full_range == null
      return

    # map the start and end points
    start = full_range.start
    end = full_range.end

    removeArray = []

    newEle = this.createSubstitutionElement(full_range.text(), substituteText, $(start))

    start.textContent = ""

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


