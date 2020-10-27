function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function backendLookup(method, endpoint, callback, data) {
    let jsonData;
    if (data) {
        jsonData = JSON.stringify(data)
    }
    const xhr = new XMLHttpRequest()
    const url = `http://localhost:8000/api${endpoint}`
    xhr.responseType = "json"
    const csrftoken = getCookie('csrftoken');
    xhr.open(method, url)
    xhr.setRequestHeader("Content-Type", "application/json")

    if (csrftoken) {
        // bỏ dòng dưới này đi thì sẽ KO bị CORS localhost:3000 & 8000
        // xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
    }
    xhr.onload = function () {
        if (xhr.status === 403) {
            const { detail } = xhr.response
            if (detail === "Authentication credentials were not provided.") {
                window.location.href = "/login?showLoginRequired=true"
            }
        }
        callback(xhr.response, xhr.status)
    }
    xhr.onerror = function (e) {
        callback({ "message": "The request was an error" }, 400)
    }
    xhr.send(jsonData)
}
