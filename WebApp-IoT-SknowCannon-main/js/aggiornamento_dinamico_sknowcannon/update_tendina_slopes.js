function updateTendinaSlopesNames (data, name_locality){
    //console.log("QEUSTI SONO I CAZZO DI DATI: "+data)
    if (data.length >0 ){
         var updatedTableBody = '<ul class="nav navbar-nav"><li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Slopes Available<span class="caret"></span></a><ul class="dropdown-menu">';
         for (var i = 0; i < data.length; i++) {
            var localityName = data[i];
             console.log(localityName);
            
             //updatedTableBody += "<li><a id=" + localityName + " href='#titolo_kit' onClick='getData(" + localityName + "')'>";
             updatedTableBody += "<li><a id=slopes" + i + " href='#selection' onClick='getSectors(" + i + ",\"" + name_locality +"\")'>";
             updatedTableBody += localityName;
            //updatedTableBody +=" - "+stato;
            updatedTableBody +='</a></li>';
         
         }
         updatedTableBody+="</ul></li></ul>"
        $("#slopes_list_container").html(updatedTableBody);
    }
    else{
        $("#slopes_list_container").html("<span>Sorry! NO LOCALITIES AVAILABLE</span>");
    }        

}


