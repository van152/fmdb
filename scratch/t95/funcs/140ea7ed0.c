__int64 __fastcall sub_140EA7ED0(__int64 **a1, __int64 **a2)
{
  __int64 v2; // rbx
  char v5; // al
  __int64 *v6; // rcx
  __int64 v7; // rbp
  __int64 *v8; // rdi
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 *v12; // rsi
  int v13; // eax
  void *v14; // rax
  __int64 *v15; // rdx
  __int64 *v16; // rcx
  __int64 v17; // rax
  __int64 v18; // rcx
  __int64 v19; // rdx
  __int64 v20; // rdi
  __int64 *v21; // rsi
  int v22; // eax
  void *v23; // rcx
  __int64 **v24; // rcx
  __int64 *v25; // rax
  __int64 *v26; // rcx
  __int64 v27; // rbp
  __int64 *v28; // rsi
  int v29; // eax
  void *v30; // rcx
  __int64 *v31; // r15
  __int64 v32; // rax
  __int64 v33; // rcx
  unsigned __int64 v34; // rcx
  __int64 v35; // r9
  __int64 v36; // rbp
  __int64 v37; // rsi
  __int64 v38; // rax
  unsigned __int64 v39; // rax
  __int64 v40; // r12
  __int64 v41; // rbp
  __int64 *v42; // rdi
  __int64 v43; // rax
  __int64 v44; // rsi
  _QWORD *v45; // rdi
  __int64 v46; // r15
  __int64 v47; // r15
  __int64 v48; // r14
  __int64 *v49; // rdx
  int v50; // eax
  __int64 v51; // rdx
  __int64 v52; // rax
  __int64 *v53; // r14
  __int64 **v54; // r12
  __int64 v55; // rax
  __int64 v56; // rcx
  __int64 *v57; // rdx
  __int64 v58; // rcx
  __int64 v59; // rdx
  __int64 *v60; // rax
  __int64 *v61; // rsi
  int v62; // eax
  void *v63; // rax
  __int64 v64; // rax
  __int64 v65; // rcx
  __int64 *v66; // rdi
  __int64 *v67; // rcx
  __int64 v68; // rax
  __int64 v69; // rcx
  __int64 v70; // rdx
  __int64 v71; // rdi
  __int64 *v72; // rsi
  int v73; // eax
  void *v74; // rcx
  __int64 *v75; // rcx
  __int64 v76; // rax
  __int64 v77; // rcx
  __int64 v78; // rbp
  __int64 *v79; // rsi
  int v80; // eax
  void *v81; // rcx
  __int64 *v82; // r15
  __int64 v83; // r10
  __int64 v84; // rcx
  unsigned __int64 v85; // rcx
  __int64 v86; // r9
  __int64 v87; // rsi
  __int64 v88; // rbp
  __int64 v89; // rax
  int v90; // eax
  unsigned int v91; // esi
  __int64 *v92; // rbx
  int v93; // eax
  void *v94; // rax
  __int64 **v95; // rcx
  __int64 *v96; // rax
  __int64 *v97; // rcx
  __int64 v98; // r8
  __int64 v99; // rsi
  __int64 v100; // rdx
  __int64 v101; // rbp
  int v102; // eax
  int v103; // esi
  __int64 *v104; // rdi
  int v105; // eax
  void *v106; // rax
  __int64 *v107; // rcx
  __int64 v108; // rax
  __int64 v109; // rcx
  __int64 v110; // rbp
  __int64 v111; // rsi
  _QWORD *v112; // rdi
  __int64 v113; // rbp
  __int64 v114; // rbp
  __int64 *v115; // rdx
  int v116; // eax
  __int64 v117; // rbx
  __int64 v118; // rcx
  __int64 *v119; // rdx
  __int64 v120; // rax
  __int64 *v121; // rdi
  int v122; // eax
  void *v123; // rax
  __int64 *v124; // rsi
  __int64 *v125; // r14
  __int64 v126; // r11
  __int64 v127; // rcx
  unsigned __int64 v128; // rcx
  __int64 v129; // r10
  unsigned __int64 v130; // rdi
  __int64 v131; // rdx
  __int64 v132; // rdx
  __int64 v133; // rbp
  __int64 v134; // r15
  __int64 v136; // rax
  __int64 v137; // rax
  __int64 v138; // rcx
  int v139; // eax
  int v140; // [rsp+20h] [rbp-58h] BYREF
  _QWORD *v141; // [rsp+28h] [rbp-50h]
  __int64 **v142; // [rsp+30h] [rbp-48h]

  v5 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(*a2);
  v6 = *a2;
  v7 = **a2;
  if ( v5 != 10 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v7 + 8))(v6, a2) != 11 )
      goto LABEL_215;
    v141 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
    v12 = a1[1];
    v13 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v12 + 56LL))(*v12);
    if ( v13 == 3 )
    {
      v14 = &unk_141B60120;
    }
    else if ( v13 == 47 )
    {
      v14 = &unk_141B60130;
    }
    else
    {
      v14 = &unk_141B60128;
    }
    v16 = *(__int64 **)(*(_QWORD *)v14 + 128LL);
    v17 = *v16;
    v18 = v16[1];
    if ( v17 == v18 )
      goto LABEL_54;
    v19 = *v12;
    v20 = 0;
    do
    {
      if ( *(_QWORD *)v17 != 0 )
      {
        v2 = *(_DWORD *)(*(_QWORD *)v17 + 40LL) == *(_DWORD *)(v19 + 12);
        v20 += v2;
      }
      v17 += 8;
    }
    while ( v17 != v18 );
    if ( v20 == 0 )
      goto LABEL_54;
