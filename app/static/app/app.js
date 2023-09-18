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
        dateClick: async function(info) {
            // クリックされた日付を取得
            var clickedDate = info.dateStr;

            // サーバーサイドでShiftモデルのデータが存在するか確認
            let response = await fetch(`/calendar/check-shift-exists/${clickedDate}/`);
            let data = await response.json();

            if (data.exists) {
                // Shiftモデルのデータが存在する場合、ページ遷移を許可
                var newUrl = '/calendar/details/' + clickedDate;
                window.location.href = newUrl;
            } else {
                // Shiftモデルのデータが存在しない場合、遷移しない
                // alert("選択された日付のシフトは存在しません。");
            }
        }
    });

    calendar.render();
});







