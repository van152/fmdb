__int64 __fastcall sub_140F59C40(__int64 a1, char a2)
{
  __int64 v4; // rax
  __int64 result; // rax
  __int64 v6; // rax
  __int64 v7; // rdi
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 *v11; // rax
  __int64 v12; // rbp
  __int64 v13; // rbx
  __int64 v14; // rax
  unsigned __int64 v15; // rbx
  __int64 v16; // rbp
  __int64 i; // r12
  __int64 v18; // rcx
  __int64 v19; // r14
  __int64 v20; // rcx
  __int64 v21; // rdx
  unsigned __int8 v22; // al
  __int64 *v23; // rbx
  __int64 v24; // rbx
  __int64 v25; // rcx
  char v26; // r8
  __int64 v27; // rbx
  __int64 v28; // rdi
  __int64 v29; // rbx
  int v30; // eax
  int v31; // eax
  char v32; // al
  _QWORD *v33; // r15
  __int64 *v34; // rcx
  __int64 v35; // rdx
  char v36; // cl
  __int64 *v37; // rcx
  __int64 v38; // rdx
  __int64 *v39; // rcx
  __int64 v40; // rcx
  __int64 v41; // rcx
  int v42; // edx
  __int64 v43; // rcx
  __int64 v44; // rax
  int v45; // edx
  int v46; // eax
  __int64 *v47; // rcx
  __int64 v48; // rcx
  _DWORD *v49; // rax
  __int64 v50; // rax
  int v51; // ecx
  int v52; // eax
  __int64 v53; // rax
  int v54; // ecx
  __int64 v55; // rcx
  char v56; // al
  __int64 *v57; // rdx
  __int64 v58; // rdx
  __int64 v59; // rcx
  __int64 v60; // rcx
  __int64 v61; // rcx
  __int64 v62; // rcx
  __int64 v63; // rcx
  __int64 v64; // rcx
  int v65; // eax
  int v66; // ecx
  __int64 v67; // rcx
  __int64 v68; // rax
  int v69; // eax
  int v70; // eax
  int v71; // edx
  __int64 v72; // rcx
  char v73; // al
  __int64 v74; // rcx
  __int64 v75; // rax
  __int64 v76; // rax
  int v77; // eax
  int v78; // edx
  __int64 v79; // rcx
  char v80; // al
  __int64 v81; // rax
  __int64 v82; // rax
  __int64 v83; // rax
  int v84; // edx
  int v85; // eax
  __int64 v86; // rax
  __int64 v87; // rax
  int v88; // eax
  __int64 v89; // rdx
  int v90; // eax
  int v91; // edx
  __int64 v92; // rax
  __int64 v93; // rdx
  __int64 v94; // r8
  __int64 v95; // rdi
  __int64 v96; // rdx
  __int64 v97; // r8
  __int64 v98; // rdx
  __int64 v99; // r8
  __int64 v100; // rdx
  __int64 v101; // r8
  __int64 v102; // rdx
  __int64 v103; // r8
  __int64 v104; // rdx
  __int64 v105; // r8
  __int64 v106; // rdx
  __int64 v107; // r8
  __int64 v108; // rdx
  __int64 v109; // r8
  __int64 v110; // rdx
  __int64 v111; // r8
  __int64 v112; // rdx
  __int64 v113; // r8
  __int64 v114; // rdx
  __int64 v115; // r8
  __int64 v116; // rax
  __int64 v117; // rdx
  __int64 v118; // r8
  __int64 v119; // rax
  __int64 **v120; // rax
  __int64 *v121; // rbp
  __int64 *v122; // r14
  __int64 v123; // rsi
  __int64 v124; // rdi
  __int64 v125; // rdx
  __int64 v126; // rbx
  _QWORD **v127; // rdi
  __int64 v128; // rax
  __int64 v129; // rbx
  __int64 j; // rbp
  _QWORD **v131; // rsi
  __int64 v132; // rdi
  __int64 k; // rbx
  __int64 v134; // [rsp+30h] [rbp-98h] BYREF
  __int16 v135; // [rsp+38h] [rbp-90h]
  char v136; // [rsp+3Ah] [rbp-8Eh]
  __int64 v137; // [rsp+40h] [rbp-88h] BYREF
  __int16 v138; // [rsp+48h] [rbp-80h]
  char v139; // [rsp+4Ah] [rbp-7Eh]
  __int64 v140; // [rsp+50h] [rbp-78h]
  __int64 v141; // [rsp+58h] [rbp-70h]
  __int64 v142; // [rsp+60h] [rbp-68h]
  __int64 v143; // [rsp+68h] [rbp-60h]
  __int64 v144; // [rsp+70h] [rbp-58h]
  __int64 v145; // [rsp+78h] [rbp-50h]
  __int64 v146; // [rsp+80h] [rbp-48h]

  v4 = sub_140F45DB0(a1: qword_141B5FDB8, a2: 2000000001);
  result = sub_141758910(a1: v4, a2: 0, a3: &unk_141AADB10, a4: &unk_141AAF850, a5: 0);
  if ( result == 0 || *(_QWORD *)(result + 368) == 0 )
  {
    sub_140F59AB0(a1, a2: 100000023, a3: 2000000001);
    if ( a2 != 0 )
      sub_140F58410(a1, a2: 0);
    sub_140F3F7E0(a1);
    v6 = sub_1400568B0(a1: qword_141B5FDD0, a2: 145174);
    if ( v6 != 0 )
    {
      v7 = v6;
      v134 = sub_140F74E40(a1: qword_141B5FDF8, a2: 8);
      LOBYTE(v135) = 100;
      sub_1408C9770(a1: v7 + 72, a2: &v134);
    }
    v8 = sub_140F45DB0(a1: qword_141B5FDC0, a2: 72006960);
    if ( v8 != 0 )
      *(_QWORD *)(v8 + 96) = 0;
    v9 = sub_140F45DB0(a1: qword_141B5FDB8, a2: 981732);
    if ( v9 != 0 )
      *(_QWORD *)(v9 + 216) = sub_1400568B0(a1: qword_141B5FDD0, a2: 390);
    *(_BYTE *)(sub_140F45DB0(a1: qword_141B5FDC0, a2: 150988) + 244) = 24;
    v10 = sub_140F45DB0(a1: qword_141B5FDB8, a2: 130834);
    if ( v10 != 0 )
      *(_QWORD *)(v10 + 216) = sub_1400568B0(a1: qword_141B5FDD0, a2: 755);
    if ( *(_BYTE *)(a1 + 1400) != 0 )
    {
      v11 = *(__int64 **)(qword_141B5FE40 + 128);
      v12 = *v11;
      v13 = v11[1];
      v146 = sub_140F45DB0(a1: qword_141B5FDC0, a2: 1301432);
      v141 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 24), a2: 7509144);
      v140 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 24), a2: 7509145);
      v143 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 24), a2: 7500141);
      v145 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 24), a2: 7500140);
      v142 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 24), a2: 7500139);
      v144 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 24), a2: 7500138);
      v14 = sub_140F45DB0(a1: qword_141B5FDC0, a2: 130671);
      if ( v14 != 0 && (*(_BYTE *)(v14 + 417) & 4) != 0 )
        *(_WORD *)(v14 + 384) = 1;
      if ( v13 != v12 )
      {
        v15 = (v13 - v12) >> 3;
        v16 = 1;
        if ( v15 >= 2 )
          v16 = v15;
        for ( i = 0; v16 != i; ++i )
        {
          v19 = *(_QWORD *)(**(_QWORD **)(*(_QWORD *)(a1 + 152) + 128LL) + 8 * i);
          if ( v19 == 0 )
            continue;
          v20 = *(_QWORD *)(v19 + 48);
          v21 = *(_QWORD *)(v19 + 80);
          if ( v20 == 0 || v21 == 0 )
          {
            v22 = *(_BYTE *)(v19 + 47);
            v23 = (__int64 *)(v20 + 368);
            if ( v22 == 0 )
              v23 = (__int64 *)(v20 + 216);
            v24 = *v23;
            if ( v24 != 0
              && *(_DWORD *)(v24 + 12) == 390
              && (*(_BYTE *)(v19 + 40) | v22) == 0
              && (*(_BYTE *)(v20 + 353) & 1) == 0 )
            {
              if ( (unsigned __int8)sub_1408FF650(a1: v20, a2: v21) != 0 )
              {
                v21 = *(_QWORD *)(v19 + 80);
              }
              else
              {
                v21 = v146;
                *(_QWORD *)(v19 + 80) = v146;
              }
            }
          }
          v25 = *(_QWORD *)(v19 + 48);
          if ( v25 != 0 && v21 != 0 && v21 == *(_QWORD *)(v19 + 104) && *(_DWORD *)(v21 + 12) == 40 )
            *(_QWORD *)(v19 + 104) = 0;
          v26 = *(_BYTE *)(v19 + 47);
          v27 = 368;
          if ( v26 == 0 )
            v27 = 216;
          v28 = *(_QWORD *)(v25 + v27);
          if ( v28 != 0 && (v21 == 0 || v25 == 0) && v26 == 0 && *(_DWORD *)(v28 + 12) == 755 )
          {
            v21 = v146;
            *(_QWORD *)(v19 + 80) = v146;
          }
          if ( v25 != 0 && v21 != 0 )
          {
            v29 = *(_QWORD *)(v25 + v27);
            if ( v29 != 0 && v26 == 0 && *(_DWORD *)(v29 + 12) == 801 )
            {
              v30 = *(_DWORD *)(v21 + 12);
              if ( v30 == 353078 || v30 == 353063 )
                sub_140E651E0();
            }
          }
          v31 = *(unsigned __int8 *)(v19 + 40);
          if ( v31 == 15 )
          {
            v32 = *(_BYTE *)(v19 + 47);
            v33 = *(_QWORD **)(v19 + 48);
            v37 = v33 + 46;
            if ( v32 == 0 )
              v37 = v33 + 27;
            v38 = *v37;
            if ( *v37 != 0 )
            {
              v36 = 11;
              if ( *(_DWORD *)(v38 + 12) == 798 )
LABEL_67:
                *(_BYTE *)(v19 + 40) = v36;
            }
          }
          else if ( v31 == 16 )
          {
            v32 = *(_BYTE *)(v19 + 47);
            v33 = *(_QWORD **)(v19 + 48);
            v34 = v33 + 46;
            if ( v32 == 0 )
              v34 = v33 + 27;
            v35 = *v34;
            if ( *v34 != 0 )
            {
              v36 = 30;
              if ( *(_DWORD *)(v35 + 12) == 784 )
                goto LABEL_67;
            }
          }
          else
          {
            v32 = *(_BYTE *)(v19 + 47);
            v33 = *(_QWORD **)(v19 + 48);
          }
          v39 = v33 + 46;
          if ( v32 == 0 )
            v39 = v33 + 27;
          v40 = *v39;
          if ( v40 != 0 && *(_DWORD *)(v40 + 12) == 788 && v33 != nullptr )
          {
            v41 = *(_QWORD *)(v19 + 80);
            if ( v41 != 0 )
            {
              v42 = *(_DWORD *)(v41 + 12);
              if ( (unsigned int)(v42 - 55065659) < 7 || v42 == 55065643 )
              {
                *(_BYTE *)(v41 + 417) |= 4u;
                v134 = -1;
                v135 = 0;
                v43 = *(_QWORD *)(v19 + 48);
                if ( v43 != 0 && (v44 = *(_QWORD *)(v19 + 80)) != 0 )
                {
                  v45 = *(_DWORD *)(v44 + 12);
                  LODWORD(v134) = v45;
                  v46 = *(_DWORD *)(v44 + 16);
                  if ( v46 == 0 )
                    v46 = v45;
                }
                else
                {
                  LODWORD(v134) = -1;
                  v46 = -1;
                }
                HIDWORD(v134) = v46;
                v136 = 2;
                if ( *(_BYTE *)(v19 + 47) != 0 )
                  v43 = 0;
                sub_140E62BA0(a1: v43, a2: &v134);
                v32 = *(_BYTE *)(v19 + 47);
                v33 = *(_QWORD **)(v19 + 48);
              }
            }
          }
          v47 = v33 + 46;
          if ( v32 == 0 )
            v47 = v33 + 27;
          v48 = *v47;
          if ( v48 != 0 && *(_DWORD *)(v48 + 12) == 45 && v32 == 0 && v33 != nullptr )
          {
            v49 = (_DWORD *)v33[39];
            if ( v49 == nullptr || ((v49[2] - *v49) & 0x7F8) == 0 )
            {
              v50 = *(_QWORD *)(v19 + 80);
              if ( v50 != 0 && (unsigned int)((v51 = *(_DWORD *)(v50 + 12)) - 136513) <= 1 )
              {
                v135 = 0;
                LODWORD(v134) = v51;
                v52 = *(_DWORD *)(v50 + 16);
                if ( v52 == 0 )
                  v52 = v51;
              }
              else
              {
                v134 = -1;
                v135 = 0;
                v53 = sub_140F45DB0(a1: qword_141B5FDC0, a2: (unsigned int)(i & 1) + 136513);
                if ( v53 != 0 )
                {
                  v54 = *(_DWORD *)(v53 + 12);
                  LODWORD(v134) = v54;
                  v52 = *(_DWORD *)(v53 + 16);
                  if ( v52 == 0 )
                    v52 = v54;
                }
                else
                {
                  LODWORD(v134) = -1;
                  v52 = -1;
                }
              }
              HIDWORD(v134) = v52;
              v136 = 1;
              sub_140E62BA0(a1: v33, a2: &v134);
            }
          }
          v55 = *(_QWORD *)(v19 + 48);
          if ( v55 == 0 || *(_QWORD *)(v19 + 80) == 0 )
            continue;
          v56 = *(_BYTE *)(v19 + 47);
          v57 = (__int64 *)(v55 + 368);
          if ( v56 == 0 )
            v57 = (__int64 *)(v55 + 216);
          v58 = *v57;
          if ( v58 == 0 || *(_DWORD *)(v58 + 12) != 760 )
            continue;
          if ( v56 != 0 )
            v55 = 0;
          if ( v140 == 0 || v141 == 0 || v55 == 0 || (unsigned __int8)sub_140E65030(a1: v55, a2: v141) != 0 )
            continue;
          v59 = *(_BYTE *)(v19 + 47) != 0 ? 0LL : *(_QWORD *)(v19 + 48);
          if ( (unsigned __int8)sub_140E65030(a1: v59, a2: v140) != 0 )
            continue;
          if ( *(_BYTE *)(v19 + 47) != 0 )
            v60 = 0;
          else
            v60 = *(_QWORD *)(v19 + 48);
          if ( (unsigned __int8)sub_140E65030(a1: v60, a2: v145) != 0
            || (*(_BYTE *)(v19 + 47) != 0 ? (v61 = 0) : (v61 = *(_QWORD *)(v19 + 48)),
                (unsigned __int8)sub_140E65030(a1: v61, a2: v144) != 0) )
          {
            v135 = 0;
            v62 = v141;
          }
          else
          {
            if ( *(_BYTE *)(v19 + 47) != 0 )
              v63 = 0;
            else
              v63 = *(_QWORD *)(v19 + 48);
            if ( (unsigned __int8)sub_140E65030(a1: v63, a2: v143) == 0 )
            {
              v64 = *(_BYTE *)(v19 + 47) != 0 ? 0LL : *(_QWORD *)(v19 + 48);
              if ( (unsigned __int8)sub_140E65030(a1: v64, a2: v142) == 0 )
              {
                v67 = *(_QWORD *)(v19 + 48);
                if ( v67 == 0 )
                  continue;
                v68 = *(_QWORD *)(v19 + 80);
                if ( v68 == 0 )
                  continue;
                v69 = *(_DWORD *)(v68 + 12);
                switch ( v69 )
                {
                  case 7500138:
                  case 7500140:
                    goto LABEL_149;
                  case 7500139:
                  case 7500141:
                    goto LABEL_160;
                  default:
                    if ( v69 == 7509145 )
                    {
LABEL_160:
                      v135 = 0;
                      v77 = *(_DWORD *)(v140 + 12);
                      LODWORD(v134) = v77;
                      v78 = *(_DWORD *)(v140 + 16);
                      if ( v78 == 0 )
                        v78 = v77;
                      HIDWORD(v134) = v78;
                      v136 = 1;
                      if ( *(_BYTE *)(v19 + 47) != 0 )
                        v67 = 0;
                      sub_140E62BA0(a1: v67, a2: &v134);
                      v79 = 0;
                      if ( *(_BYTE *)(v19 + 47) == 0 )
                        v79 = *(_QWORD *)(v19 + 48);
                      v80 = sub_140E65030(a1: v79, a2: v143);
                      v74 = *(_QWORD *)(v19 + 48);
                      if ( v80 == 0 )
                      {
                        v81 = *(_QWORD *)(v19 + 48);
                        if ( v74 != 0 )
                          v81 = *(_QWORD *)(v19 + 80);
                        if ( *(_DWORD *)(v81 + 12) == 7500141 )
                        {
                          v137 = -1;
                          v138 = 0;
                          v76 = v143;
                          goto LABEL_185;
                        }
                      }
                      if ( *(_BYTE *)(v19 + 47) != 0 )
                        v74 = 0;
                      if ( (unsigned __int8)sub_140E65030(a1: v74, a2: v142) == 0 )
                      {
                        v74 = *(_QWORD *)(v19 + 48);
                        v82 = v74;
                        if ( v74 != 0 )
                          v82 = *(_QWORD *)(v19 + 80);
                        if ( *(_DWORD *)(v82 + 12) == 7500139 )
                        {
                          v137 = -1;
                          v138 = 0;
                          v76 = v142;
                          goto LABEL_185;
                        }
                      }
                    }
                    else
                    {
                      if ( v69 != 7509144 )
                        goto LABEL_193;
LABEL_149:
                      v135 = 0;
                      v70 = *(_DWORD *)(v141 + 12);
                      LODWORD(v134) = v70;
                      v71 = *(_DWORD *)(v141 + 16);
                      if ( v71 == 0 )
                        v71 = v70;
                      HIDWORD(v134) = v71;
                      v136 = 1;
                      if ( *(_BYTE *)(v19 + 47) != 0 )
                        v67 = 0;
                      sub_140E62BA0(a1: v67, a2: &v134);
                      v72 = 0;
                      if ( *(_BYTE *)(v19 + 47) == 0 )
                        v72 = *(_QWORD *)(v19 + 48);
                      v73 = sub_140E65030(a1: v72, a2: v145);
                      v74 = *(_QWORD *)(v19 + 48);
                      if ( v73 == 0 )
                      {
                        v75 = *(_QWORD *)(v19 + 48);
                        if ( v74 != 0 )
                          v75 = *(_QWORD *)(v19 + 80);
                        if ( *(_DWORD *)(v75 + 12) == 7500140 )
                        {
                          v137 = -1;
                          v138 = 0;
                          v76 = v145;
LABEL_185:
                          if ( v76 != 0 )
                          {
                            v84 = *(_DWORD *)(v76 + 12);
                            LODWORD(v137) = v84;
                            v85 = *(_DWORD *)(v76 + 16);
                            if ( v85 == 0 )
                              v85 = v84;
                          }
                          else
                          {
                            LODWORD(v137) = -1;
                            v85 = -1;
                          }
                          HIDWORD(v137) = v85;
                          v139 = 2;
                          if ( *(_BYTE *)(v19 + 47) != 0 )
                            v74 = 0;
                          sub_140E62BA0(a1: v74, a2: &v137);
                          goto LABEL_193;
                        }
                      }
                      if ( *(_BYTE *)(v19 + 47) != 0 )
                        v74 = 0;
                      if ( (unsigned __int8)sub_140E65030(a1: v74, a2: v144) == 0 )
                      {
                        v74 = *(_QWORD *)(v19 + 48);
                        v83 = v74;
                        if ( v74 != 0 )
                          v83 = *(_QWORD *)(v19 + 80);
                        if ( *(_DWORD *)(v83 + 12) == 7500138 )
                        {
                          v137 = -1;
                          v138 = 0;
                          v76 = v144;
                          goto LABEL_185;
                        }
                      }
                    }
LABEL_193:
                    v18 = *(_QWORD *)(v19 + 48);
                    v86 = v18;
                    if ( v18 != 0 )
                      v86 = *(_QWORD *)(v19 + 80);
                    if ( *(_DWORD *)(v86 + 12) != 7500000 )
                      continue;
                    v87 = *(_QWORD *)(v19 + 96);
                    if ( v87 == 0 )
                      continue;
                    v88 = *(_DWORD *)(v87 + 12);
                    if ( v88 == 7509145 )
                    {
                      v135 = 0;
                      v89 = v140;
                    }
                    else
                    {
                      if ( v88 != 7509144 )
                        continue;
                      v135 = 0;
                      v89 = v141;
                    }
                    v90 = *(_DWORD *)(v89 + 12);
                    LODWORD(v134) = v90;
                    v91 = *(_DWORD *)(v89 + 16);
                    if ( v91 == 0 )
                      v91 = v90;
                    HIDWORD(v134) = v91;
                    v136 = 1;
                    if ( *(_BYTE *)(v19 + 47) != 0 )
                      v18 = 0;
                    break;
                }
                goto LABEL_22;
              }
            }
            v135 = 0;
            v62 = v140;
          }
          v65 = *(_DWORD *)(v62 + 12);
          LODWORD(v134) = v65;
          v66 = *(_DWORD *)(v62 + 16);
          if ( v66 == 0 )
            v66 = v65;
          HIDWORD(v134) = v66;
          v136 = 1;
          if ( *(_BYTE *)(v19 + 47) != 0 )
            v18 = 0;
          else
            v18 = *(_QWORD *)(v19 + 48);
LABEL_22:
          sub_140E62BA0(a1: v18, a2: &v134);
        }
      }
      if ( *(_BYTE *)(a1 + 1400) != 0 )
      {
        if ( (unsigned __int8)sub_140087070() != 0 )
        {
          v92 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 16), a2: 2000000000);
          if ( v92 != 0 )
          {
            v95 = v92;
            LOBYTE(v93) = 4;
            LOBYTE(v94) = 1;
            sub_1411D6720(a1: v92, a2: v93, a3: v94, a4: 72044480);
            LOBYTE(v96) = 5;
            LOBYTE(v97) = 1;
            sub_1411D6720(a1: v95, a2: v96, a3: v97, a4: 72044481);
            LOBYTE(v98) = 6;
            LOBYTE(v99) = 1;
            sub_1411D6720(a1: v95, a2: v98, a3: v99, a4: 72044482);
            LOBYTE(v100) = 7;
            LOBYTE(v101) = 1;
            sub_1411D6720(a1: v95, a2: v100, a3: v101, a4: 72044483);
            LOBYTE(v102) = 20;
            LOBYTE(v103) = 1;
            sub_1411D6720(a1: v95, a2: v102, a3: v103, a4: 0xFFFFFFFFLL);
            LOBYTE(v104) = 8;
            LOBYTE(v105) = 1;
            sub_1411D6720(a1: v95, a2: v104, a3: v105, a4: 0xFFFFFFFFLL);
            LOBYTE(v106) = 31;
            LOBYTE(v107) = 1;
            sub_1411D6720(a1: v95, a2: v106, a3: v107, a4: 0xFFFFFFFFLL);
            LOBYTE(v108) = 27;
            LOBYTE(v109) = 1;
            sub_1411D6720(a1: v95, a2: v108, a3: v109, a4: 0xFFFFFFFFLL);
            LOBYTE(v110) = 28;
            LOBYTE(v111) = 1;
            sub_1411D6720(a1: v95, a2: v110, a3: v111, a4: 0xFFFFFFFFLL);
            LOBYTE(v112) = 32;
            LOBYTE(v113) = 1;
            sub_1411D6720(a1: v95, a2: v112, a3: v113, a4: 0xFFFFFFFFLL);
            LOBYTE(v114) = 34;
            LOBYTE(v115) = 1;
            sub_1411D6720(a1: v95, a2: v114, a3: v115, a4: 0xFFFFFFFFLL);
          }
        }
        v116 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 16), a2: 2000000002);
        if ( v116 != 0 )
        {
          LOBYTE(v117) = 45;
          LOBYTE(v118) = 1;
          sub_1411D6720(a1: v116, a2: v117, a3: v118, a4: 0xFFFFFFFFLL);
        }
        if ( (unsigned __int8)sub_1400870B0() == 0 )
        {
          v119 = sub_140F45DB0(a1: *(_QWORD *)(a1 + 24), a2: 14);
          if ( v119 != 0 && *(_BYTE *)(v119 + 419) == 0 )
            *(_BYTE *)(v119 + 419) = 60;
        }
      }
    }
    v120 = *(__int64 ***)(qword_141B5FE08 + 128);
    v121 = *v120;
    v122 = v120[1];
    while ( v121 != v122 )
    {
      v123 = *v121;
      v124 = *(_QWORD *)(*v121 + 1056);
      if ( (unsigned __int64)(*(_QWORD *)(*v121 + 1064) - v124) >= 0x2D )
      {
        v125 = *(_QWORD *)(*v121 + 1064) - 44LL;
        if ( v124 != v125 )
        {
          v126 = *(_QWORD *)(*v121 + 1064) - v125;
          sub_141758A00(a1: *(_QWORD *)(*v121 + 1056), a2: v125, a3: v126);
          *(_QWORD *)(v123 + 1064) = v124 + v126;
        }
      }
      ++v121;
    }
    v127 = *(_QWORD ***)(a1 + 144);
    sub_1409E2AA0(a1: *v127[16], a2: v127[16][1], a3: (__int64)(v127[16][1] - *v127[16]) >> 3, a4: sub_1400115D0);
    v128 = ((__int64 (__fastcall *)(_QWORD **))(*v127)[6])(a1: v127);
    if ( v128 != 0 )
    {
      v129 = v128;
      for ( j = 0; j != v129; ++j )
        *(_DWORD *)(((__int64 (__fastcall *)(_QWORD **, _QWORD))(*v127)[2])(a1: v127, a2: (unsigned int)j) + 8) = j;
    }
    v131 = *(_QWORD ***)(a1 + 184);
    sub_1409E2AA0(a1: *v131[16], a2: v131[16][1], a3: (__int64)(v131[16][1] - *v131[16]) >> 3, a4: sub_1400115D0);
    result = ((__int64 (__fastcall *)(_QWORD **))(*v131)[6])(a1: v131);
    if ( result != 0 )
    {
      v132 = result;
      for ( k = 0; k != v132; ++k )
      {
        result = ((__int64 (__fastcall *)(_QWORD **, _QWORD))(*v131)[2])(a1: v131, a2: (unsigned int)k);
        *(_DWORD *)(result + 8) = k;
      }
    }
  }
  return result;
}
