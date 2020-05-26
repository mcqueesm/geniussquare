var selected = []

function boardClick(id){
    if(selected.length<=7){
        if(!selected.includes(id) && selected.length!==7){
            document.getElementById(id).style.backgroundColor = "black";
            selected.push(id);
        }
        else if(selected.includes(id)){
            document.getElementById(id).style.backgroundColor = "white";
            const index = selected.indexOf(id);
            if (index > -1) {
                selected.splice(index, 1);
            }

        }
    }
    document.getElementById('id_post').value = selected.join(" ");
   
}


