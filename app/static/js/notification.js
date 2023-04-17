const bs5Utils = new Bs5Utils();

var toast = '';
localStorage['lastMessage']

function notificationGet() {
    $.ajax({
        url: '/post/notification',
        method: 'GET',
        async: true,
        success: function(data) {
            if (localStorage['lastMessage'] != data["id"]) {
                localStorage['lastMessage'] = data["id"];
                bs5Utils.Toast.show({
                    type: 'primary',
                    title: data["title"],
                    content: data["content"],
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