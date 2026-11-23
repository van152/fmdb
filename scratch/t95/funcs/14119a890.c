__int64 __fastcall sub_14119A890(__int64 a1, int a2, __int64 **a3)
{
  __int64 v3; // rdi
  int v6; // ecx
  int v7; // ecx
  __int64 *v8; // rcx
  __int64 *v9; // rax
  __int64 v10; // rcx
  int v11; // esi
  __int64 v12; // rax
  __int64 *v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rcx
  char v17; // bl
  __int64 *v18; // rax
  __int64 v19; // rcx
  char v20; // bl
  __int64 *v21; // rax
  __int64 v22; // rcx
  char v23; // bl
  __int64 *v24; // rax
  __int64 v25; // rcx
  __int64 v26; // rcx
  int v27; // eax
  int v28; // ecx
  char v29; // bl
  __int64 *v30; // rax
  __int64 v31; // rcx
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rdx
  unsigned __int64 v35; // r13
  __int64 *v36; // r15
  __int64 v37; // rsi
  __int64 v38; // r14
  unsigned __int64 v39; // rcx
  __int64 v40; // r8
  __int64 v41; // rcx
  bool v42; // al
  char v43; // bl
  __int64 *v44; // rax
  __int64 v45; // rcx
  __int64 *v46; // rcx
  __int64 *v47; // rax
  __int64 *v48; // rcx
  __int64 v49; // r15
  __int64 v50; // rax
  __int64 v51; // [rsp+20h] [rbp-30h]
  __int64 *v52; // [rsp+28h] [rbp-28h] BYREF
  __int64 *v53; // [rsp+30h] [rbp-20h]
  __int64 *v54; // [rsp+38h] [rbp-18h] BYREF
  __int64 v55; // [rsp+40h] [rbp-10h]
  unsigned __int64 v56; // [rsp+48h] [rbp-8h]
  __int64 v57; // [rsp+50h] [rbp+0h]

  v57 = -2;
  LOBYTE(v3) = 1;
  if ( a2 <= 1347188578 )
  {
    if ( a2 <= 1347184225 )
    {
      if ( a2 <= 1347183217 )
      {
        if ( (unsigned int)(a2 - 1347174723) > 0x11 || (v7 = 196609, !_bittest(&v7, a2 - 1347174723)) )
        {
          if ( a2 != 1347178055 )
            goto LABEL_97;
        }
      }
      else if ( (unsigned int)(a2 - 1347183469) > 7 || (v6 = 161, !_bittest(&v6, a2 - 1347183469)) )
      {
        if ( a2 != 1347183218 && a2 != 1347183972 )
          goto LABEL_97;
      }
      goto LABEL_53;
    }
    if ( a2 > 1347186021 )
    {
      if ( (unsigned int)(a2 - 1347186530) >= 2 && a2 != 1347186022 && a2 != 1347187566 )
        goto LABEL_97;
    }
    else if ( a2 > 1347184994 )
    {
      if ( a2 != 1347184995 && a2 != 1347186019 )
        goto LABEL_97;
    }
    else if ( a2 != 1347184226 && a2 != 1347184236 )
    {
      goto LABEL_97;
    }
LABEL_53:
    v15 = *(_QWORD *)(a1 + 48);
    if ( v15 != 0 )
      sub_141578930(v15, a2, a3);
    return (unsigned int)v3;
  }
  if ( a2 > 1347446385 )
  {
    if ( a2 <= 1347449966 )
    {
      if ( a2 > 1347448951 )
      {
        if ( a2 == 1347448952 )
        {
          v43 = *(_BYTE *)(a1 + 88);
          v12 = sub_14083D4F0(a1) + 24;
          LOBYTE(v55) = (v43 & 2) != 0;
          v54 = (__int64 *)v12;
          if ( &v54 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v44 = v54;
            v45 = v55;
            a3[1] = (__int64 *)v55;
            *a3 = v44;
            v12 = sub_14083D4F0(v45) + 8;
            v55 = 0;
            v54 = (__int64 *)v12;
          }
        }
        else
        {
          if ( a2 != 1347449958 )
            goto LABEL_97;
          v17 = *(_BYTE *)(a1 + 88);
          v12 = sub_14083D4F0(a1) + 24;
          LOBYTE(v55) = (v17 & 8) != 0;
          v54 = (__int64 *)v12;
          if ( &v54 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v18 = v54;
            v19 = v55;
            a3[1] = (__int64 *)v55;
            *a3 = v18;
            v12 = sub_14083D4F0(v19) + 8;
            v55 = 0;
            v54 = (__int64 *)v12;
          }
        }
        goto LABEL_94;
      }
      if ( a2 != 1347446386 )
      {
        if ( a2 == 1347447155 )
          return (unsigned int)v3;
        goto LABEL_97;
      }
      v26 = *(_QWORD *)(a1 + 56);
      if ( v26 == 0 )
      {
LABEL_80:
        v27 = -1;
        v28 = -1;
LABEL_81:
        v54 = (__int64 *)__PAIR64__(v28, v27);
        sub_140FE72B0(&v54, 1416914273, a3);
        return (unsigned int)v3;
      }
    }
    else
    {
      if ( a2 > 1347450735 )
      {
        if ( a2 != 1347450736 )
        {
          if ( a2 == 1348887138 )
            goto LABEL_53;
          if ( a2 == 1349346420 )
          {
            if ( *(char *)(a1 + 90) == -1 )
            {
              (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                qword_141B5A4A0,
                &qword_141B5A4A0,
                &v54);
            }
            else
            {
              LODWORD(v55) = *(char *)(a1 + 90);
              v54 = (__int64 *)(sub_14083D4F0(a1) + 40);
            }
            if ( &v54 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              (*(void (__fastcall **)(__int64 *, __int64 **, __int64 **))(*v54 + 24))(v54, &v54, a3);
            }
LABEL_104:
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v54 + 16))(v54, &v54);
            return (unsigned int)v3;
          }
          goto LABEL_97;
        }
        v23 = *(_BYTE *)(a1 + 88);
        v12 = sub_14083D4F0(a1) + 24;
        LOBYTE(v55) = (v23 & 0x10) != 0;
        v54 = (__int64 *)v12;
        if ( &v54 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v24 = v54;
          v25 = v55;
          a3[1] = (__int64 *)v55;
          *a3 = v24;
          v12 = sub_14083D4F0(v25) + 8;
          v55 = 0;
          v54 = (__int64 *)v12;
        }
        goto LABEL_94;
      }
      if ( a2 != 1347449967 )
      {
        if ( a2 != 1347449977 )
          goto LABEL_97;
        v11 = *(char *)(a1 + 89);
        v12 = sub_14083D4F0(a1) + 40;
        LODWORD(v55) = v11;
        v54 = (__int64 *)v12;
        if ( &v54 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v13 = v54;
          v14 = v55;
          a3[1] = (__int64 *)v55;
          *a3 = v13;
          v12 = sub_14083D4F0(v14) + 8;
          v55 = 0;
          v54 = (__int64 *)v12;
        }
        goto LABEL_94;
      }
      v26 = *(_QWORD *)(a1 + 64);
      if ( v26 == 0 )
        goto LABEL_80;
    }
    v27 = *(_DWORD *)(v26 + 12);
    v28 = *(_DWORD *)(v26 + 16);
    if ( v28 == 0 )
      v28 = v27;
    goto LABEL_81;
  }
  if ( a2 <= 1347445860 )
  {
    if ( a2 <= 1347445613 )
    {
      if ( a2 != 1347188579 && a2 != 1347188583 )
        goto LABEL_97;
      goto LABEL_53;
    }
    if ( a2 != 1347445614 )
    {
      if ( a2 == 1347445857 )
        return (unsigned int)v3;
      goto LABEL_97;
    }
    sub_1407C9510(&v54);
    v32 = *(_QWORD *)(a1 + 24);
    v33 = *(_QWORD *)(a1 + 32);
    v34 = v33 - v32;
    v35 = (v33 - v32) >> 3;
    v36 = v54;
    if ( (__int64)(v56 - (_QWORD)v54) >> 3 >= v35 )
    {
      if ( v33 == v32 )
      {
LABEL_99:
        sub_14083DB80(&v52, &v54);
        v46 = *a3;
        if ( &v52 == a3 )
        {
          LOBYTE(v3) = 1;
        }
        else
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v46 + 16))(v46, a3);
          LOBYTE(v3) = 1;
          v47 = v52;
          v48 = v53;
          a3[1] = v53;
          *a3 = v47;
          v46 = (__int64 *)(sub_14083D4F0(v48) + 8);
          v53 = nullptr;
          v52 = v46;
        }
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v46 + 16))(v46, &v52);
        sub_14083B0A0(&v54);
        return (unsigned int)v3;
      }
    }
    else
    {
      if ( v34 < 0 )
        sub_1400526C0(v33, v34);
      v37 = v55;
      v38 = sub_1407E4490(qword_141ABD470, v34);
      sub_141758A00(v38, v54, v55 - (_QWORD)v54);
      if ( v54 != nullptr )
      {
        v39 = v56 - (_QWORD)v54;
        if ( v56 - (_QWORD)v54 == -1 )
          v39 = *(unsigned int *)((char *)v54 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v40 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v40) >> 3 > v39)
          && (v41 = *(_QWORD *)(v40 + 8 * v39)) != 0 )
        {
          v51 = v41;
          MEMORY[0x1419475D8](v41 + 32, (char *)v54 - *(unsigned int *)(v41 + 120));
          v33 = v51;
          v42 = *(_BYTE *)(v51 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v51 + 64)) != 0;
          if ( !v42 && *(_BYTE *)(v51 + 97) != 0 )
            sub_1412D33C0(v51);
        }
        else
        {
          MEMORY[0x141948990]((char *)v54 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      v54 = (__int64 *)v38;
      v55 = v38 + v37 - (_QWORD)v36;
      v56 = v38 + 8 * v35;
    }
    v49 = 0;
    do
    {
      v3 = *(_QWORD *)(*(_QWORD *)(a1 + 24) + 8 * v49);
      if ( v3 != 0 )
      {
        v50 = sub_14083D4F0(v33);
        v53 = nullptr;
        v52 = (__int64 *)(v50 + 8);
        sub_14119C030(v3, &v52);
        sub_14083B5F0(&v54, &v52);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v52 + 16))(v52, &v52);
      }
      ++v49;
    }
    while ( v35 != v49 );
    goto LABEL_99;
  }
  if ( a2 > 1347446372 )
  {
    if ( a2 == 1347446373 )
    {
      if ( *(int *)(a1 + 84) < 0 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v54);
      }
      else
      {
        LODWORD(v55) = *(_DWORD *)(a1 + 84);
        v54 = (__int64 *)(sub_14083D4F0(a1) + 40);
      }
      if ( &v54 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        (*(void (__fastcall **)(__int64 *, __int64 **, __int64 **))(*v54 + 24))(v54, &v54, a3);
      }
      goto LABEL_104;
    }
    if ( a2 != 1347446383 )
    {
LABEL_97:
      LODWORD(v3) = 0;
      return (unsigned int)v3;
    }
    v20 = *(_BYTE *)(a1 + 88) & 1;
    v12 = sub_14083D4F0(a1) + 24;
    LOBYTE(v55) = v20;
    v54 = (__int64 *)v12;
    if ( &v54 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v21 = v54;
      v22 = v55;
      a3[1] = (__int64 *)v55;
      *a3 = v21;
      v12 = sub_14083D4F0(v22) + 8;
      v55 = 0;
      v54 = (__int64 *)v12;
    }
