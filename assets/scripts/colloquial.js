const kor = document.querySelector('.kor-sentence');
const eng = document.querySelector('.eng-description');
const url = 'http://localhost:8080/colloquial.json';
var sentence = document.getElementById('sentence');
var nextbt = document.getElementById('next-bt');
var prevbt = document.getElementById('prev-bt');
var word1 = document.getElementById('word1');
var word2 = document.getElementById('word2');
var short = document.getElementById('short-description');
var long = document.getElementById('long-description');
var result = document.getElementById('speech_to_text');
var correct = document.getElementById('correct');

let idx = 0;
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    editHtml(data);

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
  if (idx < 16) {
    idx++;
    editHtml(data);
    result.innerHTML = '';
    correct.innerHTML = '';
    voice.value = '';
  }
  if (idx === 15) {
    nextbt.disabled = 'disabled';
  }
}

function showPrev(data) {
  nextbt.disabled = false;
  if (idx > 0) {
    idx--;
    editHtml(data);
  }

  if (idx === 0) {
    prevbt.disabled = 'disabled';
  }
}

function editHtml(data) {
  kor.innerHTML = data[idx].예문;
  eng.innerHTML = data[idx].예문번역;
  word1.innerHTML = data[idx].단어;
  word2.innerHTML = data[idx].단어;
  short.innerHTML = data[idx].설명;
  long.innerHTML = data[idx].긴설명;
  sentence.value = data[idx].예문;
}
