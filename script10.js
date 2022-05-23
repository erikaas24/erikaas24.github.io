//Velkommen til koden min! Jeg har laget et words per minute program. Jeg vil nevne at ideen om et program som sjekker hvor fort man skriver ikke er min, men jeg kan stolt si at jeg ikke har sett på noen andres kode for å lage det. Bokstavene i spillet er delt inn i egne p paragrafer og derfor lar det seg ikke spille med en skjermleser. Jeg tenkte over problemet og innså at hvis man skulle spille det med skjermleser måtte skjermleseren ha tilpasset hastigheten på ordene etter som hvor fort man skriver de, ellers gir ikke programmet mening.

//Deklarerer elementer
let bodyEl = document.querySelector("body");
let skriveFeltEl = document.querySelector("#skriveFelt");
let skriveFeltInnerEl = document.querySelector("#skriveFeltInner");
let startKnappEl = document.querySelector("#oppstartKnapp");
let navMidEl = document.querySelector("#trykkPaaStart");
let restartKnappEl = document.querySelector("#restartKnapp");
let tekstFeltEl = document.querySelector("#tekstFelt");
let plasseringTabell = document.querySelector("#tablePlassering");
let parentEgenHighScoreEl = document.querySelector("#childTablePlassering");

tekstFeltEl.innerHTML = "<h1> Trykk på start </h1>";

//Variabler for spillfunksjonalitet

/* let poeng = 0; */ //Teller hvor mange ord riktige man har klart totalt. KOMMENTERTE UT VARIABEL PGA NY WPM UTREGNING
let antallSekunderGatt = 0;
let ordRiktige = 0; //Teller hvor mange riktige ord man har klart per rad. Den resettes hver rad.
let pointer = 0; //Variabelen som hjelper pcen med å bestemme hva siste tegn skrevet er
let antallRandomizes = 0;
let ordSkrevet = ""; //Lager en tom string for teksten
let nedTelling;
let antallBokstavPoeng = 0;
let nettLeserBredde = document.body.clientWidth;
localStorage.personalBest = 0; //Localstorage variabel defineres.

//Eventlisteners

startKnappEl.addEventListener("click", startKnappTrykket);
restartKnappEl.addEventListener("click", resetProgram);


function startKnappTrykket() {
    
    nettLeserBredde = document.body.clientWidth;
    resetProgram();

    navMidEl.innerText = "30";
    bodyEl.addEventListener("keydown", sjekkTast)//Eventlistener for skriving
    bodyEl.addEventListener("keydown", trykkHendelser)//Eventlistener for hendelsene som skjer ved trykking bortsett fra skriving

    nedTelling = window.setInterval(nedTellingFunksjon, 1000);//Setter et intervall som kjører nedTellingsFnksjon hvert sekund

    /* startKnappEl.removeEventListener("click", startKnappTrykket); *///Fjerner knappen sin event listener så man ikke kan spamme den når spillet har startet

    tekstFeltEl.innerHTML = "";
    genererRekke()

    let forsteSpanEl = document.querySelector("#span" + ordRiktige);
    forsteSpanEl.style.backgroundColor = "#f0eddf";

    //Gjør at man får grønn border når man kan skrive.
    skriveFeltEl.className = "active";

    //Fjerner tabellen som viser egen plassering. Gjør at bare siste registrerte bruker dukker opp i feltet under highscoretabellen
    if (antallVellykkedeRegistreringer > 0) {
        let plasseringTabell = document.querySelector("#tablePlassering");
        leaderBoardEl.removeChild(plasseringTabell);
        registreringKnappEl.style.backgroundColor = "#FFFBE9";
        antallVellykkedeRegistreringer = 0;
    }

}

