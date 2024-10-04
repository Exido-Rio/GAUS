
let docTitle = document.title ;

window.addEventListener("blur", () => {
    document.title = "Come back (:" ;
})

window.addEventListener("focus", () => {
    document.title = docTitle;
})

function hacked(id){
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        let interval = null;
        let x = document.getElementById(id);

        x.onmouseover = event => {
            let iteration = 0;

            clearInterval(interval);

            interval = setInterval(() => {
                event.target.innerText = event.target.innerText
                    .split("")
                    .map((letter, index) => {
                        if (index < iteration) {
                            return event.target.dataset.value[index];
                        }

                        return letters[Math.floor(Math.random() * 26)]
                    })
                    .join("");

                if (iteration >= event.target.dataset.value.length) {
                    clearInterval(interval);
                }

                iteration += 1 / 3;
            }, 30);
        }
}


function clk(){
    document.getElementById('error').style.display = "none";
  }