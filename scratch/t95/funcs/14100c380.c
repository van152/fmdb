char __fastcall sub_14100C380(__int64 a1, __int64 a2, _QWORD *a3)
{
  unsigned int v5; // ebx
  unsigned __int64 v6; // rax
  __int64 v7; // rcx
  unsigned int v8; // eax
  __int64 v9; // rax
  int v10; // r8d
  int v11; // r9d
  unsigned int v12; // eax
  unsigned int v13; // eax
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v16; // rbx
  unsigned __int64 v17; // rbx
  __int64 v18; // rdx
  __int64 v19; // rbx
  __int64 v20; // rcx
  __int64 v21; // rdx
  unsigned int v22; // eax
  __int64 v23; // rax
  __int64 v24; // rcx
  __int64 v25; // rcx
  __int64 v26; // r14
  __int64 v27; // r8
  __int64 v28; // r8
  __int64 v29; // rcx
  __int64 *v30; // rcx
  __int64 v31; // rax
  __int64 v32; // rdx
  __int64 *v33; // rcx
  __int64 v34; // rax
  __int64 v35; // rdx
  _QWORD *v36; // rsi
  _QWORD *v37; // rsi
  __int64 v38; // rsi
  char v39; // al
  bool v40; // zf
  unsigned int v42; // eax
  __int64 v43; // rax
  _QWORD *v44; // rsi
  __int64 v45; // r8
  __int64 v46; // r8
  __int64 v47; // rcx
  __int64 v48; // rax
  char v49; // al
  __int64 v50; // r8
  int v51; // r9d
  int v52; // esi
  int v53; // esi
  unsigned __int16 v54; // ax
  __int16 v55; // bx
  __int16 v56; // di
  bool v57; // cc
  __int16 v58; // bx
  int v59; // r9d
  int v60; // esi
  __int16 v61; // cx
  __int16 v62; // ax
  __int16 v63; // di
  __int64 v64; // rdx
  _WORD *v65; // rdi
  __int64 v66; // rcx
  int v67; // edx
  unsigned __int16 v68; // cx
  int v69; // ecx
  __int64 v70; // rdx
  unsigned __int16 v71; // bx
  __int64 v72; // rdx
  _WORD *v73; // rax
  __int64 *v74; // r12
  __int64 v75; // rax
  __int64 v76; // rcx
  __int64 v77; // rdx
  __int64 v78; // rsi
  __int64 v79; // rsi
  __int64 v80; // rsi
  __int64 v81; // r8
  __int64 *v82; // r12
  __int64 v83; // rax
  __int64 v84; // rcx
  __int64 v85; // rdx
  __int64 v86; // r15
  __int64 v87; // rax
  __int64 v88; // r8
  unsigned int v89; // eax
  __int64 v90; // rax
  int v91; // eax
  __int64 v92; // rbx
  __int64 v93; // rax
  int v94; // r9d
  int v95; // esi
  int v96; // esi
  unsigned __int16 v97; // ax
  __int16 v98; // bx
  __int16 v99; // di
  __int16 v100; // bx
  int v101; // r9d
  int v102; // esi
  __int16 v103; // cx
  __int16 v104; // ax
  __int16 v105; // di
  __int64 v106; // rdx
  _WORD *v107; // rdi
  __int64 v108; // rcx
  int v109; // edx
  unsigned __int16 v110; // cx
  int v111; // ecx
  __int64 v112; // rdx
  unsigned __int16 v113; // bx
  __int64 v114; // rdx
  _WORD *v115; // rax
  __int64 v116; // rdx
  __int64 v117; // rdx
  __int64 v118; // rdx
  __int64 *v119; // rdx
  __int64 *v120; // rdx
  __int64 v121; // rax
  __int64 v122; // rcx
  __int64 *v123; // rdx
  __int64 v124; // rax
  __int64 v125; // rcx
  __int64 *v126; // rdx
  double v127; // xmm0_8
  int v128; // xmm6_4
  __int64 v129; // rax
  __int64 *v130; // rdx
  double v131; // xmm0_8
  int v132; // xmm6_4
  __int64 v133; // rax
  __int64 *v134; // rdx
  __int64 v135; // rax
  __int64 v136; // rsi
  __int64 v137; // r12
  __int64 *v138; // rdx
  __int64 v139; // rcx
  __int64 *v140; // rdx
  _QWORD *v141; // rax
  __int64 v142; // rax
  __int64 v143; // rdx
  __int64 v144; // rcx
  __int64 v145; // rax
  __int64 v146; // rcx
  __int64 v147; // rax
  __int64 v148; // rax
  __int64 v149; // rsi
  __int64 v150; // r12
  __int64 *v151; // rdx
  __int64 v152; // rcx
  __int64 *v153; // rdx
  _QWORD *v154; // rax
  __int64 v155; // rax
  __int64 v156; // rdx
  __int64 v157; // rcx
  __int64 v158; // rax
  __int64 v159; // rcx
  __int64 v160; // rax
  __int64 v161; // rsi
  __int64 v162; // rax
  __int64 v163; // rax
  int v164; // [rsp+30h] [rbp-50h]
  int v165; // [rsp+30h] [rbp-50h]
  __int64 v166; // [rsp+38h] [rbp-48h] BYREF
  __int64 v167; // [rsp+40h] [rbp-40h]
  __int128 v168; // [rsp+50h] [rbp-30h] BYREF
  __int64 v169; // [rsp+60h] [rbp-20h]
  _QWORD v170[2]; // [rsp+70h] [rbp-10h] BYREF
  __int64 v171; // [rsp+88h] [rbp+8h] BYREF
  int v172; // [rsp+90h] [rbp+10h]
  __int64 v173; // [rsp+98h] [rbp+18h]

  v173 = -2;
  while ( 1 )
  {
    while ( 1 )
    {
      v5 = a2;
      if ( (int)a2 > 1296585551 )
      {
        if ( (int)a2 <= 1835223123 )
        {
          if ( (int)a2 <= 1717663280 )
          {
            if ( (int)a2 <= 1315987813 )
            {
              if ( (int)a2 <= 1297240911 )
              {
                if ( (_DWORD)a2 == 1296585552 )
                {
LABEL_143:
                  if ( *(_QWORD *)(a1 - 288) == 0 )
                    return 1;
                  v39 = sub_1400870B0();
                  v40 = v5 == 1128813392;
                  goto LABEL_152;
                }
                if ( (_DWORD)a2 != 1296585817 )
                {
                  if ( (_DWORD)a2 != 1297237328 )
                    goto LABEL_176;
                  goto LABEL_136;
                }
LABEL_148:
                if ( ((_DWORD)a2 != 1128813657) != (unsigned __int8)sub_1400870B0()
                  && (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3) <= 4u )
                {
                  *(_BYTE *)(a1 - 41) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
                }
                return 1;
              }
              if ( (_DWORD)a2 != 1297240912 )
              {
                if ( (_DWORD)a2 != 1297371984 )
                {
                  if ( (_DWORD)a2 != 1315856756 )
                    goto LABEL_176;
                  v22 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
                  if ( v22 == -1 || (v23 = sub_1400568B0(qword_141B5FDD0, v22)) == 0 )
                    v23 = sub_1400568B0(qword_141B5FDD0, 765);
                  *(_QWORD *)(a1 + 112) = v23;
                  *(_QWORD *)(a1 + 136) = *(_QWORD *)(v23 + 232);
                  *(_QWORD *)(a1 + 24) = *(_QWORD *)(a1 + 24) & 0xFFFFFFFEFFFFBFFFuLL | 0x100000000LL;
                  v24 = *(_QWORD *)(a1 + 88);
                  if ( v24 != 0 )
                    *(_WORD *)(v24 + 12) = *(_WORD *)(v23 + 8);
                  v25 = *(_QWORD *)(a1 + 96);
                  if ( v25 != 0 )
                    *(_WORD *)(v25 + 12) = *(_WORD *)(v23 + 8);
                  return 1;
                }
                goto LABEL_146;
              }
              goto LABEL_145;
            }
            if ( (int)a2 <= 1315992421 )
            {
              switch ( (_DWORD)a2 )
              {
                case 0x4E706166:
                  v26 = a1 - 1104;
                  v5 = 1315987814;
                  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 16 )
                  {
                    v170[0] = 0xF0F0F0F0F0F0F0F0uLL;
                    *(_DWORD *)((char *)v170 + 7) = -252645136;
                    sub_1410280C0(&v166, a3, v170);
                    if ( (_DWORD)v166 == 0 )
                    {
                      LODWORD(v166) = 536;
                      LOBYTE(v81) = 1;
                      *(_BYTE *)(a1 - 882) = sub_141332360(v170, &v166, v81);
                      return 1;
                    }
                  }
                  break;
                case 0x4E706466:
                  v26 = a1 - 1104;
                  v5 = 1315988582;
                  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 16 )
                  {
                    v170[0] = 0xF0F0F0F0F0F0F0F0uLL;
                    *(_DWORD *)((char *)v170 + 7) = -252645136;
                    sub_1410280C0(&v166, a3, v170);
                    if ( (_DWORD)v166 == 0 )
                    {
                      LODWORD(v166) = 536;
                      LOBYTE(v88) = 1;
                      *(_BYTE *)(a1 - 883) = sub_141332360(v170, &v166, v88);
                      return 1;
                    }
                  }
                  break;
                case 0x4E707066:
                  v26 = a1 - 1104;
                  v5 = 1315991654;
                  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 16 )
                  {
                    v27 = *(_QWORD *)(a1 - 224);
                    if ( v27 != 0 )
                    {
                      sub_1410280C0(v170, a3, v27 + 144);
                      if ( LODWORD(v170[0]) == 0 )
                      {
                        v29 = *(_QWORD *)(a1 - 224) + 144LL;
                        LODWORD(v170[0]) = 536;
                        LOBYTE(v28) = 1;
                        *(_BYTE *)(a1 - 885) = sub_141332360(v29, v170, v28);
                        return 1;
                      }
                    }
                  }
                  break;
                default:
                  goto LABEL_176;
              }
              goto LABEL_114;
            }
            if ( (int)a2 <= 1684108388 )
            {
              if ( (_DWORD)a2 == 1315992422 )
              {
                v26 = a1 - 1104;
                v5 = 1315992422;
                if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 16 )
                {
                  v45 = *(_QWORD *)(a1 - 224);
                  if ( v45 != 0 )
                  {
                    sub_1410280C0(v170, a3, v45 + 155);
                    if ( LODWORD(v170[0]) == 0 )
                    {
                      v47 = *(_QWORD *)(a1 - 224) + 155LL;
                      LODWORD(v170[0]) = 536;
                      LOBYTE(v46) = 1;
                      *(_BYTE *)(a1 - 884) = sub_141332360(v47, v170, v46);
                      return 1;
                    }
                  }
                }
                goto LABEL_114;
              }
              if ( (_DWORD)a2 != 1416914273 )
                goto LABEL_176;
              return 1;
            }
            if ( (_DWORD)a2 != 1684108389 )
            {
              if ( (_DWORD)a2 == 1684951119 )
              {
                *(_BYTE *)(a1 - 26) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
                return 1;
              }
              goto LABEL_176;
            }
            v48 = sub_140DBC940();
            sub_140DBCA60(v48, v170, a3);
            *(_DWORD *)(a1 + 68) = v170[0];
            if ( (unsigned __int8)sub_140087040() != 0 )
              return 1;
            v49 = sub_14109A7A0(a1, 0x1418761ECLL);
            if ( v49 <= 19 )
            {
              while ( 1 )
              {
                v51 = *(unsigned __int16 *)(a1 + 70);
                v52 = 15;
                if ( (unsigned __int16)(23593 * v51) >= 0xA3Eu )
                  v52 = 3;
                v53 = v51 & v52;
                v54 = *(_WORD *)(a1 + 68) & 0x1FF;
                v55 = v54 - 1;
                v56 = (v53 == 0) + 333;
                LOBYTE(v50) = 12;
                if ( v56 >= (__int16)(v54 - 1) )
                {
                  v56 = (v53 == 0) + 303;
                  LOBYTE(v50) = 11;
                  if ( v56 >= v55 )
                  {
                    LOBYTE(v50) = 10;
                    if ( ((v53 == 0) | 0x110) >= v55 )
                    {
                      LOBYTE(v50) = 9;
                      if ( ((v53 == 0) | 0xF2) >= v55 )
                      {
                        LOBYTE(v50) = 8;
                        if ( (__int16)((v53 == 0) + 211) >= v55 )
                        {
                          LOBYTE(v50) = 7;
                          if ( ((v53 == 0) | 0xB4) >= v55 )
                          {
                            LOBYTE(v50) = 6;
                            if ( ((v53 == 0) | 0x96) >= v55 )
                            {
                              LOBYTE(v50) = 5;
                              if ( (__int16)((v53 == 0) + 119) >= v55 )
                              {
                                LOBYTE(v50) = 4;
                                if ( (__int16)((v53 == 0) + 89) >= v55 )
                                {
                                  LOBYTE(v50) = 3;
                                  if ( ((v53 == 0) | 0x3A) >= v55 )
                                  {
                                    LOBYTE(v50) = 2;
                                    if ( v54 <= 0x1Fu )
                                      LOBYTE(v50) = v54 != 0;
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                    v56 = (v53 == 0) | 0x110;
                    if ( v55 <= v56 )
                    {
                      v56 = (v53 == 0) | 0xF2;
                      if ( v55 <= v56 )
                      {
                        v56 = (v53 == 0) + 211;
                        if ( v55 <= v56 )
                        {
                          v56 = (v53 == 0) | 0xB4;
                          if ( v55 <= v56 )
                          {
                            v56 = (v53 == 0) | 0x96;
                            if ( v55 <= v56 )
                            {
                              v56 = (v53 == 0) + 119;
                              if ( v55 <= v56 )
                              {
                                v56 = (v53 == 0) + 89;
                                if ( v55 <= v56 )
                                {
                                  v56 = (v53 == 0) | 0x3A;
                                  if ( v55 <= v56 )
                                  {
                                    v56 = 30;
                                    if ( v54 <= 0x1Fu )
                                    {
                                      v56 = -1;
                                      if ( v54 == 0 )
                                        goto LABEL_218;
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
                v57 = v55 <= v56;
                v58 = v55 - v56;
                if ( v57 )
                  goto LABEL_218;
                v59 = v51 - 1;
                if ( (unsigned __int16)v58 < 0x1Du )
                {
                  if ( (_BYTE)v50 != 0 )
                  {
                    v60 = (unsigned __int16)v59;
                    v62 = v59
                        - 25
                        * ((((18351 * (unsigned int)(unsigned __int16)v59) >> 16)
                          + ((unsigned __int16)(v59 - ((18351 * (unsigned int)(unsigned __int16)v59) >> 16)) >> 1)) >> 4);
LABEL_224:
                    v69 = 15;
                    if ( v62 != 0 )
                      v69 = 3;
                    v70 = 0x14175C860LL;
                    if ( (v60 & v69) != 0 )
                      v70 = 0x14175C880LL;
                    v71 = (*(_WORD *)(v70 + 2LL * ((unsigned int)(unsigned __int8)v50 - 1)) + v58 + 1) & 0x1FF;
                    v67 = v59;
                    v68 = v71;
                    goto LABEL_229;
                  }
LABEL_218:
                  v67 = 0;
                  v68 = 0;
                  goto LABEL_229;
                }
                v60 = (unsigned __int16)v59;
                v61 = 15;
                v62 = v59
                    - 25
                    * ((((18351 * (unsigned int)(unsigned __int16)v59) >> 16)
                      + ((unsigned __int16)(v59 - ((18351 * (unsigned int)(unsigned __int16)v59) >> 16)) >> 1)) >> 4);
                if ( (_WORD)v59 != 25
                                 * (unsigned __int16)((((18351 * (unsigned int)(unsigned __int16)v59) >> 16)
                                                     + ((unsigned __int16)(v59
                                                                         - ((18351 * (unsigned int)(unsigned __int16)v59) >> 16)) >> 1)) >> 4) )
                  v61 = 3;
                v63 = 31;
                if ( ((unsigned __int16)v59 & (unsigned __int16)v61) != 0 )
                {
                  if ( (_BYTE)v50 == 12 )
                    goto LABEL_222;
                  v64 = (unsigned __int8)v50;
                  v65 = (_WORD *)(2LL * (unsigned __int8)v50 + 0x14175C880LL);
                  v66 = 0x14175C880LL;
                }
                else
                {
                  if ( (_BYTE)v50 == 12 )
                    goto LABEL_222;
                  v64 = (unsigned __int8)v50;
                  v65 = (_WORD *)(2LL * (unsigned __int8)v50 + 0x14175C860LL);
                  v66 = 0x14175C860LL;
                }
                v63 = *v65 - *(_WORD *)(v66 + 2 * v64 - 2);
LABEL_222:
                v67 = 0;
                if ( (_BYTE)v50 != 0 )
                {
                  v68 = 0;
                  if ( v63 >= v58 )
                    goto LABEL_224;
                }
                else
                {
                  v68 = 0;
                }
LABEL_229:
                v72 = (unsigned int)(v67 << 16);
                *(_DWORD *)(a1 + 68) = v72 | v68;
                v73 = (_WORD *)(*(__int64 (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)a1 + 536LL))(
                                 a1,
                                 v72,
                                 v50);
                if ( v73[1] != 1900 || (*v73 & 0x1FF) != 1 )
                {
                  v49 = sub_140B78960(v73, 0x1418761ECLL);
                  if ( v49 >= 20 )
                    break;
                }
              }
            }
            if ( (unsigned __int8)v49 < 0x4Cu )
              return 1;
            while ( 1 )
            {
              v94 = *(unsigned __int16 *)(a1 + 70);
              v95 = 15;
              if ( (unsigned __int16)(23593 * v94) >= 0xA3Eu )
                v95 = 3;
              v96 = v94 & v95;
              v97 = *(_WORD *)(a1 + 68) & 0x1FF;
              v98 = v97 - 1;
              v99 = (v96 == 0) + 333;
              LOBYTE(v50) = 12;
              if ( v99 >= (__int16)(v97 - 1) )
              {
                v99 = (v96 == 0) + 303;
                LOBYTE(v50) = 11;
                if ( v99 >= v98 )
                {
                  LOBYTE(v50) = 10;
                  if ( ((v96 == 0) | 0x110) >= v98 )
                  {
                    LOBYTE(v50) = 9;
                    if ( ((v96 == 0) | 0xF2) >= v98 )
                    {
                      LOBYTE(v50) = 8;
                      if ( (__int16)((v96 == 0) + 211) >= v98 )
                      {
                        LOBYTE(v50) = 7;
                        if ( ((v96 == 0) | 0xB4) >= v98 )
                        {
                          LOBYTE(v50) = 6;
                          if ( ((v96 == 0) | 0x96) >= v98 )
                          {
                            LOBYTE(v50) = 5;
                            if ( (__int16)((v96 == 0) + 119) >= v98 )
                            {
                              LOBYTE(v50) = 4;
                              if ( (__int16)((v96 == 0) + 89) >= v98 )
                              {
                                LOBYTE(v50) = 3;
                                if ( ((v96 == 0) | 0x3A) >= v98 )
                                {
                                  LOBYTE(v50) = 2;
                                  if ( v97 <= 0x1Fu )
                                    LOBYTE(v50) = v97 != 0;
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                  v99 = (v96 == 0) | 0x110;
                  if ( v98 <= v99 )
                  {
                    v99 = (v96 == 0) | 0xF2;
                    if ( v98 <= v99 )
                    {
                      v99 = (v96 == 0) + 211;
                      if ( v98 <= v99 )
                      {
                        v99 = (v96 == 0) | 0xB4;
                        if ( v98 <= v99 )
                        {
                          v99 = (v96 == 0) | 0x96;
                          if ( v98 <= v99 )
                          {
                            v99 = (v96 == 0) + 119;
                            if ( v98 <= v99 )
                            {
                              v99 = (v96 == 0) + 89;
                              if ( v98 <= v99 )
                              {
                                v99 = (v96 == 0) | 0x3A;
                                if ( v98 <= v99 )
                                {
                                  v99 = 30;
                                  if ( v97 <= 0x1Fu )
                                  {
                                    v99 = -1;
                                    if ( v97 == 0 )
                                      goto LABEL_308;
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
              v57 = v98 <= v99;
              v100 = v98 - v99;
              if ( v57 )
                goto LABEL_308;
              v101 = v94 + 1;
              if ( (unsigned __int16)v100 < 0x1Du )
              {
                if ( (_BYTE)v50 != 0 )
                {
                  v102 = (unsigned __int16)v101;
                  v104 = v101
                       - 25
                       * ((((18351 * (unsigned int)(unsigned __int16)v101) >> 16)
                         + ((unsigned __int16)(v101 - ((18351 * (unsigned int)(unsigned __int16)v101) >> 16)) >> 1)) >> 4);
LABEL_314:
                  v111 = 15;
                  if ( v104 != 0 )
                    v111 = 3;
                  v112 = 0x14175C860LL;
                  if ( (v102 & v111) != 0 )
                    v112 = 0x14175C880LL;
                  v113 = (*(_WORD *)(v112 + 2LL * ((unsigned int)(unsigned __int8)v50 - 1)) + v100 + 1) & 0x1FF;
                  v109 = v101;
                  v110 = v113;
                  goto LABEL_319;
                }
LABEL_308:
                v109 = 0;
                v110 = 0;
                goto LABEL_319;
              }
              v102 = (unsigned __int16)v101;
              v103 = 15;
              v104 = v101
                   - 25
                   * ((((18351 * (unsigned int)(unsigned __int16)v101) >> 16)
                     + ((unsigned __int16)(v101 - ((18351 * (unsigned int)(unsigned __int16)v101) >> 16)) >> 1)) >> 4);
              if ( (_WORD)v101 != 25
                                * (unsigned __int16)((((18351 * (unsigned int)(unsigned __int16)v101) >> 16)
                                                    + ((unsigned __int16)(v101
                                                                        - ((18351 * (unsigned int)(unsigned __int16)v101) >> 16)) >> 1)) >> 4) )
                v103 = 3;
              v105 = 31;
              if ( ((unsigned __int16)v101 & (unsigned __int16)v103) != 0 )
              {
                if ( (_BYTE)v50 == 12 )
                  goto LABEL_312;
                v106 = (unsigned __int8)v50;
                v107 = (_WORD *)(2LL * (unsigned __int8)v50 + 0x14175C880LL);
                v108 = 0x14175C880LL;
              }
              else
              {
                if ( (_BYTE)v50 == 12 )
                  goto LABEL_312;
                v106 = (unsigned __int8)v50;
                v107 = (_WORD *)(2LL * (unsigned __int8)v50 + 0x14175C860LL);
                v108 = 0x14175C860LL;
              }
              v105 = *v107 - *(_WORD *)(v108 + 2 * v106 - 2);
LABEL_312:
              v109 = 0;
              if ( (_BYTE)v50 != 0 )
              {
                v110 = 0;
                if ( v105 >= v100 )
                  goto LABEL_314;
              }
              else
              {
                v110 = 0;
              }
LABEL_319:
              v114 = (unsigned int)(v109 << 16);
              *(_DWORD *)(a1 + 68) = v114 | v110;
              v115 = (_WORD *)(*(__int64 (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)a1 + 536LL))(
                                a1,
                                v114,
                                v50);
              if ( v115[1] == 1900 && (*v115 & 0x1FF) == 1 || (char)sub_140B78960(v115, 0x1418761ECLL) <= 75 )
                return 1;
            }
          }
          if ( (int)a2 <= 1819174704 )
          {
            if ( (int)a2 <= 1751937891 )
            {
              v6 = (unsigned int)(a2 - 1717663281);
              if ( (unsigned int)v6 > 0x34 )
                goto LABEL_176;
              v7 = 0x10000000000007LL;
              if ( !_bittest64(&v7, v6) )
                goto LABEL_176;
              v8 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
              if ( v8 != -1 )
              {
                v9 = sub_140F45DB0(qword_141B5FDB8, v8);
                if ( v9 != 0 )
                {
                  LOBYTE(v10) = 1;
                  LOBYTE(v11) = 100;
                  sub_140E03E00(a1 + 160, v9, v10, v11, 0);
                }
              }
              return 1;
            }
            if ( (_DWORD)a2 != 1751937892 && (_DWORD)a2 != 1751937908 )
            {
              if ( (_DWORD)a2 == 1769174133 )
              {
                *(_BYTE *)(a1 - 28) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
                return 1;
              }
              goto LABEL_176;
            }
            v20 = *(_QWORD *)(a1 - 288);
            if ( v20 == 0 )
              return 1;
            goto LABEL_164;
          }
          if ( (int)a2 <= 1833132397 )
          {
            if ( (unsigned int)(a2 - 1819174705) >= 3 )
              goto LABEL_176;
            v13 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            if ( v13 != -1 )
            {
              v14 = sub_140F74E40(qword_141B5FDF8, v13);
              if ( v14 != 0 )
              {
                v15 = *(_QWORD *)(a1 + 288);
                v16 = *(_QWORD *)(a1 + 296) - v15;
                if ( v16 != 0 )
                {
                  v17 = v16 >> 3;
                  v18 = 1;
                  if ( v17 >= 2 )
                    v18 = v17;
                  v19 = 0;
                  while ( **(_QWORD **)(v15 + 8 * v19) != v14 )
                  {
                    if ( v18 == ++v19 )
                      goto LABEL_63;
                  }
                }
                else
                {
LABEL_63:
                  LOBYTE(v170[0]) = 10;
                  sub_140DE2F10(a1 + 40, v14, v170);
                }
              }
            }
            return 1;
          }
          if ( (_DWORD)a2 == 1833132398 )
            return 1;
          if ( (_DWORD)a2 != 1835222614 )
          {
            if ( (_DWORD)a2 != 1835223110 )
              goto LABEL_176;
            goto LABEL_110;
          }
          v26 = a1 - 1104;
          v82 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a3 + 176LL))(*a3, a3, 0);
          v83 = *v82;
          v84 = v82[1];
          v5 = 1835222614;
          if ( *v82 == v84 )
            goto LABEL_114;
          v85 = *v82;
          while ( *(_DWORD *)v85 != 1768169504 )
          {
            v85 += 16;
            if ( v85 == v84 )
              goto LABEL_114;
          }
          if ( v85 == v84 || *(_QWORD *)(v85 + 8) == 0 )
            goto LABEL_114;
          v118 = *v82;
          while ( *(_DWORD *)v118 != 1986096245 )
          {
            v118 += 16;
            if ( v118 == v84 )
              goto LABEL_114;
          }
          if ( v118 == v84 || *(_QWORD *)(v118 + 8) == 0 )
            goto LABEL_114;
          v120 = nullptr;
          while ( *(_DWORD *)v83 != 1768169504 )
          {
            v83 += 16;
            if ( v83 == v84 )
              goto LABEL_365;
          }
          if ( v83 == v84 )
            v120 = nullptr;
          else
            v120 = *(__int64 **)(v83 + 8);
LABEL_365:
          if ( v120 == nullptr )
            v120 = &qword_141B5A4A0;
          v165 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v120 + 80LL))(*v120);
          v124 = *v82;
          v125 = v82[1];
          v126 = nullptr;
          if ( *v82 != v125 )
          {
            while ( *(_DWORD *)v124 != 1986096245 )
            {
              v124 += 16;
              if ( v124 == v125 )
                goto LABEL_383;
            }
            if ( v124 == v125 )
              v126 = nullptr;
            else
              v126 = *(__int64 **)(v124 + 8);
          }
LABEL_383:
          if ( v126 == nullptr )
            v126 = &qword_141B5A4A0;
          v131 = (*(double (__fastcall **)(__int64))(*(_QWORD *)*v126 + 96LL))(*v126);
          v132 = LODWORD(v131);
          sub_1410282A0(a1 - 1104, &v166);
          sub_140833B50(v170, &v166);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v166 + 16LL))(v166, &v166);
          v133 = v170[0];
          v134 = nullptr;
          if ( v170[0] != v170[1] )
          {
            while ( *(_DWORD *)v133 != 1986096245 )
            {
              v133 += 16;
              if ( v133 == v170[1] )
                goto LABEL_418;
            }
            if ( v133 == v170[1] )
              v134 = nullptr;
            else
              v134 = *(__int64 **)(v133 + 8);
          }
LABEL_418:
          if ( v134 == nullptr )
            v134 = &qword_141B5A4A0;
          v148 = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v134 + 184LL))(*v134, v134, 0);
          sub_14083ADC0(&v166, v148);
          if ( v167 == v166 )
          {
LABEL_442:
            sub_1407C9510(&v168);
            v158 = sub_14083D4F0(v157);
            v172 = v165;
            v171 = v158 + 56;
            sub_140835380(&v168, 1768169504, &v171);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
            v160 = sub_14083D4F0(v159);
            v172 = v132;
            v171 = v160 + 104;
            sub_140835380(&v168, 1835222614, &v171);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
            sub_14083DC80(&v171, &v168);
            sub_14083B5F0(&v166, &v171);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
          }
          else
          {
            v149 = 1;
            if ( (unsigned __int64)((v167 - v166) >> 3) >= 2 )
              v149 = (v167 - v166) >> 3;
            v150 = 0;
            while ( 1 )
            {
              v153 = *(__int64 **)(v166 + 8 * v150);
              if ( v153 == nullptr )
                v153 = &qword_141B5A4A0;
              v154 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v153 + 176LL))(
                                 *v153,
                                 v153,
                                 0);
              v168 = 0;
              v169 = 0;
              sub_1408367A0(&v168, (__int64)(v154[1] - *v154) >> 4, v154, v154 + 1);
              v155 = v168;
              if ( (_QWORD)v168 != *((_QWORD *)&v168 + 1) )
              {
                v156 = v168;
                while ( *(_DWORD *)v156 != 1768169504 )
                {
                  v156 += 16;
                  if ( v156 == *((_QWORD *)&v168 + 1) )
                    goto LABEL_429;
                }
                if ( v156 != *((_QWORD *)&v168 + 1) && *(_QWORD *)(v156 + 8) != 0 )
                {
                  while ( *(_DWORD *)v155 != 1768169504 )
                  {
                    v155 += 16;
                    if ( v155 == *((_QWORD *)&v168 + 1) )
                      goto LABEL_441;
                  }
                  if ( v155 != *((_QWORD *)&v168 + 1) )
                  {
                    v151 = *(__int64 **)(v155 + 8);
                    goto LABEL_426;
                  }
LABEL_441:
                  v151 = nullptr;
LABEL_426:
                  if ( v151 == nullptr )
                    v151 = &qword_141B5A4A0;
                  if ( (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)*v151 + 80LL))(*v151) == v165 )
                    break;
                }
              }
LABEL_429:
              sub_140833970(&v168);
              if ( ++v150 == v149 )
                goto LABEL_442;
            }
            v163 = sub_14083D4F0(v152);
            v172 = v132;
            v171 = v163 + 104;
            sub_140835380(&v168, 1835222614, &v171);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
            sub_14083DC80(&v171, &v168);
            sub_14083BE60(&v166, &v171, v150);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
          }
LABEL_443:
          sub_140833970(&v168);
          sub_14083DA80(&v168, &v166);
          sub_140835380(v170, 1986096245, &v168);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v168 + 16LL))(v168, &v168);
          v161 = *(_QWORD *)(a1 - 288);
          sub_14083DC80(&v168, v170);
          sub_140835380(v161, 1835223110, &v168);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v168 + 16LL))(v168, &v168);
          sub_14083B0A0(&v166);
          sub_140833970(v170);
          goto LABEL_114;
        }
        if ( (int)a2 > 1852073331 )
        {
          if ( (int)a2 > 1885434738 )
          {
            if ( (int)a2 <= 1953461878 )
            {
              if ( (_DWORD)a2 != 1885434739 && (_DWORD)a2 != 1919250549 && (_DWORD)a2 != 1953330807 )
                goto LABEL_176;
            }
            else
            {
              if ( (int)a2 > 1986359919 )
              {
                if ( (_DWORD)a2 == 1986359920 )
                  return 1;
                if ( (_DWORD)a2 == 1986949953 )
                {
                  *(_BYTE *)(a1 - 29) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
                  return 1;
                }
                goto LABEL_176;
              }
              if ( (_DWORD)a2 != 1953461879 && (_DWORD)a2 != 1970496880 )
                goto LABEL_176;
            }
            return 1;
          }
          if ( (int)a2 > 1853122155 )
          {
            if ( (_DWORD)a2 == 1853122156 )
            {
              sub_141028510(a1 - 1104, a3);
              return 1;
            }
            if ( (_DWORD)a2 == 1853122419 )
            {
              sub_141021F00(a1 - 1104, a3);
              return 1;
            }
            if ( (_DWORD)a2 != 1869902957 )
              goto LABEL_176;
            return 1;
          }
          switch ( (_DWORD)a2 )
          {
            case 0x6E646574:
              sub_141021870(a1 - 1104, a3);
              return 1;
            case 0x6E6F6E69:
              v20 = *(_QWORD *)(a1 - 288);
              if ( v20 == 0 )
                return 1;
              v21 = 1852796521;
              break;
            case 0x6E6F7473:
              v20 = *(_QWORD *)(a1 - 288);
              if ( v20 == 0 )
                return 1;
              v21 = 1852798067;
              break;
            default:
              goto LABEL_176;
          }
LABEL_165:
          sub_1408351C0(v20, v21, a3);
          return 1;
        }
        if ( (int)a2 <= 1835877184 )
        {
          if ( (int)a2 > 1835495522 )
          {
            if ( (_DWORD)a2 == 1835495523 )
            {
              v78 = *(_QWORD *)(a1 - 136);
              if ( v78 != 0 )
              {
                sub_140310A60(*(_QWORD *)(a1 - 136));
                sub_140E58580(v78);
              }
              *(_QWORD *)(a1 - 136) = 0;
              v79 = sub_140E5FCC0(8);
              sub_140310A50(v79);
              *(_QWORD *)(a1 - 136) = v79;
              sub_141028350(v170, a3, v79);
              if ( LODWORD(v170[0]) != 0 )
              {
                v80 = *(_QWORD *)(a1 - 136);
                if ( v80 != 0 )
                {
                  sub_140310A60(*(_QWORD *)(a1 - 136));
                  sub_140E58580(v80);
                }
                *(_QWORD *)(a1 - 136) = 0;
              }
              return 1;
            }
            if ( (_DWORD)a2 == 1835623016 )
              goto LABEL_151;
            if ( (_DWORD)a2 != 1835876690 )
              goto LABEL_176;
          }
          else
          {
            if ( (_DWORD)a2 == 1835223124 )
            {
              v26 = a1 - 1104;
              v74 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a3 + 176LL))(
                                 *a3,
                                 a3,
                                 0);
              v75 = *v74;
              v76 = v74[1];
              v5 = 1835223124;
              if ( *v74 == v76 )
                goto LABEL_114;
              v77 = *v74;
              while ( *(_DWORD *)v77 != 1768169504 )
              {
                v77 += 16;
                if ( v77 == v76 )
                  goto LABEL_114;
              }
              if ( v77 == v76 || *(_QWORD *)(v77 + 8) == 0 )
                goto LABEL_114;
              v117 = *v74;
              while ( *(_DWORD *)v117 != 1986096245 )
              {
                v117 += 16;
                if ( v117 == v76 )
                  goto LABEL_114;
              }
              if ( v117 == v76 || *(_QWORD *)(v117 + 8) == 0 )
                goto LABEL_114;
              v119 = nullptr;
              while ( *(_DWORD *)v75 != 1768169504 )
              {
                v75 += 16;
                if ( v75 == v76 )
                  goto LABEL_356;
              }
              if ( v75 == v76 )
                v119 = nullptr;
              else
                v119 = *(__int64 **)(v75 + 8);
LABEL_356:
              if ( v119 == nullptr )
                v119 = &qword_141B5A4A0;
              v164 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v119 + 80LL))(*v119);
              v121 = *v74;
              v122 = v74[1];
              v123 = nullptr;
              if ( *v74 != v122 )
              {
                while ( *(_DWORD *)v121 != 1986096245 )
                {
                  v121 += 16;
                  if ( v121 == v122 )
                    goto LABEL_374;
                }
                if ( v121 == v122 )
                  v123 = nullptr;
                else
                  v123 = *(__int64 **)(v121 + 8);
              }
LABEL_374:
              if ( v123 == nullptr )
                v123 = &qword_141B5A4A0;
              v127 = (*(double (__fastcall **)(__int64))(*(_QWORD *)*v123 + 96LL))(*v123);
              v128 = LODWORD(v127);
              sub_1410282A0(a1 - 1104, &v166);
              sub_140833B50(v170, &v166);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v166 + 16LL))(v166, &v166);
              v129 = v170[0];
              v130 = nullptr;
              if ( v170[0] != v170[1] )
              {
                while ( *(_DWORD *)v129 != 1986096245 )
                {
                  v129 += 16;
                  if ( v129 == v170[1] )
                    goto LABEL_392;
                }
                if ( v129 == v170[1] )
                  v130 = nullptr;
                else
                  v130 = *(__int64 **)(v129 + 8);
              }
LABEL_392:
              if ( v130 == nullptr )
                v130 = &qword_141B5A4A0;
              v135 = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v130 + 184LL))(*v130, v130, 0);
              sub_14083ADC0(&v166, v135);
              if ( v167 == v166 )
              {
LABEL_416:
                sub_1407C9510(&v168);
                v145 = sub_14083D4F0(v144);
                v172 = v164;
                v171 = v145 + 56;
                sub_140835380(&v168, 1768169504, &v171);
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
                v147 = sub_14083D4F0(v146);
                v172 = v128;
                v171 = v147 + 104;
                sub_140835380(&v168, 1835223124, &v171);
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
                sub_14083DC80(&v171, &v168);
                sub_14083B5F0(&v166, &v171);
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
              }
              else
              {
                v136 = 1;
                if ( (unsigned __int64)((v167 - v166) >> 3) >= 2 )
                  v136 = (v167 - v166) >> 3;
                v137 = 0;
                while ( 1 )
                {
                  v140 = *(__int64 **)(v166 + 8 * v137);
                  if ( v140 == nullptr )
                    v140 = &qword_141B5A4A0;
                  v141 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v140 + 176LL))(
                                     *v140,
                                     v140,
                                     0);
                  v168 = 0;
                  v169 = 0;
                  sub_1408367A0(&v168, (__int64)(v141[1] - *v141) >> 4, v141, v141 + 1);
                  v142 = v168;
                  if ( (_QWORD)v168 != *((_QWORD *)&v168 + 1) )
                  {
                    v143 = v168;
                    while ( *(_DWORD *)v143 != 1768169504 )
                    {
                      v143 += 16;
                      if ( v143 == *((_QWORD *)&v168 + 1) )
                        goto LABEL_403;
                    }
                    if ( v143 != *((_QWORD *)&v168 + 1) && *(_QWORD *)(v143 + 8) != 0 )
                    {
                      while ( *(_DWORD *)v142 != 1768169504 )
                      {
                        v142 += 16;
                        if ( v142 == *((_QWORD *)&v168 + 1) )
                          goto LABEL_415;
                      }
                      if ( v142 != *((_QWORD *)&v168 + 1) )
                      {
                        v138 = *(__int64 **)(v142 + 8);
                        goto LABEL_400;
                      }
LABEL_415:
                      v138 = nullptr;
LABEL_400:
                      if ( v138 == nullptr )
                        v138 = &qword_141B5A4A0;
                      if ( (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)*v138 + 80LL))(*v138) == v164 )
                        break;
                    }
                  }
LABEL_403:
                  sub_140833970(&v168);
                  if ( ++v137 == v136 )
                    goto LABEL_416;
                }
                v162 = sub_14083D4F0(v139);
                v172 = v128;
                v171 = v162 + 104;
                sub_140835380(&v168, 1835223124, &v171);
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
                sub_14083DC80(&v171, &v168);
                sub_14083BE60(&v166, &v171, v137);
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v171 + 16LL))(v171, &v171);
              }
              goto LABEL_443;
            }
            if ( (_DWORD)a2 != 1835299961 )
            {
              if ( (_DWORD)a2 != 1835492718 )
                goto LABEL_176;
              v12 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
              sub_1410865A0(a1, v12);
              return 1;
            }
          }
        }
        else if ( (int)a2 <= 1836204864 )
        {
          if ( (_DWORD)a2 != 1835877185 && (_DWORD)a2 != 1835877202 && (_DWORD)a2 != 1836204370 )
            goto LABEL_176;
        }
        else
        {
          if ( (int)a2 > 1851878757 )
          {
            if ( (_DWORD)a2 != 1851878758 && (_DWORD)a2 != 1851878764 )
              goto LABEL_176;
            return 1;
          }
          if ( (_DWORD)a2 != 1836204865 && (_DWORD)a2 != 1836204882 )
            goto LABEL_176;
        }
LABEL_110:
        v26 = a1 - 1104;
        v30 = *(__int64 **)(a1 - 288);
        v31 = *v30;
        v32 = v30[1];
        if ( *v30 == v32 )
          goto LABEL_113;
        while ( *(_DWORD *)v31 != v5 )
        {
          v31 += 16;
          if ( v31 == v32 )
            goto LABEL_113;
        }
        if ( v31 == v32 || (v36 = *(_QWORD **)(v31 + 8)) == nullptr )
        {
LABEL_113:
          sub_140835A40(v30, v5, a3);
        }
        else if ( v36 != a3 )
        {
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v36 + 16LL))(*v36, v36);
          (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 24LL))(*a3, a3, v36);
        }
        goto LABEL_114;
      }
      if ( (int)a2 > 1215521892 )
        break;
      if ( (int)a2 <= 1214474611 )
      {
        if ( (int)a2 <= 1129468751 )
        {
          if ( (int)a2 <= 1128813656 )
          {
            if ( (_DWORD)a2 == 846094708 )
            {
              v42 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
              if ( v42 == -1 )
                v43 = 0;
              else
                v43 = sub_1400568B0(qword_141B5FDD0, v42);
              v116 = 0;
              if ( v43 != *(_QWORD *)(a1 + 112) )
                v116 = v43;
              sub_140E02680(a1 + 160, v116);
              return 1;
            }
            if ( (_DWORD)a2 != 1128813392 )
              goto LABEL_176;
            goto LABEL_143;
          }
          if ( (_DWORD)a2 != 1128813657 )
          {
            if ( (_DWORD)a2 != 1129465168 )
              goto LABEL_176;
LABEL_136:
            if ( ((_DWORD)a2 != 1129465168) != (unsigned __int8)sub_1400870B0() )
              *(_DWORD *)(a1 - 128) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
            return 1;
          }
          goto LABEL_148;
        }
        if ( (int)a2 <= 1130979943 )
        {
          if ( (_DWORD)a2 != 1129468752 )
          {
            if ( (_DWORD)a2 != 1129599824 )
              goto LABEL_176;
LABEL_146:
            if ( *(_QWORD *)(a1 - 288) == 0 )
              return 1;
            v39 = sub_1400870B0();
            v40 = v5 == 1129599824;
            goto LABEL_152;
          }
LABEL_145:
          v39 = sub_1400870B0();
          v40 = v5 == 1129468752;
LABEL_152:
          if ( !v40 == v39 )
            return 1;
          v20 = *(_QWORD *)(a1 - 288);
LABEL_164:
          v21 = v5;
          goto LABEL_165;
        }
        if ( (_DWORD)a2 != 1130979944 )
        {
          if ( (_DWORD)a2 != 1213424242 )
            goto LABEL_176;
          v37 = *(_QWORD **)(*(int *)(*(_QWORD *)(a1 - 1096) + 8LL) + a1 - 936);
          if ( v37 != nullptr
            && (*(unsigned __int8 (__fastcall **)(_QWORD))(*v37 + 80LL))(*(_QWORD *)(*(int *)(*(_QWORD *)(a1 - 1096)
                                                                                            + 8LL)
                                                                                   + a1
                                                                                   - 936)) >= 2u )
          {
            v38 = v37[2];
          }
          else
          {
            v38 = 0;
          }
          v91 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          if ( v38 != 0 )
          {
            v92 = 4592;
            if ( *(_BYTE *)(v38 + 47) == 0 )
              v92 = 3832;
            *(_DWORD *)(*(_QWORD *)(a1 - 224) + v92) = v91;
          }
          return 1;
        }
LABEL_151:
        v39 = sub_1400870B0();
        v40 = v5 == 1130979944;
        goto LABEL_152;
      }
      a2 = 1315990113;
      if ( v5 != 1215327339 )
      {
        if ( v5 != 1214474612 )
        {
          if ( v5 == 1214543447 )
          {
            sub_1410202C0(a1 - 1104, a3);
            return 1;
          }
          goto LABEL_176;
        }
        v89 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        if ( v89 == -1 || (v90 = sub_140F74650(qword_141B5FDB0, v89)) == 0 )
        {
          v93 = *(_QWORD *)(a1 + 112);
          if ( v93 != 0 )
          {
            *(_QWORD *)(a1 + 136) = *(_QWORD *)(v93 + 232);
            *(_QWORD *)(a1 + 24) = *(_QWORD *)(a1 + 24) & 0xFFFFFFFEFFFFBFFFuLL | 0x100000000LL;
          }
        }
        else
        {
          *(_QWORD *)(a1 + 136) = v90;
          *(_QWORD *)(a1 + 24) &= 0xFFFFFFFEFFFFBFFFuLL;
        }
        return 1;
      }
    }
    if ( (int)a2 <= 1215917674 )
      break;
    if ( (_DWORD)a2 != 1215917675 )
      goto LABEL_176;
    a2 = 1315990128;
  }
  switch ( (_DWORD)a2 )
  {
    case 0x48736465:
      v86 = a1 - 1104;
      v87 = sub_140FE8230(a1, a2);
      sub_14101E880(v86, a3, v87);
      return 1;
    case 0x48745261:
      sub_14101F3B0(a1 - 1104, a3);
      return 1;
    case 0x48756E57:
      sub_14101F6C0(a1 - 1104, a3);
      return 1;
    default:
      break;
  }
LABEL_176:
  v26 = a1 - 1104;
LABEL_114:
  if ( ((*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5EF38 + 32LL))(qword_141B5EF38) != 0
     || (*(unsigned __int8 (__fastcall **)(__int64, __int64, _QWORD, _QWORD *))(*(_QWORD *)qword_141B5EF38 + 48LL))(
          qword_141B5EF38,
          v26,
          v5,
          a3) == 0)
    && (unsigned __int8)sub_140DC8C00(a1 - 856, v5, a3) == 0 )
  {
    v33 = *(__int64 **)(a1 - 288);
    if ( v33 != nullptr )
    {
      v34 = *v33;
      v35 = v33[1];
      if ( *v33 == v35 )
        goto LABEL_121;
      while ( *(_DWORD *)v34 != v5 )
      {
        v34 += 16;
        if ( v34 == v35 )
          goto LABEL_121;
      }
      if ( v34 == v35 || (v44 = *(_QWORD **)(v34 + 8)) == nullptr )
      {
LABEL_121:
        sub_140835A40(v33, v5, a3);
      }
      else if ( v44 != a3 )
      {
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v44 + 16LL))(*v44, v44);
        (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 24LL))(*a3, a3, v44);
      }
    }
  }
  return 1;
}
