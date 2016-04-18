define(function(require, exports, module) {
    var $ = require('$');
    var helper = require('helper');
    var action = require('../../../lib/util/dom/action');
    var Tip = require('../../common/tip').self;
    var ConfirmBox = require('../../../lib/cmp/dialog/confirm-box');

    var tpl = {
        agreement: require('../../tpl/agreement')
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
            password: function() {
                var node = $('#password');
                var password = $.trim(node.val());
                var tipNode = node.closest('tr').find('.error').eq(0);
                var flag = true;
                if (password.length === 0) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('请输入密码');
                }else if (password.length < 6) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('密码太短');
                } else {
                    node.removeClass('ipt-error');
                    tipNode.html('&nbsp;');
                }
                return flag;
            },
            passwordSure: function() {
                var node = $('#password_sure');
                var passwordSure = $.trim(node.val());
                var originPsw = $.trim($('#password').val());
                var tipNode = node.closest('tr').find('.error').eq(0);
                var flag = true;
                if (passwordSure.length === 0) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('请再次输入密码');
                } else if (passwordSure !== originPsw) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('两次输入密码不一致');
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
        resend: function() {
            var node = $('#send_verify');
            node.addClass('btn-disabled').attr('data-action', 'disabled');
            var time = 5;
            var resend = function() {
                setTimeout(function() {
                    time--;
                    node[0].innerHTML = '(' + time + ')秒后可重新发送验证邮件';
                    if (time === 0) {
                        clearTimeout(resend);
                        node.removeClass('btn-disabled').attr('data-action', 'sendVerify').html('注册');
                    } else {
                        resend();
                    }
                }, 1000);
            };
            resend();
        },
        sendVerify: function() {
            if (shelper.check.all()) {
                var email = $.trim($('#email').val());
                var password = $.trim($('#password').val());
                $.post('/api/send_verify_email', {
                    email: email,
                    password: password
                }, function(data) {
                    //Tip.auto('已发送验证邮件到您的邮箱，请注意查收');
                    // shelper.resend();
                    window.location.href = '/register/valid?mail=' + email;
                }, 'json').fail(function(res) {
                    var data = res.responseJSON;
                    if (data['meta']) {
                        if (+data['meta']['code'] !== 200) {
                            Tip.auto(data['meta']['message'], 'error');
                        }
                    }
                });
            }
        }
    };

    $(function() {

        action.listen({
            sendVerify: function(e, node, type) {
                shelper.sendVerify();
            },
            disabled: function(e, node, type) {
                return false;
            },
            showAgreement: function(e, node, type) {
                ConfirmBox.show({
                    title: '',
                    height: 500,
                    width: 850,
                    content: tpl.agreement.render(),
                    buttons: [{
                        text: '确认',
                        className: 'btn-s btn-success mr',
                        action: 'close'
                    }]
                }).on('close', function() {
                    this.hide();
                });
            }
        });

        $(document.body).keydown(function(e) {
            if (e.keyCode === 13) {
                shelper.sendVerify();
            }
        });

    });
});