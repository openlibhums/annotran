/**
 * Created by marija on 9.3.2016..
 */
var xpath = require('xpath-range').xpath;


//function that does replacement based on xpath and offsets
function Substitution(jsonAnnotation) {
    var obj = JSON.parse(jsonAnnotation);
    var xpathPositionStart = obj.ranges[0].start;
    var xpathPositionEnd = obj.ranges[0].end;
    var startOffset = obj.ranges[0].startOffset;
    var endOffset = obj.ranges[0].endOffset;
    var startContainer = document.evaluate(xpathPositionStart, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    var endContainer = document.evaluate(xpathPositionEnd, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    var substituteText = obj.text;
    var substitutionLength = substituteText.length;
    var annotationLength = endOffset - startOffset;

    //console.log(startContainer.childNodes[0].nodeValue);

    //commonAncestor = xpath.fromNode($(commonAncestor))[0]
    //console.log(commonAncestor);

    fun = (function () {
        var commonAncestor = startContainer;
        var child = commonAncestor;
        var prefOffset = 0; //sum of all predeccessor lengths

        var findStartNodeToBeginSubstitution = function() {
            var childNodes = child.childNodes;
            for(i = 0; i < childNodes.length; i++) {
                child = childNodes[i];
                if (child.nodeType == 3) {
                    var len = child.nodeValue.length - 1;
                    if ((len + prefOffset) < startOffset) {
                        prefOffset += (child.nodeValue).length;
                        continue;
                    } else {
                        return;
                    }
                } else {
                    return findStartNodeToBeginSubstitution();}
                }
        }
        findStartNodeToBeginSubstitution();
        var substNodeLen = child.length;
        child.nodeValue = getSubstituteText(prefOffset, startOffset, endOffset, child.nodeValue, substituteText);

        var nextSibl;
        if(child.nextSibling) {
            nextSibl = child.nextSibling;
        } else if(child.parentNode) {
            nextSibl = child.parentNode.nextSibling;
        }
        var flag = true;
        while (prefOffset < endOffset && nextSibl && nextSibl != commonAncestor) {
            if (flag) {
                prefOffset += substNodeLen;
                flag = false;
            }
            prefOffset = removeHangingTextPerNodes(nextSibl, prefOffset, endOffset, true);
            nextSibl = nextSibl.parentNode.nextSibling;
        }
    })(startContainer, endContainer);

    fun(startContainer, endContainer);

    //var startNodeToBeginSubstitution = findStartNodeToBeginSubstitution(commonAncestor, startOffset, 0);
  // var commonAncestorXPath = xpath.fromNode($(commonAncestor))[0];

};

function removeHangingTextPerNodes(node, prefOffset, endOffset, callNextSibling) {
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
        removeHangingTextPerNodes(node.nextSibling, prefOffset, endOffset, true);
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
