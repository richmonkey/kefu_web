define(function(require, exports, module) {
  var $ = require('$')

  var validators = {
    '[data-required]': {
      rule: function(input) {
        return !!$.trim(input.val()).length
      }
    , invalid: '请填写{{name}}。'
    }
  }

  var _ = {
    all: function(ary, fn, context) {
      var result = true
      $.each(ary, function(idx, item) {
        result = result && fn.call(context, idx, item, ary)
      })
      return result
    }
  }

  var defaultOptions = {
    invalidSelector: '.error'
  }

  function ValidateForm(form, options) {
    this.options = $.extend({}, defaultOptions, options)
    if (!form) {
      throw new Error('A form object is requried')
    }

    form.on('submit', $.proxy(function(e) {
      if (!this.validate(form)) {
        e.preventDefault()
        e.stopPropagation()
        e.stopImmediatePropagation()
      }
    }, this))

    this.fieldsToValidate = form.find('[data-validate]')
    this.form = form
    this.bindInvalid()
  }

  ValidateForm.prototype = {
    constructor: ValidateForm.prototype.constructor
  , validate: function(form) {
      this.clearInvalids()
      var validateResult = true

      this.fieldsToValidate.each($.proxy(function(idx, el) {
        el = $(el)

        if (!this.validateElem(el)) {
          validateResult = false
        }
      }, this))

      return validateResult
    }
  , validateElem: function(el) {
      return _.all(validators, function(selector, validator) {
        if (!el.is(selector)) { return true }
        var valid = validator.rule(el)
        if (valid) { return true }
        var invalidMessage = validator.invalid
        el.trigger('invalid', invalidMessage && invalidMessage
          .replace('{{name}}', el.data('name') || '文字'))
        return valid
      }, this)
    }
  , bindInvalid: function() {
      this.form.on('invalid', $.proxy(this.handleInvalid, this))
    }
  , handleInvalid: function(e, invalidMessage) {
      var target = $(e.target)
        , errMsgElem = target.closest('td')
            .find(this.options.invalidSelector)
      errMsgElem.text(invalidMessage)
      target.addClass('ipt-error')
    }
  , clearInvalids: function() {
      this.form.find(this.options.invalidSelector).html('&nbsp;')
      this.fieldsToValidate.removeClass('ipt-error')
    }
  }

  module.exports = ValidateForm
});