TLDR: Scraper de pe Google Search + Text Extractor cu filtre. results7.json contine rezultatele. 821 de companii cautate, 71 VAT-uri gasite, 36 (61%) True Positives, 25 (39%) False Positives, 6 (60%) True Negatives, 4 (40%) False Negatives din identificate 71 (9%) din 821. Pentru a lucra la o scara mai larga, ar trebui sa incerc sa accesez si documente, nu doar preview-ul de la rezultatele de pe Google. Am ales aceasta abordare pentru ca Google deja s-a ocupat de crearea unui motor de cautare a datelor pe care le caut eu. Provocarea mea a fost sa filtrez toate rezultatele nedorite si eronate.



# Pasi incercati: 

Solutia 1: Identificare manuala. Am stat caut de mana surse. Evident, nu era solutia finala, dar a trebuit sa imi fac o idee despre ce scraper va fi nevoie. Am identificat problema 1: nu exista nicio regula in unde voi gasi pe site-ul unei companii un numar VAT. Foarte multe nu il au, iar cele care il au il pun in locuri similare, dar nu identice. Chiar si de pe site-ul Marks and Spencer a fost dificil sa il gasesc singur. 

Solutia 2: Scraper folosind un site map. Am identificat problema 2: O sa dureze foarte mult sa accesez paginile si sa obtin harta. Nu am nici cum sa obtin justificabil de multe astfel de harti. 

Solutia 3: Scraper de pe Google Search, extragand doar codurile din preajma secventelor „vat ”. Am identificat problema 3: Coduri insuficient de putine, scrise sub formate diverse, cu spatii aleatorii sau deloc. 

Solutia curenta: 

Am implementat un scraper care aduna date din rezultatele unui google search, de tipul **„nume companie” uk company vat** . Pentru a evita sistemul anti bot, este folosita o instanta de chromium, conectata la un cont de google de personal, cu cookie-uri si istoric, pentru a creste credibilitatea. Fereastra este afisata pe ecran, in care scriptul introduce tasta cu tasta query-ul. Intervalul de timp dintre fiecare tasta este random, intre 0.08 si 0.24 secunde, iar numele companiei este introdus prin paste din clipboard, pentru a reduce timpul necesar unei cautari. 

In cazul in care o pagina CAPTCHA se deschide, script-ul verifica odata la 10 secunde daca aceasta dispare, scotand la acelasi interval un sunet prin orice device audio e conectat in clipa aceea la dispozitiv (pentru a imi atrage atentia ca trebuie sa spun ca nu sunt un robot. Nu e nici pe departe cea mai automata/ eficienta solutie, dar a functionat pentru un zero-budget proof of concept). 

Pagina care se incarca contine multiple rezultate gasite de search engine, fiecare fiind site-ul si micul snippet cu continutul relevant mie (cel cu cuvintele cheie cautate). Scraper-ul descarca page source-ul si trece la urmatoarea pagina. Browser-ul este setat ca Gemini sa nu genereze vreun raspuns (pierd niste rezultate, dar evit orice sansa la vreo halucinatie. E mai scump un numar gresit decat absenta lui.) 

In paralel, un text extractor cauta in tot fisierul instante „vat ”, ignorand case-ul. Din jurul acestora, extrage toate secventele ce ar putea contribui la un numar VAT (fie numarul intreg, fie pe bucatele daca e scris cu spatii) si le salveaza in lista1. Un cod similar cauta in tot textul toate instantele ce ar putea fi un numar VAT, indiferent de proximitatea lor de cuvant. Acestea sunt filtrate cu 2 checkere (%97 si +55%97) si salvate in lista2. Toate numerele din lista1 sunt cautate in lista2 si numarate. Numarul cu cele mai multe aparitii este considerat VAT-ul companiei. Este salvat, alaturi de orice alt numar continand si codul tarii, factorul de credibilitate (0-1) si numarul de aparitii in pagina. Factorul poate fi folosit pentru prioritatea acestora de verificare (manuala sau cu API-urile guvernamentale). 

La crearea listei lista2 pot fi activate 3 setari de filtrare a fals pozitivelor. 

Masura 1: Cresterea limitei minima necesara de aparitii (primitiva) 
Masura 2: Cautarea unor cuvinte cheie care ar putea semnifica apartenenta numarului VAT la alta companie (journal, book, article, etc) 
Masura 3: Verificarea prezentei numarului companiei in preajma instantelor de VAT identificate. 

