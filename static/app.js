const findButton=document.getElementById("find");
const resultBox=document.getElementById("result");
findButton.addEventListener("click",async()=>{
  const source=document.getElementById("source").value;
  const destination=document.getElementById("destination").value;
  const algorithm=document.getElementById("algorithm").value;
  resultBox.classList.remove("hidden");
  resultBox.innerHTML="<p>Calculating…</p>";
  findButton.disabled=true;
  try{
    const response=await fetch("/api/navigate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({source,destination,algorithm})});
    const data=await response.json();
    if(!response.ok||data.error) throw new Error(data.error||"Unable to calculate.");
    if(data.mode==="mst"){
      resultBox.innerHTML=`<h3>${data.algorithm} — Minimum Spanning Tree</h3><p><b>Total network distance: ${data.total} m</b></p><div class="edge-list">${data.edges.map(e=>`<div class="edge"><span>${e.from} ↔ ${e.to}</span><b>${e.distance} m</b></div>`).join("")}</div>`;
    }else{
      resultBox.innerHTML=`<h3>${data.algorithm} result</h3><p><b>Estimated route distance: ${data.distance} metres</b></p><div class="route">${data.route.map((p,i)=>`${i?'<span class="arrow">→</span>':''}<span class="stop">${p}</span>`).join("")}</div><p>${data.message}</p>`;
    }
  }catch(err){resultBox.innerHTML=`<p><b>Unable to calculate route:</b> ${err.message}</p>`;}
  finally{findButton.disabled=false;}
});
fetch("/api/graph").then(r=>r.json()).then(data=>{
  document.getElementById("edges").innerHTML=data.edges.map(e=>`<div class="edge"><span>${e.from} ↔ ${e.to}</span><b>${e.distance} m</b></div>`).join("");
}).catch(()=>{document.getElementById("edges").textContent="Could not load campus connections.";});
