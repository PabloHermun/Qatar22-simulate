
document.addEventListener("DOMContentLoaded", function(){
    // Display round of 16 contender flags 
    let round = document.getElementsByName('R16')
    for (let game of round) {
        // From html get the {group|position} labels for each game
        let label1 = game.querySelector('#t1').innerHTML;
        let label2 = game.querySelector('#t2').innerHTML;
        // Get corresponding flags 
        let flag1 = document.getElementsByName(label1.trim())[0].querySelector('#team');
        let flag2 = document.getElementsByName(label2.trim())[0].querySelector('#team');
        // Replace labels with (larger) flags
        game.querySelector('#t1').innerHTML = flag1.innerHTML.replace("sq-2", "sq-3").replace("50%","45%")
        game.querySelector('#t2').innerHTML = flag2.innerHTML.replace("sq-2", "sq-3").replace("50%","45%")
    }
});

function sim_r16(stage) {
    // Simulate the round of 16
    // Iterate over html rows
    let rows = document.getElementsByName('bracket-row');
    for (let j = 0; j < rows.length; j++) {
	    const row = rows[j];
        // Get the 2 qf-games in the row
	    qf_lists = row.querySelectorAll("table[name='"+stage+"']");
        for (let i=0; i<2; i++) {
            let winner = rand_winner() + 1;
            try {
                // Select looser
                let looser = row.querySelectorAll('#t'+ (winner%2 + 1))[i].querySelector('img')
                looser.classList.remove('opacity-100')
                looser.classList.add('opacity-25')

                row.querySelectorAll('#t'+ winner)[i].querySelector('img').classList.remove('opacity-25')
            }
            catch(err) {
            }
            // Winner passes to QF
            qf_lists[i].querySelector('td').innerHTML = row.querySelectorAll('#t'+ winner)[i].innerHTML
            
        }
    }
}

function sim_qf(first, last) {
    // Simulates all the KO-games in the range [first, last]
    for (let g = first; g < last +1; g++) {
        
        let teams = document.querySelectorAll('#g'+g)
        // Simulate a winner
        let winner = rand_winner();
        
        try {
            // Select looser
            let looser = teams[(winner+1)%2].querySelector('img')
            looser.classList.remove('opacity-100')
            looser.classList.add('opacity-25')

            // Select winner (change opacity if it is currently a looser)
            teams[winner].querySelector('img').classList.remove('opacity-25')

            // 3rd place contenders (special case)
            document.querySelector('#L'+g).innerHTML = teams[(winner+1)%2].querySelector('td').innerHTML
        }
        catch(err) {
        }
        // Winner passes
        document.querySelector('#W'+g).innerHTML = teams[winner].querySelector('td').innerHTML
    }
    // Edit size of finalists
    final=document.getElementById('final')
    final.innerHTML = final.innerHTML.replaceAll("sq-3","sq-4")
    champion = document.getElementById('champion')
    champion.innerHTML = champion.innerHTML.replaceAll("sq-3","sq-4").replace("45%","60%")
    third = document.getElementById('3rd')
    third.innerHTML = third.innerHTML.replaceAll("sq-3","sq-4").replace("45%","35%")
    try{
        // Decorate champion if there is one
        champion.querySelector('img').style.border = "5px solid #FFD700"
        champion.querySelector('img').classList.add('img-thumbnail')
    }
    catch (err){}
}

function rand_winner() {
    let num = Math.random();
    if (num < 0.5){
        return 0;
    }
    return 1;
}