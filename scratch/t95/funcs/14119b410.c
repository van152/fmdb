__int64 __fastcall sub_14119B410(__int64 a1, int a2, unsigned int *a3)
{
  __int64 i; // rsi
  int v6; // ecx
  int v7; // ecx
  char v8; // al
  __int64 v9; // rbx
  __int64 v10; // rcx
  char v12; // al
  char v13; // cl
  char v14; // al
  char v15; // cl
  char v16; // al
  char v17; // cl
  __int64 v18; // r14
  char v19; // al
  char v20; // cl
  __int64 v21; // r14
  char v22; // al
  __int64 *v23; // rcx
  __int64 v24; // rbp
  __int64 *v25; // rbx
  __int64 v26; // rax
  __int64 v27; // rcx
  __int64 v28; // rdx
  __int64 v29; // rdx
  _QWORD *v30; // r15
  __int64 v31; // rbx
  __int64 v32; // r14
  __int64 v33; // r12
  __int64 v34; // rbp
  __int64 v35; // rdi
  unsigned int v36; // eax
  __int64 v37; // rax
  unsigned __int64 v38; // rax
  __int64 v39; // r12
  __int64 *v40; // rdi
  __int64 v41; // rax
  __int64 v42; // rbx
  _QWORD *v43; // rdi
  __int64 v44; // rbp
  __int64 v45; // rbp
  __int64 v46; // r14
  unsigned int *v47; // r8
  __int64 v48; // rax
  __int64 *v49; // rdx
  __int64 *v50; // r14
  __int64 v51; // rax
  __int64 v52; // rcx
  __int64 *v53; // rdx
  __int64 v54; // rcx
  __int64 v55; // rdx
  __int64 *v56; // rax
  __int64 v57; // rdi
  __int64 v58; // rbx
  __int64 v59; // rdi
  __int64 v60; // r14
  __int64 v61; // r12
  __int64 v62; // rbp
  __int64 v63; // r15
  __int64 v64; // rax
  __int64 v65; // rcx
  __int64 *v66; // rbx
  int v67; // eax
  __int64 v68; // rdi
  __int64 v69; // rbp
  __int64 v70; // rcx
  unsigned int *v71; // rdx
  __int64 v72; // rax
  unsigned int *v73; // rbx
  unsigned int v74; // eax
  __int64 v75; // rbx
  __int64 v76; // rcx
  __int64 v77; // rdi
  __int64 v78; // rdi
  _QWORD *v79; // rbx
  __int64 v80; // rbp
  unsigned int *v81; // r8
  int v82; // eax
  __int64 v83; // [rsp+28h] [rbp-60h] BYREF
  __int64 v84; // [rsp+30h] [rbp-58h] BYREF
  __int64 *v85; // [rsp+38h] [rbp-50h] BYREF
  _QWORD v86[9]; // [rsp+40h] [rbp-48h] BYREF

  LOBYTE(i) = 1;
  if ( a2 <= 1347188578 )
  {
    if ( a2 <= 1347184225 )
    {
      if ( a2 <= 1347183217 )
      {
        if ( (unsigned int)(a2 - 1347174723) > 0x11 || (v7 = 196609, !_bittest(&v7, a2 - 1347174723)) )
        {
          if ( a2 != 1347178055 )
            goto LABEL_180;
        }
      }
      else if ( (unsigned int)(a2 - 1347183469) > 7 || (v6 = 161, !_bittest(&v6, a2 - 1347183469)) )
      {
        if ( a2 != 1347183218 && a2 != 1347183972 )
          goto LABEL_180;
      }
      goto LABEL_53;
    }
    if ( a2 > 1347186021 )
    {
      if ( (unsigned int)(a2 - 1347186530) >= 2 && a2 != 1347186022 && a2 != 1347187566 )
        goto LABEL_180;
    }
    else if ( a2 > 1347184994 )
    {
      if ( a2 != 1347184995 && a2 != 1347186019 )
        goto LABEL_180;
    }
    else if ( a2 != 1347184226 && a2 != 1347184236 )
    {
      goto LABEL_180;
    }
LABEL_53:
    v10 = *(_QWORD *)(a1 + 48);
    if ( v10 != 0 )
      sub_1415799B0(v10, a2, a3);
    return (unsigned int)i;
  }
  if ( a2 <= 1347446385 )
  {
    if ( a2 > 1347445860 )
    {
      if ( a2 > 1347446372 )
      {
        if ( a2 == 1347446373 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 84) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 84) = -1;
          return (unsigned int)i;
        }
        if ( a2 == 1347446383 )
        {
          v14 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
          v15 = *(_BYTE *)(a1 + 88);
          if ( v14 != 0 )
            *(_BYTE *)(a1 + 88) = v15 | 1;
          else
            *(_BYTE *)(a1 + 88) = v15 & 0xFE;
          return (unsigned int)i;
        }
        goto LABEL_180;
      }
      if ( a2 == 1347445861 )
      {
        v19 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v20 = *(_BYTE *)(a1 + 88);
        if ( v19 != 0 )
          *(_BYTE *)(a1 + 88) = v20 | 4;
        else
          *(_BYTE *)(a1 + 88) = v20 & 0xFB;
        return (unsigned int)i;
      }
      if ( a2 != 1347445876 )
        goto LABEL_180;
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
      if ( *(__int64 **)a3 == &qword_141B5C8A0 )
      {
        v36 = a3[2];
        WORD1(v83) = v36 >> 17;
        LOWORD(v83) = (v36 >> 8) & 0x1FF | ((_WORD)v36 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
      {
        (*(void (__fastcall **)(_QWORD, __int64 **, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, &v85, a3);
        sub_1413CA830(&v83, &v85);
      }
      else
      {
        LODWORD(v83) = 124518401;
      }
      *(_DWORD *)(a1 + 80) = v83;
    }
    else
    {
      if ( a2 <= 1347445613 )
      {
        if ( a2 != 1347188579 && a2 != 1347188583 )
          goto LABEL_180;
        goto LABEL_53;
      }
      if ( a2 != 1347445614 )
      {
        if ( a2 == 1347445857 )
          return (unsigned int)i;
        goto LABEL_180;
      }
      v83 = a1;
      v84 = a1;
      v85 = &v83;
      v86[0] = &v84;
      v22 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3);
      v23 = *(__int64 **)a3;
      v24 = **(_QWORD **)a3;
      if ( v22 == 10 )
      {
        LODWORD(i) = 0;
        v25 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, unsigned int *, _QWORD))(v24 + 176))(v23, a3, 0);
        v26 = *v25;
        v27 = v25[1];
        if ( *v25 != v27 )
        {
          v28 = *v25;
          while ( *(_DWORD *)v28 != 1819504496 )
          {
            v28 += 16;
            if ( v28 == v27 )
              goto LABEL_180;
          }
          if ( v28 == v27 || *(_QWORD *)(v28 + 8) == 0 )
            goto LABEL_180;
          v49 = nullptr;
          while ( *(_DWORD *)v26 != 1819504496 )
          {
            v26 += 16;
            if ( v26 == v27 )
              goto LABEL_129;
          }
          if ( v26 == v27 )
            v49 = nullptr;
          else
            v49 = *(__int64 **)(v26 + 8);
LABEL_129:
          v50 = &qword_141B5A4A0;
          if ( v49 == nullptr )
            v49 = &qword_141B5A4A0;
          switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v49 + 64LL))(*v49) )
          {
            case 0u:
              LOBYTE(i) = sub_1415E9600(&v83) != 0;
              return (unsigned int)i;
            case 1u:
              v51 = *v25;
              v52 = v25[1];
              v53 = nullptr;
              if ( *v25 != v52 )
              {
                while ( *(_DWORD *)v51 != 1869379180 )
                {
                  v51 += 16;
                  if ( v51 == v52 )
                    goto LABEL_160;
                }
                if ( v51 == v52 )
                  v53 = nullptr;
                else
                  v53 = *(__int64 **)(v51 + 8);
              }
LABEL_160:
              if ( v53 == nullptr )
                v53 = &qword_141B5A4A0;
              v67 = sub_14119C260(v86, v53);
              if ( v67 < 0 )
                goto LABEL_180;
              v68 = *(_QWORD *)(*(_QWORD *)(v84 + 24) + 8LL * (unsigned int)v67);
              if ( v68 == 0 )
                goto LABEL_180;
              v69 = *v25;
              v70 = v25[1];
              v71 = nullptr;
              if ( *v25 == v70 )
              {
                v73 = (unsigned int *)&qword_141B5A4A0;
              }
              else
              {
                v72 = *v25;
                while ( *(_DWORD *)v72 != 1986096245 )
                {
                  v72 += 16;
                  if ( v72 == v70 )
                    goto LABEL_192;
                }
                if ( v72 == v70 )
                  v71 = nullptr;
                else
                  v71 = *(unsigned int **)(v72 + 8);
LABEL_192:
                v73 = (unsigned int *)&qword_141B5A4A0;
                if ( v71 != nullptr )
                  v73 = v71;
                v71 = nullptr;
                while ( *(_DWORD *)v69 != 1768169504 )
                {
                  v69 += 16;
                  if ( v69 == v70 )
                    goto LABEL_201;
                }
                if ( v69 == v70 )
                  v71 = nullptr;
                else
                  v71 = *(unsigned int **)(v69 + 8);
              }
LABEL_201:
              if ( v71 != nullptr )
                v50 = (__int64 *)v71;
              v82 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v50 + 80LL))(*v50, v50);
              LODWORD(i) = sub_141194740(v68, v82, v73);
              return (unsigned int)i;
            case 2u:
              v54 = *v25;
              v55 = v25[1];
              v56 = nullptr;
              if ( *v25 != v55 )
              {
                while ( *(_DWORD *)v54 != 1869379180 )
                {
                  v54 += 16;
                  if ( v54 == v55 )
                    goto LABEL_173;
                }
                if ( v54 == v55 )
                  v56 = nullptr;
                else
                  v56 = *(__int64 **)(v54 + 8);
              }