//Funksjonen står for timeren og at den fjerner funksjonalitet når timeren er på 0 sekunder
function nedTellingFunksjon() {

    antallSekunderGatt++;
    navMidEl.innerText = 3 - antallSekunderGatt;

    if (antallSekunderGatt == 3) {
        /* let WPM = (poeng * 2); */ //Dette var gamle måten å regne ut WPM på

        //Utregningen for WPM tar alle bokstaver man har skrevet riktig og deler det på gjennomsnittslengden av et ord i listen av ord. Det ganger så med 2 for å få et minutt. Det fører til mindre tilfeldigheter og mindre flaks for WPM man får. Det ble implementert slik at leaderboard ble mer skill-based og mindre avhengig av heldig ord-rekke.
        let WPM = (Math.ceil((antallBokstavPoeng)/snittOrdLengde))*2;

        console.log(WPM);
        clearInterval(nedTelling);
        bodyEl.removeEventListener("keydown", sjekkTast);
        bodyEl.removeEventListener("keydown", trykkHendelser);
        skriveFeltInnerEl.innerText = "";
        navMidEl.innerText = "";
        skrivingTillatt = false;

        skriveFeltEl.className = "inactive"; //Gir rød border
        

        if(localStorage.personalBest < WPM){
            localStorage.personalBest = WPM;
        };

        tekstFeltEl.innerHTML = `<h1> Words per minute: ${WPM} </h1>`;
        tekstFeltEl.innerHTML += `<h3>Personal best: ${localStorage.personalBest} </h3>`;

        //Justerer css etter skjermbredde. Se forklaring under resetProgram()
        if(nettLeserBredde <= 750){
            tekstFeltEl.className = "active";
        }

    }
}


//Lukk listen med ord så koden blir oversiktlig
let listeOrd = [
    "kort"
    ,
    "viktig"
    ,
    "ellers"
    ,
    "minst"
    ,
    "fortsatt"
    ,
    "op"
    ,
    "veien"
    ,
    "seier"
    ,
    "mål"
    ,
    "kjent"
    ,
    "slags"
    ,
    "Frode"
    ,
    "stund"
    ,
    "arbeid"
    ,
    "finnes"
    ,
    "ingenting"
    ,
    "lange"
    ,
    "gangen"
    ,
    "stå"
    ,
    "lot"
    ,
    "rekke"
    ,
    "redd"
    ,
    "høre"
    ,
    "Vilde"
    ,
    "ga"
    ,
    "ti"
    ,
    "forteller"
    ,
    "overfor"
    ,
    "stadig"
    ,
    "burde"
    ,
    "visst"
    ,
    "syntes"
    ,
    "fjor"
    ,
    "sette"
    ,
    "funnet"
    ,
    "hjelp"
    ,
    "største"
    ,
    "løpet"
    ,
    "meter"
    ,
    "norges"
    ,
    "hånden"
    ,
    "spørsmål"
    ,
    "mente"
    ,
    "søndag"
    ,
    "følge"
    ,
    "fremdeles"
    ,
    "imot"
    ,
    "hus"
    ,
    "kvinne"
    ,
    "ventet"
    ,
    "reiste"
    ,
    "hendene"
    ,
    "trodde"
    ,
    "USA"
    ,
    "legger"
    ,
    "viste"
    ,
    "regjering"
    ,
    "eg"
    ,
    "årene"
    ,
    "eksempel"
    ,
    "tenkt"
    ,
    "Ole"
    ,
    "slikt"
    ,
    "Erik"
    ,
    "moren"
    ,
    "holder"
    ,
    "seks"
    ,
    "tenker"
    ,
    "stedet"
    ,
    "tillegg"
    ,
    "helst"
    ,
    "bruke"
    ,
    "skolen"
    ,
    "kampen"
    ,
    "nettopp"
    ,
    "døren"
    ,
    "egne"
    ,
    "eget"
    ,
    "sterkt"
    ,
    "betyr"
    ,
    "vant"
    ,
    "enkelte"
    ,
    "nærmere"
    ,
    "hvad"
    ,
    "dårlig"
    ,
    "Per"
    ,
    "trenger"
    ,
    "menneske"
    ,
    "måten"
    ,
    "vise"
    ,
    "oppe"
    ,
    "finner"
    ,
    "Toralf"
    ,
    "Eirik"
    ,
    "Jakob"
    ,
    "Benjamin"
];
const LENGDELISTE = listeOrd.length //Nyttig variabel
let tilfeldigListe = [];
let ordFjernet = [];

