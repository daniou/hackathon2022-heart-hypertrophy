var tempClass="p0";
async function process(){
    var filePath = document.getElementById("myFile").files[0].name;
    
    if(filePath != null)
    {
        document.getElementById("score").style.display = "none";
        document.getElementById("processing").style.display = "block";
        console.log(filePath); 
        // alert(filePath);
        result = await eel.process(filePath)(); 
        document.getElementById("processing").style.display = "none";
        document.getElementById("score").style.display = "inherit";
        
        document.getElementById("score").classList.remove(tempClass);
        tempClass = "p"+result.toString();
        document.getElementById("score").classList.add(tempClass);
        document.getElementById("spantext").textContent=result.toString()+"%";
    }
    else{
        alert("Select a video to start detecting");
    }

}

