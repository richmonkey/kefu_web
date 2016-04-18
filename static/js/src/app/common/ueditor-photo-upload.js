define(function (require, exports, module) {
    var $ = require('$');

    var UE = require('editor');
    var Upload = require('../../lib/util/dom/upload/upload');
    var tpl = require('./tpl/content');

    UE.addPlugin({
        name: 'photo',
        description: '插入图片',
        dialog: {
            content: tpl.render({
                supportDraggable: Upload.isSupportHTML5Upload
            })
        },
        execCommand: function (cmdName, dialog) {
            dialog.open();
            var node = $(dialog.getDom());
            var that = this;

            var resultNode = node.find('.upload-result').eq(0);
            var form = $('#update_form');
            var progressNode;
            var u = new Upload({
                url: '/pictures/' + form.find('[name=game_id]').val() + '/' + form.find('[name=id]').val(),
                swf: '/public/swf/swfupload.swf',
                node: node.find(':file').eq(0),
                container: node,
                type: '*.jpg; *.gif; *.png; *.jpeg',
                maxSize: '5MB', // 文件大小限制
                maxCount: 1, // 文件数量限制，-1不限制
                multi: false, // 是否允许多文件上传
                max: 2,
                fileName: 'Filedata',
                data: {},
                text: '上传'
            }).on('overSizeLimit',function (size, file) { // 超过大小限制
                    alert('超过' + size + '大小限制');
                }).on('zeroSize',function (file) { // 空文件
                    alert('空文件');
                }).on('overCountLimit',function (limit) { // 超过数量限制
                    alert('超过数量限制：' + limit + '，不能再增加文件');
                }).on('notAllowType',function (file) { // 不允许文件类型
                    alert('只允许上传图片');
                }).on('successAdd',function (file, files) { // 成功加入队列
                    node.find('.upload-result').html('正在上传...<span class="progress">0%</span>');
                    u.upload();
                    progressNode = node.find('.progress').eq(0);
                }).on('errorAdd',function (file, files) { // 加入队列失败
                    alert('添加图片失败');
                }).on('progress',function (file, loaded, total) { // 上传进度
                    progressNode.text((loaded / total * 100).toFixed(2) + '%');
                }).on('success',function (file, data) { // 上传成功
                    that.execCommand("insertImage", [
                        {
                            src: '/pictures?path=' + data.data.path
                        }
                    ]);
                    dialog.close();
                    u = null;
                }).on('error',function (file, data) { // 文件上传失败时或者被终止时触发，引起的可能性有：上传地址不存在/主动终止
                    alert('上传文件失败' + '\n' + data)
                }).on('complete',function (file) { // 上传文件完成，无论失败成功
                }).on('finish',function (file) { // 上传所有文件完成
                }).on('reset',function () {
                    resultNode.html('');
                }).on('abort',function (file, index) {
                }).on('remove',function (file, index) {
                    $('#upfile_' + index).remove();
                }).on('drop', function (files) {
                    this.add(files);
                });
            node.find('[data-action=close]').click(function (e, node, type) {
                dialog.close();
            });
        }
    });
});