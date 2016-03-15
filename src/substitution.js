/**
 * Created by marija on 9.3.2016..
 */
var xpath = require('xpath-range').xpath;


//function that does replacement based on xpath and offsets
function Substitution(jsonAnnotation, substituteText) {
    var obj = JSON.parse(jsonAnnotation);
    var xpathPositionStart = obj.ranges[0].start;
    var xpathPositionEnd = obj.ranges[0].end;
    var startOffset = obj.ranges[1].startOffset;
    var endOffset = obj.ranges[1].endOffset;
    var startContainer = document.evaluate(xpathPositionStart, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    var endContainer = document.evaluate(xpathPositionEnd, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

    console.log("start container: " + startContainer);
    console.log("end conatiner: " + endContainer);

    var substitutionLength = substituteText.length;
    var annotationLength = endOffset - startOffset;

    console.log(startContainer.childNodes[0].nodeValue);

    var commonAncestor = startContainer;

    while (!contains(commonAncestor, endContainer)) {
        commonAncestor = commonAncestor.parentNode;
    }
    //commonAncestor = xpath.fromNode($(commonAncestor))[0]
    //console.log(commonAncestor);

    var startNodeToBeginSubstitution = findStartNodeToBeginSubstitution(commonAncestor, startOffset, 0);

  // var commonAncestorXPath = xpath.fromNode($(commonAncestor))[0];

    var substNodeLen = startNodeToBeginSubstitution[0].length;
    var prefOffset = startNodeToBeginSubstitution[1]; //sum of all predeccessor lengths
    startNodeToBeginSubstitution[0].nodeValue = getSubstituteText(prefOffset, startOffset, endOffset, startNodeToBeginSubstitution[0].nodeValue, substituteText);

    if (annotationLength > substNodeLen) {
        prefOffset += substNodeLen;
      // var node = findContainingChildNode(commonAncestor, startNodeToBeginSubstitution[0]);
        removeHangingTextPerNodes(startNodeToBeginSubstitution[0].nextSibling, prefOffset, endOffset);
    }
};

/*
function findContainingChildNode(commonAncestor, node) {
    var childNodes = commonAncestor.childNodes;
    for(i = 0; i < childNodes.length; i++) {
        var child = childNodes[i];
        if (child != node && child.childNodes) {
            if (findInDepth(child, node))
                return child;
        } else if (child == node) {
            return child;
        }
    }
}

function findInDepth(node, nodeToFind) {
    var childNodes = node.childNodes;
    for(i = 0; i < childNodes.length; i++) {
        var child = childNodes[i];
        if (child == nodeToFind)
            return true;
        if (child.childNodes)
            findInDepth(child, nodeToFind);
    }
    return false;
}
*/

function removeHangingTextPerNodes(node, prefOffset, endOffset) {
   /* if ((prefOffset + prefOffsetWithinNode) >= endOffset) {
        return;
    }*/
   // endOffset = endOffset - prefOffset;
    if (node.nodeType == 3) {
        var remainedTxtToRemove = endOffset - prefOffset;
        var len = node.nodeValue.length;
        prefOffset += len;
        if (remainedTxtToRemove > len) {
            node.nodeValue = "";
        } else {
            node.nodeValue = (node.nodeValue).substring(remainedTxtToRemove, len);
        }
    } else {
        var childNodes = node.childNodes;
        for(i = 0; i < childNodes.length; i++) {
            var child = childNodes[i];
            if (prefOffset < endOffset) {
                prefOffset = removeHangingTextPerNodes(child, prefOffset, endOffset);
            } else {
                break;
            }
        }
    }
    if (prefOffset < endOffset && node.nextSibling != null) {
        removeHangingTextPerNodes(node.nextSibling, prefOffset, endOffset);
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
