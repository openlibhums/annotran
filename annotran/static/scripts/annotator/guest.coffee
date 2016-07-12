Guest =  require('../../../../../h/h/static/scripts/annotator/guest.coffee');
extend = require('extend')
Annotator = require('annotator')
$ = Annotator.$

class GuestExt extends Guest
    html: extend {}, Annotator::html,
      adder: '''
        <div class="annotator-adder">
          <button class="h-icon-insert-comment" data-action="comment" title="New Translation"></button>
        </div>
      '''


module.exports = GuestExt