__int64 __fastcall sub_141063F30(__int64 a1, __int64 a2, __int64 *a3)
{
  __int64 j; // rbx
  __int64 *v4; // rsi
  _WORD *v5; // rdi
  __int64 v6; // r8
  char v7; // al
  __int64 v8; // rcx
  __int64 v9; // rdi
  __int64 *v10; // rsi
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rdx
  char v14; // al
  _QWORD *v15; // rcx
  __int64 v16; // rdi
  __int64 *v17; // rsi
  __int64 v18; // rax
  __int64 v19; // rcx
  __int64 v20; // rdx
  char v21; // al
  __int64 v22; // rcx
  __int64 v23; // rdi
  __int64 *v24; // rsi
  __int64 v25; // rax
  __int64 v26; // rcx
  __int64 v27; // rdx
  char v28; // al
  __int64 v29; // rcx
  __int64 v30; // rdi
  __int64 *v31; // rsi
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rdx
  char v35; // al
  __int64 v36; // rcx
  __int64 v37; // rdi
  __int64 *v38; // rsi
  __int64 v39; // rax
  __int64 v40; // rcx
  __int64 v41; // rdx
  __int64 v43; // rdi
  __int64 v44; // rcx
  __int64 v45; // r8
  __int64 v46; // rdx
  _QWORD *v47; // r14
  __int64 v48; // r15
  __int64 v49; // rdi
  _QWORD *v50; // rsi
  _QWORD *v51; // r14
  __int64 v52; // r15
  __int64 v53; // rdi
  _QWORD *v54; // rsi
  _QWORD *v55; // r15
  __int64 v56; // rdi
  __int64 v57; // rdi
  _QWORD *v58; // rsi
  _QWORD *v59; // r14
  __int64 v60; // r15
  __int64 v61; // rdi
  _QWORD *v62; // rsi
  __int64 v63; // rdx
  _QWORD *v64; // r14
  _QWORD *v65; // rax
  __int64 v66; // rdi
  __int64 v67; // rdi
  bool v68; // cf
  _QWORD *v69; // rax
  __int64 v70; // rax
  unsigned __int64 v71; // rax
  __int64 v72; // rsi
  __int64 *v73; // rdx
  __int64 v74; // rax
  __int64 v75; // rax
  unsigned __int64 v76; // rax
  __int64 v77; // rsi
  __int64 *v78; // rdx
  __int64 v79; // rax
  __int64 v80; // rax
  unsigned __int64 v81; // rax
  __int64 i; // rsi
  __int64 *v83; // rdx
  __int64 v84; // rax
  __int64 v85; // rax
  unsigned __int64 v86; // rax
  __int64 v87; // rsi
  __int64 *v88; // rdx
  __int64 v89; // rax
  __int64 v90; // rax
  unsigned __int64 v91; // rax
  __int64 k; // rsi
  __int64 *v93; // rdx
  __int64 v94; // rax
  __int64 *v95; // rax
  __int64 v96; // r14
  unsigned int v97; // eax
  __int64 *v98; // rdx
  __int64 *v99; // rdx
  __int64 *v100; // rdx
  __int64 *v101; // rdx
  __int64 *v102; // rdx
  __int64 v103; // rdx
  __int64 v104; // r8
  __int64 v105; // rdi
  _QWORD *v106; // rax
  __int64 v107; // rax
  __int64 v108; // rcx
  __int64 *v109; // rdx
  __int64 v110; // rcx
  __int64 v111; // rdx
  __int64 v112; // rax
  __int64 v113; // rdi
  __int64 v114; // r14
  unsigned __int64 v115; // rdi
  __int64 v116; // rsi
  _QWORD *v117; // r15
  __int64 v118; // rcx
  __int64 v119; // rdx
  __int64 v120; // rax
  __int64 v121; // rax
  __int64 v122; // rcx
  __int64 *v123; // rdx
  __int64 v124; // rcx
  __int64 v125; // rdx
  __int64 v126; // rax
  __int64 v127; // r15
  __int64 v128; // r15
  __int64 v129; // rdi
  _QWORD *v130; // rsi
  __int64 v131; // rcx
  __int64 v132; // rdx
  __int64 v133; // rax
  __int64 v134; // rax
  __int64 v135; // rcx
  __int64 *v136; // rdx
  __int64 v137; // rcx
  __int64 v138; // rdx
  __int64 v139; // rax
  __int64 v140; // rdi
  __int64 v141; // r14
  unsigned __int64 v142; // rdi
  __int64 v143; // rsi
  _QWORD *v144; // r15
  __int64 v145; // rcx
  __int64 v146; // rdx
  __int64 v147; // rax
  __int64 v148; // rax
  __int64 v149; // rcx
  __int64 *v150; // rdx
  __int64 v151; // rcx
  __int64 v152; // rdx
  __int64 v153; // rax
  __int64 v154; // rdi
  __int64 v155; // r14
  unsigned __int64 v156; // rdi
  __int64 v157; // rsi
  _QWORD *v158; // r15
  __int64 v159; // rcx
  __int64 v160; // rdx
  __int64 v161; // rax
  __int64 v162; // rax
  __int64 v163; // rcx
  __int64 *v164; // rdx
  __int64 v165; // rcx
  __int64 v166; // rdx
  __int64 v167; // rax
  _QWORD *v168; // rax
  __int64 v169; // rsi
  __int64 v170; // rsi
  _QWORD *v171; // rax
  __int64 v172; // rcx
  __int64 v173; // rdx
  __int64 v174; // rax
  int v175; // eax
  __int64 v176; // r14
  __int64 v177; // r14
  __int64 v178; // rdi
  __int64 v179; // rcx
  __int64 *v180; // rdx
  __int64 v181; // rax
  __int64 *v182; // rsi
  int v183; // eax
  _QWORD *v184; // rsi
  __int64 v185; // rcx
  int v186; // eax
  __int64 v187; // r12
  __int64 v188; // r15
  __int64 v189; // rdi
  __int64 v190; // rcx
  __int64 *v191; // rdx
  __int64 v192; // rax
  __int64 *v193; // rsi
  int v194; // eax
  _QWORD *v195; // rsi
  __int64 v196; // rcx
  int v197; // eax
  __int64 v198; // r14
  __int64 v199; // r14
  __int64 v200; // rdi
  __int64 v201; // rcx
  __int64 *v202; // rdx
  __int64 v203; // rax
  __int64 *v204; // rsi
  int v205; // eax
  _QWORD *v206; // rsi
  __int64 v207; // rcx
  int v208; // eax
  __int64 v209; // r14
  __int64 v210; // r14
  __int64 v211; // rdi
  __int64 v212; // rcx
  __int64 *v213; // rdx
  __int64 v214; // rax
  __int64 *v215; // rsi
  int v216; // eax
  _QWORD *v217; // rsi
  __int64 v218; // rcx
  int v219; // eax
  __int64 *v220; // rcx
  __int64 v221; // r15
  __int64 v222; // r14
  __int64 v223; // rdi
  __int64 v224; // rcx
  __int64 *v225; // rdx
  __int64 v226; // rax
  int v227; // eax
  _QWORD *v228; // rcx
  __int64 *v229; // rsi
  unsigned int v230; // eax
  __int64 v231; // r15
  int v232; // eax
  unsigned int v233; // eax
  unsigned int v234; // eax
  __int64 v235; // r14
  int v236; // eax
  __int128 v237; // [rsp+30h] [rbp-50h] BYREF
  __int64 v238; // [rsp+40h] [rbp-40h]
  __int64 v239; // [rsp+48h] [rbp-38h]
  __int128 *v240; // [rsp+188h] [rbp+108h] BYREF
  char *v241; // [rsp+190h] [rbp+110h] BYREF
  _QWORD *v242; // [rsp+198h] [rbp+118h] BYREF
  _QWORD v243[8]; // [rsp+1A0h] [rbp+120h] BYREF

  v243[1] = -2;
  v4 = a3;
  v5 = (_WORD *)a1;
  if ( (int)a2 > 1315202415 )
  {
    if ( (int)a2 > 1315791217 )
    {
      if ( (int)a2 > 1316189281 )
      {
        if ( (int)a2 > 1316318560 )
        {
          switch ( (_DWORD)a2 )
          {
            case 0x4E756D61:
              *(_BYTE *)(a1 + 1950) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
              goto LABEL_325;
            case 0x4E75706D:
              *(_BYTE *)(a1 + 1972) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
              goto LABEL_325;
            case 0x4E776964:
              *(_BYTE *)(a1 + 1973) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
              goto LABEL_325;
            default:
              break;
          }
          goto LABEL_124;
        }
        switch ( (_DWORD)a2 )
        {
          case 0x4E737462:
            *(_BYTE *)(a1 + 1970) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E74706F:
            *(_BYTE *)(a1 + 1971) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E747263:
            v242 = (_QWORD *)a1;
            v243[0] = a1;
            v240 = (__int128 *)&v242;
            v241 = (char *)v243;
            v14 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
            v15 = (_QWORD *)*v4;
            v16 = *(_QWORD *)*v4;
            if ( v14 == 10 )
            {
              LODWORD(j) = 0;
              v17 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD *, __int64 *, _QWORD))(v16 + 176))(v15, v4, 0);
              v18 = *v17;
              v19 = v17[1];
              if ( *v17 != v19 )
              {
                v20 = *v17;
                while ( *(_DWORD *)v20 != 1819504496 )
                {
                  v20 += 16;
                  if ( v20 == v19 )
                    goto LABEL_669;
                }
                if ( v20 != v19 && *(_QWORD *)(v20 + 8) != 0 )
                {
                  v99 = nullptr;
                  while ( *(_DWORD *)v18 != 1819504496 )
                  {
                    v18 += 16;
                    if ( v18 == v19 )
                      goto LABEL_333;
                  }
                  if ( v18 == v19 )
                    v99 = nullptr;
                  else
                    v99 = *(__int64 **)(v18 + 8);
LABEL_333:
                  j = (__int64)&qword_141B5A4A0;
                  if ( v99 == nullptr )
                    v99 = &qword_141B5A4A0;
                  switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v99 + 64LL))(*v99) )
                  {
                    case 0u:
                      v237 = 0;
                      LOWORD(v239) = 0;
                      v238 = 0;
                      sub_14103AF20(v242 + 24, &v237);
                      goto LABEL_325;
                    case 1u:
                      v121 = *v17;
                      v122 = v17[1];
                      v123 = nullptr;
                      if ( *v17 != v122 )
                      {
                        while ( *(_DWORD *)v121 != 1869379180 )
                        {
                          v121 += 16;
                          if ( v121 == v122 )
                            goto LABEL_496;
                        }
                        if ( v121 == v122 )
                          v123 = nullptr;
                        else
                          v123 = *(__int64 **)(v121 + 8);
                      }
LABEL_496:
                      if ( v123 == nullptr )
                        v123 = &qword_141B5A4A0;
                      v186 = sub_141076640(&v241, v123);
                      if ( v186 < 0 )
                        goto LABEL_669;
                      v187 = *(_QWORD *)(v243[0] + 192LL);
                      if ( v187 == 0 )
                        goto LABEL_669;
                      v188 = (unsigned int)v186;
                      v189 = *v17;
                      v190 = v17[1];
                      v191 = nullptr;
                      if ( *v17 == v190 )
                      {
                        v193 = &qword_141B5A4A0;
                      }
                      else
                      {
                        v192 = *v17;
                        while ( *(_DWORD *)v192 != 1986096245 )
                        {
                          v192 += 16;
                          if ( v192 == v190 )
                            goto LABEL_599;
                        }
                        if ( v192 == v190 )
                          v191 = nullptr;
                        else
                          v191 = *(__int64 **)(v192 + 8);
LABEL_599:
                        v193 = &qword_141B5A4A0;
                        if ( v191 != nullptr )
                          v193 = v191;
                        v191 = nullptr;
                        while ( *(_DWORD *)v189 != 1768169504 )
                        {
                          v189 += 16;
                          if ( v189 == v190 )
                            goto LABEL_631;
                        }
                        if ( v189 == v190 )
                          v191 = nullptr;
                        else
                          v191 = *(__int64 **)(v189 + 8);
                      }
LABEL_631:
                      v231 = 32 * v188;
                      if ( v191 != nullptr )
                        j = (__int64)v191;
                      v232 = (*(__int64 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)j + 80LL))(*(_QWORD *)j, j);
                      LODWORD(j) = 0;
                      if ( v232 <= 1668574321 )
                      {
                        if ( v232 == 1667460214 )
                        {
                          *(_BYTE *)(v187 + v231 + 24) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v193 + 64LL))(
                                                           *v193,
                                                           v193);
                        }
                        else
                        {
                          if ( v232 != 1667460464 )
                            return (unsigned int)j;
                          j = qword_141B5FDC0;
                          sub_140FE7960(&v237, v193, 1668246896);
                          *(_QWORD *)(v187 + v231 + 16) = sub_140F7A940(j, &v237);
                        }
                      }
                      else
                      {
                        switch ( v232 )
                        {
                          case 1668574322:
                            j = qword_141B5FE00;
                            sub_140FE7960(&v237, v193, 1818456679);
                            *(_QWORD *)(v187 + v231 + 8) = sub_140FA1860(j, &v237);
                            break;
                          case 1668575091:
                            *(_BYTE *)(v187 + v231 + 25) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v193 + 64LL))(
                                                             *v193,
                                                             v193);
                            break;
                          case 1668574817:
                            j = qword_141B5FDD0;
                            sub_140FE7960(&v237, v193, 1315856756);
                            *(_QWORD *)(v231 + v187) = sub_14002F670(j, &v237);
                            break;
                          default:
                            return (unsigned int)j;
                        }
                      }
                      goto LABEL_325;
                    case 2u:
                      v124 = *v17;
                      v125 = v17[1];
                      v126 = 0;
                      if ( *v17 != v125 )
                      {
                        while ( *(_DWORD *)v124 != 1869379180 )
                        {
                          v124 += 16;
                          if ( v124 == v125 )
                            goto LABEL_509;
                        }
                        if ( v124 == v125 )
                          v126 = 0;
                        else
                          v126 = *(_QWORD *)(v124 + 8);
                      }
