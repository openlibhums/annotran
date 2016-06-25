var extend = require('extend');
var Annotator = require('annotator');

// Polyfills
var g = Annotator.Util.getGlobal();
if (g.wgxpath) {
  g.wgxpath.install();
}

// Applications
Annotator.Guest = require('../../../../../h/h/static/scripts/annotator/guest');
Annotator.Host = require('../../../../../h/h/static/scripts/annotator/host');
Annotator.Sidebar = require('./sidebar');
Annotator.PdfSidebar = require('../../../../../h/h/static/scripts/annotator/pdf-sidebar');

// UI plugins
Annotator.Plugin.BucketBar = require('../../../../../h/h/static/scripts/annotator/plugin/bucket-bar');
Annotator.Plugin.Toolbar = require('../../../../../h/h/static/scripts/annotator/plugin/toolbar');

// Document type plugins
Annotator.Plugin.PDF = require('../../../../../h/h/static/scripts/annotator/plugin/pdf');
require('../../../../../h/h/static/scripts/vendor/annotator.document');  // Does not export the plugin :(

// Selection plugins
Annotator.Plugin.TextSelection = require('../../../../../h/h/static/scripts/annotator/plugin/textselection');
Annotator.Plugin.SentenceSelection = require('./plugin/sentenceselection');

// Cross-frame communication
Annotator.Plugin.CrossFrame = require('../../../../../h/h/static/scripts/annotator/plugin/cross-frame');
Annotator.Plugin.CrossFrame.AnnotationSync = require('../../../../../h/h/static/scripts/annotation-sync');
Annotator.Plugin.CrossFrame.Bridge = require('../../../../../h/h/static/scripts/bridge');
Annotator.Plugin.CrossFrame.Discovery = require('../../../../../h/h/static/scripts/discovery');

var docs = 'https://h.readthedocs.org/en/latest/hacking/customized-embedding.html';
var options = {
  app: jQuery('link[type="application/annotator+html"]').attr('href')
};

if (window.hasOwnProperty('hypothesisConfig')) {
  if (typeof window.hypothesisConfig === 'function') {
    extend(options, window.hypothesisConfig());
  } else {
    throw new TypeError('hypothesisConfig must be a function, see: ' + docs);
  }
}

Annotator.noConflict().$.noConflict(true)(function() {
  'use strict';
  var Klass = window.PDFViewerApplication ?
      Annotator.PdfSidebar :
      Annotator.Sidebar;
  if (options.hasOwnProperty('constructor')) {
    Klass = options.constructor;
    delete options.constructor;
  }
  window.annotator = new Klass(document.body, options);
});
