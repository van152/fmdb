__int64 __fastcall sub_1411B5630(__int64 a1, __int64 a2, __int64 **a3)
{
  __int64 k; // rsi
  __int64 **v4; // rbx
  __int64 v6; // rdx
  __int64 *v7; // r14
  __int64 v8; // rcx
  int v9; // eax
  int v10; // ecx
  int v11; // ecx
  int v12; // r9d
  int v13; // r8d
  int v14; // eax
  __int64 v15; // rdi
  unsigned __int64 v16; // rcx
  __int64 v17; // rbx
  __int64 v18; // rbx
  char v19; // al
  __int64 *v20; // rcx
  __int64 v21; // rdi
  __int64 *v22; // rbx
  __int64 v23; // rax
  __int64 v24; // rcx
  __int64 v25; // rdx
  __int64 v26; // rax
  __int64 v27; // rax
  __int64 v28; // rcx
  __int64 v29; // rax
  __int64 v30; // rcx
  __int64 v31; // rax
  __int64 v32; // rax
  __int16 v33; // cx
  __int64 v34; // rcx
  __int64 v35; // rax
  __int64 v36; // rcx
  __int64 v37; // rax
  __int64 v39; // r14
  __int64 v40; // rax
  __int64 v41; // rdi
  __int64 v42; // r15
  __int64 v43; // rbx
  __int64 v44; // rax
  __int64 v45; // rbx
  __int64 v46; // rax
  __int64 v47; // r8
  int v48; // eax
  int v49; // ecx
  __int64 v50; // rax
  unsigned __int64 v51; // rax
  __int64 v52; // r12
  __int64 *v53; // rdi
  __int64 v54; // rax
  __int64 v55; // rbx
  _QWORD *v56; // rdi
  __int64 v57; // r14
  __int64 v58; // r14
  __int64 v59; // r15
  __int64 *v60; // r8
  __int64 v61; // rcx
  __int64 v62; // rax
  __int64 v63; // rax
  int v64; // eax
  __int64 *v65; // rdx
  int v66; // esi
  __int64 v67; // rax
  __int64 v68; // rcx
  __int64 v69; // rax
  int v70; // esi
  __int64 v71; // rcx
  __int64 v72; // rax
  __int64 v73; // rcx
  __int64 v74; // rax
  int v75; // r9d
  __int64 v76; // rax
  __int64 v77; // rax
  __int64 v78; // rcx
  __int64 *v79; // r14
  __int64 v80; // rax
  __int64 v81; // rcx
  __int64 *v82; // rdx
  __int64 v83; // rcx
  __int64 v84; // rdx
  __int64 *v85; // rax
  __int64 v86; // r14
  __int64 v87; // rax
  __int64 v88; // r15
  __int64 *v89; // rdi
  __int64 v90; // rbx
  __int64 v91; // rax
  __int64 v92; // rdi
  __int64 j; // rbx
  __int64 v94; // rax
  __int64 v95; // rcx
  __int64 *v96; // rbx
  int v97; // eax
  __int64 v98; // r15
  __int64 v99; // rsi
  __int64 v100; // rcx
  __int64 *v101; // rdx
  __int64 v102; // rax
  __int64 *v103; // rbx
  int v104; // eax
  __int64 v105; // rax
  __int64 v106; // rdi
  _QWORD *v107; // rbx
  __int64 v108; // rax
  __int64 v109; // r14
  __int64 i; // rbx
  __int64 v111; // r15
  _QWORD *v112; // rbx
  __int64 v113; // rdi
  __int64 *v114; // r8
  unsigned int v115; // eax
  _DWORD v116[2]; // [rsp+68h] [rbp-18h] BYREF
  _QWORD *v117; // [rsp+70h] [rbp-10h]
  __int64 v118; // [rsp+78h] [rbp-8h] BYREF
  __int64 v119; // [rsp+80h] [rbp+0h] BYREF
  __int64 v120; // [rsp+88h] [rbp+8h]
  __int64 v121; // [rsp+90h] [rbp+10h]
  __int64 v122; // [rsp+A0h] [rbp+20h] BYREF
  _QWORD v123[9]; // [rsp+A8h] [rbp+28h] BYREF

  v123[1] = -2;
  v4 = a3;
  if ( (int)a2 > 1416520808 )
  {
    if ( (int)a2 > 1416656497 )
    {
      if ( (int)a2 <= 1416852584 )
      {
        if ( (_DWORD)a2 != 1416656498 )
        {
          if ( (_DWORD)a2 != 1416783216 )
          {
            if ( (_DWORD)a2 == 1416851817 )
            {
              v6 = a1;
              LOBYTE(a3) = 1;
              goto LABEL_42;
            }
            return sub_1411C2DF0(a1, a2, a3);
          }
          *(_WORD *)(a1 + 168) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          goto LABEL_112;
        }
        goto LABEL_32;
      }
      if ( (_DWORD)a2 == 1416852585 )
      {
        k = qword_141B5FE28;
        sub_140FE7960(&v118, a3, 1937006948);
        v32 = sub_140F7A940(k, &v118);
        *(_QWORD *)(a1 + 120) = v32;
        LOBYTE(k) = 1;
        if ( v32 != 0 )
        {
          v33 = *(_WORD *)(v32 + 166);
          if ( (v33 & 4) != 0 )
            *(_WORD *)(v32 + 166) = v33 & 0xFFF3;
        }
        return (unsigned int)k;
      }
      if ( (_DWORD)a2 != 1417044848 )
      {
        if ( (_DWORD)a2 != 1417111661 )
          return sub_1411C2DF0(a1, a2, a3);
        goto LABEL_32;
      }
      v118 = 0;
      sub_140FE8040(&v118, a3);
      v34 = v118;
      if ( (*(_BYTE *)(qword_141B5FE40 + 90) & 4) != 0 )
      {
        if ( v118 == 0 || (v35 = (*(__int64 (**)(void))(*(_QWORD *)v118 + 1672LL))()) == 0 )
        {
          *(_QWORD *)(a1 + 144) = 0;
          goto LABEL_112;
        }
        v34 = v35 + *(int *)(*(_QWORD *)(v35 + 8) + 4LL) + 8;
      }
      *(_QWORD *)(a1 + 144) = v34;
LABEL_112:
      LOBYTE(k) = 1;
      return (unsigned int)k;
    }
    if ( (int)a2 <= 1416586350 )
    {
      if ( (_DWORD)a2 == 1416520809 )
      {
        k = qword_141B5FDC0;
        sub_140FE7960(&v118, a3, 1668246896);
        *(_QWORD *)(a1 + 88) = sub_140F7A940(k, &v118);
      }
      else
      {
        if ( (_DWORD)a2 != 1416523620 )
          return sub_1411C2DF0(a1, a2, a3);
        k = qword_141B5FDC0;
        sub_140FE7960(&v118, a3, 1668246896);
        *(_QWORD *)(a1 + 112) = sub_140F7A940(k, &v118);
      }
      goto LABEL_112;
    }
    if ( (_DWORD)a2 == 1416586351 )
    {
      k = qword_141B5FDC0;
      sub_140FE7960(&v118, a3, 1668246896);
      *(_QWORD *)(a1 + 104) = sub_140F7A940(k, &v118);
      goto LABEL_112;
    }
    if ( (_DWORD)a2 == 1416588400 )
    {
      *(_BYTE *)(a1 + 170) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_112;
    }
    if ( (_DWORD)a2 != 1416652905 )
      return sub_1411C2DF0(a1, a2, a3);
    v6 = a1;
    LOBYTE(a3) = 12;
LABEL_42:
    sub_141535610(&v118, v6, a3);
    v122 = (__int64)&v118;
    v123[0] = &v119;
    v14 = sub_140EB22A0(&v122, v4);
LABEL_43:
    LODWORD(k) = v14;
    goto LABEL_44;
  }
  if ( (int)a2 <= 1416392813 )
  {
    if ( (int)a2 > 1415800939 )
    {
      if ( (_DWORD)a2 == 1415800940 )
      {
        v118 = a1;
        k = (__int64)&v119;
        sub_1415EA230(&v119, a1);
        v122 = (__int64)&v118;
        v123[0] = &v119;
        v19 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**v4 + 8))(*v4, v4);
        v20 = *v4;
        v21 = **v4;
        if ( v19 == 10 )
        {
          LODWORD(k) = 0;
          v22 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v21 + 176))(v20, v4, 0);
          v23 = *v22;
          v24 = v22[1];
          if ( *v22 == v24 )
            goto LABEL_44;
          v25 = *v22;
          while ( *(_DWORD *)v25 != 1819504496 )
          {
            v25 += 16;
            if ( v25 == v24 )
              goto LABEL_219;
          }
          if ( v25 != v24 && *(_QWORD *)(v25 + 8) != 0 )
          {
            v65 = nullptr;
            while ( *(_DWORD *)v23 != 1819504496 )
            {
              v23 += 16;
              if ( v23 == v24 )
                goto LABEL_160;
            }
            if ( v23 == v24 )
              v65 = nullptr;
            else
              v65 = *(__int64 **)(v23 + 8);
LABEL_160:
            v79 = &qword_141B5A4A0;
            if ( v65 == nullptr )
              v65 = &qword_141B5A4A0;
            switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v65 + 64LL))(*v65) )
            {
              case 0u:
                LOBYTE(k) = sub_1415EA540(&v118) != 0;
                goto LABEL_44;
              case 1u:
                v80 = *v22;
                v81 = v22[1];
                v82 = nullptr;
                if ( *v22 != v81 )
                {
                  while ( *(_DWORD *)v80 != 1869379180 )
                  {
                    v80 += 16;
                    if ( v80 == v81 )
                      goto LABEL_196;
                  }
                  if ( v80 == v81 )
                    v82 = nullptr;
                  else
                    v82 = *(__int64 **)(v80 + 8);
                }
LABEL_196:
                if ( v82 == nullptr )
                  v82 = &qword_141B5A4A0;
                v97 = sub_1411C12D0(v123, v82);
                if ( v97 < 0 )
                  goto LABEL_219;
                v15 = v119;
                v98 = *(_QWORD *)(v119 + 8LL * (unsigned int)v97);
                if ( v98 == 0 )
                  goto LABEL_220;
                v99 = *v22;
                v100 = v22[1];
                v101 = nullptr;
                if ( *v22 == v100 )
                {
                  v103 = &qword_141B5A4A0;
                }
                else
                {
                  v102 = *v22;
                  while ( *(_DWORD *)v102 != 1986096245 )
                  {
                    v102 += 16;
                    if ( v102 == v100 )
                      goto LABEL_232;
                  }
                  if ( v102 == v100 )
                    v101 = nullptr;
                  else
                    v101 = *(__int64 **)(v102 + 8);
LABEL_232:
                  v103 = &qword_141B5A4A0;
                  if ( v101 != nullptr )
                    v103 = v101;
                  v101 = nullptr;
                  while ( *(_DWORD *)v99 != 1768169504 )
                  {
                    v99 += 16;
                    if ( v99 == v100 )
                      goto LABEL_241;
                  }
                  if ( v99 == v100 )
                    v101 = nullptr;
                  else
                    v101 = *(__int64 **)(v99 + 8);
                }
LABEL_241:
                if ( v101 != nullptr )
                  v79 = v101;
                v115 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v79 + 80LL))(*v79, v79);
                v14 = sub_141570750(v98, v115, v103);
                goto LABEL_43;
              case 2u:
                v83 = *v22;
                v84 = v22[1];
                v85 = nullptr;
                if ( *v22 != v84 )
                {
                  while ( *(_DWORD *)v83 != 1869379180 )
                  {
                    v83 += 16;
                    if ( v83 == v84 )
                      goto LABEL_209;
                  }
                  if ( v83 == v84 )
                    v85 = nullptr;
                  else
                    v85 = *(__int64 **)(v83 + 8);
                }
