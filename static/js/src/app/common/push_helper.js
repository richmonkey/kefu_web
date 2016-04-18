define(function(require, exports, module) {
    var $ = require('$');
    var helper = require('./helper');
    var Tip = require('./tip');
    var cookie = require('../../lib/util/bom/cookie');

    var cache = {
        appList: {}
    };

    var phelper = {
        getAppList: function(callback, afterCallback) {
            helper.apiCall([{
                url: 'push-v1/developer/apps'
            }], function(data) {
                data = data[0]['data'];
                var gameSelectHtml = '';
                var platformSelectHtml = '';
                for(var key in data) {
                    var id = data[key]['id'];
                    var clients = data[key]['clients'];
                    cache.appList[id] = data[key];
                    cache.appList[id]['clients'] = {};
                    for(var skey in clients) {
                        var sitem = clients[skey];
                        cache.appList[id]['clients'][sitem['platform_type']] = sitem;
                    }
                    gameSelectHtml += '<option value="' + data[key]['id'] + '">' + data[key]['name'] + '</option>';
                }
                $('#game_select')[0].innerHTML = gameSelectHtml;
                var currentGame = $('#game_id').val();
                var currentPlatform = $('#platform').val();
                for(var pkey in cache.appList[currentGame]['clients']) {
                    var item = cache.appList[currentGame]['clients'][pkey];
                    if (+item['is_active'] === 1) {
                        var platform = 'Android';
                        if (+item['platform_type'] === 2) {
                            platform = 'iOS';
                        }
                        platformSelectHtml += '<option value="' + item['platform_type'] + '">' + platform + '</option>';
                    }
                }
                $('#platform_select')[0].innerHTML = platformSelectHtml;

                var gOption = $('#game_select')[0].options;
                var pOption = $('#platform_select')[0].options;
                setTimeout(function() {
                    for(var i = 0, len = gOption.length; i < len; i++){
                        if( gOption[i].value == currentGame ){
                            gOption[i].selected = true;
                            break;
                        }
                    }
                    for(var i = 0, len = pOption.length; i < len; i++){
                        if( pOption[i].value == currentPlatform ){
                            pOption[i].selected = true;
                            break;
                        }
                    }
                },100);
                phelper.listenChange(cache.appList, callback);
                afterCallback && afterCallback();
            });
        },
        listenChange: function(list, callback) {
            var gameIdNode = $('#game_select');
            var platformNode = $('#platform_select');
            gameIdNode.on('change', function() {
                var gameId = gameIdNode.val();
                var platform = platformNode.val();
                var clientId = list[gameId]['clients'][platform]['id'];
                callback && callback.call(null, gameId, platform, clientId);
            });
            platformNode.on('change', function() {
                var gameId = gameIdNode.val();
                var platform = platformNode.val();
                var clientId = list[gameId]['clients'][platform]['id'];
                callback && callback.call(null, gameId, platform, clientId);
            });
        },
        setToken: function() {
            cookie.sets({
                'FZ_L_': accessToken
            });
        }
    };

    $(function() {
        phelper.setToken();
    });

    module.exports = phelper;
});
