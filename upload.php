<?php

define('ROOT_DIR', dirname(__FILE__));

$target_file = ROOT_DIR . '/uploads/' .$_FILES['fileToUpload']['name'];
$docFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
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


//if ($readyToGo == 1) {
$ch = curl_init("http://localhost:8081/?http://localhost/analiz_IT/uploads/test.docx");
$fp = fopen("uploads/result.txt", "w");

curl_setopt($ch, CURLOPT_FILE, $fp);
curl_setopt($ch, CURLOPT_HEADER, 0);

curl_exec($ch);
curl_close($ch);
fclose($fp);
	#$response = http_get("http://127.0.0.1:8081/");
//}


//echo $docFileType
?>
