/*
 Substitute Annotator Plugin v0.1
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

// standard boilerplate Annotator plugin code

var substitution1 = require('./substitution');


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

    Annotator.Plugin.Substitutions = (function (superClass) {
        extend(Substitutions, superClass);

        // for now, hard-wired country tags

        Substitutions.prototype.options = {
            showField: true,
            substitutions: [
                {
                    value: "bbk:english",
                    label: "English"
                }, {
                    value: "bbk:french",
                    label: "French"
                }, {
                    value: "bbk:german",
                    label: "German"
                }, {
                    value: "bbk:croatian",
                    label: "Croatian"
                }, {
                    value: "bbk:arabic",
                    label: "Arabic"
                }, {
                    value: "bbk:hebrew",
                    label: "Hebrew"
                }, {
                    value: "bbk:thai",
                    label: "Thai"
                }, {
                    value: "bbk:spanish",
                    label: "Spanish"
                }, {
                    value: "bbk:dutch",
                    label: "Dutch"
                }, {
                    value: "bbk:swedish",
                    label: "Swedish"
                }, {
                    value: "bbk:danish",
                    label: "Danish"
                }, {
                    value: "bbk:finnish",
                    label: "Finnish"
                }
            ]
        };

        Substitutions.prototype.field = null;

        Substitutions.prototype.input = null;

        Substitutions.prototype.subButton = null;


        // register for annotator events to keep tag list up-to-date

        Substitutions.prototype.events = {
            "annotationCreated": "updateAnnotationTags",
            "annotationUpdated": "updateAnnotationTags",
//      "annotationDeleted": "_onAnnotationDeleted"
            "annotationsLoaded": "annotationsLoadedDump"
        };


        tagstore = [];  // internal state list of tags
        substitutionTag = null;
        annotationsCache = [];
        substituteFlag = false;
        currentAnnotation = [];

        // create a drop-down menu as a new field on the annotator floating dialog

        Substitutions.prototype.pluginInit = function () {
            var i, id, len, m, newfield, ref, select;
            if (!Annotator.supported()) {
                return;
            }

            // language support taken out for now while testing substitution

            /*
             this.field = this.annotator.editor.addField({

             label: Annotator._t('LanguageDropdown'),
             load: this.updateField,
             submit: this.setAnnotationSubstitutions
             });
             id = Annotator.$(this.field).find('input').attr('id');
             select = '<li class="annotator-item"><select style="width:100%"><option value="">(No language)</option>';
             ref = this.options.substitutions;
             for (i = 0, len = ref.length; i < len; i++) {
             m = ref[i];
             select += '<option value="' + m.value + '">' + m.label + '</option>';
             }
             select += '</select></li>';
             newfield = Annotator.$(select);
             Annotator.$(this.field).replaceWith(newfield);
             this.field = newfield[0];
             this.annotator.viewer.addField({
             load: this.updateViewer,
             annoPlugin: this
             });
             */
            // add button to execute substitution

            this.field = this.annotator.editor.addField({
                id: 'substitution-button',
                type: 'input', //options (textarea,input,select,checkbox)
                label: 'Substitute Annotations'
//                submit: this.buttonsActions

            });

            //Modify the element created with annotator to be an invisible span
            butt = '<a href="#save" class="annotator-save annotator-focus">' + 'Substitute' + '</a>';

            var newfield = Annotator.$('<li class="annotator-item">' + '<button id = "subsButton" type="button">' + butt + '</button>' + '</li>');
            Annotator.$(this.field).replaceWith(newfield);
            this.field = newfield[0];

            var button = document.querySelector('#subsButton');
            button.addEventListener('click', this.buttonsActions);


            //-- Viewer
            this.subButton = $(this.field).find(':input');

            this.field = this.annotator.editor.addField({
                label: Annotator._t('No tags yet defined'),
                type: 'textarea',
                load: this.updateField,
                submit: this.setAnnotationSubstitutions
            });

            id = Annotator.$(this.field).find('input').attr('id');


            return this.input = Annotator.$(this.field).find('select');
        }


        Substitutions.prototype.buttonsActions = function () {
            var i, j;
//            console.log("buttonsActions");

            substituteFlag = true;
        }

        Substitutions.prototype.substituteExecute = function () {
            var i, j;
//            console.log("substituteExecute", substitutionTag);
            annotationsToSub = [];

            if (substitutionTag) {
                for (i = 0; i < annotationsCache.length; i++) {
                    annoToCheck = annotationsCache[i];

                    for (j = 0; j < annotationsCache[i].tags.length; j++) {
                        if (annoToCheck.tags.indexOf(substitutionTag) >= 0) {
                            annotationsToSub.push(annotationsCache[i]);
                        }
                    }

                }
            }
            else {
                annotationsToSub.push(currentAnnotation);

            }


            jsonObjects = JSON.stringify(JSON.decycle(annotationsToSub[0]), null, "  ");
            console.log(jsonObjects);


            // API call to substitute DOM

            substitution1.Substitution(jsonObjects);
            substituteFlag = false;

        }


        function Substitutions(element, options) {
            this.setAnnotationSubstitutions = bind(this.setAnnotationSubstitutions, this);
            this.updateField = bind(this.updateField, this);
            this.subButton = bind(this.subButton, this);
            this.updateViewer = bind(this.updateViewer, this);
            _ref = Substitutions.__super__.constructor.apply(this, arguments);
            if (options.substitutions) {
                this.options.substitutions = options.substitutions;
            }
            return _ref;
        }

        Substitutions.prototype.updateField = function (field, annotation) {
            var value;
            value = '';
            if (substitutionTag) {
                value = substitutionTag;
            }
//            console.log("updateField", substitutionTag);
            return this.input.val(value);
        }

        Substitutions.prototype.setAnnotationSubstitutions = function (field, annotation) {
            //           console.log("setAnnotationSubstitutions", this.input.val());
            return substitutionTag = this.input.val();
        }

        Substitutions.prototype.dropdownChange = function () {
            this.input = Annotator.$(this.field).find('select');
            substitutionTag = this.input.val();

        }


        Substitutions.prototype.updateViewerTags = function (field, annotation) {
            var displayValue, i, len, m, ref, results;
            field = Annotator.$(field);
            this.input = Annotator.$(this.field).find('select');
            var value = '';
            displayValue = this.input.val(value);
//            console.log("updateViewerTags fired", substitutionTag);
            if (annotation.substitution) {
                displayValue = annotation.substitution;
//                console.log(displayvalue);
                ref = this.annoPlugin.options.substitutions;
                results = [];
                for (i = 0, len = ref.length; i < len; i++) {
                    m = ref[i];
                    if (m.value === annotation.substitution) {
                        displayValue = m.label;
                        field.parent().parent().find('.annotator-substitution').html(Annotator.Util.escape(displayValue) + " ");
                        if (this.annoPlugin.options.showField) {
                            results.push(field.addClass('annotator-substitution').html('<span class="annotator-substitution">' + Annotator.Util.escape(displayValue) + '</span>'));
                        } else {
                            results.push(field.remove());
                        }
                    } else {
                        results.push(void 0);
                    }
                }
                return results;
            } else {
                return field.remove();
            }
        }


        // maintain list of tags

        Substitutions.prototype.updateAnnotationTags = function (annotation) {
            var i, len;
            id = Annotator.$(this.field).find('input').attr('id');
//            console.log("updateAnnotationTags", annotation);

            currentAnnotation = annotation;

            annotationsCache.push(annotation);

            for (i = 0, len = annotation.tags.length; i < len; i++) {
                if (tagstore.indexOf(annotation.tags[i]) <= 0) {
                    tagstore.push(annotation.tags[i]);
//                    console.log(annotation.tags[i]);

                    select = '<li class="annotator-item"><select style="width:100% " id = "annotator-subsdropdown"><option value="">Substitute Current Annotation</option>';
                    for (i = 0, len = tagstore.length; i < len; i++) {
                        m = tagstore[i];
                        select += '<option value="' + m + '">' + m + '</option>';
                    }
                    select += '</select></li>';
                    newfield = Annotator.$(select);
                    Annotator.$(this.field).replaceWith(newfield);
                    this.field = newfield[0];

                    this.annotator.viewer.addField({
                        load: this.updateViewerTags,
                        annoPlugin: this
                    });

                    var dropdownMenu = document.querySelector('#annotator-subsdropdown');
                    dropdownMenu.addEventListener('change', this.dropdownChange);


                }
            }
            if (substituteFlag) {
                this.substituteExecute();
            }
            return this.input = Annotator.$(this.field).find('select');

        }

        Substitutions.prototype.annotationsLoadedDump = function (annotations) {
//            console.log("annotations loaded");
            //       var annotations = [];
            for (i = 0, len = annotations.length; i < len; i++) {
                annotation = annotations[i];
                //               annotationsCache.push(annotation);
                this.updateAnnotationTags(annotation);
//                console.log(JSON.stringify(annotations, null, "  "));
            }
        }

        return Substitutions;

    })(Annotator.Plugin);

}).call(this);

