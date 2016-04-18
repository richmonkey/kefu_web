define(function (require, exports, module) {
    Tip = require('../common/tip').self
        , $ = require('$')
        , helper = require('helper')
        , Validate = require('../../mod/validate');

    function makePlatformExpandable(context) {
        var platformGroup = context.find('.android-extra, .ios-extra');
        $.each(['ios', 'android'], function (idx, platformName) {
            var platform = context.find('.' + platformName + '-extra')
                , item = $('.platform-item.' + platformName);

            item.click(function (e) {
                if (item.hasClass('checked') && item.hasClass('is-select')) {
                    return false
                }
                var itemIsChecked = item.hasClass('checked');
                item[itemIsChecked ? 'removeClass' : 'addClass']('checked');
                platform[itemIsChecked ? 'hide' : 'show']()
            })
        });

        $('#xinge_push_type').change(function () {
            $('#form_xinge').css('display', this.checked ? 'block' : 'none');
        });

        $('#mi_push_type').change(function () {
            $('#form_mi').css('display', this.checked ? 'block' : 'none');
        });

        $('#hw_push_type').change(function () {
            $('#form_hw').css('display', this.checked ? 'block' : 'none');
        });

        $('#gcm_push_type').change(function () {
            $('#form_gcm').css('display', this.checked ? 'block' : 'none');
        });

    }

    function initGameForm(form, options) {
        form.on('submit', function (e) {
            if (form.find('.checked').length === 0) {
                Tip.auto('至少要勾选一个平台', 'error');
                return false;
            }

            var clientAndroidNode = form.find('.android');
            var clientAndroidIdentityNode = form.find('.client-android-identity');
            var clientIosNode = form.find('.ios');
            var clientIosIdentityNode = form.find('.client-ios-identity');
            var identity = $.trim(clientAndroidIdentityNode.val());

            if (clientAndroidNode.hasClass('checked')) {
                if (identity.length === 0) {
                    Tip.auto('请填写包名', 'error');
                    clientAndroidIdentityNode.addClass('ipt-error');
                    return false;
                } else {
                    clientAndroidIdentityNode.removeClass('ipt-error');
                }
            }

            identity = $.trim(clientIosIdentityNode.val());

            if (clientIosNode.hasClass('checked')) {
                if (identity.length === 0) {
                    Tip.auto('请填写BundleID', 'error');
                    clientIosIdentityNode.addClass('ipt-error');
                    return false;
                } else {
                    clientIosIdentityNode.removeClass('ipt-error');
                }
            }

            var developApns = form.find('#develop_apns');
            if (developApns.val() && developApns.val().split('.').pop() != 'p12') {
                Tip.auto('请上传 `.p12` 格式的文件', 'error');
                developApns.addClass('ipt-error');
                return false;
            }

            var productionApns = form.find('#production_apns');
            if (productionApns.val() && productionApns.val().split('.').pop() != 'p12') {
                Tip.auto('请上传 `.p12` 格式的文件', 'error');
                productionApns.addClass('ipt-error');
                return false;
            }

            return true;
        })
    }

    module.exports = function (form, options) {
        makePlatformExpandable(form);

        initGameForm(form, options);
    }
});
