__int64 __fastcall sub_140EA6E20(_QWORD **a1, __int64 **a2)
{
  __int64 *v2; // rdi
  char v4; // al
  __int64 *v5; // rcx
  __int64 v6; // rbp
  __int64 *v7; // rbx
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rdx
  __int64 v11; // r9
  __int64 *v12; // rcx
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // r12
  __int64 *v16; // rdx
  __int64 **v17; // r13
  __int64 *v18; // r8
  __int64 v19; // rdx
  __int64 *v20; // rcx
  unsigned __int64 v21; // rdx
  __int64 v22; // rsi
  __int64 v23; // rbx
  __int64 v24; // rbp
  __int64 v25; // rcx
  __int64 v26; // rcx
  __int64 v27; // rax
  unsigned __int64 v28; // rax
  __int64 v29; // rcx
  __int64 i; // r12
  __int64 *v31; // rdi
  int v32; // ebx
  __int64 v33; // rsi
  __int64 v34; // rcx
  __int64 v35; // r14
  __int64 v36; // r14
  __int64 v37; // r15
  __int64 *v38; // rdx
  int v39; // eax
  __int64 v40; // rax
  __int64 *v41; // r14
  int v42; // esi
  __int64 v43; // rax
  __int64 v44; // rcx
  __int64 v45; // rax
  __int64 v46; // rcx
  __int64 *v47; // rdx
  __int64 v48; // rcx
  __int64 v49; // rdx
  __int64 *v50; // rax
  __int64 v51; // r9
  __int64 *v52; // rcx
  __int64 v53; // rax
  __int64 v54; // rcx
  __int64 v55; // r15
  __int64 v56; // rax
  __int64 v57; // rcx
  __int64 *v58; // r13
  __int64 v59; // rbx
  __int64 v60; // r8
  __int64 v61; // rdx
  __int64 v62; // rcx
  unsigned __int64 v63; // rdx
  __int64 v64; // rax
  __int64 v65; // rbp
  __int64 v66; // rsi
  __int64 v67; // rcx
  __int64 v68; // rcx
  int v69; // eax
  __int64 **v70; // rdx
  __int64 *v71; // rcx
  __int64 *v72; // rdx
  __int64 v73; // r8
  __int64 v74; // rax
  __int64 v75; // rsi
  __int64 v76; // rbp
  __int64 v77; // rcx
  __int64 *v78; // rdx
  __int64 v79; // rax
  int v80; // eax
  __int64 *v81; // r14
  __int64 v82; // r11
  __int64 v83; // r8
  __int64 v84; // r15
  __int64 v85; // rdx
  __int64 v86; // rbp
  unsigned __int64 v88; // rbp
  unsigned __int64 v89; // rbx
  __int64 v90; // rdx
  __int64 v91; // rdx
  __int64 v92; // rsi
  __int64 v93; // rcx
  __int64 v94; // rax
  __int64 v95; // rax
  __int64 v96; // rcx
  int v97; // esi
  __int64 v98; // r12
  __int64 v99; // rcx
  _QWORD *v100; // rbx
  __int64 v101; // rbp
  __int64 v102; // rbp
  __int64 v103; // rsi
  __int64 *v104; // rdx
  int v105; // eax
  __int64 *v106; // rbx
  int v107; // eax
  _QWORD **v109; // [rsp+28h] [rbp-60h]
  int v110; // [rsp+30h] [rbp-58h] BYREF
  _QWORD *v111; // [rsp+38h] [rbp-50h]
  __int64 v112; // [rsp+40h] [rbp-48h]

  v4 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(*a2);
  v5 = *a2;
  v6 = **a2;
  if ( v4 != 10 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v6 + 8))(v5, a2) == 11 )
    {
      v111 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
      v11 = qword_141B60148;
      v12 = *(__int64 **)(qword_141B60148 + 128);
      v13 = *v12;
      v14 = v12[1];
      if ( v13 == v14 )
        goto LABEL_40;
      v15 = 0;
      do
      {
        if ( *(_QWORD *)v13 != 0 )
          v15 += *(_DWORD *)(*(_QWORD *)v13 + 24LL) == *(_DWORD *)(*a1[1] + 12LL);
        v13 += 8;
      }
      while ( v13 != v14 );
      if ( v15 == 0 )
      {
LABEL_40:
        v27 = v111[1] - *v111;
        if ( v27 != 0 )
        {
          v28 = v27 >> 3;
          v29 = 1;
          if ( v28 >= 2 )
            v29 = v28;
          v112 = v29;
          for ( i = 0; i != v112; ++i )
          {
            v31 = *(__int64 **)(*v111 + 8 * i);
            if ( v31 == nullptr )
              v31 = &qword_141B5A4A0;
            v32 = *(_DWORD *)(**a1 + 12LL);
            v33 = sub_141750CC0(40);
            *(_DWORD *)(v33 + 8) = -1;
            *(_DWORD *)(v33 + 16) = 0;
            *(_QWORD *)v33 = 0x141884E08LL;
            *(_DWORD *)(v33 + 24) = v32;
            *(_DWORD *)(v33 + 28) = -1;
            *(_WORD *)(v33 + 32) = 3584;
            *(_BYTE *)(v33 + 34) = 45;
            v34 = qword_141B60148;
            *(_DWORD *)(v33 + 12) = *(_DWORD *)(qword_141B60148 + 80) + 1;
            sub_140F74F20(v34, v33);
            v2 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v31 + 176LL))(
                              *v31,
                              v31,
                              0);
            v35 = v2[1] - *v2;
            if ( v35 != 0 )
            {
              v36 = v35 >> 4;
              v37 = 8;
              do
              {
                v38 = *(__int64 **)(*v2 + v37);
                if ( v38 == nullptr )
                  v38 = &qword_141B5A4A0;
                v39 = *(_DWORD *)(*v2 + v37 - 8);
                if ( v39 > 1851880552 )
                {
                  if ( v39 == 1918989417 )
                  {
                    *(_BYTE *)(v33 + 32) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v38 + 64LL))(*v38);
                  }
                  else if ( v39 == 1851880553 )
                  {
                    sub_140FE7960((__int64)&v110, v38, 0);
                    *(_DWORD *)(v33 + 28) = v110;
                  }
                }
                else if ( v39 == 1835104353 )
                {
                  *(_BYTE *)(v33 + 34) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v38 + 80LL))(*v38);
                }
                else if ( v39 == 1835626081 )
                {
                  *(_BYTE *)(v33 + 33) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v38 + 80LL))(*v38);
                }
                v37 += 16;
                --v36;
              }
              while ( v36 != 0 );
            }
          }
        }
        v40 = qword_141B60C30;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v40 != 1986359923 )
          {
            v40 += 16;
            if ( v40 == qword_141B60C38 )
              goto LABEL_64;
          }
          if ( v40 != qword_141B60C38 )
          {
            LOBYTE(v2) = 1;
            if ( *(_QWORD *)(v40 + 8) != 0 )
              goto LABEL_143;
          }
        }
