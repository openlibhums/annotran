/**
 * Created by marija on 9.3.2016..
 */
var xpath = require('xpath-range').xpath;

function MultipleSubstitution(annotationsToSub) {
    var prefOffset = 0, jsonObj, obj, xpathPositionStart, xpathPositionEnd, startOffset, endOffset, substituteText;
    var prevXpathStart = null, prevXpathEnd = null;
    for (i = 0; i < annotationsToSub.length; i++) {
       jsonObj = JSON.stringify(JSON.decycle(annotationsToSub[i]), null, "  ");
       obj = JSON.parse(jsonObj);
       xpathPositionStart = obj.ranges[0].start;
       xpathPositionEnd = obj.ranges[0].end;
       startOffset = obj.ranges[0].startOffset;
       endOffset = obj.ranges[0].endOffset;
       if (isWithinSameXPath(prevXpathStart, xpathPositionStart, prevXpathEnd, xpathPositionEnd)) {
         if (annotationLen < substituteTextLen) {
           prefOffset += (substituteTextLen - annotationLen);
         } else {
           prefOffset -= (annotationLen - substituteTextLen);
         }
           startOffset += prefOffset;
           endOffset += prefOffset;
       } else {
           prefOffset = 0;
       }
       substituteText = obj.text;
       var annotationLen = endOffset - startOffset;
       var substituteTextLen = substituteText.length;
       Substitution(xpathPositionStart, xpathPositionEnd, startOffset, endOffset, substituteText);
       prevXpathStart = xpathPositionStart; prevXpathEnd = xpathPositionEnd;
    }
}

function isWithinSameXPath(prevXpathStart, xpathPositionStart, prevXpathEnd, xpathPositionEnd) {
    if (prevXpathStart != null && prevXpathEnd != null) {
        if (prevXpathStart == xpathPositionStart && prevXpathEnd == xpathPositionEnd) {
            return true;
        } else {
            return false;
        }
    }
    return false;
}

//function that does replacement based on xpath and offsets
function Substitution(xpathPositionStart, xpathPositionEnd, startOffset, endOffset, substituteText) {
    /*
    if (document.implementation.hasFeature("Range", "2.0")) {
        var oRange = document.createRange();
       // oRange.setStart(xpathPositionStart, startOffset);
       // oRange.setEnd(xpathPositionEnd, endOffset);
        console.log(oRange);
             //range code here
    }*/

   // var test = xpath.toRange('//div/p[1]', 8, '//div/p[1]', 37, "/");

    var startContainer = document.evaluate('/'+ xpathPositionStart, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    var endContainer = document.evaluate('/' + xpathPositionEnd, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

    // var p = xpath.toRange('/'+ xpathPositionStart, startOffset, '/' + xpathPositionEnd, endOffset);
    //var tst = xpath.toRange('html/body/div[1]/div[1]/p[1]', 0, 'html/body/div[1]/div[1]/p[1]', 5);

    var substitutionLength = substituteText.length;
    var annotationLength = endOffset - startOffset;

    //console.log(startContainer.childNodes[0].nodeValue);

    //commonAncestor = xpath.fromNode($(commonAncestor))[0]
    //console.log(commonAncestor);

    var fun = (function () {
        var commonAncestor = startContainer;
        var child = commonAncestor;
        var prefOffset = 0; //sum of all predeccessor lengths
        var startNode = null;

        var findStartNodeToBeginSubstitution = function() {
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
       /* if(child.nextSibling) {
            nextSibl = child.nextSibling;
        } else if(child.parentNode) {
            var innerParent = child.parentNode;
            while ((innerParent.nextSibling == null && innerParent != startContainer)) {
                innerParent = innerParent.parentNode;
            }
            if (innerParent == startContainer && innerParent.nextSibling == null) {
                    innerParent = innerParent.parentNode;
            }
            nextSibl = innerParent.nextSibling;
        }*/
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

    // fun(startContainer, endContainer);

    //var startNodeToBeginSubstitution = findStartNodeToBeginSubstitution(commonAncestor, startOffset, 0);
  // var commonAncestorXPath = xpath.fromNode($(commonAncestor))[0];

};

function getNonWhitespaceNextSibling(node, startContainer, endContainer) {
    var nextNonWhiteSpaceNextSibling;
    if (node.nextSibling != null && isIgnorable(node.nextSibling)) {
        nextNonWhiteSpaceNextSibling = getNonWhitespaceNextSibling(node.nextSibling, startContainer, endContainer);
    } else if (node.nextSibling != null) {
        nextNonWhiteSpaceNextSibling =  node.nextSibling;
    } else {
        var innerParent = node.parentNode;
        while ((innerParent.nextSibling == null && innerParent != startContainer)) {
            innerParent = innerParent.parentNode;
        }
        if((innerParent == startContainer) && (startContainer == endContainer)) {
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
        while(nextNode.nextElementSibling == null && nextNode != startContainer) {
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


/*
function findStartNodeToBeginSubstitution(commonAncestor, offset, prefOffset) {
    var childNodes = commonAncestor.childNodes;
    for(i = 0; i < childNodes.length; i++) {
        var child = childNodes[i];
        if (child.nodeType == 3) {
            var len = child.nodeValue.length - 1;
            if ((len + prefOffset) < offset) {
                prefOffset += (child.nodeValue).length;
                continue;
            } else {
                return [child, prefOffset];
            }
        } else {
            return findStartNodeToBeginSubstitution(child, offset, prefOffset);
        }
    }
};
*/

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
};

exports.Substitution = Substitution;
exports.MultipleSubstitution = MultipleSubstitution;