Intrucat prima nu garanteaza identificarea propriu-zisa a fals pozitivelor, doar ignorandu-le pe cele cu putine rezultate, a doua verifica scenariul in care compania cautata este regasita intr-o publicatie. Intrucat majoritatea companiilor care se ocupa de carti, reviste, etc sunt nevoite sa aiba un numar VAT public, este posibil ca numarul identificat sa fie al producatorului si nu cel care ne intereseaza pe noi (un caz din cele 200 cautate). A treia masura exista doar pentru a putea relaxa regula 2. Daca in numele companiei se regaseste un cuvant cheie, toate VAT-urile identificare pot ajunge sa fie ignorate degeaba. In aceasta situatie, se poate ignora cautarea cuvintelor (o abordare mai buna ar fi fost sa identific direct numele si sa il ignor, verificand restul string-ului, dar pentru ca numele poate sa difere, fie ca e prescurtat un cuvant, abreviat, etc, am decis sa nu pierd timpul pe un comparator in aceasta faza a proiectului). 

Am produs 8 rezultate, pentru a observa performanta proiectului meu, unul cu rezultatele finale, celelalte existand doar pentru observarea diferentelor create de masuri (in cazul in care 1 si 2 sunt prea stricte si cel in care 3 ar putea permite fals pozitivelor sa treaca mai departe). Printre rezultate se regasesc si companii care si-au schimbat intre timp numele (1, Pipeline 44 Group -> The Social Selling Company), dar si coduri VAT expirate (1, The Social Girl LTD - GB409020437). In prezent, nu am o solutie pentru aceasta problema. 

