define(function (require, exports, module) {
    var $ = require('$');
    var Widget = require('../../lib/cmp/widget');
    var Sticky = require('../../lib/util/dom/sticky');
    var undef;

    var Tip = Widget.extend({
        attrs: {
            timer: null, // 显示的timer
            hideTimer: null, // 隐藏的timer
            timeout: 3000,
            template: '<div class="tips-pop"><span></span><a class="close" href="#" data-action="close">×</a></div>',
            top: 99
        },
        events: {
            'click [data-action=close]': function (e) {
                this.hide();
                return false;
            }
        },
        setup: function () {
            Tip.superclass.setup.call(this);
            Sticky.fix(this.element);
        },
        /**
         * 显示tip
         * @param text 文本
         * @param cls 样式
         * @param pos 位置
         */
        show: function (text, cls, params) {
            params = params || {};
            var pos = params.position;
            this.element.find('a.close')[params.hideClose === true ? 'hide' : 'show']();
            this.element.children('span:first').text(text);
            if (pos) {
                this.element.css(pos);
                if (pos.left === undef) {
                    this.element.css('left', ($(window).width() - this.element.width()) / 2);
                }
            } else {
                this.element.css({
                    left: ($(window).width() - this.element.width()) / 2,
                    top: this.get('top')
                });
            }
            this.element.removeClass().addClass('tips-pop ' + (cls || ''));
            this.element.show();
            return this;
        },
        /**
         * 隐藏
         */
        hide: function () {
            this.element.hide();
            if (this.timer) {
                clearTimeout(this.timer);
                this.timer = null;
            }
            return this;
        },
        /**
         * 成功消息可调用这个
         * @param text
         */
        success: function (text) {
            return this.show(text);
        },
        /**
         * 失败消息可调用这个
         * @param text
         */
        error: function (text) {
            return this.show(text, 'tips-failure');
        },
        /**
         * 显示后自动隐藏，默认3秒后
         */
        auto: function (text, type, params) {
            var that = this;
            params = params || {};
            params.delay = 0;
            params.hideClose = params.hideClose !== false;
            this.delay(text, type, params);
            if (this.hideTimer) {
                clearTimeout(this.hideTimer);
                this.hideTimer = null;
            }
            this.hideTimer = setTimeout(function () {
                that.hideTimer = null;
                that.hide();
            }, params.time || 3000);
            return this;
        },
        delay: function (text, type, params) {
            var that = this;
            var cls = '';
            params = params || {};
            if (params.cls) {
                cls = params.cls;
            } else {
                if (type === 'error') {
                    cls = 'tips-failure';
                }
            }
            if (this.timer) {
                clearTimeout(this.timer);
            }
            this.timer = setTimeout(function () {
                that.timer = null;
                that.show(text, cls, params);
            }, params.delay === undef ? 1000 : params.delay);
            return this;
        }
    });

    module.exports = {
        common: new Tip().render(),
        self: new Tip().render()
    };
});