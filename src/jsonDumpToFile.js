/*
 JSON dump to file Annotator Plugin v0.1
 Copyright (C) 2016 Birkbeck, University of London
 License:

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

// Annotator plugin to save all annotations on a page to a JSON file
// assumes you have permission to save files on your client side

// standard boilerplate Annotator plugin code

(function () {
    var bind = function (fn, me) {
            return function () {
                return fn.apply(me, arguments);
            };
        },
        extend = function (child, parent) {
            for (var key in parent) {
                if (hasProp.call(parent, key)) child[key] = parent[key];
            }
            function ctor() {
                this.constructor = child;
            }

            ctor.prototype = parent.prototype;
            child.prototype = new ctor();
            child.__super__ = parent.prototype;
            return child;
        },
        hasProp = {}.hasOwnProperty;

    Annotator.Plugin.jsonDumpToFile = (function (superClass) {
        extend(jsonDumpToFile, superClass);

        // register for annotator events to keep tag list up-to-date

        jsonDumpToFile.prototype.events = {
            "annotationsLoaded": "annotationsLoadedDump"
        };

        // create a drop-down menu as a new field on the annotator floating dialog

        jsonDumpToFile.prototype.pluginInit = function () {
            var i, id, len, m, newfield, ref, select;
            if (!Annotator.supported()) {
                return;
            }
        }

        function jsonDumpToFile(element, options) {
            this.setAnnotationDump = bind(this.setAnnotationDump, this);
            jsonDumpToFile.__super__.constructor.apply(this, arguments);
            if (options.jsonDumpToFile) {
                this.options.jsonDumpToFile = options.jsonDumpoFile;
            }
        }


        jsonDumpToFile.prototype.annotationsLoadedDump = function (annotations) {
            for (i = 0, len = annotations.length; i < len; i++) {
                annotation = annotations[i];
                console.log(JSON.stringify(annotation, null, "  "));
            }
            saveJSON(annotations);


        }

        function saveJSON(data, filename) {

            if (!data) {
                console.error('saveJSON: No data');
                return;
            }

            if (!filename) filename = 'annotations.json';

            if (typeof data === "object") {
                data = JSON.stringify(data, undefined, 4);
            }

            var blob = new Blob([data], {type: 'text/json'}),
                e = document.createEvent('MouseEvents'),
                a = document.createElement('a');

            a.download = filename;
            a.href = window.URL.createObjectURL(blob);
            a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
            e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            a.dispatchEvent(e);
        }

        return jsonDumpToFile;


    })(Annotator.Plugin);

}).call(this);


