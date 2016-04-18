define(function (require, exports, module) {
    var $ = require('$');
    var helper = require('helper');
    var action = require('../../../lib/util/dom/action');
    var Tip = require('../../common/tip').self;

    var tpl = {};

    var cache = {};

    var shelper = {
        resend: function () {
            var node = $('#resend');
            node.addClass('label-disabled').attr('data-action', 'disabled');
            var time = 60;
            var resendTimeout = function () {
                setTimeout(function () {
                    time--;
                    node[0].innerHTML = '(' + time + ')秒后可重新发送验证邮件';
                    if (time === 0) {
                        clearTimeout(resendTimeout);
                        node.removeClass('label-disabled').attr('data-action', 'sendVerify').html('重新发送激活邮件');
                    } else {
                        resendTimeout();
                    }
                }, 1000);
            };
            resendTimeout();
        }
    };

    $(function () {

        action.listen({
            resend: function (e, node, type) {
                var email = $.trim($('#email').text());
                $.post('/api/verify_email', {
                    'email': email
                }, function (data) {
                    if (data['meta']) {
                        if (+data['meta']['code'] !== 200) {
                            Tip.auto(data['meta']['message'], 'error');
                        } else {
                            Tip.auto('已发送验证邮件到您的邮箱，请注意查收');
                            // shelper.resend();
                        }
                    }
                }, 'json').fail(function (res) {
                    var data = res.responseJSON;
                    if (data['meta']) {
                        if (+data['meta']['code'] !== 200) {
                            Tip.auto(data['meta']['message'], 'error');
                        }
                    }
                });
            },
            disabled: function (e, node, type) {
                return false;
            }
        });

        var error = $.trim($('#error').val());

        if (error.length > 0) {
            Tip.auto(error, 'error');
        }

    });
});