LABEL_64:
        LOBYTE(v2) = 1;
        sub_140DD5C90();
        goto LABEL_143;
      }
LABEL_23:
      --v15;
      v17 = *(__int64 ***)(v11 + 128);
      v2 = *v17;
      v18 = v17[1];
      if ( *v17 == v18 )
        goto LABEL_22;
      v19 = 0;
      v20 = *v17;
      while ( 1 )
      {
        if ( *v20 != 0 && *(_DWORD *)(*v20 + 24) == *(_DWORD *)(*a1[1] + 12LL) )
        {
          if ( v19 == v15 )
          {
            v21 = v18 - v2;
            if ( v21 < 2 )
              v21 = 1;
            v22 = 0;
            v23 = 0;
            v24 = 0;
            while ( 1 )
            {
              v25 = v2[v23];
              if ( v25 != 0 && *(_DWORD *)(v25 + 24) == *(_DWORD *)(**a1 + 12LL) )
              {
                if ( v24 == v15 )
                {
                  v26 = *(__int64 *)((char *)v2 + (v22 >> 29));
                  if ( v26 != 0 )
                    sub_141750CFC(v26);
                  sub_141758A00();
                  --v17[1];
                  v11 = qword_141B60148;
LABEL_22:
                  if ( v15 == 0 )
                    goto LABEL_40;
                  goto LABEL_23;
                }
                ++v24;
              }
              ++v23;
              v22 += 0x100000000LL;
              if ( v21 == v23 )
                goto LABEL_22;
            }
          }
          ++v19;
        }
        if ( ++v20 == v18 )
          goto LABEL_22;
      }
    }
