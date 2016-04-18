define(function(require, exports, module) {
    var $ = require('$');
    var helper = require('helper');
    var action = require('../../../lib/util/dom/action');
    var Tip = require('../../common/tip').self;

    var tpl = {
    };

    var cache = {
    };

    var shelper = {
        check: {
            email: function() {
                var node = $('#email');
                var email = $.trim(node.val());
                var mailReg = /^[a-z0-9!#$%&’*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&’*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
                var tipNode = node.closest('tr').find('.error').eq(0);
                var flag = true;
                if(!email) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('邮箱地址必填');
                } else if (!mailReg.test(email)) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('邮箱格式有误');
                } else {
                    node.removeClass('ipt-error');
                    tipNode.html('&nbsp;');
                }
                return flag;
            },
            all: function() {
                var flag = true;
                for(var key in shelper.check) {
                    if(key !== 'all') {
                        var result = shelper.check[key]();
                        if(flag) {
                            flag = result;
                        }
                    }
                }
                return flag;
            }
        },
        sendResetVerify: function() {
            if (shelper.check.all()) {
                var email = $.trim($('#email').val());
                $.post('/api/send_reset_email', {
                    email: email
                }, function(data) {
                    console.log(data);
                    if (data['meta']) {
                        if (+data['meta']['code'] !== 200) {
                            Tip.auto(data['meta']['message'], 'error');
                        } else {
                            window.location.href = '/forget/valid?mail=' + email;
                        }
                    } else {
                        // Tip.auto('已发送验证邮件到您的邮箱，请注意查收');
                        // shelper.resend();
                        window.location.href = '/forget/valid?mail=' + email;
                    }
                }, 'json').fail(function(res) {
                    Tip.error(res.responseJSON.meta.message);
                });
            }
        }
    };

    $(function() {

        action.listen({
            sendResetVerify: function(e, node, type) {
                shelper.sendResetVerify();
            },
            disabled: function(e, node, type) {
                return false;
            }
        });

        $(document.body).keydown(function(e) {
            if (e.keyCode === 13) {
                shelper.sendVerify();
            }
        });

    });
});