LABEL_28:
    v21 = a1[1];
    v22 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)*v21 + 56LL))(*v21, v19);
    v23 = &unk_141B60120;
    if ( v22 != 3 )
    {
      if ( v22 == 47 )
        v23 = &unk_141B60130;
      else
        v23 = &unk_141B60128;
    }
    --v20;
    v24 = *(__int64 ***)(*(_QWORD *)v23 + 128LL);
    v25 = *v24;
    v26 = v24[1];
    if ( v25 == v26 )
      goto LABEL_27;
    v19 = *v21;
    v27 = 0;
    while ( 1 )
    {
      v2 = *v25;
      if ( *v25 != 0 )
      {
        LODWORD(v2) = *(_DWORD *)(v2 + 40);
        if ( (_DWORD)v2 == *(_DWORD *)(v19 + 12) )
        {
          if ( v27 == v20 )
          {
            v28 = *a1;
            v29 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)**a1 + 56LL))(**a1);
            v30 = &unk_141B60120;
            if ( v29 != 3 )
            {
              if ( v29 == 47 )
                v30 = &unk_141B60130;
              else
                v30 = &unk_141B60128;
            }
            v31 = *(__int64 **)(*(_QWORD *)v30 + 128LL);
            v32 = *v31;
            v33 = v31[1] - *v31;
            if ( v33 != 0 )
            {
              v34 = v33 >> 3;
              if ( v34 < 2 )
                v34 = 1;
              v35 = *v28;
              v19 = 0;
              v36 = 0;
              v2 = 0;
              do
              {
                v37 = *(_QWORD *)(v32 + 8 * v36);
                if ( v37 != 0 && *(_DWORD *)(v37 + 40) == *(_DWORD *)(v35 + 12) )
                {
                  if ( v2 == v20 )
                  {
                    if ( *(_QWORD *)(v32 + (v19 >> 29)) != 0 )
                      ((void (*)(void))sub_140FB2020)();
                    sub_141758A00();
                    v31[1] -= 8;
                    break;
                  }
                  ++v2;
                }
                ++v36;
                v19 += 0x100000000LL;
              }
              while ( v34 != v36 );
            }
LABEL_27:
            if ( v20 != 0 )
              goto LABEL_28;
LABEL_54:
            v142 = a1;
            v38 = v141[1] - *v141;
            if ( v38 != 0 )
            {
              v39 = v38 >> 3;
              v40 = 1;
              if ( v39 >= 2 )
                v40 = v39;
              v41 = 0;
              v2 = (__int64)&qword_141B5A4A0;
              do
              {
                v42 = *(__int64 **)(*v141 + 8 * v41);
                v43 = sub_141530EF0(*v142);
                if ( v43 != 0 )
                {
                  v44 = v43;
                  if ( v42 == nullptr )
                    v42 = &qword_141B5A4A0;
                  v45 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v42 + 176LL))(
                                    *v42,
                                    v42,
                                    0);
                  v46 = v45[1] - *v45;
                  if ( v46 != 0 )
                  {
                    v47 = v46 >> 4;
                    v48 = 8;
                    do
                    {
                      v49 = *(__int64 **)(*v45 + v48);
                      if ( v49 == nullptr )
                        v49 = &qword_141B5A4A0;
                      v50 = *(_DWORD *)(*v45 + v48 - 8);
                      if ( v50 > 1768386158 )
                      {
                        if ( v50 == 1768386159 )
                        {
                          *(_BYTE *)(v44 + 36) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v49 + 48LL))(*v49);
                        }
                        else if ( v50 == 1885696611 )
                        {
                          *(float *)(v44 + 32) = (*(float (__fastcall **)(__int64))(*(_QWORD *)*v49 + 96LL))(*v49);
                        }
                      }
                      else if ( v50 == 1181639028 )
                      {
                        sub_140FE7960((__int64)&v140, v49, 0);
                        *(_DWORD *)(v44 + 24) = v140;
                      }
                      else if ( v50 == 1399742836 )
                      {
                        sub_140FE7960((__int64)&v140, v49, 0);
                        *(_DWORD *)(v44 + 28) = v140;
                      }
                      v48 += 16;
                      --v47;
                    }
                    while ( v47 != 0 );
                  }
                }
                ++v41;
              }
              while ( v41 != v40 );
            }
            v51 = qword_141B60C38;
            v52 = qword_141B60C30;
            if ( qword_141B60C30 != qword_141B60C38 )
            {
              while ( *(_DWORD *)v52 != 1986359923 )
              {
                v52 += 16;
                if ( v52 == qword_141B60C38 )
                  goto LABEL_82;
              }
              if ( v52 != qword_141B60C38 )
              {
                LOBYTE(v2) = 1;
                if ( *(_QWORD *)(v52 + 8) != 0 )
                  goto LABEL_216;
              }
            }