//Regner ut hva snittlengden er på ord i listen

let sumBokstaver = 0;
for(let i = 0; i < LENGDELISTE; i++){
    for(let j = 0; j < (listeOrd[i].length)-1; j++){
        sumBokstaver++;
    }
}
let snittOrdLengde = sumBokstaver/LENGDELISTE;

//Funksjonen som resetter programmet hver gang jeg trykker på reset
function resetProgram() {

    //Nullstiller tekst
    tekstFeltEl.innerHTML = "<h1> Trykk på start </h1>";
    skriveFeltInnerEl.innerText = "";
    navMidEl.innerText = "";
    ordSkrevet = "";

    //Hvis reset er siste knappen trykket vil den bruke "inactive" classen sin styling
    skriveFeltEl.className = "inactive";

    //Justerer css etter nettleserbredde. Gjør at tekstfeltet viser "WPM: xx" og "Personal Best: xx" med flex direction column fremfor row når nettleseren er under 750px. Lengden av nettleseren sjekkes hver gang man trykker på start så koden nedenfor vil ikke fungere hvis man febrilsk justerer skjermvinduet etter man har fått en score
    if(nettLeserBredde <= 750){
        tekstFeltEl.className = "inactive";
    }
    registreringKnappEl.style.backgroundColor = "#FFFBE9";

    randomizeListe();//Lager en ny ordliste
    ordFjernet = [];

    //Setter variabelverdiene til 0 igjen
    /* poeng = 0; */ //Variabelen har blitt erstattet etter ny utregning av WPM
    antallBokstavPoeng = 0;
    antallKeydown = 0;
    pointer = 0;
    ordFasit = tilfeldigListe[0];
    ordRiktige = 0;
    antallSekunderGatt = 0;

    //Fjerner eventlisteners slik at man må trykke på start igjen
    bodyEl.removeEventListener("keydown", trykkHendelser);
    bodyEl.removeEventListener("keydown", sjekkTast);
    startKnappEl.addEventListener("click", startKnappTrykket);

    //Fjerner eventuell feilmelding
    
    if(antallFeilMeldinger > 0){
        feilMeldingEl.innerText = ``
    }

    //Fjerner timeout, altså det som skjer når programmet skal regne ut WPM
    clearInterval(nedTelling);
}


function randomizeListe() {
    antallRandomizes++;

    if (antallRandomizes > 1) {
        tilfeldigListe = [];
        //Dette legger tilbake ordene man fjernet fra listen etter hvert som man skrev
        for (let i = 0; i < ordFjernet.length; i++) {
            listeOrd.unshift(ordFjernet[i]);
        }
    }
    let randomTall = Math.floor(Math.random() * (listeOrd.length));

    for (let i = 0; i < LENGDELISTE; i++) {
        let randomTall = Math.floor(Math.random() * (listeOrd.length));
        tilfeldigListe.push(listeOrd[randomTall]) //Legger til det valgte ordet i en annen liste
        listeOrd.splice(randomTall, 1); //Fjerner ordet som ble valgt fra den opprinnelige listen
    }

    listeOrd = tilfeldigListe; //Setter forrige liste til nye liste slik at den gamle listen kan randomizes igjen

}

randomizeListe();
let ordFasit = tilfeldigListe[0];

