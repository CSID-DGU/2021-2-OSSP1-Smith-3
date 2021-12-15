const kor = document.querySelector('.kor-sentence');
const url = 'http://localhost:8080/tonguetwister.json';
var sentence = document.getElementById('sentence');
var nextbt = document.getElementById('next-bt');
var prevbt = document.getElementById('prev-bt');
var result = document.getElementById('speech_to_text');
var correct = document.getElementById('correct');
var meme = document.getElementById('meme');

let idx = 0;
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    kor.innerHTML = data[idx].문장;
    sentence.value = data[idx].문장;

    prevbt.disabled = 'disabled';
    nextbt.addEventListener('click', function () {
      showNext(data);
    });
    prevbt.addEventListener('click', function () {
      showPrev(data);
    });
  });

function showNext(data) {
  prevbt.disabled = false;
  if (idx < 6) {
    idx++;
    kor.innerHTML = data[idx].문장;
    sentence.value = data[idx].문장;
    result.innerHTML = '';
    correct.innerHTML = '';
    voice.value = '';
    meme.src = '';
  }
  if (idx === 5) {
    nextbt.disabled = 'disabled';
  }
}

function showPrev(data) {
  nextbt.disabled = false;
  if (idx > 0) {
    idx--;
    kor.innerHTML = data[idx].문장;
    sentence.value = data[idx].문장;
    result.innerHTML = '';
    correct.innerHTML = '';
    voice.value = '';
    meme.src = '';
  }

  if (idx === 0) {
    prevbt.disabled = 'disabled';
  }
}