LABEL_509:
                      if ( v126 != 0 )
                        j = v126;
                      v194 = sub_141076640(&v241, j);
                      if ( v194 < 0 || *(_QWORD *)(v243[0] + 192LL) == 0 )
                        goto LABEL_669;
                      v195 = v242;
                      v196 = v242[24] + 32LL * (unsigned int)v194;
                      sub_141758A00(v196, v196 + 32, v242[25] - (v196 + 32));
                      v195[25] -= 32LL;
                      goto LABEL_325;
                    case 3u:
                      LOBYTE(j) = 1;
                      v127 = *(_QWORD *)(v243[0] + 200LL) - *(_QWORD *)(v243[0] + 192LL);
                      if ( v127 != 0 )
                      {
                        v128 = v127 >> 5;
                        v129 = (v128 << 32) - 0x100000000LL;
                        do
                        {
                          --v128;
                          if ( *(_QWORD *)(v243[0] + 192LL) != 0 )
                          {
                            v130 = v242;
                            sub_141758A00(
                              v242[24] + (v129 >> 27),
                              v242[24] + (v129 >> 27) + 32,
                              v242[25] - (v242[24] + (v129 >> 27) + 32));
                            v130[25] -= 32LL;
                          }
                          v129 -= 0x100000000LL;
                        }
                        while ( v128 != 0 );
                      }
                      return (unsigned int)j;
                    case 4u:
                      v131 = *v17;
                      v132 = v17[1];
                      v133 = 0;
                      if ( *v17 == v132 )
                        goto LABEL_515;
                      break;
                    case 5u:
