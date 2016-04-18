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
            password: function() {
                var node = $('#password');
                var password = $.trim(node.val());
                var tipNode = node.closest('tr').find('.error').eq(0);
                var flag = true;
                if (password.length === 0) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('请输入新密码');
                } else if (password.length < 6) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('密码太短');
                } else {
                    node.removeClass('ipt-error');
                    tipNode.html('&nbsp;');
                }
                return flag;
            },
            surePassword: function() {
                var node = $('#password_sure');
                var surePassword = $.trim(node.val());
                var password = $.trim($('#password').val());
                var tipNode = node.closest('tr').find('.error').eq(0);
                var flag = true;
                if (surePassword.length === 0) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('请再次输入新密码');
                } else if (password !== surePassword) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('两次输入的密码不一致');
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
        reset: function() {
            if (shelper.check.all()) {
                var code = $.trim($('#code').val());
                var password = $.trim($('#password').val());

                $.ajax({
                    url: '/api/reset_password',
                    method: 'POST',
                    data: helper.stringify({
                        'code': code,
                        'password': password
                    }),
                    success: function (data) {
                        if (+data['meta']['code'] === 200) {
                            Tip.auto('重置密码成功', 'success');
                            window.location.href = '/login';
                        } else {
                            Tip.auto(data['meta']['message'], 'error');
                        }
                    },
                    error: function (res) {
                        Tip.error(res.responseJSON.meta.message);
                    },
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'Application/json; charset=UTF-8'
                });
            }
        }
    };

    $(function() {

        action.listen({
            resetPassword: function(e, node, type) {
                shelper.reset();
            }
        });

        $(document.body).keydown(function(e) {
            if (e.keyCode === 13) {
                shelper.reset();
            }
        });

    });
});
