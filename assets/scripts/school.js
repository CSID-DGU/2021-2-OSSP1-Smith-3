const kor = document.querySelector('.kor-sentence');
const situation = document.querySelector('.situation');
const eng = document.querySelector('.eng-description');
const url = 'http://localhost:8080/school.json';
var sentence = document.getElementById("sentence");
var nextbt = document.getElementById('next-bt');
var prevbt = document.getElementById('prev-bt');

let idx = 0;
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    kor.innerHTML = data[idx].한국어;
    situation.innerHTML = data[idx].소분류;
    eng.innerHTML = data[idx].영어;
    sentence.value = data[idx].한국어;

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
  if (idx < 10) {
    idx++;
    kor.innerHTML = data[idx].한국어;
    situation.innerHTML = data[idx].소분류;
    eng.innerHTML = data[idx].영어;
    sentence.value = data[idx].한국어;
  }
  if (idx === 9) {
    nextbt.disabled = 'disabled';
  }
}

function showPrev(data) {
  nextbt.disabled = false;
  if (idx > 0) {
    idx--;
    kor.innerHTML = data[idx].한국어;
    situation.innerHTML = data[idx].소분류;
    eng.innerHTML = data[idx].영어;
    sentence.value = data[idx].한국어;
  }

  if (idx === 0) {
    prevbt.disabled = 'disabled';
  }
}
