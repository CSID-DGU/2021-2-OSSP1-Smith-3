const kor = document.querySelector('.kor-sentence');
const eng = document.querySelector('.eng-description');
const url = 'http://localhost:8080/colloquial.json';
var nextbt = document.getElementById('next-bt');
var prevbt = document.getElementById('prev-bt');
var word = document.getElementById('word');
var short = document.getElementById('short-description');
var long = document.getElementById('long-description');

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
  if (idx < 20) {
    idx++;
    editHtml(data);
  }
  if (idx === 19) {
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
  word.innerHTML = data[idx].단어;
  short.innerHTML = data[idx].설명;
  long.innerHTML = data[idx].긴설명;
}
