$(function()){
$('#confirmation').click(function){
    var confirm=confirm('Serius');
    if(confirm==true){
    $.ajax({
    url:'perbarui_model',
    success:function(response){
    console.log(response);
    },
    eror:function(eror){
    console.log(eror);}
    });}
    else{
    }
}
};