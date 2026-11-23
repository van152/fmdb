__int64 __fastcall sub_14145A590(_DWORD *a1, int a2, __int64 **a3)
{
  __int64 j; // rsi
  __int64 v5; // rbx
  __int64 v6; // rbx
  char v7; // al
  __int64 *v8; // rcx
  __int64 v9; // rbx
  __int64 *v10; // rbx
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rdx
  _DWORD *v14; // rdx
  __int64 v15; // rax
  volatile signed __int32 *v16; // rcx
  volatile signed __int32 *v17; // rdi
  volatile signed __int32 *v18; // rdi
  char v19; // al
  __int64 *v20; // rcx
  __int64 v21; // rbx
  __int64 *v22; // rbx
  __int64 v23; // rax
  __int64 v24; // rcx
  __int64 v25; // rdx
  __int64 v27; // rdi
  bool v28; // cf
  __int64 v29; // rcx
  __int64 v30; // rdx
  _QWORD *v31; // r15
  __int64 v32; // rdi
  __int64 v33; // rdi
  __int64 v34; // rbx
  __int64 v35; // rax
  unsigned __int64 v36; // rax
  __int64 v37; // rbx
  __int64 i; // rdi
  __int64 *v39; // rdx
  __int64 v40; // rcx
  __int64 v41; // rax
  __int64 v42; // rax
  unsigned __int64 v43; // rax
  __int64 v44; // rbx
  __int64 *v45; // rdx
  __int64 v46; // rax
  _DWORD *v47; // rcx
  __int64 *v48; // rdx
  __int64 *v49; // rdx
  __int64 v50; // rcx
  __int64 v51; // rdx
  __int64 v52; // rax
  __int64 *v53; // rax
  __int64 v54; // rdi
  __int64 v55; // rax
  __int64 v56; // rcx
  __int64 *v57; // rdx
  __int64 v58; // rcx
  __int64 v59; // rdx
  __int64 v60; // rax
  __int64 v61; // rdi
  __int64 v62; // rbx
  __int64 v63; // rcx
  __int64 v64; // rax
  __int64 v65; // rcx
  __int64 *v66; // rdx
  __int64 v67; // rcx
  __int64 v68; // rdx
  __int64 v69; // rax
  __int64 v70; // r15
  __int64 v71; // r15
  __int64 v72; // rbx
  _DWORD *v73; // rdi
  __int64 v74; // rcx
  __int64 v75; // rdx
  __int64 v76; // rax
  int v77; // eax
  __int64 v78; // rcx
  int v79; // eax
  __int64 v80; // rcx
  unsigned __int64 v81; // rdx
  __int64 v82; // rbx
  __int64 v83; // rbx
  bool v84; // al
  int v85; // eax
  __int64 v86; // r14
  __int64 v87; // r15
  __int64 v88; // rdi
  __int64 v89; // rcx
  __int64 *v90; // rdx
  __int64 v91; // rax
  __int64 *v92; // rbx
  int v93; // eax
  __int64 v94; // rcx
  __int64 v95; // r15
  int v96; // eax
  _DWORD *v97; // [rsp+20h] [rbp-68h] BYREF
  _DWORD *v98; // [rsp+28h] [rbp-60h] BYREF
  _DWORD *v99; // [rsp+30h] [rbp-58h] BYREF
  __int64 v100; // [rsp+38h] [rbp-50h] BYREF
  __int64 v101; // [rsp+40h] [rbp-48h]
  __int64 v102; // [rsp+48h] [rbp-40h]
  _QWORD *v103; // [rsp+50h] [rbp-38h] BYREF
  _QWORD v104[6]; // [rsp+58h] [rbp-30h] BYREF

  j = (__int64)a1;
  if ( a2 <= 1282436975 )
  {
    if ( a2 != 1281583476 )
    {
      if ( a2 == 1282302317 )
      {
        (*(void (__fastcall **)(__int64 *, _DWORD **, __int64 **))(**a3 + 128))(*a3, &v99, a3);
        j += 24;
        if ( (_DWORD **)j != &v99 )
        {
          v14 = v99;
          v15 = *(_QWORD *)j;
          v16 = (volatile signed __int32 *)(*(_QWORD *)j - 4LL);
          if ( *(_QWORD *)j == 0 )
            v16 = nullptr;
          v17 = v99 - 1;
          if ( v99 != nullptr )
          {
            if ( v15 != 0 && _InterlockedDecrement(v16) == 0 )
              sub_1412EC9A0(v16, v14);
            *(_QWORD *)j = 0;
            _InterlockedIncrement(v17);
            v18 = v17 + 1;
          }
          else
          {
            if ( v15 != 0 && _InterlockedDecrement(v16) == 0 )
              sub_1412EC9A0(v16, v14);
            v18 = nullptr;
          }
          *(_QWORD *)j = v18;
        }
        v47 = v99;
        if ( v99 != nullptr && _InterlockedDecrement(v99 - 1) == 0 )
          sub_1412EC9A0(v47 - 1, v14);
        goto LABEL_74;
      }
      if ( a2 == 1282302324 )
      {
        v5 = qword_141B5FDD0;
        sub_140FE7960(&v99, a3, 1315856756);
        *(_QWORD *)(j + 96) = sub_14002F670(v5, &v99);
LABEL_74:
        LOBYTE(j) = 1;
        return (unsigned int)j;
      }
      return sub_140FE2700(a1, a2, a3);
    }
    v99 = a1;
    sub_141729A10(&v100, a1);
    v103 = &v99;
    v104[0] = &v100;
    v7 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
    v8 = *a3;
    v9 = **a3;
    if ( v7 == 10 )
    {
      LODWORD(j) = 0;
      v10 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v9 + 176))(v8, a3, 0);
      v11 = *v10;
      v12 = v10[1];
      if ( *v10 == v12 )
      {
LABEL_183:
        v61 = v100;
LABEL_184:
        if ( v61 != 0 )
        {
LABEL_185:
          v81 = v102 - v61;
          if ( v102 - v61 == -1 )
            v81 = *(unsigned int *)(v61 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v82 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v82) >> 3 > v81)
            && (v83 = *(_QWORD *)(v82 + 8 * v81)) != 0 )
          {
            MEMORY[0x1419475D8](v83 + 32, v61 - *(unsigned int *)(v83 + 120));
            v84 = *(_BYTE *)(v83 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 + 64)) != 0;
            if ( !v84 && *(_BYTE *)(v83 + 97) != 0 )
              sub_1412D33C0(v83);
          }
          else
          {
            MEMORY[0x141948990](v61 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        return (unsigned int)j;
      }
      v13 = *v10;
      while ( *(_DWORD *)v13 != 1819504496 )
      {
        v13 += 16;
        if ( v13 == v12 )
          goto LABEL_182;
      }
      if ( v13 != v12 && *(_QWORD *)(v13 + 8) != 0 )
      {
        v48 = nullptr;
        while ( *(_DWORD *)v11 != 1819504496 )
        {
          v11 += 16;
          if ( v11 == v12 )
            goto LABEL_99;
        }
        if ( v11 == v12 )
          v48 = nullptr;
        else
          v48 = *(__int64 **)(v11 + 8);
LABEL_99:
        j = (__int64)&qword_141B5A4A0;
        if ( v48 == nullptr )
          v48 = &qword_141B5A4A0;
        switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v48 + 64LL))(*v48) )
        {
          case 0u:
            v50 = *v10;
            v51 = v10[1];
            v52 = 0;
            if ( *v10 == v51 )
              goto LABEL_173;
            while ( *(_DWORD *)v50 != 1986096245 )
            {
              v50 += 16;
              if ( v50 == v51 )
                goto LABEL_173;
            }
            goto LABEL_170;
          case 1u:
            v55 = *v10;
            v56 = v10[1];
            v57 = nullptr;
            if ( *v10 != v56 )
            {
              while ( *(_DWORD *)v55 != 1869379180 )
              {
                v55 += 16;
                if ( v55 == v56 )
                  goto LABEL_161;
              }
              if ( v55 == v56 )
                v57 = nullptr;
              else
                v57 = *(__int64 **)(v55 + 8);
            }
LABEL_161:
            if ( v57 == nullptr )
              v57 = &qword_141B5A4A0;
            v77 = sub_14145B9C0(v104, v57);
            if ( v77 < 0 )
              goto LABEL_182;
            v61 = v100;
            v78 = *(_QWORD *)(v100 + 8LL * (unsigned int)v77);
            if ( v78 == 0 )
              goto LABEL_197;
            if ( (unsigned __int8)sub_141729F20(v78, (unsigned int)v77) == 0 )
              goto LABEL_182;
            v50 = *v10;
            v51 = v10[1];
            v52 = 0;
            if ( *v10 == v51 )
              goto LABEL_173;
            while ( *(_DWORD *)v50 != 1986096245 )
            {
              v50 += 16;
              if ( v50 == v51 )
                goto LABEL_173;
            }
            goto LABEL_170;
          case 2u:
            v58 = *v10;
            v59 = v10[1];
            v60 = 0;
            if ( *v10 != v59 )
            {
              while ( *(_DWORD *)v58 != 1869379180 )
              {
                v58 += 16;
                if ( v58 == v59 )
                  goto LABEL_177;
              }
              if ( v58 == v59 )
                v60 = 0;
              else
                v60 = *(_QWORD *)(v58 + 8);
            }
LABEL_177:
            if ( v60 != 0 )
              j = v60;
            v79 = sub_14145B9C0(v104, j);
            if ( v79 < 0 )
              goto LABEL_182;
            v61 = v100;
            v80 = *(_QWORD *)(v100 + 8LL * (unsigned int)v79);
            if ( v80 != 0 )
            {
              LODWORD(j) = sub_141729F20(v80, (unsigned int)v79);
              goto LABEL_183;
            }
LABEL_197:
            LODWORD(j) = 0;
            goto LABEL_185;
          case 3u:
            v61 = v101;
            if ( v101 == v100 )
            {
              LOBYTE(j) = 1;
              goto LABEL_184;
            }
            v62 = ((v101 - v100) >> 3) - 1;
            do
            {
              v63 = *(_QWORD *)(v100 + 8 * v62);
              if ( v63 != 0 )
                sub_141729F20(v63, v62);
              LOBYTE(j) = 1;
              v28 = v62-- != 0;
            }
            while ( v28 );
            goto LABEL_183;
          case 4u:
            v50 = *v10;
            v51 = v10[1];
            v52 = 0;
            if ( *v10 == v51 )
              goto LABEL_173;
            break;
          case 5u:
            sub_140DF3CB0(0);
            LOBYTE(j) = 1;
            goto LABEL_183;
          default:
            goto LABEL_182;
        }
        while ( *(_DWORD *)v50 != 1869379180 )
        {
          v50 += 16;
          if ( v50 == v51 )
            goto LABEL_173;
        }
