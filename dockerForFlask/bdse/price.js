window.onload=init;
var errMsg="";
var lat,lng,a,b,c,d,e,f,g,h,i,j,k,target,l,flag;
var map, marker, infoWindow = new google.maps.InfoWindow({ content: "" });;
function init() {    
    document.getElementById("corrs").onclick=codeAddress;
    document.getElementById("buildType").onchange=checkBuildType;
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: {lat: 25.055451, lng: 121.557889}
        });
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(25.055451, 121.557889),
        map: map,
    });
    }
function chlt() {
    a = document.getElementById("district").value;
    b = document.getElementById("buildType").value;
    c = document.getElementById("year").value;
    d = document.getElementById("mechPark").value;
    e = document.getElementById("planePark").value;
    f = document.getElementById("room").value;
    g = document.getElementById("living").value;
    h = document.getElementById("bath").value;
    i = document.getElementById("totFloor").value;
    j = document.getElementById("floor").value;
    k = document.getElementById("area").value;
    l = document.getElementById("manage").value;
    }
function checkBuildType(){
    if (document.getElementById("buildType").value == 4) {
         $("#floor").val("0")
         $("#floor").prop("disabled", true)
     } else {
         $("#floor").prop("disabled", false)
     }
}
function checkBox(){
    errMsg="";
    if (c == undefined || c=="") {errMsg+="請輸入屋齡\n"}
        else if (c > 80) { errMsg+="屋齡請輸入80以下\n" }
    if (d == undefined || d == "") { errMsg+="請輸入機械車位數量\n" }
        else if (d > 10) { errMsg+="機械車位請輸入10以下\n"}
    if (e == undefined || e == "") { errMsg+="請輸入平面車位數量\n" }
        else if (e > 10) { errMsg+="平面車位請輸入10以下\n"}
    if (f == undefined || f == "") { errMsg+="請輸入房間數量\n" }
        else if (f > 10) { errMsg+="房間數量請輸入10以下\n" }
    if (g == undefined || g == "") { errMsg+="請輸入客廳數量\n" }
        else if (g > 10) { errMsg+="客廳數量請輸入10以下\n" }
    if (h == undefined || h == "") { errMsg+="請輸入衛浴數量\n" }
        else if (h > 10) { errMsg+="衛浴數量請輸入10以下\n" }
    if (i == undefined || i == "") { errMsg+="請輸入總樓層\n" }
        else if (i > 30) { errMsg+="總樓層請輸入30以下\n" }         
    if (j == undefined || j == "") { errMsg+="請輸入樓層\n" }
        else if (j > 30) { errMsg+="樓層請輸入30以下\n" }
        else if (j > i) { errMsg+="樓層須小於總樓層\n" }
    if (k == undefined || k == "") { errMsg+="請輸入坪數\n" }
        else if (k > 200) { errMsg+="坪數請輸入200以下\n" }
    
    if(errMsg == ""){
        flag=true;
    }else{
        flag=false;
    }
    
}

var codeAddress =function() {
    //get all value
    var address = document.getElementById('address').value;  
    chlt();
    checkBox();
    if (address == undefined || address == "") { errMsg+="請輸入地址\n" }  
    if(flag){
        var geocoder= new google.maps.Geocoder();
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == 'OK') {
                var loc=results[0].geometry.location;
                lat=loc.lat();
                lng=loc.lng();
                addMarker(loc,map)
                target=a + "," + b + "," + c + "," + d + "," + e + "," + f + "," + g + "," + h + "," + i+","+j+","+k+","+lat+","+lng+","+l;
                //$.ajax({
                //    type: 'GET',
                //    url: 'http://192.168.35.14:5000/test/'+target,
                 //   dataType:'text'
                 //   }).done(function (data) {
                   //     //var str=data.text;
                     //   alert('每坪單價:'+data)
                   // })
                }else {
                alert('地址輸入錯誤，請重新檢查!');            
                }
        //console.log(target);
        })
    }
    else{
        alert(errMsg)
    }}
function addMarker(loc, map) {
    alert(document.getElementById("district").text);
    map= new google.maps.Map(document.getElementById('map'), {
        zoom: 17,
        center: { lat: loc.lat(), lng: loc.lng() }
    });
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(loc.lat(), loc.lng()),
        map: map
    });
    var anchor = new google.maps.MVCObject();
    anchor.set("position", loc);
    var str = [];
    str.push(document.getElementById("district").text);
    infoWindow.setContent(str.join(''));
    infoWindow.open(map, anchor);
}