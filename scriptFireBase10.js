


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
let leaderBoardEl = document.querySelector("#leaderBoard");

let antallLikeScore = 0;
let telleVariabel = 0;

function skrivUtData() {

    // Henter data. Når dataene er ferdig hentet, starter "then"-biten
    db.collection("brukere").orderBy("Score", "desc").get().then((snapshot) => {


        //Deklarerer variablene for tabellen
        let tabellEl = document.createElement("table");
        tabellEl.setAttribute("id", ("tabell" + telleVariabel));
        //Lager et table haed elemenet
        let theadEl = document.createElement("thead");
        //Lager et table body element
        let tbodyEl = document.createElement("tbody");

        //Lager øverste rekke manuelt
        let trEl = document.createElement("tr");
        let thEl1 = document.createElement("th");
        let thEl2 = document.createElement("th");
        let thEl3 = document.createElement("th");

        //Sørger for å slette den gamle tabellen når man generer en ny tabell med oppdatert informasjon.
        if (telleVariabel > 0) {
            let parentTabellSlett = document.querySelector("#leaderBoard");
            let tabellOriginal = document.querySelector(("#tabell" + (telleVariabel - 1)));
            parentTabellSlett.removeChild(tabellOriginal);
        }
        telleVariabel++;


        // Henter ut dokumentene
        let dokumenter = snapshot.docs;

        //Genererer tittel-ordene for første rad

        thEl1.innerHTML += `<th>Plassering</th>`;
        trEl.appendChild(thEl1);

        thEl2.innerHTML += `<th>Brukernavn</th>`;
        trEl.appendChild(thEl2);

        thEl3.innerHTML += `<th>Score</th>`;
        trEl.appendChild(thEl3);

        theadEl.appendChild(trEl)


        //Skriver ut top 10 brukere fra databasen
        for (let j = 0; j < 10; j++) {

            let bruker = dokumenter[j].data();
            let trEl = document.createElement("tr");

            for (let i = 0; i < 3; i++) {
                let tdEl = document.createElement("td");

                //Virker som om det gir lite mening å ha if-tester som sørger for at noe skjer 1 gang i en løkke. Men hvis jeg ikke hadde gjort det sånn måtte jeg ha lagd 3 tdEl elementer med ulikt navn. Da måtte jeg ha skrevet all koden nedenfor 3 ganger siden navnet er ulikt.
                if (i == 0) {

                    //Koden genererer plasseringstallene. Gjør at hvis flere får samme score vil de få samme plassering. F.eks kan man ha to med plassering #1. Hvis de har samme score. Dette gjelder bare top 10. For de resterende brukerene ville jeg ikke innføre det samme systemet, fordi det virker som et dårlig system hvis jeg får tusenvis av brukere med lik score, det blir mye for løkken å gjennomgå. Betyr også at man praktisk sett får omtrent 140 plasseringer, noe som kan gi et falsk inntrykk av at man er top 200 i verden med en gang man spiller. Føler likevel at plasseringsystemet går greit med top 10.

                    let bruker2 = dokumenter[j + 1].data(); //Lager ny bruker slik at programmet kan sammenligne score verdiene mellom to brukere.

                    if (bruker.Score == bruker2.Score) {
                        tdEl.innerHTML += `<td> #${((j + 1) - antallLikeScore)}</td>`;
                        trEl.appendChild(tdEl);
                        antallLikeScore++;
                    } else {
                        tdEl.innerHTML += `<td> #${((j + 1) - antallLikeScore)}</td>`;
                        trEl.appendChild(tdEl);
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
        leaderBoardEl.appendChild(tabellEl);

    });

}






//Deklarerer variabler for registrering

let inputFelt = document.querySelector("#brukerNavnInput")
let registreringKnappEl = document.querySelector("#registrerKnapp");
let tittelOgFeilmeldingEl = document.querySelector("#tittelOgFeilmelding");
let feilMeldingEl = document.querySelector("#feilMelding");
registreringKnappEl.addEventListener("click", registrerBruker);

let antallVellykkedeRegistreringer = 0; //Brukes for å fortelle PCen når den skal fjerne forrige registrerte tabell som ble generert
let antallFeilMeldinger = 0; // Brukes for å fortelle PC'en om den skal nullstille en feilmelding

function registrerBruker() {
    let WPM = (Math.ceil((antallBokstavPoeng) / snittOrdLengde)) * 2; //Regner WPM ved å ta antall bokstaverSkrevet riktig og delt på gjennomsnittslengden av hvert ord i hele ordlisten. Gir et mer konsistent mindre flaks-basert resultat.
   
    //Koden nedenfor definerer brukernavnet midlertigig. Det brukes for å gå gjennom alle testene for om registreringen skal være gyldig.
    let midlertidigBrukerNavn = inputFelt.value;

    if (WPM == 0) {
        antallFeilMeldinger++;
        registreringKnappEl.style.backgroundColor = "#f54242";
        feilMeldingEl.innerText = `Skaff poeng før du registrerer`;
        return
    }

    if (midlertidigBrukerNavn == ``) {
        antallFeilMeldinger++;
        registreringKnappEl.style.backgroundColor = "#f54242";
        feilMeldingEl.innerText = `Lag et brukernavn for registrering`;
        return
    }
    //Noen har en tendens til å programmere at de har evig mange poeng i konsollen. Setter en sperre på det
    if (WPM > 180) {
        antallFeilMeldinger++
        registreringKnappEl.style.backgroundColor = "#f54242";
        feilMeldingEl.innerText = `Ulovlig god`;
        return
    }

    //Sjekker brukernavnet for forekomster av < og >. Det stopper registrering fordi det kan brukes til å legge inn HTML kode i leaderBoardet.
    for (let i = 0; i < midlertidigBrukerNavn.length; i++) {
        if (midlertidigBrukerNavn[i] == "<" || midlertidigBrukerNavn[i] == ">") {
            antallFeilMeldinger++;
            registreringKnappEl.style.backgroundColor = "#f54242";
            feilMeldingEl.innerText = `Brukernavn kan ikke inneholde "<" eller ">"`;
            return
        }
    }

    //Setter nytt brukernavn etter at det midlertidige har gått gjennom testene.
    let brukerNavn = midlertidigBrukerNavn;
    antallVellykkedeRegistreringer++;

    //Legger til et nytt dokument med brukernavn fra input og Score som er WPM man fikk. Legger det til databasen
    db.collection("brukere").add({
        Username: brukerNavn,
        Score: WPM
    });
    //Skriver ut ny data nå for å oppdatere tabellen i tilfelle brukeren kom på top 10.
    skrivUtData();

    //Genererer en ny tabell nedenfor den originale tabellen som viser brukeren sin plassering uavhengig av om brukeren nådde top 10
    db.collection("brukere").orderBy("Score", "desc").get().then((snapshot) => {

        let dokumenter = snapshot.docs;


        let merGlobalTellevariabel = 0;

        //Løkken finner hvilken index brukeren fikk i dokumentlisten sortert etter score. Løkken er nødvendig fordi da får jeg en tellevariabel som viser hvilke plass brukeren(eller en annen med samme score som brukeren) fikk. 
        for (let i = 0; i < dokumenter.length; i++) {

            let bruker = dokumenter[i].data();
            if (bruker.Score == WPM) {
                break
            }

            merGlobalTellevariabel++;
        }

        //Deklarerer tabellelementer
        let tableEl = document.createElement("table");
        tableEl.setAttribute("id", "tablePlassering");

        let tbodyEl = document.createElement("tbody");
        tbodyEl.setAttribute("id", "childTablePlassering");
        let trEl = document.createElement("tr");


        let tdEl1 = document.createElement("td");
        let tdEl2 = document.createElement("td");
        let tdEl3 = document.createElement("td");

        //Plasseringen finnes ved at man førstfinner dokumentet sin index, plusser 1 siden tellevariablene begynner på 0, så subtraherer antall ganger 2 brukere har samme highscore fra top 10.
        tdEl1.innerHTML += `<td>#${(merGlobalTellevariabel + 1) - antallLikeScore}</td>`;
        trEl.appendChild(tdEl1);

        tdEl2.innerHTML += `<td>${brukerNavn}</td>`;
        trEl.appendChild(tdEl2);

        tdEl3.innerHTML += `<td>${WPM}</td>`;
        trEl.appendChild(tdEl3);

        tbodyEl.appendChild(trEl);

        tableEl.appendChild(tbodyEl);

        leaderBoardEl.appendChild(tableEl);

        registreringKnappEl.style.backgroundColor = "#039e18"
    })






    inputFelt.value = "";
    antallBokstavPoeng = 0;




}

skrivUtData()