LABEL_421:
                      sub_140DD5C90(&v240, 0);
                      goto LABEL_325;
                    default:
                      goto LABEL_669;
                  }
                  while ( *(_DWORD *)v131 != 1869379180 )
                  {
                    v131 += 16;
                    if ( v131 == v132 )
                      goto LABEL_515;
                  }
                  if ( v131 == v132 )
                    v133 = 0;
                  else
                    v133 = *(_QWORD *)(v131 + 8);
LABEL_515:
                  if ( v133 != 0 )
                    j = v133;
                  sub_141076FD0(&v240, j);
                  goto LABEL_325;
                }
                goto LABEL_669;
              }
              return (unsigned int)j;
            }
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD *, __int64 *))(v16 + 8))(v15, v4) != 11 )
              goto LABEL_669;
            v55 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v4 + 184LL))(*v4, v4, 0);
            v56 = *(_QWORD *)(v243[0] + 200LL) - *(_QWORD *)(v243[0] + 192LL);
            if ( v56 != 0 )
            {
              v57 = v56 >> 5;
              j = (v57 << 32) - 0x100000000LL;
              do
              {
                --v57;
                if ( *(_QWORD *)(v243[0] + 192LL) != 0 )
                {
                  v58 = v242;
                  sub_141758A00(v242[24] + (j >> 27), v242[24] + (j >> 27) + 32, v242[25] - (v242[24] + (j >> 27) + 32));
                  v58[25] -= 32LL;
                }
                j -= 0x100000000LL;
              }
              while ( v57 != 0 );
            }
            v80 = v55[1] - *v55;
            if ( v80 != 0 )
            {
              v81 = v80 >> 3;
              j = 1;
              if ( v81 >= 2 )
                j = v81;
              for ( i = 0; i != j; ++i )
              {
                v83 = *(__int64 **)(*v55 + 8 * i);
                if ( v83 == nullptr )
                  v83 = &qword_141B5A4A0;
                sub_141076FD0(&v240, v83);
              }
            }
            v84 = qword_141B60C30;
            if ( qword_141B60C30 != qword_141B60C38 )
            {
              while ( *(_DWORD *)v84 != 1986359923 )
              {
                v84 += 16;
                if ( v84 == qword_141B60C38 )
                  goto LABEL_207;
              }
              if ( v84 != qword_141B60C38 )
              {
                LOBYTE(j) = 1;
                if ( *(_QWORD *)(v84 + 8) != 0 )
                  return (unsigned int)j;
              }
            }
            goto LABEL_207;
          default:
            break;
        }
      }
      else
      {
        if ( (int)a2 <= 1315923557 )
        {
          if ( (_DWORD)a2 == 1315791218 )
          {
            *(_BYTE *)(a1 + 1967) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          }
          if ( (_DWORD)a2 == 1315797345 )
          {
            *(_BYTE *)(a1 + 1956) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          }
          if ( (_DWORD)a2 != 1315861616 )
            goto LABEL_124;
          v242 = (_QWORD *)a1;
          v243[0] = a1;
          v240 = (__int128 *)&v242;
          v241 = (char *)v243;
          v7 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
          v8 = *v4;
          v9 = *(_QWORD *)*v4;
          if ( v7 == 10 )
          {
            LODWORD(j) = 0;
            v10 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(v9 + 176))(v8, v4, 0);
            v11 = *v10;
            v12 = v10[1];
            if ( *v10 != v12 )
            {
              v13 = *v10;
              while ( *(_DWORD *)v13 != 1819504496 )
              {
                v13 += 16;
                if ( v13 == v12 )
                  goto LABEL_669;
              }
              if ( v13 != v12 && *(_QWORD *)(v13 + 8) != 0 )
              {
                v98 = nullptr;
                while ( *(_DWORD *)v11 != 1819504496 )
                {
                  v11 += 16;
                  if ( v11 == v12 )
                    goto LABEL_328;
                }
                if ( v11 == v12 )
                  v98 = nullptr;
                else
                  v98 = *(__int64 **)(v11 + 8);
LABEL_328:
                j = (__int64)&qword_141B5A4A0;
                if ( v98 == nullptr )
                  v98 = &qword_141B5A4A0;
                switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v98 + 64LL))(*v98) )
                {
                  case 0u:
                    v237 = 0x10E2D12u;
                    sub_1408C9770(v242 + 30, &v237);
                    goto LABEL_325;
                  case 1u:
                    v107 = *v10;
                    v108 = v10[1];
                    v109 = nullptr;
                    if ( *v10 != v108 )
                    {
                      while ( *(_DWORD *)v107 != 1869379180 )
                      {
                        v107 += 16;
                        if ( v107 == v108 )
                          goto LABEL_473;
                      }
                      if ( v107 == v108 )
                        v109 = nullptr;
                      else
                        v109 = *(__int64 **)(v107 + 8);
                    }
LABEL_473:
                    if ( v109 == nullptr )
                      v109 = &qword_141B5A4A0;
                    v175 = sub_1410753B0(&v241, v109);
                    if ( v175 < 0 )
                      goto LABEL_669;
                    v176 = *(_QWORD *)(v243[0] + 240LL);
                    if ( v176 == 0 )
                      goto LABEL_669;
                    v177 = 16LL * (unsigned int)v175 + v176;
                    v178 = *v10;
                    v179 = v10[1];
                    v180 = nullptr;
                    if ( *v10 == v179 )
                    {
                      v182 = &qword_141B5A4A0;
                    }
                    else
                    {
                      v181 = *v10;
                      while ( *(_DWORD *)v181 != 1986096245 )
                      {
                        v181 += 16;
                        if ( v181 == v179 )
                          goto LABEL_590;
                      }
                      v180 = v181 == v179 ? nullptr : *(__int64 **)(v181 + 8);
LABEL_590:
                      v182 = &qword_141B5A4A0;
                      if ( v180 != nullptr )
                        v182 = v180;
                      v180 = nullptr;
                      while ( *(_DWORD *)v178 != 1768169504 )
                      {
                        v178 += 16;
                        if ( v178 == v179 )
                          goto LABEL_626;
                      }
                      v180 = v178 == v179 ? nullptr : *(__int64 **)(v178 + 8);
                    }
LABEL_626:
                    if ( v180 != nullptr )
                      j = (__int64)v180;
                    v230 = (*(__int64 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)j + 80LL))(*(_QWORD *)j, j);
                    if ( (unsigned __int8)sub_14141DE20(v177, v230, v182) == 0 )
                      goto LABEL_669;
                    sub_141074440(v242[30], v242[31], (__int64)(v242[31] - v242[30]) >> 4);
                    goto LABEL_325;
                  case 2u:
                    v110 = *v10;
                    v111 = v10[1];
                    v112 = 0;
                    if ( *v10 != v111 )
                    {
                      while ( *(_DWORD *)v110 != 1869379180 )
                      {
                        v110 += 16;
                        if ( v110 == v111 )
                          goto LABEL_486;
                      }
                      if ( v110 == v111 )
                        v112 = 0;
                      else
                        v112 = *(_QWORD *)(v110 + 8);
                    }
LABEL_486:
                    if ( v112 != 0 )
                      j = v112;
                    v183 = sub_1410753B0(&v241, j);
                    if ( v183 < 0 || *(_QWORD *)(v243[0] + 240LL) == 0 )
                      goto LABEL_669;
                    v184 = v242;
                    v185 = v242[30] + 16LL * (unsigned int)v183;
                    sub_141758A00(v185, v185 + 16, v242[31] - (v185 + 16));
                    v184[31] -= 16LL;
                    goto LABEL_325;
                  case 3u:
                    LOBYTE(j) = 1;
                    v113 = *(_QWORD *)(v243[0] + 248LL) - *(_QWORD *)(v243[0] + 240LL);
                    if ( v113 != 0 )
                    {
                      v114 = v113 >> 4;
                      v115 = v113 & 0xFFFFFFFFFFFFFFF0uLL;
                      v116 = -(__int64)v115;
                      do
                      {
                        --v114;
                        if ( *(_QWORD *)(v243[0] + 240LL) != 0 )
                        {
                          v117 = v242;
                          sub_141758A00(v242[30] + v115 - 16, v242[30] + v115, v116 + v242[31] - v242[30]);
                          v117[31] -= 16LL;
                        }
                        v115 -= 16LL;
                        v116 += 16;
                      }
                      while ( v114 != 0 );
                    }
                    return (unsigned int)j;
                  case 4u:
                    v118 = *v10;
                    v119 = v10[1];
                    v120 = 0;
                    if ( *v10 == v119 )
                      goto LABEL_492;
                    break;
                  case 5u:
                    goto LABEL_421;
                  default:
                    goto LABEL_669;
                }
                while ( *(_DWORD *)v118 != 1869379180 )
                {
                  v118 += 16;
                  if ( v118 == v119 )
                    goto LABEL_492;
                }
                if ( v118 == v119 )
                  v120 = 0;
                else
                  v120 = *(_QWORD *)(v118 + 8);