LABEL_82:
            LOBYTE(v2) = 1;
            LOBYTE(v51) = 1;
            sub_140EA8A70(v142, v51);
            goto LABEL_216;
          }
          ++v27;
        }
      }
      if ( ++v25 == v26 )
        goto LABEL_27;
    }
  }
  LODWORD(v2) = 0;
  v8 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v7 + 176))(v6, a2, 0);
  v9 = *v8;
  v10 = v8[1];
  if ( *v8 == v10 )
    goto LABEL_216;
  v11 = *v8;
  while ( *(_DWORD *)v11 != 1819504496 )
  {
    v11 += 16;
    if ( v11 == v10 )
      goto LABEL_215;
  }
  if ( v11 == v10 || *(_QWORD *)(v11 + 8) == 0 )
    goto LABEL_215;
  v15 = nullptr;
  while ( *(_DWORD *)v9 != 1819504496 )
  {
    v9 += 16;
    if ( v9 == v10 )
      goto LABEL_86;
  }
  if ( v9 == v10 )
    v15 = nullptr;
  else
    v15 = *(__int64 **)(v9 + 8);
LABEL_86:
  v53 = &qword_141B5A4A0;
  if ( v15 == nullptr )
    v15 = &qword_141B5A4A0;
  switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v15 + 64LL))(*v15) )
  {
    case 0u:
      LOBYTE(v2) = sub_141530EF0(*a1) != 0;
      goto LABEL_216;
    case 1u:
      v54 = a1 + 1;
      v55 = *v8;
      v56 = v8[1];
      v57 = nullptr;
      if ( *v8 != v56 )
      {
        while ( *(_DWORD *)v55 != 1869379180 )
        {
          v55 += 16;
          if ( v55 == v56 )
            goto LABEL_150;
        }
        if ( v55 == v56 )
          v57 = nullptr;
        else
          v57 = *(__int64 **)(v55 + 8);
      }
LABEL_150:
      if ( v57 == nullptr )
        v57 = &qword_141B5A4A0;
      v90 = sub_140EA8D60(v54, v57);
      if ( v90 < 0 )
        goto LABEL_215;
      v91 = v90;
      v92 = *v54;
      v93 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)**v54 + 56LL))(**v54);
      if ( v93 == 3 )
        v94 = &unk_141B60120;
      else
        v94 = v93 == 47 ? &unk_141B60130 : &unk_141B60128;
      v95 = *(__int64 ***)(*(_QWORD *)v94 + 128LL);
      v96 = *v95;
      v97 = v95[1];
      if ( v96 == v97 )
        goto LABEL_215;
      v98 = v91;
      v99 = *v92;
      v100 = 0;
      while ( 2 )
      {
        v101 = *v96;
        if ( *v96 == 0 || *(_DWORD *)(v101 + 40) != *(_DWORD *)(v99 + 12) )
          goto LABEL_160;
        if ( v100 != v98 )
        {
          ++v100;
LABEL_160:
          ++v96;
          LODWORD(v2) = 0;
          if ( v96 == v97 )
            goto LABEL_216;
          continue;
        }
        break;
      }
      v117 = *v8;
      v118 = v8[1];
      v119 = nullptr;
      if ( *v8 == v118 )
      {
        v124 = &qword_141B5A4A0;
      }
      else
      {
        v120 = *v8;
        while ( *(_DWORD *)v120 != 1986096245 )
        {
          v120 += 16;
          if ( v120 == v118 )
            goto LABEL_228;
        }
        if ( v120 == v118 )
          v119 = nullptr;
        else
          v119 = *(__int64 **)(v120 + 8);
LABEL_228:
        v124 = &qword_141B5A4A0;
        if ( v119 != nullptr )
          v124 = v119;
        v119 = nullptr;
        while ( *(_DWORD *)v117 != 1768169504 )
        {
          v117 += 16;
          if ( v117 == v118 )
            goto LABEL_237;
        }
        if ( v117 == v118 )
          v119 = nullptr;
        else
          v119 = *(__int64 **)(v117 + 8);
      }
