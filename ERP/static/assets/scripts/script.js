// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();

/* Passar o mouse por cima do menu e ver as opções*/
$(document).ready(function() {
  $('.visu').hover(
    function () {
      $('.subvisu').css({"display":"block"});
    }, 
    function () {
      $('.subvisu').css({"display":"none"});
    }
  );  
  $('.subvisu').hover(
  function () {
    $('.subvisu').css({"display":"block"});
  }, 
  function () {
    $('.subvisu').css({"display":"none"});
  }
  );
  $('.visu2').hover(
    function () {
      $('.subvisu2').css({"display":"block"});
    }, 
    function () {
      $('.subvisu2').css({"display":"none"});
    }
  );  
  $('.subvisu2').hover(
  function () {
    $('.subvisu2').css({"display":"block"});
  }, 
  function () {
    $('.subvisu2').css({"display":"none"});
  }
  );
});

/*Acrescentar div com base no input select*/
function clicou(){
  var divPai = $('#res');
  //var res = document.getElementById('res')
  res.append("<div class='textoBox' style='display:table-cell;width:99%'>div texto</div>");
}

(function(){
var divPai = $('.Linha');
var btnCriar = $('#criarLinha');
btnCriar.click(function(){
  divPai.append("<div class='textoBox' style='display:table-cell;width:99%'>div texto</div>");
  divPai.append("<div class='mostraBox' style='display:table-cell;width:20px;vertical-align:middle;'>div mostra</div>");
  divPai.append("<div class='mudarBox' style='display:table-cell;width:20px;vertical-align:middle;'>div mudar</div>");
  divPai.append("<div class='excluirBox' style='display:table-cell;width:20px;vertical-align:middle;'>div excluir</div>");
});
  
})()

/*Acrescentar div do select tipo pessoa */ 
$(function(){
  $("#selectServicos").change(function(){
      var valor = $(this).val();
      var valor1 = Number(valor)
      var lerDiv = document.getElementById("divCampos")
      var display = document.getElementById("divCampos").style.display;
      document.getElementById("divCampos").style.display = 'inline';
      if(valor1 == 1){
        lerDiv.innerHTML = '<div class="label-float"><input type="text" class="form-control mr-4"  name="validationTooltip15" id="validationTooltip15" placeholder=" " required/><label for="validationTooltip15">CPF</label><div class="invalid-tooltip">Insira o CPF</div></div>'
      }else if(valor1 == 2){
        lerDiv.innerHTML = '<div class="label-float"><input type="text" class="form-control mr-4" name="validationTooltip16" id="validationTooltip016" placeholder=" " required/><label for="validationTooltip16">CNPJ</label><div class="invalid-tooltip">Insira o CNPJ</div></div>'
      }else if(valor1 == 3){
        lerDiv.innerHTML = '<div class="label-float"><input type="text" class="form-control mr-4" name="validationTooltip17" id="validationTooltip17" placeholder=" " required/><label for="validationTooltip17">UF</label><div class="invalid-tooltip">Insira a UF</div></div>'
      }else{
        document.getElementById("divCampos").style.display = 'none';
        teste.innerHTML = " "
      }
  });
});

/*Mascarar valores dos inputs*/
function mascara(t, mask){
  var i = t.value.length;
 
  var saida = mask.substring(2,1);
  var texto = mask.substring(i);
  if (texto.substring(0,1) != saida){
    t.value += texto.substring(0,1);
  }
}

/*Ampliar e diminuir imagens*/ 
function bigImg(x)
{
  x.style.height="200px";
  x.style.width="200px";
}

function normalImg(x)
{
  x.style.height="100px";
  x.style.width="100px";
}

/*Bloquear lado direito do mouse*/
if (document.addEventListener) {
  document.addEventListener("contextmenu", function(e) {
      e.preventDefault();
      return false;
  });
} else { //Versões antigas do IE
  document.attachEvent("oncontextmenu", function(e) {
      e = e || window.event;
      e.returnValue = false;
      return false;
  });
}

if (document.addEventListener) {
  document.addEventListener("keydown", bloquearSource);
} else { //Versões antigas do IE
  document.attachEvent("onkeydown", bloquearSource);
}

/*Bloquear ctrl + U e ctrl + S */
function bloquearSource(e) {
  e = e || window.event;

  var code = e.which || e.keyCode;

  if (
      e.ctrlKey &&
      (code == 83 || code == 85) //83 = S, 85 = U
  ) {
      if (e.preventDefault) {
          e.preventDefault();
      } else {
          e.returnValue = false;
      }

      return false;
  }
}

function somenteNumeros(num) {
  var er = /[^0-9.]/;
  er.lastIndex = 0;
  var campo = num;
  if (er.test(campo.value)) {
    campo.value = "";
  }
}

function fazerLogin(){
    var lerLogin = document.getElementById('validationTooltip02')

    if(lerLogin.value.length == 0){
      document.getElementById('alertaLogin').style.display = 'inline'
    }
}
function clicou(){
  document.getElementById('alertaLogin').style.display = 'none'
}

document.getElementById('olho').addEventListener('mousedown', function() {
  document.getElementById('pass').type = 'text';
});

document.getElementById('olho').addEventListener('mouseup', function() {
  document.getElementById('pass').type = 'password';
});

// Para que o password não fique exposto apos mover a imagem.
document.getElementById('olho').addEventListener('mousemove', function() {
  document.getElementById('pass').type = 'password';
});