LABEL_170:
        if ( v50 == v51 )
          v52 = 0;
        else
          v52 = *(_QWORD *)(v50 + 8);
LABEL_173:
        if ( v52 != 0 )
          j = v52;
        LOBYTE(j) = sub_141729CF0(&v99, j) != 0;
        goto LABEL_183;
      }
    }
    else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v9 + 8))(v8, a3) == 11 )
    {
      j = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      if ( v101 != v100 )
      {
        v27 = ((v101 - v100) >> 3) - 1;
        do
        {
          v29 = *(_QWORD *)(v100 + 8 * v27);
          if ( v29 != 0 )
            sub_141729F20(v29, v27);
          v28 = v27-- != 0;
        }
        while ( v28 );
      }
      v35 = *(_QWORD *)(j + 8) - *(_QWORD *)j;
      if ( v35 != 0 )
      {
        v36 = v35 >> 3;
        v37 = 1;
        if ( v36 >= 2 )
          v37 = v36;
        for ( i = 0; i != v37; ++i )
        {
          v39 = *(__int64 **)(*(_QWORD *)j + 8 * i);
          if ( v39 == nullptr )
            v39 = &qword_141B5A4A0;
          sub_141729CF0(&v99, v39);
        }
      }
      v40 = qword_141B60C38;
      v41 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_54;
      while ( *(_DWORD *)v41 != 1986359923 )
      {
        v41 += 16;
        if ( v41 == qword_141B60C38 )
          goto LABEL_54;
      }
      if ( v41 == qword_141B60C38 || (LOBYTE(j) = 1, *(_QWORD *)(v41 + 8) == 0) )
      {
LABEL_54:
        LOBYTE(j) = 1;
        LOBYTE(v40) = 1;
        sub_140DF3CB0(v40);
      }
      goto LABEL_183;
    }
