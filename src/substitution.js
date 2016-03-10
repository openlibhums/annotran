/**
 * Created by marija on 9.3.2016..
 */

//todo - write function that does replacement based on xpath and offsets
function Substitution() {
    this.startContainer = document.evaluate('//html', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    this.startOffset = 0;
    this.endContainer = document.evaluate('//html', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    this.endOffset = 1;



};
exports.Substitution = Substitution;
