define(function (require, exports, module) {
    var $ = require('$');
    var helper = require('helper');
    var action = require('../../../lib/util/dom/action');
    var Tip = require('../../common/tip').self;
    var Placeholder = require('../../../lib/util/dom/placeholder');
    var urlKit = require('../../../mod/url');
    var tpl = {};

    var cache = {};

    var shelper = {
        check: {
            email: function () {
                var node = $('#email');
                var email = $.trim(node.val());
                var mailReg = /^[a-z0-9!#$%&’*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&’*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
                var tipNode = node.closest('tr').find('.error').eq(0);
                var flag = true;
                if (!email) {
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
            password: function () {
                var node = $('#password');
                var password = $.trim(node.val());
                var tipNode = node.closest('tr').find('.error').eq(0);
                var flag = true;
                if (password.length === 0) {
                    flag = false;
                    node.addClass('ipt-error');
                    tipNode.text('请输入密码');
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
            all: function () {
                var flag = true;
                for (var key in shelper.check) {
                    if (key !== 'all') {
                        var result = shelper.check[key]();
                        if (flag) {
                            flag = result;
                        }
                    }
                }
                return flag;
            }
        },
        login: function () {
            var email = $.trim($('#email').val());
            var password = $.trim($('#password').val());
            var mailReg = /^[a-z0-9!#$%&’*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&’*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
            if (email.length === 0) {
                Tip.auto('请输入邮箱', 'error');
                $('#email').addClass('ipt-error');
                return false;
            } else {
                $('#email').removeClass('ipt-error');
            }
            if (!mailReg.test(email)) {
                Tip.auto('邮箱格式有误', 'error');
                $('#email').addClass('ipt-error');
                return false;
            } else {
                $('#email').removeClass('ipt-error');
            }
            if (password.length === 0) {
                Tip.auto('请输入密码', 'error');
                $('#password').addClass('ipt-error');
                return false;
            } else {
                $('#password').removeClass('ipt-error');
            }
            $.post('/api/login', {
                email: email,
                password: password
            }, function (data) {
                if (data['meta']) {
                    if (+data['meta']['code'] !== 200) {
                        Tip.auto(data['meta']['message'], 'error');
                    }
                } else {
                    window.location.href = urlKit.getURLParameter('redirect_url', location.search) || '/im'
                }
            }, 'json').fail(function (res) {
                Tip.auto(res.responseJSON.meta.message, 'error');
            });
        }
    };

    $(function () {

        action.listen({
            login: function (e, node, type) {
                shelper.login();
            }
        });

        Placeholder.render();

        $(document.body).keydown(function (e) {
            if (e.keyCode === 13) {
                shelper.login();
            }
        });

    });
});