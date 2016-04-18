define(function (require, exports, module) {
    var $ = require('$');
    var tip = require('./tip').common;
    var Pjax = require('../../lib/util/pjax');

    $(function () {
        var doc = $(document);
        doc.ajaxSend(function (e, xhr, settings) { // 开始一个ajax请求
            tip.delay('正在载入数据...');
            // console.log('send:', settings.type, '-->', settings.url);
        }).ajaxStart(function () { // 开始一个ajax请求且无其他ajax请求过程

        }).ajaxSuccess(function (e, xhr, settings) { // 一个ajax成功
            tip.hide();
            // console.log('success', settings.url);
        }).ajaxError(function (e, xhr, settings, err) { // 一个ajax失败
            // todo: 根据具体错误类型提示
            // console.log('error', settings.url, err, xhr);
            if (err !== 'abort') {
                var msg = xhr && xhr.responseJSON && xhr.responseJSON.meta && xhr.responseJSON.meta.message;
                tip.auto(msg || err, 'error');
            }
        }).ajaxComplete(function (e, xhr, settings) { // 一个ajax完成

        }).ajaxStop(function () { // 所有ajax完成

        });

        if ($.support.pjax) {
            doc.on('click', 'a[data-pjax]', function (e) {
                $.pjax.click(e, {container: $(this).attr('data-pjax')});
            }).on('submit', 'form[data-pjax]', function (e) {
                $.pjax.submit(e, $(this).attr('data-pjax'));
            });
        }
    });

    module.exports = $.ajax;
});