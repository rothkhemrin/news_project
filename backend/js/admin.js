$(document).ready(function () {

    var body=$('body');
    var btn_add=$('#btn-add');
    var str_popup='<div class="container-fluid popup-box" id="popup-box"></div>';
    var ind;

    btn_add.click(function () {

        /* if user click one of left menu. then btn-add will work */
        if (ind>=0){

            var frms=['menu_frm','news_frm'];

            /* display popup box */
            body.append(str_popup);
            /*---------------------*/


            /* load frm into popup box on body */
            $('#popup-box').load("../frm/"+ frms[ind]+'.php', function(responseTxt, statusTxt, xhr){
                if(statusTxt == "success")
                //alert("External content loaded successfully!");
                    if(statusTxt == "error")
                        alert("Error: " + xhr.status + ": " + xhr.statusText);
            });
        }
        /*-------------------------------------------------------------------*/

        /* if user didn't click menu list then alert massage */
        else{

            var mgs_frm='msg_frm.php';
            var msg_title='Invalid data';
            var msg_body='Please select one of the left menus';

            /* display pop up frm */
            body.append(str_popup);

            /* display message box to valid data */
            $('#popup-box').load("../frm/"+mgs_frm , function(responseTxt, statusTxt, xhr){
                if(statusTxt == "success")
                    $('#msg-title').text(msg_title);
                $('#msg-body').text(msg_body);
                //alert("External content loaded successfully!");
                if(statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText);
            });
        }
        /*-----------------------------------------*/
    });

    /* get value of menu list when user click on li */
    $('#body-left-menu').on('click','li',function () {

        var ethis=$(this);

        ind=ethis.data('id');

        /* change background color when user click on list itme left menu */
        $('#body-left-menu').find('li').css({'background-color':'#fffeb7'},{'color':'#005a80'});
        ethis.css({'background-color':'#ff0000'});
        /*-----------------------------------------------*/

        /* set name as item list menu left */
        $('#item-list').text($.trim(ethis.text())) ;
        /*------------------*/

    });
    /* --------------------------- */

    /* remove news-frm */
    body.on('click','#btn-cancel-frm-news',function () {

        $('#popup-box').remove();
    });
    /*-------------------------*/

    /* remove close-frm */
    body.on('click','#btn-close-frm',function () {
        $('#popup-box').remove();
    });
    /*-------------------------*/

    /* remove close-frm */
    body.on('click','#btn-msg-close',function () {
        $('#popup-box').remove();
    });
    /*-------------------------*/

    /* remove close-frm */
    body.on('click','#btn-msg-cancel',function () {
        $('#popup-box').remove();
    });
    /*-------------------------*/

    /* remove menu-frm */
    body.on('click','#btn-menu-close',function () {
        $('#popup-box').remove();
    });
    /*-------------------------*/

    /* remove menu-frm */
    body.on('click','#btn-menu-cancel',function () {
        $('#popup-box').remove();
    });
    /*-------------------------*/

    body.on('click','#btn-menu-save',function () {
       var txt_menu=$('#txt-menu-menu');
       var txt_disable=$('#txt-disable-menu');
       var txt_order=$('#txt-order-menu');
       var txt_photo = $('#txt-photo-menu');

       // var frm=$(this).closest('form.frm');
       // var frm_data=new FormData(frm[0]);
        alert(txt_photo.val());
        $.ajax({
            url: '../action/insert.php',
            type: 'POST',
            data: {txt_menu: txt_menu.val(),
                    txt_disable:txt_disable.val(),
                    txt_order:txt_order.val(),
                    photo:txt_photo.val()},
            //data:frm_data,

            cache: false,
            //contentType: false,
            //processData: false,
            //dataType:'json',






        });




        });
});