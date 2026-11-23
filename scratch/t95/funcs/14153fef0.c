char __fastcall sub_14153FEF0(__int64 a1, int a2, __int128 *a3)
{
  char result; // al
  __int64 *v6; // rcx
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // r8
  __int64 v10; // rcx
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 v13; // r8
  __int64 v14; // rcx
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v17; // r9
  __int64 v18; // rcx
  __int64 v19; // rcx
  __int64 v20; // rax
  __int64 v21; // rcx
  __int64 v22; // rax
  __int64 v23; // rcx
  __int64 v24; // rcx
  __int64 v25; // rax
  __int64 v26; // r8
  __int64 v27; // rcx
  __int64 v28; // rcx
  __int64 v29; // rax
  __int64 v30; // rcx
  __int64 v31; // rcx
  __int64 v32; // rax
  __int64 v33; // r8
  __int64 v34; // rcx
  __int64 v35; // rcx
  __int64 v36; // rax
  __int64 v37; // r8
  __int64 v38; // rcx
  __int64 v39; // rcx
  __int64 v40; // rax
  __int64 v41; // rcx
  __int64 v42; // rcx
  __int64 v43; // rax
  __int64 v44; // rcx
  __int64 v45; // rcx
  __int64 v46; // rdx
  __int64 v47; // rcx
  __int64 v48; // rbx
  __int64 v49; // rdx
  __int64 v50; // rdi
  __int64 v51; // rbx
  int v52; // edi
  __int64 *v53; // rdi
  __int64 v54; // rcx
  int v55; // eax
  int v56; // ecx
  __int64 v57; // rcx
  __int64 v58; // rbx
  __int64 v59; // rdx
  __int64 v60; // rdi
  __int64 v61; // rbx
  __int64 v62; // rcx
  __int64 v63; // rbx
  __int64 v64; // rdx
  __int64 v65; // rdi
  __int64 v66; // rbx
  unsigned __int64 v67; // rcx
  __int64 v68; // rbx
  __int64 v69; // rsi
  unsigned __int64 v70; // rcx
  __int64 v71; // rbx
  __int64 v72; // rsi
  int v73; // edi
  __int128 *v74; // [rsp+20h] [rbp-40h] BYREF
  __int64 v75; // [rsp+28h] [rbp-38h] BYREF
  __int64 v76; // [rsp+30h] [rbp-30h]
  __int64 v77; // [rsp+38h] [rbp-28h]
  __int128 v78; // [rsp+40h] [rbp-20h] BYREF
  __int64 v79; // [rsp+50h] [rbp-10h]
  __int64 v80; // [rsp+60h] [rbp+0h]

  v80 = -2;
  result = 0;
  if ( a2 > 1768846187 )
  {
    if ( a2 > 1886151780 )
    {
      if ( a2 != 1886151781 )
      {
        if ( a2 == 1886155372 )
        {
          v43 = sub_140FE84D0();
          if ( v43 == 0
            || (v44 = *(_QWORD *)(a1 + 24)) == 0
            || ((v9 = 0, *(_BYTE *)(v44 + 47) != 0) ? (v45 = 0) : (v45 = *(_QWORD *)(v44 + 48)), v43 != v45) )
          {
            LOBYTE(v9) = 1;
          }
          v46 = a1;
        }
        else
        {
          if ( a2 != 1886155378 )
            return result;
          v16 = sub_140FE84D0();
          if ( v16 != 0
            && (v18 = *(_QWORD *)(a1 + 24)) != 0
            && (*(_BYTE *)(v18 + 47) != 0 ? (v19 = 0) : (v19 = *(_QWORD *)(v18 + 48)), v16 == v19) )
          {
            LOBYTE(v9) = 1;
          }
          else
          {
            v9 = 0;
          }
          v46 = a1;
        }
        LOBYTE(v17) = 1;
        goto LABEL_131;
      }
      v40 = sub_140FE84D0();
      if ( v40 == 0
        || (v41 = *(_QWORD *)(a1 + 24)) == 0
        || ((v9 = 0, *(_BYTE *)(v41 + 47) != 0) ? (v42 = 0) : (v42 = *(_QWORD *)(v41 + 48)), v40 != v42) )
      {
        LOBYTE(v9) = 1;
      }
      v46 = a1;
    }
    else
    {
      if ( a2 == 1768846188 )
      {
        v25 = sub_140FE84D0();
        if ( v25 != 0
          && (v27 = *(_QWORD *)(a1 + 24)) != 0
          && (*(_BYTE *)(v27 + 47) != 0 ? (v28 = 0) : (v28 = *(_QWORD *)(v27 + 48)), v25 == v28) )
        {
          LOBYTE(v26) = 1;
        }
        else
        {
          v26 = 0;
        }
        sub_141732D00(&v75, a1, v26);
        v48 = v76 - v75;
        v78 = 0;
        v79 = 0;
        v49 = v76 - v75;
        if ( v76 == v75 )
          goto LABEL_98;
        if ( v76 - v75 >= 0 )
        {
LABEL_73:
          v50 = sub_1407E4490(qword_141ABD470, v49);
          *(_QWORD *)&v78 = v50;
          v79 = v50 + 8 * (v48 >> 3);
          v51 = v76 - v75;
          sub_141758A00(v50, v75, v76 - v75);
          *((_QWORD *)&v78 + 1) = v50 + v51;
LABEL_98:
          v74 = &v78;
          sub_1415420A0(&v74, a3);
          goto LABEL_135;
        }
LABEL_97:
        sub_1400526C0(v47, v49);
      }
      if ( a2 == 1869902957 )
      {
        v29 = sub_140FE84D0();
        if ( v29 != 0
          && (v30 = *(_QWORD *)(a1 + 24)) != 0
          && (*(_BYTE *)(v30 + 47) != 0 ? (v31 = 0) : (v31 = *(_QWORD *)(v30 + 48)), v29 == v31) )
        {
          v53 = (__int64 *)(a1 + 32);
        }
        else
        {
          v53 = (__int64 *)(a1 + 24);
        }
        v54 = *v53;
        if ( *v53 != 0 )
        {
          v55 = *(_DWORD *)(v54 + 12);
          v56 = *(_DWORD *)(v54 + 16);
          if ( v56 == 0 )
            v56 = v55;
        }
        else
        {
          v55 = -1;
          v56 = -1;
        }
        *(_QWORD *)&v78 = __PAIR64__(v56, v55);
        sub_140FE72B0(&v78, 1416914273, a3);
        return 1;
      }
      if ( a2 != 1886151026 )
        return result;
      v8 = sub_140FE84D0();
      if ( v8 != 0
        && (v10 = *(_QWORD *)(a1 + 24)) != 0
        && (*(_BYTE *)(v10 + 47) != 0 ? (v11 = 0) : (v11 = *(_QWORD *)(v10 + 48)), v8 == v11) )
      {
        LOBYTE(v9) = 1;
      }
      else
      {
        v9 = 0;
      }
      v46 = a1;
    }
    v17 = 0;
LABEL_131:
    sub_141731E80(&v75, v46, v9, v17);
    v63 = v76 - v75;
    v78 = 0;
    v79 = 0;
    v64 = v76 - v75;
    if ( v76 != v75 )
    {
      if ( v76 - v75 < 0 )
        sub_1400526C0(v62, v64);
      v65 = sub_1407E4490(qword_141ABD470, v64);
      *(_QWORD *)&v78 = v65;
      v79 = v65 + 8 * (v63 >> 3);
      v66 = v76 - v75;
      sub_141758A00(v65, v75, v76 - v75);
      *((_QWORD *)&v78 + 1) = v65 + v66;
    }
    v74 = &v78;
    sub_1415418B0(&v74, a3);
LABEL_135:
    if ( (_QWORD)v78 == 0 )
      goto LABEL_146;
    v67 = v79 - v78;
    if ( v79 - (_QWORD)v78 == -1 )
    {
      v67 = *(unsigned int *)(v78 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_145;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_145;
    }
    v68 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v68) >> 3 > v67 )
    {
      v69 = *(_QWORD *)(v68 + 8 * v67);
      if ( v69 != 0 )
      {
        MEMORY[0x1419475D8](v69 + 32, v78 - *(unsigned int *)(v69 + 120));
        if ( (*(_BYTE *)(v69 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v69 + 64)) == 0)
          && *(_BYTE *)(v69 + 97) != 0 )
        {
          sub_1412D33C0(v69);
        }
LABEL_146:
        if ( v75 == 0 )
          return 1;
        v70 = v77 - v75;
        if ( v77 - v75 == -1 )
        {
          v70 = *(unsigned int *)(v75 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
LABEL_156:
            MEMORY[0x141948990](v75 - *(unsigned int *)(qword_141ABD470 + 48));
            return 1;
          }
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_156;
        }
        v71 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v71) >> 3 > v70 )
        {
          v72 = *(_QWORD *)(v71 + 8 * v70);
          if ( v72 != 0 )
          {
            MEMORY[0x1419475D8](v72 + 32, v75 - *(unsigned int *)(v72 + 120));
            if ( (*(_BYTE *)(v72 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v72 + 64)) == 0)
              && *(_BYTE *)(v72 + 97) != 0 )
            {
              sub_1412D33C0(v72);
            }
            return 1;
          }
        }
        goto LABEL_156;
      }
    }