//Denne funksjonen er ansvarlig for å la brukeren kunne skrive inn i tekstfeltet. Jeg kunne ha brukt textarea men det er morsommere å gjøre det fra bunnen av
function sjekkTast(e) {

    let valgtTast = e.key;
    let tekst = skriveFeltEl.innerText;

    if (e.keyCode == 32) {
        skriveFeltInnerEl.innerHTML += "&nbsp;"; //Legger til HTML-hardkoden for et mellomrom i skriveFeltet. Er bare visuelt

    } else if (e.keyCode == 8 || e.key == "Backspace") {
        //Fjerner siste ledd av stringen ved bruk av slice. Slice kommandoen lager en ny string og redigerer ikke den gamle
        let nyTekst = tekst.slice(0, -1);
        skriveFeltInnerEl.innerText = nyTekst; 
    
    } else if (e.keyCode >= 65 && e.keyCode <= 90) {
        //If testen gjør slik at alle tall som ikke er bokstaver ikke skrives inn i feltet når de trykkes på
        skriveFeltInnerEl.innerText += valgtTast; 

    } else if (/* e.keyCode == 222 */e.key == "æ" || /* e.keyCode == 219 */e.key == "å" || /* e.keyCode == 186 */ e.key == "ø") {
        //legger til æ ø å siden de ikke dekkes av keycode-intervallet i if-testen ovenfor. Byttet fra e.keyCode til e.key fordi e.key er mer universialt mens e.keyCode varierer fra PC til PC

        skriveFeltInnerEl.innerText += valgtTast; 
    }
}


//Funksjonen som sjekker om ordet som er skrevet er det samme som det i listen. Inkluderer også det som skjer hvis man har skrevet ferdig en hel rad.;
function trykkHendelser(e) {

    let spanEl = document.querySelector("#span" + ordRiktige);
    spanEl.style.backgroundColor = "#f0eddf"; //Fargelegger span

    //Gjør det som skjer når ordene er like. Løkkene kan leses slik. Hvis ordet man skal skrive er det samme som ordet man har skrevet, og man har trykket på space, skjer koden.
    if (ordFasit == ordSkrevet) {
        //Kunne ha brukt en && operator men tar tid å fjerne et innrykk på hver eneste linje i neste if test
        if (e.keyCode == 32) {

            skriveFeltInnerEl.innerText = "";
            ordSkrevet = "";

            antallBokstavPoeng += ordFasit.length;
        
            ordFjernet.push(tilfeldigListe[0]);
            tilfeldigListe.shift();
            ordFasit = tilfeldigListe[0];

            pointer = 0;
            ordRiktige++;
            
            //Fargelegging av spanelementer

            spanEl.style.backgroundColor = "#FFFBE9"; //Denne fargelegger ordet man akkurat skrev til kremhvit

            //If testene gjør at span2 kun defineres så lenge ordriktige er under 10 fordi hvis variabelen hadde blitt 10, ville ikke neste rekke generere siden første ord i neste rekke også hadde fått id span10 i genererRekke funksjonen
            if (ordRiktige < 10) {
                let spanEl2 = document.querySelector("#span" + ordRiktige);
                if (spanEl2.id != "span9") {
                    spanEl2.style.backgroundColor = "#f0eddf";//Fargelegger til "grå". Er egentlig mørk kremhvit men pga bakgrunnsfargen ser den grå ut
                }
            }

            //If testen utfører hendelsene når man har klart 10 riktige ord
            if (ordRiktige == 10) {
                ordRiktige = 0;
                tekstFeltEl.innerText = "";
                genererRekke();
            }
        }
    }




    let bokstavEl = document.querySelector("#p" + ordRiktige + pointer);

    //If testen sier at så lenge man trykker på en bokstav i det norske alfabetet så skal den være true. La til e.key fordi keyCode varierer fra pc til pc. e.key er mer universielt
    if (e.keyCode == 222 || e.key == "å" || e.keyCode == 219 || e.key == "æ" || e.key == "ø" || e.keyCode == 186 || e.keyCode == 32 || (e.keyCode >= 65 && e.keyCode <= 90)) {

        //If testen sier at den skal legge til bokstaven skrevet i ordSkrevet variabelen så lenge man ikke har trykket på space og ordet er det samme. Den legger til space med template literals i else if løkken. Det funker kun med template literals
        if (e.keyCode != 32) {
            ordSkrevet += e.key;

        } else if (e.keyCode == 32) {
            ordSkrevet += ` `
        }

        //Fargelegging av bokstaver

        //Hvis ordene er like og tasten trykket ikke er space skal koden fargelegge bokstaven grønt. Dette forhindrer space fra å farge første bokstav i neste ord grønt når man trykker space for å komme til neste ord
        if ((ordSkrevet[pointer] == ordFasit[pointer]) && (e.keyCode != 32)) {
            bokstavEl.style.color = "#039e18";
        }


        //Gjør at hvis ordet starter på space så fargelegger ikke space noe. Det fargelegger rødt
        if (ordSkrevet[pointer] != ordFasit[pointer]) {
            if (ordSkrevet[0] != ` `) {

                //Lagde ny if test som fikser en feilmelding om at programmet prøver å fargelegge en bokstav som ikke finnes
                if (pointer < ordFasit.length) {
                    bokstavEl.style.color = "#f54242";
                }

            }
        }

        pointer++;

    }




    //Denne koden sjekker om ordet starter på mellomrom, og fjerner mellomrommet. Etter man har tastet space etter å ha skrevet inn et riktig ord legger den til space i det neste ordet så det må fjernes. Den reduserer også pointercounten med 1 siden pointeren vanligvis skal gå opp hvis man trykket på space midt i et ord. Det er ikke en veldig elegant løsning på problemet men det funker
    if (ordSkrevet[0] == ` `) {
        ordSkrevet = ordSkrevet.substring(1, 2);
        pointer--;
    }


    //Fjerner siste tegn i ordskrevet når man visker
    if (e.keyCode == 8) {
        ordSkrevet = ordSkrevet.substring(0, ordSkrevet.length - 1);
        //Sier at pointer ikke kan bli mindre enn 0 når man visker
        if (pointer > 0) {
            pointer--;
        }
    }
}



