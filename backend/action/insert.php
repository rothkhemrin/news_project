<?php

    include ('../db/cn.php');

    //$txt_menu=$_POST['txt_menu'];
    $txt_menu=$_POST['txt_menu'];
    $txt_disable=$_POST['txt_disable'];
    $txt_order=$_POST['txt_order'];

    //$txt_photo=$_POST['photo'];

//        $txt_menu='abc';
//        $txt_disable=1;
//        $txt_order=22;
//        $txt_photo=$_POST['photo'];


    $file = $_FILES['photo'];
    $name = $file['name'];
    $tmp = $file['tmp_name'];
    $type = pathinfo($name, PATHINFO_EXTENSION);
    $time = time();
    $check = getimagesize($tmp);
    $size = $file['size'];

if ($check == false) {
    echo 'Fake Image, Please chose Image not fake';
} else {
    if ($type != 'jpg' && $type != 'png' && $type != 'gif') {

        echo 'Invalided image extension ';
    }
    else {
        $path='../img/' . $time . '.' . $type;
        move_uploaded_file($tmp,$path);
        //$res['path']=$path;
        //echo json_encode($res);

    }
}

$sql = "insert into tbl_menu values (null,'".$txt_menu."',".$txt_disable.",".$txt_order.",'".$file."','name link')";
//$sql="insert into tbl_menu values (null,'".$txt_menu."',".$txt_disable.",".$txt_order.",'".$file."','name link')";

    if($cn->query($sql)){

        echo "successful";
    }
    else{
        echo "unsuccessful";
    }
?>