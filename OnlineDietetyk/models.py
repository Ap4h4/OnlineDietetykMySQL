from django.db import models

# Create your models here.
class Danie(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nazwa = models.CharField(db_column='Nazwa', max_length=50)  # Field name made lowercase.
    kategoria_dania = models.ForeignKey('KategorieDan', models.DO_NOTHING, db_column='Kategoria_dania')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Danie'


class DanieProdukt(models.Model):
    id_dania = models.ForeignKey(Danie, models.DO_NOTHING, db_column='Id_dania', primary_key=True)  # Field name made lowercase.
    id_produktu = models.ForeignKey('ProduktyZywn', models.DO_NOTHING, db_column='Id_produktu')  # Field name made lowercase.
    prod_na_100g = models.DecimalField(db_column='Ilosc_prod', max_digits=18, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Danie_produkt'
        unique_together = (('id_dania', 'id_produktu'),)


class DietaDanie(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    id_diety = models.ForeignKey('Diety', models.DO_NOTHING, db_column='Id_diety')  # Field name made lowercase.
    id_dania = models.ForeignKey(Danie, models.DO_NOTHING, db_column='Id_dania')  # Field name made lowercase.
    dzien = models.IntegerField(db_column='Dzien')  # Field name made lowercase.
    pora_dnia = models.ForeignKey('PoryPosilkow', models.DO_NOTHING, db_column='Pora_dnia', blank=True, null=True)  # Field name made lowercase.
    porcje = models.DecimalField(db_column='Porcje', max_digits=18, decimal_places=0)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'Dieta_danie'


class Diety(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nazwa = models.CharField(db_column='Nazwa', max_length=50)  # Field name made lowercase.
    typ = models.ForeignKey('TypDiety', models.DO_NOTHING, db_column='Typ')  # Field name made lowercase.
    data_dodania = models.DateField(db_column='Data_dodania')  # Field name made lowercase.
    wersja = models.CharField(db_column='Wersja', max_length=50, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'Diety'


class KategoriaProduktow(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nazwa = models.CharField(db_column='Nazwa', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Kategoria_produktow'


class KategorieDan(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nazwa = models.CharField(db_column='Nazwa', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Kategorie_dan'


class Pacjenci(models.Model):
    id_pacjenta = models.AutoField(db_column='Id_pacjenta', primary_key=True)
    nazwisko = models.CharField(db_column='Nazwisko', max_length=50)  # Field name made lowercase.
    imie = models.CharField(db_column='Imie', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    telefon = models.CharField(db_column='Telefon', max_length=50, blank=True, null=True)  # Field name made lowercase.
    data_ur = models.DateField(db_column='Data_ur')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Pacjenci'


class PacjentDieta(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    id_pacjenta = models.ForeignKey(Pacjenci, models.DO_NOTHING, db_column='Id_pacjenta')  # Field name made lowercase.
    id_diety = models.ForeignKey(Diety, models.DO_NOTHING, db_column='Id_diety')  # Field name made lowercase.
    aktywna = models.BooleanField(db_column='Aktywna')  # Field name made lowercase.
    data_rozpoczecia = models.DateField(db_column='Data_rozpoczecia', blank=True, null=True)  # Field name made lowercase.
    data_zakonczenia = models.DateField(db_column='Data_zakonczenia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pacjent_dieta'

class PoryPosilkow(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    pora_dnia = models.CharField(db_column='Pora_dnia', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pory_posilkow'

class ProduktSkladnik(models.Model):
    id_prod = models.ForeignKey('ProduktyZywn', models.DO_NOTHING, db_column='Id_prod', primary_key=True)  # Field name made lowercase.
    id_skl = models.ForeignKey('SkladnikiZyw', models.DO_NOTHING, db_column='Id_skl')  # Field name made lowercase.
    proc_skl = models.IntegerField(db_column='Proc_skl')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Produkt_skladnik'
        unique_together = (('id_prod', 'id_skl'),)


class ProduktyZywn(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nazwa = models.CharField(db_column='Nazwa', max_length=50)  # Field name made lowercase.
    kategoria_prod = models.ForeignKey(KategoriaProduktow, models.DO_NOTHING, db_column='Kategoria_prod')  # Field name made lowercase.
    kcal = models.DecimalField(db_column='Kcal', max_digits=18, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Produkty_zywn'


class SkladnikiZyw(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nazwa = models.CharField(db_column='Nazwa', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Skladniki_zyw'


class TypDiety(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    typ = models.CharField(db_column='Typ', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Typ_diety'


class Wizyty(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    id_pacjenta = models.ForeignKey(Pacjenci, models.DO_NOTHING, db_column='Id_pacjenta')  # Field name made lowercase.
    data = models.DateTimeField(db_column='Data')  # Field name made lowercase.
    potwierdzona = models.BooleanField(db_column='Potwierdzona', blank=True, null=True)  # Field name made lowercase.
    zakonczona = models.BooleanField(db_column='Zakonczona', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Wizyty'


class WynikiBadan(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    id_pacjenta = models.ForeignKey(Pacjenci, models.DO_NOTHING, db_column='Id_pacjenta')  # Field name made lowercase.
    data_badania = models.DateField(db_column='Data_badania')  # Field name made lowercase.
    waga = models.DecimalField(db_column='Waga', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    plytki_krwi = models.DecimalField(db_column='Plytki_krwi', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    bmi = models.DecimalField(db_column='BMI', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Wyniki_badan'

