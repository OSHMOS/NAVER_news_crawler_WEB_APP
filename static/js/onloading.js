const btn = document.querySelector('#btn');
const load = document.querySelector('#loading');

function req (){
  window.onsubmit = onLoading;
};

function onLoading (){
  btn.className += ' hidden';
  load.classList.remove('hidden');
};