LABEL_209:
                if ( v85 != nullptr )
                  v79 = v85;
                v104 = sub_1411C12D0(v123, v79);
                if ( v104 < 0 )
                  goto LABEL_219;
                v15 = v119;
                v105 = *(_QWORD *)(v119 + 8LL * (unsigned int)v104);
                if ( v105 == 0 )
                {
LABEL_220:
                  LODWORD(k) = 0;
                  goto LABEL_45;
                }
                v106 = qword_141B60158;
                v107 = *(_QWORD **)(qword_141B60158 + 128);
                k = *v107 + 8LL * *(int *)(v105 + 8);
                if ( *(_QWORD *)k != 0 )
                  sub_140FB2750();
                sub_141758A00(k, k + 8, v107[1] - (k + 8));
                v107[1] -= 8LL;
                v108 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v106 + 48LL))(v106);
                LOBYTE(k) = 1;
                if ( v108 != 0 )
                {
                  v109 = v108;
                  for ( i = 0; i != v109; ++i )
                    *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v106 + 16LL))(
                                  v106,
                                  (unsigned int)i)
                              + 8) = i;
                }
                goto LABEL_44;
              case 3u:
                v15 = v120;
                if ( v120 != v119 )
                {
                  v86 = (v120 - v119) >> 3;
                  do
                  {
                    v87 = *(_QWORD *)(v119 + 8 * v86-- - 8);
                    if ( v87 != 0 )
                    {
                      k = qword_141B60158;
                      v88 = *(int *)(v87 + 8);
                      v89 = *(__int64 **)(qword_141B60158 + 128);
                      v90 = *v89;
                      if ( *(_QWORD *)(*v89 + 8 * v88) != 0 )
                        sub_140FB2750();
                      sub_141758A00(v90 + 8 * v88, v90 + 8 * v88 + 8, v89[1] - (v90 + 8 * v88 + 8));
                      v89[1] -= 8;
                      v91 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)k + 48LL))(k);
                      if ( v91 != 0 )
                      {
                        v92 = v91;
                        for ( j = 0; j != v92; ++j )
                          *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)k + 16LL))(
                                        k,
                                        (unsigned int)j)
                                    + 8) = j;
                      }
                    }
                    LOBYTE(k) = 1;
                  }
                  while ( v86 != 0 );
                  goto LABEL_44;
                }
                LOBYTE(k) = 1;
                if ( v120 != 0 )
                  goto LABEL_45;
                return (unsigned int)k;
              case 4u:
                v94 = *v22;
                v95 = v22[1];
                v96 = nullptr;
                if ( v94 == v95 )
                  goto LABEL_222;
                break;
              case 5u:
                sub_140DF3CB0(0);
                LOBYTE(k) = 1;
                goto LABEL_44;
              default:
                goto LABEL_219;
            }
            while ( *(_DWORD *)v94 != 1869379180 )
            {
              v94 += 16;
              if ( v94 == v95 )
                goto LABEL_222;
            }
            if ( v94 == v95 )
              v96 = nullptr;
            else
              v96 = *(__int64 **)(v94 + 8);
