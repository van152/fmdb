__int64 __fastcall sub_140E834A0(__int64 a1, int a2, _QWORD *a3)
{
  __int64 **v3; // rsi
  __int64 v7; // rdx
  __int64 v8; // rcx
  __int64 v9; // r8
  __int64 v10; // rdx
  __int64 v11; // rcx
  __int64 v12; // r8
  int v13; // ecx
  __int64 v14; // rcx
  __int64 v15; // r8
  _QWORD *v16; // rax
  __int64 v17; // rcx
  __int64 v18; // r8
  int v19; // ecx
  __int64 v20; // rax
  __int64 v21; // r15
  __int64 v22; // rax
  __int64 **v23; // rcx
  __int64 v24; // rdx
  int v25; // ecx
  char v27; // al
  int v28; // ecx
  unsigned int v29; // ecx
  __int64 v30; // rax
  char v31; // al
  __int64 v32; // rcx
  char v33; // al
  int v34; // ecx
  char v35; // al
  int v36; // ecx
  __int64 v37; // rdi
  _QWORD *v38; // rax
  __int64 v39; // rcx
  __int64 v40; // r8
  __int64 *v41; // rax
  __int64 v42; // rcx
  int v43; // eax
  int v44; // edx
  __int64 v45; // rdx
  __int64 *v46; // rcx
  char v47; // al
  _DWORD *v48; // rax
  __int64 v49; // rcx
  int v50; // eax
  char v51; // al
  int v52; // ecx
  __int64 **v53; // rax
  __int64 v54; // rax
  __int64 v55; // rdx
  unsigned int v56; // eax
  __int64 v57; // rdx
  __int64 v58; // rax
  __int64 v59; // rdx
  __int64 v60; // rdi
  __int64 v61; // rax
  __int64 v62; // rax
  __int64 v63; // rbx
  __int64 v64; // rcx
  __int64 v65; // r15
  __int64 v66; // r9
  __int64 v67; // r8
  unsigned __int64 v68; // rdx
  __int64 v69; // rbx
  __int64 v70; // rcx
  __int64 v71; // rcx
  __int64 *v72; // rax
  __int64 v73; // rax
  bool v74; // zf
  __int64 v75; // rdx
  char v76; // al
  int v77; // ecx
  __int64 v78; // rdx
  __int64 *v79; // rcx
  char v80; // al
  _DWORD *v81; // rax
  _QWORD *v82; // rax
  __int64 v83; // rdx
  __int64 v84; // rdx
  __int64 *v85; // rcx
  __int64 v86; // rdx
  __int64 *v87; // rcx
  __int64 v88; // rdx
  __int64 *v89; // rcx
  __int64 v90; // r14
  __int64 v91; // rbx
  __int64 v92; // rax
  __int64 v93; // rax
  __int64 *v94; // rax
  __int64 v95; // rax
  __int64 v96; // rax
  __int64 *v97; // rcx
  __int64 *v98; // rdx
  __int64 v99; // rax
  __int64 v100; // rax
  __int64 v101; // rcx
  __int64 v102; // rax
  __int64 v103; // rcx
  __int64 v104; // rsi
  unsigned __int64 v105; // rsi
  __int64 v106; // rax
  __int64 v107; // rcx
  __int64 v108; // rax
  __int64 v109; // rcx
  __int64 v110; // rax
  __int64 v111; // rcx
  __int64 v112; // rax
  __int64 v113; // rax
  unsigned int v114; // eax
  __int64 v115; // rsi
  __int64 v116; // rsi
  __int64 *v117; // rax
  __int64 v118; // rbx
  unsigned int v119; // eax
  __int64 v120; // rax
  char v121; // bl
  unsigned int v122; // eax
  __int64 v123; // rax
  _QWORD *v124; // rax
  __int64 v125; // rax
  __int64 v126; // rax
  __int64 v127; // rbx
  __int64 v128; // rax
  __int64 v129; // rbx
  __int64 v130; // rcx
  __int64 v131; // rcx
  __int64 *v132; // rax
  __int64 v133; // rax
  __int64 v134; // rcx
  __int64 v135; // rax
  int v136; // esi
  __int64 v137; // rcx
  __int64 v138; // rax
  __int64 v139; // rcx
  __int64 v140; // rax
  int v141; // edi
  __int64 v142; // rcx
  __int64 v143; // rax
  __int64 v144; // rcx
  __int64 v145; // rax
  __int64 v146; // rcx
  __int64 v147; // r8
  __int64 *v148; // rcx
  __int64 v149; // rcx
  __int64 v150; // rax
  __int64 v151; // rdi
  __int64 v152; // rax
  __int64 v153; // rdx
  __int64 v154; // rax
  __int64 v155; // rax
  __int64 v156; // rax
  __int64 v157; // rax
  __int64 v158; // rax
  __int64 v159; // rax
  __int64 v160; // rax
  __int64 v161; // rax
  __int64 v162; // rcx
  __int64 v163; // rax
  int v164; // esi
  __int64 v165; // rcx
  __int64 v166; // rax
  __int64 v167; // rcx
  __int64 v168; // rax
  int v169; // edi
  __int64 v170; // rcx
  __int64 v171; // rax
  __int64 *v172; // rax
  __int64 v173; // rcx
  __int64 v174; // rsi
  __int64 v175; // rax
  __int64 v176; // r8
  __int64 v177; // rcx
  __int64 v178; // rax
  __int64 v179; // rax
  int v180; // r9d
  __int64 v181; // rcx
  __int64 v182; // rcx
  __int64 v183; // rsi
  __int64 v184; // rsi
  __int64 v185; // rax
  __int64 v186; // rcx
  __int64 v187; // rax
  __int64 v188; // rcx
  __int64 v189; // rax
  __int64 v190; // rcx
  __int64 v191; // rax
  __int64 v192; // rax
  unsigned int v193; // eax
  __int64 v194; // rsi
  __int64 v195; // rsi
  __int64 v196; // rax
  int v197; // r9d
  __int64 v198; // [rsp+60h] [rbp-20h] BYREF
  __int64 v199; // [rsp+68h] [rbp-18h]
  __int64 *v200; // [rsp+70h] [rbp-10h] BYREF
  _QWORD *v201; // [rsp+78h] [rbp-8h] BYREF
  __int64 v202; // [rsp+80h] [rbp+0h]
  __int64 v203; // [rsp+88h] [rbp+8h]
  bool v204; // [rsp+90h] [rbp+10h] BYREF
  __int64 v205; // [rsp+A8h] [rbp+28h] BYREF
  _QWORD v206[8]; // [rsp+B0h] [rbp+30h] BYREF

  v206[2] = -2;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5EDE8 + 32LL))(qword_141B5EDE8) == 0 )
  {
    LOBYTE(v3) = 1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64, _QWORD, _QWORD *))(*(_QWORD *)qword_141B5EDE8 + 280LL))(
           qword_141B5EDE8,
           a1,
           (unsigned int)a2,
           a3) != 0 )
      return (unsigned int)v3;
  }
  if ( a2 <= 1130588768 )
  {
    if ( a2 > 1127511405 )
    {
      if ( a2 > 1129136495 )
      {
        if ( a2 > 1129542258 )
        {
          if ( a2 > 1130524264 )
          {
            if ( a2 <= 1130587232 )
            {
              if ( a2 > 1130586957 )
              {
                if ( a2 == 1130586958 )
                {
                  sub_140E834A0(a1, 1413704814, a3);
                  sub_140E834A0(a1, 1413706606, a3);
                  *(_BYTE *)(a1 + 354) |= 1u;
                  if ( *(_QWORD *)(a1 + 256) != 0 )
                  {
                    (*(void (__fastcall **)(_QWORD, __int64 **, _QWORD *))(*(_QWORD *)*a3 + 128LL))(*a3, &v200, a3);
                    sub_140809170(*(_QWORD *)(a1 + 256), &v200);
                    v85 = v200;
                    if ( v200 != nullptr && _InterlockedDecrement((volatile signed __int32 *)v200 - 1) == 0 )
                      sub_1412EC9A0((char *)v85 - 4, v84);
                    v3 = *(__int64 ***)(a1 + 256);
                    if ( (int)sub_14080B450(v3) >= 7 )
                    {
                      sub_14080C2A0(v3, &v200, 6);
                      sub_140809170(*(_QWORD *)(a1 + 256), &v200);
                      v87 = v200;
                      if ( v200 != nullptr && _InterlockedDecrement((volatile signed __int32 *)v200 - 1) == 0 )
                        sub_1412EC9A0((char *)v87 - 4, v86);
                    }
                  }
                  LOBYTE(v3) = 1;
                  if ( *(_QWORD *)(a1 + 176) != 0 )
                  {
                    (*(void (__fastcall **)(_QWORD, __int64 **, _QWORD *))(*(_QWORD *)*a3 + 128LL))(*a3, &v200, a3);
                    sub_140809170(*(_QWORD *)(a1 + 176) + 152LL, &v200);
                    v89 = v200;
                    if ( v200 != nullptr && _InterlockedDecrement((volatile signed __int32 *)v200 - 1) == 0 )
                      sub_1412EC9A0((char *)v89 - 4, v88);
                    v90 = *(_QWORD *)(a1 + 256);
                    if ( v90 != 0 )
                    {
                      v91 = *(_QWORD *)(a1 + 176) + 152LL;
                      if ( (int)sub_14080B450(v91) >= 7 )
                        sub_140809100(v91, v90);
                    }
                  }
                  return (unsigned int)v3;
                }
                if ( a2 != 1130586990 )
                  return sub_1411F4F70(a1, (unsigned int)a2, a3);
                v37 = a1 + 240;
              }
              else
              {
                if ( a2 != 1130524265 )
                {
                  if ( a2 != 1130586721 )
                    return sub_1411F4F70(a1, (unsigned int)a2, a3);
                  goto LABEL_419;
                }
                v37 = a1 + 232;
              }
              sub_140FE7D20(v37, a3);
              goto LABEL_788;
            }
            if ( a2 <= 1130587716 )
            {
              if ( a2 != 1130587233 && a2 != 1130587250 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
            }
            if ( a2 == 1130587717 )
            {
              if ( *(_QWORD *)(a1 + 256) != 0 )
              {
                LOBYTE(v3) = 1;
                LOBYTE(v7) = 1;
                if ( sub_140E65F60(a1, v7) != 0 )
                {
                  LOBYTE(v59) = 1;
                  v60 = sub_140E65F60(a1, v59);
                  *(_BYTE *)(v60 + 96) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
                  return (unsigned int)v3;
                }
                goto LABEL_830;
              }
              v57 = 1130587717;
              goto LABEL_503;
            }
            if ( a2 == 1130587745 )
            {
              v64 = *(_QWORD *)(a1 + 336);
              LOBYTE(v3) = 1;
              if ( v64 != 0 && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v64 + 56LL))(v64) == 1 )
                *(_BYTE *)(*(_QWORD *)(a1 + 336) + 2229LL) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(
                                                               *a3,
                                                               a3);
              return (unsigned int)v3;
            }
            if ( a2 != 1130588265 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v11 = a1;
            v7 = 0;
            v12 = 1415800937;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 > 1130458222 )
          {
            if ( a2 > 1130460015 )
            {
              if ( a2 != 1130460016 )
              {
                if ( a2 != 1130521196 )
                  return sub_1411F4F70(a1, (unsigned int)a2, a3);
                return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
              }
              goto LABEL_419;
            }
            if ( a2 != 1130458223 )
            {
              if ( a2 != 1130458467 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
            }
            v200 = (__int64 *)a1;
            v75 = a1;
            v9 = 0;
            goto LABEL_581;
          }
          if ( a2 > 1130456172 )
          {
            if ( a2 != 1130456173 )
            {
              if ( a2 != 1130456684 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              v200 = (__int64 *)a1;
              sub_141532AB0(&v201, a1, 0);
              v205 = (__int64)&v200;
              v206[0] = &v201;
              LODWORD(v3) = sub_140EAE7F0(&v205, a3);
              sub_140E87AD0(&v200);
              return (unsigned int)v3;
            }
            goto LABEL_419;
          }
          if ( a2 != 1129542259 )
          {
            if ( a2 != 1130443630 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
          }
          if ( *(_BYTE *)(qword_141B601A0 + 89) != 0 )
          {
            v200 = (__int64 *)a1;
            sub_14152B240(&v201, a1);
            v205 = (__int64)&v200;
            v206[0] = &v201;
            v50 = sub_140EAA7D0(&v205, a3);
            goto LABEL_651;
          }
          sub_1407C9510(&v200);
          v163 = sub_14083D4F0(v162);
          LODWORD(v206[0]) = 3;
          v205 = v163 + 40;
          sub_140835380(&v200, 1685353593, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          v164 = *(_DWORD *)(a1 + 12);
          v166 = sub_14083D4F0(v165);
          LODWORD(v206[0]) = v164;
          v205 = v166 + 40;
          sub_140835380(&v200, 1685417577, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          v168 = sub_14083D4F0(v167);
          LODWORD(v206[0]) = 1129542259;
          v205 = v168 + 56;
          sub_140835380(&v200, 1886549113, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          sub_1408351C0(&v200, 1853322860, a3);
          v169 = sub_140FE3DB0();
          v171 = sub_14083D4F0(v170);
          LODWORD(v206[0]) = v169;
          v205 = v171 + 40;
          sub_140835380(&v200, 1986359923, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          v144 = qword_141B601A0;
LABEL_799:
          v3 = &v200;
          sub_140FFACE0(v144, &v200);
          sub_140833970(&v200);
          goto LABEL_788;
        }
        if ( a2 > 1129140077 )
        {
          if ( a2 > 1129215087 )
          {
            if ( a2 <= 1129345867 )
            {
              if ( a2 == 1129215088 )
              {
                if ( (_BYTE)word_141B60320 != 0 )
                {
                  v205 = a1;
                  v206[0] = a1;
                  v200 = &v205;
                  v201 = v206;
                  LODWORD(v3) = sub_140EA6E20(&v200, a3);
                  return (unsigned int)v3;
                }
                goto LABEL_830;
              }
              if ( a2 != 1129263982 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
            }
            else
            {
              if ( a2 == 1129345868 )
              {
                v205 = a1;
                v206[0] = a1;
                v200 = &v205;
                v201 = v206;
                LODWORD(v3) = sub_140EACD60(&v200, a3);
                return (unsigned int)v3;
              }
              if ( a2 == 1129538130 )
              {
                v120 = sub_140E741E0(a1);
                if ( v120 != 0 )
                  return sub_14100C380(v120 + 1104, 1213424242, a3);
                goto LABEL_830;
              }
              if ( a2 != 1129538384 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
            }
            return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
          }
          if ( a2 > 1129142084 )
          {
            if ( a2 != 1129142085 )
            {
              if ( a2 != 1129214821 || (_BYTE)word_141B60320 == 0 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              v205 = a1;
              v206[0] = a1;
              v200 = &v205;
              v201 = v206;
              LODWORD(v3) = sub_140EA7ED0(&v200, a3);
              return (unsigned int)v3;
            }
            goto LABEL_497;
          }
          if ( a2 == 1129140078 )
          {
            v14 = a1;
            LOBYTE(v7) = 22;
            v15 = 1937010285;
          }
          else
          {
            if ( a2 != 1129140080 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v14 = a1;
            LOBYTE(v7) = 22;
            v15 = 1937008996;
          }
        }
        else if ( a2 > 1129138022 )
        {
          if ( a2 > 1129138031 )
          {
            if ( a2 == 1129138032 )
            {
              v14 = a1;
              LOBYTE(v7) = 2;
              v15 = 1937008996;
            }
            else
            {
              if ( a2 != 1129140071 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              v14 = a1;
              LOBYTE(v7) = 22;
              v15 = 1735355507;
            }
          }
          else if ( a2 == 1129138023 )
          {
            v14 = a1;
            LOBYTE(v7) = 2;
            v15 = 1735355507;
          }
          else
          {
            if ( a2 != 1129138030 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v14 = a1;
            LOBYTE(v7) = 2;
            v15 = 1937010285;
          }
        }
        else
        {
          switch ( a2 )
          {
            case 1129136996:
              v14 = a1;
              LOBYTE(v7) = 34;
              v15 = 1937007732;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1129136997:
            case 1129136998:
            case 1129136999:
            case 1129137000:
            case 1129137001:
            case 1129137002:
            case 1129137003:
            case 1129137004:
            case 1129137005:
            case 1129137007:
            case 1129137009:
            case 1129137010:
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            case 1129137006:
              v14 = a1;
              LOBYTE(v7) = 34;
              v15 = 1937010285;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1129137008:
              v14 = a1;
              LOBYTE(v7) = 34;
              v15 = 1937008996;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1129137011:
              v14 = a1;
              LOBYTE(v7) = 34;
              v15 = 1734438259;
              return sub_1411E9540(v14, v7, v15, a3);
            default:
              if ( a2 != 1129136496 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              v14 = a1;
              LOBYTE(v7) = 1;
              v15 = 1937008996;
              break;
          }
        }
      }
      else if ( a2 > 1128810338 )
      {
        if ( a2 <= 1128813153 )
        {
          switch ( a2 )
          {
            case 1128811617:
              v14 = a1;
              LOBYTE(v7) = 30;
              v15 = 1869048947;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128811618:
            case 1128811621:
            case 1128811623:
            case 1128811624:
            case 1128811625:
            case 1128811626:
            case 1128811627:
            case 1128811628:
            case 1128811629:
            case 1128811630:
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            case 1128811619:
              v14 = a1;
              LOBYTE(v7) = 30;
              v15 = 1668246896;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128811620:
              v14 = a1;
              LOBYTE(v7) = 30;
              v15 = 1937007732;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128811622:
              v14 = a1;
              LOBYTE(v7) = 30;
              v15 = 1735355507;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128811631:
              v14 = a1;
              LOBYTE(v7) = 30;
              goto LABEL_715;
            default:
              switch ( a2 )
              {
                case 1128810339:
                  v14 = a1;
                  LOBYTE(v7) = 20;
                  v15 = 1668246896;
                  return sub_1411E9540(v14, v7, v15, a3);
                case 1128810343:
                  v14 = a1;
                  LOBYTE(v7) = 20;
                  v15 = 1735355507;
                  return sub_1411E9540(v14, v7, v15, a3);
                case 1128810350:
                  v14 = a1;
                  LOBYTE(v7) = 20;
                  v15 = 1937010285;
                  return sub_1411E9540(v14, v7, v15, a3);
                case 1128810352:
                  v14 = a1;
                  LOBYTE(v7) = 20;
                  v15 = 1937008996;
                  return sub_1411E9540(v14, v7, v15, a3);
                default:
                  return sub_1411F4F70(a1, (unsigned int)a2, a3);
              }
          }
        }
        if ( a2 <= 1128883051 )
        {
          switch ( a2 )
          {
            case 1128813154:
              v14 = a1;
              LOBYTE(v7) = 6;
LABEL_715:
              v15 = 1869899892;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128813156:
              v14 = a1;
              LOBYTE(v7) = 6;
              v15 = 1937007732;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128813158:
              v14 = a1;
              LOBYTE(v7) = 6;
              v15 = 1667330920;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128813166:
              v14 = a1;
              LOBYTE(v7) = 6;
              v15 = 1937010285;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128813168:
              v14 = a1;
              LOBYTE(v7) = 6;
              v15 = 1937008996;
              return sub_1411E9540(v14, v7, v15, a3);
            default:
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
          }
        }
        if ( a2 <= 1129136480 )
        {
          if ( a2 != 1128883052 )
          {
            if ( a2 != 1128885875 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v33 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
            v34 = *(_DWORD *)(a1 + 352);
            if ( v33 != 0 )
              v29 = v34 | 0x400;
            else
              v29 = v34 & 0xFFFFFBFF;
            goto LABEL_787;
          }
LABEL_459:
          if ( *(_BYTE *)(qword_141B60190 + 89) != 0 )
          {
            LOBYTE(v9) = a2 == 1128883052;
            v200 = (__int64 *)a1;
            sub_141532480(&v201, a1, v9);
            v204 = a2 == 1128883052;
            v205 = (__int64)&v200;
            v206[0] = &v201;
            v50 = sub_140EADC50(&v205, a3);
            goto LABEL_651;
          }
          sub_1407C9510(&v200);
          v135 = sub_14083D4F0(v134);
          LODWORD(v206[0]) = 3;
          v205 = v135 + 40;
          sub_140835380(&v200, 1685353593, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          v136 = *(_DWORD *)(a1 + 12);
          v138 = sub_14083D4F0(v137);
          LODWORD(v206[0]) = v136;
          v205 = v138 + 40;
          sub_140835380(&v200, 1685417577, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          v140 = sub_14083D4F0(v139);
          LODWORD(v206[0]) = a2;
          v205 = v140 + 56;
          sub_140835380(&v200, 1886549113, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          sub_1408351C0(&v200, 1853322860, a3);
          v141 = sub_140FE3DB0();
          v143 = sub_14083D4F0(v142);
          LODWORD(v206[0]) = v141;
          v205 = v143 + 40;
          sub_140835380(&v200, 1986359923, &v205);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
          v144 = qword_141B60190;
          goto LABEL_799;
        }
        if ( a2 == 1129136481 )
        {
          v14 = a1;
          LOBYTE(v7) = 1;
          v15 = 1634758771;
        }
        else
        {
          if ( a2 != 1129136494 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v14 = a1;
          LOBYTE(v7) = 1;
          v15 = 1937010285;
        }
      }
      else
      {
        if ( a2 > 1128481378 )
        {
          switch ( a2 )
          {
            case 1128746083:
              v14 = a1;
              LOBYTE(v7) = 21;
              v15 = 1668246896;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128746084:
              v14 = a1;
              LOBYTE(v7) = 21;
              v15 = 1937007732;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128746085:
            case 1128746086:
            case 1128746088:
            case 1128746089:
            case 1128746090:
            case 1128746091:
            case 1128746092:
            case 1128746093:
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            case 1128746087:
              v14 = a1;
              LOBYTE(v7) = 21;
              v15 = 1735355507;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128746094:
              v14 = a1;
              LOBYTE(v7) = 21;
              v15 = 1937010285;
              return sub_1411E9540(v14, v7, v15, a3);
            case 1128746095:
              v14 = a1;
              LOBYTE(v7) = 21;
              goto LABEL_715;
            case 1128746096:
              v14 = a1;
              LOBYTE(v7) = 21;
              v15 = 1937008996;
              return sub_1411E9540(v14, v7, v15, a3);
            default:
              switch ( a2 )
              {
                case 1128810084:
                  v14 = a1;
                  LOBYTE(v7) = 5;
                  v15 = 1937007732;
                  return sub_1411E9540(v14, v7, v15, a3);
                case 1128810085:
                case 1128810087:
                case 1128810088:
                case 1128810089:
                case 1128810090:
                case 1128810091:
                case 1128810092:
                case 1128810093:
                case 1128810095:
                case 1128810097:
                case 1128810098:
                  return sub_1411F4F70(a1, (unsigned int)a2, a3);
                case 1128810086:
                  v14 = a1;
                  LOBYTE(v7) = 5;
                  v15 = 1667330920;
                  return sub_1411E9540(v14, v7, v15, a3);
                case 1128810094:
                  v14 = a1;
                  LOBYTE(v7) = 5;
                  v15 = 1937010285;
                  return sub_1411E9540(v14, v7, v15, a3);
                case 1128810096:
                  v14 = a1;
                  LOBYTE(v7) = 5;
                  v15 = 1937008996;
                  return sub_1411E9540(v14, v7, v15, a3);
                case 1128810099:
                  v14 = a1;
                  LOBYTE(v7) = 5;
                  goto LABEL_715;
                default:
                  if ( a2 != 1128481379 )
                    return sub_1411F4F70(a1, (unsigned int)a2, a3);
                  return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
              }
          }
        }
        if ( a2 > 1128350051 )
        {
          if ( a2 != 1128350052 )
          {
            if ( a2 != 1128354676 )
            {
              if ( a2 != 1128361314 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
            }
            v51 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
            v52 = *(_DWORD *)(a1 + 352);
            if ( v51 != 0 )
              v29 = v52 | 0x100;
            else
              v29 = v52 & 0xFFFFFEFF;
            goto LABEL_787;
          }
          v14 = a1;
          LOBYTE(v7) = 29;
          v15 = 1937007732;
        }
        else
        {
          if ( a2 == 1127511406 )
          {
            v11 = a1;
            LOWORD(v7) = 3;
            v12 = 1685417577;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 == 1127512161 )
          {
            v17 = a1;
            LOBYTE(v7) = 3;
            v18 = 1131247713;
            return sub_140E885E0(v17, v7, v18, a3);
          }
          if ( a2 != 1128350049 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v14 = a1;
          LOBYTE(v7) = 29;
          v15 = 1635021925;
        }
      }
      return sub_1411E9540(v14, v7, v15, a3);
    }
    if ( a2 > 1127444076 )
    {
      if ( a2 > 1127507761 )
      {
        if ( a2 > 1127509809 )
        {
          if ( a2 > 1127510639 )
          {
            switch ( a2 )
            {
              case 1127510889:
                v11 = a1;
                LOWORD(v7) = 3;
                goto LABEL_482;
              case 1127510890:
              case 1127510891:
              case 1127510892:
              case 1127510893:
              case 1127510895:
              case 1127510896:
              case 1127510898:
              case 1127510899:
              case 1127510900:
              case 1127510901:
              case 1127510902:
              case 1127510903:
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              case 1127510894:
                v11 = a1;
                LOWORD(v7) = 3;
                v12 = 1416851041;
                return sub_1411F76F0(v11, v7, v12, a3);
              case 1127510897:
                v11 = a1;
                LOWORD(v7) = 3;
                v12 = 1416851817;
                return sub_1411F76F0(v11, v7, v12, a3);
              case 1127510904:
                v11 = a1;
                LOWORD(v7) = 3;
                v12 = 1131640942;
                return sub_1411F76F0(v11, v7, v12, a3);
              default:
                if ( a2 == 1127510640 )
                {
                  v11 = a1;
                  LOWORD(v7) = 3;
                  goto LABEL_725;
                }
                if ( a2 != 1127511161 )
                  return sub_1411F4F70(a1, (unsigned int)a2, a3);
                v11 = a1;
                LOWORD(v7) = 3;
                v12 = 1416919408;
                break;
            }
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          switch ( a2 )
          {
            case 1127509810:
              v17 = a1;
              LOBYTE(v7) = 3;
              v18 = 1416326962;
              break;
            case 1127509811:
              v17 = a1;
              LOBYTE(v7) = 3;
              v18 = 1416326963;
              break;
            case 1127509860:
              v11 = a1;
              LOWORD(v7) = 3;
              v12 = 1416586351;
              return sub_1411F76F0(v11, v7, v12, a3);
            default:
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
          }
          return sub_140E885E0(v17, v7, v18, a3);
        }
        if ( a2 > 1127509357 )
        {
          if ( a2 <= 1127509603 )
          {
            if ( a2 == 1127509358 )
            {
              v11 = a1;
              LOWORD(v7) = 3;
              v12 = 1416457833;
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            if ( a2 != 1127509601 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v17 = a1;
            LOBYTE(v7) = 3;
            v18 = 1131245153;
          }
          else
          {
            if ( a2 == 1127509604 )
            {
              v11 = a1;
              LOWORD(v7) = 3;
              v12 = 1416520809;
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            if ( a2 == 1127509613 )
            {
              v11 = a1;
              LOWORD(v7) = 3;
              v12 = 1416392289;
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            if ( a2 != 1127509809 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v17 = a1;
            LOBYTE(v7) = 3;
            v18 = 1416326961;
          }
          return sub_140E885E0(v17, v7, v18, a3);
        }
        if ( a2 > 1127509091 )
        {
          if ( a2 == 1127509092 )
          {
            v11 = a1;
            LOWORD(v7) = 3;
            v12 = 1416389737;
          }
          else
          {
            if ( a2 != 1127509104 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v11 = a1;
            LOWORD(v7) = 3;
            v12 = 1416392819;
          }
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 != 1127507762 )
        {
          if ( a2 != 1127507763 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v17 = a1;
          LOBYTE(v7) = 3;
          v18 = 1416324915;
          return sub_140E885E0(v17, v7, v18, a3);
        }
        v17 = a1;
        LOBYTE(v7) = 3;
        goto LABEL_671;
      }
      if ( a2 > 1127445624 )
      {
        if ( a2 <= 1127506291 )
        {
          if ( a2 == 1127445625 )
          {
            v11 = a1;
            LOWORD(v7) = 2;
            v12 = 1416919408;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 == 1127445870 )
          {
            v11 = a1;
            LOWORD(v7) = 2;
            v12 = 1685417577;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 != 1127446625 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v17 = a1;
          LOBYTE(v7) = 2;
          v18 = 1131247713;
          return sub_140E885E0(v17, v7, v18, a3);
        }
        if ( a2 > 1127507061 )
        {
          if ( a2 == 1127507062 )
          {
            v11 = a1;
            LOWORD(v7) = 3;
            v12 = 1415870057;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 != 1127507761 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v17 = a1;
          LOBYTE(v7) = 3;
          v18 = 1416324913;
          return sub_140E885E0(v17, v7, v18, a3);
        }
        if ( a2 != 1127506292 )
        {
          if ( a2 != 1127507059 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v11 = a1;
          LOWORD(v7) = 3;
          v12 = 1684632417;
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        v17 = a1;
        LOBYTE(v7) = 3;
        goto LABEL_620;
      }
      if ( a2 <= 1127444323 )
      {
        if ( a2 > 1127444273 )
        {
          if ( a2 == 1127444274 )
          {
            v17 = a1;
            LOBYTE(v7) = 2;
            v18 = 1416326962;
          }
          else
          {
            if ( a2 != 1127444275 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v17 = a1;
            LOBYTE(v7) = 2;
            v18 = 1416326963;
          }
        }
        else
        {
          if ( a2 == 1127444077 )
          {
            v11 = a1;
            LOWORD(v7) = 2;
            v12 = 1416392289;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 != 1127444273 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v17 = a1;
          LOBYTE(v7) = 2;
          v18 = 1416326961;
        }
        return sub_140E885E0(v17, v7, v18, a3);
      }
      switch ( a2 )
      {
        case 1127445353:
          v11 = a1;
          LOWORD(v7) = 2;
LABEL_482:
          v12 = 1416852585;
          return sub_1411F76F0(v11, v7, v12, a3);
        case 1127445354:
        case 1127445355:
        case 1127445356:
        case 1127445357:
        case 1127445359:
        case 1127445360:
        case 1127445362:
        case 1127445363:
        case 1127445364:
        case 1127445365:
        case 1127445366:
        case 1127445367:
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        case 1127445358:
          v11 = a1;
          LOWORD(v7) = 2;
          v12 = 1416851041;
          return sub_1411F76F0(v11, v7, v12, a3);
        case 1127445361:
          v11 = a1;
          LOWORD(v7) = 2;
          v12 = 1416851817;
          return sub_1411F76F0(v11, v7, v12, a3);
        case 1127445368:
          v11 = a1;
          LOWORD(v7) = 2;
          v12 = 1131640942;
          return sub_1411F76F0(v11, v7, v12, a3);
        default:
          if ( a2 == 1127444324 )
          {
            v11 = a1;
            LOWORD(v7) = 2;
            v12 = 1416586351;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 != 1127445104 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v11 = a1;
          LOWORD(v7) = 2;
          break;
      }
    }
    else
    {
      if ( a2 > 1127379816 )
      {
        if ( a2 > 1127441525 )
        {
          if ( a2 > 1127443555 )
          {
            if ( a2 <= 1127443821 )
            {
              if ( a2 == 1127443556 )
              {
                v11 = a1;
                LOWORD(v7) = 2;
                v12 = 1416389737;
              }
              else
              {
                if ( a2 != 1127443568 )
                  return sub_1411F4F70(a1, (unsigned int)a2, a3);
                v11 = a1;
                LOWORD(v7) = 2;
                v12 = 1416392819;
              }
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            if ( a2 == 1127443822 )
            {
              v11 = a1;
              LOWORD(v7) = 2;
              v12 = 1416457833;
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            if ( a2 != 1127444065 )
            {
              if ( a2 != 1127444068 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              v11 = a1;
              LOWORD(v7) = 2;
              v12 = 1416520809;
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            v17 = a1;
            LOBYTE(v7) = 2;
            v18 = 1131245153;
            return sub_140E885E0(v17, v7, v18, a3);
          }
          if ( a2 <= 1127442225 )
          {
            if ( a2 == 1127441526 )
            {
              v11 = a1;
              LOWORD(v7) = 2;
              v12 = 1415870057;
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            if ( a2 != 1127442225 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v17 = a1;
            LOBYTE(v7) = 2;
            v18 = 1416324913;
            return sub_140E885E0(v17, v7, v18, a3);
          }
          if ( a2 != 1127442226 )
          {
            if ( a2 != 1127442227 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v17 = a1;
            LOBYTE(v7) = 2;
            v18 = 1416324915;
            return sub_140E885E0(v17, v7, v18, a3);
          }
          v17 = a1;
          LOBYTE(v7) = 2;
LABEL_671:
          v18 = 1416324914;
          return sub_140E885E0(v17, v7, v18, a3);
        }
        if ( a2 <= 1127380333 )
        {
          switch ( a2 )
          {
            case 1127379817:
              v11 = a1;
              LOWORD(v7) = 1;
              goto LABEL_482;
            case 1127379818:
            case 1127379819:
            case 1127379820:
            case 1127379821:
            case 1127379823:
            case 1127379824:
            case 1127379826:
            case 1127379827:
            case 1127379828:
            case 1127379829:
            case 1127379830:
            case 1127379831:
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            case 1127379822:
              v11 = a1;
              LOWORD(v7) = 1;
              v12 = 1416851041;
              return sub_1411F76F0(v11, v7, v12, a3);
            case 1127379825:
              v11 = a1;
              LOWORD(v7) = 1;
              v12 = 1416851817;
              return sub_1411F76F0(v11, v7, v12, a3);
            case 1127379832:
              v11 = a1;
              LOWORD(v7) = 1;
              v12 = 1131640942;
              return sub_1411F76F0(v11, v7, v12, a3);
            default:
              if ( a2 != 1127380089 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              v11 = a1;
              LOWORD(v7) = 1;
              v12 = 1416919408;
              break;
          }
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 <= 1127440755 )
        {
          if ( a2 == 1127380334 )
          {
            v11 = a1;
            LOWORD(v7) = 1;
            v12 = 1685417577;
            return sub_1411F76F0(v11, v7, v12, a3);
          }
          if ( a2 != 1127381089 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v17 = a1;
          LOBYTE(v7) = 1;
          v18 = 1131247713;
          return sub_140E885E0(v17, v7, v18, a3);
        }
        if ( a2 != 1127440756 )
        {
          if ( a2 != 1127441523 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v11 = a1;
          LOWORD(v7) = 2;
          v12 = 1684632417;
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        v17 = a1;
        LOBYTE(v7) = 2;
LABEL_620:
        v18 = 1130460260;
        return sub_140E885E0(v17, v7, v18, a3);
      }
      if ( a2 <= 1127378285 )
      {
        if ( a2 > 1127376688 )
        {
          if ( a2 > 1127376690 )
          {
            if ( a2 != 1127376691 )
            {
              if ( a2 == 1127378020 )
              {
                v11 = a1;
                LOWORD(v7) = 1;
                v12 = 1416389737;
              }
              else
              {
                if ( a2 != 1127378032 )
                  return sub_1411F4F70(a1, (unsigned int)a2, a3);
                v11 = a1;
                LOWORD(v7) = 1;
                v12 = 1416392819;
              }
              return sub_1411F76F0(v11, v7, v12, a3);
            }
            v17 = a1;
            LOBYTE(v7) = 1;
            v18 = 1416324915;
            return sub_140E885E0(v17, v7, v18, a3);
          }
          if ( a2 == 1127376689 )
          {
            v17 = a1;
            LOBYTE(v7) = 1;
            v18 = 1416324913;
            return sub_140E885E0(v17, v7, v18, a3);
          }
          v17 = a1;
          LOBYTE(v7) = 1;
          goto LABEL_671;
        }
        if ( a2 > 1127375986 )
        {
          if ( a2 == 1127375987 )
          {
            v11 = a1;
            LOWORD(v7) = 1;
            v12 = 1684632417;
          }
          else
          {
            if ( a2 != 1127375990 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v11 = a1;
            LOWORD(v7) = 1;
            v12 = 1415870057;
          }
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 == 1127314289 )
        {
          v11 = a1;
          v7 = 0;
          v12 = 1416851817;
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 != 1127375220 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        v17 = a1;
        LOBYTE(v7) = 1;
        goto LABEL_620;
      }
      if ( a2 <= 1127378736 )
      {
        if ( a2 > 1127378531 )
        {
          if ( a2 == 1127378532 )
          {
            v11 = a1;
            LOWORD(v7) = 1;
            v12 = 1416520809;
          }
          else
          {
            if ( a2 != 1127378541 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v11 = a1;
            LOWORD(v7) = 1;
            v12 = 1416392289;
          }
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 == 1127378286 )
        {
          v11 = a1;
          LOWORD(v7) = 1;
          v12 = 1416457833;
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 != 1127378529 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        v17 = a1;
        LOBYTE(v7) = 1;
        v18 = 1131245153;
        return sub_140E885E0(v17, v7, v18, a3);
      }
      if ( a2 <= 1127378738 )
      {
        v17 = a1;
        LOBYTE(v7) = 1;
        if ( a2 == 1127378737 )
          v18 = 1416326961;
        else
          v18 = 1416326962;
        return sub_140E885E0(v17, v7, v18, a3);
      }
      if ( a2 == 1127378739 )
      {
        v17 = a1;
        LOBYTE(v7) = 1;
        v18 = 1416326963;
        return sub_140E885E0(v17, v7, v18, a3);
      }
      if ( a2 == 1127378788 )
      {
        v11 = a1;
        LOWORD(v7) = 1;
        v12 = 1416586351;
        return sub_1411F76F0(v11, v7, v12, a3);
      }
      if ( a2 != 1127379568 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      v11 = a1;
      LOWORD(v7) = 1;
    }
LABEL_725:
    v12 = 1416783216;
    return sub_1411F76F0(v11, v7, v12, a3);
  }
  if ( a2 <= 1131373672 )
  {
    if ( a2 <= 1130722147 )
    {
      if ( a2 <= 1130591352 )
      {
        if ( a2 > 1130590306 )
        {
          if ( (unsigned int)(a2 - 1130591074) > 0x17 || (v25 = 8602193, !_bittest(&v25, a2 - 1130591074)) )
          {
            if ( a2 != 1130590307 )
            {
              if ( a2 != 1130590825 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              goto LABEL_830;
            }
          }
        }
        else
        {
          if ( (unsigned int)(a2 - 1130588769) > 0x18 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v13 = 17600973;
          if ( !_bittest(&v13, a2 - 1130588769) )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
        }
        return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
      }
      if ( a2 <= 1130717795 )
      {
        if ( a2 > 1130656360 )
        {
          if ( a2 > 1130657384 )
          {
            if ( a2 == 1130657385 )
            {
              v3 = (__int64 **)qword_141B5FDC0;
              sub_140FE7960(&v200, a3, 1668246896);
              v96 = sub_140F7A940(v3, &v200);
              v97 = *(__int64 **)(a1 + 24);
              v98 = *(__int64 **)(a1 + 32);
              if ( v97 != v98 )
              {
                if ( *v97 != 0 )
                {
                  *(_QWORD *)(*v97 + 80) = v96;
                  v97 = *(__int64 **)(a1 + 24);
                  v98 = *(__int64 **)(a1 + 32);
                }
                LOBYTE(v3) = 1;
                if ( v97 != v98 )
                {
                  v99 = *v97;
                  if ( *v97 != 0 && *(_QWORD *)(v99 + 48) != 0 )
                  {
                    v100 = *(_QWORD *)(v99 + 80);
                    if ( v100 != 0 && *(_QWORD *)(v100 + 96) != 0 )
                    {
                      sub_1407C9510(&v200);
                      v102 = sub_14083D4F0(v101);
                      LODWORD(v206[0]) = 3;
                      v205 = v102 + 40;
                      sub_140833EB0(&v200, 1685353593, &v205);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
                      v103 = *(unsigned int *)(a1 + 16);
                      v104 = *(unsigned int *)(a1 + 12);
                      if ( (_DWORD)v103 != 0 )
                        v104 = (unsigned int)v103;
                      v105 = *(int *)(a1 + 12) | (unsigned __int64)(v104 << 32);
                      v106 = sub_14083D4F0(v103);
                      v206[0] = v105;
                      v205 = v106 + 72;
                      sub_140833EB0(&v200, 1685417577, &v205);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
                      v108 = sub_14083D4F0(v107);
                      LODWORD(v206[0]) = 1131312233;
                      v205 = v108 + 56;
                      sub_140833EB0(&v200, 1886549113, &v205);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
                      v110 = sub_14083D4F0(v109);
                      LOBYTE(v206[0]) = 1;
                      v205 = v110 + 24;
                      sub_140833EB0(&v200, 1230193478, &v205);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
                      v111 = **(_QWORD **)(a1 + 24);
                      v112 = *(_QWORD *)(v111 + 48);
                      if ( v112 != 0 )
                        v112 = *(_QWORD *)(v111 + 80);
                      v113 = *(_QWORD *)(v112 + 96);
                      if ( v113 != 0 )
                      {
                        v111 = *(int *)(v113 + 12);
                        v114 = *(_DWORD *)(v113 + 16);
                        v115 = (unsigned int)v111;
                        if ( v114 != 0 )
                          v115 = v114;
                        v116 = v111 | (v115 << 32);
                      }
                      else
                      {
                        v116 = -1;
                      }
                      v179 = sub_14083D4F0(v111);
                      v206[0] = v116;
                      v205 = v179 + 72;
                      sub_140833EB0(&v200, 1853322860, &v205);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
                      LOBYTE(v180) = 1;
                      sub_140F47AD0(
                        (unsigned int)&qword_141B5FDA8,
                        (unsigned int)&v200,
                        0,
                        v180,
                        1,
                        0,
                        1,
                        0,
                        0,
                        1,
                        0,
                        0);
                      sub_1407C9510(&v205);
                      LODWORD(v199) = 3;
                      v198 = sub_14083D4F0(v181) + 40;
                      sub_140833EB0(&v205, 1685353593, &v198);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v198 + 16LL))(v198, &v198);
                      v182 = *(unsigned int *)(a1 + 16);
                      v183 = *(unsigned int *)(a1 + 12);
                      if ( (_DWORD)v182 != 0 )
                        v183 = (unsigned int)v182;
                      v184 = *(int *)(a1 + 12) | (unsigned __int64)(v183 << 32);
                      v185 = sub_14083D4F0(v182);
                      v199 = v184;
                      v198 = v185 + 72;
                      sub_140833EB0(&v205, 1685417577, &v198);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v198 + 16LL))(v198, &v198);
                      v187 = sub_14083D4F0(v186);
                      LODWORD(v199) = 1130586990;
                      v198 = v187 + 56;
                      sub_140833EB0(&v205, 1886549113, &v198);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v198 + 16LL))(v198, &v198);
                      v189 = sub_14083D4F0(v188);
                      LOBYTE(v199) = 1;
                      v198 = v189 + 24;
                      sub_140833EB0(&v205, 1230193478, &v198);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v198 + 16LL))(v198, &v198);
                      v190 = **(_QWORD **)(a1 + 24);
                      v191 = *(_QWORD *)(v190 + 48);
                      if ( v191 != 0 )
                        v191 = *(_QWORD *)(v190 + 80);
                      v192 = *(_QWORD *)(v191 + 96);
                      if ( v192 != 0 )
                      {
                        v190 = *(int *)(v192 + 12);
                        v193 = *(_DWORD *)(v192 + 16);
                        v194 = (unsigned int)v190;
                        if ( v193 != 0 )
                          v194 = v193;
                        v195 = v190 | (v194 << 32);
                      }
                      else
                      {
                        v195 = -1;
                      }
                      v196 = sub_14083D4F0(v190);
                      v199 = v195;
                      v198 = v196 + 72;
                      v3 = (__int64 **)&v198;
                      sub_140833EB0(&v205, 1853322860, &v198);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v198 + 16LL))(v198, &v198);
                      LOBYTE(v3) = 1;
                      LOBYTE(v197) = 1;
                      sub_140F47AD0(
                        (unsigned int)&qword_141B5FDA8,
                        (unsigned int)&v205,
                        0,
                        v197,
                        1,
                        0,
                        1,
                        0,
                        0,
                        1,
                        0,
                        0);
                      sub_140833970(&v205);
                      sub_140833970(&v200);
                    }
                  }
                }
                return (unsigned int)v3;
              }
              goto LABEL_788;
            }
            if ( a2 != 1130717540 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            goto LABEL_419;
          }
          if ( a2 == 1130656361 )
          {
            v82 = *(_QWORD **)(a1 + 24);
            if ( v82 == *(_QWORD **)(a1 + 32) || *v82 == 0 )
              goto LABEL_830;
            v83 = a1;
            LOBYTE(v9) = 6;
            goto LABEL_669;
          }
          if ( a2 == 1130656624 )
          {
            v10 = a1;
            LOBYTE(v9) = 2;
            goto LABEL_650;
          }
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        }
        if ( a2 <= 1130654069 )
        {
          if ( a2 == 1130591353 )
          {
            v65 = *(_QWORD *)(a1 + 248);
            sub_140FE7E60(a1 + 248, a3);
            LOBYTE(v3) = 1;
            if ( (unsigned __int8)sub_140087040() != 0 && *(_QWORD *)(a1 + 248) != 0 )
            {
              v66 = *(_QWORD *)(a1 + 24);
              v67 = *(_QWORD *)(a1 + 32);
              if ( v67 != v66 )
              {
                v68 = 0;
                if ( v65 != 0 )
                {
                  do
                  {
                    v69 = *(_QWORD *)(v66 + 8 * v68);
                    while ( 1 )
                    {
                      v70 = *(_QWORD *)(v69 + 120);
                      if ( v70 != 0 )
                        break;
                      v71 = *(_QWORD *)(v69 + 48);
                      if ( v71 != 0 )
                      {
                        v72 = *(__int64 **)(v71 + 24);
                        if ( *(__int64 **)(v71 + 32) != v72 )
                        {
                          v73 = *v72;
                          v74 = v73 == v69;
                          v69 = v73;
                          if ( !v74 )
                            continue;
                        }
                      }
                      goto LABEL_544;
                    }
                    if ( v65 == *(_QWORD *)(v70 + 80) )
                    {
                      *(_QWORD *)(v70 + 80) = *(_QWORD *)(a1 + 248);
                      v66 = *(_QWORD *)(a1 + 24);
                      v67 = *(_QWORD *)(a1 + 32);
                    }
LABEL_544:
                    ++v68;
                  }
                  while ( v68 < (v67 - v66) >> 3 );
                }
                else
                {
                  do
                  {
                    v129 = *(_QWORD *)(v66 + 8 * v68);
                    while ( 1 )
                    {
                      v130 = *(_QWORD *)(v129 + 120);
                      if ( v130 != 0 )
                        break;
                      v131 = *(_QWORD *)(v129 + 48);
                      if ( v131 != 0 )
                      {
                        v132 = *(__int64 **)(v131 + 24);
                        if ( *(__int64 **)(v131 + 32) != v132 )
                        {
                          v133 = *v132;
                          v74 = v133 == v129;
                          v129 = v133;
                          if ( !v74 )
                            continue;
                        }
                      }
                      goto LABEL_697;
                    }
                    *(_QWORD *)(v130 + 80) = *(_QWORD *)(a1 + 248);
                    v66 = *(_QWORD *)(a1 + 24);
                    v67 = *(_QWORD *)(a1 + 32);
LABEL_697:
                    ++v68;
                  }
                  while ( v68 < (v67 - v66) >> 3 );
                }
              }
            }
            return (unsigned int)v3;
          }
          if ( a2 != 1130652276 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
        }
        if ( a2 == 1130654070 )
        {
          v92 = sub_14083D4F0(v8);
          v202 = 0;
          v201 = (_QWORD *)(v92 + 8);
          sub_140FEB270(&v200, a3);
          v93 = sub_140F8F320(&v200);
          if ( v93 == 0
            || (v3 = (__int64 **)v93, (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v93 + 56LL))(v93) != 25) )
          {
            v3 = nullptr;
          }
          v94 = *(__int64 **)(a1 + 24);
          if ( v94 != *(__int64 **)(a1 + 32) )
          {
            v95 = *v94;
            if ( v95 != 0 )
              *(_QWORD *)(v95 + 80) = v3;
          }
          (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v201 + 16LL))(v201, &v201);
          goto LABEL_788;
        }
        if ( a2 != 1130655590 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        v38 = *(_QWORD **)(a1 + 24);
        if ( v38 == *(_QWORD **)(a1 + 32) || *v38 == 0 )
          goto LABEL_830;
        sub_140FE7960(&v200, a3, 0);
        if ( (_DWORD)v200 != -1 )
        {
          v41 = *(__int64 **)(a1 + 24);
          if ( v41 != *(__int64 **)(a1 + 32) )
          {
            v42 = *v41;
            if ( *v41 != 0 )
            {
              v43 = *(_DWORD *)(a1 + 12);
              LODWORD(v200) = v43;
              v44 = *(_DWORD *)(a1 + 16);
              if ( v44 == 0 )
                v44 = v43;
              HIDWORD(v200) = v44;
              LOBYTE(v40) = 10;
              LODWORD(v3) = sub_1411B5560(v42, a3, v40, &v200);
              return (unsigned int)v3;
            }
          }
          goto LABEL_830;
        }
        v174 = *(_QWORD *)(a1 + 328);
        if ( (*(_BYTE *)(qword_141B5FDB8 + 90) & 4) != 0 )
        {
          if ( v174 == 0 )
            goto LABEL_830;
          v178 = sub_14083D4F0(v39);
          v201 = nullptr;
          v200 = (__int64 *)(v178 + 8);
          sub_140FE7F20(v174 + *(int *)(*(_QWORD *)(v174 + 8) + 4LL) + 8, &v200);
          sub_140FE7960(&v205, &v200, 0);
          if ( (int)v205 >= 0 )
            goto LABEL_813;
        }
        else
        {
          if ( (_DWORD)v174 == -1 )
            goto LABEL_830;
          v175 = sub_14083D4F0(v39);
          v201 = nullptr;
          v200 = (__int64 *)(v175 + 8);
          sub_140FE7F20(v174, &v200);
          sub_140FE7960(&v205, &v200, 0);
          if ( (int)v205 >= 0 )
          {
LABEL_813:
            v177 = **(_QWORD **)(a1 + 24);
            v205 = -1;
            LOBYTE(v176) = 10;
            LODWORD(v3) = sub_1411B5560(v177, &v200, v176, &v205);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v200 + 16))(v200, &v200);
            return (unsigned int)v3;
          }
        }
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v200 + 16))(v200, &v200);
        goto LABEL_830;
      }
      if ( a2 > 1130720370 )
      {
        if ( a2 > 1130720631 )
        {
          if ( a2 != 1130720632 && a2 != 1130721394 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
        }
        else
        {
          if ( a2 == 1130720371 )
          {
            if ( *(_QWORD *)(a1 + 256) == 0 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            *(_BYTE *)(*(_QWORD *)(a1 + 256) + 303LL) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(
                                                          *a3,
                                                          a3);
            goto LABEL_788;
          }
          if ( a2 != 1130720622 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
        }
      }
      else
      {
        if ( a2 > 1130718319 )
        {
          if ( a2 == 1130718320 )
          {
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) != 0 )
              sub_140E63B60(a1);
            else
              sub_140E63BF0(a1);
            goto LABEL_788;
          }
          if ( a2 != 1130718564 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          goto LABEL_419;
        }
        if ( a2 != 1130717796 && a2 != 1130718068 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
      }
      return sub_140E882D0(a1, (unsigned int)a2, a3);
    }
    if ( a2 > 1131180142 )
    {
      if ( a2 <= 1131307366 )
      {
        if ( a2 <= 1131245160 )
        {
          if ( a2 > 1131241830 )
          {
            if ( a2 != 1131241831 )
            {
              if ( a2 != 1131244645 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
            }
            v11 = a1;
            v7 = 0;
            v12 = 1131241831;
          }
          else if ( a2 == 1131180143 )
          {
            v11 = a1;
            v7 = 0;
            v12 = 1416392815;
          }
          else
          {
            if ( a2 != 1131180147 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v11 = a1;
            v7 = 0;
            v12 = 1416392819;
          }
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 <= 1131246700 )
        {
          if ( a2 != 1131245161 )
          {
            if ( a2 != 1131246697 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
          }
          v11 = a1;
          v7 = 0;
          v12 = 1416457833;
          return sub_1411F76F0(v11, v7, v12, a3);
        }
        if ( a2 != 1131246701 )
        {
          if ( a2 == 1131246704 )
            goto LABEL_419;
          if ( a2 != 1131299670 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v27 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
          v28 = *(_DWORD *)(a1 + 352);
          if ( v27 != 0 )
            v29 = v28 | 0x1000000;
          else
            v29 = v28 & 0xFEFFFFFF;
          goto LABEL_787;
        }
        return sub_140E882D0(a1, (unsigned int)a2, a3);
      }
      if ( a2 <= 1131308386 )
      {
        if ( a2 <= 1131307379 )
        {
          if ( a2 != 1131307367 )
          {
            if ( a2 != 1131307373 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            LOBYTE(v3) = 1;
            if ( (*(_BYTE *)(a1 + 352) & 4) != 0 || (unsigned __int8)sub_140E83430() != 0 )
              return (unsigned int)v3;
            if ( (unsigned __int8)sub_140E834A0(a1, 1413704814, a3) != 0 )
            {
              *(_BYTE *)(a1 + 354) |= 1u;
              return (unsigned int)v3;
            }
            goto LABEL_830;
          }
          v11 = a1;
          v7 = 0;
          v12 = 1131307367;
        }
        else
        {
          if ( a2 == 1131307380 )
          {
            v61 = sub_14083D4F0(v8);
            v3 = &v201;
            v202 = 0;
            v201 = (_QWORD *)(v61 + 8);
            sub_140FEB270(&v200, a3);
            v62 = sub_140F8F320(&v200);
            if ( v62 == 0 || (v63 = v62, (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v62 + 56LL))(v62) != 10) )
              v63 = 0;
            *(_QWORD *)(a1 + 216) = v63;
            (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v201 + 16LL))(v201, &v201);
            goto LABEL_788;
          }
          if ( a2 == 1131307884 )
          {
            sub_140FE7DE0(&v200, a3);
            sub_140E75A70(a1, v200);
            goto LABEL_788;
          }
          if ( a2 != 1131308137 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v11 = a1;
          v7 = 0;
          v12 = 1416520809;
        }
        return sub_1411F76F0(v11, v7, v12, a3);
      }
      if ( a2 <= 1131311969 )
      {
        if ( a2 == 1131308387 )
        {
          v10 = a1;
          LOBYTE(v9) = 55;
          goto LABEL_650;
        }
        if ( a2 != 1131310948 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        v11 = a1;
        v7 = 0;
        v12 = 1416523620;
        return sub_1411F76F0(v11, v7, v12, a3);
      }
      if ( a2 == 1131311970 || a2 == 1131312226 )
        goto LABEL_419;
      if ( a2 != 1131312233 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      v200 = nullptr;
      sub_140FE7D20(&v200, a3);
      v31 = sub_140087040();
      v32 = *(_QWORD *)(a1 + 216);
      if ( v31 != 0 && v32 != 0 && v200 == nullptr )
      {
        *(_QWORD *)(a1 + 224) = v32;
      }
      else if ( v32 == 0 )
      {
        goto LABEL_802;
      }
      if ( *(_BYTE *)(a1 + 185) != 0 )
      {
        v145 = *(_QWORD *)(v32 + 272);
        if ( v145 != 0 )
        {
LABEL_801:
          --*(_WORD *)(v145 + 412);
          goto LABEL_802;
        }
        if ( *(_QWORD *)(v32 + 264) != 0 )
        {
          v145 = *(_QWORD *)(v32 + 264);
          goto LABEL_801;
        }
      }
      else
      {
        v145 = *(_QWORD *)(v32 + 264);
        if ( v145 != 0 )
          goto LABEL_801;
      }
LABEL_802:
      v172 = v200;
      *(_QWORD *)(a1 + 216) = v200;
      if ( v172 != nullptr && (*(_BYTE *)(a1 + 185) != 0 && (v173 = v172[34]) != 0 || (v173 = v172[33]) != 0) )
        ++*(_WORD *)(v173 + 412);
      goto LABEL_788;
    }
    if ( a2 <= 1130919016 )
    {
      if ( a2 > 1130784367 )
      {
        if ( a2 <= 1130788463 )
        {
          if ( a2 != 1130784368 && a2 != 1130785902 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
        }
        if ( a2 == 1130788464 )
        {
          v10 = a1;
          LOBYTE(v9) = 1;
          goto LABEL_650;
        }
        if ( a2 != 1130914150 && a2 != 1130918756 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        goto LABEL_419;
      }
      if ( a2 > 1130723443 )
      {
        if ( a2 == 1130723444 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) == 0 )
          {
            LOBYTE(v3) = 1;
            if ( *(_QWORD *)(a1 + 216) == 0 )
            {
              v161 = *(_QWORD *)(a1 + 224);
              *(_QWORD *)(a1 + 216) = v161;
              if ( v161 == 0 )
                *(_QWORD *)(a1 + 216) = sub_140F61810(0);
              *(_QWORD *)(a1 + 224) = 0;
            }
            return (unsigned int)v3;
          }
          if ( (unsigned __int8)sub_140835E00(&qword_141B60C30, 1668178792) == 0 )
          {
            sub_140823B40(qword_141ABD468, &v200, 400500);
            sub_14081EC00(&v200, &v205);
            sub_140FE8810(1668179565, &v205);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
            goto LABEL_808;
          }
          v125 = *(_QWORD *)(a1 + 216);
          if ( v125 != 0 )
            *(_QWORD *)(a1 + 224) = v125;
          sub_140E87580(a1, 0);
LABEL_788:
          LOBYTE(v3) = 1;
          return (unsigned int)v3;
        }
        if ( a2 != 1130770736 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        goto LABEL_112;
      }
      if ( a2 == 1130722148 )
        goto LABEL_419;
      if ( a2 != 1130722412 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      return sub_140E882D0(a1, (unsigned int)a2, a3);
    }
    if ( a2 <= 1131177835 )
    {
      if ( a2 > 1131164525 )
      {
        if ( a2 == 1131164526 )
          return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
        if ( a2 != 1131177065 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        v11 = a1;
        v7 = 0;
        v12 = 1416389737;
        return sub_1411F76F0(v11, v7, v12, a3);
      }
      if ( a2 == 1130919017 )
      {
        *(_BYTE *)(*(_QWORD *)(a1 + 256) + 298LL) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(
                                                      *a3,
                                                      a3);
        goto LABEL_788;
      }
      if ( a2 != 1130972001 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      v35 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
      v36 = *(_DWORD *)(a1 + 352);
      if ( v35 != 0 )
        v29 = v36 | 4;
      else
        v29 = v36 & 0xFFFFFFFB;
      goto LABEL_787;
    }
    if ( a2 > 1131179631 )
    {
      if ( a2 != 1131179632 )
      {
        if ( a2 == 1131179888 )
        {
          v11 = a1;
          v7 = 0;
          v12 = 1416588400;
        }
        else
        {
          if ( a2 != 1131180142 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v11 = a1;
          v7 = 0;
          v12 = 1416392814;
        }
        return sub_1411F76F0(v11, v7, v12, a3);
      }
      v200 = (__int64 *)a1;
      v75 = a1;
      LOBYTE(v9) = 1;
LABEL_581:
      sub_141537730(&v201, v75, v9);
      v205 = (__int64)&v200;
      v206[0] = &v201;
      v50 = sub_140EB29D0(&v205, a3);
      goto LABEL_651;
    }
    if ( a2 != 1131177836 )
    {
      if ( a2 != 1131178099 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
    }
    goto LABEL_459;
  }
  if ( a2 > 1131639906 )
  {
    if ( a2 <= 1131768939 )
    {
      if ( a2 <= 1131703413 )
      {
        if ( a2 <= 1131700588 )
        {
          switch ( a2 )
          {
            case 1131639907:
              if ( (_BYTE)word_141B60320 == 0 )
                goto LABEL_830;
              v16 = *(_QWORD **)(a1 + 24);
              if ( v16 == *(_QWORD **)(a1 + 32) || *v16 == 0 )
                goto LABEL_830;
              sub_1415337E0(&v200);
              v205 = (__int64)&v200;
              v206[0] = &v204;
              LODWORD(v3) = sub_140EB1800(&v205, a3);
              sub_1409FF7C0(&v200);
              break;
            case 1131639908:
            case 1131639910:
            case 1131639911:
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            case 1131639909:
            case 1131639912:
              return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
            case 1131639913:
              v11 = a1;
              v7 = 0;
              goto LABEL_482;
            default:
              if ( a2 != 1131640942 )
                return sub_1411F4F70(a1, (unsigned int)a2, a3);
              return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
          }
          return (unsigned int)v3;
        }
        if ( a2 > 1131701568 )
        {
          if ( a2 != 1131701569 && a2 != 1131701859 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          goto LABEL_419;
        }
        if ( a2 == 1131700589 )
        {
          v53 = *(__int64 ***)(a1 + 24);
          if ( v53 != *(__int64 ***)(a1 + 32) && *v53 != nullptr )
          {
            v200 = *v53;
            sub_141530F90(&v201);
            v205 = (__int64)&v200;
            v206[0] = &v201;
            v50 = sub_140EA93A0(&v205, a3);
            goto LABEL_651;
          }
          goto LABEL_830;
        }
        if ( a2 != 1131700853 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
LABEL_497:
        if ( *(_QWORD *)(a1 + 256) != 0 )
        {
          LOBYTE(v7) = 1;
          if ( sub_140E65F60(a1, v7) != 0 )
          {
            if ( a2 == 1131572578 )
            {
              v56 = 52 * (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            }
            else
            {
              if ( a2 != 1131700853 )
              {
LABEL_741:
                LOBYTE(v55) = 1;
                v150 = sub_140E65F60(a1, v55);
                return sub_141536D80(v150, (unsigned int)a2, a3);
              }
              v56 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            }
            if ( v56 == 0 )
              goto LABEL_741;
            v146 = *(_QWORD *)(a1 + 336);
            if ( v146 != 0 )
            {
              v147 = *(unsigned __int8 *)(v146 + 60);
              v148 = *(__int64 **)(a1 + 24);
              LOWORD(v55) = 1500;
              if ( v148 != *(__int64 **)(a1 + 32) )
              {
                v149 = *v148;
                if ( v149 != 0 )
                  v55 = *(unsigned __int16 *)(v149 + 168);
              }
              if ( (unsigned __int8)sub_14147BD40(v56, v55, v147) != 0 )
                goto LABEL_741;
            }
            sub_140823B40(qword_141ABD468, &v200, 521012);
            sub_14081EC00(&v200, &v205);
            sub_140FE8810(1684170098, &v205);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v205 + 16LL))(v205, &v205);
LABEL_808:
            sub_14081D040(&v200);
            LODWORD(v3) = 0;
            return (unsigned int)v3;
          }
LABEL_830:
          LODWORD(v3) = 0;
          return (unsigned int)v3;
        }
LABEL_502:
        v57 = (unsigned int)a2;
LABEL_503:
        sub_140F4AEF0(&qword_141B5FDA8, v57, a3);
        goto LABEL_788;
      }
      if ( (unsigned int)(a2 - 1131767345) >= 9 )
      {
        if ( a2 != 1131703414 )
        {
          if ( a2 != 1131705193 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v3 = (__int64 **)qword_141B5FE28;
          sub_140FE7960(&v200, a3, 1937006948);
          *(_QWORD *)(a1 + 320) = sub_140F7A940(v3, &v200);
          goto LABEL_788;
        }
        return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
      }
LABEL_112:
      v20 = *(_QWORD *)(a1 + 256);
      if ( v20 != 0 )
      {
        v21 = a1 + 256;
        switch ( a2 )
        {
          case 1131767345:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v22 = sub_140E5FC10(72);
              *(_QWORD *)v22 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v22 + 8) = -1;
              *(_QWORD *)(v22 + 60) = 0;
              *(_QWORD *)(v22 + 12) = 0;
              *(_QWORD *)(v22 + 20) = 0;
              *(_QWORD *)(v22 + 28) = 0;
              *(_QWORD *)(v22 + 36) = 0;
              *(_QWORD *)(v22 + 44) = 0;
              *(_QWORD *)(v22 + 49) = 0;
              *(_BYTE *)(v22 + 12) = 10;
              *(_DWORD *)(v22 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v22;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            v24 = 0;
            goto LABEL_782;
          case 1131767346:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v151 = *(_QWORD *)(v20 + 72);
            if ( v151 == 0 )
            {
              v152 = sub_140E5FC10(72);
              *(_QWORD *)v152 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v152 + 8) = -1;
              *(_QWORD *)(v152 + 60) = 0;
              *(_QWORD *)(v152 + 12) = 0;
              *(_QWORD *)(v152 + 20) = 0;
              *(_QWORD *)(v152 + 28) = 0;
              *(_QWORD *)(v152 + 36) = 0;
              *(_QWORD *)(v152 + 44) = 0;
              *(_QWORD *)(v152 + 49) = 0;
              *(_BYTE *)(v152 + 12) = 10;
              *(_DWORD *)(v152 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v152;
              v151 = *(_QWORD *)(*(_QWORD *)v21 + 72LL);
              if ( v151 == 0 )
                v151 = 0;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            LOBYTE(v3) = 1;
            LOBYTE(v153) = 1;
            sub_140D4D580(v151, v153);
            return (unsigned int)v3;
          case 1131767347:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v154 = sub_140E5FC10(72);
              *(_QWORD *)v154 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v154 + 8) = -1;
              *(_QWORD *)(v154 + 60) = 0;
              *(_QWORD *)(v154 + 12) = 0;
              *(_QWORD *)(v154 + 20) = 0;
              *(_QWORD *)(v154 + 28) = 0;
              *(_QWORD *)(v154 + 36) = 0;
              *(_QWORD *)(v154 + 44) = 0;
              *(_QWORD *)(v154 + 49) = 0;
              *(_BYTE *)(v154 + 12) = 10;
              *(_DWORD *)(v154 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v154;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 2;
            goto LABEL_782;
          case 1131767348:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v155 = sub_140E5FC10(72);
              *(_QWORD *)v155 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v155 + 8) = -1;
              *(_QWORD *)(v155 + 60) = 0;
              *(_QWORD *)(v155 + 12) = 0;
              *(_QWORD *)(v155 + 20) = 0;
              *(_QWORD *)(v155 + 28) = 0;
              *(_QWORD *)(v155 + 36) = 0;
              *(_QWORD *)(v155 + 44) = 0;
              *(_QWORD *)(v155 + 49) = 0;
              *(_BYTE *)(v155 + 12) = 10;
              *(_DWORD *)(v155 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v155;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 3;
            goto LABEL_782;
          case 1131767349:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v156 = sub_140E5FC10(72);
              *(_QWORD *)v156 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v156 + 8) = -1;
              *(_QWORD *)(v156 + 60) = 0;
              *(_QWORD *)(v156 + 12) = 0;
              *(_QWORD *)(v156 + 20) = 0;
              *(_QWORD *)(v156 + 28) = 0;
              *(_QWORD *)(v156 + 36) = 0;
              *(_QWORD *)(v156 + 44) = 0;
              *(_QWORD *)(v156 + 49) = 0;
              *(_BYTE *)(v156 + 12) = 10;
              *(_DWORD *)(v156 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v156;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 4;
            goto LABEL_782;
          case 1131767350:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v158 = sub_140E5FC10(72);
              *(_QWORD *)v158 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v158 + 8) = -1;
              *(_QWORD *)(v158 + 60) = 0;
              *(_QWORD *)(v158 + 12) = 0;
              *(_QWORD *)(v158 + 20) = 0;
              *(_QWORD *)(v158 + 28) = 0;
              *(_QWORD *)(v158 + 36) = 0;
              *(_QWORD *)(v158 + 44) = 0;
              *(_QWORD *)(v158 + 49) = 0;
              *(_BYTE *)(v158 + 12) = 10;
              *(_DWORD *)(v158 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v158;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 5;
            goto LABEL_782;
          case 1131767351:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v159 = sub_140E5FC10(72);
              *(_QWORD *)v159 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v159 + 8) = -1;
              *(_QWORD *)(v159 + 60) = 0;
              *(_QWORD *)(v159 + 12) = 0;
              *(_QWORD *)(v159 + 20) = 0;
              *(_QWORD *)(v159 + 28) = 0;
              *(_QWORD *)(v159 + 36) = 0;
              *(_QWORD *)(v159 + 44) = 0;
              *(_QWORD *)(v159 + 49) = 0;
              *(_BYTE *)(v159 + 12) = 10;
              *(_DWORD *)(v159 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v159;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 6;
            goto LABEL_782;
          case 1131767352:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v157 = sub_140E5FC10(72);
              *(_QWORD *)v157 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v157 + 8) = -1;
              *(_QWORD *)(v157 + 60) = 0;
              *(_QWORD *)(v157 + 12) = 0;
              *(_QWORD *)(v157 + 20) = 0;
              *(_QWORD *)(v157 + 28) = 0;
              *(_QWORD *)(v157 + 36) = 0;
              *(_QWORD *)(v157 + 44) = 0;
              *(_QWORD *)(v157 + 49) = 0;
              *(_BYTE *)(v157 + 12) = 10;
              *(_DWORD *)(v157 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v157;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 7;
            goto LABEL_782;
          case 1131767353:
            if ( *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v160 = sub_140E5FC10(72);
              *(_QWORD *)v160 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v160 + 8) = -1;
              *(_QWORD *)(v160 + 60) = 0;
              *(_QWORD *)(v160 + 12) = 0;
              *(_QWORD *)(v160 + 20) = 0;
              *(_QWORD *)(v160 + 28) = 0;
              *(_QWORD *)(v160 + 36) = 0;
              *(_QWORD *)(v160 + 44) = 0;
              *(_QWORD *)(v160 + 49) = 0;
              *(_BYTE *)(v160 + 12) = 10;
              *(_DWORD *)(v160 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v160;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 8;
            goto LABEL_782;
          default:
            if ( a2 != 1130770736 || *(_QWORD *)(a1 + 216) == 0 )
              goto LABEL_830;
            v3 = *(__int64 ***)(v20 + 72);
            if ( v3 == nullptr )
            {
              v54 = sub_140E5FC10(72);
              *(_QWORD *)v54 = 0xFFFFFFFF00000000uLL;
              *(_DWORD *)(v54 + 8) = -1;
              *(_QWORD *)(v54 + 60) = 0;
              *(_QWORD *)(v54 + 12) = 0;
              *(_QWORD *)(v54 + 20) = 0;
              *(_QWORD *)(v54 + 28) = 0;
              *(_QWORD *)(v54 + 36) = 0;
              *(_QWORD *)(v54 + 44) = 0;
              *(_QWORD *)(v54 + 49) = 0;
              *(_BYTE *)(v54 + 12) = 10;
              *(_DWORD *)(v54 + 68) = 0;
              *(_QWORD *)(*(_QWORD *)v21 + 72LL) = v54;
              v3 = *(__int64 ***)(*(_QWORD *)v21 + 72LL);
              if ( v3 == nullptr )
                v3 = nullptr;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
            v23 = v3;
            LOBYTE(v24) = 9;
LABEL_782:
            sub_140D4D580(v23, v24);
            break;
        }
        goto LABEL_788;
      }
      goto LABEL_502;
    }
    if ( a2 > 1413704813 )
    {
      if ( a2 > 1415800939 )
      {
        if ( a2 <= 1417111660 )
        {
          if ( a2 == 1415800940 )
          {
            v11 = a1;
            v7 = 0;
            v12 = 1415800940;
          }
          else
          {
            if ( a2 != 1416456301 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            v11 = a1;
            v7 = 0;
            v12 = 1416456301;
          }
        }
        else
        {
          if ( a2 != 1417111661 )
          {
            if ( a2 == 1467114864 )
            {
              *(_WORD *)(a1 + 358) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
              goto LABEL_788;
            }
            if ( a2 != 1885565044 )
              return sub_1411F4F70(a1, (unsigned int)a2, a3);
            return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
          }
          v11 = a1;
          v7 = 0;
          v12 = 1417111661;
        }
        return sub_1411F76F0(v11, v7, v12, a3);
      }
      if ( a2 <= 1413706351 )
      {
        if ( a2 != 1413704814 )
        {
          if ( a2 != 1413705577 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
        }
        (*(void (__fastcall **)(_QWORD, __int64 **, _QWORD *))(*(_QWORD *)*a3 + 128LL))(*a3, &v200, a3);
        LODWORD(v3) = a1 + 192;
        sub_140809100(a1 + 192, &v200);
        v79 = v200;
        if ( v200 != nullptr && _InterlockedDecrement((volatile signed __int32 *)v200 - 1) == 0 )
          sub_1412EC9A0((char *)v79 - 4, v78);
        v80 = 2;
        if ( dword_141B60300 != 12 )
          v80 = 3 * (dword_141B60300 == 18);
        *(_BYTE *)(a1 + 356) = v80;
        LOWORD(v78) = 24;
        sub_140E45100(a1 + 208, v78);
        v81 = *(_DWORD **)(a1 + 200);
        if ( v81 == nullptr || *v81 == 0 )
        {
          sub_140809100(a1 + 200, a1 + 192);
          *(_BYTE *)(a1 + 357) = *(_BYTE *)(a1 + 356);
        }
LABEL_574:
        sub_1411F7CB0(a1);
        goto LABEL_788;
      }
      if ( a2 == 1413706352 )
      {
        if ( (unsigned __int8)sub_1400015B0() != 0 && (_BYTE)word_141B60320 != 0 )
          *(_WORD *)(a1 + 358) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      }
      if ( a2 == 1413706606 )
      {
        (*(void (__fastcall **)(_QWORD, __int64 **, _QWORD *))(*(_QWORD *)*a3 + 128LL))(*a3, &v200, a3);
        LODWORD(v3) = a1 + 200;
        sub_140809100(a1 + 200, &v200);
        v46 = v200;
        if ( v200 != nullptr && _InterlockedDecrement((volatile signed __int32 *)v200 - 1) == 0 )
          sub_1412EC9A0((char *)v46 - 4, v45);
        v47 = 2;
        if ( dword_141B60300 != 12 )
          v47 = 3 * (dword_141B60300 == 18);
        *(_BYTE *)(a1 + 357) = v47;
        LOWORD(v45) = 25;
        sub_140E45100(a1 + 208, v45);
        v48 = *(_DWORD **)(a1 + 192);
        if ( v48 == nullptr || *v48 == 0 )
        {
          sub_140809100(a1 + 192, a1 + 200);
          *(_BYTE *)(a1 + 356) = *(_BYTE *)(a1 + 357);
        }
        goto LABEL_574;
      }
      return sub_1411F4F70(a1, (unsigned int)a2, a3);
    }
    if ( a2 > 1132029549 )
    {
      if ( a2 > 1132033141 )
      {
        if ( a2 != 1132033142 )
        {
          if ( a2 != 1145392197 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          LOBYTE(v3) = 1;
          LOBYTE(v7) = 1;
          sub_140E87580(a1, v7);
          return (unsigned int)v3;
        }
      }
      else if ( a2 != 1132029550 && a2 != 1132030317 )
      {
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      }
      return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
    }
    if ( a2 > 1131902817 )
    {
      if ( a2 != 1131902818 )
      {
        if ( a2 != 1132029538 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
      }
      goto LABEL_419;
    }
    if ( a2 != 1131768940 )
    {
      if ( a2 != 1131897708 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
    }
    v76 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
    v77 = *(_DWORD *)(a1 + 352);
    if ( v76 != 0 )
      v29 = v77 & 0xFFFDFFFF;
    else
      v29 = v77 | 0x20000;
LABEL_787:
    *(_DWORD *)(a1 + 352) = v29;
    goto LABEL_788;
  }
  if ( a2 > 1131635819 )
  {
    if ( a2 > 1131638643 )
    {
      if ( a2 > 1131639416 )
      {
        switch ( a2 )
        {
          case 1131639621:
            LOBYTE(v7) = 35;
            v3 = (__int64 **)sub_1411EACB0(a1, v7, 0xFFFFFFFFLL, 0xFFFFFFFFLL);
            v30 = sub_140DBC940();
            sub_140DBCA60(v30, &v200, a3);
            *((_DWORD *)v3 + 3) = (_DWORD)v200;
            goto LABEL_788;
          case 1131639622:
          case 1131639623:
          case 1131639624:
          case 1131639625:
          case 1131639626:
          case 1131639627:
          case 1131639628:
          case 1131639629:
          case 1131639630:
          case 1131639631:
          case 1131639633:
          case 1131639634:
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          case 1131639632:
            LOBYTE(v7) = 35;
            v3 = (__int64 **)sub_1411EACB0(a1, v7, 0xFFFFFFFFLL, 0xFFFFFFFFLL);
            *((_DWORD *)v3 + 5) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_788;
          case 1131639635:
            LOBYTE(v7) = 35;
            v3 = (__int64 **)sub_1411EACB0(a1, v7, 0xFFFFFFFFLL, 0xFFFFFFFFLL);
            v58 = sub_140DBC940();
            sub_140DBCA60(v58, &v200, a3);
            *((_DWORD *)v3 + 2) = (_DWORD)v200;
            goto LABEL_788;
          case 1131639636:
            LOBYTE(v7) = 35;
            v3 = (__int64 **)sub_1411EACB0(a1, v7, 0xFFFFFFFFLL, 0xFFFFFFFFLL);
            *((_DWORD *)v3 + 4) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            goto LABEL_788;
          default:
            if ( a2 == 1131639417 )
              goto LABEL_497;
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
        }
      }
      if ( (unsigned int)(a2 - 1131638882) > 0x12 || (v19 = 393225, !_bittest(&v19, a2 - 1131638882)) )
      {
        if ( a2 != 1131638644 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        *(_DWORD *)(a1 + 352) = (*(_DWORD *)(a1 + 352) & 0xFFFFFFFD)
                              + 2
                              * (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
        goto LABEL_788;
      }
      return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
    }
    if ( a2 <= 1131638116 )
    {
      if ( a2 > 1131637859 )
      {
        if ( a2 != 1131637860 )
        {
          if ( a2 != 1131637881 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
        }
      }
      else
      {
        if ( a2 == 1131635820 )
          goto LABEL_419;
        if ( a2 != 1131637348 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
      }
    }
    else if ( a2 <= 1131638368 )
    {
      if ( a2 == 1131638117 )
      {
        v205 = a1;
        v206[0] = a1;
        v200 = &v205;
        v201 = v206;
        LODWORD(v3) = sub_140EB0810(&v200, a3);
        return (unsigned int)v3;
      }
      if ( a2 != 1131638126 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
    }
    else if ( a2 != 1131638369 )
    {
      if ( a2 == 1131638381 )
      {
        LOBYTE(v3) = 1;
        if ( (*(_BYTE *)(a1 + 352) & 4) != 0 || (unsigned __int8)sub_140E83430() != 0 )
          return (unsigned int)v3;
        if ( (unsigned __int8)sub_140E834A0(a1, 1413706606, a3) != 0 )
        {
          v123 = sub_140E78A80();
          sub_140FF5990(v123, *(unsigned int *)(a1 + 12), a1 + 200);
          return (unsigned int)v3;
        }
        goto LABEL_830;
      }
      if ( a2 != 1131638627 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
    }
    return sub_140E87C00(a1, (unsigned int)a2, a3);
  }
  if ( a2 <= 1131570543 )
  {
    if ( a2 > 1131439712 )
    {
      if ( a2 > 1131442802 )
      {
        if ( a2 == 1131442803 )
        {
          v121 = sub_140087040();
          LODWORD(v3) = (unsigned __int8)word_141B60320;
          v122 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          if ( v121 != 0 && (_BYTE)v3 != 0 )
          {
            (*(void (__fastcall **)(__int64, __int64, _QWORD, __int64))(*(_QWORD *)qword_141B5EDE8 + 88LL))(
              qword_141B5EDE8,
              a1,
              v122,
              2);
          }
          else
          {
            *(_BYTE *)(a1 + 362) = v122;
            if ( (_BYTE)v122 == 20 )
            {
              *(_BYTE *)(a1 + 362) = 3;
              *(_BYTE *)(a1 + 353) |= 0x20u;
            }
            else
            {
              *(_BYTE *)(a1 + 353) &= ~0x20u;
            }
          }
          goto LABEL_788;
        }
        if ( a2 != 1131570018 )
        {
          if ( a2 != 1131570284 )
            return sub_1411F4F70(a1, (unsigned int)a2, a3);
          v205 = a1;
          v206[0] = a1;
          v200 = &v205;
          v201 = v206;
          LODWORD(v3) = sub_140EAB300(&v200, a3);
          return (unsigned int)v3;
        }
        return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
      }
      if ( a2 != 1131439713 )
      {
        if ( a2 != 1131440233 )
          return sub_1411F4F70(a1, (unsigned int)a2, a3);
        v11 = a1;
        v7 = 0;
        v12 = 1416652905;
        return sub_1411F76F0(v11, v7, v12, a3);
      }
LABEL_419:
      v49 = *(_QWORD *)(a1 + 336);
      if ( v49 != 0 )
        return (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD *))(*(_QWORD *)v49 + 24LL))(v49, (unsigned int)a2, a3);
      goto LABEL_830;
    }
    if ( a2 > 1131378541 )
    {
      if ( a2 == 1131378542 )
      {
        *(_BYTE *)(*(_QWORD *)(a1 + 256) + 297LL) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(
                                                      *a3,
                                                      a3);
        v126 = *(_QWORD *)(a1 + 256);
        LOBYTE(v3) = 1;
        if ( ((*(_BYTE *)(v126 + 297) - 3) & 0xFB) == 0 && *(_QWORD *)(v126 + 120) == 0 )
        {
          v127 = sub_140E5F8C0();
          sub_141521AA0(v127, a1);
          v128 = *(_QWORD *)(a1 + 256);
          if ( v128 != 0 && *(_QWORD *)(v128 + 120) == 0 )
            *(_QWORD *)(v128 + 120) = v127;
          else
            sub_140E58670(v127);
        }
        return (unsigned int)v3;
      }
      if ( a2 == 1131435081 )
      {
        sub_141530050(&v200, a1);
        v205 = (__int64)&v200;
        v206[0] = &v201;
        v50 = sub_140EA61C0(&v205, a3);
        goto LABEL_651;
      }
      return sub_1411F4F70(a1, (unsigned int)a2, a3);
    }
    if ( a2 != 1131373673 )
    {
      if ( a2 != 1131374958 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
    }
    v11 = a1;
    v7 = 0;
    v12 = 1416586351;
    return sub_1411F76F0(v11, v7, v12, a3);
  }
  if ( a2 > 1131628352 )
  {
    if ( a2 <= 1131635045 )
    {
      if ( a2 == 1131628353 )
        return sub_140E71F20(a1, a3);
      if ( a2 == 1131631681 )
        return sub_140E72050(a1, a3);
      return sub_1411F4F70(a1, (unsigned int)a2, a3);
    }
    if ( a2 == 1131635046 )
      return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
    if ( a2 != 1131635561 )
    {
      if ( a2 != 1131635565 )
        return sub_1411F4F70(a1, (unsigned int)a2, a3);
      v205 = a1;
      v206[0] = a1;
      v200 = &v205;
      v201 = v206;
      LODWORD(v3) = sub_140EAF7B0(&v200, a3);
      return (unsigned int)v3;
    }
    v124 = *(_QWORD **)(a1 + 24);
    if ( v124 == *(_QWORD **)(a1 + 32) || *v124 == 0 )
      goto LABEL_830;
    v83 = a1;
    LOBYTE(v9) = 14;
LABEL_669:
    sub_141535790(&v200, v83, v9);
    v205 = (__int64)&v200;
    v206[0] = &v201;
    v50 = sub_140EB22A0(&v205, a3);
LABEL_651:
    LODWORD(v3) = v50;
    if ( v201 != nullptr )
      sub_1407E4890(qword_141ABD470, v201, v203 - (_QWORD)v201);
    return (unsigned int)v3;
  }
  if ( a2 <= 1131572577 )
  {
    if ( a2 == 1131570544 )
    {
      v117 = *(__int64 **)(a1 + 24);
      LOBYTE(v3) = 1;
      if ( v117 != *(__int64 **)(a1 + 32) )
      {
        v118 = *v117;
        if ( *v117 != 0 )
        {
          LODWORD(v201) = *(__int16 *)(v118 + 168);
          v200 = (__int64 *)(sub_14083D4F0(v8) + 40);
          sub_141405B90(a1, 1099938928, (unsigned int)&v200, (_DWORD)a3, 0);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v200 + 16))(v200, &v200);
          v119 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          sub_140FC9D50(v118, v119, 0);
        }
      }
      return (unsigned int)v3;
    }
    if ( a2 != 1131572084 )
      return sub_1411F4F70(a1, (unsigned int)a2, a3);
    return sub_140E587E0(*(_QWORD *)(a1 + 256), a1, (unsigned int)a2, a3);
  }
  if ( a2 == 1131572578 )
    goto LABEL_497;
  if ( a2 != 1131574393 )
  {
    if ( a2 == 1131574883 )
    {
      v10 = a1;
      LOBYTE(v9) = 5;
LABEL_650:
      sub_140E879C0(&v200, v10, v9);
      v205 = (__int64)&v200;
      v206[0] = &v201;
      v50 = sub_140EAC3E0(&v205, a3);
      goto LABEL_651;
    }
    return sub_1411F4F70(a1, (unsigned int)a2, a3);
  }
  v200 = (__int64 *)a1;
  sub_1415314A0(&v201, a1);
  v205 = (__int64)&v200;
  v206[0] = &v201;
  LODWORD(v3) = sub_140EA9EB0(&v205, a3);
  sub_140E878A0(&v200);
  return (unsigned int)v3;
}
