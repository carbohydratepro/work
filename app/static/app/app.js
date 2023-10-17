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


// ①Django側にPOST送信する際に記述する"お決まりのコード"
const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                return decodeURIComponent(value);
            }
        }
    }
};
const csrftoken = getCookie('csrftoken');

// ②選択されたセレクトメニュー情報をDjango側にPOST送信する
document.addEventListener('DOMContentLoaded', (event) => {
    const categoryList = document.getElementById('category_select');
    if (categoryList) {
        categoryList.addEventListener('change', handleCategoryChange);
    }
});
function handleCategoryChange(event) {
    // セレクトメニュー内の要素を取得する
    const categoryList = document.getElementById('category_select');
    const selectedCategory = categoryList.value;
    // 非同期処理を記述する

    async function send_view_type() {
        const url = '/calendar/update_user_view_type';
        let res = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                    'X-CSRFToken': csrftoken,
                },
                body: `view_type=${selectedCategory}`
            });
    
        // レスポンスをJSONとして解析
        let data = await res.json();
    
        // statusが'ok'の場合、display-calendarにリダイレクト
        if (data.status === 'ok') {
            window.location.href = "/calendar/";
        } else {
            // エラー処理（必要に応じて）
            console.error("Error updating view type:", data.errors);
        }
    }
    
    // 定義した関数を実行する
    send_view_type();
};