LABEL_142:
    LODWORD(v2) = 0;
    goto LABEL_143;
  }
  LODWORD(v2) = 0;
  v7 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v6 + 176))(v5, a2, 0);
  v8 = *v7;
  v9 = v7[1];
  if ( *v7 == v9 )
    goto LABEL_143;
  v10 = *v7;
  while ( *(_DWORD *)v10 != 1819504496 )
  {
    v10 += 16;
    if ( v10 == v9 )
      goto LABEL_142;
  }
  if ( v10 == v9 || *(_QWORD *)(v10 + 8) == 0 )
    goto LABEL_142;
  v16 = nullptr;
  while ( *(_DWORD *)v8 != 1819504496 )
  {
    v8 += 16;
    if ( v8 == v9 )
      goto LABEL_71;
  }
  if ( v8 == v9 )
    v16 = nullptr;
  else
    v16 = *(__int64 **)(v8 + 8);
LABEL_71:
  v41 = &qword_141B5A4A0;
  if ( v16 == nullptr )
    v16 = &qword_141B5A4A0;
  switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v16 + 64LL))(*v16) )
  {
    case 0u:
      v42 = *(_DWORD *)(**a1 + 12LL);
      v43 = sub_141750CC0(40);
      *(_DWORD *)(v43 + 8) = -1;
      *(_DWORD *)(v43 + 16) = 0;
      *(_QWORD *)v43 = 0x141884E08LL;
      *(_DWORD *)(v43 + 24) = v42;
      *(_DWORD *)(v43 + 28) = -1;
      *(_WORD *)(v43 + 32) = 3584;
      *(_BYTE *)(v43 + 34) = 45;
      v44 = qword_141B60148;
      *(_DWORD *)(v43 + 12) = *(_DWORD *)(qword_141B60148 + 80) + 1;
      sub_140F74F20(v44, v43);
      LOBYTE(v2) = 1;
      goto LABEL_143;
    case 1u:
      v109 = a1 + 1;
      v45 = *v7;
      v46 = v7[1];
      v47 = nullptr;
      if ( *v7 != v46 )
      {
        while ( *(_DWORD *)v45 != 1869379180 )
        {
          v45 += 16;
          if ( v45 == v46 )
            goto LABEL_121;
        }
        if ( v45 == v46 )
          v47 = nullptr;
        else
          v47 = *(__int64 **)(v45 + 8);
      }
LABEL_121:
      if ( v47 == nullptr )
        v47 = &qword_141B5A4A0;
      v69 = sub_140EA7920(v109, v47);
      if ( v69 < 0 )
        goto LABEL_142;
      v70 = *(__int64 ***)(qword_141B60148 + 128);
      v71 = *v70;
      v72 = v70[1];
      if ( v71 == v72 )
        goto LABEL_142;
      v73 = (unsigned int)v69;
      v74 = 0;
      while ( 2 )
      {
        v75 = *v71;
        if ( *v71 == 0 || *(_DWORD *)(v75 + 24) != *(_DWORD *)(**v109 + 12LL) )
          goto LABEL_127;
        if ( v74 != v73 )
        {
          ++v74;
LABEL_127:
          ++v71;
          LODWORD(v2) = 0;
          if ( v71 == v72 )
            goto LABEL_143;
          continue;
        }
        break;
      }
      v76 = *v7;
      v77 = v7[1];
      v78 = nullptr;
      if ( *v7 == v77 )
      {
        v106 = &qword_141B5A4A0;
      }
      else
      {
        v79 = *v7;
        while ( *(_DWORD *)v79 != 1986096245 )
        {
          v79 += 16;
          if ( v79 == v77 )
            goto LABEL_181;
        }
        if ( v79 == v77 )
          v78 = nullptr;
        else
          v78 = *(__int64 **)(v79 + 8);
LABEL_181:
        v106 = &qword_141B5A4A0;
        if ( v78 != nullptr )
          v106 = v78;
        v78 = nullptr;
        while ( *(_DWORD *)v76 != 1768169504 )
        {
          v76 += 16;
          if ( v76 == v77 )
            goto LABEL_190;
        }
        if ( v76 == v77 )
          v78 = nullptr;
        else
          v78 = *(__int64 **)(v76 + 8);
      }
LABEL_190:
      if ( v78 != nullptr )
        v41 = v78;
      v107 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v41 + 80LL))(*v41, v41);
      LODWORD(v2) = 0;
      if ( v107 > 1851880552 )
      {
        if ( v107 == 1918989417 )
        {
          *(_BYTE *)(v75 + 32) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v106 + 64LL))(*v106, v106);
          LOBYTE(v2) = 1;
        }
        else if ( v107 == 1851880553 )
        {
          sub_140FE7960((__int64)&v110, v106, 0);
          *(_DWORD *)(v75 + 28) = v110;
          LOBYTE(v2) = 1;
        }
      }
      else if ( v107 == 1835104353 )
      {
        *(_BYTE *)(v75 + 34) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v106 + 80LL))(*v106, v106);
        LOBYTE(v2) = 1;
      }
      else if ( v107 == 1835626081 )
      {
        *(_BYTE *)(v75 + 33) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v106 + 80LL))(*v106, v106);
        LOBYTE(v2) = 1;
      }
