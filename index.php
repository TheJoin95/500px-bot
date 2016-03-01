<?php
session_start();

define('CONSUMER_KEY', 'bxuX6lD1wdvOy7PjEJz3mmr994j9Ul0mByZ3IG7N');
define('CONSUMER_SECRET', 'F8pgNdJbj9jGvDp5qp0Q105Mbw8jcX0ebjc9okag');

ini_set('display_errors', 1);
error_reporting(E_ALL ^ (E_NOTICE | E_WARNING | E_DEPRECATED));
define('DIR_WEB', dirname(__FILE__));

// require_once('./config/config.inc.php');
require_once('./vendor/autoload.php');
require_once(DIR_WEB.'/lib/functions.php');

mb_internal_encoding('UTF-8');

$config_file_path = './config/config.inc.php';

// $router = new AltoRouter();
// // $router->setBasePath(DIR_WEB);
// // EXTERNAL APPLICATIONS
// $router->map('GET','/list', array('controller' => 'default', 'action' => 'list','view' =>'default'),'list');
// // match current request
// $match = $router->match();
// echo $_SERVER['DOCUMENT_ROOT'];
// print_r($match);
// exit();

$hybridauth = new Hybrid_Auth( $config_file_path );
$auth = $hybridauth->authenticate('px500');
try {
  $user = $auth->getUserProfile();
  $user->access_tokens = $auth->getAccessToken();
  $_SESSION['user'] = (array)$user;
} catch (Exception $e) {
  print_r($e);
}

if(isset($_SESSION['user']['access_tokens'])) {
  include DIR_WEB . '/controllers/default.php';
}

// // Interpreta e assegna Controll er e View
// $controller =(isset($match['target']['controller']))?$match['target']['controller']:'default';
// $action =(isset($match['target']['action']))?$match['target']['action']:'default';
// $view =(isset($match['target']['view']))?$match['target']['view']:'default';
// $parameters=$match['params'];
//
// include DIR_WEB . '/controllers/' . $controller.".php";

?>
