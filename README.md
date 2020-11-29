# Estropadak parser

Library to parse calendar and results for any of the sea rowing leagues (estropada) played
in the Basque Country.

Euskal Herrian jokatzen diren estropada ligen egutegi eta emaitzak parseatzeko liburutegia.
Estropadaren URL edo HTML-a emanda, `Estropada` datu egitura bat itzuliko du orritik ateratako
informazioarekin.

# Usage / Erabilera

Instace a `EstropadakParser` object with the correct league code and just invoke it's `parse()` method.
It will return an `Estropada` object with can be dumped as text with `dump_text()` or as JSON with `dump_json()`.

`EstropadakParser` objectu bat instantziatu, liga kode egokia erabiliz, eta `parse()` metodoa inbokatu.
`Estropada` objektu bat itzuliko du zeinen edukia testu moduan `dump_text()` edo JSON moduan `dump_json()` lortu 
dezakegun.

```python
>>> from estropadakparser.estropadakparser import EstropadakParser

>>> e = EstropadakParser('act').parse('https://www.euskolabelliga.com/resultados/ver.php?id=es&r=1586168644')
>>> e.dump_text()

Postua Tanda   Kalea               Taldea                      Ziabogak                Denbora
0         1       1     KAIKU VUSA                      02:27   05:54   10:18           20:14,32
0         1       2     CR ARES                         02:26   05:54   10:19           19:49,08
0         1       3     ONDARROA CIKAUTXO               02:28   05:44   10:12           19:42,88
0         1       4     ZARAUTZ BABYAUTO                02:31   05:39   10:05           19:32,54
0         2       1     DONOSTIARRA AMENABAR            02:30   05:43   10:03           19:38,76
0         2       2     CABO                            02:28   05:39   10:04           Descal
0         2       3     LEKITTARRA ELECNOR              02:31   05:39   10:02           19:34,34
0         2       4     ZIERBENA BAHIAS DE BIZKAIA      02:31   05:32   09:49           19:06,74
0         3       1     BERMEO URDAIBAI AVIA            02:35   05:43   09:54           19:30,08
0         3       2     SANTURTZI TRANSPORTES Y GRUAS AGUADO    02:31   05:41   09:53           19:20,84
0         3       3     ORIO ARRAUNKETA ELKARTEA        02:31   05:35   09:52           19:23,00
0         3       4     GO FIT HONDARRIBIA              02:34   05:35   09:50           19:18,66
```

```python
>>> python3 -m estropadakparser.estropadakparser ACT text "https://www.euskolabelliga.com/resultados/ver.php?id=eu&r=1586168644"

Santurtziko XLI. Ikurriña
Postua	Tanda	Kalea	            Taldea            	        Ziabogak         	Denbora
1     	  2  	  4  	ZIERBENA BAHIAS DE BIZKAIA    	02:31	05:32	09:49        	19:06,74
2     	  3  	  4  	GO FIT HONDARRIBIA            	02:34	05:35	09:50        	19:18,66
3     	  3  	  2  	SANTURTZI TRANSPORTES Y GRUAS AGUADO	02:31	05:41	09:53        	19:20,84
4     	  3  	  3  	ORIO ARRAUNKETA ELKARTEA      	02:31	05:35	09:52        	19:23,00
5     	  3  	  1  	BERMEO URDAIBAI AVIA          	02:35	05:43	09:54        	19:30,08
6     	  1  	  4  	ZARAUTZ BABYAUTO              	02:31	05:39	10:05        	19:32,54
7     	  2  	  3  	LEKITTARRA ELECNOR            	02:31	05:39	10:02        	19:34,34
8     	  2  	  1  	DONOSTIARRA AMENABAR          	02:30	05:43	10:03        	19:38,76
9     	  1  	  3  	ONDARROA CIKAUTXO             	02:28	05:44	10:12        	19:42,88
10    	  1  	  2  	CR ARES                       	02:26	05:54	10:19        	19:49,08
11    	  1  	  1  	KAIKU VUSA                    	02:27	05:54	10:18        	20:14,32
12    	  2  	  2  	CABO                          	02:28	05:39	10:04        	Descal
```

# Contact / Harremana

You can contact me on Twitter (@estropadak) 

Twitter bidez kontaktatu nazakezue (@estropadak)