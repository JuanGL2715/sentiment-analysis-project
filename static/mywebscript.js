let RunSentimentAnalysis = ()=>{
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const encodedText = encodeURIComponent(textToAnalyze);

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("system_response").innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("GET", "emotionDetector?textToAnalyze=" + encodedText, true);
    xhttp.send();
}