LABEL_237:
      if ( v119 != nullptr )
        v53 = v119;
      v139 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v53 + 80LL))(*v53, v53);
      LODWORD(v2) = 0;
      if ( v139 > 1768386158 )
      {
        if ( v139 == 1768386159 )
        {
          *(_BYTE *)(v101 + 36) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v124 + 48LL))(*v124, v124);
          LOBYTE(v2) = 1;
        }
        else if ( v139 == 1885696611 )
        {
          *(float *)(v101 + 32) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v124 + 96LL))(*v124, v124);
          LOBYTE(v2) = 1;
        }
      }
      else if ( v139 == 1181639028 )
      {
        sub_140FE7960((__int64)&v140, v124, 0);
        *(_DWORD *)(v101 + 24) = v140;
        LOBYTE(v2) = 1;
      }
      else if ( v139 == 1399742836 )
      {
        sub_140FE7960((__int64)&v140, v124, 0);
        *(_DWORD *)(v101 + 28) = v140;
        LOBYTE(v2) = 1;
      }
LABEL_216:
      LOBYTE(v2) = v2 & 1;
      return (unsigned int)v2;
    case 2u:
      v58 = *v8;
      v59 = v8[1];
      v60 = nullptr;
      if ( *v8 != v59 )
      {
        while ( *(_DWORD *)v58 != 1869379180 )
        {
          v58 += 16;
          if ( v58 == v59 )
            goto LABEL_166;
        }
        if ( v58 == v59 )
          v60 = nullptr;
        else
          v60 = *(__int64 **)(v58 + 8);
      }
