define(function (require, exports, module) {
    var Pagination = require('../../lib/cmp/pagination/pagination');
    module.exports = Pagination.extend({
        attrs: {
            totalName: 'pagination.rows_found',
            showPN: false
        },
        view: function (flag) {
            var html = '<span class="item">共<em>' + this.get('total') + '</em>个</span>';
            html += '<span class="item">第<em>' + this.get('current') + '/' + Math.ceil(this.get('total') / this.get('size')) + '</em>页</span>';
            html += '<a href="#" data-action="prev" class="prev">&lt;</a>';
            html += '<a href="#" data-action="next" class="next">&gt;</a>';

            this.element.html(html);
            this.reflow();
            this.ajax();
            return this;
        }
    });
});