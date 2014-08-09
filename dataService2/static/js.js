// JavaScript Document
function clear_search_text(){
  document.getElementById('search_text').value='';
}

function checkUserCreate(id)
{
  var flag=true;
  if(id=='userName' || id=='form')
  {    
    document.getElementById("e1").innerHTML='';
    temp = document.getElementById("userName").value;
    if(temp.length<4)
    {
      document.getElementById("e1").innerHTML='Too short';
      flag=false;
    }
    else if(repeatedTest("/regist_loginName_check/?n="+temp)!=0)
    {
      document.getElementById("e1").innerHTML='user name has been used!';
      flag=false;
    }
    else
    {
      document.getElementById("e1").innerHTML='user name right!';
    }
  }
  if(id=='userPass' || id=='form')
  {
    temp = document.getElementById("userPass").value;
    if(temp.length<6) 
    {
      document.getElementById("e2").innerHTML='Too short';
      flag=false;
    }
    else
    {
      document.getElementById("e2").innerHTML='Right';
    }
  }
  if(id=='passConfirm' || id=='form')
  {
    temp = document.getElementById("passConfirm").value;
    if(temp=='')
    {
      document.getElementById("e3").innerHTML='Too short';
    }
    else if(temp!=document.getElementById("userPass").value)
    { 
      document.getElementById("e3").innerHTML='Password does not match!';
      flag=false;
    }
    else
    {
      document.getElementById("e3").innerHTML='Right';
    }
  }
  if(id=='userEmail' || id=='form')
  {
    temp = document.getElementById("userEmail").value;
    var strReg=/^\w+((-\w+)|(\.\w+))*\@{1}\w+\.{1}\w{2,4}(\.{0,1}\w{2}){0,1}/ig;
    if(temp.search(strReg))
    {
      document.getElementById("e4").innerHTML='Email address format error!';
      flag=false;
    }
    else if(repeatedTest("/regist_email_check/?e="+temp)!=0)
    {
      document.getElementById("e4").innerHTML='Email address has been used!';
      flag=false;
    }
    else
    {
      document.getElementById("e4").innerHTML='Email address right!';
    }
  }
  return flag;
}
function checkTenantCreate(id)
{
  var flag=true;
  if(id=='tenantName' || id=='form')
  {
    document.getElementById("e1").innerHTML='';
    var temp = document.getElementById("tenantName").value;
    if(temp.length<4)
    {
      document.getElementById("e1").innerHTML='Too short';
      flag=false;
    }    
    else if(repeatedTest("/my/project/create/check/?PN="+temp)!=0)
    {
      document.getElementById("e1").innerHTML='tenant name has been used!';
      flag=false;
    }
    else
    {
      document.getElementById("e1").innerHTML='tenant name right!';
    }
  }
  return flag;
}

function checkLogin(id)
{
  var flag=true;
  if(id=='loginName'||id=='form')
  {
    document.getElementById("e1").innerHTML='';
    var temp = document.getElementById("loginName").value;
    if(temp.length<4)
    {
      document.getElementById("e1").innerHTML='Too short';
      flag=false;
    }
  }
  if(id=='pass'||id=='form')
  {
    document.getElementById("e2").innerHTML='';
    temp = document.getElementById("pass").value;
    if(temp.length<6) 
    {
      document.getElementById("e2").innerHTML='Too short';
      flag=false;
    }
  }
  return flag;
}

function checkRegist(id)
{
  var flag=true;
//  alert(id);
  if(id=='loginName'||id=='form')
  {
    document.getElementById("e1").innerHTML='';
//    alert('check loginName');
    temp = document.getElementById("loginName").value;
    if(temp.length<4)
    {
      document.getElementById("e1").innerHTML='Too short';
//      alert('check loginName short false');
      flag=false;
    }
    else if(repeatedTest("/regist_loginName_check/?n="+temp)!=0)
    {
      document.getElementById("e1").innerHTML='Login name has been used!';
//      alert('check loginName used false');
      flag=false;
    }
    else
    {
      document.getElementById("e1").innerHTML='Login name right!';
//      alert('check loginName right');
    }
  }
  if(id=='password1'||id=='form')
  {
//    alert('check password1');
    temp = document.getElementById("password1").value;
    if(temp.length<6) 
    {
      document.getElementById("e2").innerHTML='Too short';
//      alert('check password1 false');
      flag=false;
    }
    else
    {
      document.getElementById("e2").innerHTML='Right';
//      alert('check password1 right');
    }
  }
  if(id=='password2'||id=='form')
  {
//    alert('check password2');
    temp = document.getElementById("password2").value;
    if(temp=='')
    {
      document.getElementById("e3").innerHTML='Too short';
    }
    else if(temp!=document.getElementById("password1").value)
    { 
      document.getElementById("e3").innerHTML='Password does not match!';
//      alert('check password2 false');
      flag=false;
    }
    else
    {
      document.getElementById("e3").innerHTML='Right';
//      alert('check password2 right');
    }
  }
  if(id=='email'||id=='form')
  {
//    alert('check email');
    temp = document.getElementById("email").value;
    var strReg=/^\w+((-\w+)|(\.\w+))*\@{1}\w+\.{1}\w{2,4}(\.{0,1}\w{2}){0,1}/ig;
    if(temp.search(strReg))
    {
      document.getElementById("e4").innerHTML='Email address format error!';
//      alert('check email false');
      flag=false;
    }
    else if(repeatedTest("/regist_email_check/?e="+temp)!=0)
    {
      document.getElementById("e4").innerHTML='Email address has been used!';
//      alert('check Email used false');
      flag=false;
    }
    else
    {
      document.getElementById("e4").innerHTML='Email address right!';
//      alert('check Email right');
    }
  }
//  alert(flag);
  return flag;
}

function repeatedTest(url)
{
//  alert(url);
  var xmlhttp;
  if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  }
  else
  {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.open("GET",url,false);
  xmlhttp.send();
  return xmlhttp.responseText;
}

function changeLaunchSourceType()
{  
  a=document.getElementById('sourceType').value;
  if(a=='Image')
  {
    document.getElementById('sourceImage').style["display"]="";
    document.getElementById('sourceImageSelect').style["display"]="";
    document.getElementById('sourceSnapshot').style["display"]="none";
    document.getElementById('sourceSnapshotSelect').style["display"]="none";
  }
  else if(a=='Snapshot')
  {
    document.getElementById('sourceImage').style["display"]="none";
    document.getElementById('sourceImageSelect').style["display"]="none";
    document.getElementById('sourceSnapshot').style["display"]="";
    document.getElementById('sourceSnapshotSelect').style["display"]="";
  }
  else
  {
    document.getElementById('sourceImage').style["display"]="none";
    document.getElementById('sourceImageSelect').style["display"]="none";
    document.getElementById('sourceSnapshot').style["display"]="none";
    document.getElementById('sourceSnapshotSelect').style["display"]="none";
  }
}




