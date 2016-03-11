/**
 * Created by marija on 9.3.2016..
 */
var xpath = require('xpath-range').xpath;


//function that does replacement based on xpath and offsets
//TODO: finish replacement by using offsets...
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
    var annotationLength = xpathPositionEnd - xpathPositionStart;

    console.log(startContainer.childNodes[0].nodeValue);

    var commonAncestor = startContainer;

    while (!contains(commonAncestor, endContainer)) {
        commonAncestor = commonAncestor.parentNode;
    }
    //commonAncestor = xpath.fromNode($(commonAncestor))[0]
    //console.log(commonAncestor);

    var startNodeToBeginSubstitution = findStartNodeToBeginSubstitution(commonAncestor, startOffset, 0);
    console.log(startNodeToBeginSubstitution);

  // var commonAncestorXPath = xpath.fromNode($(commonAncestor))[0];

    var substNodeLen = startNodeToBeginSubstitution[0].length;
    var prefOffset = startNodeToBeginSubstitution[1];
    //call function that will make substitution
    startNodeToBeginSubstitution[0].nodeValue = getSubstituteText(prefOffset, startOffset, endOffset, startNodeToBeginSubstitution[0].nodeValue, substituteText);

    if (substNodeLen < endOffset) {
        removeHangingTextPerNodes(startNodeToBeginSubstitution[0].nextSibling, prefOffset, endOffset);
    }

    /*
    var txt = commonAncestor.childNodes[0];
    var childNodes = commonAncestor.childNodes;
    var flag = 0, arr = [];
    for(i = 0; i < childNodes.length; i++) {
        var child = childNodes[i];
        var type = child.nodeType;

       //node types 1..12
       if (child.nodeType == 3 && !flag) { //text node
           flag = 1;
           child.nodeValue = substituteText;
          // var substitutionText = document.createTextNode(substitutionText);
           //startContainer.replaceChild(substitutionText, child);
        } else {
            arr.push(i);
       }
    }
    var flag = 0;
    for (i = 0; i < arr.length; i++) {
        if (!flag) {
            flag = 1;
            startContainer.removeChild(childNodes[arr[i]]);
        } else {
            startContainer.removeChild(childNodes[arr[--i]]);
        }
    }
    console.log(startContainer);
    */
};

function removeHangingTextPerNodes(node, prefOffset, endOffset) {
    endOffset = endOffset - prefOffset;
    if (node.nodeType == 3 && node.length < endOffset) {
        node.nodeValue = "";
    } else if (node.nodeType == 3) {
        var textToRemain = (node.nodeValue).substring(0, endOffset);
        prefOffset += prefOffset;
        node.nodeValue = textToRemain;
    } else {
        var childNodes = node.childNodes;
        for(i = 0; i < childNodes.length; i++) {
            var child = childNodes[i];
            removeHangingTextPerNodes(child, prefOffset, endOffset);
        }
    }
    if (node.nextSibling) {
        removeHangingTextPerNodes(node.nextSibling, prefOffset, endOffset);
    }
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

function findStartNodeToBeginSubstitution(commonAncestor, startOffset, prefOffset) {
    var childNodes = commonAncestor.childNodes;
    for(i = 0; i < childNodes.length; i++) {
        var child = childNodes[i];
        var len = child.length;
        if (child.nodeType == 3 && ((len + prefOffset) < startOffset) ) {
            prefOffset += (child.nodeValue).length;
            continue;
        } else if (child.nodeType == 3) {
            return [child, prefOffset];
        } else {
            return findStartNodeToBeginSubstitution(child, startOffset, prefOffset);
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
