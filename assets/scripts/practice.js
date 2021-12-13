var sentence = document.getElementById('sentence');
const user_text = document.getElementById('user_text');
var kor = document.querySelector('.kor-sentence');

user_text.addEventListener('click', function() {
  sentence.value = kor.value;
});









