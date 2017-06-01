/*function readFile(e) {
	var file = e.target.files[0];
	if(!file) {
		return;
	}
	var reader  = new FileReader();
	reader.onload = function(e){
		var contents = e.target.result;
		displayContents(contents);
	};
}
function displayContents(contents){
	var element = document.getElementById('file-content');
	element.innerHTML = contents;
}
document.getElementById('file-input').addEventListener('change', readSingleFile, false);
*/
var playerLeft;
var playerRight;
var scoreLeft;
var scoreRight;
var round;
var commentary1;
var commentary2;

var xmlDoc;
var xhr = new XMLHttpRequest();

var animating = false;
var doUpdate = false;

function init() {
	xhr.overrideMimeType('text/xml');
	$('#player1').html('');
	$('#player2').html('');
	$('#score1').html('');
	$('#score2').html('');
	$('#round').html('');
	$('#commentary1').html('');
	$('#commentary2').html('');
	$('#board').tween({
		top:{
			start:'-100',
			stop:'0',
			units:'px',
			time:0,
			duration:0.8,
			effect:'easeOut'
		}
	});
	$.play();
}