LABEL_182:
    LODWORD(j) = 0;
    goto LABEL_183;
  }
  if ( a2 == 1282436976 )
  {
    a1[28] = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    goto LABEL_74;
  }
  if ( a2 != 1282567276 )
  {
    if ( a2 == 1282893153 )
    {
      v6 = qword_141B5FE48;
      sub_140FE7960(&v99, a3, 2004117618);
      *(_QWORD *)(j + 104) = sub_140FA1860(v6, &v99);
      goto LABEL_74;
    }
    return sub_140FE2700(a1, a2, a3);
  }
  v97 = a1;
  v98 = a1;
  v103 = &v97;
  v104[0] = &v98;
  v19 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
  v20 = *a3;
  v21 = **a3;
  if ( v19 != 10 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v21 + 8))(v20, a3) == 11 )
    {
      v31 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      v32 = *((_QWORD *)v98 + 7) - *((_QWORD *)v98 + 6);
      if ( v32 != 0 )
      {
        v33 = v32 >> 4;
        v34 = (v33 << 32) - 0x100000000LL;
        do
        {
          --v33;
          if ( *((_QWORD *)v98 + 6) != 0 )
          {
            j = (__int64)v97;
            sub_141758A00(
              *((_QWORD *)v97 + 6) + (v34 >> 28),
              *((_QWORD *)v97 + 6) + (v34 >> 28) + 16,
              *((_QWORD *)v97 + 7) - (*((_QWORD *)v97 + 6) + (v34 >> 28) + 16));
            *(_QWORD *)(j + 56) -= 16LL;
          }
          v34 -= 0x100000000LL;
        }
        while ( v33 != 0 );
      }
      v42 = v31[1] - *v31;
      if ( v42 != 0 )
      {
        v43 = v42 >> 3;
        v44 = 1;
        if ( v43 >= 2 )
          v44 = v43;
        for ( j = 0; j != v44; ++j )
        {
          v45 = *(__int64 **)(*v31 + 8 * j);
          if ( v45 == nullptr )
            v45 = &qword_141B5A4A0;
          sub_14145BF70(&v103, v45);
        }
      }
      v46 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_65;
      while ( *(_DWORD *)v46 != 1986359923 )
      {
        v46 += 16;
        if ( v46 == qword_141B60C38 )
          goto LABEL_65;
      }
      if ( v46 == qword_141B60C38 || (LOBYTE(j) = 1, *(_QWORD *)(v46 + 8) == 0) )
      {
LABEL_65:
        LOBYTE(j) = 1;
        LOBYTE(v30) = 1;
        sub_140DD5C90(&v103, v30);
      }
      return (unsigned int)j;
    }
