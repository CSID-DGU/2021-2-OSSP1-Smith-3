const kor = document.querySelector('.kor-sentence');
const url = 'http://localhost:8080/tonguetwister.json';
var nextbt = document.getElementById('next-bt');
var prevbt = document.getElementById('prev-bt');

let idx = 0;
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    kor.innerHTML = data[idx].문장;

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
    kor.innerHTML = data[idx].문장;
  }
  if (idx === 9) {
    nextbt.disabled = 'disabled';
  }
}

function showPrev(data) {
  nextbt.disabled = false;
  if (idx > 0) {
    idx--;
    kor.innerHTML = data[idx].문장;
  }

  if (idx === 0) {
    prevbt.disabled = 'disabled';
  }
}