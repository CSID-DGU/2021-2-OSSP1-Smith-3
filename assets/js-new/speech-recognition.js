
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// 인스턴스 생성
const recognition = new SpeechRecognition();
let is_mic_on = false;

// true면 음절을 연속적으로 인식하나 false면 한 음절만 기록함
recognition.interimResults = true;
// 값이 없으면 HTML의 <html lang="en">을 참고합니다. ko-KR, en-US
recognition.lang = "ko-KR";
// true means continuous, and false means not continuous (single result each time.)
// true면 음성 인식이 안 끝나고 계속됩니다.
recognition.continuous = true;
// 숫자가 작을수록 발음대로 적고, 크면 문장의 적합도에 따라 알맞은 단어로 대체합니다.
// maxAlternatives가 크면 이상한 단어도 문장에 적합하게 알아서 수정합니다.
// 기본은 10000이었다.
recognition.maxAlternatives = 10000;

const speech_to_text = document.getElementById("speech_to_text");
const voice = document.getElementById("voice");

let speechToText = "";

recognition.addEventListener("result", (e) => {

    let interimTranscript = "";
    for (let i = e.resultIndex, len = e.results.length; i < len; i++) {
        let transcript = e.results[i][0].transcript;
        console.log(transcript);
        if (e.results[i].isFinal) {
            speechToText += transcript;
        } else {
            interimTranscript += transcript;
        }
    }
    speech_to_text.innerHTML = speechToText + interimTranscript;
});

const btn_mic_toggle = document.getElementById("btn_mic_toggle");
btn_mic_toggle.addEventListener("click", () => {
    // 음성 인식 켜져 있으면
    if (is_mic_on) {
        btn_mic_toggle.textContent = "연습 시작";
        is_mic_on = false;
        recognition.abort();
        voice.value = speech_to_text.innerHTML;
    }
    // 꺼져 있으면
    else {
        btn_mic_toggle.textContent = "종료";
        speechToText = "";  // 연습 새로 시작할 때 리프레시
        is_mic_on = true;
        recognition.start();
    }
});