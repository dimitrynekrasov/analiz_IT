<?php

define('ROOT_DIR', dirname(__FILE__));

echo $_FILES['fileToUpload']['name'];
$uploadedfile = $_FILES['fileToUpload']['name'];
$newfilename = translit(pathinfo($uploadedfile,PATHINFO_FILENAME));
$docFileType = strtolower(pathinfo($uploadedfile,PATHINFO_EXTENSION));
$newfile = $newfilename . "." . $docFileType;
$target_file = ROOT_DIR . '/uploads/' . $newfile;
$uploadOk = 1;
$readyToGo = 0;
if (file_exists($target_file)) {
    echo "Такой файл уже существует!";
    $uploadOk = 0;
}

if($docFileType != "docx" && $docFileType != "doc") {
    echo "Извините, разрешено загружать только документы форматов DOCX и DOC !";
    $uploadOk = 0;
}

if ($uploadOk == 0) {
    echo "Извините, некорректный файл!";
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "Файл ". basename( $_FILES["fileToUpload"]["name"]). " был загружен и отправлен на выполнение";
        $readyToGo = 1;
    } else {
        echo "Возникла ошибка при загрузке файла на сервер!";
    }
}

if ($readyToGo == 1) {
    $ch = curl_init("http://localhost:8081/?http://localhost/analiz_IT/uploads/". $newfile);
    $fp = fopen("uploads/result.txt", "w");

    curl_setopt($ch, CURLOPT_FILE, $fp);
    curl_setopt($ch, CURLOPT_HEADER, 0);

    curl_exec($ch);
    curl_close($ch);
    fclose($fp);
    header("location: http://localhost/analiz_IT/uploads/result.txt");
}
function translit($s) {
  $s = (string) $s; // преобразуем в строковое значение
  $s = strip_tags($s); // убираем HTML-теги
  $s = str_replace(array("\n", "\r"), " ", $s); // убираем перевод каретки
  $s = preg_replace("/\s+/", ' ', $s); // удаляем повторяющие пробелы
  $s = trim($s); // убираем пробелы в начале и конце строки
  $s = function_exists('mb_strtolower') ? mb_strtolower($s) : strtolower($s); // переводим строку в нижний регистр (иногда надо задать локаль)
  $s = strtr($s, array('а'=>'a','б'=>'b','в'=>'v','г'=>'g','д'=>'d','е'=>'e','ё'=>'e','ж'=>'j','з'=>'z','и'=>'i','й'=>'y','к'=>'k','л'=>'l','м'=>'m','н'=>'n','о'=>'o','п'=>'p','р'=>'r','с'=>'s','т'=>'t','у'=>'u','ф'=>'f','х'=>'h','ц'=>'c','ч'=>'ch','ш'=>'sh','щ'=>'shch','ы'=>'y','э'=>'e','ю'=>'yu','я'=>'ya','ъ'=>'','ь'=>''));
  $s = preg_replace("/[^0-9a-z-_ ]/i", "", $s); // очищаем строку от недопустимых символов
  $s = str_replace(" ", "-", $s); // заменяем пробелы знаком минус
  return $s; // возвращаем результат
}
?>