LABEL_222:
            v111 = sub_1415EA540(&v118);
            if ( v111 != 0 )
            {
              if ( v96 == nullptr )
                v96 = &qword_141B5A4A0;
              v112 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v96 + 176LL))(
                                 *v96,
                                 v96,
                                 0);
              k = v112[1] - *v112;
              if ( k != 0 )
              {
                k >>= 4;
                v113 = 8;
                do
                {
                  v114 = *(__int64 **)(*v112 + v113);
                  if ( v114 == nullptr )
                    v114 = &qword_141B5A4A0;
                  sub_141570750(v111, *(unsigned int *)(*v112 + v113 - 8), v114);
                  v113 += 16;
                  --k;
                }
                while ( k != 0 );
              }
            }
            LOBYTE(k) = v111 != 0;
            goto LABEL_44;
          }
        }
        else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v21 + 8))(v20, v4) == 11 )
        {
          v117 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**v4 + 184))(*v4, v4, 0);
          if ( v120 != v119 )
          {
            v39 = (v120 - v119) >> 3;
            do
            {
              v40 = *(_QWORD *)(v119 + 8 * v39-- - 8);
              if ( v40 != 0 )
              {
                v41 = qword_141B60158;
                v42 = *(int *)(v40 + 8);
                k = *(_QWORD *)(qword_141B60158 + 128);
                v43 = *(_QWORD *)k;
                if ( *(_QWORD *)(*(_QWORD *)k + 8 * v42) != 0 )
                  sub_140FB2750();
                sub_141758A00(v43 + 8 * v42, v43 + 8 * v42 + 8, *(_QWORD *)(k + 8) - (v43 + 8 * v42 + 8));
                *(_QWORD *)(k + 8) -= 8LL;
                v44 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v41 + 48LL))(v41);
                if ( v44 != 0 )
                {
                  v45 = v44;
                  for ( k = 0; k != v45; ++k )
                    *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v41 + 16LL))(
                                  v41,
                                  (unsigned int)k)
                              + 8) = k;
                }
              }
            }
            while ( v39 != 0 );
          }
          v50 = v117[1] - *v117;
          if ( v50 != 0 )
          {
            v51 = v50 >> 3;
            v52 = 1;
            if ( v51 >= 2 )
              v52 = v51;
            for ( k = 0; k != v52; ++k )
            {
              v53 = *(__int64 **)(*v117 + 8 * k);
              v54 = sub_1415EA540(&v118);
              if ( v54 != 0 )
              {
                v55 = v54;
                if ( v53 == nullptr )
                  v53 = &qword_141B5A4A0;
                v56 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v53 + 176LL))(
                                  *v53,
                                  v53,
                                  0);
                v57 = v56[1] - *v56;
                if ( v57 != 0 )
                {
                  v58 = v57 >> 4;
                  v59 = 8;
                  do
                  {
                    v60 = *(__int64 **)(*v56 + v59);
                    if ( v60 == nullptr )
                      v60 = &qword_141B5A4A0;
                    sub_141570750(v55, *(unsigned int *)(*v56 + v59 - 8), v60);
                    v59 += 16;
                    --v58;
                  }
                  while ( v58 != 0 );
                }
              }
            }
          }
          v61 = qword_141B60C38;
          v62 = qword_141B60C30;
          if ( qword_141B60C30 == qword_141B60C38 )
            goto LABEL_131;
          while ( *(_DWORD *)v62 != 1986359923 )
          {
            v62 += 16;
            if ( v62 == qword_141B60C38 )
              goto LABEL_131;
          }
          if ( v62 == qword_141B60C38 || (LOBYTE(k) = 1, *(_QWORD *)(v62 + 8) == 0) )
          {
LABEL_131:
            LOBYTE(k) = 1;
            LOBYTE(v61) = 1;
            sub_140DF3CB0(v61);
          }
          goto LABEL_44;
        }