LABEL_492:
                if ( v120 != 0 )
                  j = v120;
                sub_1410758A0(&v240, j);
                goto LABEL_325;
              }
              goto LABEL_669;
            }
            return (unsigned int)j;
          }
          if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(v9 + 8))(v8, v4) != 11 )
            goto LABEL_669;
          v51 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v4 + 184LL))(*v4, v4, 0);
          j = *(_QWORD *)(v243[0] + 248LL) - *(_QWORD *)(v243[0] + 240LL);
          if ( j != 0 )
          {
            v52 = j >> 4;
            j &= 0xFFFFFFFFFFFFFFF0uLL;
            v53 = -j;
            do
            {
              --v52;
              if ( *(_QWORD *)(v243[0] + 240LL) != 0 )
              {
                v54 = v242;
                sub_141758A00(v242[30] + j - 16, v242[30] + j, v53 + v242[31] - v242[30]);
                v54[31] -= 16LL;
              }
              j -= 16;
              v53 += 16;
            }
            while ( v52 != 0 );
          }
          v75 = v51[1] - *v51;
          if ( v75 != 0 )
          {
            v76 = v75 >> 3;
            v77 = 1;
            if ( v76 >= 2 )
              v77 = v76;
            for ( j = 0; j != v77; ++j )
            {
              v78 = *(__int64 **)(*v51 + 8 * j);
              if ( v78 == nullptr )
                v78 = &qword_141B5A4A0;
              sub_1410758A0(&v240, v78);
            }
          }
          v79 = qword_141B60C30;
          if ( qword_141B60C30 != qword_141B60C38 )
          {
            while ( *(_DWORD *)v79 != 1986359923 )
            {
              v79 += 16;
              if ( v79 == qword_141B60C38 )
                goto LABEL_207;
            }
            if ( v79 != qword_141B60C38 )
            {
              LOBYTE(j) = 1;
              if ( *(_QWORD *)(v79 + 8) != 0 )
                return (unsigned int)j;
            }
          }
LABEL_207:
          LOBYTE(j) = 1;
          LOBYTE(v46) = 1;
          sub_140DD5C90(&v240, v46);
          return (unsigned int)j;
        }
        switch ( (_DWORD)a2 )
        {
          case 0x4E6F6666:
            *(_BYTE *)(a1 + 1968) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E707273:
            *(_BYTE *)(a1 + 1969) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E727470:
            v242 = (_QWORD *)a1;
            v243[0] = a1;
            v240 = (__int128 *)&v242;
            v241 = (char *)v243;
            v21 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
            v22 = *v4;
            v23 = *(_QWORD *)*v4;
            if ( v21 == 10 )
            {
              LODWORD(j) = 0;
              v24 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(v23 + 176))(v22, v4, 0);
              v25 = *v24;
              v26 = v24[1];
              if ( *v24 != v26 )
              {
                v27 = *v24;
                while ( *(_DWORD *)v27 != 1819504496 )
                {
                  v27 += 16;
                  if ( v27 == v26 )
                    goto LABEL_669;
                }
                if ( v27 != v26 && *(_QWORD *)(v27 + 8) != 0 )
                {
                  v100 = nullptr;
                  while ( *(_DWORD *)v25 != 1819504496 )
                  {
                    v25 += 16;
                    if ( v25 == v26 )
                      goto LABEL_338;
                  }
                  if ( v25 == v26 )
                    v100 = nullptr;
                  else
                    v100 = *(__int64 **)(v25 + 8);
LABEL_338:
                  j = (__int64)&qword_141B5A4A0;
                  if ( v100 == nullptr )
                    v100 = &qword_141B5A4A0;
                  switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v100 + 64LL))(*v100) )
                  {
                    case 0u:
                      LODWORD(v237) = 17706258;
                      *((_QWORD *)&v237 + 1) = 0;
                      sub_1408C9770(v242 + 36, &v237);
                      goto LABEL_325;
                    case 1u:
                      v134 = *v24;
                      v135 = v24[1];
                      v136 = nullptr;
                      if ( *v24 != v135 )
                      {
                        while ( *(_DWORD *)v134 != 1869379180 )
                        {
                          v134 += 16;
                          if ( v134 == v135 )
                            goto LABEL_519;
                        }
                        if ( v134 == v135 )
                          v136 = nullptr;
                        else
                          v136 = *(__int64 **)(v134 + 8);
                      }
LABEL_519:
                      if ( v136 == nullptr )
                        v136 = &qword_141B5A4A0;
                      v197 = sub_141075FE0(&v241, v136);
                      if ( v197 < 0 )
                        goto LABEL_669;
                      v198 = *(_QWORD *)(v243[0] + 288LL);
                      if ( v198 == 0 )
                        goto LABEL_669;
                      v199 = 16LL * (unsigned int)v197 + v198;
                      v200 = *v24;
                      v201 = v24[1];
                      v202 = nullptr;
                      if ( *v24 == v201 )
                      {
                        v204 = &qword_141B5A4A0;
                      }
                      else
                      {
                        v203 = *v24;
                        while ( *(_DWORD *)v203 != 1986096245 )
                        {
                          v203 += 16;
                          if ( v203 == v201 )
                            goto LABEL_608;
                        }
                        v202 = v203 == v201 ? nullptr : *(__int64 **)(v203 + 8);
LABEL_608:
                        v204 = &qword_141B5A4A0;
                        if ( v202 != nullptr )
                          v204 = v202;
                        v202 = nullptr;
                        while ( *(_DWORD *)v200 != 1768169504 )
                        {
                          v200 += 16;
                          if ( v200 == v201 )
                            goto LABEL_645;
                        }
                        v202 = v200 == v201 ? nullptr : *(__int64 **)(v200 + 8);
                      }
LABEL_645:
                      if ( v202 != nullptr )
                        j = (__int64)v202;
                      v233 = (*(__int64 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)j + 80LL))(*(_QWORD *)j, j);
                      if ( (unsigned __int8)sub_14141DFC0(v199, v233, v204) == 0 )
                        goto LABEL_669;
                      sub_141074440(v242[36], v242[37], (__int64)(v242[37] - v242[36]) >> 4);
                      goto LABEL_325;
                    case 2u:
                      v137 = *v24;
                      v138 = v24[1];
                      v139 = 0;
                      if ( *v24 != v138 )
                      {
                        while ( *(_DWORD *)v137 != 1869379180 )
                        {
                          v137 += 16;
                          if ( v137 == v138 )
                            goto LABEL_532;
                        }
                        if ( v137 == v138 )
                          v139 = 0;
                        else
                          v139 = *(_QWORD *)(v137 + 8);
                      }
