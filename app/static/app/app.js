document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
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
