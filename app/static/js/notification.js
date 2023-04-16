const bs5Utils = new Bs5Utils();

var toast = '';
localStorage['lastMessage']

function notificationGet() {
    $.ajax({
        url: '/post/notification',
        method: 'GET',
        async: true,
        success: function(data) {
            if (localStorage['lastMessage'] != data) {
                localStorage['lastMessage'] = data;
                bs5Utils.Toast.show({
                    type: 'primary',
                    title: "Последняя активность",
                    content: data,
                    delay: 0,
                    dismissible: true
                });
                if (document.hidden) {
                    ion.sound({
                        sounds: [
                            {name: "notification"},
                        ],
                        path: "/static/sound/",
                        preload: true,
                        multiplay: true,
                        volume: 0.9
                    });
                    ion.sound.play("notification");
                }
            }
            setTimeout(notificationGet, 5000)
        }
    });
}
notificationGet();