LABEL_94:
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v12 + 16LL))(v12, &v54);
    return (unsigned int)v3;
  }
  if ( a2 == 1347445861 )
  {
    v29 = *(_BYTE *)(a1 + 88);
    v12 = sub_14083D4F0(a1) + 24;
    LOBYTE(v55) = (v29 & 4) != 0;
    v54 = (__int64 *)v12;
    if ( &v54 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v30 = v54;
      v31 = v55;
      a3[1] = (__int64 *)v55;
      *a3 = v30;
      v12 = sub_14083D4F0(v31) + 8;
      v55 = 0;
      v54 = (__int64 *)v12;
    }
    goto LABEL_94;
  }
  if ( a2 != 1347445876 )
    goto LABEL_97;
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
  LODWORD(v55) = ((*(_WORD *)(a1 + 80) & 0x1FF) << 8)
               | (*(unsigned __int16 *)(a1 + 80) >> 9)
               | (*(unsigned __int16 *)(a1 + 82) << 17);
  v8 = &qword_141B5C8A0;
  v54 = &qword_141B5C8A0;
  if ( &v54 != a3 )
  {
    (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
    v9 = v54;
    v10 = v55;
    a3[1] = (__int64 *)v55;
    *a3 = v9;
    v8 = (__int64 *)(sub_14083D4F0(v10) + 8);
    v55 = 0;
    v54 = v8;
  }
  (*(void (__fastcall **)(__int64 *, __int64 **))(*v8 + 16))(v8, &v54);
  return (unsigned int)v3;
}