//Funksjonen genererer rekken med ord fra arrayen med tilfeldige ord

function genererRekke() {


    //De tre løkkene lager hendholdsvis linjer med ord(div), ordene(span), og bokstavene(p)

    for (let s = 0; s < 2; s++) {

        let tekstLinje = document.createElement("div");
        tekstLinje.setAttribute("class", "tekstLinje")
        tekstFeltEl.appendChild(tekstLinje);

        for (let i = 0; i < 10; i++) {


            //Opprinnelig løsning på problem er det som er kommentert ut. Den var veldig vanskelig å modifisere så jeg lagde en ny løsning der 10 ulike span tags blir laget med unik ID. Dette gjør at jeg kan modifisere hvert enkelt ord sin styling. Den opprinnelige løsningen legger HTML koden for et mellomrom direkte inn mellom ordene. Det funker visuelt men ikke hvis man skal style det. Den overordna for-løkken(s som løkkevariabel) fantes ikke på dette tidspunktet

            /* tekstFeltEl.innerText += tilfeldigListe[i];
            
            tekstFeltEl.innerHTML += "&nbsp;"; */

            /* let tekstLinje = document.createElement("div");
            if((i%10) == 0 ){
                tekstLinje.setAttribute("id",("tekstLinje" + (i/10)))
                tekstFeltEl.appendChild(tekstLinje);
                console.log("linje generert");
            } */

            let span = document.createElement("span");
            span.setAttribute("id", ("span" + i));
            tekstLinje.appendChild(span);

            if (s == 0) {
                let lengdeOrd1 = tilfeldigListe[i].length;

                //Denne løkken ble lagt til etterhvert. Jeg innså at jeg måtte gjøre hver bokstav til et eget p element med unik ID for å kunne modifisere fargen til hver bokstav ettersom man skriver riktig
                for (let j = 0; j < lengdeOrd1; j++) {
                    let p = document.createElement("p");
                    p.setAttribute("id", ("p" + i + j));
                    p.setAttribute("class", "bokstaver")
                    p.innerText = tilfeldigListe[i][j];
                    span.appendChild(p);
                }

            } else {
                //Setter id til bokstavene i andre ordrekke til å ha tellevariabel i + 10
                let i_2 = i + 10;
                let lengdeOrd2 = tilfeldigListe[i_2].length;

                for (let j = 0; j < lengdeOrd2; j++) {

                    let p = document.createElement("p");
                    p.setAttribute("id", ("p" + i_2));
                    p.setAttribute("class", "bokstaver")
                    p.innerText = tilfeldigListe[i_2][j];
                    span.appendChild(p);
                }
            }
        }
    }
}

