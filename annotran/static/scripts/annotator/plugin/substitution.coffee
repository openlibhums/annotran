Annotator = require('annotator')
$ = Annotator.$
xpathRange = Annotator.Range
Util = Annotator.Util

# This plugin implements the UI code for selecting sentences by clicking
module.exports = class Substitution extends Annotator.Plugin

  pluginInit: ->
# Register the event handlers required for creating a selection
    $(document).bind({
      "click": @makeSubstitution
    })

    null

  destroy: ->
    $(document).unbind({
      "click": @makeSubstitution
    })
    super

# This is called when the mouse is clicked on a DOM element.
# Checks to see if there is a sentence that we can select, if so
# calls Annotator's onSuccessfulSelection method.
#
# event - The event triggered this. Usually it's a click Event
#
# Returns nothing.
  makeSubstitution: (event = {}) =>
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

    alert("starting substition")

    DoSubstitution(full_xpath, full_xpath, 0, desiredText.length, "This is a replacement")

  # Raw javascript functions follow
  `
  //function that does replacement based on xpath and offsets
  function DoSubstitution(xpathPositionStart, xpathPositionEnd, startOffset, endOffset, substituteText) {

      // setup an associative array with the data from the parameters
      var data = {};
      data["start"] = xpathPositionStart;
      data["startOffset"] = startOffset;
      data["end"] = xpathPositionEnd;
      data["endOffset"] = endOffset;

      // load a SerializedRange object that spans the thing we want
      var full_range = new xpathRange.SerializedRange(data).normalize(document)
      var startContainer = full_range.startContainer;
      var endContainer = full_range.endContainer;

      // calculate the length of the annotation and the length of the substitution
      var substitutionLength = substituteText.length;
      var annotationLength = endOffset - startOffset;


      var fun = (function () {
          var commonAncestor = startContainer;
          var child = commonAncestor;
          var prefOffset = 0; //sum of all predeccessor lengths
          var startNode = null;

          var findStartNodeToBeginSubstitution = function () {
              var childNodes = child.childNodes;
              var i = 0, num = childNodes.length;
              while (i < num && startNode == null) {
                  child = childNodes[i];
                  i++;
                  if (child.nodeType == 3) {
                      var len;
                      if (child.nodeValue != "") {
                          len = child.nodeValue.length - 1;
                      } else {
                          len = 0;
                      }
                      if ((len + prefOffset) < startOffset) {
                          prefOffset += (child.nodeValue).length;
                          continue;
                      } else {
                          startNode = child;
                          return;
                      }
                  } else {
                      findStartNodeToBeginSubstitution();
                  }
              }
              return;
          }
          findStartNodeToBeginSubstitution();
          child = startNode;

          var substNodeLen = child.length;
          if (xpathPositionStart != xpathPositionEnd) {
              //because we want to remove all remaining text within that node as annotation will end within some other node,
              // and endOffset will denote the end character within that node
              child.nodeValue = getSubstituteText(prefOffset, startOffset, child.nodeValue.length, child.nodeValue, substituteText);
          } else {
              child.nodeValue = getSubstituteText(prefOffset, startOffset, endOffset, child.nodeValue, substituteText);
          }

          var nextSibl, nextNodeSelection = null;

          nextSibl = getNonWhitespaceNextSibling(child, startContainer, endContainer);

          //determine node selection
          if (!isNodeSubNodeOfNode(startContainer, nextSibl)) {
              nextNodeSelection = nextSibl;
              prefOffset = 0;
          }
          if (xpathPositionStart != xpathPositionEnd && nextSibl != null) {
              //the rest of the text within that nextSibl node must be removed as the annotation ends within some other node
              nextNodeSelection = removeNestedNodes(nextSibl, startContainer, endContainer);
              nextSibl = nextNodeSelection;
          } else if (nextNodeSelection != null && isNodeSubNodeOfNode(startContainer, nextSibl)) {
              nextNodeSelection = removeNestedNodes(nextNodeSelection, startContainer, endContainer);
              nextSibl = nextNodeSelection;
          }
          var flag = true;
          while (prefOffset < endOffset && nextSibl && nextSibl != commonAncestor) {
              if (flag && nextNodeSelection == null) {
                  prefOffset += substNodeLen;
                  flag = false;
              }
              prefOffset = removeHangingTextPerNodes(nextSibl, prefOffset, endOffset, true, endContainer);
              nextSibl = nextSibl.parentNode.nextSibling;
          }
      })(startContainer, endContainer);


  };

  function getNonWhitespaceNextSibling(node, startContainer, endContainer) {
      var nextNonWhiteSpaceNextSibling;
      if (node.nextSibling != null && isIgnorable(node.nextSibling)) {
          nextNonWhiteSpaceNextSibling = getNonWhitespaceNextSibling(node.nextSibling, startContainer, endContainer);
      } else if (node.nextSibling != null) {
          nextNonWhiteSpaceNextSibling = node.nextSibling;
      } else {
          var innerParent = node.parentNode;
          while ((innerParent.nextSibling == null && innerParent != startContainer)) {
              innerParent = innerParent.parentNode;
          }
          if ((innerParent == startContainer) && (startContainer == endContainer)) {
              return null; //sibling has been searched for within the same xpath
          }
          nextNonWhiteSpaceNextSibling = getNonWhitespaceNextSibling(innerParent, startContainer, endContainer);
      }
      return nextNonWhiteSpaceNextSibling;
  }

  function isNodeSubNodeOfNode(node, subnode) {
      //starting from startContainer, and the next that is not within it a new node selection, until endContainer
      var parent = subnode;
      if (parent == node) {
          return true;
      }
      while (parent != null && parent != node) {
          parent = parent.parentNode;
          if (parent == node) {
              return true;
          }
      }
      return false;
  };

  //this function will empty all nodes between startContainer and endContainer
  function removeNestedNodes(nextNodeSelection, startContainer, endContainer) {
      var nextNode = nextNodeSelection;
      while (nextNode != null && !isNodeSubNodeOfNode(endContainer, nextNode)) {
          if (nextNode.nodeType == 3) {
              nextNode.nodeValue = "";
          }
          if (nextNode.childNodes != null && nextNode.childNodes.length != 0) {
              var childNodes = nextNode.childNodes;
              var foundChild = null, i = 0, num = childNodes.length;
              while (i < num) {
                  var child = childNodes[i];
                  if (isNodeSubNodeOfNode(endContainer, child)) {
                      foundChild = child;
                      break;
                  }
                  i++;
              }
              var j = 0;
              while (j < i) {
                  nextNode.removeChild(childNodes[0]);
                  j++;
              }
              if (foundChild != null) {
                  return foundChild;
              }
          }
          while (nextNode.nextElementSibling == null && nextNode != startContainer) {
              nextNode = nextNode.parentNode;
          }
          if (nextNode == startContainer && nextNode.nextElementSibling == null) {
              nextNode = nextNode.parentNode;
          }
          nextNode = nextNode.nextElementSibling;
      }
      return nextNode;
  }

  function removeHangingTextPerNodes(node, prefOffset, endOffset, callNextSibling, endContainer) {
      console.log(node);
      console.log(endContainer);
      if (node.nodeType == 3) {
          var remainedTxtToRemove = endOffset - prefOffset;
          var len = node.nodeValue.length;
          prefOffset += len;
          if (remainedTxtToRemove > len) {
              node.nodeValue = "";
          } else {
              node.nodeValue = (node.nodeValue).substring(remainedTxtToRemove, len);
          }
      } else if (node.childNodes) {
          var childNodes = node.childNodes;
          var i = 0, num = childNodes.length;
          while (i < num) {
              var child = childNodes[i];
              console.log(child);
              console.log(i);
              if (prefOffset < endOffset) {
                  prefOffset = removeHangingTextPerNodes(child, prefOffset, endOffset, false);
              } else {
                  break;
              }
              i++;
          }
      }
      if (prefOffset < endOffset && node.nextSibling != null && callNextSibling) {
          prefOffset = removeHangingTextPerNodes(node.nextSibling, prefOffset, endOffset, true);
      }
      return prefOffset;
  };

  function getSubstituteText(prefOffset, startOffset, endOffset, originalText, substituteText) {
      var leftTextToSubstitute;
      var origTextLen = originalText.length;
      var subsTextLen = substituteText.length;
      //there is a guarantee that first letter of a substituteText is within an originalText
      var prefText = "", sufText = "";
      startOffset = startOffset - prefOffset;
      endOffset = endOffset - prefOffset;
      if (startOffset != 0) {
          prefText = originalText.substring(0, startOffset);
      }
      if (origTextLen > endOffset) {
          sufText = originalText.substring(endOffset, origTextLen);
      }
      return prefText + substituteText + sufText;
  };

  function isWhiteSpaceNode(node) {
      return !(/[^\t\n\r ]/.test(node.textContent));
  }

  function isIgnorable(node) {
      return (node.nodeType == 8) || ( (node.nodeType == 3) && isWhiteSpaceNode(node) );
  }


  function contains(parent, child) {
      var node;
      node = child;
      while (node !== null) {
          if (node === parent) {
              return true;
          }
          node = node.parentNode;
      }
      return false;
  };`



