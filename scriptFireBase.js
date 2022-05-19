


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAaZwQig94nmBSRWWH5DkpZYzqgFAKycoQ",
    authDomain: "wpm-spill.firebaseapp.com",
    projectId: "wpm-spill",
    storageBucket: "wpm-spill.appspot.com",
    messagingSenderId: "1020037318482",
    appId: "1:1020037318482:web:35615dfca962376f1b5c8b"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Lager en referanse til databasen
let db = firebase.firestore();


//Henter hoved element
let highScoreEl = document.querySelector("#highScoreList");

/* let tabellEl = document.createElement("table");

let theadEl = document.createElement("thead");

let tbodyEl = document.createElement("tbody"); */





let antallLikeScore = 0;
let telleVariabel = 0;

function skrivUtData() {

    // Henter data. Når dataene er ferdig hentet, starter "then"-biten
    db.collection("brukere").orderBy("Score", "desc").get().then((snapshot) => {



        let tabellEl = document.createElement("table");
        tabellEl.setAttribute("id", ("tabell" + telleVariabel));
        //Lager et table haed elemenet
        let theadEl = document.createElement("thead");
        //Lager et table body element
        let tbodyEl = document.createElement("tbody");

        let trEl = document.createElement("tr");
        let thEl1 = document.createElement("th");
        let thEl2 = document.createElement("th");
        let thEl3 = document.createElement("th");






        if (telleVariabel > 0) {
            let parentTabellSlett = document.querySelector("#highScoreList");
            let tabellOriginal = document.querySelector(("#tabell" + (telleVariabel - 1)));
            /* console.log("parentTabellEl",parentTabellSlett);
            console.log("TabellSlett",tabellOriginal); */
            parentTabellSlett.removeChild(tabellOriginal);

        }
        telleVariabel++;


        // Henter ut dokumentene
        let dokumenter = snapshot.docs;
        console.log(dokumenter[0].id)




        // Skriver dokumentene til konsollen



        //Genererer tabell. Først genererer jeg table head ordene: "Username" og "Score"




        thEl1.innerHTML += `<th>Plassering</th>`;
        trEl.appendChild(thEl1);

        thEl2.innerHTML += `<th>Brukernavn</th>`;
        trEl.appendChild(thEl2);

        thEl3.innerHTML += `<th>Score</th>`;
        trEl.appendChild(thEl3);


        /* for (let key in dokumenter[0].data()) {


            let stamBruker = dokumenter[0].data();

            if (key == "Username") {
                let thEl = document.createElement("th");
                thEl.innerHTML += `<th>Username</th>`;
                trEl.appendChild(thEl);
            } else if (key == "Score") {
                let thEl = document.createElement("th");
                thEl.innerHTML += `<th>Score</th>`;
                trEl.appendChild(thEl);
            }
            console.log()
        }
        */



        

        theadEl.appendChild(trEl)
        //Skriver ut top 10 brukere fra databasen
        for (let j = 0; j < 10; j++) {

            let bruker = dokumenter[j].data();


            

            

            let trEl = document.createElement("tr");

            for (let i = 0; i < 3; i++) {
                let tdEl = document.createElement("td");

                if (i == 0) {

                    //Koden genererer plasseringstallene. Gjør at hvis flere får samme score vil de få samme plassering. F.eks kan man ha to med plassering #1. Hvis de har samme score

                    if(j<10){
                        let bruker2 = dokumenter[j+1].data(); //Lager ny bruker slik at programmet kan sammenligne score verdiene
                        
                        if(bruker.Score == bruker2.Score){
                            tdEl.innerHTML += `<td> #${((j+1)-antallLikeScore)}</td>`;
                            trEl.appendChild(tdEl);
                            antallLikeScore++;
                        } else{
                            tdEl.innerHTML += `<td> #${((j+1)-antallLikeScore)}</td>`;
                            trEl.appendChild(tdEl);
                        }
                    } 
                    
                    
                }

                if (i == 1) {
                    tdEl.innerHTML += `<td> ${bruker.Username}</td>`;
                    trEl.appendChild(tdEl);
                }
                if (i == 2) {
                    tdEl.innerHTML += `<td> ${bruker.Score}</td>`;
                    trEl.appendChild(tdEl);
                }

            }

            antallLikeScore = 0;
            tbodyEl.appendChild(trEl);
        }

        //Legger til thead og tbody elementet i tabell elementet
        tabellEl.appendChild(tbodyEl);
        tabellEl.appendChild(theadEl);

        //Legger til tabell elementet i hoved elementet
        highScoreEl.appendChild(tabellEl);

    });

}






//Input

let inputFelt = document.querySelector("#brukerNavn")
let registreringKnappEl = document.querySelector("#registrerKnapp");
registreringKnappEl.addEventListener("click", registrerBruker);
let antallRegistreringer = 0;


function registrerBruker() {
    antallRegistreringer++;
    let WPM = poeng * 2;

    let brukerNavn = inputFelt.value;
    

    //Gjør at den ikke legger til informasjonen til databasen hvis man får 0 i poeng
    if (WPM != 0) {
        db.collection("brukere").add({
            Username: brukerNavn,
            Score: WPM
        });

        skrivUtData();

        

        db.collection("brukere").orderBy("Score", "desc").get().then((snapshot) => {
            let dokumenter = snapshot.docs;

            let merGlobalTellevariabel = 0;

            for (let i = 0; i < dokumenter.length; i++) {

                let bruker = dokumenter[i].data();
                console.log(i);
                if (bruker.Score == WPM) {
                    console.log("Du fikk plass", i + 1);
                    break
                }

                merGlobalTellevariabel++;
            }

            


            let tableEl = document.createElement("table");
            tableEl.setAttribute("id","tablePlassering");

            let tbodyEl = document.createElement("tbody");
            tbodyEl.setAttribute("id","childTablePlassering");
            let trEl = document.createElement("tr");
            

            let tdEl1 = document.createElement("td");
            let tdEl2 = document.createElement("td");
            let tdEl3 = document.createElement("td");


            tdEl1.innerHTML += `<td>#${(merGlobalTellevariabel+1)-antallLikeScore}</td>`;
            trEl.appendChild(tdEl1);

            tdEl2.innerHTML += `<td>${brukerNavn}</td>`;
            trEl.appendChild(tdEl2);

            tdEl3.innerHTML += `<td>${WPM}</td>`;
            trEl.appendChild(tdEl3);

            tbodyEl.appendChild(trEl);

            tableEl.appendChild(tbodyEl);
            
            highScoreEl.appendChild(tableEl);

            registreringKnappEl.style.backgroundColor = "#039e18"
        })
    }





    inputFelt.value = "";
    poeng = 0;
    

    //Genererer en rekke som viser din plassering uavhengig av om man kom på leaderboard eller ikke


}

skrivUtData()