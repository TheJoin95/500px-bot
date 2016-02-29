<?php

function apiCall($url, $params=array(),$isPost=false){
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_POST, $isPost);

  if(count($params) > 0 && $isPost) {
      curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
  }
    
  curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)');
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  $response = curl_exec($ch);
  curl_close($ch);

  $JSONresponse = json_decode($response, true);
  return ($response !== false) ? $JSONresponse : $response;

}

?>
