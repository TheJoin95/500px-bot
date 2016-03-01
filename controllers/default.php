<?php
echo '<pre>';
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

$listing = apiCall('https://api.500px.com/v1/photos?'.$query);
// print_r($listing);
// foreach ($listing['photos'] as $key => $item) {
//   print_r($item); exit();
// }

echo '</pre>';

$sign_method = 'HMAC-SHA1';
$mt = microtime();
$rand = mt_rand();
$nonce = md5($mt.$rand);
$time = time();

$query = array(
    "oauth_consumer_key" => CONSUMER_KEY,
    "oauth_signature_method"=>$sign_method,
    "oauth_signature"=>$CONSUMER_SECRET,
    "oauth_timestamp"=>$time,
    "oauth_nonce"=>$nonce,
    "oauth_version" =>"1.0"
  );
var_dump(apiCall('https://api.500px.com/v1/photos/142020435/comments', $query, true));


// use NlpTools\Tokenizers\WhitespaceTokenizer;
// use NlpTools\Models\FeatureBasedNB;
// use NlpTools\Documents\TrainingSet;
// use NlpTools\Documents\TokensDocument;
// use NlpTools\FeatureFactories\DataAsFeatures;
// use NlpTools\Classifiers\MultinomialNBClassifier;
//
// // ---------- Data ----------------
// // data is taken from http://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection
// // we use a part for training
// $training = array(
//     array('ham','Go until jurong point, crazy.. Available only in bugis n great world la e buffet... Cine there got amore wat...'),
//     array('ham','Fine if that\'s the way u feel. That\'s the way its gota b'),
//     array('spam','England v Macedonia - dont miss the goals/team news. Txt ur national team to 87077 eg ENGLAND to 87077 Try:WALES, SCOTLAND 4txt/ú1.20 POBOXox36504W45WQ 16+')
// );
// // and another for evaluating
// $testing = array(
//     array('ham','I\'ve been searching for the right words to thank you for this breather. I promise i wont take your help for granted and will fulfil my promise. You have been wonderful and a blessing at all times.'),
//     array('ham','I HAVE A DATE ON SUNDAY WITH WILL!!'),
//     array('spam','XXXMobileMovieClub: To use your credit, click the WAP link in the next txt message or click here>> http://wap. xxxmobilemovieclub.com?n=QJKGIGHJJGCBL')
// );
//
// $tset = new TrainingSet(); // will hold the training documents
// $tok = new WhitespaceTokenizer(); // will split into tokens
// $ff = new DataAsFeatures(); // see features in documentation
//
// // ---------- Training ----------------
// foreach ($training as $d)
// {
//     $tset->addDocument(
//         $d[0], // class
//         new TokensDocument(
//             $tok->tokenize($d[1]) // The actual document
//         )
//     );
// }
//
// $model = new FeatureBasedNB(); // train a Naive Bayes model
// $model->train($ff,$tset);
//
//
// // ---------- Classification ----------------
// $cls = new MultinomialNBClassifier($ff,$model);
// $correct = 0;
// foreach ($testing as $d)
// {
//     // predict if it is spam or ham
//     $prediction = $cls->classify(
//         array('ham','spam'), // all possible classes
//         new TokensDocument(
//             $tok->tokenize($d[1]) // The document
//         )
//     );
//     if ($prediction==$d[0])
//         $correct ++;
// }
// printf("Accuracy: %.2f\n", 100*$correct / count($testing));


// use NlpTools\Tokenizers\WhitespaceTokenizer;
// use NlpTools\Documents\WordDocument;
// use NlpTools\Documents\Document;
// use NlpTools\Documents\TrainingSet;
// use NlpTools\Models\Maxent;
// use NlpTools\Optimizers\MaxentGradientDescent;
// use NlpTools\FeatureFactories\FunctionFeatures;
//
// $s = "When the objects of an inquiry, in any department, have principles, conditions, or elements, it is through acquaintance with these that knowledge, that is to say scientific knowledge, is attained.
//     For we do not think that we know a thing until we are acquainted with its primary conditions or first principles, and have carried our analysis as far as its simplest elements.
//     Plainly therefore in the science of Nature, as in other branches of study, our first task will be to try to determine what relates to its principles.";
//
// // tokens 0,30,62 are the start of a new sentence
// // the rest will be said to have the class other
//
// $tok = new WhitespaceTokenizer();
// $tokens = $tok->tokenize($s);
//
// $tset = new TrainingSet();
// array_walk(
//     $tokens,
//     function ($t,$i) use($tset,$tokens) {
//         if (!in_array($i,array(0,30,62))) {
//             $tset->addDocument(
//                 'other',
//                 new WordDocument($tokens,$i,1) // get word and the previous/next
//             );
//         } else {
//             $tset->addDocument(
//                 'sentence',
//                 new WordDocument($tokens,$i,1) // get word and the previous/next
//             );
//         }
//     }
// );
//
// // Remember that in maxent a feature should also target the class
// // thus we prepend each feature name with the class name
// $ff = new FunctionFeatures(
//     array(
//         function ($class, $d) {
//             // $data[0] is the current word
//             // $data[1] is an array of previous words
//             // $data[2] is an array of following words
//             $data = $d->getDocumentData();
//             // check if the previous word ends with '.'
//             if (isset($data[1][0])) {
//                 return (substr($data[1][0],-1)=='.') ? "$class ^ prev_ends_with(.)" : null;
//             }
//         },
//         function ($class, $d) {
//             $data = $d->getDocumentData();
//             // check if this word starts with a capital
//             return (ctype_upper($data[0][0])) ? "$class ^ startsUpper" : null;
//         },
//         function ($class, $d) {
//             $data = $d->getDocumentData();
//             // check if this word is all lowercase
//             return (ctype_lower($data[0])) ? "$class ^ isLower" : null;
//         }
//     )
// );
//
// // instanciate a gradient descent optimizer for maximum entropy
// $optimizer = new MaxentGradientDescent(
//     0.001, // Stop if each weight changes less than 0.001
//     0.1,   // learning rate
//     10     // maximum iterations
// );
// // an empty maxent model
// $maxent = new Maxent(array());
//
// // train
// $maxent->train($ff,$tset,$optimizer);
//
// // show the weights
// $maxent->dumpWeights();
?>
