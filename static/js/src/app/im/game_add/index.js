define(function(require, exports, module) {
  var $ = require('$')
    , helper = require('helper')
    , Tip = require('../../../app/common/tip').self
    , makeGameForm = require('../../../app/widget/game_form');

  var form = $('.push-add-form form');

  makeGameForm(form);
});
