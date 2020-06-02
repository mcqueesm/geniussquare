var selected = []

function boardClick(id){
    if(selected.length<=7){
        if(!selected.includes(id) && selected.length!==7){
            document.getElementById(id).style.backgroundColor = "white";
            selected.push(id);
        }
        else if(selected.includes(id)){
            document.getElementById(id).style.backgroundColor = "black";
            const index = selected.indexOf(id);
            if (index > -1) {
                selected.splice(index, 1);
            }

        }
    }
    document.getElementById('id_post').value = selected.join(" ");
   
}

function submitForm(){
    if(selected.length==7){
        var frm = document.getElementById('form1');
        frm.submit();
        frm.reset();
    }
    else{
        document.getElementById('warning').innerHTML="Please click on exactly 7 boxes";
    }
}


