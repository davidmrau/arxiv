const table = document.querySelector('.artistTable');
const url = 'data.jsonl';
window.addEventListener('DOMContentLoaded',()=>{
   fetchData();
})
let images = new Set()

function fetchData(){
    fetch(url)
      .then(response => response.text())
      .then(data => {
        const lines = data.split('\n').reverse();
        lines.forEach(line => {
          if (line.trim() !== '') {
            const obj = JSON.parse(line);
            // Do something with the object
                console.log(images.has(obj.img))
              if (!images.has(obj.img)){
                    addToPage(obj)
                  }

          }
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });

}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}



function addToPage(el){

   const tr = document.createElement('tr')

   insertAfter(tr,  table.firstElementChild);
   images.add(el.img)
   const td1 = document.createElement('td');
   td1.textContent = el.name1;
   tr.append(td1);
   const td2 = document.createElement('td');
   td2.textContent = el.name2;
   tr.append(td2);
   const tdImg = document.createElement('td');
   const img = document.createElement('img');
   img.src = el.img

   const link = document.createElement('a');
    
   link.href = el.img + '_small.jpeg'
   link.appendChild(img)
   tdImg.append(link)
   tr.append(tdImg)
}


const refreshIntervalSeconds = 5; // Change this value to your desired interval
setInterval(fetchData, refreshIntervalSeconds * 1000);