LABEL_145:
    MEMORY[0x141948990](v78 - *(unsigned int *)(qword_141ABD470 + 48));
    goto LABEL_146;
  }
  if ( a2 > 1685217643 )
  {
    switch ( a2 )
    {
      case 1685217644:
        v32 = sub_140FE84D0();
        if ( v32 != 0
          && (v34 = *(_QWORD *)(a1 + 24)) != 0
          && (*(_BYTE *)(v34 + 47) != 0 ? (v35 = 0) : (v35 = *(_QWORD *)(v34 + 48)), v32 == v35) )
        {
          LOBYTE(v33) = 1;
        }
        else
        {
          v33 = 0;
        }
        sub_141732730(&v75, a1, v33);
        v58 = v76 - v75;
        v78 = 0;
        v79 = 0;
        v59 = v76 - v75;
        if ( v76 == v75 )
          goto LABEL_120;
        if ( v76 - v75 >= 0 )
        {
LABEL_119:
          v60 = sub_1407E4490(qword_141ABD470, v59);
          *(_QWORD *)&v78 = v60;
          v79 = v60 + 8 * (v58 >> 3);
          v61 = v76 - v75;
          sub_141758A00(v60, v75, v76 - v75);
          *((_QWORD *)&v78 + 1) = v60 + v61;
LABEL_120:
          v74 = &v78;
          sub_141541B90(&v74, a3);
          goto LABEL_135;
        }
        break;
      case 1701077356:
        v36 = sub_140FE84D0();
        if ( v36 == 0
          || (v38 = *(_QWORD *)(a1 + 24)) == 0
          || ((v37 = 0, *(_BYTE *)(v38 + 47) != 0) ? (v39 = 0) : (v39 = *(_QWORD *)(v38 + 48)), v36 != v39) )
        {
          LOBYTE(v37) = 1;
        }
        sub_141732730(&v75, a1, v37);
        v58 = v76 - v75;
        v78 = 0;
        v79 = 0;
        v59 = v76 - v75;
        if ( v76 == v75 )
          goto LABEL_120;
        if ( v76 - v75 >= 0 )
          goto LABEL_119;
        break;
      case 1702390131:
        v12 = sub_140FE84D0();
        if ( v12 == 0
          || (v14 = *(_QWORD *)(a1 + 24)) == 0
          || ((v13 = 0, *(_BYTE *)(v14 + 47) != 0) ? (v15 = 0) : (v15 = *(_QWORD *)(v14 + 48)), v12 != v15) )
        {
          LOBYTE(v13) = 1;
        }
        sub_141732D00(&v75, a1, v13);
        v48 = v76 - v75;
        v78 = 0;
        v79 = 0;
        v49 = v76 - v75;
        if ( v76 == v75 )
          goto LABEL_98;
        if ( v76 - v75 >= 0 )
          goto LABEL_73;
        goto LABEL_97;
      default:
        return result;
    }
    sub_1400526C0(v57, v59);
  }
  switch ( a2 )
  {
    case 1634495602:
      v20 = sub_140FE84D0();
      if ( v20 != 0
        && (v21 = *(_QWORD *)(a1 + 24)) != 0
        && (*(_BYTE *)(v21 + 47) != 0 ? (v21 = 0) : (v21 = *(_QWORD *)(v21 + 48)), v20 == v21)
        || (v52 = *(_DWORD *)(a1 + 44)) == 0 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v78);
      }
      else
      {
        DWORD2(v78) = v52;
        *(_QWORD *)&v78 = sub_14083D4F0(v21) + 40;
      }
      if ( &v78 != a3 )
      {
        (*(void (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)a3 + 16LL))(*(_QWORD *)a3, a3);
        (*(void (__fastcall **)(_QWORD, __int128 *, __int128 *))(*(_QWORD *)v78 + 24LL))(v78, &v78, a3);
      }
      break;
    case 1634495603:
      v22 = sub_140FE84D0();
      if ( v22 != 0
        && (v23 = *(_QWORD *)(a1 + 24)) != 0
        && (*(_BYTE *)(v23 + 47) != 0 ? (v24 = 0) : (v24 = *(_QWORD *)(v23 + 48)),
            v22 == v24 && (v73 = *(_DWORD *)(a1 + 44)) != 0) )
      {
        DWORD2(v78) = v73;
        *(_QWORD *)&v78 = sub_14083D4F0(v24) + 40;
      }
      else
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v78);
      }
      if ( &v78 != a3 )
      {
        (*(void (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)a3 + 16LL))(*(_QWORD *)a3, a3);
        (*(void (__fastcall **)(_QWORD, __int128 *, __int128 *))(*(_QWORD *)v78 + 24LL))(v78, &v78, a3);
      }
      break;
    case 1684108389:
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          sub_140DBC9B0(&qword_141B5C8A0);
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      DWORD2(v78) = ((*(_WORD *)(a1 + 40) & 0x1FF) << 8)
                  | (*(unsigned __int16 *)(a1 + 40) >> 9)
                  | (*(unsigned __int16 *)(a1 + 42) << 17);
      v6 = &qword_141B5C8A0;
      *(_QWORD *)&v78 = &qword_141B5C8A0;
      if ( &v78 != a3 )
      {
        (*(void (__fastcall **)(_QWORD, __int128 *))(**(_QWORD **)a3 + 16LL))(*(_QWORD *)a3, a3);
        v7 = *((_QWORD *)&v78 + 1);
        *a3 = v78;
        v6 = (__int64 *)(sub_14083D4F0(v7) + 8);
        v78 = (unsigned __int64)v6;
      }
      (*(void (__fastcall **)(__int64 *, __int128 *))(*v6 + 16))(v6, &v78);
      return 1;
    default:
      return result;
  }
  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v78 + 16LL))(v78, &v78);
  return 1;
}
