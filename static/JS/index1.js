function updateProgress(progress) {
    var progressBar = document.getElementById('progress');
    progressBar.style.width = progress + '%';
    progressBar.innerHTML = progress + '%';
}

function simulateProgress() {
    var progress = 0;
    var interval = setInterval(function() {
        progress += 0.083;
        updateProgress( Math.round(progress * 100) / 100);
        if (progress >= 99.99) {
            clearInterval(interval);
        }
    }, 50); // 每0.05秒更新一次進度
}

function startProgress() {
    simulateProgress(); // 开始模擬進度
}