LABEL_173:
              if ( v56 != nullptr )
                v50 = v56;
              v74 = sub_14119C260(v86, v50);
              if ( (v74 & 0x80000000) != 0 || *(_QWORD *)(*(_QWORD *)(v84 + 24) + 8LL * v74) == 0 )
                goto LABEL_180;
              v75 = v83;
              v76 = *(_QWORD *)(v83 + 24);
              i = v76 + 8LL * v74;
              v77 = *(_QWORD *)i;
              if ( *(_QWORD *)i != 0 )
              {
                sub_141191740(*(_QWORD *)(v76 + 8LL * v74));
                sub_140FB07F0(v77);
              }
              sub_141758A00(i, i + 8, *(_QWORD *)(v75 + 32) - (i + 8));
              *(_QWORD *)(v75 + 32) -= 8LL;
              LOBYTE(i) = 1;
              return (unsigned int)i;
            case 3u:
              LOBYTE(i) = 1;
              v57 = *(_QWORD *)(v84 + 32) - *(_QWORD *)(v84 + 24);
              if ( v57 != 0 )
              {
                v58 = v57 >> 3;
                v59 = -(__int64)(v57 & 0xFFFFFFFFFFFFFFF8uLL);
                do
                {
                  v60 = v58 - 1;
                  if ( *(_QWORD *)(*(_QWORD *)(v84 + 24) + 8 * v58 - 8) != 0 )
                  {
                    v61 = v83;
                    v62 = *(_QWORD *)(v83 + 24);
                    v63 = *(_QWORD *)(v62 + 8 * v58 - 8);
                    if ( v63 != 0 )
                    {
                      sub_141191740(*(_QWORD *)(v62 + 8 * v58 - 8));
                      sub_140FB07F0(v63);
                    }
                    sub_141758A00(v62 + 8 * v58 - 8, v62 + 8 * v58, v59 + *(_QWORD *)(v61 + 32) - v62);
                    *(_QWORD *)(v61 + 32) -= 8LL;
                  }
                  v59 += 8;
                  --v58;
                }
                while ( v60 != 0 );
              }
              return (unsigned int)i;
            case 4u:
              v64 = *v25;
              v65 = v25[1];
              v66 = nullptr;
              if ( v64 == v65 )
                goto LABEL_182;
              break;
            case 5u:
              sub_140DD5C90(&v85, 0);
              LOBYTE(i) = 1;
              return (unsigned int)i;
            default:
              goto LABEL_180;
          }
          while ( *(_DWORD *)v64 != 1869379180 )
          {
            v64 += 16;
            if ( v64 == v65 )
              goto LABEL_182;
          }
          if ( v64 == v65 )
            v66 = nullptr;
          else
            v66 = *(__int64 **)(v64 + 8);
