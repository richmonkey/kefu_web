define(function(require, exports, module) {
  var formUtil = {}

  formUtil.toDict = function(form) {
    var dict = {}
      , array = form.serializeArray()
      , item

    for (var i = 0; i < array.length; i++) {
      item = array[i]
      dict[item.name] = item.value
    }

    return dict
  }

  module.exports = formUtil
});