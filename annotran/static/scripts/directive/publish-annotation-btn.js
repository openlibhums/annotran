'use strict';

var eventsa =  require('../events');

/**
 * @ngdoc directive
 * @name publishAnnotationBtn
 * @description Displays a combined privacy/selection post button to post
 *              a new annotation
 */
// @ngInject
function publishAnnotationBtnController(crossframe, $rootScope, $scope) {

    this.showDropdown = false;
    this.privateLabel = 'Only Me';

    $rootScope.$on('moving_to_sentence', function () {
      if($rootScope.sentencebysentence == "on") {
        $scope.vm.onCancel();
      }
    });

    this.publishDestination = function () {
      return this.isShared ? this.group.name : this.privateLabel;
    }

    this.moveToNext = function() {
        crossframe.call("moveToNextSentence");
    }

    this.groupType = function () {
      return this.group.public ? 'public' : 'group';
    }

    this.setPrivacy = function (level) {
      this.onSetPrivacy({level: level});
    }
}

/**
 * @ngdoc directive
 * @name languageList
 * @restrict AE
 * @description Displays a list of available languages
 */
// @ngInject
function publishAnnotationBtn($window, languages, settings) {
  return {
    bindToController: true,
    controller: publishAnnotationBtnController,
    controllerAs: 'vm',
    restrict: 'E',
    scope: {
      group: '=',
      canPost: '=',
      isShared: '=',
      onCancel: '&',
      onSave: '&',
      onSetPrivacy: '&'
    },
    templateUrl: 'publish_annotation_btn.html'
  };
};

module.exports = {
  directive: publishAnnotationBtn,
  Controller: publishAnnotationBtnController
};
