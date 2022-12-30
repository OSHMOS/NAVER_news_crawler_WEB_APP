const submit = document.querySelector('#submit');
const load = document.querySelector('#loading');

function onLoading (){
  submit.className += ' hidden';
  load.classList.remove('hidden');
};