 2888  sed -i -e '/^Rekeninghouder/d' -e '/^Personal Account/d' -e '/^Periode/d' -e '/Bij- en afschrijvingen/d' -e '/Aantal afschrijvingen/d' -e '/Totaal afgeschreven/d'  -e '/Bedrag af/d' -e '/^Saldo/d' -e '/^Datum/d'  test.out
 3127  history | grep sed | grep 2888
