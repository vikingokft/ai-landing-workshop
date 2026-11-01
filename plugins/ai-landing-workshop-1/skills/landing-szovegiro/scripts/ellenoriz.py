#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ellenoriz.py - a landing-szovegiro kimenetének gyors ellenőrzése.

  python3 ellenoriz.py oldalak/<ajanlat>/szoveg.md

Megnézi, hogy megvan-e mind a 15 blokk a helyes sorrendben, és kiírja a kimaradt blokkokat,
a [KITÖLTENDŐ] helyeket és a tipográfiai hibákat (mondat közbeni gondolatjel, egyenes vagy angol idézőjel).
Hibának veszi, ha a céges agy belső jelölése (például [[HIÁNYZIK]], (következtetés, erősítsd meg),
(piaci hang, forrás: …)) bennmaradt a szövegben.
"""
import re
import sys

BLOKKOK = [
    'Hero', 'Problémák és következményeik', 'Vágyott eredmény',
    'Ajánlat bemutatása', 'Visszajelzések', 'Mechanizmus', 'Termékjellemzők, funkciók',
    'Előnyök', 'Bemutatkozás', 'Hitelességnövelő elemek: esettanulmány', 'Hogyan működik?',
    'Kinek igen, kinek nem', 'Hitelességnövelő elemek: logósor', 'CTA szakasz', 'GYIK',
]

# A céges agy belső jelölései: az agy/-nak szólnak, az oldalra nem kerülhetnek (szabalyok.md 7.)
BELSO_JELOLES = re.compile(
    r'\[\[\s*HIÁNYZIK[^\]]*\]\]'
    r'|\((?:következtetés|saját állítás|piaci hang|kockázatos állítás|kizárva|elmesélt|belső'
    r'|kitalált|megerősítendő|feltételezés)\b[^)]*\)',
    flags=re.I)


def main(path):
    md = open(path, encoding='utf-8').read()
    if md.startswith('---'):
        if '\n---' not in md[3:]:
            print('HIBA: a fájl eleji fejléc (---) nincs lezárva egy második --- sorral.')
            return 1
        test = md[3:].split('\n---', 1)[1]
    else:
        test = md
    fejek = re.findall(r'^##\s+(\d+)\.\s+(.+?)\s*$', test, flags=re.M)
    hibak, kimaradt, kitoltendo = [], [], []
    nevek = [re.sub(r'\s*✱\s*$', '', n) for _, n in fejek]
    if nevek != BLOKKOK:
        hibak.append(f'A blokkok sora nem az L1-é. Talált: {len(nevek)} blokk.')
        for i, (v, t) in enumerate(zip(BLOKKOK, nevek + [''] * len(BLOKKOK)), 1):
            if v != t:
                hibak.append(f'  {i}. helyen „{v}” kellene, ez áll: „{t}”')
    reszek = re.split(r'^##\s+\d+\.\s+.+$', test, flags=re.M)[1:]
    for (n, nev), resz in zip(fejek, reszek):
        szoveg = resz.strip()
        if szoveg.startswith('Kimarad:'):
            kimaradt.append(f'{n}. {nev}: {szoveg.splitlines()[0]}')
        for m in re.findall(r'\[KITÖLTENDŐ[^\]]*\]', szoveg):
            kitoltendo.append(f'{n}. {nev}: {m}')
        # a számtartomány nagykötőjele (60–90) helyes, csak a mondat közbeni gondolatjel hiba
        mondatkozi = re.sub(r'(?<=\d)–(?=\d)', '', szoveg)
        for jel, mi, hol in (('—', 'hosszú gondolatjel', szoveg), ('–', 'gondolatjel', mondatkozi),
                             ('"', 'egyenes idézőjel („…” kell; idézeten belül »…«, véleményben is, a szavakhoz nem nyúlva)', szoveg), ('“', 'angol idézőjel („…” kell; idézeten belül »…«)', szoveg)):
            if jel in hol:
                hibak.append(f'{n}. {nev}: {mi} a szövegben.')
        for m in BELSO_JELOLES.finditer(szoveg):
            hibak.append(f'{n}. {nev}: belső jelölés maradt a szövegben: „{m.group(0)}” (ez az agy/-nak szól, töröld vagy írd át).')
    figyelj, cimsorok = [], []
    for (n, nev), resz in zip(fejek, reszek):
        fv = re.search(r'^\*\*Felvezető:\*\*\s*(.+?)\s*$', resz, flags=re.M)
        for cs in re.findall(r'^###\s+(.+?)\s*$', resz, flags=re.M):
            db = len(re.findall(r'\w+', cs))
            cimsorok.append((n, nev, cs, db, fv.group(1) if fv else ''))
            if fv and fv.group(1).strip(' .') == cs.strip(' .'):
                figyelj.append(f'{n}. {nev}: a felvezető ugyanaz, mint a címsor.')
            if '!' in cs:
                figyelj.append(f'{n}. {nev}: felkiáltójel a címsorban.')
            fv = None
    elsok = [c[2].split()[0].lower() for c in cimsorok if c[1] != 'GYIK' and c[2].split()]
    for i in range(len(elsok) - 2):
        if elsok[i] == elsok[i + 1] == elsok[i + 2]:
            figyelj.append(f'Három címsor egymás után „{elsok[i]}” szóval kezdődik.')
    felv = sum(1 for c in cimsorok if c[4])
    szavak = len(re.findall(r'\w+', '\n'.join(reszek)))
    print(f'Blokkok: {len(fejek)} · szavak: {szavak} · címsorok: {len(cimsorok)}, ebből felvezetővel: {felv}')
    if cimsorok:
        print('\nCímsorok (szószám):')
        for n, nev, cs, db, f in cimsorok:
            if nev != 'GYIK':
                print(f'  {n}. {f + " · " if f else ""}{cs} ({db})')
    if figyelj:
        print('\nFIGYELJ (nem hiba, nézd át):')
        for x in figyelj:
            print('  - ' + x)
    for cim, lista in (('Kimaradt blokk', kimaradt), ('[KITÖLTENDŐ]', kitoltendo)):
        if lista:
            print(f'\n{cim} ({len(lista)}):')
            for x in lista:
                print('  - ' + x)
    if hibak:
        print('\nHIBA:')
        for h in hibak:
            print('  - ' + h)
        return 1
    print('\nRendben.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