//Funksjonalitet for spørsmåltegnknappen

let instruksjonsMenyEl = document.querySelector("#instruksjonsMeny");
let instruksjonsTekstEl = document.querySelector("#instruksjonsTekst");

let questionMarkEl = document.querySelector("#questionMark");
questionMarkEl.addEventListener("click", InstruksjonsKnappTrykket);
let questionMarkTrykk = 0;

let leaderBoardButtonEl = document.querySelector("#leaderBoardButton");
leaderBoardButtonEl.addEventListener("click", leaderBoardButtonTrykket)
let leaderBoardTrykket = 0;


function InstruksjonsKnappTrykket() {
    questionMarkTrykk++;
    questionMarkEl.classList.toggle("active");
    instruksjonsMenyEl.classList.toggle("active");
    /* Classlist returnerer alle Css klassene til elementet. Jeg sier at Css'en som skal gjelde hører til #instruksjonsMeny.active  */

    //Dette bytter mellom spørsmåltegn og kryss. 
    if ((questionMarkTrykk % 2) == 0) {
        questionMarkEl.src = "./Bilder/questionMark.png";
        /* navMidEl.innerText = "Trykk på start"; */
    } else {
        questionMarkEl.src = "./Bilder/x.png";
    }

    //If testen gjør at hvis brukeren har åpnet to av pop up divene samtidig så vil den automatisk lukke den som ble først åpnet
    if ((questionMarkTrykk % 2) != 0 && (leaderBoardTrykket % 2) != 0) {
        leaderBoardButtonEl.classList.toggle("active");
        leaderBoardEl.classList.toggle("active");
        leaderBoardTrykket++;
        leaderBoardButtonEl.src = "./Bilder/leaderBoard.jpeg";
    }

}

function leaderBoardButtonTrykket() {
    leaderBoardTrykket++;
    leaderBoardButtonEl.classList.toggle("active");
    leaderBoardEl.classList.toggle("active");

    if ((leaderBoardTrykket % 2) == 0) {
        leaderBoardButtonEl.src = "./Bilder/leaderBoard.jpeg";
        /* navMidEl.innerText = "Trykk på start"; */
    } else {
        leaderBoardButtonEl.src = "./Bilder/x.png";

    }
    //If testen gjør at hvis brukeren har åpnet to av pop up divene samtidig så vil den automatisk lukke den som ble først åpnet
    if ((questionMarkTrykk % 2) != 0 && (leaderBoardTrykket % 2) != 0) {
        questionMarkTrykk++;
        questionMarkEl.classList.toggle("active");
        instruksjonsMenyEl.classList.toggle("active");
        questionMarkEl.src = "./Bilder/questionMark.png";
    }

}

//Koden som forandrer teksten når man bruker mobil
let skjermBredde = screen.width;
if (skjermBredde < 500) {
    instruksjonsTekstEl.innerHTML = "<h1>Programmet er ikke kompatibelt med mobil </h1>";
}
