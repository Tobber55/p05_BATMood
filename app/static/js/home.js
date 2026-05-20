const myLink = document.getElementById('my-link');
const changeButton = document.getElementById('change-btn');

changeButton.addEventListener('click', () => {
  // Use setAttribute to change the 'href' attribute
  myLink.setAttribute('href', '/imposter');
});

/*
logic:
create button attached to defaultpfp
defaultpfp checks session to see if logged in
if logged in, go to profile html
if not, go to login html
logout will be shown in profile html
*/


// https://tutorialreference.com/javascript/examples/faq/javascript-how-to-change-href-attribute-of-a-link-tag
