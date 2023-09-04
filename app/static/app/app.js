document.addEventListener('DOMContentLoaded', function() {
    // Define colors

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: function(fetchInfo, successCallback, failureCallback) {
            // fetchInfo には start と end の日付情報が含まれています。
            var startStr = fetchInfo.startStr;
            var endStr = fetchInfo.endStr;
    
            fetch(`get-events?start=${startStr}&end=${endStr}`)
                .then(response => response.json())
                .then(events => {
                    successCallback(events);
                })
                .catch(error => {
                    failureCallback(error);
                });
        },
        dateClick: function(info) {
            // クリックされた日付を取得
            var clickedDate = info.dateStr;

            // 新しいページに遷移するURLを構築
            var newUrl = '/calendar/details/' + clickedDate;

            // 新しいページに遷移
            window.location.href = newUrl;
        }
    });

    calendar.render();
});
