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
'''
**/

/**
 * @ngdoc service
 * @name  groups
 *
 * @description Provides access to the list of groups that the user is currently
 *              a member of and the currently selected group in the UI.
 *
 *              The list of groups is initialized from the session state
 *              and can then later be updated using the add() and remove()
 *              methods.
 */
'use strict';

var STORAGE_KEY = 'hypothesis.groups.focus';

// this assumes that h is stored in the same root directory as annotran
var events = require('../../../../h/h/static/scripts/events.js');

// @ngInject
function groups(localStorage, session, settings, $rootScope, $http) {
  // The currently focused group. This is the group that's shown as selected in
  // the groups dropdown, the annotations displayed are filtered to only ones
  // that belong to this group, and any new annotations that the user creates
  // will be created in this group.
  var focusedGroup;
  var eventBroadcasted = false;

  function all() {
    return session.state.groups || [];
  };

  // Return the full object for the group with the given id.
  function get(id) {
    var gs = all();
    for (var i = 0, max = gs.length; i < max; i++) {
      if (gs[i].id === id) {
        //$rootScope.$broadcast(events.GROUP_FOCUSED, gs[i].id);
        return gs[i];
      }
    }
  };

  /** Leave the group with the given ID.
   * Returns a promise which resolves when the action completes.
   */
  function leave(id) {
    var response = $http({
      method: 'POST',
      url: settings.serviceUrl + 'groups/' + id + '/leave',
    });

    // the groups list will be updated in response to a session state
    // change notification from the server. We could improve the UX here
    // by optimistically updating the session state

    return response;
  };


  /** Return the currently focused group. If no group is explicitly focused we
   * will check localStorage to see if we have persisted a focused group from
   * a previous session. Lastly, we fall back to the first group available.
   */
  function focused() {
    if (focusedGroup) {
      if ($rootScope.firstLoad == undefined) {
        $rootScope.firstLoad = true;
        $rootScope.$broadcast(events.GROUP_FOCUSED, focusedGroup.id);
      }
      return focusedGroup;
    }

    var fromStorage = get(localStorage.getItem(STORAGE_KEY));

    if (fromStorage) {
      focusedGroup = fromStorage;

      if ($rootScope.firstLoad == undefined) {
        $rootScope.firstLoad = true;
        $rootScope.$broadcast(events.GROUP_FOCUSED, focusedGroup.id);
      }

      return focusedGroup.id;
    }

    if ($rootScope.firstLoad == undefined) {
      $rootScope.firstLoad = true;
      $rootScope.$broadcast(events.GROUP_FOCUSED, all()[0].id);
    }
    return all()[0].id;
  }

  /** Set the group with the passed id as the currently focused group. */
  function focus(id) {
   var g = get(id);
   if (g) {
     focusedGroup = g;
     localStorage.setItem(STORAGE_KEY, g.id);
     $rootScope.$broadcast(events.GROUP_FOCUSED, g.id);
   }
  }

  // reset the focused group if the user leaves it
  $rootScope.$on(events.GROUPS_CHANGED, function () {

    if (focusedGroup) {
      focusedGroup = get(focusedGroup.id);
      $rootScope.$broadcast(events.LANGUAGE_FOCUSED, focusedGroup.id);
      if (!focusedGroup) {
        var focusResult = focused();

        $rootScope.$broadcast(events.LANGUAGE_FOCUSED, focused());
      }
    }
  });

  return {
    all: all,
    get: get,

    leave: leave,

    focused: focused,
    focus: focus,
  };
}

module.exports = groups;