LABEL_236:
    LODWORD(j) = 0;
    return (unsigned int)j;
  }
  LODWORD(j) = 0;
  v22 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v21 + 176))(v20, a3, 0);
  v23 = *v22;
  v24 = v22[1];
  if ( *v22 != v24 )
  {
    v25 = *v22;
    while ( *(_DWORD *)v25 != 1819504496 )
    {
      v25 += 16;
      if ( v25 == v24 )
        goto LABEL_236;
    }
    if ( v25 != v24 && *(_QWORD *)(v25 + 8) != 0 )
    {
      v49 = nullptr;
      while ( *(_DWORD *)v23 != 1819504496 )
      {
        v23 += 16;
        if ( v23 == v24 )
          goto LABEL_107;
      }
      if ( v23 == v24 )
        v49 = nullptr;
      else
        v49 = *(__int64 **)(v23 + 8);
LABEL_107:
      j = (__int64)&qword_141B5A4A0;
      if ( v49 == nullptr )
        v49 = &qword_141B5A4A0;
      switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v49 + 64LL))(*v49) )
      {
        case 0u:
          v53 = *(__int64 **)(qword_141B5FDF8 + 128);
          j = *v53;
          v54 = v53[1];
          if ( v54 != *v53 )
          {
            v99 = nullptr;
            LOBYTE(v100) = 100;
            sub_1408C9770(v97 + 12, &v99);
          }
          LOBYTE(j) = v54 != j;
          return (unsigned int)j;
        case 1u:
          v64 = *v22;
          v65 = v22[1];
          v66 = nullptr;
          if ( *v22 != v65 )
          {
            while ( *(_DWORD *)v64 != 1869379180 )
            {
              v64 += 16;
              if ( v64 == v65 )
                goto LABEL_199;
            }
            if ( v64 == v65 )
              v66 = nullptr;
            else
              v66 = *(__int64 **)(v64 + 8);
          }
LABEL_199:
          if ( v66 == nullptr )
            v66 = &qword_141B5A4A0;
          v85 = sub_14145BCB0(v104, v66);
          if ( v85 < 0 )
            goto LABEL_236;
          v86 = *((_QWORD *)v98 + 6);
          if ( v86 == 0 )
            goto LABEL_236;
          v87 = (unsigned int)v85;
          v88 = *v22;
          v89 = v22[1];
          v90 = nullptr;
          if ( *v22 == v89 )
          {
            v92 = &qword_141B5A4A0;
          }
          else
          {
            v91 = *v22;
            while ( *(_DWORD *)v91 != 1986096245 )
            {
              v91 += 16;
              if ( v91 == v89 )
                goto LABEL_222;
            }
            if ( v91 == v89 )
              v90 = nullptr;
            else
              v90 = *(__int64 **)(v91 + 8);
LABEL_222:
            v92 = &qword_141B5A4A0;
            if ( v90 != nullptr )
              v92 = v90;
            v90 = nullptr;
            while ( *(_DWORD *)v88 != 1768169504 )
            {
              v88 += 16;
              if ( v88 == v89 )
                goto LABEL_231;
            }
            if ( v88 == v89 )
              v90 = nullptr;
            else
              v90 = *(__int64 **)(v88 + 8);
          }
LABEL_231:
          v95 = 16 * v87;
          if ( v90 != nullptr )
            j = (__int64)v90;
          v96 = (*(__int64 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)j + 80LL))(*(_QWORD *)j, j);
          if ( v96 == 1282172784 )
          {
            *(_BYTE *)(v86 + v95 + 8) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v92 + 64LL))(
                                          *v92,
                                          v92);
          }
          else
          {
            if ( v96 != 1282172780 )
              goto LABEL_236;
            j = qword_141B5FDF8;
            sub_140FE7960(&v99, v92, 1818324583);
            *(_QWORD *)(v95 + v86) = sub_140FA1860(j, &v99);
          }
          goto LABEL_74;
        case 2u:
          v67 = *v22;
          v68 = v22[1];
          v69 = 0;
          if ( *v22 != v68 )
          {
            while ( *(_DWORD *)v67 != 1869379180 )
            {
              v67 += 16;
              if ( v67 == v68 )
                goto LABEL_212;
            }
            if ( v67 == v68 )
              v69 = 0;
            else
              v69 = *(_QWORD *)(v67 + 8);
          }
