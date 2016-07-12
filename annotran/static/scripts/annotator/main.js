/*
Copyright (c) 2013-2014 Hypothes.is Project and contributors

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

var extend = require('extend');
var Annotator = require('annotator');

// Polyfills
var g = Annotator.Util.getGlobal();
if (g.wgxpath) {
  g.wgxpath.install();
}

// Applications
Annotator.Guest = require('./guest');
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
Annotator.Plugin.Substitution = require('./plugin/substitution');

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