LABEL_532:
                      if ( v139 != 0 )
                        j = v139;
                      v205 = sub_141075FE0(&v241, j);
                      if ( v205 < 0 || *(_QWORD *)(v243[0] + 288LL) == 0 )
                        goto LABEL_669;
                      v206 = v242;
                      v207 = v242[36] + 16LL * (unsigned int)v205;
                      sub_141758A00(v207, v207 + 16, v242[37] - (v207 + 16));
                      v206[37] -= 16LL;
                      goto LABEL_325;
                    case 3u:
                      LOBYTE(j) = 1;
                      v140 = *(_QWORD *)(v243[0] + 296LL) - *(_QWORD *)(v243[0] + 288LL);
                      if ( v140 != 0 )
                      {
                        v141 = v140 >> 4;
                        v142 = v140 & 0xFFFFFFFFFFFFFFF0uLL;
                        v143 = -(__int64)v142;
                        do
                        {
                          --v141;
                          if ( *(_QWORD *)(v243[0] + 288LL) != 0 )
                          {
                            v144 = v242;
                            sub_141758A00(v242[36] + v142 - 16, v242[36] + v142, v143 + v242[37] - v242[36]);
                            v144[37] -= 16LL;
                          }
                          v142 -= 16LL;
                          v143 += 16;
                        }
                        while ( v141 != 0 );
                      }
                      return (unsigned int)j;
                    case 4u:
                      v145 = *v24;
                      v146 = v24[1];
                      v147 = 0;
                      if ( *v24 == v146 )
                        goto LABEL_538;
                      break;
                    case 5u:
                      goto LABEL_421;
                    default:
                      goto LABEL_669;
                  }
                  while ( *(_DWORD *)v145 != 1869379180 )
                  {
                    v145 += 16;
                    if ( v145 == v146 )
                      goto LABEL_538;
                  }
                  if ( v145 == v146 )
                    v147 = 0;
                  else
                    v147 = *(_QWORD *)(v145 + 8);
LABEL_538:
                  if ( v147 != 0 )
                    j = v147;
                  sub_141076560(&v240, j);
                  goto LABEL_325;
                }
                goto LABEL_669;
              }
              return (unsigned int)j;
            }
            if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(v23 + 8))(v22, v4) != 11 )
              goto LABEL_669;
            v59 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v4 + 184LL))(*v4, v4, 0);
            j = *(_QWORD *)(v243[0] + 296LL) - *(_QWORD *)(v243[0] + 288LL);
            if ( j != 0 )
            {
              v60 = j >> 4;
              j &= 0xFFFFFFFFFFFFFFF0uLL;
              v61 = -j;
              do
              {
                --v60;
                if ( *(_QWORD *)(v243[0] + 288LL) != 0 )
                {
                  v62 = v242;
                  sub_141758A00(v242[36] + j - 16, v242[36] + j, v61 + v242[37] - v242[36]);
                  v62[37] -= 16LL;
                }
                j -= 16;
                v61 += 16;
              }
              while ( v60 != 0 );
            }
            v85 = v59[1] - *v59;
            if ( v85 != 0 )
            {
              v86 = v85 >> 3;
              v87 = 1;
              if ( v86 >= 2 )
                v87 = v86;
              for ( j = 0; j != v87; ++j )
              {
                v88 = *(__int64 **)(*v59 + 8 * j);
                if ( v88 == nullptr )
                  v88 = &qword_141B5A4A0;
                sub_141076560(&v240, v88);
              }
            }
            v89 = qword_141B60C30;
            if ( qword_141B60C30 != qword_141B60C38 )
            {
              while ( *(_DWORD *)v89 != 1986359923 )
              {
                v89 += 16;
                if ( v89 == qword_141B60C38 )
                  goto LABEL_207;
              }
              if ( v89 != qword_141B60C38 )
              {
                LOBYTE(j) = 1;
                if ( *(_QWORD *)(v89 + 8) != 0 )
                  return (unsigned int)j;
              }
            }
            goto LABEL_207;
          default:
            break;
        }
      }
    }
    else if ( (int)a2 > 1315335276 )
    {
      if ( (int)a2 > 1315336288 )
      {
        switch ( (_DWORD)a2 )
        {
          case 0x4E667061:
            *(_BYTE *)(a1 + 1957) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E66726C:
            *(_BYTE *)(a1 + 1966) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E67696D:
            *(_BYTE *)(a1 + 1949) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          default:
            break;
        }
      }
      else
      {
        switch ( (_DWORD)a2 )
        {
          case 0x4E666C6D:
            *(_BYTE *)(a1 + 1964) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E666C78:
            *(_BYTE *)(a1 + 1965) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          case 0x4E666D6C:
            *(_BYTE *)(a1 + 1958) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_325;
          default:
            break;
        }
      }
    }
    else if ( (int)a2 > 1315332472 )
    {
      switch ( (_DWORD)a2 )
      {
        case 0x4E666179:
          if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
            v5[962] = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v4 + 64LL))(*v4, v4);
          else
            v5[962] = 0;
          goto LABEL_325;
        case 0x4E666479:
          if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
            v5[963] = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v4 + 64LL))(*v4, v4);
          else
            v5[963] = 0;
          goto LABEL_325;
        case 0x4E66666D:
          *(_BYTE *)(a1 + 1951) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
          goto LABEL_325;
        default:
          break;
      }
    }
    else
    {
      switch ( (_DWORD)a2 )
      {
        case 0x4E646570:
          *(_BYTE *)(a1 + 1962) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          goto LABEL_325;
        case 0x4E646972:
          *(_BYTE *)(a1 + 1963) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          goto LABEL_325;
        case 0x4E666170:
          *(_BYTE *)(a1 + 1955) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          goto LABEL_325;
        default:
          break;
      }
    }