LABEL_219:
        LODWORD(k) = 0;
LABEL_44:
        v15 = v119;
        if ( v119 != 0 )
        {
LABEL_45:
          v16 = v121 - v15;
          if ( v121 - v15 == -1 )
            v16 = *(unsigned int *)(v15 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v17 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > v16)
            && (v18 = *(_QWORD *)(v17 + 8 * v16)) != 0 )
          {
            MEMORY[0x1419475D8](v18 + 32, v15 - *(unsigned int *)(v18 + 120));
            if ( (*(_BYTE *)(v18 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v18 + 64)) == 0)
              && *(_BYTE *)(v18 + 97) != 0 )
            {
              sub_1412D33C0(v18);
            }
          }
          else
          {
            MEMORY[0x141948990](v15 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        return (unsigned int)k;
      }
      if ( (_DWORD)a2 == 1415870057 )
      {
        k = qword_141B5FDC0;
        sub_140FE7960(&v118, a3, 1668246896);
        v26 = sub_140F7A940(k, &v118);
        *(_QWORD *)(a1 + 80) = v26;
        LOBYTE(k) = 1;
        if ( v26 != 0 && *(_QWORD *)(v26 + 96) != 0 && *(_BYTE *)(a1 + 47) == 0 )
        {
          v27 = *(_QWORD *)(a1 + 48);
          if ( v27 != 0 && *(_DWORD *)(v27 + 12) == *(_DWORD *)(a1 + 12) )
          {
            sub_1407C9510(&v118);
            v29 = sub_14083D4F0(v28);
            LODWORD(v123[0]) = 3;
            v122 = v29 + 40;
            sub_140833EB0(&v118, 1685353593, &v122);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v122 + 16LL))(v122, &v122);
            if ( *(_BYTE *)(a1 + 47) != 0 )
              v31 = 0;
            else
              v31 = *(_QWORD *)(a1 + 48);
            v66 = *(_DWORD *)(v31 + 12);
            v67 = sub_14083D4F0(v30);
            LODWORD(v123[0]) = v66;
            v122 = v67 + 40;
            sub_140833EB0(&v118, 1685417577, &v122);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v122 + 16LL))(v122, &v122);
            v69 = sub_14083D4F0(v68);
            LODWORD(v123[0]) = 1131312233;
            v122 = v69 + 56;
            sub_140833EB0(&v118, 1886549113, &v122);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v122 + 16LL))(v122, &v122);
            v70 = *(_DWORD *)(*(_QWORD *)(*(_QWORD *)(a1 + 80) + 96LL) + 12LL);
            v72 = sub_14083D4F0(v71);
            LODWORD(v123[0]) = v70;
            v122 = v72 + 40;
            sub_140833EB0(&v118, 1853322860, &v122);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v122 + 16LL))(v122, &v122);
            v74 = sub_14083D4F0(v73);
            LOBYTE(v123[0]) = 1;
            v122 = v74 + 24;
            k = (__int64)&v122;
            sub_140833EB0(&v118, 1230193478, &v122);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v122 + 16LL))(v122, &v122);
            LOBYTE(k) = 1;
            LOBYTE(v75) = 1;
            sub_140F47AD0((unsigned int)&qword_141B5FDA8, (unsigned int)&v118, 0, v75, 1, 0, 1, 0, 0, 1, 0, 0);
            sub_140833970(&v118);
          }
        }
        return (unsigned int)k;
      }
      if ( (_DWORD)a2 != 1416389737 )
        return sub_1411C2DF0(a1, a2, a3);
      k = qword_141B5FDC0;
      sub_140FE7960(&v118, a3, 1668246896);
      *(_QWORD *)(a1 + 96) = sub_140F7A940(k, &v118);
      goto LABEL_112;
    }
    if ( (_DWORD)a2 == 1415799152 )
    {
      v118 = 0;
      sub_140FE8040(&v118, a3);
      v36 = v118;
      if ( (*(_BYTE *)(qword_141B5FE40 + 90) & 4) != 0 )
      {
        if ( v118 != 0 && (v37 = (*(__int64 (**)(void))(*(_QWORD *)v118 + 1672LL))()) != 0 )
          v36 = v37 + *(int *)(*(_QWORD *)(v37 + 8) + 4LL) + 8;
        else
          v36 = 0;
      }
      *(_QWORD *)(a1 + 136) = v36;
      goto LABEL_112;
    }
    if ( (_DWORD)a2 != 1415800937 )
      return sub_1411C2DF0(a1, a2, a3);
    v6 = a1;
    LOBYTE(a3) = 2;
    goto LABEL_42;
  }
  if ( (int)a2 <= 1416392818 )
  {
    if ( (_DWORD)a2 == 1416392814 )
    {
      *(_BYTE *)(a1 + 172) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    }
    else
    {
      if ( (_DWORD)a2 != 1416392815 )
        return sub_1411C2DF0(a1, a2, a3);
      *(_BYTE *)(a1 + 178) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    }
    goto LABEL_112;
  }
  if ( (_DWORD)a2 == 1416392819 )
  {
    *(_BYTE *)(a1 + 171) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    goto LABEL_112;
  }
  if ( (_DWORD)a2 == 1416456301 )
  {
LABEL_32:
    k = *(_QWORD *)(a1 + 160);
    if ( k != 0 )
    {
      if ( (_DWORD)a2 == 1416456301 )
      {
        *(_BYTE *)(k + 266) = sub_1409DAB30((_DWORD)a3, 1099332336, 0, 0, 0, 0);
      }
      else if ( (_DWORD)a2 == 1416656498 )
      {
        *(_WORD *)(k + 248) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      }
      else
      {
        *(_BYTE *)(k + 265) = sub_1409DAB30((_DWORD)a3, 1099332336, 0, 0, 0, 0);
      }
    }
    else
    {
      sub_140F4AEF0(&qword_141B5FDA8, a2, a3);
    }
    goto LABEL_112;
  }
  if ( (_DWORD)a2 != 1416457833 )
    return sub_1411C2DF0(a1, a2, a3);
  v7 = &v118;
  sub_140FE7960(&v118, a3, 0);
  if ( (_DWORD)v118 != -1 )
  {
    v9 = *(_DWORD *)(a1 + 12);
    v116[0] = v9;
    v10 = *(_DWORD *)(a1 + 16);
    if ( v10 == 0 )
      v10 = v9;
    v116[1] = v10;
    LODWORD(k) = 0;
    sub_140FE7960(&v122, v4, 0);
    sub_1407C9510(&v118);
    LOBYTE(v11) = *(_BYTE *)(a1 + 47) == 0;
    LOBYTE(v12) = 16;
    if ( (unsigned __int8)sub_141037A60(v11, (unsigned int)&v122, (unsigned int)v116, v12, 16, (__int64)&v118) != 0 )
    {
      LOBYTE(v13) = 1;
      LODWORD(k) = sub_140F47AD0((unsigned int)&qword_141B5FDA8, (unsigned int)&v118, v13, 0, 1, 0, 1, 0, 0, 1, 0, 0);
    }
    sub_140833970(&v118);
    return (unsigned int)k;
  }
  if ( (*(_BYTE *)(qword_141B5FE40 + 90) & 4) != 0 )
  {
    v63 = *(_QWORD *)(a1 + 128);
    LOBYTE(v7) = 16;
    if ( v63 != 0 )
    {
      v8 = *(unsigned __int8 *)(a1 + 47);
      if ( (_DWORD)v8 == 1 )
      {
        v64 = sub_140DE2A80(*(int *)(*(_QWORD *)(v63 + 8) + 8LL) + v63 + 344);
      }
      else
      {
        if ( *(_BYTE *)(a1 + 47) != 0 )
          goto LABEL_151;
        v64 = sub_140DE2680(*(int *)(*(_QWORD *)(v63 + 8) + 8LL) + v63 + 344, 0);
      }
      LODWORD(v7) = v64;
    }
LABEL_151:
    v76 = sub_14083D4F0(v8);
    v119 = 0;
    v118 = v76 + 8;
    v77 = *(_QWORD *)(a1 + 128);
    if ( v77 != 0 )
      v78 = v77 + *(int *)(*(_QWORD *)(v77 + 8) + 4LL) + 8;
    else
      v78 = 0;
    sub_140FE7F20(v78, &v118);
    LODWORD(k) = 0;
    sub_140FE7960(&v122, &v118, 0);
    if ( (int)v122 >= 0 )
    {
      v122 = -1;
      LODWORD(k) = sub_1411B5560(a1, &v118, (unsigned int)v7, &v122);
    }
    goto LABEL_108;
  }
  v46 = sub_14083D4F0(v8);
  v119 = 0;
  v118 = v46 + 8;
  sub_140FE7F20(*(_QWORD *)(a1 + 128), &v118);
  LODWORD(k) = 0;
  sub_140FE7960(&v122, &v118, 0);
  if ( (int)v122 >= 0 )
  {
    v48 = *(_DWORD *)(a1 + 12);
    LODWORD(v122) = v48;
    v49 = *(_DWORD *)(a1 + 16);
    if ( v49 == 0 )
      v49 = v48;
    HIDWORD(v122) = v49;
    LOBYTE(v47) = 2;
    LODWORD(k) = sub_1411B5560(a1, &v118, v47, &v122);
  }
LABEL_108:
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v118 + 16LL))(v118, &v118);
  return (unsigned int)k;
}
