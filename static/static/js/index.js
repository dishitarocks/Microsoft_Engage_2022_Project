const playPauseButton = document.getElementById("playerSection__songPlayer__playPauseButton");
var progressBar = document.getElementById("songProgressBar");

var togglePlay = false;
var totalSeconds = 0;
var progressBarWidth = 0.0;
var completeInterval = false;

var identity = setInterval(function () {
    if ((progressBarWidth >= 100) || (totalSeconds >= 180)) {
        togglePlay = false;
        completeInterval = true;
        playPauseButton.src = "./assets/playButtonIcon.svg";
        document.getElementById("songTimer").innerHTML = "00 : 00";
        totalSeconds = 0;
        progressBarWidth = 0.0;
        progressBar.style.width = progressBarWidth + "%";
        clearInterval(identity);
    } else if (((progressBarWidth < 100) || (totalSeconds < 180)) && (togglePlay)) {
        ++totalSeconds;
        var minute = Math.floor(totalSeconds / 60);
        var seconds = totalSeconds - (minute * 60);
        if ((minute < 10) && (seconds < 10)) {
            document.getElementById("songTimer").innerHTML = "0" + minute + " : 0" + seconds;
        } else if (minute < 10) {
            document.getElementById("songTimer").innerHTML = "0" + minute + " : " + seconds;
        } else if (seconds < 10) {
            document.getElementById("songTimer").innerHTML = minute + " : 0" + seconds;
        } else {
            document.getElementById("songTimer").innerHTML = minute + " : " + seconds;
        }

        progressBarWidth = ((100 / 180) * totalSeconds);
        progressBar.style.width = progressBarWidth + "%";
    }
}, 1000);

function playerController () {
    togglePlay = (!togglePlay);

    if (togglePlay) {
        playPauseButton.src = "./assets/pauseButtonIcon.svg";
    } else {
        playPauseButton.src = "./assets/playButtonIcon.svg";
    }

    if (completeInterval) {
        completeInterval = false;
        var identity = setInterval(function () {
            if ((progressBarWidth >= 100) || (totalSeconds >= 180)) {
                togglePlay = false;
                completeInterval = true;
                playPauseButton.src = "./assets/playButtonIcon.svg";
                document.getElementById("songTimer").innerHTML = "00 : 00";
                totalSeconds = 0;
                progressBarWidth = 0.0;
                progressBar.style.width = progressBarWidth + "%";
                clearInterval(identity);
            } else if (((progressBarWidth < 100) || (totalSeconds < 180)) && (togglePlay)) {
                ++totalSeconds;
                var minute = Math.floor(totalSeconds / 60);
                var seconds = totalSeconds - (minute * 60);
                if ((minute < 10) && (seconds < 10)) {
                    document.getElementById("songTimer").innerHTML = "0" + minute + " : 0" + seconds;
                } else if (minute < 10) {
                    document.getElementById("songTimer").innerHTML = "0" + minute + " : " + seconds;
                } else if (seconds < 10) {
                    document.getElementById("songTimer").innerHTML = minute + " : 0" + seconds;
                } else {
                    document.getElementById("songTimer").innerHTML = minute + " : " + seconds;
                }
        
                progressBarWidth = ((100 / 180) * totalSeconds);
                progressBar.style.width = progressBarWidth + "%";
            }
        }, 1000);
    }
}