LABEL_124:
    if ( (_BYTE)word_141B60320 == 0 )
      return sub_1411F4F70(a1, a2, a3);
    if ( (int)a2 <= 1315335535 )
    {
      if ( (int)a2 > 1315254575 )
      {
        switch ( (int)a2 )
        {
          case 1315271985:
            v43 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v44 = v43;
            v45 = 0;
            goto LABEL_324;
          case 1315271986:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 1;
            goto LABEL_323;
          case 1315271987:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 2;
            goto LABEL_323;
          case 1315271988:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 3;
            goto LABEL_323;
          case 1315271989:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 4;
            goto LABEL_323;
          case 1315271990:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 5;
            goto LABEL_323;
          case 1315271991:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 6;
            goto LABEL_323;
          case 1315271992:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 7;
            goto LABEL_323;
          case 1315271993:
            v105 = a1 + 1056;
            LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v45 = 8;
            goto LABEL_323;
          default:
            if ( (_DWORD)a2 == 1315254576 )
            {
              v105 = a1 + 1056;
              LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
              v45 = 9;
            }
            else
            {
              if ( (_DWORD)a2 != 1315254577 )
                return sub_1411F4F70(a1, a2, a3);
              v105 = a1 + 1056;
              LODWORD(v237) = (*(float (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
              v45 = 10;
            }
LABEL_323:
            v44 = v105;
LABEL_324:
            sub_14086F950(v44, &v237, v45);
            break;
        }
        goto LABEL_325;
      }
      if ( (int)a2 <= 1314342773 )
      {
        if ( (_DWORD)a2 == 1314091123 )
        {
          v103 = a1;
          LOBYTE(a3) = 2;
          goto LABEL_295;
        }
        if ( (_DWORD)a2 == 1314148982 )
        {
          v103 = a1;
          LOBYTE(a3) = 1;
LABEL_295:
          sub_1415D1D00(&v237, v103, a3);
          v240 = &v237;
          v241 = (char *)&v237;
          LODWORD(j) = sub_141078DE0(&v240, v4);
          return (unsigned int)j;
        }
        return sub_1411F4F70(a1, a2, a3);
      }
      if ( (_DWORD)a2 == 1314342774 )
      {
        v103 = a1;
        a3 = nullptr;
        goto LABEL_295;
      }
      if ( (_DWORD)a2 != 1315137641 )
        return sub_1411F4F70(a1, a2, a3);
      if ( (*(_BYTE *)(a1 + 1150) & 2) == 0 || (unsigned __int8)sub_1400015E0() == 0 )
      {
        a1 = (__int64)v5;
        v104 = 1415800937;
        return sub_1411F76F0(a1, 0, v104, v4);
      }
LABEL_669:
      LODWORD(j) = 0;
      return (unsigned int)j;
    }
    if ( (int)a2 > 1315989608 )
    {
      if ( (int)a2 <= 1316124269 )
      {
        if ( (_DWORD)a2 != 1315989609 )
        {
          if ( (_DWORD)a2 == 1316119920 )
          {
            v95 = *(__int64 **)(a1 + 24);
            LOBYTE(j) = 1;
            if ( v95 != *(__int64 **)(a1 + 32) )
            {
              v96 = *v95;
              if ( *v95 != 0 )
              {
                DWORD2(v237) = *(__int16 *)(v96 + 168);
                *(_QWORD *)&v237 = sub_14083D4F0(a1) + 40;
                sub_141405B90((_DWORD)v5, 1099938928, (unsigned int)&v237, (_DWORD)v4, 0);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v237 + 16LL))(v237, &v237);
                v97 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v4 + 64LL))(*v4, v4);
                sub_140FC9D50(v96, v97, 0);
              }
            }
            return (unsigned int)j;
          }
          return sub_1411F4F70(a1, a2, a3);
        }
        if ( (*(_BYTE *)(a1 + 1150) & 2) == 0 || (unsigned __int8)sub_1400015E0() == 0 )
        {
          a1 = (__int64)v5;
          v104 = 1416652905;
          return sub_1411F76F0(a1, 0, v104, v4);
        }
        goto LABEL_669;
      }
      if ( (_DWORD)a2 == 1316124270 )
      {
        sub_1410667A0(&v237, a1);
        v240 = &v237;
        v241 = (char *)&v237 + 8;
        LODWORD(j) = sub_140EAC3E0(&v240, v4);
        if ( *((_QWORD *)&v237 + 1) != 0 )
          sub_1407E4890(qword_141ABD470, *((_QWORD *)&v237 + 1), v239 - *((_QWORD *)&v237 + 1));
        return (unsigned int)j;
      }
      if ( (_DWORD)a2 != 1415800940 )
        return sub_1411F4F70(a1, a2, a3);
      v104 = 1415800940;
      return sub_1411F76F0(a1, 0, v104, v4);
    }
    if ( (_DWORD)a2 == 1315335536 )
    {
      v240 = (__int128 *)a1;
      v241 = (char *)a1;
      *(_QWORD *)&v237 = &v240;
      *((_QWORD *)&v237 + 1) = &v241;
      LODWORD(j) = sub_141077A80(&v237, a3);
      return (unsigned int)j;
    }
    if ( (_DWORD)a2 != 1315336816 )
    {
      if ( (_DWORD)a2 != 1315794537 )
        return sub_1411F4F70(a1, a2, a3);
      if ( (*(_BYTE *)(a1 + 1150) & 2) != 0 && (unsigned __int8)sub_1400015E0() != 0 )
        goto LABEL_669;
      a1 = (__int64)v5;
      v104 = 1416457833;
      return sub_1411F76F0(a1, 0, v104, v4);
    }
    *(_WORD *)(a1 + 562) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
LABEL_325:
    LOBYTE(j) = 1;
    return (unsigned int)j;
  }
  if ( (int)a2 <= 1313686881 )
  {
    if ( (int)a2 > 1313362529 )
    {
      switch ( (int)a2 )
      {
        case 1313362530:
          LOBYTE(a2) = 32;
          v6 = 1869899892;
          return sub_1411E9540(a1, a2, v6, v4);
        case 1313362532:
          LOBYTE(a2) = 32;
          v6 = 1937007732;
          return sub_1411E9540(a1, a2, v6, v4);
        case 1313362534:
          LOBYTE(a2) = 32;
          v6 = 1667330920;
          return sub_1411E9540(a1, a2, v6, v4);
        case 1313362542:
          LOBYTE(a2) = 32;
          v6 = 1937010285;
          return sub_1411E9540(a1, a2, v6, v4);
        case 1313362544:
          LOBYTE(a2) = 32;
          goto LABEL_101;
        case 1313362547:
          LOBYTE(a2) = 32;
          v6 = 1952801133;
          return sub_1411E9540(a1, a2, v6, v4);
        default:
          goto LABEL_124;
      }
    }
    switch ( (int)a2 )
    {
      case 1313362018:
        LOBYTE(a2) = 33;
        v6 = 1869899892;
        return sub_1411E9540(a1, a2, v6, v4);
      case 1313362019:
      case 1313362021:
      case 1313362023:
      case 1313362024:
      case 1313362025:
      case 1313362026:
      case 1313362027:
      case 1313362028:
      case 1313362029:
      case 1313362031:
      case 1313362033:
      case 1313362034:
        goto LABEL_124;
      case 1313362020:
        LOBYTE(a2) = 33;
        v6 = 1937007732;
        return sub_1411E9540(a1, a2, v6, v4);
      case 1313362022:
        LOBYTE(a2) = 33;
        v6 = 1667330920;
        return sub_1411E9540(a1, a2, v6, v4);
      case 1313362030:
        LOBYTE(a2) = 33;
        v6 = 1937010285;
        return sub_1411E9540(a1, a2, v6, v4);
      case 1313362032:
        LOBYTE(a2) = 33;
        goto LABEL_101;
      case 1313362035:
        LOBYTE(a2) = 33;
        v6 = 1952801133;
        return sub_1411E9540(a1, a2, v6, v4);
      default:
        if ( (_DWORD)a2 == 1131572084 )
          return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, 1131572084, a3);
        if ( (_DWORD)a2 != 1313043055 )
          goto LABEL_124;
        v240 = (__int128 *)a1;
        v241 = (char *)a1;
        *(_QWORD *)&v237 = &v240;
        *((_QWORD *)&v237 + 1) = &v241;
        v28 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
        v29 = *v4;
        v30 = *(_QWORD *)*v4;
        if ( v28 == 10 )
        {
          LODWORD(j) = 0;
          v31 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(v30 + 176))(v29, v4, 0);
          v32 = *v31;
          v33 = v31[1];
          if ( *v31 == v33 )
            return (unsigned int)j;
          v34 = *v31;
          while ( *(_DWORD *)v34 != 1819504496 )
          {
            v34 += 16;
            if ( v34 == v33 )
              goto LABEL_669;
          }
          if ( v34 == v33 || *(_QWORD *)(v34 + 8) == 0 )
            goto LABEL_669;
          v102 = nullptr;
          while ( *(_DWORD *)v32 != 1819504496 )
          {
            v32 += 16;
            if ( v32 == v33 )
              goto LABEL_348;
          }
          if ( v32 == v33 )
            v102 = nullptr;
          else
            v102 = *(__int64 **)(v32 + 8);
LABEL_348:
          j = (__int64)&qword_141B5A4A0;
          if ( v102 == nullptr )
            v102 = &qword_141B5A4A0;
          switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v102 + 64LL))(*v102) )
          {
            case 0u:
              LODWORD(j) = 0;
              sub_141062A00(v240, 0, 100);
              v106 = *((_QWORD **)v240 + 159);
              if ( v106 != nullptr )
                LOBYTE(j) = *v106 != 0;
              return (unsigned int)j;
            case 1u:
              v162 = *v31;
              v163 = v31[1];
              v164 = nullptr;
              if ( *v31 != v163 )
              {
                while ( *(_DWORD *)v162 != 1869379180 )
                {
                  v162 += 16;
                  if ( v162 == v163 )
                    goto LABEL_565;
                }
                if ( v162 == v163 )
                  v164 = nullptr;
                else
                  v164 = *(__int64 **)(v162 + 8);
              }
LABEL_565:
              if ( v164 == nullptr )
                v164 = &qword_141B5A4A0;
              v219 = sub_141077170((char *)&v237 + 8, v164);
              if ( v219 < 0 )
                goto LABEL_669;
              v220 = *((__int64 **)v241 + 159);
              if ( v220 == nullptr )
                goto LABEL_669;
              v221 = *v220;
              if ( *v220 == 0 )
                goto LABEL_669;
              v222 = (unsigned int)v219;
              v223 = *v31;
              v224 = v31[1];
              v225 = nullptr;
              if ( *v31 == v224 )
              {
                v229 = &qword_141B5A4A0;
              }
              else
              {
                v226 = *v31;
                while ( *(_DWORD *)v226 != 1986096245 )
                {
                  v226 += 16;
                  if ( v226 == v224 )
                    goto LABEL_655;
                }
                if ( v226 == v224 )
                  v225 = nullptr;
                else
                  v225 = *(__int64 **)(v226 + 8);
LABEL_655:
                v229 = &qword_141B5A4A0;
                if ( v225 != nullptr )
                  v229 = v225;
                v225 = nullptr;
                while ( *(_DWORD *)v223 != 1768169504 )
                {
                  v223 += 16;
                  if ( v223 == v224 )
                    goto LABEL_664;
                }
                if ( v223 == v224 )
                  v225 = nullptr;
                else
                  v225 = *(__int64 **)(v223 + 8);
              }
LABEL_664:
              v235 = 16 * v222;
              if ( v225 != nullptr )
                j = (__int64)v225;
              v236 = (*(__int64 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)j + 80LL))(*(_QWORD *)j, j);
              if ( v236 == 1668441456 )
              {
                *(_DWORD *)(v221 + v235 + 8) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v229 + 64LL))(
                                                 *v229,
                                                 v229);
              }
              else
              {
                if ( v236 != 1668246896 )
                  goto LABEL_669;
                j = qword_141B5FDC0;
                sub_140FE7960(&v242, v229, 1668246896);
                *(_QWORD *)(v235 + v221) = sub_140F7A940(j, &v242);
              }
              goto LABEL_325;
            case 2u:
              v165 = *v31;
              v166 = v31[1];
              v167 = 0;
              if ( *v31 != v166 )
              {
                while ( *(_DWORD *)v165 != 1869379180 )
                {
                  v165 += 16;
                  if ( v165 == v166 )
                    goto LABEL_576;
                }
                if ( v165 == v166 )
                  v167 = 0;
                else
                  v167 = *(_QWORD *)(v165 + 8);
              }
