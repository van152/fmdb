__int64 __fastcall sub_14119D0F0(__int64 a1, int a2, unsigned __int64 *a3)
{
  __int64 *v4; // rdi
  __int64 v5; // rcx
  int v6; // eax
  int v7; // ecx
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rcx
  int v11; // eax
  int v12; // edi
  __int64 v13; // rax
  unsigned __int64 v14; // rax
  unsigned __int64 v15; // rcx
  unsigned __int64 v16; // rax
  unsigned __int64 v17; // rcx
  __int64 v18; // rcx
  int v19; // eax
  __int64 *v20; // rdx
  __int64 v21; // rcx
  __int64 v22; // rdx
  __int64 v23; // rdx
  bool v24; // zf
  __int64 v25; // rax
  __int64 v26; // rax
  int v27; // ecx
  __int64 v28; // rcx
  int v29; // eax
  int v30; // ecx
  char v31; // bl
  __int64 v32; // rax
  unsigned __int64 v33; // rax
  unsigned __int64 v34; // rcx
  int v35; // edi
  unsigned __int64 v36; // rax
  unsigned __int64 v37; // rcx
  unsigned __int64 v38; // rax
  unsigned __int64 v39; // rcx
  int v40; // edi
  unsigned __int64 v41; // rax
  unsigned __int64 v42; // rcx
  unsigned __int64 v43; // rax
  unsigned __int64 v44; // rcx
  __int64 v45; // rcx
  __int64 *v46; // rdx
  __int64 v47; // rcx
  __int64 v48; // rdx
  __int64 v49; // rcx
  int v50; // eax
  int v51; // ecx
  char v52; // bl
  unsigned __int64 v53; // rax
  unsigned __int64 v54; // rcx
  __int64 v55; // rdx
  __int64 v57; // rcx
  __int64 v58; // rdx
  int v59; // ecx
  unsigned __int64 v60; // [rsp+30h] [rbp-10h] BYREF
  unsigned __int64 v61; // [rsp+38h] [rbp-8h]
  __int64 v62; // [rsp+40h] [rbp+0h]

  v62 = -2;
  LODWORD(v4) = 0;
  if ( a2 > 1416456300 )
  {
    if ( a2 > 1416919407 )
    {
      if ( a2 > 1953328750 )
      {
        if ( a2 == 1953328751 )
        {
          v52 = *(_BYTE *)(a1 + 71);
          v32 = sub_14083D4F0(a1) + 24;
          LOBYTE(v61) = (v52 & 4) != 0;
          v60 = v32;
          if ( &v60 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v53 = v60;
            v54 = v61;
            a3[1] = v61;
            *a3 = v53;
            v32 = sub_14083D4F0(v54) + 8;
            v61 = 0;
            v60 = v32;
          }
        }
        else
        {
          if ( a2 != 1953328758 )
            return (unsigned int)v4;
          v31 = *(_BYTE *)(a1 + 71);
          v32 = sub_14083D4F0(a1) + 24;
          LOBYTE(v61) = (v31 & 2) != 0;
          v60 = v32;
          if ( &v60 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v33 = v60;
            v34 = v61;
            a3[1] = v61;
            *a3 = v33;
            v32 = sub_14083D4F0(v34) + 8;
            v61 = 0;
            v60 = v32;
          }
        }
        (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v32 + 16LL))(v32, &v60);
LABEL_100:
        LOBYTE(v4) = 1;
        return (unsigned int)v4;
      }
      if ( a2 == 1416919408 )
      {
        LODWORD(v4) = *(char *)(a1 + 68);
        if ( (_DWORD)v4 != -1 )
        {
          v13 = sub_14083D4F0(a1) + 40;
          LODWORD(v61) = (_DWORD)v4;
          v60 = v13;
          if ( &v60 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v43 = v60;
            v44 = v61;
            a3[1] = v61;
            *a3 = v43;
            v13 = sub_14083D4F0(v44) + 8;
            v61 = 0;
            v60 = v13;
          }
          goto LABEL_76;
        }
      }
      else
      {
        if ( a2 != 1417111661 )
          return (unsigned int)v4;
        LODWORD(v4) = *(char *)(a1 + 69);
        if ( *(_BYTE *)(a1 + 69) != 0 )
        {
          v13 = sub_14083D4F0(a1) + 40;
          LODWORD(v61) = (_DWORD)v4;
          v60 = v13;
          if ( &v60 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v16 = v60;
            v17 = v61;
            a3[1] = v61;
            *a3 = v16;
            v13 = sub_14083D4F0(v17) + 8;
            v61 = 0;
            v60 = v13;
          }
          goto LABEL_76;
        }
      }
    }
    else
    {
      if ( a2 > 1416852584 )
      {
        if ( a2 == 1416852585 )
        {
          v49 = *(_QWORD *)(a1 + 48);
          if ( v49 != 0 )
          {
            v50 = *(_DWORD *)(v49 + 12);
            v51 = *(_DWORD *)(v49 + 16);
            if ( v51 == 0 )
              v51 = v50;
          }
          else
          {
            v50 = -1;
            v51 = -1;
          }
          v60 = __PAIR64__(v51, v50);
          v55 = 1937006948;
          goto LABEL_99;
        }
        if ( a2 == 1416914273 )
        {
          v25 = *(_QWORD *)(a1 + 24);
          LODWORD(v4) = -1;
          if ( v25 != 0 )
          {
            v26 = sub_1411DC000(v25, *(unsigned __int8 *)(a1 + 68), 0, 0, 1, 0);
            v27 = -1;
            if ( v26 != 0 )
            {
              LODWORD(v4) = *(_DWORD *)(v26 + 12);
              v27 = *(_DWORD *)(v26 + 16);
              if ( v27 == 0 )
                v27 = *(_DWORD *)(v26 + 12);
            }
          }
          else
          {
            v27 = -1;
          }
          v60 = __PAIR64__(v27, (unsigned int)v4);
          v55 = 1416914273;
          goto LABEL_99;
        }
        return (unsigned int)v4;
      }
      if ( a2 != 1416456301 )
      {
        if ( a2 != 1416586351 )
          return (unsigned int)v4;
        v8 = *(_QWORD *)(a1 + 24);
        LODWORD(v4) = -1;
        if ( v8 != 0
          && (v9 = sub_1411DC000(v8, *(unsigned __int8 *)(a1 + 68), 0, 0, 1, 0)) != 0
          && *(_QWORD *)(v9 + 48) != 0 )
        {
          v10 = *(_QWORD *)(v9 + 80);
          v11 = -1;
          if ( v10 != 0 )
          {
            LODWORD(v4) = *(_DWORD *)(v10 + 12);
            v11 = *(_DWORD *)(v10 + 16);
            if ( v11 == 0 )
              v11 = *(_DWORD *)(v10 + 12);
          }
        }
        else
        {
          v11 = -1;
        }
        v60 = __PAIR64__(v11, (unsigned int)v4);
LABEL_98:
        v55 = 1668246896;
LABEL_99:
        sub_140FE72B0(&v60, v55, a3);
        goto LABEL_100;
      }
      LODWORD(v4) = *(char *)(a1 + 70);
      if ( *(_BYTE *)(a1 + 70) != 0 )
      {
        v13 = sub_14083D4F0(a1) + 40;
        LODWORD(v61) = (_DWORD)v4;
        v60 = v13;
        if ( &v60 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v38 = v60;
          v39 = v61;
          a3[1] = v61;
          *a3 = v38;
          v13 = sub_14083D4F0(v39) + 8;
          v61 = 0;
          v60 = v13;
        }
        goto LABEL_76;
      }
    }
    LOBYTE(v4) = 1;
    if ( a3 != (unsigned __int64 *)&qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, unsigned __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    return (unsigned int)v4;
  }
  if ( a2 > 1131245152 )
  {
    if ( a2 <= 1415870056 )
    {
      if ( a2 == 1131245153 )
      {
        v40 = *(_DWORD *)(a1 + 64);
        v13 = sub_14083D4F0(a1) + 40;
        LODWORD(v61) = v40;
        v60 = v13;
        if ( &v60 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v41 = v60;
          v42 = v61;
          a3[1] = v61;
          *a3 = v41;
          v13 = sub_14083D4F0(v42) + 8;
          v61 = 0;
          v60 = v13;
        }
      }
      else
      {
        if ( a2 != 1131247713 )
          return (unsigned int)v4;
        v12 = *(_DWORD *)(a1 + 60);
        v13 = sub_14083D4F0(a1) + 40;
        LODWORD(v61) = v12;
        v60 = v13;
        if ( &v60 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v14 = v60;
          v15 = v61;
          a3[1] = v61;
          *a3 = v14;
          v13 = sub_14083D4F0(v15) + 8;
          v61 = 0;
          v60 = v13;
        }
      }
      goto LABEL_76;
    }
    if ( a2 == 1415870057 )
    {
      v28 = *(_QWORD *)(a1 + 32);
      if ( v28 != 0 )
      {
LABEL_54:
        v29 = *(_DWORD *)(v28 + 12);
        v30 = *(_DWORD *)(v28 + 16);
        goto LABEL_55;
      }
    }
    else
    {
      if ( a2 != 1416389737 )
        return (unsigned int)v4;
      v28 = *(_QWORD *)(a1 + 40);
      if ( v28 != 0 )
        goto LABEL_54;
    }
    v29 = -1;
    goto LABEL_91;
  }
  if ( a2 > 1130657384 )
  {
    if ( a2 != 1130657385 )
    {
      if ( a2 == 1131180649 )
      {
        v18 = *(_QWORD *)(a1 + 24);
        v19 = -1;
        if ( v18 == 0 )
          goto LABEL_113;
        v20 = *(__int64 **)(v18 + 24);
        if ( v20 == *(__int64 **)(v18 + 32) )
          goto LABEL_113;
        v21 = *v20;
        while ( 1 )
        {
          v22 = *(_QWORD *)(v21 + 120);
          if ( v22 != 0 )
            break;
          v23 = *(_QWORD *)(v21 + 48);
          if ( v23 != 0 )
          {
            v4 = *(__int64 **)(v23 + 24);
            if ( *(__int64 **)(v23 + 32) != v4 )
            {
              v24 = *v4 == v21;
              v21 = *v4;
              if ( !v24 )
                continue;
            }
          }
          goto LABEL_113;
        }
        v57 = *(_QWORD *)(v22 + 80);
        if ( v57 != 0 )
        {
          v58 = *(_QWORD *)(v57 + 56);
          v59 = -1;
          if ( v58 != 0 )
          {
            v19 = *(_DWORD *)(v58 + 12);
            v59 = *(_DWORD *)(v58 + 16);
            if ( v59 == 0 )
              v59 = *(_DWORD *)(v58 + 12);
          }
        }
        else
        {
LABEL_113:
          v59 = -1;
        }
        v60 = __PAIR64__(v59, v19);
        v55 = 1818456679;
        goto LABEL_99;
      }
      return (unsigned int)v4;
    }
    v45 = *(_QWORD *)(a1 + 24);
    v29 = -1;
    if ( v45 != 0 )
    {
      v46 = *(__int64 **)(v45 + 24);
      if ( v46 != *(__int64 **)(v45 + 32) )
      {
        v47 = *v46;
        if ( *v46 != 0 && *(_QWORD *)(v47 + 48) != 0 )
        {
          v48 = *(_QWORD *)(v47 + 80);
          v30 = -1;
          if ( v48 != 0 )
          {
            v29 = *(_DWORD *)(v48 + 12);
            v30 = *(_DWORD *)(v48 + 16);
LABEL_55:
            if ( v30 == 0 )
              v30 = v29;
          }
LABEL_92:
          v60 = __PAIR64__(v30, v29);
          goto LABEL_98;
        }
      }
    }
LABEL_91:
    v30 = -1;
    goto LABEL_92;
  }
  if ( a2 == 1130460260 )
  {
    v35 = *(_DWORD *)(a1 + 56);
    v13 = sub_14083D4F0(a1) + 40;
    LODWORD(v61) = v35;
    v60 = v13;
    if ( &v60 != a3 )
    {
      (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v36 = v60;
      v37 = v61;
      a3[1] = v61;
      *a3 = v36;
      v13 = sub_14083D4F0(v37) + 8;
      v61 = 0;
      v60 = v13;
    }
LABEL_76:
    v4 = *(__int64 **)v13;
    (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v13 + 16LL))(v13, &v60);
    goto LABEL_100;
  }
  if ( a2 == 1130589301 )
  {
    v5 = *(_QWORD *)(a1 + 24);
    if ( v5 != 0 )
    {
      v6 = *(_DWORD *)(v5 + 12);
      v7 = *(_DWORD *)(v5 + 16);
      if ( v7 == 0 )
        v7 = v6;
    }
    else
    {
      v6 = -1;
      v7 = -1;
    }
    v60 = __PAIR64__(v7, v6);
    v55 = 1130589301;
    goto LABEL_99;
  }
  return (unsigned int)v4;
}