LABEL_166:
      if ( v60 != nullptr )
        v53 = v60;
      v102 = sub_140EA8D60(a1 + 1, v53);
      if ( v102 < 0 )
        goto LABEL_215;
      v103 = v102;
      v104 = a1[1];
      v105 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v104 + 56LL))(*v104);
      if ( v105 == 3 )
        v106 = &unk_141B60120;
      else
        v106 = v105 == 47 ? &unk_141B60130 : &unk_141B60128;
      v107 = *(__int64 **)(*(_QWORD *)v106 + 128LL);
      v108 = *v107;
      v109 = v107[1];
      if ( v108 == v109 )
        goto LABEL_215;
      v110 = 0;
      while ( 1 )
      {
        if ( *(_QWORD *)v108 != 0 )
        {
          LODWORD(v2) = *(_DWORD *)(*(_QWORD *)v108 + 40LL);
          if ( (_DWORD)v2 == *(_DWORD *)(*v104 + 12) )
          {
            if ( v110 == v103 )
            {
              v121 = *a1;
              v122 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)**a1 + 56LL))(**a1);
              if ( v122 == 3 )
              {
                v123 = &unk_141B60120;
              }
              else if ( v122 == 47 )
              {
                v123 = &unk_141B60130;
              }
              else
              {
                v123 = &unk_141B60128;
              }
              v125 = *(__int64 **)(*(_QWORD *)v123 + 128LL);
              v126 = *v125;
              v127 = v125[1] - *v125;
              if ( v127 != 0 )
              {
                v128 = v127 >> 3;
                v129 = *v121;
                v130 = 1;
                v131 = 1;
                if ( v128 >= 2 )
                  v131 = v128;
                v132 = -v131;
                LOBYTE(v2) = 1;
                v133 = 0;
                v134 = 0;
                while ( 1 )
                {
                  v137 = *(_QWORD *)(v126 + 8 * v130 - 8);
                  if ( v137 != 0 && *(_DWORD *)(v137 + 40) == *(_DWORD *)(v129 + 12) )
                  {
                    if ( v134 == v103 )
                    {
                      v138 = *(_QWORD *)(v126 + (v133 >> 29));
                      if ( v138 != 0 )
                        sub_140FB2020(v138, v132);
                      sub_141758A00();
                      v125[1] -= 8;
                      goto LABEL_216;
                    }
                    ++v134;
                  }
                  LOBYTE(v2) = v130 < v128;
                  v133 += 0x100000000LL;
                  v136 = v132 + v130++ + 1;
                  if ( v136 == 1 )
                    goto LABEL_216;
                }
              }
LABEL_215:
              LODWORD(v2) = 0;
              goto LABEL_216;
            }
            ++v110;
          }
        }
        v108 += 8;
        LODWORD(v2) = 0;
        if ( v108 == v109 )
          goto LABEL_216;
      }
    case 3u:
      v61 = a1[1];
      v62 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v61 + 56LL))(*v61);
      if ( v62 == 3 )
      {
        v63 = &unk_141B60120;
      }
      else if ( v62 == 47 )
      {
        v63 = &unk_141B60130;
      }
      else
      {
        v63 = &unk_141B60128;
      }
      v67 = *(__int64 **)(*(_QWORD *)v63 + 128LL);
      v68 = *v67;
      v69 = v67[1];
      LOBYTE(v2) = 1;
      if ( v68 == v69 )
        goto LABEL_216;
      v70 = *v61;
      v71 = 0;
      do
      {
        if ( *(_QWORD *)v68 != 0 )
          v71 += *(_DWORD *)(*(_QWORD *)v68 + 40LL) == *(_DWORD *)(v70 + 12);
        v68 += 8;
      }
      while ( v68 != v69 );
      if ( v71 == 0 )
        goto LABEL_216;
      while ( 1 )
      {
        v72 = a1[1];
        v73 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)*v72 + 56LL))(*v72, v70);
        v74 = &unk_141B60120;
        if ( v73 != 3 )
        {
          if ( v73 == 47 )
            v74 = &unk_141B60130;
          else
            v74 = &unk_141B60128;
        }
        --v71;
        v75 = *(__int64 **)(*(_QWORD *)v74 + 128LL);
        v76 = *v75;
        v77 = v75[1];
        if ( v76 == v77 )
          goto LABEL_122;
        v70 = *v72;
        v78 = 0;
        do
        {
          if ( *(_QWORD *)v76 != 0 && *(_DWORD *)(*(_QWORD *)v76 + 40LL) == *(_DWORD *)(v70 + 12) )
          {
            if ( v78 == v71 )
            {
              v79 = *a1;
              v80 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)**a1 + 56LL))(**a1);
              v81 = &unk_141B60120;
              if ( v80 != 3 )
              {
                if ( v80 == 47 )
                  v81 = &unk_141B60130;
                else
                  v81 = &unk_141B60128;
              }
              v82 = *(__int64 **)(*(_QWORD *)v81 + 128LL);
              v83 = *v82;
              v84 = v82[1] - *v82;
              if ( v84 == 0 )
                break;
              v85 = v84 >> 3;
              if ( v85 < 2 )
                v85 = 1;
              v86 = *v79;
              v70 = 0;
              v87 = 0;
              v88 = 0;
              while ( 1 )
              {
                v89 = *(_QWORD *)(v83 + 8 * v87);
                if ( v89 != 0 && *(_DWORD *)(v89 + 40) == *(_DWORD *)(v86 + 12) )
                {
                  if ( v88 == v71 )
                  {
                    if ( *(_QWORD *)(v83 + (v70 >> 29)) != 0 )
                      ((void (*)(void))sub_140FB2020)();
                    sub_141758A00();
                    v82[1] -= 8;
                    goto LABEL_122;
                  }
                  ++v88;
                }
                ++v87;
                v70 += 0x100000000LL;
                if ( v85 == v87 )
                  goto LABEL_122;
              }
            }
            ++v78;
          }
          v76 += 8;
        }
        while ( v76 != v77 );