LABEL_143:
      LOBYTE(v2) = (unsigned __int8)v2 & 1;
      return (unsigned int)v2;
    case 2u:
      v48 = *v7;
      v49 = v7[1];
      v50 = nullptr;
      if ( *v7 != v49 )
      {
        while ( *(_DWORD *)v48 != 1869379180 )
        {
          v48 += 16;
          if ( v48 == v49 )
            goto LABEL_137;
        }
        if ( v48 == v49 )
          v50 = nullptr;
        else
          v50 = *(__int64 **)(v48 + 8);
      }
LABEL_137:
      if ( v50 != nullptr )
        v41 = v50;
      v80 = sub_140EA7920(a1 + 1, v41);
      if ( v80 >= 0 )
      {
        v81 = *(__int64 **)(qword_141B60148 + 128);
        v82 = *v81;
        v83 = v81[1];
        if ( *v81 != v83 )
        {
          v84 = (unsigned int)v80;
          v85 = 0;
          v86 = *v81;
          while ( 1 )
          {
            if ( *(_QWORD *)v86 != 0 && *(_DWORD *)(*(_QWORD *)v86 + 24LL) == *(_DWORD *)(*a1[1] + 12LL) )
            {
              if ( v85 == v80 )
              {
                v88 = (v83 - v82) >> 3;
                v89 = 1;
                v90 = 1;
                if ( v88 >= 2 )
                  v90 = (v83 - v82) >> 3;
                v91 = -v90;
                LOBYTE(v2) = 1;
                v92 = 0;
                v93 = 0;
                while ( 1 )
                {
                  v95 = *(_QWORD *)(v82 + 8 * v89 - 8);
                  if ( v95 != 0 && *(_DWORD *)(v95 + 24) == *(_DWORD *)(**a1 + 12LL) )
                  {
                    if ( v93 == v84 )
                    {
                      v96 = *(_QWORD *)(v82 + (v92 >> 29));
                      if ( v96 != 0 )
                        sub_141750CFC(v96);
                      sub_141758A00();
                      v81[1] -= 8;
                      goto LABEL_143;
                    }
                    ++v93;
                  }
                  LOBYTE(v2) = v89 < v88;
                  v92 += 0x100000000LL;
                  v94 = v91 + v89++ + 1;
                  if ( v94 == 1 )
                    goto LABEL_143;
                }
              }
              ++v85;
            }
            v86 += 8;
            LODWORD(v2) = 0;
            if ( v86 == v83 )
              goto LABEL_143;
          }
        }
      }
      goto LABEL_142;
    case 3u:
      v51 = qword_141B60148;
      v52 = *(__int64 **)(qword_141B60148 + 128);
      v53 = *v52;
      v54 = v52[1];
      LOBYTE(v2) = 1;
      if ( v53 == v54 )
        goto LABEL_143;
      v55 = 0;
      do
      {
        if ( *(_QWORD *)v53 != 0 )
          v55 += *(_DWORD *)(*(_QWORD *)v53 + 24LL) == *(_DWORD *)(*a1[1] + 12LL);
        v53 += 8;
      }
      while ( v53 != v54 );
      if ( v55 == 0 )
        goto LABEL_143;
      while ( 1 )
      {
        --v55;
        v58 = *(__int64 **)(v51 + 128);
        v59 = *v58;
        v60 = v58[1];
        if ( *v58 != v60 )
        {
          v61 = 0;
          v62 = *v58;
          do
          {
            if ( *(_QWORD *)v62 != 0 && *(_DWORD *)(*(_QWORD *)v62 + 24LL) == *(_DWORD *)(*a1[1] + 12LL) )
            {
              if ( v61 == v55 )
              {
                v63 = (v60 - v59) >> 3;
                if ( v63 < 2 )
                  v63 = 1;
                v64 = 0;
                v65 = 0;
                v66 = 0;
                while ( 1 )
                {
                  v67 = *(_QWORD *)(v59 + 8 * v65);
                  if ( v67 != 0 && *(_DWORD *)(v67 + 24) == *(_DWORD *)(**a1 + 12LL) )
                  {
                    if ( v66 == v55 )
                    {
                      v68 = *(_QWORD *)(v59 + (v64 >> 29));
                      if ( v68 != 0 )
                        sub_141750CFC(v68);
                      sub_141758A00();
                      v58[1] -= 8;
                      v51 = qword_141B60148;
                      goto LABEL_96;
                    }
                    ++v66;
                  }
                  ++v65;
                  v64 += 0x100000000LL;
                  if ( v63 == v65 )
                    goto LABEL_96;
                }
              }
              ++v61;
            }
            v62 += 8;
          }
          while ( v62 != v60 );
        }
LABEL_96:
        if ( v55 == 0 )
          goto LABEL_143;
      }
    case 4u:
      v56 = *v7;
      v57 = v7[1];
      v2 = nullptr;
      if ( *v7 == v57 )
        goto LABEL_161;
      break;
    case 5u:
      sub_140DD5C90();
      LOBYTE(v2) = 1;
      goto LABEL_143;
    default:
      goto LABEL_142;
  }
  while ( *(_DWORD *)v56 != 1869379180 )
  {
    v56 += 16;
    if ( v56 == v57 )
      goto LABEL_161;
  }
  if ( v56 == v57 )
    v2 = nullptr;
  else
    v2 = *(__int64 **)(v56 + 8);
