let running = false;
function refresh(password){
  if (!running) {
    running = true;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, true); // false for synchronous request
    xmlHttp.send( null );
    xmlHttp.onload = function (e) {
      if (xmlHttp.readyState === 4) {
        if (xmlHttp.status === 200) {
          var whole_response = xmlHttp.responseText;
          var span_response = /<span.*?>([\s\S]*)<\/span>/.exec(whole_response)[1];
          var key = btoa(md5(password));
          var secret = new fernet.Secret(key);
          var token = new fernet.Token({
            secret: secret,
            token: span_response,
            ttl: 0
          })
          decoded_response = token.decode();
          ReplaceContent(decoded_response);
        }
      }
    }
    running = false;
  }
  setTimeout(function() {
    refresh(password);
  }, 1000);
}
//document.getElementById('table_container').innerHTML
