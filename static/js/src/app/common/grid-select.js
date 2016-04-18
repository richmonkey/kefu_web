define(function (require, exports, module) {
    var $ = require('$');
    var Dialog = require('../../lib/cmp/dialog/confirm-box');

    var actions = {
        selectAll: function (e, node, key) {
            $('#datagrid :checkbox').each(function () {
                var status = node[0].checked;
                this.checked = status;
                $(this).closest('li[data-id]')[status ? 'addClass' : 'removeClass']('highlight');
            });
        },
        selectSingle: function (e, node, key) {
            var all = $('#select_all')[0];
            var li = node.closest('li[data-id]');
            if (!node[0].checked) {
                all.checked = false;
                li.removeClass('highlight');
            } else {
                var flag = true;
                $('#datagrid :checkbox').each(function () {
                    var status = this.checked;
                    if (!status) {
                        flag = false;
                        return;
                    }
                });
                li.addClass('highlight');
                all.checked = flag;
            }
        },
        del: function (e, node, key, action) {
            var list = $('#datagrid :checked');
            var ids = list.map(function (i, el) {
                return $(el).closest('li[data-id]').attr('data-id');
            }).get().join(',');
            
            if (ids) {
                Dialog.confirm({
                    title: '确认删除',
                    content: '确认删除选中的数据?',
                    buttons: [
                        {
                            text: '确定',
                            action: 'confirm'
                        },
                        {
                            text: '取消'
                        }
                    ]
                }).on('confirm', function () {
                    action.call(this, ids);
                });
            }
        }
    };

    module.exports = actions;
});