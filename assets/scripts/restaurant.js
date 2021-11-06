const kor = document.querySelector('.kor-sentence');
const situation = document.querySelector('.situation');
const eng = document.querySelector('.eng-description');
const url = 'http://localhost:8080/restaurant.json';

let idx = 0;
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    kor.innerHTML = data[idx].한국어;
    situation.innerHTML = data[idx].소분류;
    eng.innerHTML = data[idx].영어;
  });