LABEL_161:
  if ( v2 == nullptr )
    v2 = &qword_141B5A4A0;
  v97 = *(_DWORD *)(**a1 + 12LL);
  v98 = sub_141750CC0(40);
  *(_DWORD *)(v98 + 8) = -1;
  *(_DWORD *)(v98 + 16) = 0;
  *(_QWORD *)v98 = 0x141884E08LL;
  *(_DWORD *)(v98 + 24) = v97;
  *(_DWORD *)(v98 + 28) = -1;
  *(_WORD *)(v98 + 32) = 3584;
  *(_BYTE *)(v98 + 34) = 45;
  v99 = qword_141B60148;
  *(_DWORD *)(v98 + 12) = *(_DWORD *)(qword_141B60148 + 80) + 1;
  sub_140F74F20(v99, v98);
  v100 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, __int64 *, _QWORD))(*(_QWORD *)*v2 + 176LL))(*v2, v2, 0);
  LOBYTE(v2) = 1;
  v101 = v100[1] - *v100;
  if ( v101 != 0 )
  {
    v102 = v101 >> 4;
    v103 = 8;
    do
    {
      v104 = *(__int64 **)(*v100 + v103);
      if ( v104 == nullptr )
        v104 = &qword_141B5A4A0;
      v105 = *(_DWORD *)(*v100 + v103 - 8);
      if ( v105 > 1851880552 )
      {
        if ( v105 == 1918989417 )
        {
          *(_BYTE *)(v98 + 32) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v104 + 64LL))(*v104);
        }
        else if ( v105 == 1851880553 )
        {
          sub_140FE7960((__int64)&v110, v104, 0);
          *(_DWORD *)(v98 + 28) = v110;
        }
      }
      else if ( v105 == 1835104353 )
      {
        *(_BYTE *)(v98 + 34) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v104 + 80LL))(*v104);
      }
      else if ( v105 == 1835626081 )
      {
        *(_BYTE *)(v98 + 33) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v104 + 80LL))(*v104);
      }
      v103 += 16;
      --v102;
    }
    while ( v102 != 0 );
  }
  goto LABEL_143;
}