LABEL_576:
              if ( v167 != 0 )
                j = v167;
              v227 = sub_141077170((char *)&v237 + 8, j);
              if ( v227 < 0 )
                goto LABEL_669;
              v228 = *((_QWORD **)v241 + 159);
              if ( v228 == nullptr || *v228 == 0 )
                goto LABEL_669;
              sub_141062BE0(v240, (unsigned int)v227);
              goto LABEL_325;
            case 3u:
              v168 = *((_QWORD **)v241 + 159);
              LOBYTE(j) = 1;
              if ( v168 != nullptr )
              {
                v169 = v168[1] - *v168;
                if ( v169 != 0 )
                {
                  v170 = (v169 >> 4) - 1;
                  do
                  {
                    v171 = *((_QWORD **)v241 + 159);
                    if ( v171 != nullptr && *v171 != 0 )
                      sub_141062BE0(v240, v170);
                    v68 = v170-- != 0;
                  }
                  while ( v68 );
                }
              }
              return (unsigned int)j;
            case 4u:
              v172 = *v31;
              v173 = v31[1];
              v174 = 0;
              if ( *v31 == v173 )
                goto LABEL_583;
              break;
            case 5u:
              sub_140DD5C90(&v237, 0);
              goto LABEL_325;
            default:
              goto LABEL_669;
          }
          while ( *(_DWORD *)v172 != 1869379180 )
          {
            v172 += 16;
            if ( v172 == v173 )
              goto LABEL_583;
          }
          if ( v172 == v173 )
            v174 = 0;
          else
            v174 = *(_QWORD *)(v172 + 8);
LABEL_583:
          if ( v174 != 0 )
            j = v174;
          LODWORD(j) = sub_141077950(&v237, j);
        }
        else
        {
          if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(v30 + 8))(v29, v4) != 11 )
            goto LABEL_669;
          v64 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v4 + 184LL))(*v4, v4, 0);
          v65 = *((_QWORD **)v241 + 159);
          if ( v65 != nullptr )
          {
            v66 = v65[1] - *v65;
            if ( v66 != 0 )
            {
              v67 = (v66 >> 4) - 1;
              do
              {
                v69 = *((_QWORD **)v241 + 159);
                if ( v69 != nullptr && *v69 != 0 )
                  sub_141062BE0(v240, v67);
                v68 = v67-- != 0;
              }
              while ( v68 );
            }
          }
          v90 = v64[1] - *v64;
          if ( v90 != 0 )
          {
            v91 = v90 >> 3;
            j = 1;
            if ( v91 >= 2 )
              j = v91;
            for ( k = 0; k != j; ++k )
            {
              v93 = *(__int64 **)(*v64 + 8 * k);
              if ( v93 == nullptr )
                v93 = &qword_141B5A4A0;
              sub_141077950(&v237, v93);
            }
          }
          v94 = qword_141B60C30;
          if ( qword_141B60C30 == qword_141B60C38 )
            goto LABEL_218;
          while ( *(_DWORD *)v94 != 1986359923 )
          {
            v94 += 16;
            if ( v94 == qword_141B60C38 )
              goto LABEL_218;
          }
          if ( v94 == qword_141B60C38 || (LOBYTE(j) = 1, *(_QWORD *)(v94 + 8) == 0) )
          {
LABEL_218:
            LOBYTE(j) = 1;
            LOBYTE(v63) = 1;
            sub_140DD5C90(&v237, v63);
            return (unsigned int)j;
          }
        }
        break;
    }
    return (unsigned int)j;
  }
  if ( (int)a2 > 1314476659 )
  {
    if ( (int)a2 <= 1315009651 )
    {
      if ( (_DWORD)a2 == 1314476660 )
      {
        DWORD2(v237) = *(__int16 *)(a1 + 1932);
        *(_QWORD *)&v237 = sub_14083D4F0(a1) + 40;
        j = (__int64)&v237;
        sub_141405B90((_DWORD)v5, 1099982729, (unsigned int)&v237, (_DWORD)v4, 0);
        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v237 + 16LL))(v237, &v237);
        v5[966] = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v4 + 64LL))(*v4, v4);
        goto LABEL_325;
      }
      if ( (_DWORD)a2 == 1315006073 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          v5[964] = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v4 + 64LL))(*v4, v4);
        else
          v5[964] = 0;
        goto LABEL_325;
      }
      goto LABEL_124;
    }
    if ( (_DWORD)a2 == 1315009652 )
    {
      *(_BYTE *)(a1 + 1961) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_325;
    }
    if ( (_DWORD)a2 == 1315140720 )
    {
      v242 = (_QWORD *)a1;
      v243[0] = a1;
      v240 = (__int128 *)&v242;
      v241 = (char *)v243;
      v35 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
      v36 = *v4;
      v37 = *(_QWORD *)*v4;
      if ( v35 == 10 )
      {
        LODWORD(j) = 0;
        v38 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(v37 + 176))(v36, v4, 0);
        v39 = *v38;
        v40 = v38[1];
        if ( *v38 != v40 )
        {
          v41 = *v38;
          while ( *(_DWORD *)v41 != 1819504496 )
          {
            v41 += 16;
            if ( v41 == v40 )
              goto LABEL_669;
          }
          if ( v41 != v40 && *(_QWORD *)(v41 + 8) != 0 )
          {
            v101 = nullptr;
            while ( *(_DWORD *)v39 != 1819504496 )
            {
              v39 += 16;
              if ( v39 == v40 )
                goto LABEL_343;
            }
            if ( v39 == v40 )
              v101 = nullptr;
            else
              v101 = *(__int64 **)(v39 + 8);
LABEL_343:
            j = (__int64)&qword_141B5A4A0;
            if ( v101 == nullptr )
              v101 = &qword_141B5A4A0;
            switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v101 + 64LL))(*v101) )
            {
              case 0u:
                LODWORD(v237) = 17706258;
                *((_QWORD *)&v237 + 1) = 0;
                sub_1408C9770(v242 + 33, &v237);
                goto LABEL_325;
              case 1u:
                v148 = *v38;
                v149 = v38[1];
                v150 = nullptr;
                if ( *v38 != v149 )
                {
                  while ( *(_DWORD *)v148 != 1869379180 )
                  {
                    v148 += 16;
                    if ( v148 == v149 )
                      goto LABEL_542;
                  }
                  if ( v148 == v149 )
                    v150 = nullptr;
                  else
                    v150 = *(__int64 **)(v148 + 8);
                }
LABEL_542:
                if ( v150 == nullptr )
                  v150 = &qword_141B5A4A0;
                v208 = sub_141075980(&v241, v150);
                if ( v208 < 0 )
                  goto LABEL_669;
                v209 = *(_QWORD *)(v243[0] + 264LL);
                if ( v209 == 0 )
                  goto LABEL_669;
                v210 = 16LL * (unsigned int)v208 + v209;
                v211 = *v38;
                v212 = v38[1];
                v213 = nullptr;
                if ( *v38 == v212 )
                {
                  v215 = &qword_141B5A4A0;
                }
                else
                {
                  v214 = *v38;
                  while ( *(_DWORD *)v214 != 1986096245 )
                  {
                    v214 += 16;
                    if ( v214 == v212 )
                      goto LABEL_617;
                  }
                  v213 = v214 == v212 ? nullptr : *(__int64 **)(v214 + 8);
LABEL_617:
                  v215 = &qword_141B5A4A0;
                  if ( v213 != nullptr )
                    v215 = v213;
                  v213 = nullptr;
                  while ( *(_DWORD *)v211 != 1768169504 )
                  {
                    v211 += 16;
                    if ( v211 == v212 )
                      goto LABEL_650;
                  }
                  v213 = v211 == v212 ? nullptr : *(__int64 **)(v211 + 8);
                }
LABEL_650:
                if ( v213 != nullptr )
                  j = (__int64)v213;
                v234 = (*(__int64 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)j + 80LL))(*(_QWORD *)j, j);
                if ( (unsigned __int8)sub_14141DF00(v210, v234, v215) == 0 )
                  goto LABEL_669;
                sub_141074440(v242[33], v242[34], (__int64)(v242[34] - v242[33]) >> 4);
                goto LABEL_325;
              case 2u:
                v151 = *v38;
                v152 = v38[1];
                v153 = 0;
                if ( *v38 != v152 )
                {
                  while ( *(_DWORD *)v151 != 1869379180 )
                  {
                    v151 += 16;
                    if ( v151 == v152 )
                      goto LABEL_555;
                  }
                  if ( v151 == v152 )
                    v153 = 0;
                  else
                    v153 = *(_QWORD *)(v151 + 8);
                }