LABEL_122:
        if ( v71 == 0 )
          goto LABEL_216;
      }
    case 4u:
      v64 = *v8;
      v65 = v8[1];
      v66 = nullptr;
      if ( v64 == v65 )
        goto LABEL_182;
      break;
    case 5u:
      sub_140EA8A70(a1, 0);
      LOBYTE(v2) = 1;
      goto LABEL_216;
    default:
      goto LABEL_215;
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
  v111 = sub_141530EF0(*a1);
  if ( v111 != 0 )
  {
    if ( v66 == nullptr )
      v66 = &qword_141B5A4A0;
    v112 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v66 + 176LL))(*v66, v66, 0);
    v113 = v112[1] - *v112;
    if ( v113 != 0 )
    {
      v114 = v113 >> 4;
      v2 = 8;
      do
      {
        v115 = *(__int64 **)(*v112 + v2);
        if ( v115 == nullptr )
          v115 = &qword_141B5A4A0;
        v116 = *(_DWORD *)(*v112 + v2 - 8);
        if ( v116 > 1768386158 )
        {
          if ( v116 == 1768386159 )
          {
            *(_BYTE *)(v111 + 36) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v115 + 48LL))(*v115);
          }
          else if ( v116 == 1885696611 )
          {
            *(float *)(v111 + 32) = (*(float (__fastcall **)(__int64))(*(_QWORD *)*v115 + 96LL))(*v115);
          }
        }
        else if ( v116 == 1181639028 )
        {
          sub_140FE7960((__int64)&v140, v115, 0);
          *(_DWORD *)(v111 + 24) = v140;
        }
        else if ( v116 == 1399742836 )
        {
          sub_140FE7960((__int64)&v140, v115, 0);
          *(_DWORD *)(v111 + 28) = v140;
        }
        v2 += 16;
        --v114;
      }
      while ( v114 != 0 );
    }
  }
  LOBYTE(v2) = v111 != 0;
  goto LABEL_216;
}
