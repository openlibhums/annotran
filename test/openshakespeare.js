OpenShakespeare = ("OpenShakespeare" in window) ? OpenShakespeare : {}

OpenShakespeare.Annotator = function (element) {
  var $ = jQuery, self = this

  this.annotator = $(element).annotator().data('annotator')
  this.currentUser = null

  this.options = {
    user: { }


  }



  return this
}
