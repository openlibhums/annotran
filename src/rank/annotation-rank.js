
Annotator.Plugin.Message = function (element, options) {
    Annotator.Plugin.apply(this, arguments);
};

Annotator.Plugin.Message.prototype = new Annotator.Plugin();


Annotator.Plugin.Message.prototype.pluginInit = function () {
       this.annotator.viewer.addField({
        load: function (field, annotation) {
            var rankStar = '<div class="rank">';
            rankStar += '<span>&#9734</span><span>&#9734</span><span>&#9734</span><span>&#9734</span><span>&#9734</span>';
            rankStar += '</div>';
            field.innerHTML = rankStar;
        }
    })
};