const btn = document.getElementById("summarise");
btn.addEventListener("click", function () {
    btn.disabled = true;
    btn.innerHTML = "Summarising...";
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        var url = tabs[0].url;
        var xhr = new XMLHttpRequest();
        // if the following url doesn't work, you can use the flask backend locally
        xhr.open("GET", "https://yt-summary-sizd.onrender.com/summary?url=" + url, true);
        // xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url, true);
        xhr.onload = function () {
            var text = xhr.responseText;
            const p = document.getElementById("output");
            p.innerHTML = text;
            btn.disabled = false;
            btn.innerHTML = "Summarise";
        }
        xhr.send();
    });
});