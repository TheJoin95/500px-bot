<?php
session_start();

ini_set('display_errors', 1);
error_reporting(E_ALL ^ (E_NOTICE | E_WARNING | E_DEPRECATED));
define('DIR_WEB', dirname(__FILE__));

// require_once('./config/config.inc.php');
require_once('./vendor/autoload.php');
require_once(DIR_WEB.'/lib/functions.php');

mb_internal_encoding('UTF-8');

$config_file_path = './config/config.inc.php';

$hybridauth = new Hybrid_Auth( $config_file_path );

$auth = $hybridauth->authenticate('px500');

$access_tokens = $auth->getAccessToken();

$query = http_build_query(
          array(
              'consumer_key' => CONSUMER_KEY,
              'feature' => 'popular',
              'sort' => 'times_viewed',
              'sort_direction' => 'desc',
              'rpp' => 100
            )
        );
        // TODO: pagination, search by editors and other, search tags related at comment/photo
        // cron, auto oauth for multiple usrs.
print_r(apiCall('https://api.500px.com/v1/photos?'.$query));

// $router = new AltoRouter();
// // EXTERNAL APPLICATIONS
// $router->map('GET','/', array('controller' => 'default', 'action' => 'list','view' =>'default'),'list');
// // match current request
// $match = $router->match();
// var_dump($match);
// exit();
// // Interpreta e assegna Controll er e View
// $controller =(isset($match['target']['controller']))?$match['target']['controller']:'default';
// $action =(isset($match['target']['action']))?$match['target']['action']:'default';
// $view =(isset($match['target']['view']))?$match['target']['view']:'default';
// $parameters=$match['params'];
//
// include DIR_WEB . '/controllers/' . $controller.".php";

?>