LABEL_212:
          if ( v69 != 0 )
            j = v69;
          v93 = sub_14145BCB0(v104, j);
          if ( v93 < 0 || *((_QWORD *)v98 + 6) == 0 )
            goto LABEL_236;
          j = (__int64)v97;
          v94 = *((_QWORD *)v97 + 6) + 16LL * (unsigned int)v93;
          sub_141758A00(v94, v94 + 16, *((_QWORD *)v97 + 7) - (v94 + 16));
          *(_QWORD *)(j + 56) -= 16LL;
          goto LABEL_74;
        case 3u:
          LOBYTE(j) = 1;
          v70 = *((_QWORD *)v98 + 7) - *((_QWORD *)v98 + 6);
          if ( v70 != 0 )
          {
            v71 = v70 >> 4;
            v72 = (v71 << 32) - 0x100000000LL;
            do
            {
              --v71;
              if ( *((_QWORD *)v98 + 6) != 0 )
              {
                v73 = v97;
                sub_141758A00(
                  *((_QWORD *)v97 + 6) + (v72 >> 28),
                  *((_QWORD *)v97 + 6) + (v72 >> 28) + 16,
                  *((_QWORD *)v97 + 7) - (*((_QWORD *)v97 + 6) + (v72 >> 28) + 16));
                *((_QWORD *)v73 + 7) -= 16LL;
              }
              v72 -= 0x100000000LL;
            }
            while ( v71 != 0 );
          }
          return (unsigned int)j;
        case 4u:
          v74 = *v22;
          v75 = v22[1];
          v76 = 0;
          if ( *v22 == v75 )
            goto LABEL_218;
          break;
        case 5u:
          sub_140DD5C90(&v103, 0);
          goto LABEL_74;
        default:
          goto LABEL_236;
      }
      while ( *(_DWORD *)v74 != 1869379180 )
      {
        v74 += 16;
        if ( v74 == v75 )
          goto LABEL_218;
      }
      if ( v74 == v75 )
        v76 = 0;
      else
        v76 = *(_QWORD *)(v74 + 8);
LABEL_218:
      if ( v76 != 0 )
        j = v76;
      LODWORD(j) = sub_14145BF70(&v103, j);
      return (unsigned int)j;
    }
    goto LABEL_236;
  }
  return (unsigned int)j;
}