LABEL_555:
                if ( v153 != 0 )
                  j = v153;
                v216 = sub_141075980(&v241, j);
                if ( v216 < 0 || *(_QWORD *)(v243[0] + 264LL) == 0 )
                  goto LABEL_669;
                v217 = v242;
                v218 = v242[33] + 16LL * (unsigned int)v216;
                sub_141758A00(v218, v218 + 16, v242[34] - (v218 + 16));
                v217[34] -= 16LL;
                goto LABEL_325;
              case 3u:
                LOBYTE(j) = 1;
                v154 = *(_QWORD *)(v243[0] + 272LL) - *(_QWORD *)(v243[0] + 264LL);
                if ( v154 != 0 )
                {
                  v155 = v154 >> 4;
                  v156 = v154 & 0xFFFFFFFFFFFFFFF0uLL;
                  v157 = -(__int64)v156;
                  do
                  {
                    --v155;
                    if ( *(_QWORD *)(v243[0] + 264LL) != 0 )
                    {
                      v158 = v242;
                      sub_141758A00(v242[33] + v156 - 16, v242[33] + v156, v157 + v242[34] - v242[33]);
                      v158[34] -= 16LL;
                    }
                    v156 -= 16LL;
                    v157 += 16;
                  }
                  while ( v155 != 0 );
                }
                return (unsigned int)j;
              case 4u:
                v159 = *v38;
                v160 = v38[1];
                v161 = 0;
                if ( *v38 == v160 )
                  goto LABEL_561;
                break;
              case 5u:
                goto LABEL_421;
              default:
                goto LABEL_669;
            }
            while ( *(_DWORD *)v159 != 1869379180 )
            {
              v159 += 16;
              if ( v159 == v160 )
                goto LABEL_561;
            }
            if ( v159 == v160 )
              v161 = 0;
            else
              v161 = *(_QWORD *)(v159 + 8);
LABEL_561:
            if ( v161 != 0 )
              j = v161;
            sub_141075F00(&v240, j);
            goto LABEL_325;
          }
          goto LABEL_669;
        }
        return (unsigned int)j;
      }
      if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(v37 + 8))(v36, v4) != 11 )
        goto LABEL_669;
      v47 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v4 + 184LL))(*v4, v4, 0);
      j = *(_QWORD *)(v243[0] + 272LL) - *(_QWORD *)(v243[0] + 264LL);
      if ( j != 0 )
      {
        v48 = j >> 4;
        j &= 0xFFFFFFFFFFFFFFF0uLL;
        v49 = -j;
        do
        {
          --v48;
          if ( *(_QWORD *)(v243[0] + 264LL) != 0 )
          {
            v50 = v242;
            sub_141758A00(v242[33] + j - 16, v242[33] + j, v49 + v242[34] - v242[33]);
            v50[34] -= 16LL;
          }
          j -= 16;
          v49 += 16;
        }
        while ( v48 != 0 );
      }
      v70 = v47[1] - *v47;
      if ( v70 != 0 )
      {
        v71 = v70 >> 3;
        v72 = 1;
        if ( v71 >= 2 )
          v72 = v71;
        for ( j = 0; j != v72; ++j )
        {
          v73 = *(__int64 **)(*v47 + 8 * j);
          if ( v73 == nullptr )
            v73 = &qword_141B5A4A0;
          sub_141075F00(&v240, v73);
        }
      }
      v74 = qword_141B60C30;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v74 != 1986359923 )
        {
          v74 += 16;
          if ( v74 == qword_141B60C38 )
            goto LABEL_207;
        }
        if ( v74 != qword_141B60C38 )
        {
          LOBYTE(j) = 1;
          if ( *(_QWORD *)(v74 + 8) != 0 )
            return (unsigned int)j;
        }
      }
      goto LABEL_207;
    }
    goto LABEL_124;
  }
  switch ( (int)a2 )
  {
    case 1313686882:
      LOBYTE(a2) = 31;
      v6 = 1869899892;
      break;
    case 1313686884:
      LOBYTE(a2) = 31;
      v6 = 1937007732;
      break;
    case 1313686886:
      LOBYTE(a2) = 31;
      v6 = 1667330920;
      break;
    case 1313686894:
      LOBYTE(a2) = 31;
      v6 = 1937010285;
      break;
    case 1313686896:
      LOBYTE(a2) = 31;
LABEL_101:
      v6 = 1937008996;
      break;
    case 1313686899:
      LOBYTE(a2) = 31;
      v6 = 1952801133;
      break;
    default:
      goto LABEL_124;
  }
  return sub_1411E9540(a1, a2, v6, v4);
}
