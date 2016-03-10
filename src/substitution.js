/**
 * Created by marija on 9.3.2016..
 */
var xpath = require('xpath-range').xpath;


//function that does replacement based on xpath and offsets
function Substitution(jsonAnnotation, substitutionText) {
    var obj = JSON.parse(jsonAnnotation);
    var xpathPositionStart = obj.ranges[0].start;
    var xpathPositionEnd = obj.ranges[0].end;
    var startOffset = obj.ranges[1].startOffset;
    var endOffset = obj.ranges[1].endOffset;
    var startContainer = document.evaluate(xpathPositionStart, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    var endContainer = document.evaluate(xpathPositionEnd, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

   // var substitutionLength = substitutionText.length;

    console.log(startContainer.childNodes[0].nodeValue);

    var commonAncestor = startContainer;

    while (!contains(commonAncestor, endContainer)) {
        commonAncestor = commonAncestor.parentNode;
    }
  // var commonAncestorXPath = xpath.fromNode($(commonAncestor))[0];

    var txt = commonAncestor.childNodes[0];
    var childNodes = commonAncestor.childNodes;
    var flag = 0, arr = [];
    for(i = 0; i < childNodes.length; i++) {
        var child = childNodes[i];
        var type = child.nodeType;

       //node types 1..12
       if (child.nodeType == 3 && !flag) { //text node
           flag = 1;
           child.nodeValue = substitutionText;
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
}


exports.Substitution = Substitution;
