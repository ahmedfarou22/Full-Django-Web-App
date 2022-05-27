var form = document.getElementById('validate');
var user_name = document.getElementsByName('user-name')[0];
var email = document.getElementsByName('email')[0];
var subject = document.getElementsByName('subject')[0];
var message = document.getElementsByName('message')[0];

// =============== IF values were non-empty; Notify php to catch these values ===============

var name_v = document.getElementsByName('name-v')[0] ;
var email_v = document.getElementsByName('email-v')[0] ;
var subject_v = document.getElementsByName('subject-v')[0] ;
var message_v = document.getElementsByName('message-v')[0] ;

// submit event
form.addEventListener('submit', function(event){

  var nameV = user_name.value.trim() ;
  var emailV = email.value.trim() ;
  var subjectV = subject.value.trim() ;
  var messageV = message.value.trim() ;

  checkEmpty(user_name,nameV,"You cannot leave the name field empty!",name_v,event) ;
  checkEmpty(email,emailV,"You cannot leave the email field empty!",email_v,event) ;
  checkEmpty(subject,subjectV,"You cannot leave the subject field empty!",subject_v,event) ;
  checkEmpty(message,messageV,"You cannot leave the message field empty!",message_v,event) ;



});

function checkEmpty(elem,elemValue,msg,flag,event){

    if (elemValue == "") {
      event.preventDefault() ;
      addRedOutline(elem);
      ShowErrorDiv(elem,msg);
      makeInvalid(flag) ;
    } else {
        removeOutline(elem) ;
        hideErrorDiv(elem) ;
        makeValid(flag);

      }
}




// =============== Functions to execute if values wrre empty=================
function addRedOutline(elem){// function def --> parameter
  elem.classList.add('input_errors')
}

function ShowErrorDiv(elem,msg){
  var div = elem.nextElementSibling ;
  div.firstElementChild.innerText = msg ;
}

function makeInvalid(elem){
  elem.value = "" ;
}

// =============== Functions to execute if values wrre nonempty=================

function removeOutline(elem){// function def --> parameter
  elem.classList.remove('input_errors')
}

function hideErrorDiv(elem){
  var div = elem.nextElementSibling ;
  div.firstElementChild.innerText = "" ;
}

function makeValid(elem){
  elem.value = "valid" ;
}