Imi este clar ca nici aceasta solutie nu este una nici pe departe optima, reusind sa produca rezultate pentru doar 4% din setul pe care am incercat (primele 200 de intrari din csv-ul pus la dispozitie de Companies House la https://download.companieshouse.gov.uk/BasicCompanyData-2026-09-01-part7_7.zip.)



## Primul test

200 a fost numarul ales de mine pentru a vedea ce probleme pot sa apara la prima vedere, in mai putin de o ora. Toate valorile obtinute au fost verificate. Initial, numarul de numere pozitive a fost de 10, din care 2 erau false (publicatii in reviste). Rata initiala de fals pozitive a fost de 20%. Actual 0%, dar din nou, pe un set mic de date, dupa ce am studiat explicit de ce acelea erau eronate si am facut masuri croite impotriva lor. Pentru verificare am folosit pagina web pusa la dispozitie de HMRC.

Cu toate ca nu a reusit sa evite complet, script-ul meu a reusit sa extraga datele despre 200 de companii dupa 4 zile de cautari repetate, identice (pentru primele variante ale codului), urmate de cautarile pentru setul real de date, automat, fiind necesara interventia umana pentru sistemul anti-bot de doar 6 ori. In primele faze ale proiectului, majoritatea cautarilor se blocau instantaneu in interfata “nu sunt un robot”. Codul prezentat contine versiunea 3 a scraper-ului si 2 a text extractor-ului.

Exemplu de fragment de text problematic: "VAT sales tax information. VAT id GB352385887. Company ... GB361001456 · THE SOCIAL PROJECT LTD · GB381764275. Share page on Facebook. Lookup UK VAT number for a ...". Acesta contine 3 numere VAT. Momentan, le-am ignorat pe cele neasociate THE SOCIAL PROJECT LTD, dar celelalte 2 puteau fi salvate si cautate prin checker sau tot pe internet si asociate companiilor lor.

Am incercat si sa imi fac cont la HMRC, dar dupa 2 ore pierdute pe configurare, mi-am dat seama ca varianta sandbox nu imi este deloc utila pentru verificarea unor numere reale VAT.



## Al doilea test (final): 

821 de companii. Rezultate: 
36/61     (59%) adevarat pozitive
25/61     (41%) fals pozitive
6/10       (60%) adevarat negative
4/10       (40%) fals negative
750/821 (91%) neidentificate

Codul a ramas acelasi pe partea de extragere si filtrare a numerelor (specializat pe primele 200). Singura modificare adusa a fost eliminarea sufixelor companiilor (LTD, LIMITED, Co., etc) din nume pentru a reduce numarul de companii negasite deloc pe Google (inca 3 gasite din 240 negasite). Din cate am inteles, doua companii ce difera prin nume doar prin aceste sufixe nu pot coexista, dar ma pot insela in aceasta privinta. Diferenta de rezultate dintre primul test si cel de-al doilea este ca in urma primului test, am cautat specific de ce au aparut acele erori si le-am remediat. De aceea il numesc specializat. Pentru cel de-al doilea test, nu am mai facut modificari.

Numerele gresite pot fi impartite in 3 categorii: gresite, expirate sau gresite si expirate. Cele gresite sunt numere ce apartin altor companii. Cele expirate sunt coduri care au apartinut companiei cautate, dar au fost scoase din uz. 


Tiparele principale identificate de mine pentru o parte mare din numerele gresite sunt aparitiile companiilor cautate in publicatiile altor companii (solutia = extinderea cuvintelor cheie cautate de masura 2, dar si crearea inca unei masuri care sa recunoasca existenta unui nume ale altei companii in preajma numarului VAT, cel mai primitiv exemplu ar fi sa caute daca mai exista cuvinte scrise in Sentence Case sau ALL CAPS, acompaniate optional de sufixe de companii), dar si faptul ca acestea sunt vecine geografice (aceeasi strada, diferenta de un numar) sau ca impartasesc aceeasi adresa. In urma acestei proximitati, codul meu a marcat numarul vecinului ca fiind numarul companiei cautate de mine (7/25 numerele gresite sunt corelate prin adresa companiei cautate si prin cea apartinatoare, vecinul).

Exemple din setul meu de date de vecini directi:
- OCMIS LTD detine gb406792245, identificat pentru THE SOMERSET CIDER BRANDY COMPANY LIMITED
- KENT AUTO PANELS LTD detine gb336047511, identificat pentru THE SONGWRITING ACADEMY LIMITED 

Exemple din setul meu de date de aceeasi adresa (ultimele 3 sunt si expirate):
- DIMARK LTD detine gb835713423, identificat pentru THE SOHO SANDWICH COMPANY LTD
- GEO-4D LIMITED, detine gb169044203 identificat pentru THE SOLID BAR COMPANY LTD
- 97 FOXES LIMITED detine gb189479925, identificat pentru THE SOUND BARN LIMITED
- OPERAMATICS LIMITED detine gb225431338, identificat pentru THE SOLAR BUREAU LTD
- CAPITAL CONVERSIONS & CONSTRUCTION LTD detine gb225628213, identificat pentru THE SOLUTION ORGANISATION LIMITED
- DBR CONSULTANCY (DORSET) LTD detine gb241232257, identificat pentru THE SOLUTIONS CENTRE LIMITED


Nu am identificat alte tipare momentan. 

Page source-urile sunt salvate fiecare intr-un html file, cu titlul ca numele companiei, fara sufixe. Sufixele ar trebui bagate inapoi in titlu pentru consistenta in proiect. De aceea unele apar salvate de 2 ori (cu si fara sufixe). 

Decid sa ma opresc la acest test deoarece au fost necesare 2 adrese de internet (casa + mobil) pentru HMRC. Prea multe request-uri.

Un aspect de care sunt mandru in urma acestui proiect este ca este capabil in anumite circumstante sa recunoasca un nr. VAT corect, chiar si daca acesta nu este cel mai des intalnit in pagina:

THE SOCIAL WORK AWARDS
Found after 'vat ': {'gb229800113075811301144458': 1, 'gb229800113': 3, '1802016': 1}
Could be vat: {'gb328315313': 40, 'gb229800113': 16}
A identificat corect ca GB229800113 este codul sau, nu GB328315313. Key = VAT, Value = instante.


## Pareri personale despre abordare
Daca ar fi sa imi evaluez abordarea (incercarea de a face rost de coduri utilizand Google Search), as clasifica-o ca o metoda ineficienta (putine rezultate), impanzita de rezultate false, pe a caror surse nu am cum sa le prezic in totalitate si care variaza de la des intalnite (mentionari in articole publicate de o companie for-profit), pana la cele specifice putinor companii. E necesara verificarea constanta a rezultatelor pentru a descoperi probleme nemaintalnite pana acum. Nu toate sunt evidente. De asemenea, rezolvarea CAPTCHA-ului devenise absurda spre final (rare, dar 6 task-uri succesive). 
Au fost multe aspecte neprevazute de-a lungul acestui proiect, dar pe departe cel mai mare soc l-am avut dupa efectuarea testului 2. Primul test parea sa prezinte un scenariu optimist. Cel de-al doilea l-a invalidat complet. Codul trebuie adaptat, iar abordarea trebuie extinsa si pe alte metode, cu vulnerabilitati diferite, pentru a se completa intre ele si a face identificarea erorilor mai usoara.  



# Ce imbunatatiri as aduce metodei mele: 

Mai multe filtre care sa verifice rezultatele obtinute. Cele 3 metode ale mele sunt strict pe problemele identificate momentan si chiar si asa nu le elimina complet. 

Paralelizare. Nu m-am folosit deloc de acest aspect deoarece procesul de obtinere al datelor imi cerea sa fiu prezent pentru a rezolva CAPTCHA-ul si dispun momentan de un singur monitor. Putea fi impartit, cu multiple instante de scraper-e, dar nu am vrut sa ofer mai multe motive de suspiciune ca as folosi un script. Codul responsabil de extragerea textului este mult mai rapid decat cel de obtinere al acestuia asa ca nu a avut pe ce date sa lucreze in paralel. 

Ar trebui sa ma documentez mult mai bine despre care companii sunt obligate sa isi faca VAT-ul public si sa ma concentrez mai intai pe acestea. 

Incercarea mea cu Google Search Engine duce la multe probleme. Dureaza mult (15 secunde pe query fara verificare), este necesara asistenta umana pentru rezolvarea CAPTCHA-urilor, multe rezultate inselatoare, mai ales pentru companiile care nu au un VAT public. Ar putea fi folosit Google Custom Search JSON API (100 gratis + $5/1000 queries pana la 10000 pe zi), dar dupa ne-am lovi de limita de 10K pe zi. Consider ca adevaratea cale de a gasi aceste numere este prin obtinerea si filtrarea documentelor precum cele dintre companii si a declaratii lor lor (pentru cele mici care nu sunt obligate sa il declare public). Recunosc ca nu am reusit personal sa identific astfel de surse, dar nici nu am alocat suficient timp pe aceasta directie, fiind limitat si concentrandu-ma momentan pe rezultatele mai accesibile (si ca sa vad personal cat de putine sunt publice). Presimt ca o parte din solutie ar fi si metode similare celei folosite de mine (de tip scraper care sa se confrunte des cu sisteme anti-bot, dar cu rezolvari mai eficiente impotriva lor). 

Codul curent cauta doar numere VAT de tipul “ddd ddd ddd” sau “ll ddd ddd ddd”, unde ll permise sunt doar GB si XI (Marea Britanie si Irlanda de Nord). Ignor complet “ll ddd ddd ddd ddd” sau pe cele pentru departamentele de guvern (GBGD ddd) si autoritatile de sanatate (GBHA ddd). Trebuie extins sa acopere si aceste coduri posibile si pentru celelalte tari ale setului de date. 

As folosi mare parte din puterea de calcul pentru a monitoriza si prezice situatia companiilor scanate, dupa factori de risc precum situatii anterioare, valoarea lor estimata, situatia in care se afla bunurile din pe care le prelucreaza fiecare companie si de care depind. As lua in considerare, dar cu precautie, si profilele de LinkedIn ale companiilor, rata de angajari, comentarii si review-uri lasate de clienti si gesturile si declaratii le publice facute de angajatii la companiile respective (parasirea functiei – semnificativa daca sunt persoane importante din firma sau un volum mare de angajati mai mici), postari 

pe retelele de socializare (sentimentul general si numarul de vacante), dar acestea sunt doar idei de moment, care probabil ar fi mult prea costisitoare, dificil de implementat la o scara larga (imposibila pentru companiile foarte mici) si care ar putea fi inlocuita de metode de monitorizare mai eficiente. Nu cunosc suficient tehnicile actuale ale pietei in acest sens, dar m-as concentra in egala masura pe obtinerea datelor noi cat si pe astfel de detalii pentru a mentine setul de date actual, mai ales pentru companiile mai vitale si semnificative. 

Nu consider ca va exista vreodata o solutie permanenta. Mereu va fi ceva de actualizat (un crawler care nu mai evita sistemele anti-bot), idei noi de detectare a semnelor prevestitoare pentru companii, care pot fi cu mult mai bune decat cele implementate curent, dar care trebuie totusi testate cu rigoare inainte de punere in functiune si monitorizarea continua a statutului setului. 




# Debate Topics 

## UK VAT numbers are nine digits with a checksum, so only a small fraction of the possible combinations are valid. What happens if you point that observation at HMRC’s checker, and is it a good idea?

Consider ca nu ar fi o optiune sigura sa introduc numere aleatorii, conform checksum-ului, in checker. Ingrijoararea mea principala ar fi consecintele legale. Accesul la API trebuie mai intai aprobat pentru nivelul de productie. Nivelul sandbox este complet inutil. Daca as trimite cereri la o frecventa rezonabila sarcinii de a crea un set de date intr-un timp util, ar fi foarte usor de reperat si mi-ar putea limita sau bloca accesul pe viitor la checker. In cazul improbabil in care reusesc sa evit acest scenariu, a doua problema este explicabilitatea obtinerii acelor date. Nu doar ca un set de date mai stufos ar contine date vitale despre companii si ar putea parea suspicios din privinta comiterii impersonarilor si fraudelor, dar mai poate si contine date care sa nu fi fost declarate nicaieri de catre companie, cu exceptia guvernelor. Ar fi date (protejate cred eu) la care eu nu ar trebui sa am acces si totusi am. As folosi alte metode, nu pe aceasta. O ultima problema, cea mai minora dupa mine, dar totusi importanta, ar fi faptul ca ar fi imposibil sa mentin setul de date actualizat. O companie noua ar fi depistata extrem de lent. 


## how would you keep this dataset current, given companies register and deregister continuously?

As monitoriza documente publice cum ar fi The Gazette dupa nume noi de companii. Ar fi asemenea unei plase de salvare pentru companiile care scap altor metode. Cea mai sigura metoda ar fi sa folosesc serviciul oferit de HMRC, descris la [https://www.gov.uk/guidance/apply-to-receive-non-fnanciali-vat-registratoni-data-from-hmrc#data-file-to-be-shared](https://www.gov.uk/guidance/apply-to-receive-non-financial-vat-registration-data-from-hmrc#data-file-to-be-shared). Aceasta metoda nu este totusi aplicabila, intrucat nu consider ca am fi eligibili conform acestui regulament [Small Business, Enterprise and Employment Act 2015](https://www.legislation.gov.uk/ukpga/2015/26/section/8) (subsectiunea 3 e incalcata, subsectiunea 4 nu poate fi garantata, daca le inteleg bine). Presupunand ca si celelalte metode oficiale dispun de astfel de gatekeeping-uri, intrevad doar optiuni informale de obtinere a datelor, prin scraping si crawling pe documente, declarati de taxe, etc, facute publice, fara a avea garantia ca datele sunt mereu actuale. Folosind tehnici mentionate in partea acestui document in care am vorbit despre ce as face cu mai multe resurse, as prioritiza anumite companii mai des decat pe altele, verificand mai des situatia lor decat pe a altora. 


## how would you know your dataset was wrong at scale, with nothing complete to compare it against? 

Cu cat setul de date ar fi mai mare, cu atat ar fi mai usor sa verific daca acesta contine duplicate. Daca un cod VAT apare de doua ori la doua sau mai multe companii, ar fi un indicator ca acele companii ar fi aceeasi sub diferite nume sau ca s-a produs o eroare (cum ar fi in cazul analizei mele cand o companie cu VAT public scrie articole si jurnale despre companii mai mici, cu VAT-ul mai greu de identificat, si pe care crawler-ele companiei le-au marcat eronat). 

Cu toate ca nu am un set cu care sa il compar, as putea sa impart setul de date in functie de scoruri de credibilitate (asemenea celui creat de mine, al meu e primitiv). As lua mici fragmente din fiecare, si le-as introduce in checker. Din asta as putea trage mai multe concluzii. Nu am nevoie se compar tot setul, doar o portiune mica din el. 

Daca mica parte din numerele cu valoare scazuta sunt predominant gresite, dar celelalte fragmente nu, ar insemna ca factorii mei de aproximare a corectitudinii si metodele de suprimare a valorilor gresite functioneaza si as fi precaut in legatura cu cei carora ajung sa le transmit acele date, fiind gresite. 

Daca mai multe fragmente reies ca ar fi gresite, aleatoriu, sau marea majoritate, rezultatele ar vorbi de la sine. 5/100 din companiile pe care le consideram sigur corecte fiind gresite ar fi un semnal grav de alarma. 


## which of your sources would you not be comfortable using in a product we sell, and why?

Prima si cea mai clara pentru mine ar fi modelele de limbaj natural. Orice ar genera modelele ar trebui verificat oricum si nu sunt surse sigure. O a doua sursa ar fi alte seturi de date similare, daca reusesc sa obtin acces la ele. Chiar si daca datele ar fi corecte (nu e confirmabil) si de acutalitate, tot nu as putea sa justific provenienta lor si ca nu le-am furat din alta parte. Le-as folosi totusi pentru a-mi compara setul meu cu cel procurat. Sursele oficiale ar fi greu de utilizat din cauza cerintelor de incadrare la persoana ce poate intra in posesia datelor si as evita sa le folosesc daca stiu ca poate fi considerat sau chiar incalc regulamentul. Alte surse asemanatoare ar fi orice companie care ofera date dar mentioneaza ca acestea sunt oferite doar pentru utilizare interna, nu pentru productie. In final, sursele mentionate anterior precum LinkedIn ar fi luate in considerare, dar nu facute o prioritate, intrucat ar fi o constanta lupta de reparare si imbunatatire a crawler-elor, care aduce roade de valoare redusa si poate chiar inselatoare. 

