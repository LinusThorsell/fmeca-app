
Hej!

Här kommer ett litet dummy projekt ni kan analysera.
Ni kommer få något mer komplett senare... 
...jag insåg när jag satt med det att det blir lite för enkelt...

Efter att ni sett detta så kommer ni ha många frågor. :) :) :)
Förhoppningsvis kan ni börja prototypa lite, ni kommer behöva mer input från oss.

Mvh,
/Rickard&Oscar&Sara&Chrisopher

/// /// ///

Kommentar 1
=======
Ni kan utgå från att vi kommer peka ut en path.
I den pathen hittar ni: infrastructure

infrastructure i sin tur är indelat i två sidor.
fc och mc. 
Där fc står för flight critical och är typisk hög DAL. (typ, flyg-dator, t.ex.)
Där mc står för mission critical och är typisk låg DAL. (typ, linux-dator, t.ex.)

fc och mc har filen system.xml

Prio Hög att hantera.

Kommentar 2
=======

system.xml beskriver vilka delar vi har och var/path de kan hittas.

Prio Hög att hantera.

Kommentar 3
=======

Den kommer peka ut topologier som ser olika ut beroende på om de är fc eller mc.
hw_topology.xml och sw_topology.xml
En beskriver hw aspekter av systemet och en beskriver de mjukare sidorna.

Prio Hög att hantera.

Kommentar 4
=======

Utöver system.xml, hw_topology.xml och sw_topology.xml
så hittar ni en katalog med equipment som används på sidan.

Prio Låg att hantera.

Kommentar 5
=======

Applications

De övriga delarna ni kommer hitta, se root, är:
applications - innehåller en application.xml som beskriver portar.
Portar är ett koncept som används i hårda realtidssytem. I lite lösare är signal vanligt.
Vad är det? Ofta ett physiskt minne som bär på data ( tänk memcopy() )

Det innehåller även olika targets / kan ha flera.
Samt en resource.xml i config som beskriver hur mycket resurser vi behöver.

Prio Hög att hantera.

Kommentar 6
=======

ifs

Här hittar ni interface specifikationer som ageras lite som proxy eller klister mellan olika delar.
Utifrån de här får man automatgenererad kod.

Tittar man i system, hw_- sw_topology så hittar man ofta dessa.
Dvs. ändrar man en ifs så slår det även på delar av fc och mc sidan.
Mer detaljer går att läsa.

Prio Medel att hantera.

Kommentar 7
=======

Interfaces

Här hittar ni enklare interfaces.
Beskriver typer etc. Olika typer av interfaces som kan användas i portar.

Prio Medel/Hög att hantera.

Kommentar 8
=======

Tillbaka till Infrastrukture.
Infrastrukture och Applications är de viktigaste delarna att kunna hantera bra.

Där hittar vi: functional_topology

functional_topology beskriver vilka instancer av applicationer vi har i systemet.
T.ex. Vi kan ha en applikation A som vi ger tre olika namn och startar. Då har vi tre applikationer som kör.

Den har en viktig katalog connections.

Där har varje instans en egen katalog med filen connections.xml
connections.xml beskriver hur de portar som finns i applikationens application.xml ska kopplas.
T.ex.: Application_Inst1_PortA <----> PortB_Application_Inst2

Prio Hög att hantera.