LABEL_182:
          v78 = sub_1415E9600(&v83);
          if ( v78 != 0 )
          {
            if ( v66 == nullptr )
              v66 = &qword_141B5A4A0;
            v79 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v66 + 176LL))(
                              *v66,
                              v66,
                              0);
            i = v79[1] - *v79;
            if ( i != 0 )
            {
              i >>= 4;
              v80 = 8;
              do
              {
                v81 = *(unsigned int **)(*v79 + v80);
                if ( v81 == nullptr )
                  v81 = (unsigned int *)&qword_141B5A4A0;
                sub_141194740(v78, *(_DWORD *)(*v79 + v80 - 8), v81);
                v80 += 16;
                --i;
              }
              while ( i != 0 );
            }
          }
          LOBYTE(i) = v78 != 0;
        }
      }
      else
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, unsigned int *))(v24 + 8))(v23, a3) != 11 )
          goto LABEL_180;
        v30 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, unsigned int *, _QWORD))(**(_QWORD **)a3 + 184LL))(
                          *(_QWORD *)a3,
                          a3,
                          0);
        i = *(_QWORD *)(v84 + 32) - *(_QWORD *)(v84 + 24);
        if ( i != 0 )
        {
          v31 = i >> 3;
          i = -(__int64)(i & 0xFFFFFFFFFFFFFFF8uLL);
          do
          {
            v32 = v31 - 1;
            if ( *(_QWORD *)(*(_QWORD *)(v84 + 24) + 8 * v31 - 8) != 0 )
            {
              v33 = v83;
              v34 = *(_QWORD *)(v83 + 24);
              v35 = *(_QWORD *)(v34 + 8 * v31 - 8);
              if ( v35 != 0 )
              {
                sub_141191740(*(_QWORD *)(v34 + 8 * v31 - 8));
                sub_140FB07F0(v35);
              }
              sub_141758A00(v34 + 8 * v31 - 8, v34 + 8 * v31, i + *(_QWORD *)(v33 + 32) - v34);
              *(_QWORD *)(v33 + 32) -= 8LL;
            }
            i += 8;
            --v31;
          }
          while ( v32 != 0 );
        }
        v37 = v30[1] - *v30;
        if ( v37 != 0 )
        {
          v38 = v37 >> 3;
          v39 = 1;
          if ( v38 >= 2 )
            v39 = v38;
          for ( i = 0; i != v39; ++i )
          {
            v40 = *(__int64 **)(*v30 + 8 * i);
            v41 = sub_1415E9600(&v83);
            if ( v41 != 0 )
            {
              v42 = v41;
              if ( v40 == nullptr )
                v40 = &qword_141B5A4A0;
              v43 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v40 + 176LL))(
                                *v40,
                                v40,
                                0);
              v44 = v43[1] - *v43;
              if ( v44 != 0 )
              {
                v45 = v44 >> 4;
                v46 = 8;
                do
                {
                  v47 = *(unsigned int **)(*v43 + v46);
                  if ( v47 == nullptr )
                    v47 = (unsigned int *)&qword_141B5A4A0;
                  sub_141194740(v42, *(_DWORD *)(*v43 + v46 - 8), v47);
                  v46 += 16;
                  --v45;
                }
                while ( v45 != 0 );
              }
            }
          }
        }
        v48 = qword_141B60C30;
        if ( qword_141B60C30 == qword_141B60C38 )
          goto LABEL_116;
        while ( *(_DWORD *)v48 != 1986359923 )
        {
          v48 += 16;
          if ( v48 == qword_141B60C38 )
            goto LABEL_116;
        }
        if ( v48 == qword_141B60C38 || (LOBYTE(i) = 1, *(_QWORD *)(v48 + 8) == 0) )
        {
LABEL_116:
          LOBYTE(i) = 1;
          LOBYTE(v29) = 1;
          sub_140DD5C90(&v85, v29);
        }
      }
    }
  }
  else if ( a2 <= 1347449966 )
  {
    if ( a2 > 1347448951 )
    {
      if ( a2 == 1347448952 )
      {
        *(_BYTE *)(a1 + 88) |= 2u;
        return (unsigned int)i;
      }
      if ( a2 == 1347449958 )
      {
        v12 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v13 = *(_BYTE *)(a1 + 88);
        if ( v12 != 0 )
          *(_BYTE *)(a1 + 88) = v13 | 8;
        else
          *(_BYTE *)(a1 + 88) = v13 & 0xF7;
        return (unsigned int)i;
      }
      goto LABEL_180;
    }
    if ( a2 == 1347446386 )
    {
      v18 = qword_141B5FE40;
      sub_140FE7960(&v85, a3, 1416914273);
      *(_QWORD *)(a1 + 56) = sub_140FA3700(v18, &v85);
      return (unsigned int)i;
    }
    if ( a2 != 1347447155 )
      goto LABEL_180;
  }
  else
  {
    if ( a2 > 1347450735 )
    {
      switch ( a2 )
      {
        case 1347450736:
          v16 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
          v17 = *(_BYTE *)(a1 + 88);
          if ( v16 != 0 )
            *(_BYTE *)(a1 + 88) = v17 | 0x10;
          else
            *(_BYTE *)(a1 + 88) = v17 & 0xEF;
          return (unsigned int)i;
        case 1348887138:
          goto LABEL_53;
        case 1349346420:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_BYTE *)(a1 + 90) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                    *(_QWORD *)a3,
                                    a3);
          else
            *(_BYTE *)(a1 + 90) = -1;
          return (unsigned int)i;
        default:
          break;
      }
LABEL_180:
      LODWORD(i) = 0;
      return (unsigned int)i;
    }
    if ( a2 == 1347449967 )
    {
      v21 = qword_141B5FE40;
      sub_140FE7960(&v85, a3, 1416914273);
      *(_QWORD *)(a1 + 64) = sub_140FA3700(v21, &v85);
      return (unsigned int)i;
    }
    if ( a2 != 1347449977 )
      goto LABEL_180;
    v8 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
    *(_BYTE *)(a1 + 89) = v8;
    if ( v8 == 3 && *(_QWORD *)(a1 + 48) == 0 )
    {
      v9 = sub_140F72AF0(104);
      sub_140F72BA0(v9);
      *(_QWORD *)(a1 + 48) = v9;
    }
  }
  return (unsigned int)i;
}
