__int64 __fastcall sub_140EC0A60(__int64 a1, int a2, __int64 *a3)
{
  unsigned __int64 v3; // rbx
  __int64 v5; // r12
  char v6; // bl
  __int64 v7; // rax
  __int64 v8; // rcx
  int v10; // esi
  __int64 v11; // rdx
  __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r9
  _DWORD *v15; // rcx
  unsigned __int64 *v16; // rax
  __int64 v17; // rsi
  unsigned __int64 v18; // rsi
  unsigned __int64 v19; // rdi
  __int64 v21; // rcx
  __int64 v22; // r8
  __int64 v23; // rcx
  int v24; // esi
  __int64 v25; // rax
  __int64 v26; // rcx
  __int64 v27; // rax
  char v28; // bl
  __int64 v29; // rax
  unsigned int v30; // eax
  int v31; // ecx
  int v32; // esi
  __int64 v33; // rax
  __int64 v34; // rax
  int v35; // ecx
  __int64 v36; // rax
  __int64 v37; // rdx
  int v38; // ecx
  int v39; // ecx
  unsigned int v40; // eax
  int v41; // esi
  __int64 v42; // rax
  __int64 v43; // rcx
  __int64 v44; // rcx
  __int64 v45; // rax
  __int64 v46; // rax
  __int64 v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rcx
  __int64 v50; // rax
  __int64 *v51; // rcx
  __int64 v52; // rcx
  __int64 v53; // rcx
  int v54; // esi
  __int64 v55; // rax
  __int64 v56; // rax
  __int64 v57; // rcx
  _OWORD *v58; // r12
  __int64 v59; // rax
  __int64 v60; // rcx
  char v61; // bl
  __int64 v62; // rax
  __int64 v63; // rax
  __int64 v64; // rax
  __int64 v65; // rax
  int v66; // esi
  __int64 v67; // rax
  __int64 v68; // rax
  __int64 v69; // rax
  __int64 v70; // rcx
  __int64 v71; // rax
  unsigned int v72; // eax
  char v73; // si
  __int64 v74; // rsi
  __int64 v75; // rcx
  __int64 v76; // rax
  int v77; // edx
  __int64 v78; // rcx
  __int64 v79; // rax
  __int64 v80; // rsi
  __int64 v81; // rax
  __int64 v82; // rdx
  __int64 *v83; // rax
  __int64 v84; // rax
  __int64 v85; // rax
  __int64 v86; // rdi
  __int64 v87; // rcx
  __int64 v88; // rax
  int v89; // eax
  int v90; // edx
  _QWORD *v91; // rax
  __int64 v92; // rax
  __int64 v93; // rsi
  int v94; // ecx
  __int64 v95; // rcx
  char *v96; // rax
  __int64 v97; // rcx
  __int64 v98; // rcx
  char v99; // bl
  __int64 v100; // rcx
  __int64 v101; // rcx
  int v102; // esi
  __int64 v103; // rcx
  char v104; // bl
  __int64 v105; // rcx
  int v106; // esi
  __int64 v107; // rcx
  int v108; // esi
  __int64 v109; // rcx
  __int64 v110; // rax
  __int64 v111; // rax
  int v112; // esi
  __int64 v113; // rax
  int v114; // edi
  __int64 v115; // rcx
  __int64 v116; // rax
  __int64 v117; // rcx
  __int64 v118; // rax
  __int64 v119; // rcx
  float v120; // xmm6_4
  char v121; // bl
  __int64 v122; // rax
  __int64 v123; // rcx
  __int64 v124; // rax
  __int64 v125; // rdx
  __int64 v126; // rax
  __int64 v127; // r15
  unsigned int v128; // r13d
  __int64 v129; // rcx
  __int64 v130; // rcx
  _QWORD *v131; // rax
  __int64 v132; // rcx
  unsigned __int64 v133; // r15
  __int64 v134; // r13
  int v135; // r12d
  __int64 v136; // rax
  __int64 v137; // rax
  __int64 v138; // rax
  _QWORD *v139; // rax
  __int64 v140; // rax
  __int64 v141; // rcx
  __int64 v142; // rdi
  char v143; // cl
  __int64 **v144; // rdx
  __int64 *v145; // rax
  __int64 v146; // rcx
  double v147; // xmm0_8
  __int64 v148; // rax
  __int64 v149; // r13
  unsigned __int64 i; // r15
  _QWORD *v151; // r12
  _QWORD *v152; // r15
  __int64 v153; // rsi
  __int64 v154; // rcx
  __int64 v155; // rax
  __int64 v156; // rax
  __int64 v157; // rax
  __int64 v158; // r15
  __int64 v159; // rax
  __int64 *v160; // rsi
  int v161; // esi
  __int64 v162; // rax
  char v163; // bl
  __int64 v164; // rax
  __int64 v165; // rcx
  __int64 v166; // rax
  __int64 v167; // rcx
  __int64 v168; // rax
  __int64 v169; // rcx
  __int64 v170; // rax
  __int64 v171; // rcx
  __int64 v172; // rax
  __int64 v173; // rcx
  __int64 v174; // rax
  __int64 v175; // rcx
  __int64 v176; // rax
  __int64 v177; // rax
  __int64 v178; // rax
  __int64 v179; // rcx
  __int64 v180; // rax
  __int64 v181; // rcx
  __int64 v182; // rax
  _OWORD *v183; // r12
  __int64 v184; // rcx
  __int64 v185; // rcx
  __int64 v186; // rax
  __int64 v187; // rcx
  __int64 v188; // rax
  __int64 v189; // rax
  int v190; // esi
  __int64 v191; // rax
  char v192; // bl
  __int64 v193; // rax
  __int64 v194; // rax
  __int64 v195; // rsi
  int v196; // eax
  unsigned int v197; // edi
  __int64 v198; // rax
  int v199; // esi
  __int64 v200; // rax
  char v201; // bl
  __int64 v202; // rax
  __int64 v203; // rax
  __int64 v204; // rcx
  __int64 v205; // rax
  __int64 v206; // rcx
  __int64 v207; // rax
  __int64 v208; // rcx
  __int64 v209; // rax
  __int64 v210; // rsi
  __int64 v211; // rax
  __int64 v212; // rdx
  __int64 *v213; // rax
  __int64 v214; // rax
  __int64 v215; // rax
  __int64 v216; // rdi
  __int64 v217; // rcx
  char v218; // si
  char v219; // bl
  __int64 v220; // rcx
  __int64 v221; // rax
  __int64 v222; // rax
  unsigned int v223; // eax
  int v224; // edi
  __int64 v225; // rcx
  __int64 v226; // rax
  int v227; // esi
  __int64 v228; // rcx
  __int64 v229; // rax
  char v230; // bl
  __int64 v231; // rax
  __int64 v232; // rdx
  __int64 v233; // r8
  __int64 v234; // rcx
  __int64 v235; // rax
  __int64 v236; // rsi
  int v237; // r9d
  __int64 v238; // rax
  unsigned __int64 v239; // rax
  __int64 v240; // rdx
  __int64 v241; // r13
  __int64 v242; // rcx
  __int64 v243; // rcx
  __int64 v244; // rcx
  __int64 v245; // rcx
  __int64 v246; // rdx
  __int64 v247; // r8
  __int64 v248; // rcx
  __int64 v249; // rax
  __int64 v250; // rsi
  int v251; // r9d
  __int64 v252; // rax
  unsigned __int64 v253; // rax
  __int64 v254; // rdx
  __int64 v255; // r13
  char v256; // bl
  __int64 v257; // rcx
  __int64 v258; // rax
  __int64 v259; // rax
  __int64 v260; // rcx
  __int64 v261; // rcx
  __int64 v262; // rax
  __int64 v263; // rax
  __int64 v264; // rcx
  unsigned int v265; // eax
  __int64 v266; // rax
  __int64 v267; // rcx
  __int64 v268; // rax
  __int64 v269; // rcx
  unsigned int v270; // eax
  int v271; // ecx
  int v272; // esi
  __int64 v273; // rcx
  __int64 v274; // rax
  __int64 v275; // rdi
  __int64 v276; // rax
  __int64 v277; // rdx
  unsigned __int64 v278; // r15
  __int64 v279; // rsi
  __int64 v280; // rdx
  unsigned __int64 v281; // rsi
  __int64 v282; // rcx
  __int64 v283; // rax
  _OWORD *v284; // r12
  __int64 v285; // rcx
  int v286; // esi
  int v287; // esi
  __int64 v288; // rax
  __int64 v289; // r8
  __int64 v290; // rax
  __int64 v291; // rax
  __int64 v292; // rax
  __int64 v293; // rax
  __int64 v294; // rcx
  __int64 *v295; // rax
  char v296; // si
  __int64 v297; // rax
  int v298; // esi
  __int64 v299; // rcx
  __int64 v300; // rax
  __int64 v301; // rcx
  __int64 v302; // rax
  __int64 v303; // rax
  __int64 v304; // rax
  unsigned int v305; // eax
  __int64 v306; // rcx
  __int64 v307; // rax
  __int64 v308; // r8
  __int64 v309; // rcx
  _QWORD *v310; // rsi
  __int64 v311; // rax
  __int64 v312; // rax
  __int64 *v313; // rcx
  __int64 v314; // rax
  __int64 v315; // rcx
  _BYTE *v316; // rsi
  __int64 v317; // rdx
  __int64 v318; // rax
  _QWORD *v319; // rcx
  __int64 v320; // rcx
  __int64 v321; // rax
  __int64 v322; // rax
  __int64 v323; // rdi
  __int64 v324; // rcx
  __int64 v325; // rsi
  __int64 v326; // r15
  __int64 v327; // rax
  unsigned int v328; // eax
  int v329; // edx
  __int64 v330; // rax
  __int64 v331; // rax
  __int64 v332; // rdi
  __int64 v333; // rcx
  __int64 v334; // rsi
  __int64 v335; // r15
  __int64 v336; // rax
  unsigned int v337; // eax
  int v338; // edx
  __int64 v339; // rax
  __int64 v340; // rdx
  unsigned __int64 *v341; // rcx
  __int64 v342; // rcx
  __int64 v343; // rdx
  __int64 v344; // rdx
  __int64 v345; // rcx
  __int64 v346; // rax
  int **v347; // rdx
  int *v348; // rax
  __int64 v349; // rax
  __int64 v350; // rcx
  __int64 v351; // rax
  __int64 *v352; // rdx
  int v353; // eax
  __int64 v354; // r8
  __int64 v355; // rcx
  __int64 v356; // rax
  __int64 v357; // rax
  _QWORD *v358; // r12
  __int64 v359; // rdi
  __int64 j; // rsi
  __int64 k; // r15
  _QWORD *v362; // r13
  __int64 v363; // rdi
  unsigned __int64 v364; // rsi
  __int64 v365; // r15
  unsigned __int64 v366; // rax
  __int64 v367; // rdx
  __int64 *v368; // rax
  __int64 *v369; // rdx
  __int64 v370; // rcx
  __int64 v371; // rdx
  __int64 v372; // r13
  __int64 v373; // rax
  __int64 v374; // rax
  __int64 v375; // rax
  __int64 v376; // rcx
  __int64 v377; // rcx
  __int64 *v378; // r13
  __int64 *m; // rdi
  int v380; // esi
  __int64 v381; // rax
  unsigned int v382; // eax
  __int64 v383; // rax
  __int64 v384; // rax
  __int64 *v385; // rdx
  __int64 v386; // rax
  __int64 v387; // rsi
  __int64 v388; // rax
  __int64 v389; // r9
  char v390; // cl
  __int64 v391; // rdx
  int v392; // esi
  __int64 v393; // rcx
  __int64 v394; // rax
  int v395; // esi
  __int64 v396; // rax
  __int64 v397; // rcx
  int v398; // esi
  __int64 v399; // rcx
  int v400; // eax
  __int64 *v401; // rdx
  __int64 v402; // rax
  __int64 *v403; // rsi
  __int64 v404; // rax
  __int64 v405; // rsi
  __int64 v406; // rcx
  __int64 v407; // rax
  unsigned __int64 n; // rdi
  __int64 v409; // r15
  unsigned __int64 v410; // rcx
  __int64 v411; // r12
  __int64 v412; // rax
  unsigned __int64 v413; // r13
  __int64 *v414; // rbx
  __int64 v415; // rax
  __int64 v416; // rax
  __int64 v417; // rax
  __int64 v418; // rax
  __int64 v419; // rax
  __int64 v420; // rax
  __int64 v421; // rax
  char v422; // [rsp+20h] [rbp-60h]
  char v423; // [rsp+28h] [rbp-58h]
  char v424; // [rsp+28h] [rbp-58h]
  _BYTE v425[16]; // [rsp+68h] [rbp-18h] BYREF
  _BYTE v426[16]; // [rsp+78h] [rbp-8h] BYREF
  _BYTE v427[16]; // [rsp+88h] [rbp+8h] BYREF
  __int64 v428; // [rsp+98h] [rbp+18h] BYREF
  int v429; // [rsp+A0h] [rbp+20h]
  __int64 v430; // [rsp+A8h] [rbp+28h]
  __int16 v431; // [rsp+B0h] [rbp+30h] BYREF
  unsigned __int16 v432; // [rsp+B2h] [rbp+32h]
  __int64 v433; // [rsp+B8h] [rbp+38h]
  _QWORD *v434; // [rsp+C0h] [rbp+40h] BYREF
  __int64 v435; // [rsp+C8h] [rbp+48h] BYREF
  _QWORD *v436; // [rsp+D8h] [rbp+58h] BYREF
  __int64 v437; // [rsp+E0h] [rbp+60h]
  unsigned __int64 v438; // [rsp+E8h] [rbp+68h] BYREF
  _QWORD v439[2]; // [rsp+F0h] [rbp+70h] BYREF
  __int128 v440; // [rsp+100h] [rbp+80h] BYREF
  __int64 v441; // [rsp+110h] [rbp+90h]
  __int128 v442; // [rsp+120h] [rbp+A0h] BYREF
  __int64 v443; // [rsp+130h] [rbp+B0h]
  __int64 v444; // [rsp+168h] [rbp+E8h]

  v444 = -2;
  v5 = a1;
  if ( a2 == 1668639854 )
  {
    v6 = *(_BYTE *)(a1 + 417);
    v7 = sub_14083D4F0(a1) + 24;
    BYTE8(v442) = (v6 & 0x40) != 0;
    *(_QWORD *)&v442 = v7;
    if ( &v442 != (__int128 *)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v8 = *((_QWORD *)&v442 + 1);
      *(_OWORD *)a3 = v442;
      v7 = sub_14083D4F0(v8) + 8;
      v442 = (unsigned __int64)v7;
    }
LABEL_4:
    v3 = *(_QWORD *)v7;
    (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v7 + 16LL))(v7, &v442);
LABEL_5:
    LOBYTE(v3) = 1;
    return (unsigned int)v3;
  }
  do
  {
    while ( 1 )
    {
      while ( 1 )
      {
        while ( 1 )
        {
LABEL_7:
          v10 = a2;
          if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5ED20 + 32LL))(qword_141B5ED20) == 0
            && (*(unsigned __int8 (__fastcall **)(__int64, __int64, _QWORD, __int64 *))(*(_QWORD *)qword_141B5ED20 + 40LL))(
                 qword_141B5ED20,
                 v5,
                 (unsigned int)v10,
                 a3) != 0 )
          {
            goto LABEL_5;
          }
          if ( v10 <= 1666475104 )
          {
            if ( v10 <= 1131237474 )
            {
              if ( v10 <= 1129138031 )
              {
                if ( v10 > 1128810340 )
                {
                  if ( v10 <= 1129075298 )
                  {
                    if ( v10 > 1128813408 )
                    {
                      switch ( v10 )
                      {
                        case 1128813409:
                          v21 = v5;
                          LOBYTE(v11) = 25;
                          v22 = 1869048947;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1128813410:
                        case 1128813413:
                        case 1128813415:
                        case 1128813416:
                        case 1128813417:
                        case 1128813418:
                        case 1128813419:
                        case 1128813420:
                        case 1128813421:
                        case 1128813422:
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        case 1128813411:
                          v21 = v5;
                          LOBYTE(v11) = 25;
                          goto LABEL_820;
                        case 1128813412:
                          v21 = v5;
                          LOBYTE(v11) = 25;
                          v22 = 1937007732;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1128813414:
                          v21 = v5;
                          LOBYTE(v11) = 25;
                          v22 = 1735355507;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1128813423:
                          v21 = v5;
                          LOBYTE(v11) = 25;
                          v22 = 1869899892;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        default:
                          switch ( v10 )
                          {
                            case 1129070945:
                              v21 = v5;
                              LOBYTE(v11) = 26;
                              v22 = 1635021925;
                              return sub_143CA2E60(v21, v11, v22, a3);
                            case 1129070946:
                            case 1129070949:
                            case 1129070950:
                            case 1129070951:
                            case 1129070952:
                            case 1129070953:
                            case 1129070954:
                            case 1129070955:
                            case 1129070956:
                            case 1129070957:
                            case 1129070958:
                              return sub_140FE3F20((_DWORD *)v5, v10, a3);
                            case 1129070947:
                              v21 = v5;
                              LOBYTE(v11) = 26;
                              goto LABEL_820;
                            case 1129070948:
                              v21 = v5;
                              LOBYTE(v11) = 26;
                              v22 = 1937007732;
                              return sub_143CA2E60(v21, v11, v22, a3);
                            case 1129070959:
                              v21 = v5;
                              LOBYTE(v11) = 26;
                              v22 = 1869899892;
                              return sub_143CA2E60(v21, v11, v22, a3);
                            default:
                              if ( v10 != 1128874822 )
                                return sub_140FE3F20((_DWORD *)v5, v10, a3);
                              v163 = *(_BYTE *)(v5 + 244);
                              v164 = sub_14083D4F0(v12);
                              BYTE8(v442) = v163 == 12;
                              *(_QWORD *)&v442 = v164 + 24;
                              sub_14083DFA0(a3, &v442);
                              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                              break;
                          }
                          goto LABEL_5;
                      }
                    }
                    switch ( v10 )
                    {
                      case 1128810341:
                        v21 = v5;
                        LOBYTE(v11) = 20;
                        v22 = 1701733492;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1128810343:
                        v21 = v5;
                        LOBYTE(v11) = 20;
                        v22 = 1735355507;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1128810350:
                        v21 = v5;
                        LOBYTE(v11) = 20;
                        v22 = 1937010285;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1128810352:
                        v21 = v5;
                        LOBYTE(v11) = 20;
                        v22 = 1937008996;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1128810355:
                        v21 = v5;
                        LOBYTE(v11) = 20;
                        v22 = 1937007732;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1128810356:
                        v21 = v5;
                        LOBYTE(v11) = 20;
                        goto LABEL_820;
                      default:
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    }
                  }
                  if ( v10 > 1129136495 )
                  {
                    if ( v10 > 1129138022 )
                    {
                      if ( v10 == 1129138023 )
                      {
                        v21 = v5;
                        LOBYTE(v11) = 2;
                        v22 = 1735355507;
                      }
                      else
                      {
                        if ( v10 != 1129138030 )
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        v21 = v5;
                        LOBYTE(v11) = 2;
                        v22 = 1937010285;
                      }
                    }
                    else
                    {
                      switch ( v10 )
                      {
                        case 1129136995:
                          v21 = v5;
                          LOBYTE(v11) = 34;
                          goto LABEL_820;
                        case 1129136996:
                          v21 = v5;
                          LOBYTE(v11) = 34;
                          v22 = 1937007732;
                          return sub_143CA2E60(v21, v11, v22, a3);
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
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        case 1129137006:
                          v21 = v5;
                          LOBYTE(v11) = 34;
                          v22 = 1937010285;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129137008:
                          v21 = v5;
                          LOBYTE(v11) = 34;
                          v22 = 1937008996;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129137011:
                          v21 = v5;
                          LOBYTE(v11) = 34;
                          v22 = 1734438259;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        default:
                          if ( v10 != 1129136496 )
                            return sub_140FE3F20((_DWORD *)v5, v10, a3);
                          v21 = v5;
                          LOBYTE(v11) = 1;
                          v22 = 1937008996;
                          break;
                      }
                    }
                  }
                  else
                  {
                    if ( v10 <= 1129083473 )
                    {
                      switch ( v10 )
                      {
                        case 1129075299:
                          v21 = v5;
                          LOBYTE(v11) = 13;
                          goto LABEL_820;
                        case 1129075301:
                          v21 = v5;
                          LOBYTE(v11) = 13;
                          v22 = 1701733492;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129075303:
                          v21 = v5;
                          LOBYTE(v11) = 13;
                          v22 = 1734438259;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129075315:
                          v21 = v5;
                          LOBYTE(v11) = 13;
                          v22 = 1937007732;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        default:
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      }
                    }
                    if ( v10 <= 1129136480 )
                    {
                      if ( v10 == 1129083474 )
                      {
                        v262 = sub_140EBAA10(v5);
                        if ( v262 == 0 )
                          goto LABEL_790;
                        v48 = *(_QWORD *)(v262 + 16);
                        if ( v48 == 0 )
                          goto LABEL_790;
                      }
                      else
                      {
                        if ( v10 != 1129084754 )
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        v65 = sub_140EBAA10(v5);
                        if ( v65 == 0 )
                          goto LABEL_790;
                        v48 = *(_QWORD *)(v65 + 8);
                        if ( v48 == 0 )
                          goto LABEL_790;
                      }
LABEL_745:
                      (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v48 + 144LL))(v48, &v442);
                      sub_140FEAD00(&v442, &v440);
                      sub_14083DFA0(a3, &v440);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                      (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v442 + 1) + 16LL))(
                        *((_QWORD *)&v442 + 1),
                        (char *)&v442 + 8);
                      goto LABEL_5;
                    }
                    if ( v10 == 1129136481 )
                    {
                      v21 = v5;
                      LOBYTE(v11) = 1;
                      v22 = 1634758771;
                    }
                    else
                    {
                      if ( v10 != 1129136494 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      v21 = v5;
                      LOBYTE(v11) = 1;
                      v22 = 1937010285;
                    }
                  }
                  return sub_143CA2E60(v21, v11, v22, a3);
                }
                if ( v10 > 1128679266 )
                {
                  switch ( v10 )
                  {
                    case 1128679267:
                      v21 = v5;
                      LOBYTE(v11) = 24;
                      goto LABEL_820;
                    case 1128679268:
                      v21 = v5;
                      LOBYTE(v11) = 24;
                      v22 = 1937007732;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1128679269:
                    case 1128679270:
                    case 1128679271:
                    case 1128679272:
                    case 1128679273:
                    case 1128679274:
                    case 1128679275:
                    case 1128679276:
                    case 1128679277:
                    case 1128679281:
                    case 1128679282:
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    case 1128679278:
                      v21 = v5;
                      LOBYTE(v11) = 24;
                      v22 = 1937010285;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1128679279:
                      v21 = v5;
                      LOBYTE(v11) = 24;
                      v22 = 1869899892;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1128679280:
                      v21 = v5;
                      LOBYTE(v11) = 24;
                      v22 = 1937008996;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1128679283:
                      v21 = v5;
                      LOBYTE(v11) = 24;
                      v22 = 1718839156;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    default:
                      switch ( v10 )
                      {
                        case 1128746339:
                          v21 = v5;
                          LOBYTE(v11) = 23;
                          goto LABEL_820;
                        case 1128746340:
                          v21 = v5;
                          LOBYTE(v11) = 23;
                          v22 = 1937007732;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1128746341:
                        case 1128746342:
                        case 1128746344:
                        case 1128746345:
                        case 1128746346:
                        case 1128746347:
                        case 1128746348:
                        case 1128746349:
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        case 1128746343:
                          v21 = v5;
                          LOBYTE(v11) = 23;
                          v22 = 1735355507;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1128746350:
                          v21 = v5;
                          LOBYTE(v11) = 23;
                          v22 = 1937010285;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1128746351:
                          v21 = v5;
                          LOBYTE(v11) = 23;
                          v22 = 1869899892;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1128746352:
                          v21 = v5;
                          LOBYTE(v11) = 23;
                          v22 = 1937008996;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        default:
                          switch ( v10 )
                          {
                            case 1128808801:
                              v21 = v5;
                              LOBYTE(v11) = 7;
                              v22 = 1635021925;
                              return sub_143CA2E60(v21, v11, v22, a3);
                            case 1128808803:
                              v21 = v5;
                              LOBYTE(v11) = 7;
                              goto LABEL_820;
                            case 1128808804:
                              v21 = v5;
                              LOBYTE(v11) = 7;
                              v22 = 1937007732;
                              return sub_143CA2E60(v21, v11, v22, a3);
                            case 1128808815:
                              v21 = v5;
                              LOBYTE(v11) = 7;
                              v22 = 1869899892;
                              return sub_143CA2E60(v21, v11, v22, a3);
                            default:
                              return sub_140FE3F20((_DWORD *)v5, v10, a3);
                          }
                      }
                  }
                }
                if ( v10 > 1128350050 )
                {
                  switch ( v10 )
                  {
                    case 1128421217:
                      v21 = v5;
                      LOBYTE(v11) = 8;
                      v22 = 1869048947;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1128421218:
                    case 1128421221:
                    case 1128421223:
                    case 1128421224:
                    case 1128421225:
                    case 1128421226:
                    case 1128421227:
                    case 1128421228:
                    case 1128421229:
                    case 1128421230:
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    case 1128421219:
                      v21 = v5;
                      LOBYTE(v11) = 8;
                      goto LABEL_820;
                    case 1128421220:
                      v21 = v5;
                      LOBYTE(v11) = 8;
                      v22 = 1937007732;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1128421222:
                      v21 = v5;
                      LOBYTE(v11) = 8;
                      v22 = 1735355507;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1128421231:
                      v21 = v5;
                      LOBYTE(v11) = 8;
                      v22 = 1869899892;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    default:
                      if ( v10 == 1128350051 )
                      {
                        v21 = v5;
                        LOBYTE(v11) = 29;
                        goto LABEL_820;
                      }
                      if ( v10 != 1128350052 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      v21 = v5;
                      LOBYTE(v11) = 29;
                      v22 = 1937007732;
                      break;
                  }
                  return sub_143CA2E60(v21, v11, v22, a3);
                }
                if ( v10 <= 1098269547 )
                {
                  if ( v10 == 1097032556 )
                  {
LABEL_262:
                    sub_1407C9510(&v442);
                    sub_140EBC8F0(v5, &v438);
                    v63 = sub_141335F60();
                    DWORD2(v440) = v438;
                    *(_QWORD *)&v440 = v63;
                    v3 = (unsigned __int64)&v440;
                    sub_14083B5F0(&v442, &v440);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                    sub_140EBC750(v5, &v438);
                    v64 = sub_141335F60();
                    DWORD2(v440) = v438;
                    *(_QWORD *)&v440 = v64;
                    sub_14083B5F0(&v442, &v440);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                    sub_14083DB80(&v440, &v442);
                    sub_14083DFA0(a3, &v440);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                    goto LABEL_1152;
                  }
                  if ( v10 != 1097092197 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  sub_141563EB0(&v442, v5);
                  sub_140ECB110(&v442, a3);
                  goto LABEL_804;
                }
                if ( v10 != 1098269548 )
                {
                  if ( v10 != 1128350049 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  v21 = v5;
                  LOBYTE(v11) = 29;
                  v22 = 1635021925;
                  return sub_143CA2E60(v21, v11, v22, a3);
                }
                sub_1407C9510(&v442);
                v148 = (*(_QWORD *)(*(_QWORD *)(qword_141B5FE40 + 128) + 8LL) - **(_QWORD **)(qword_141B5FE40 + 128)) >> 3;
                if ( (int)v148 > 0 )
                {
                  v149 = (unsigned int)v148;
                  for ( i = 0; i != v149; ++i )
                  {
                    if ( (_BYTE)word_141B60320 != 0 )
                    {
                      v313 = *(__int64 **)(qword_141B5FE40 + 128);
                      v314 = *v313;
                      v315 = v313[1];
                    }
                    else
                    {
                      v314 = *(_QWORD *)(qword_141B5FE40 + 96);
                      v315 = *(_QWORD *)(qword_141B5FE40 + 104);
                    }
                    if ( (v315 - v314) >> 3 <= i )
                      v3 = 0;
                    else
                      v3 = *(_QWORD *)(v314 + 8 * i);
                    if ( *(_BYTE *)(v3 + 47) == 0 )
                    {
                      v316 = *(_BYTE **)(v3 + 48);
                      if ( v316 != nullptr
                        && (v316[353] & 1) == 0
                        && (unsigned __int8)sub_1408FF650(*(_QWORD *)(v3 + 48)) == 0
                        && (*(unsigned __int8 (__fastcall **)(_BYTE *))(*(_QWORD *)v316 + 352LL))(v316) == 0 )
                      {
                        if ( *(_BYTE *)(v3 + 40) == 0
                          || (LOBYTE(v317) = 1, (unsigned __int8)sub_140FCA180(v3, v317) != 0) )
                        {
                          v318 = *(_QWORD *)(v3 + 48);
                          v319 = (_QWORD *)(v318 + 368);
                          if ( *(_BYTE *)(v3 + 47) == 0 )
                            v319 = (_QWORD *)(v318 + 216);
                          if ( *v319 != 0 && (v318 != 0 && *(_QWORD *)(v3 + 80) == v5 || *(_QWORD *)(v3 + 104) == v5) )
                          {
                            v440 = (unsigned __int64)(sub_14083D4F0(v319) + 8);
                            sub_140F10C50(v3, &v440);
                            sub_14083B2B0(&v442, &v440);
                            (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                          }
                        }
                      }
                    }
                  }
                }
LABEL_756:
                sub_14083DB80(&v440, &v442);
                sub_14083DFA0(a3, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                goto LABEL_1152;
              }
              if ( v10 <= 1129796194 )
              {
                if ( v10 <= 1129476722 )
                {
                  if ( v10 > 1129272162 )
                  {
                    switch ( v10 )
                    {
                      case 1129272163:
                        v21 = v5;
                        LOBYTE(v11) = 28;
                        goto LABEL_820;
                      case 1129272164:
                        v21 = v5;
                        LOBYTE(v11) = 28;
                        v22 = 1937007714;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1129272173:
                        v21 = v5;
                        LOBYTE(v11) = 28;
                        v22 = 1937007732;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1129272174:
                        v21 = v5;
                        LOBYTE(v11) = 28;
                        v22 = 1937010285;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1129272175:
                        v21 = v5;
                        LOBYTE(v11) = 28;
                        v22 = 1869899892;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1129272176:
                        v21 = v5;
                        LOBYTE(v11) = 28;
                        v22 = 1937008996;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      default:
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    }
                  }
                  switch ( v10 )
                  {
                    case 1129271395:
                      v21 = v5;
                      LOBYTE(v11) = 11;
                      goto LABEL_820;
                    case 1129271396:
                      v21 = v5;
                      LOBYTE(v11) = 11;
                      v22 = 1937007714;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129271397:
                    case 1129271398:
                    case 1129271399:
                    case 1129271400:
                    case 1129271401:
                    case 1129271402:
                    case 1129271403:
                    case 1129271404:
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    case 1129271405:
                      v21 = v5;
                      LOBYTE(v11) = 11;
                      v22 = 1937007732;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129271406:
                      v21 = v5;
                      LOBYTE(v11) = 11;
                      v22 = 1937010285;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129271407:
                      v21 = v5;
                      LOBYTE(v11) = 11;
                      v22 = 1869899892;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129271408:
                      v21 = v5;
                      LOBYTE(v11) = 11;
                      v22 = 1937008996;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    default:
                      if ( v10 == 1129138032 )
                      {
                        v21 = v5;
                        LOBYTE(v11) = 2;
                        v22 = 1937008996;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      }
                      if ( v10 != 1129206861 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      break;
                  }
                  goto LABEL_447;
                }
                if ( v10 > 1129608312 )
                {
                  switch ( v10 )
                  {
                    case 1129792355:
                      v21 = v5;
                      LOBYTE(v11) = 18;
LABEL_820:
                      v22 = 1952801133;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129792356:
                    case 1129792358:
                    case 1129792360:
                    case 1129792361:
                    case 1129792362:
                    case 1129792363:
                    case 1129792364:
                    case 1129792365:
                    case 1129792366:
                    case 1129792367:
                    case 1129792368:
                    case 1129792369:
                    case 1129792370:
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    case 1129792357:
                      v21 = v5;
                      LOBYTE(v11) = 18;
                      v22 = 1701733492;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129792359:
                      v21 = v5;
                      LOBYTE(v11) = 18;
                      v22 = 1734438259;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129792371:
                      v21 = v5;
                      LOBYTE(v11) = 18;
                      v22 = 1937007732;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    default:
                      switch ( v10 )
                      {
                        case 1129794659:
                          v21 = v5;
                          LOBYTE(v11) = 14;
                          goto LABEL_820;
                        case 1129794660:
                        case 1129794662:
                        case 1129794664:
                        case 1129794665:
                        case 1129794666:
                        case 1129794667:
                        case 1129794668:
                        case 1129794669:
                        case 1129794670:
                        case 1129794671:
                        case 1129794672:
                        case 1129794673:
                        case 1129794674:
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        case 1129794661:
                          v21 = v5;
                          LOBYTE(v11) = 14;
                          v22 = 1701733492;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129794663:
                          v21 = v5;
                          LOBYTE(v11) = 14;
                          v22 = 1734438259;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129794675:
                          v21 = v5;
                          LOBYTE(v11) = 14;
                          v22 = 1937007732;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        default:
                          if ( v10 != 1129608313 )
                            return sub_140FE3F20((_DWORD *)v5, v10, a3);
                          v287 = *(char *)(v5 + 421);
                          v288 = sub_14083D4F0(v12);
                          DWORD2(v442) = v287;
                          *(_QWORD *)&v442 = v288 + 40;
                          sub_14083DFA0(a3, &v442);
                          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                          break;
                      }
                      goto LABEL_5;
                  }
                }
                if ( v10 > 1129538368 )
                {
                  if ( v10 == 1129538369 )
                  {
                    v156 = sub_14083D4F0(v12);
                    DWORD2(v442) = 0;
                    *(_QWORD *)&v442 = v156 + 40;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    LOBYTE(v3) = 1;
                    if ( *(_QWORD *)(v5 + 176) != 0 )
                    {
                      v157 = sub_140FE8230();
                      if ( v157 != 0 )
                      {
                        v158 = v157;
                        v159 = qword_141B60C30;
                        v160 = nullptr;
                        if ( qword_141B60C30 != qword_141B60C38 )
                        {
                          while ( *(_DWORD *)v159 != 1214805357 )
                          {
                            v159 += 16;
                            if ( v159 == qword_141B60C38 )
                              goto LABEL_1091;
                          }
                          if ( v159 == qword_141B60C38 )
                            v160 = nullptr;
                          else
                            v160 = *(__int64 **)(v159 + 8);
                        }
LABEL_1091:
                        v384 = sub_14083D4F0(qword_141B60C38);
                        v385 = &qword_141B5A4A0;
                        if ( v160 != nullptr )
                          v385 = v160;
                        v443 = 0;
                        *((_QWORD *)&v442 + 1) = v384 + 8;
                        sub_140FEB270(&v442, v385);
                        v386 = sub_140F8F320(&v442);
                        if ( v386 != 0 )
                        {
                          v387 = v386;
                          if ( (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v386 + 56LL))(v386) == 1 )
                          {
                            v388 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v387 + 1752LL))(v387);
                            if ( v388 != 0 )
                            {
                              v390 = *(_BYTE *)(v158 + 47);
                              v391 = 2;
                              if ( v390 != 1 )
                                v391 = v390 == 0;
                              LOBYTE(v389) = 1;
                              v392 = ((sub_14101ADD0(v388, v391, *(_QWORD *)(*(_QWORD *)(v5 + 176) + 288LL), v389) != 0) << 17)
                                   + 0x20000;
                              v394 = sub_14083D4F0(v393);
                              DWORD2(v440) = v392;
                              *(_QWORD *)&v440 = v394 + 40;
                              sub_14083DFA0(a3, &v440);
                              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                            }
                          }
                        }
                        (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v442 + 1) + 16LL))(
                          *((_QWORD *)&v442 + 1),
                          (char *)&v442 + 8);
                      }
                    }
                    return (unsigned int)v3;
                  }
                  if ( v10 != 1129598291 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  goto LABEL_337;
                }
                if ( v10 == 1129476723 )
                {
                  if ( *(_QWORD *)(v5 + 176) != 0 )
                  {
                    LODWORD(v436) = dword_141AAE084;
                    LOBYTE(v3) = 1;
                    LOBYTE(v14) = 1;
                    sub_140B54340(
                      *(_QWORD *)(qword_141B5AD60 + 8) + 8,
                      (unsigned int)&v434,
                      (unsigned int)&v436,
                      v14,
                      v5,
                      0,
                      0,
                      1,
                      -1,
                      0,
                      1,
                      0,
                      0);
                    if ( v434 != nullptr )
                    {
                      sub_1407C9510(&v442);
                      sub_140893BE0(&v442, (__int64)(v434[1] - *v434) >> 3);
                      v151 = (_QWORD *)*v434;
                      v152 = (_QWORD *)v434[1];
                      if ( (_QWORD *)*v434 != v152 )
                      {
                        do
                        {
                          v153 = *v151;
                          if ( (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)*v151 + 240LL))(*v151) != 0 )
                          {
                            v155 = sub_14083D4F0(v154);
                            v439[0] = 0;
                            v438 = v155 + 8;
                            (*(void (__fastcall **)(__int64, unsigned __int64 *, char *))(*(_QWORD *)(v155 + 8) + 24LL))(
                              v155 + 8,
                              &v438,
                              (char *)&v440 + 8);
                            LODWORD(v440) = -8388609;
                            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                              v438,
                              &v438);
                            sub_1414B18A0(v153, &v440);
                            sub_140FEAD00(&v440, &v438);
                            sub_14083B5F0(&v442, &v438);
                            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                              v438,
                              &v438);
                            (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v440 + 1) + 16LL))(
                              *((_QWORD *)&v440 + 1),
                              (char *)&v440 + 8);
                          }
                          ++v151;
                        }
                        while ( v151 != v152 );
                      }
                      sub_14083DB80(&v440, &v442);
                      sub_14083DFA0(a3, &v440);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                      sub_14083B0A0(&v442);
                    }
                    sub_140E359D0(&v434);
                    return (unsigned int)v3;
                  }
                  goto LABEL_5;
                }
                if ( v10 != 1129477229 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                v37 = v5;
                LOBYTE(v13) = -1;
LABEL_742:
                sub_141563520(&v442, v37, v13);
                sub_140ECA610(&v442, a3);
LABEL_804:
                if ( (_QWORD)v442 != 0 )
                  sub_1407E4890(qword_141ABD470, v442, v443 - v442);
                goto LABEL_5;
              }
              if ( v10 <= 1129927522 )
              {
                if ( v10 > 1129797474 )
                {
                  switch ( v10 )
                  {
                    case 1129926755:
                      v21 = v5;
                      LOBYTE(v11) = 10;
                      goto LABEL_820;
                    case 1129926756:
                      v21 = v5;
                      LOBYTE(v11) = 10;
                      v22 = 1937007714;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129926757:
                    case 1129926758:
                    case 1129926759:
                    case 1129926760:
                    case 1129926761:
                    case 1129926762:
                    case 1129926763:
                    case 1129926764:
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    case 1129926765:
                      v21 = v5;
                      LOBYTE(v11) = 10;
                      v22 = 1937007732;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129926766:
                      v21 = v5;
                      LOBYTE(v11) = 10;
                      v22 = 1937010285;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129926767:
                      v21 = v5;
                      LOBYTE(v11) = 10;
                      v22 = 1869899892;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    case 1129926768:
                      v21 = v5;
                      LOBYTE(v11) = 10;
                      v22 = 1937008996;
                      return sub_143CA2E60(v21, v11, v22, a3);
                    default:
                      switch ( v10 )
                      {
                        case 1129797475:
                          v21 = v5;
                          LOBYTE(v11) = 15;
                          goto LABEL_820;
                        case 1129797477:
                          v21 = v5;
                          LOBYTE(v11) = 15;
                          v22 = 1701733492;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129797479:
                          v21 = v5;
                          LOBYTE(v11) = 15;
                          v22 = 1734438259;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        case 1129797491:
                          v21 = v5;
                          LOBYTE(v11) = 15;
                          v22 = 1937007732;
                          return sub_143CA2E60(v21, v11, v22, a3);
                        default:
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      }
                  }
                }
                switch ( v10 )
                {
                  case 1129796195:
                    v21 = v5;
                    LOBYTE(v11) = 12;
                    goto LABEL_820;
                  case 1129796196:
                  case 1129796198:
                  case 1129796200:
                  case 1129796201:
                  case 1129796202:
                  case 1129796203:
                  case 1129796204:
                  case 1129796205:
                  case 1129796206:
                  case 1129796207:
                  case 1129796208:
                  case 1129796209:
                  case 1129796210:
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  case 1129796197:
                    v21 = v5;
                    LOBYTE(v11) = 12;
                    v22 = 1701733492;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  case 1129796199:
                    v21 = v5;
                    LOBYTE(v11) = 12;
                    v22 = 1734438259;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  case 1129796211:
                    v21 = v5;
                    LOBYTE(v11) = 12;
                    v22 = 1937007732;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  default:
                    switch ( v10 )
                    {
                      case 1129796451:
                        v21 = v5;
                        LOBYTE(v11) = 19;
                        goto LABEL_820;
                      case 1129796453:
                        v21 = v5;
                        LOBYTE(v11) = 19;
                        v22 = 1701733492;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1129796455:
                        v21 = v5;
                        LOBYTE(v11) = 19;
                        v22 = 1734438259;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      case 1129796467:
                        v21 = v5;
                        LOBYTE(v11) = 19;
                        v22 = 1937007732;
                        return sub_143CA2E60(v21, v11, v22, a3);
                      default:
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    }
                }
              }
              if ( v10 <= 1130777706 )
              {
                switch ( v10 )
                {
                  case 1129927523:
                    v21 = v5;
                    LOBYTE(v11) = 27;
                    goto LABEL_820;
                  case 1129927524:
                    v21 = v5;
                    LOBYTE(v11) = 27;
                    v22 = 1937007714;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  case 1129927525:
                  case 1129927526:
                  case 1129927527:
                  case 1129927528:
                  case 1129927529:
                  case 1129927530:
                  case 1129927531:
                  case 1129927532:
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  case 1129927533:
                    v21 = v5;
                    LOBYTE(v11) = 27;
                    v22 = 1937007732;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  case 1129927534:
                    v21 = v5;
                    LOBYTE(v11) = 27;
                    v22 = 1937010285;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  case 1129927535:
                    v21 = v5;
                    LOBYTE(v11) = 27;
                    v22 = 1869899892;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  case 1129927536:
                    v21 = v5;
                    LOBYTE(v11) = 27;
                    v22 = 1937008996;
                    return sub_143CA2E60(v21, v11, v22, a3);
                  default:
                    if ( v10 != 1130590821 )
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    v161 = *(char *)(v5 + 420);
                    v162 = sub_14083D4F0(v12);
                    DWORD2(v442) = v161;
                    *(_QWORD *)&v442 = v162 + 40;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    break;
                }
                goto LABEL_5;
              }
              if ( v10 <= 1130917739 )
              {
                if ( v10 == 1130777707 )
                {
                  v208 = *(_QWORD *)(v5 + 176);
                  if ( v208 != 0
                    && sub_141758910(v208, 0, &unk_141A80850, &unk_141AAA600, 0) != 0
                    && (unsigned __int8)sub_14094B2D0(v5) != 0 )
                  {
                    goto LABEL_1009;
                  }
                  sub_140FE7190(v5, &v442);
                  v3 = (unsigned __int64)&v440;
                  sub_140FEAD00(&v442, &v440);
                  sub_14083DFA0(a3, &v440);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                  (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v442 + 1) + 16LL))(
                    *((_QWORD *)&v442 + 1),
                    (char *)&v442 + 8);
                  LOBYTE(v3) = 1;
                  if ( *(_QWORD *)(v5 + 176) == 0
                    || (unsigned __int8)sub_1409083C0() == 0
                    && (*(_QWORD *)(v5 + 176) == 0 || (unsigned __int8)sub_140968430() == 0) )
                  {
                    return (unsigned int)v3;
                  }
                  v209 = *(_QWORD *)(v5 + 176);
                  v210 = v5;
                  if ( v209 != 0 )
                  {
                    v210 = v5;
                    if ( *(_QWORD *)(v209 + 192) != *(_QWORD *)(v209 + 200) )
                    {
                      v210 = v5;
                      if ( (unsigned __int8)sub_140EBA600(v5) == 0 )
                      {
                        v211 = *(_QWORD *)(v5 + 176);
                        v210 = v5;
                        if ( v211 != 0 )
                        {
                          v212 = 0;
                          if ( *(_QWORD *)(v211 + 192) != *(_QWORD *)(v211 + 200) )
                            v212 = *(_QWORD *)(v5 + 176);
                          v213 = *(__int64 **)(v212 + 192);
                          v210 = v5;
                          if ( *(__int64 **)(v212 + 200) != v213 )
                          {
                            v214 = *v213;
                            if ( v214 == 0 )
                              goto LABEL_1009;
                            v210 = *(_QWORD *)(v214 + 288);
                          }
                        }
                      }
                    }
                  }
                  v215 = *(_QWORD *)(v210 + 176);
                  if ( v215 != 0 )
                    v210 = *(_QWORD *)(v215 + 288);
                  if ( v210 != 0 && v210 != v5 )
                  {
                    v216 = *(_QWORD *)(v210 + 176);
                    if ( v216 != 0
                      && sub_141751B70(*(_QWORD *)(v216 + 424), *(_QWORD *)(v216 + 432), v5) == *(_QWORD *)(v216 + 432) )
                    {
                      sub_140FE7190(v210, &v442);
                      sub_140FEAD00(&v442, &v440);
                      sub_14083DFA0(a3, &v440);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                      (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v442 + 1) + 16LL))(
                        *((_QWORD *)&v442 + 1),
                        (char *)&v442 + 8);
                    }
                  }
                  return (unsigned int)v3;
                }
                if ( v10 == 1130783083 )
                {
                  v219 = sub_14094B2D0(v5);
                  v221 = sub_14083D4F0(v220);
                  BYTE8(v442) = v219;
                  *(_QWORD *)&v442 = v221 + 24;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                if ( v10 != 1130917714 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                v45 = *(_QWORD *)(v5 + 176);
                if ( v45 != 0 )
                {
                  v5 = *(_QWORD *)(v45 + 288);
                  v46 = *(_QWORD *)(v45 + 656);
                  if ( v46 != 0 )
                  {
                    v47 = *(_QWORD *)(v46 + 176);
                    if ( v47 != 0 )
                      v5 = *(_QWORD *)(v47 + 288);
                  }
                  if ( v5 == 0 )
                    goto LABEL_5;
                }
                v48 = *(_QWORD *)(v5 + 184);
                if ( v48 == 0 )
                {
                  v320 = *(_QWORD *)(v5 + 176);
                  if ( v320 != 0 )
                  {
                    LOBYTE(v13) = 1;
                    v321 = sub_1408FF7F0(v320, v5, v13);
                  }
                  else
                  {
                    v321 = *(_QWORD *)(v5 + 168);
                  }
                  LOBYTE(v3) = 1;
                  if ( v321 == 0 )
                    return (unsigned int)v3;
                  v48 = *(_QWORD *)(v321 + 8);
                  if ( v48 == 0 )
                    return (unsigned int)v3;
                }
                goto LABEL_745;
              }
              if ( v10 == 1130917740 )
              {
                sub_1407C9510(&v442);
                v217 = *(_QWORD *)(v5 + 176);
                if ( v217 != 0 )
                  v218 = sub_140908A80();
                else
                  v218 = 0;
                v307 = sub_14083D4F0(v217);
                BYTE8(v440) = v218;
                *(_QWORD *)&v440 = v307 + 24;
                sub_140835380(&v442, 1633907817, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                v309 = *(_QWORD *)(v5 + 176);
                if ( v309 != 0 )
                {
                  LOBYTE(v308) = 1;
                  v310 = (_QWORD *)sub_1408FF7F0(v309, v5, v308);
                }
                else
                {
                  v310 = *(_QWORD **)(v5 + 168);
                }
                if ( v310 != nullptr )
                {
                  sub_140F10C50(v310[1], a3);
                  sub_1408351C0(&v442, 1, a3);
                  sub_140F10C50(v310[2], a3);
                  sub_1408351C0(&v442, 2, a3);
                  sub_140F10C50(v310[3], a3);
                  sub_1408351C0(&v442, 3, a3);
                }
                goto LABEL_906;
              }
              if ( v10 != 1130982756 )
              {
                if ( v10 != 1130984262 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                v71 = *(_QWORD *)(v5 + 176);
                if ( v71 != 0 )
                {
                  v72 = *(unsigned __int8 *)(v71 + 572);
                  v73 = 1;
                  if ( v72 > 0x18 || (v12 = 16785920, !_bittest((const int *)&v12, v72)) )
                  {
                    if ( v72 != 104 )
                      v73 = 0;
                  }
                }
                else
                {
                  v311 = *(unsigned __int8 *)(v5 + 244);
                  LOBYTE(v12) = (_BYTE)v311 == 9;
                  v73 = (_BYTE)v311 == 9 || (_BYTE)v311 == 24;
                }
                goto LABEL_902;
              }
              v222 = *(_QWORD *)(v5 + 176);
              if ( v222 == 0
                || (v12 = *(_QWORD *)(v222 + 288)) == 0
                || *(_QWORD *)(v12 + 96) == 0
                || (v223 = *(unsigned __int8 *)(v222 + 572)) > 0xE
                || (v12 = 16387, !_bittest((const int *)&v12, v223))
                || (unsigned __int8)v223 < 2u )
              {
LABEL_999:
                v349 = sub_14083D4F0(v12);
                BYTE8(v442) = 0;
                *(_QWORD *)&v442 = v349 + 24;
                sub_14083DFA0(a3, &v442);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                goto LABEL_5;
              }
LABEL_751:
              v266 = sub_14083D4F0(v12);
              BYTE8(v442) = 1;
              *(_QWORD *)&v442 = v266 + 24;
              sub_14083DFA0(a3, &v442);
              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
              goto LABEL_5;
            }
            if ( v10 <= 1348694881 )
            {
              if ( v10 <= 1232290114 )
              {
                if ( v10 <= 1131638124 )
                {
                  if ( v10 > 1131367496 )
                  {
                    if ( v10 <= 1131635301 )
                    {
                      if ( v10 <= 1131627880 )
                      {
                        if ( v10 != 1131367497 )
                        {
                          if ( v10 != 1131434608 )
                            return sub_140FE3F20((_DWORD *)v5, v10, a3);
                          if ( (unsigned __int8)sub_1408B4E50(v5, 0, *(_QWORD *)(v5 + 88), 0, 0) != 0 )
                          {
                            v24 = *(char *)(v5 + 392);
                            v25 = sub_14083D4F0(v23);
                            DWORD2(v442) = v24;
                            *(_QWORD *)&v442 = v25 + 40;
                            sub_14083DFA0(a3, &v442);
                            (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                            goto LABEL_5;
                          }
                          goto LABEL_790;
                        }
                        LOBYTE(v3) = 1;
                        if ( *(_QWORD *)(v5 + 176) == 0 )
                          return (unsigned int)v3;
                        if ( (unsigned __int8)sub_1409083C0() == 0 )
                          return (unsigned int)v3;
                        v234 = *(_QWORD *)(v5 + 176);
                        if ( v234 == 0 )
                          return (unsigned int)v3;
                        LOBYTE(v3) = 1;
                        LOBYTE(v232) = -1;
                        LOBYTE(v233) = 1;
                        v235 = sub_140924370(v234, v232, v233);
                        if ( v235 == 0 )
                          return (unsigned int)v3;
                        v236 = v235;
                        sub_1407C9510(&v442);
                        v238 = *(_QWORD *)(v236 + 1984) - *(_QWORD *)(v236 + 1976);
                        if ( v238 != 0 )
                        {
                          v239 = v238 >> 3;
                          v240 = 1;
                          if ( v239 >= 2 )
                            v240 = v239;
                          v241 = 0;
                          v437 = v236;
                          v433 = v240;
                          do
                          {
                            v322 = *(_QWORD *)(*(_QWORD *)(v236 + 1976) + 8 * v241);
                            if ( v322 != 0 )
                            {
                              v323 = *(_QWORD *)(v322 + 8);
                              if ( v323 != 0 )
                              {
                                v324 = *(unsigned __int8 *)(v322 + 39);
                                if ( (_BYTE)v324 != *(_BYTE *)(v322 + 40) )
                                  goto LABEL_951;
                                v325 = v240;
                                *(_QWORD *)&v440 = 0;
                                LOBYTE(v237) = 1;
                                if ( (sub_140928730(*(_QWORD *)(v5 + 176), v323, (unsigned int)&v440, v237, 0) & 0x80u) != 0LL )
                                  goto LABEL_938;
                                v326 = v440;
                                if ( (_QWORD)v440 == 0 )
                                  goto LABEL_938;
                                if ( (v324 = *(_QWORD *)(v5 + 176), (v327 = *(_QWORD *)(v324 + 288)) != 0)
                                  && *(_QWORD *)(v327 + 96) != 0
                                  && (v328 = *(unsigned __int8 *)(v324 + 572)) <= 0xE
                                  && (v329 = 16387, _bittest(&v329, v328))
                                  || (unsigned __int8)sub_140932C50() != 0
                                  || (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, _QWORD, _QWORD, _QWORD))(*(_QWORD *)v326 + 48LL))(
                                       v326,
                                       0,
                                       0,
                                       0,
                                       0) == 0 )
                                {
LABEL_951:
                                  v330 = sub_14083D4F0(v324);
                                  v439[0] = 0;
                                  v438 = v330 + 8;
                                  sub_140F10C50(v323, &v438);
                                  (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *, _BYTE *))(*(_QWORD *)v438 + 24LL))(
                                    v438,
                                    &v438,
                                    v425);
                                  sub_140833C60(&v440, 1416914273, v425);
                                  sub_1407EB3A0(v323, &v434, 1296845164);
                                  sub_140835380(&v440, 1415924076, &v434);
                                  (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v434 + 16LL))(v434, &v434);
                                  sub_14083DC80(&v434, &v440);
                                  sub_14083B5F0(&v442, &v434);
                                  (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v434 + 16LL))(v434, &v434);
                                  sub_140833970(&v440);
                                  (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                                    v438,
                                    &v438);
                                  v236 = v437;
                                  v240 = v433;
                                }
                                else
                                {
LABEL_938:
                                  v240 = v325;
                                  v236 = v437;
                                }
                              }
                            }
                            ++v241;
                          }
                          while ( v240 != v241 );
                        }
                        sub_14083DB80(&v440, &v442);
                        sub_14083DFA0(a3, &v440);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
LABEL_1014:
                        sub_14083B0A0(&v442);
                        return (unsigned int)v3;
                      }
                      if ( v10 == 1131627881 )
                      {
                        LOBYTE(v3) = 1;
                        if ( *(_QWORD *)(v5 + 176) == 0 )
                          return (unsigned int)v3;
                        if ( (unsigned __int8)sub_1409083C0() == 0 )
                          return (unsigned int)v3;
                        v248 = *(_QWORD *)(v5 + 176);
                        if ( v248 == 0 )
                          return (unsigned int)v3;
                        LOBYTE(v3) = 1;
                        LOBYTE(v246) = -1;
                        LOBYTE(v247) = 1;
                        v249 = sub_140924370(v248, v246, v247);
                        if ( v249 == 0 )
                          return (unsigned int)v3;
                        v250 = v249;
                        sub_1407C9510(&v442);
                        v252 = *(_QWORD *)(v250 + 1984) - *(_QWORD *)(v250 + 1976);
                        if ( v252 != 0 )
                        {
                          v253 = v252 >> 3;
                          v254 = 1;
                          if ( v253 >= 2 )
                            v254 = v253;
                          v255 = 0;
                          v437 = v250;
                          v433 = v254;
                          do
                          {
                            v331 = *(_QWORD *)(*(_QWORD *)(v250 + 1976) + 8 * v255);
                            if ( v331 != 0 )
                            {
                              v332 = *(_QWORD *)(v331 + 8);
                              if ( v332 != 0 )
                              {
                                v333 = *(unsigned __int8 *)(v331 + 39);
                                if ( (_BYTE)v333 != *(_BYTE *)(v331 + 40) )
                                  goto LABEL_965;
                                v334 = v254;
                                *(_QWORD *)&v440 = 0;
                                LOBYTE(v251) = 1;
                                if ( (sub_140928730(*(_QWORD *)(v5 + 176), v332, (unsigned int)&v440, v251, 0) & 0x80u) != 0LL )
                                  goto LABEL_952;
                                v335 = v440;
                                if ( (_QWORD)v440 == 0 )
                                  goto LABEL_952;
                                if ( (v333 = *(_QWORD *)(v5 + 176), (v336 = *(_QWORD *)(v333 + 288)) != 0)
                                  && *(_QWORD *)(v336 + 96) != 0
                                  && (v337 = *(unsigned __int8 *)(v333 + 572)) <= 0xE
                                  && (v338 = 16387, _bittest(&v338, v337))
                                  || (unsigned __int8)sub_140932C50() != 0
                                  || (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, _QWORD, _QWORD, _QWORD))(*(_QWORD *)v335 + 48LL))(
                                       v335,
                                       0,
                                       0,
                                       0,
                                       0) == 0 )
                                {
LABEL_965:
                                  v339 = sub_14083D4F0(v333);
                                  v439[0] = 0;
                                  v438 = v339 + 8;
                                  sub_140F10C50(v332, &v438);
                                  (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *, _BYTE *))(*(_QWORD *)v438 + 24LL))(
                                    v438,
                                    &v438,
                                    v426);
                                  sub_140833C60(&v440, 1416914273, v426);
                                  sub_1407EB3A0(v332, &v434, 1299400041);
                                  sub_140835380(&v440, 1415924076, &v434);
                                  (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v434 + 16LL))(v434, &v434);
                                  sub_14083DC80(&v434, &v440);
                                  sub_14083B5F0(&v442, &v434);
                                  (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v434 + 16LL))(v434, &v434);
                                  sub_140833970(&v440);
                                  (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                                    v438,
                                    &v438);
                                  v250 = v437;
                                  v254 = v433;
                                }
                                else
                                {
LABEL_952:
                                  v254 = v334;
                                  v250 = v437;
                                }
                              }
                            }
                            ++v255;
                          }
                          while ( v254 != v255 );
                        }
                        sub_14083DB80(&v440, &v442);
                        sub_14083DFA0(a3, &v440);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                        goto LABEL_1014;
                      }
                      if ( v10 != 1131635058 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
LABEL_469:
                      v126 = sub_140FE8230();
                      LOBYTE(v3) = 1;
                      if ( v126 != 0 )
                      {
                        v127 = v126;
                        if ( v10 > 1131638124 )
                        {
                          if ( v10 > 1131639910 )
                          {
                            v128 = 1416852583;
                            if ( v10 != 1131639911 )
                              v128 = 1416853859;
                          }
                          else if ( v10 == 1131638125 )
                          {
                            v128 = 1416850797;
                          }
                          else
                          {
                            v128 = 1416852067;
                          }
                        }
                        else if ( v10 > 1131635301 )
                        {
                          if ( v10 == 1131635302 )
                            v128 = 1416847974;
                          else
                            v128 = 1416850785;
                        }
                        else if ( v10 == 1131237475 )
                        {
                          v128 = 1416450147;
                        }
                        else
                        {
                          v128 = 1416847730;
                        }
                        sub_140FE7190(v5, &v442);
                        sub_140FEAD00(&v442, &v440);
                        sub_140FE8810(1935893360, &v440);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                        (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v442 + 1) + 16LL))(
                          *((_QWORD *)&v442 + 1),
                          (char *)&v442 + 8);
                        (*(void (__fastcall **)(__int64, _QWORD, __int64 *))(*(_QWORD *)v127 + 16LL))(v127, v128, a3);
                      }
                      return (unsigned int)v3;
                    }
                    if ( v10 > 1131636851 )
                    {
                      if ( v10 != 1131636852 )
                      {
                        if ( v10 != 1131638113 )
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        goto LABEL_469;
                      }
                    }
                    else
                    {
                      if ( v10 == 1131635302 )
                        goto LABEL_469;
                      if ( v10 != 1131636848 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    }
                    v137 = sub_140FE35F0();
                    LOBYTE(v3) = 1;
                    if ( v137 == 0 )
                      return (unsigned int)v3;
                    if ( (*(_BYTE *)(v5 + 417) & 8) != 0 )
                    {
                      v292 = *(_QWORD *)(*(int *)(*(_QWORD *)(v137 + 8) + 8LL) + v137 + 176);
                      if ( v292 == 0 )
                        return (unsigned int)v3;
                      v293 = *(_QWORD *)(v292 + 16);
                      if ( v293 == 0 )
                        return (unsigned int)v3;
                      v138 = *(_QWORD *)(v293 + 16);
                    }
                    else
                    {
                      v138 = sub_141096A40(v137 + 1104);
                    }
                    if ( v138 == 0 || *(_QWORD *)(v5 + 176) == 0 )
                      return (unsigned int)v3;
                    v294 = qword_141B60C30;
                    v437 = v138;
                    if ( qword_141B60C30 == qword_141B60C38 )
                      goto LABEL_1017;
                    v295 = nullptr;
                    while ( *(_DWORD *)v294 != 1937009006 )
                    {
                      v294 += 16;
                      if ( v294 == qword_141B60C38 )
                        goto LABEL_1018;
                    }
                    if ( v294 == qword_141B60C38 )
LABEL_1017:
                      v295 = nullptr;
                    else
                      v295 = *(__int64 **)(v294 + 8);
LABEL_1018:
                    v352 = &qword_141B5A4A0;
                    if ( v295 != nullptr )
                      v352 = v295;
                    v353 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v352 + 64LL))(*v352);
                    v355 = *(_QWORD *)(v5 + 176);
                    if ( (_BYTE)v353 == 0xFF )
                    {
                      if ( v355 == 0 )
                        return (unsigned int)v3;
                      LOBYTE(v354) = -1;
                      v357 = sub_140933C00(v355, v5, v354);
                    }
                    else
                    {
                      LOBYTE(v354) = -1;
                      v356 = sub_1408FA590(v355, v353, v354, 0, 1);
                      if ( v356 == 0 )
                        return (unsigned int)v3;
                      v357 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v356 + 240LL))(v356);
                    }
                    v358 = (_QWORD *)v357;
                    if ( v357 == 0 )
                      return (unsigned int)v3;
                    LODWORD(v440) = 0;
                    sub_140ED19B0(&v442, &v440);
                    if ( v10 == 1131636852 )
                    {
                      v359 = 3;
                      if ( (unsigned __int64)((__int64)(v358[248] - v358[247]) >> 3) < 3 )
                        v359 = (__int64)(v358[248] - v358[247]) >> 3;
                      for ( j = 1; j != 118; ++j )
                      {
                        if ( (j & 0xFFFE) != 0x58 )
                        {
                          sub_140A44CC0(v358, (unsigned int)j, 0);
                          if ( v359 != 0 )
                          {
                            for ( k = 0; k != v359; ++k )
                            {
                              v362 = *(_QWORD **)(v358[247] + 8 * k);
                              if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v362 + 40LL))(v362) != 0
                                && v362[1] == v437 )
                              {
                                LODWORD(v438) = j;
                                sub_140ED1AC0(&v442, &v440, &v438);
                              }
                            }
                          }
                        }
                      }
LABEL_1080:
                      sub_1407C9510(&v440);
                      v378 = *((__int64 **)&v442 + 1);
                      for ( m = **((__int64 ***)&v442 + 1); m != v378; m = (__int64 *)*m )
                      {
                        v380 = *((_DWORD *)m + 4);
                        v381 = sub_14083D4F0(v377);
                        LODWORD(v439[0]) = v380;
                        v438 = v381 + 56;
                        sub_14083B5F0(&v440, &v438);
                        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                          v438,
                          &v438);
                      }
                      sub_14083DB80(&v438, &v440);
                      sub_14083DFA0(a3, &v438);
                      (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                        v438,
                        &v438);
                      sub_14083B0A0(&v440);
                      sub_140EC9B80(&v442);
                      return (unsigned int)v3;
                    }
                    v363 = 3;
                    if ( (unsigned __int64)((__int64)(v358[590] - v358[589]) >> 3) < 3 )
                      v363 = (__int64)(v358[590] - v358[589]) >> 3;
                    v364 = 1;
                    while ( 1 )
                    {
                      if ( (v364 & 0xFFFE) != 0x58 )
                      {
                        sub_141560090(v358, (unsigned int)v364, 0, 0xFFFFFFFFLL);
                        if ( v363 != 0 )
                          break;
                      }
LABEL_1053:
                      if ( ++v364 == 142 )
                        goto LABEL_1080;
                    }
                    v365 = 0;
                    while ( 1 )
                    {
                      v366 = **(unsigned int **)(v358[589] + 8 * v365);
                      if ( (v366 & 0x80000000) == 0LL && qword_141B5FE10 != 0 )
                      {
                        if ( (_BYTE)word_141B60320 == 0 )
                        {
                          v367 = *(_QWORD *)(qword_141B5FE10 + 96);
                          if ( (*(_QWORD *)(qword_141B5FE10 + 104) - v367) >> 3 > v366 )
                          {
                            v368 = (__int64 *)(v367 + 8 * v366);
                            goto LABEL_1068;
                          }
                        }
                        v369 = *(__int64 **)(qword_141B5FE10 + 128);
                        v370 = *v369;
                        v371 = v369[1] - *v369;
                        if ( v371 != 0 && v371 >> 3 > (unsigned __int64)(unsigned int)v366 )
                        {
                          v368 = (__int64 *)(v370 + 8LL * (unsigned int)v366);
LABEL_1068:
                          v372 = *v368;
                          if ( *v368 != 0 )
                          {
                            if ( v364 > 0x23
                              || (v373 = 0x800000088LL, !_bittest64(&v373, v364))
                              || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v372 + 1672LL))(v372) != 0
                              && (v374 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v372 + 1672LL))(v372),
                                  (*(char (__fastcall **)(__int64))(*(_QWORD *)v374 + 808LL))(v374) >= 15) )
                            {
                              v375 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v372 + 672LL))(v372);
                              v376 = *(_BYTE *)(v437 + 47) != 0 ? 0LL : *(_QWORD *)(v437 + 48);
                              if ( v375 == v376
                                && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v372 + 672LL))(v372) != 0
                                || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v372 + 640LL))(v372) == v437
                                && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v372 + 640LL))(v372) != 0 )
                              {
                                LODWORD(v438) = v364;
                                sub_140ED1AC0(&v442, &v440, &v438);
                              }
                            }
                          }
                        }
                      }
                      if ( v363 == ++v365 )
                        goto LABEL_1053;
                    }
                  }
                  if ( v10 <= 1131311212 )
                  {
                    if ( v10 != 1131237475 )
                    {
                      if ( v10 != 1131243876 )
                      {
                        if ( v10 != 1131307884 )
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        if ( qword_141ABD470 == 0 )
                          qword_141ABD470 = sub_1407E4940();
                        v442 = 0;
                        v443 = 0;
                        sub_14090B120(*(_QWORD *)(v5 + 176), &v442, 0);
                        v74 = (__int64)(*((_QWORD *)&v442 + 1) - v442) >> 3;
                        v76 = sub_14083D4F0(v75);
                        *((_QWORD *)&v440 + 1) = v74;
                        *(_QWORD *)&v440 = v76 + 88;
                        sub_14083DFA0(a3, &v440);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                        goto LABEL_804;
                      }
                      v263 = *(_QWORD *)(v5 + 176);
                      if ( v263 == 0
                        || (v264 = *(_QWORD *)(v263 + 288)) == 0
                        || *(_QWORD *)(v264 + 96) == 0
                        || (v265 = *(unsigned __int8 *)(v263 + 572)) > 0xE
                        || (v12 = 16387, !_bittest((const int *)&v12, v265)) )
                      {
                        if ( (unsigned __int8)sub_1400015B0() == 0 )
                          goto LABEL_999;
                        v12 = *(_QWORD *)(v5 + 176);
                        if ( v12 == 0 )
                          goto LABEL_999;
                        v290 = *(_QWORD *)(v12 + 288);
                        if ( v290 == 0 )
                          goto LABEL_999;
                        if ( *(_DWORD *)(v290 + 12) != 100000023 )
                          goto LABEL_999;
                        LOBYTE(v289) = -1;
                        if ( sub_1408FA960(v12, 0, v289, 0) == 0 )
                          goto LABEL_999;
                      }
                      goto LABEL_751;
                    }
                    goto LABEL_469;
                  }
                  if ( v10 > 1131366728 )
                  {
                    if ( v10 == 1131366729 )
                    {
                      v256 = sub_140EBF730(v5);
                      v258 = sub_14083D4F0(v257);
                      BYTE8(v442) = v256;
                      *(_QWORD *)&v442 = v258 + 24;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                    if ( v10 != 1131366740 )
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    LOBYTE(v3) = 1;
                    if ( *(_QWORD *)(v5 + 176) == 0 || (unsigned __int8)sub_1409083C0() == 0 )
                      return (unsigned int)v3;
                    sub_1407C9510(&v442);
                    if ( (unsigned __int8)sub_140EBAEC0(v5, &v442) != 0 )
                    {
                      sub_14083DB80(&v440, &v442);
                      sub_14083DFA0(a3, &v440);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                    }
                    goto LABEL_1014;
                  }
                  if ( v10 == 1131311213 )
                  {
                    v244 = *(_QWORD *)(v5 + 176);
                    if ( v244 != 0 )
                    {
                      DWORD2(v442) = (__int16)sub_1409725C0(v244, 0, 0);
                      *(_QWORD *)&v442 = sub_14083D4F0(v245) + 40;
                    }
                    else
                    {
                      (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                        qword_141B5A4A0,
                        &qword_141B5A4A0,
                        &v442);
                    }
                    if ( &v442 != (__int128 *)a3 )
                    {
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                      (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v442 + 24LL))(v442, &v442, a3);
                    }
                  }
                  else
                  {
                    if ( v10 != 1131311717 )
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    v43 = *(_QWORD *)(v5 + 176);
                    if ( v43 != 0 )
                    {
                      LODWORD(v3) = sub_1409728C0(v43, 0, 0);
                      DWORD2(v442) = (char)v3;
                      *(_QWORD *)&v442 = sub_14083D4F0(v44) + 40;
                    }
                    else
                    {
                      (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                        qword_141B5A4A0,
                        &qword_141B5A4A0,
                        &v442);
                    }
                    if ( &v442 != (__int128 *)a3 )
                    {
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                      (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v442 + 24LL))(v442, &v442, a3);
                    }
                  }
LABEL_900:
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                if ( v10 > 1145392196 )
                {
                  if ( v10 <= 1212892515 )
                  {
                    switch ( v10 )
                    {
                      case 1145392197:
                        v230 = *(_BYTE *)(v5 + 417);
                        v231 = sub_14083D4F0(v12);
                        BYTE8(v442) = (v230 & 2) != 0;
                        *(_QWORD *)&v442 = v231 + 24;
                        sub_14083DFA0(a3, &v442);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                        goto LABEL_5;
                      case 1212367201:
                        v21 = v5;
                        LOBYTE(v11) = 36;
                        v22 = 1635021925;
                        break;
                      case 1212367204:
                        v21 = v5;
                        LOBYTE(v11) = 36;
                        v22 = 1937007732;
                        break;
                      default:
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    }
                    return sub_143CA2E60(v21, v11, v22, a3);
                  }
                  if ( (unsigned int)(v10 - 1212892516) > 0x12 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  v35 = 360961;
                  if ( !_bittest(&v35, v10 - 1212892516) )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  v26 = *(_QWORD *)(v5 + 216);
                  if ( v10 == 1212892532 && v26 == 0 )
                  {
                    v36 = sub_14083D4F0(0);
                    BYTE8(v442) = 0;
                    *(_QWORD *)&v442 = v36 + 24;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    goto LABEL_5;
                  }
                  goto LABEL_213;
                }
                if ( v10 <= 1131639910 )
                {
                  if ( v10 != 1131638125 )
                  {
                    if ( v10 == 1131638899 )
                    {
                      sub_1407C9510(&v442);
                      v267 = *(_QWORD *)(v5 + 176);
                      if ( v267 != 0 )
                      {
                        v268 = *(_QWORD *)(v267 + 296);
                        if ( *(_QWORD *)(v267 + 304) != v268 )
                        {
                          v3 = 0;
                          do
                          {
                            sub_140FE7190(*(_QWORD *)(v268 + 8 * v3), &v440);
                            sub_140FEAD00(&v440, &v438);
                            sub_14083B5F0(&v442, &v438);
                            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                              v438,
                              &v438);
                            (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v440 + 1) + 16LL))(
                              *((_QWORD *)&v440 + 1),
                              (char *)&v440 + 8);
                            ++v3;
                            v269 = *(_QWORD *)(v5 + 176);
                            v268 = *(_QWORD *)(v269 + 296);
                          }
                          while ( v3 < (*(_QWORD *)(v269 + 304) - v268) >> 3 );
                        }
                      }
                      goto LABEL_756;
                    }
                    if ( v10 != 1131639395 )
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  }
                  goto LABEL_469;
                }
                if ( v10 <= 1131704942 )
                {
                  if ( v10 != 1131639911 && v10 != 1131641187 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  goto LABEL_469;
                }
                if ( v10 == 1131704943 )
                {
                  if ( *(_DWORD *)(v5 + 12) == 1301385 )
                  {
                    v259 = sub_14083D4F0(v12);
                    DWORD2(v442) = 1;
                    *(_QWORD *)&v442 = v259 + 40;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  }
                  else if ( (unsigned __int8)sub_140EBF730(v5) != 0 )
                  {
                    v302 = sub_14083D4F0(v301);
                    DWORD2(v442) = 2;
                    *(_QWORD *)&v442 = v302 + 40;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  }
                  else
                  {
                    v344 = *(_QWORD *)(v5 + 96);
                    v345 = *(unsigned __int8 *)(v5 + 244);
                    if ( v344 != 0 || (_BYTE)v345 != 21 )
                    {
                      if ( (_BYTE)v345 == 5 )
                      {
                        v351 = sub_14083D4F0(v345);
                        DWORD2(v442) = 11;
                        *(_QWORD *)&v442 = v351 + 40;
                        sub_14083DFA0(a3, &v442);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      }
                      else
                      {
                        v382 = (unsigned __int8)v345;
                        if ( v344 != 0 )
                        {
                          switch ( (char)v345 )
                          {
                            case 0:
                              v418 = sub_14083D4F0(v345);
                              DWORD2(v442) = 5;
                              *(_QWORD *)&v442 = v418 + 40;
                              sub_14083DFA0(a3, &v442);
                              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                              break;
                            case 1:
                            case 14:
                              if ( *(_BYTE *)(v5 + 418) == 1 )
                              {
                                v383 = sub_14083D4F0(v345);
                                DWORD2(v442) = 6;
                              }
                              else
                              {
                                v383 = sub_14083D4F0(v345);
                                DWORD2(v442) = 7;
                              }
                              *(_QWORD *)&v442 = v383 + 40;
                              sub_14083DFA0(a3, &v442);
                              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                              break;
                            case 2:
                              v419 = sub_14083D4F0(v345);
                              DWORD2(v442) = 8;
                              *(_QWORD *)&v442 = v419 + 40;
                              sub_14083DFA0(a3, &v442);
                              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                              break;
                            case 3:
                              goto LABEL_1163;
                            default:
                              v420 = sub_14083D4F0(v345);
                              DWORD2(v442) = 10;
                              *(_QWORD *)&v442 = v420 + 40;
                              sub_14083DFA0(a3, &v442);
                              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                              break;
                          }
                        }
                        else if ( (unsigned __int8)v345 > 0x16u
                               || (v345 = 6295572, _bittest((const int *)&v345, v382))
                               || v382 != 3 )
                        {
                          v417 = sub_14083D4F0(v345);
                          DWORD2(v442) = 4;
                          *(_QWORD *)&v442 = v417 + 40;
                          sub_14083DFA0(a3, &v442);
                          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                        }
                        else
                        {
LABEL_1163:
                          v421 = sub_14083D4F0(v345);
                          DWORD2(v442) = 9;
                          *(_QWORD *)&v442 = v421 + 40;
                          sub_14083DFA0(a3, &v442);
                          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                        }
                      }
                    }
                    else
                    {
                      v346 = sub_14083D4F0(v345);
                      DWORD2(v442) = 3;
                      *(_QWORD *)&v442 = v346 + 40;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    }
                  }
                  goto LABEL_5;
                }
                if ( v10 != 1131955832 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                sub_1407C9510(&v442);
                v123 = qword_141B60C38;
                v124 = qword_141B60C30;
                if ( qword_141B60C30 != qword_141B60C38 )
                {
                  v125 = qword_141B60C30;
                  while ( *(_DWORD *)v125 != 1416589424 )
                  {
                    v125 += 16;
                    if ( v125 == qword_141B60C38 )
                      goto LABEL_1119;
                  }
                  if ( v125 != qword_141B60C38 && *(_QWORD *)(v125 + 8) != 0 )
                  {
                    v3 = 0;
                    while ( *(_DWORD *)v124 != 1416589424 )
                    {
                      v124 += 16;
                      if ( v124 == qword_141B60C38 )
                        goto LABEL_1116;
                    }
                    if ( v124 == qword_141B60C38 )
                      v3 = 0;
                    else
                      v3 = *(_QWORD *)(v124 + 8);
LABEL_1116:
                    v401 = &qword_141B5A4A0;
                    if ( v3 != 0 )
                      v401 = (__int64 *)v3;
                    v402 = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v401 + 184LL))(
                             *v401,
                             v401,
                             0);
                    sub_14083BFF0(&v442, v402);
                    v123 = qword_141B60C38;
                    v124 = qword_141B60C30;
                  }
LABEL_1119:
                  v403 = nullptr;
                  if ( v124 == v123 )
                  {
LABEL_1126:
                    if ( v403 == nullptr )
                      v403 = &qword_141B5A4A0;
                    v404 = sub_140DBC940();
                    sub_140DBCA60(v404, &v431, v403);
                    v405 = sub_140FE8230();
                    sub_1407C9510(&v440);
                    v437 = v405;
                    if ( v405 != 0 )
                    {
                      v406 = *(_QWORD *)(v5 + 176);
                      if ( v406 != 0 )
                      {
                        sub_1409D4CE0(v406, &v436, v437);
                        if ( v436 != nullptr )
                        {
                          v407 = *v436;
                          if ( v436[1] != *v436 )
                          {
                            v430 = *((_QWORD *)&v442 + 1);
                            v433 = v442;
                            for ( n = 0; n < (__int64)(v436[1] - *v436) >> 3; ++n )
                            {
                              v409 = *(_QWORD *)(v407 + 8 * n);
                              v410 = *(unsigned __int16 *)(v409 + 78);
                              if ( v432 <= (unsigned __int16)v410 )
                              {
                                if ( v432 < (unsigned __int16)v410
                                  || (v410 = *(_WORD *)(v409 + 76) & 0x1FF,
                                      (unsigned __int16)(v431 & 0x1FF) <= (unsigned __int16)v410) )
                                {
                                  if ( v430 != v433 )
                                  {
                                    v411 = *(_QWORD *)(v409 + 8);
                                    if ( v411 == v437 )
                                      v411 = *(_QWORD *)(v409 + 16);
                                    if ( v411 == 0 )
                                      goto LABEL_1133;
                                    v412 = v442;
                                    if ( *((_QWORD *)&v442 + 1) == (_QWORD)v442 )
                                      goto LABEL_1133;
                                    v413 = 0;
                                    while ( 1 )
                                    {
                                      v414 = *(__int64 **)(v412 + 8 * v413);
                                      v415 = sub_14083D4F0(v410);
                                      if ( v414 == nullptr )
                                        v414 = &qword_141B5A4A0;
                                      v439[1] = 0;
                                      v439[0] = v415 + 8;
                                      sub_140FEB270(&v438, v414);
                                      v3 = (unsigned __int64)&v434;
                                      (*(void (__fastcall **)(__int64, _QWORD **))(*(_QWORD *)v411 + 144LL))(
                                        v411,
                                        &v434);
                                      LOBYTE(v3) = sub_140FEB670(&v434, &v438);
                                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v435 + 16LL))(v435, &v435);
                                      if ( (_BYTE)v3 != 0 )
                                        break;
                                      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v439[0] + 16LL))(
                                        v439[0],
                                        v439);
                                      ++v413;
                                      v412 = v442;
                                      v410 = (__int64)(*((_QWORD *)&v442 + 1) - v442) >> 3;
                                      if ( v413 >= v410 )
                                        goto LABEL_1133;
                                    }
                                    sub_140EBE5B0(&v442, &v434, v413);
                                    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v439[0] + 16LL))(
                                      v439[0],
                                      v439);
                                  }
                                  v416 = sub_14083D4F0(v410);
                                  v435 = 0;
                                  v434 = (_QWORD *)(v416 + 8);
                                  v3 = (unsigned __int64)&v434;
                                  (*(void (__fastcall **)(__int64, _QWORD **, _QWORD *))(*(_QWORD *)(v416 + 8) + 24LL))(
                                    v416 + 8,
                                    &v434,
                                    v439);
                                  LODWORD(v438) = -8388609;
                                  (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v434 + 16LL))(v434, &v434);
                                  sub_1414B18A0(v409, &v438);
                                  sub_140FEAD00(&v438, &v434);
                                  sub_14083B5F0(&v440, &v434);
                                  (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v434 + 16LL))(v434, &v434);
                                  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v439[0] + 16LL))(v439[0], v439);
                                }
                              }
LABEL_1133:
                              v407 = *v436;
                            }
                          }
                        }
                        sub_140E359D0(&v436);
                      }
                    }
                    sub_14083DB80(&v438, &v440);
                    sub_14083DFA0(a3, &v438);
                    (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
                    sub_14083B0A0(&v440);
                    goto LABEL_1152;
                  }
                  while ( *(_DWORD *)v124 != 1684108389 )
                  {
                    v124 += 16;
                    if ( v124 == v123 )
                      goto LABEL_1126;
                  }
                  if ( v124 != v123 )
                  {
                    v403 = *(__int64 **)(v124 + 8);
                    goto LABEL_1126;
                  }
                }
                v403 = nullptr;
                goto LABEL_1126;
              }
              if ( v10 <= 1348691040 )
              {
                if ( v10 <= 1330924882 )
                {
                  if ( v10 <= 1296134763 )
                  {
                    if ( v10 <= 1279476064 )
                    {
                      if ( v10 == 1232290115 )
                        goto LABEL_5;
                      if ( v10 != 1279350083 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      v66 = *(char *)(v5 + 423);
                      if ( v66 == -1 )
                        goto LABEL_790;
                      goto LABEL_292;
                    }
                    if ( v10 == 1279476065 )
                    {
                      v21 = v5;
                      LOBYTE(v11) = 37;
                      v22 = 1635021925;
                    }
                    else
                    {
                      if ( v10 != 1279476068 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      v21 = v5;
                      LOBYTE(v11) = 37;
                      v22 = 1937007732;
                    }
                    return sub_143CA2E60(v21, v11, v22, a3);
                  }
                  if ( v10 <= 1299148908 )
                  {
                    if ( v10 == 1296134764 )
                    {
                      LOBYTE(v3) = 1;
                      if ( *(_QWORD *)(v5 + 176) == 0 )
                        return (unsigned int)v3;
                      if ( (unsigned __int8)sub_1409083C0() == 0 )
                        return (unsigned int)v3;
                      if ( (unsigned __int8)sub_140087070() == 0 )
                        return (unsigned int)v3;
                      if ( qword_141B5D2F0 == 0 )
                        return (unsigned int)v3;
                      if ( *(_QWORD *)(qword_141B5D2F0 + 288) != v5 )
                        return (unsigned int)v3;
                      v275 = *(_QWORD *)(qword_141B5D2F0 + 1568);
                      if ( v275 == 0 )
                        return (unsigned int)v3;
                      sub_1407C9510(&v442);
                      v276 = *(_QWORD *)(v275 + 40);
                      v277 = *(_QWORD *)(v275 + 48);
                      if ( v277 != v276 )
                      {
                        v278 = 0;
                        do
                        {
                          v306 = *(_QWORD *)(v276 + 8 * v278);
                          if ( v306 != 0 )
                          {
                            (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v306 + 144LL))(v306, &v440);
                            sub_140FEAD00(&v440, &v438);
                            sub_14083B5F0(&v442, &v438);
                            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                              v438,
                              &v438);
                            (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v440 + 1) + 16LL))(
                              *((_QWORD *)&v440 + 1),
                              (char *)&v440 + 8);
                            v276 = *(_QWORD *)(v275 + 40);
                            v277 = *(_QWORD *)(v275 + 48);
                          }
                          ++v278;
                        }
                        while ( v278 < (v277 - v276) >> 3 );
                      }
                      sub_1407C9510(&v440);
                      sub_14083DB80(&v438, &v442);
                      sub_140835380(&v440, 1296134764, &v438);
                      (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                        v438,
                        &v438);
                      sub_14083DDA0(&v438, &v440);
                      sub_14083DFA0(a3, &v438);
                      (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(
                        v438,
                        &v438);
                      sub_140833970(&v440);
                      goto LABEL_1014;
                    }
                    if ( v10 != 1298559075 )
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    v129 = *(_QWORD *)(v5 + 176);
                    if ( v129 != 0 )
                    {
                      LOBYTE(v13) = 1;
                      DWORD2(v442) = (__int16)sub_1409725C0(v129, 0, v13);
                      *(_QWORD *)&v442 = sub_14083D4F0(v130) + 40;
                    }
                    else
                    {
                      (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                        qword_141B5A4A0,
                        &qword_141B5A4A0,
                        &v442);
                    }
                    if ( &v442 != (__int128 *)a3 )
                    {
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                      (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v442 + 24LL))(v442, &v442, a3);
                    }
                  }
                  else
                  {
                    switch ( v10 )
                    {
                      case 1299148909:
                        v260 = *(_QWORD *)(v5 + 176);
                        if ( v260 != 0 )
                        {
                          LOBYTE(v11) = 1;
                          DWORD2(v442) = (__int16)sub_1409725C0(v260, v11, 0);
                          *(_QWORD *)&v442 = sub_14083D4F0(v261) + 40;
                        }
                        else
                        {
                          (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                            qword_141B5A4A0,
                            &qword_141B5A4A0,
                            &v442);
                        }
                        if ( &v442 != (__int128 *)a3 )
                        {
                          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                          (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v442 + 24LL))(
                            v442,
                            &v442,
                            a3);
                        }
                        break;
                      case 1299149413:
                        v242 = *(_QWORD *)(v5 + 176);
                        if ( v242 != 0 )
                        {
                          LOBYTE(v11) = 1;
                          LODWORD(v3) = sub_1409728C0(v242, v11, 0);
                          DWORD2(v442) = (char)v3;
                          *(_QWORD *)&v442 = sub_14083D4F0(v243) + 40;
                        }
                        else
                        {
                          (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                            qword_141B5A4A0,
                            &qword_141B5A4A0,
                            &v442);
                        }
                        if ( &v442 != (__int128 *)a3 )
                        {
                          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                          (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v442 + 24LL))(
                            v442,
                            &v442,
                            a3);
                        }
                        break;
                      case 1314082628:
LABEL_502:
                        v423 = v10 == 1314082628;
                        LOBYTE(v3) = 1;
                        v77 = v5;
                        LOBYTE(v13) = 1;
                        goto LABEL_503;
                      default:
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    }
                  }
                  goto LABEL_900;
                }
                if ( (unsigned int)(v10 - 1348564016) >= 6 )
                {
                  if ( v10 != 1330924883 )
                  {
                    if ( v10 == 1347184494 )
                    {
                      v41 = *(unsigned __int8 *)(v5 + 245);
                      v42 = sub_14083D4F0(v12);
                      DWORD2(v442) = v41;
                      *(_QWORD *)&v442 = v42 + 40;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  }
                  goto LABEL_331;
                }
LABEL_383:
                if ( a3 != &qword_141B5A4A0 )
                {
                  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                  (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                    qword_141B5A4A0,
                    &qword_141B5A4A0,
                    a3);
                }
                v95 = *(_QWORD *)(v5 + 200);
                LOBYTE(v3) = 1;
                if ( v95 == 0 )
                  return (unsigned int)v3;
                v96 = (char *)sub_14155E670(v95, (unsigned int)v10);
                if ( v96 == nullptr )
                  return (unsigned int)v3;
                LODWORD(v3) = 0;
                if ( v10 <= 1349348911 )
                {
                  v101 = (unsigned int)(v10 - 1348564016);
                  if ( (unsigned int)v101 < 6 )
                  {
                    v104 = v96[4];
                    v7 = sub_14083D4F0(v101) + 24;
                    BYTE8(v442) = v104;
                    *(_QWORD *)&v442 = v7;
                    if ( &v442 != (__int128 *)a3 )
                    {
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                      v105 = *((_QWORD *)&v442 + 1);
                      *(_OWORD *)a3 = v442;
                      v7 = sub_14083D4F0(v105) + 8;
                      v442 = (unsigned __int64)v7;
                    }
                  }
                  else
                  {
                    if ( (unsigned int)(v10 - 1348890928) >= 6 )
                      return (unsigned int)v3;
                    v102 = (unsigned __int8)*v96;
                    v7 = sub_14083D4F0(v101) + 56;
                    DWORD2(v442) = v102;
                    *(_QWORD *)&v442 = v7;
                    if ( &v442 != (__int128 *)a3 )
                    {
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                      v103 = *((_QWORD *)&v442 + 1);
                      *(_OWORD *)a3 = v442;
                      v7 = sub_14083D4F0(v103) + 8;
                      v442 = (unsigned __int64)v7;
                    }
                  }
                }
                else
                {
                  v97 = (unsigned int)(v10 - 1349348912);
                  if ( (unsigned int)v97 < 6 )
                  {
                    v108 = v96[1];
                    v7 = sub_14083D4F0(v97) + 40;
                    DWORD2(v442) = v108;
                    *(_QWORD *)&v442 = v7;
                    if ( &v442 != (__int128 *)a3 )
                    {
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                      v109 = *((_QWORD *)&v442 + 1);
                      *(_OWORD *)a3 = v442;
                      v7 = sub_14083D4F0(v109) + 8;
                      v442 = (unsigned __int64)v7;
                    }
                  }
                  else
                  {
                    v98 = (unsigned int)(v10 - 1349351472);
                    if ( (unsigned int)v98 < 6 )
                    {
                      v106 = v96[2];
                      v7 = sub_14083D4F0(v98) + 40;
                      DWORD2(v442) = v106;
                      *(_QWORD *)&v442 = v7;
                      if ( &v442 != (__int128 *)a3 )
                      {
                        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                        v107 = *((_QWORD *)&v442 + 1);
                        *(_OWORD *)a3 = v442;
                        v7 = sub_14083D4F0(v107) + 8;
                        v442 = (unsigned __int64)v7;
                      }
                    }
                    else
                    {
                      if ( (unsigned int)(v10 - 1349476912) >= 6 )
                        return (unsigned int)v3;
                      v99 = v96[3];
                      v7 = sub_14083D4F0(v98) + 24;
                      BYTE8(v442) = v99;
                      *(_QWORD *)&v442 = v7;
                      if ( &v442 != (__int128 *)a3 )
                      {
                        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                        v100 = *((_QWORD *)&v442 + 1);
                        *(_OWORD *)a3 = v442;
                        v7 = sub_14083D4F0(v100) + 8;
                        v442 = (unsigned __int64)v7;
                      }
                    }
                  }
                }
                goto LABEL_4;
              }
              if ( (unsigned int)(v10 - 1348692577) > 0x18 || (v38 = 17076549, !_bittest(&v38, v10 - 1348692577)) )
              {
                if ( (unsigned int)(v10 - 1348691041) > 0x11 || (v39 = 131105, !_bittest(&v39, v10 - 1348691041)) )
                {
                  if ( v10 != 1348692068 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                }
              }
              return sub_14151EF00(v5 + 393, (unsigned int)v10, a3);
            }
            if ( v10 <= 1349476911 )
            {
              if ( v10 <= 1349348911 )
              {
                v30 = v10 - 1348694882;
                if ( (unsigned int)(v10 - 1348694882) > 0x17 )
                  goto LABEL_382;
                v31 = 8471121;
                if ( _bittest(&v31, v30) )
                  return sub_14151E3B0(v5 + 408, (unsigned int)v10, a3);
                v94 = 131074;
                if ( !_bittest(&v94, v30) )
                {
LABEL_382:
                  if ( (unsigned int)(v10 - 1348890928) < 6 )
                    goto LABEL_383;
                  if ( v10 != 1348695140 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                }
                return sub_14151EF00(v5 + 393, (unsigned int)v10, a3);
              }
              if ( (unsigned int)(v10 - 1349348912) < 6 )
                goto LABEL_383;
              v40 = v10 - 1349351472;
            }
            else
            {
              if ( v10 > 1447121507 )
              {
                if ( v10 > 1633907820 )
                {
                  if ( v10 > 1665558893 )
                  {
                    if ( v10 > 1666336111 )
                    {
                      if ( v10 != 1666336112 )
                      {
                        if ( v10 != 1666348910 )
                          return sub_140FE3F20((_DWORD *)v5, v10, a3);
                        if ( (_BYTE)word_141B60320 == 0 )
                          goto LABEL_1009;
                        sub_1407C9510(&v442);
                        sub_140EBA000(v5, &v436);
                        v131 = v436;
                        if ( v436 != nullptr )
                        {
                          v132 = *v436;
                          v3 = v436[1];
                          v133 = v3 - 160;
                          if ( v3 - *v436 < 0xA1 )
                            v133 = *v436;
                          if ( v133 != v3 )
                          {
                            do
                            {
                              v134 = *(_QWORD *)v133;
                              if ( *(_QWORD *)(*(_QWORD *)v133 + 8LL) != 0 )
                              {
                                v135 = *(__int16 *)(v134 + 84);
                                v136 = sub_14083D4F0(v132);
                                v429 = v135;
                                v428 = v136 + 40;
                                (*(void (__fastcall **)(_QWORD, unsigned __int64 *))(**(_QWORD **)(v134 + 8) + 144LL))(
                                  *(_QWORD *)(v134 + 8),
                                  &v438);
                                v3 = (unsigned __int64)v427;
                                sub_140FEAD00(&v438, v427);
                                sub_140834550(
                                  (unsigned int)&v440,
                                  1416914273,
                                  (unsigned int)v427,
                                  2036687218,
                                  (__int64)&v428);
                                sub_14083DDA0(&v434, &v440);
                                sub_14083B5F0(&v442, &v434);
                                (*(void (__fastcall **)(_QWORD *, _QWORD **))(*v434 + 16LL))(v434, &v434);
                                sub_140833970(&v440);
                                (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v439[0] + 16LL))(v439[0], v439);
                                v131 = v436;
                              }
                              v133 += 8LL;
                            }
                            while ( v133 != v131[1] );
                          }
                        }
                        sub_14083DB80(&v440, &v442);
                        sub_14083DFA0(a3, &v440);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                        sub_140EBA2F0(&v436);
                        goto LABEL_1152;
                      }
LABEL_105:
                      v32 = *(__int16 *)(v5 + 390);
                      v33 = sub_14083D4F0(v12);
                      DWORD2(v442) = v32;
                      *(_QWORD *)&v442 = v33 + 40;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                    if ( v10 != 1665558894 )
                    {
                      if ( v10 != 1666204498 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      v68 = *(_QWORD *)(v5 + 176);
                      if ( v68 != 0 )
                      {
                        v69 = *(_QWORD *)(v68 + 1576);
                        if ( v69 != 0 )
                          v70 = *(_QWORD *)(v69 + 288);
                        else
                          v70 = 0;
                      }
                      else
                      {
                        v70 = 0;
                        if ( *(_QWORD *)(v5 + 104) != v5 )
                          v70 = *(_QWORD *)(v5 + 104);
                      }
                      goto LABEL_979;
                    }
                    v12 = *(_QWORD *)(v5 + 176);
                    if ( v12 != 0 )
                    {
                      LOBYTE(v11) = 1;
                      LOBYTE(v14) = -1;
                      v73 = (*(__int64 (__fastcall **)(__int64, __int64, _QWORD, __int64, char, char, _BYTE, _QWORD))(*(_QWORD *)v12 + 360LL))(
                              v12,
                              v11,
                              0,
                              v14,
                              1,
                              1,
                              0,
                              0);
                    }
                    else
                    {
                      v73 = 0;
                    }
LABEL_902:
                    v312 = sub_14083D4F0(v12);
                    BYTE8(v442) = v73;
                    *(_QWORD *)&v442 = v312 + 24;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    goto LABEL_5;
                  }
                  if ( v10 > 1664314477 )
                  {
                    if ( v10 != 1664314478 )
                    {
                      if ( v10 != 1665363794 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      v70 = *(_QWORD *)(v5 + 88);
                      goto LABEL_979;
                    }
                    v284 = (_OWORD *)(v5 + 80);
                    v59 = sub_14083D4F0(v12);
                    *((_QWORD *)&v442 + 1) = 0;
                    if ( (__int128 *)((char *)&v442 + 8) != v284 )
                    {
                      v285 = *(_QWORD *)v284;
                      if ( *(_QWORD *)v284 != 0 )
                        _InterlockedIncrement((volatile signed __int32 *)(v285 - 4));
                      *((_QWORD *)&v442 + 1) = v285;
                    }
LABEL_787:
                    *(_QWORD *)&v442 = v59 + 136;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    goto LABEL_5;
                  }
                  if ( v10 != 1633907821 )
                  {
                    if ( v10 != 1651204972 )
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    goto LABEL_416;
                  }
                  v279 = *(_QWORD *)(v5 + 176);
                  sub_1407C9510(&v442);
                  if ( v279 != 0 )
                  {
                    if ( qword_141ABD470 == 0 )
                      qword_141ABD470 = sub_1407E4940();
                    v440 = 0;
                    v441 = 0;
                    sub_14090B120(v279, &v440, 0);
                    v280 = *((_QWORD *)&v440 + 1);
                    if ( *((_QWORD *)&v440 + 1) != (_QWORD)v440 )
                    {
                      sub_140893BE0(&v442, (__int64)(*((_QWORD *)&v440 + 1) - v440) >> 3);
                      v280 = *((_QWORD *)&v440 + 1);
                      if ( *((_QWORD *)&v440 + 1) != (_QWORD)v440 )
                      {
                        v281 = 0;
                        do
                        {
                          v3 = sub_140ECAC40(16);
                          v283 = sub_14083D4F0(v282);
                          *(_QWORD *)(v3 + 8) = 0;
                          *(_QWORD *)v3 = v283 + 8;
                          v438 = v3;
                          sub_14087F540(&v442, &v438);
                          sub_140F10C50(*(_QWORD *)(v440 + 8 * v281), *(_QWORD *)(v442 + 8 * v281));
                          ++v281;
                          v280 = v440;
                        }
                        while ( v281 < (__int64)(*((_QWORD *)&v440 + 1) - v440) >> 3 );
                      }
                    }
                    if ( v280 != 0 )
                      sub_1407E4890(qword_141ABD470, v280, v441 - v280);
                  }
                  goto LABEL_756;
                }
                if ( (unsigned int)(v10 - 1447121508) > 0x12
                  || (v12 = 360965, !_bittest((const int *)&v12, v10 - 1447121508)) )
                {
                  if ( v10 != 1466974830 )
                  {
                    if ( v10 == 1633907779 )
                    {
                      v91 = *(_QWORD **)(v5 + 176);
                      if ( v91 != nullptr
                        && (v12 = v91[115] | v91[116], *(_OWORD *)(v91 + 115) == 0)
                        && (v92 = v91[66]) != 0 )
                      {
                        v93 = (__int64)(*(_QWORD *)(v92 + 1984) - *(_QWORD *)(v92 + 1976)) >> 3;
                      }
                      else
                      {
                        v93 = 0;
                      }
                      v291 = sub_14083D4F0(v12);
                      *((_QWORD *)&v442 + 1) = v93;
                      *(_QWORD *)&v442 = v291 + 88;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  }
                  if ( *(_QWORD *)(v5 + 96) != 0 )
                  {
                    v270 = *(unsigned __int8 *)(v5 + 244);
                    if ( v270 <= 0xE )
                    {
                      v271 = 16387;
                      if ( _bittest(&v271, v270) )
                      {
                        v272 = (unsigned __int8)(sub_140EC9C30(v5) + 1);
                        v274 = sub_14083D4F0(v273);
                        DWORD2(v442) = v272;
                        *(_QWORD *)&v442 = v274 + 40;
                        sub_14083DFA0(a3, &v442);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                        goto LABEL_5;
                      }
                    }
                  }
                  goto LABEL_790;
                }
                v26 = *(_QWORD *)(v5 + 208);
                if ( v10 == 1447121524 && v26 == 0 )
                {
                  v27 = sub_14083D4F0(0);
                  DWORD2(v442) = 5;
                  *(_QWORD *)&v442 = v27 + 40;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
LABEL_213:
                if ( v26 != 0 )
                  return sub_140EB60C0(v26, (unsigned int)v10, a3);
                goto LABEL_790;
              }
              if ( v10 > 1383287855 )
              {
                switch ( v10 )
                {
                  case 1383287856:
                    v37 = v5;
                    v13 = 0;
                    goto LABEL_742;
                  case 1383287857:
                    LOBYTE(v3) = 1;
                    LOBYTE(v13) = 1;
                    sub_141563520(&v442, v5, v13);
                    sub_140ECA610(&v442, a3);
                    goto LABEL_505;
                  case 1383287858:
                    v37 = v5;
                    LOBYTE(v13) = 2;
                    goto LABEL_742;
                  case 1383287859:
                    v37 = v5;
                    LOBYTE(v13) = 3;
                    goto LABEL_742;
                  case 1383287860:
                    v37 = v5;
                    LOBYTE(v13) = 4;
                    goto LABEL_742;
                  case 1383287861:
                    v37 = v5;
                    LOBYTE(v13) = 5;
                    goto LABEL_742;
                  default:
                    if ( v10 == 1415014509 )
                    {
                      sub_1407C9510(&v442);
                      LOBYTE(v438) = 0;
                      LOBYTE(v434) = 0;
                      sub_140EBB2B0(v5, &v438, &v434);
                      v224 = (char)v438;
                      v226 = sub_14083D4F0(v225);
                      DWORD2(v440) = v224;
                      *(_QWORD *)&v440 = v226 + 40;
                      sub_140833EB0(&v442, 1145333874, &v440);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                      v227 = (char)v434;
                      v229 = sub_14083D4F0(v228);
                      DWORD2(v440) = v227;
                      *(_QWORD *)&v440 = v229 + 40;
                      sub_140833EB0(&v442, 1145335150, &v440);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                      sub_14083DDA0(&v440, &v442);
                      sub_14083DFA0(a3, &v440);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                      goto LABEL_907;
                    }
                    if ( v10 != 1447117651 )
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    v89 = *(_DWORD *)(v5 + 12);
                    if ( v89 > 102413 )
                    {
                      if ( v89 > 1301384 )
                      {
                        v305 = v89 - 1301385;
                        if ( v305 > 5 )
                          goto LABEL_999;
                        v12 = 57;
                        if ( !_bittest((const int *)&v12, v305) )
                          goto LABEL_999;
                        goto LABEL_751;
                      }
                      if ( v89 == 102414 || v89 == 145509 || v89 == 147032 )
                        goto LABEL_751;
                    }
                    else
                    {
                      v12 = (unsigned int)(v89 - 100100);
                      if ( (unsigned int)v12 <= 9 )
                      {
                        v90 = 575;
                        if ( _bittest(&v90, v12) )
                          goto LABEL_751;
                      }
                      if ( v89 == 102412 )
                        goto LABEL_751;
                    }
                    break;
                }
                goto LABEL_999;
              }
              v40 = v10 - 1349476912;
            }
            if ( v40 >= 6 )
              return sub_140FE3F20((_DWORD *)v5, v10, a3);
            goto LABEL_383;
          }
          if ( v10 > 1835954274 )
            break;
          if ( v10 <= 1751609442 )
          {
            if ( v10 > 1668183144 )
            {
              if ( v10 > 1668509556 )
              {
                if ( v10 > 1668641645 )
                {
                  if ( v10 <= 1684173944 )
                  {
                    if ( v10 == 1668641646 )
                    {
                      v201 = *(_BYTE *)(v5 + 417) & 1;
                      v202 = sub_14083D4F0(v12);
                      BYTE8(v442) = v201;
                      *(_QWORD *)&v442 = v202 + 24;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                    if ( v10 != 1668769139 )
                    {
                      if ( v10 == 1683177847 )
                      {
                        v28 = *(_BYTE *)(v5 + 245);
                        v29 = sub_14083D4F0(v12);
                        BYTE8(v442) = v28;
                        *(_QWORD *)&v442 = v29 + 24;
                        sub_14083DFA0(a3, &v442);
                        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                        goto LABEL_5;
                      }
                      return sub_140FE3F20((_DWORD *)v5, v10, a3);
                    }
                    v57 = *(_QWORD *)(v5 + 144);
                    goto LABEL_674;
                  }
                  if ( v10 != 1684173945 )
                  {
                    if ( v10 != 1684303986 )
                    {
                      if ( v10 != 1717792620 )
                        return sub_140FE3F20((_DWORD *)v5, v10, a3);
                      goto LABEL_419;
                    }
                    sub_1407C9510(&v442);
                    v205 = sub_14083D4F0(v204);
                    DWORD2(v440) = 1668444275;
                    *(_QWORD *)&v440 = v205 + 56;
                    sub_14083B5F0(&v442, &v440);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                    v207 = sub_14083D4F0(v206);
                    DWORD2(v440) = 1668178292;
                    *(_QWORD *)&v440 = v207 + 56;
                    sub_14083B5F0(&v442, &v440);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                    sub_14083DB80(&v440, &v442);
                    sub_14083DFA0(a3, &v440);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
LABEL_1152:
                    sub_14083B0A0(&v442);
                    goto LABEL_5;
                  }
                  v66 = *(char *)(v5 + 244);
                  if ( v66 == -1 )
                    goto LABEL_790;
LABEL_292:
                  v67 = sub_14083D4F0(v12);
                  DWORD2(v442) = v66;
                  *(_QWORD *)&v442 = v67 + 40;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                if ( v10 <= 1668572011 )
                {
                  if ( v10 != 1668509557 )
                  {
                    if ( v10 == 1668510575 )
                    {
                      v121 = *(_BYTE *)(v5 + 248);
                      v122 = sub_14083D4F0(v12);
                      BYTE8(v442) = v121;
                      *(_QWORD *)&v442 = v122 + 24;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  }
                  v57 = *(_QWORD *)(v5 + 136);
                  goto LABEL_674;
                }
                if ( v10 == 1668572012 )
                {
                  v203 = sub_141335F60();
                  DWORD2(v442) = *(_DWORD *)(v5 + 296);
                  *(_QWORD *)&v442 = v203;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                if ( v10 != 1668574579 )
                {
                  if ( v10 == 1668637029 )
                  {
                    v61 = *(_BYTE *)(v5 + 247);
                    v62 = sub_14083D4F0(v12);
                    BYTE8(v442) = v61;
                    *(_QWORD *)&v442 = v62 + 24;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    goto LABEL_5;
                  }
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                }
LABEL_337:
                v424 = v10 == 1129598291;
                v422 = 0;
LABEL_803:
                sub_141561880((unsigned int)&v442, v5, 0, 0, v422, v424);
                sub_140ECA230(&v442, a3);
                goto LABEL_804;
              }
              if ( v10 <= 1668441455 )
              {
                if ( v10 > 1668246895 )
                {
                  if ( v10 != 1668246896 )
                  {
                    if ( v10 == 1668248434 )
                    {
                      v190 = *(char *)(v5 + 249);
                      v191 = sub_14083D4F0(v12);
                      if ( v190 == -1 )
                      {
                        DWORD2(v442) = 1314212940;
                        *(_QWORD *)&v442 = v191 + 56;
                      }
                      else
                      {
                        DWORD2(v442) = v190;
                        *(_QWORD *)&v442 = v191 + 40;
                      }
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                    if ( v10 == 1668309869 )
                    {
                      sub_140FE75A0(*(_QWORD *)(v5 + 104), a3);
                      goto LABEL_5;
                    }
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  }
                  v70 = v5;
LABEL_979:
                  sub_140F10C50(v70, a3);
                  goto LABEL_5;
                }
                if ( v10 == 1668183145 )
                {
                  sub_140FCC110(*(_QWORD *)(v5 + 96), a3);
                  goto LABEL_5;
                }
                if ( v10 != 1668183149 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
LABEL_447:
                LOBYTE(v3) = 1;
                LOBYTE(v13) = 1;
                sub_141561880((unsigned int)&v442, v5, v13, 0, 0, v10 == 1129206861);
                goto LABEL_504;
              }
              if ( v10 <= 1668444274 )
              {
                if ( v10 == 1668441456 )
                {
                  v199 = *(__int16 *)(v5 + 384);
                  v200 = sub_14083D4F0(v12);
                  DWORD2(v442) = v199;
                  *(_QWORD *)&v442 = v200 + 40;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                if ( v10 == 1668441972 )
                {
                  *(_QWORD *)&v442 = v5;
                  *(_QWORD *)&v440 = &v442;
                  sub_140ED2390(&v440, a3);
                  goto LABEL_5;
                }
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              }
              if ( v10 != 1668444275 )
              {
                if ( v10 == 1668505968 )
                {
                  sub_141561480(&v442, v5);
                  sub_140EC9E70(&v442, a3);
                  goto LABEL_804;
                }
                if ( v10 != 1668509293 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                v58 = (_OWORD *)(v5 + 72);
                v59 = sub_14083D4F0(v12);
                *((_QWORD *)&v442 + 1) = 0;
                if ( (__int128 *)((char *)&v442 + 8) != v58 )
                {
                  v60 = *(_QWORD *)v58;
                  if ( *(_QWORD *)v58 != 0 )
                    _InterlockedIncrement((volatile signed __int32 *)(v60 - 4));
                  *((_QWORD *)&v442 + 1) = v60;
                }
                goto LABEL_787;
              }
              sub_1407C9510(&v442);
              if ( *(_DWORD *)(v5 + 12) == 100000023 )
              {
                v186 = sub_14083D4F0(v185);
                DWORD2(v440) = 20;
                *(_QWORD *)&v440 = v186 + 40;
                sub_140833EB0(&v442, 1986096245, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                v188 = sub_14083D4F0(v187);
                DWORD2(v440) = 200;
                *(_QWORD *)&v440 = v188 + 40;
                sub_140833EB0(&v442, 1936880751, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
              }
              else
              {
                v296 = 11;
                if ( (__int16)(int)(float)((float)((float)*(__int16 *)(v5 + 384) * MEMORY[0x1417AB7C8])
                                         + MEMORY[0x141775530]) >= 12 )
                  v296 = (int)(float)((float)((float)*(__int16 *)(v5 + 384) * MEMORY[0x1417AB7C8]) + MEMORY[0x141775530]);
                v297 = sub_14083D4F0(v185);
                DWORD2(v440) = v296;
                *(_QWORD *)&v440 = v297 + 40;
                sub_140833EB0(&v442, 1986096245, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                v298 = *(__int16 *)(v5 + 384);
                v300 = sub_14083D4F0(v299);
                DWORD2(v440) = v298;
                *(_QWORD *)&v440 = v300 + 40;
                sub_140833EB0(&v442, 1936880751, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
              }
LABEL_906:
              sub_14083DDA0(&v440, &v442);
              sub_14083DFA0(a3, &v440);
              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
              goto LABEL_907;
            }
            if ( v10 <= 1667789683 )
            {
              if ( v10 <= 1667462248 )
              {
                if ( v10 <= 1667326816 )
                {
                  if ( v10 == 1666475105 )
                  {
                    LODWORD(v440) = 124518401;
                    v194 = sub_140EBB440(v5, 0);
                    if ( v194 != 0 )
                    {
                      v195 = v194;
                      v196 = *(unsigned __int8 *)(v194 + 86);
                      if ( v196 != 9 && v196 != 38 )
                      {
                        v197 = HIWORD(dword_141AAE084);
                        sub_140AF9070(&v438, HIWORD(dword_141AAE084));
                        WORD2(v442) = *(_WORD *)(v195 + 30);
                        LODWORD(v442) = *(_DWORD *)(v195 + 26);
                        sub_14135B130(&v442, &v440, &v438, v197);
                      }
                    }
                    v198 = sub_140DBC940();
                    LODWORD(v3) = ((v440 & 0x1FF) << 8) | ((unsigned __int16)v440 >> 9) | (WORD1(v440) << 17);
                    DWORD2(v442) = v3;
                    *(_QWORD *)&v442 = v198;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    goto LABEL_5;
                  }
                  if ( v10 != 1666475124 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  LOBYTE(v11) = 1;
                  v111 = sub_140EBB440(v5, v11);
                  if ( v111 != 0 )
                    v66 = *(__int16 *)(v111 + 72);
                  else
                    v66 = 2400;
                  goto LABEL_292;
                }
                if ( v10 != 1667326817 )
                {
                  if ( v10 == 1667392364 )
                  {
                    v189 = sub_141335F60();
                    DWORD2(v442) = *(_DWORD *)(v5 + 292);
                    *(_QWORD *)&v442 = v189;
                    sub_14083DFA0(a3, &v442);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                    goto LABEL_5;
                  }
                  if ( v10 != 1667461744 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  goto LABEL_105;
                }
                v12 = *(_QWORD *)(v5 + 176);
                if ( v12 != 0 )
                  v73 = sub_1409083C0();
                else
                  v73 = 0;
                goto LABEL_902;
              }
              if ( v10 <= 1667588466 )
              {
                if ( v10 == 1667462249 )
                {
                  sub_140FE7860(*(_QWORD *)(v5 + 88), a3);
                  goto LABEL_5;
                }
                if ( v10 != 1667524966 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                sub_1407C9510(&v442);
                v114 = *(__int16 *)(v5 + 388) - *(__int16 *)(v5 + 390);
                v116 = sub_14083D4F0(v115);
                DWORD2(v440) = v114;
                *(_QWORD *)&v440 = v116 + 40;
                sub_140833EB0(&v442, 1986096245, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                v118 = sub_14083D4F0(v117);
                *((_QWORD *)&v440 + 1) = 0;
                v119 = qword_141B59EE0;
                if ( qword_141B59EE0 != 0 )
                  _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
                *((_QWORD *)&v440 + 1) = v119;
                *(_QWORD *)&v440 = v118 + 136;
                sub_140833EB0(&v442, 1952807028, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                sub_14083DDA0(&v440, &v442);
                sub_14083DFA0(a3, &v440);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                goto LABEL_907;
              }
              if ( v10 != 1667588467 )
              {
                if ( v10 == 1667594356 )
                {
                  v192 = *(_BYTE *)(v5 + 417);
                  v193 = sub_14083D4F0(v12);
                  BYTE8(v442) = (v192 & 4) != 0;
                  *(_QWORD *)&v442 = v193 + 24;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                if ( v10 == 1667654508 )
                {
                  v56 = sub_141335F60();
                  DWORD2(v442) = *(_DWORD *)(v5 + 288);
                  *(_QWORD *)&v442 = v56;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              }
              v57 = *(_QWORD *)(v5 + 152);
LABEL_674:
              sub_140FE76A0(v57, a3);
              goto LABEL_5;
            }
            if ( v10 > 1668118635 )
            {
              if ( v10 > 1668178284 )
              {
                if ( v10 == 1668178285 )
                {
                  v183 = (_OWORD *)(v5 + 64);
                  v59 = sub_14083D4F0(v12);
                  *((_QWORD *)&v442 + 1) = 0;
                  if ( (__int128 *)((char *)&v442 + 8) != v183 )
                  {
                    v184 = *(_QWORD *)v183;
                    if ( *(_QWORD *)v183 != 0 )
                      _InterlockedIncrement((volatile signed __int32 *)(v184 - 4));
                    *((_QWORD *)&v442 + 1) = v184;
                  }
                  goto LABEL_787;
                }
                if ( v10 == 1668178292 )
                {
LABEL_501:
                  v70 = *(_QWORD *)(v5 + 96);
                  goto LABEL_979;
                }
                if ( v10 != 1668181874 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                v57 = *(_QWORD *)(v5 + 128);
                goto LABEL_674;
              }
              if ( v10 == 1668118636 )
              {
                v120 = (float)*(__int16 *)(v5 + 344) / MEMORY[0x141775530];
                if ( v120 > MEMORY[0x141759000] )
                  goto LABEL_856;
              }
              else
              {
                if ( v10 != 1668118647 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
                v120 = (float)*(__int16 *)(v5 + 346) / MEMORY[0x141775530];
                if ( v120 > MEMORY[0x141759000] )
                  goto LABEL_856;
              }
            }
            else
            {
              if ( v10 <= 1668116075 )
              {
                if ( v10 == 1667789684 )
                {
                  sub_141563A40(&v442, v5);
                  sub_140ECAD50(&v442, a3);
                  goto LABEL_804;
                }
                if ( v10 != 1668051568 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
LABEL_426:
                v112 = *(__int16 *)(v5 + 388);
                v113 = sub_14083D4F0(v12);
                DWORD2(v442) = v112;
                *(_QWORD *)&v442 = v113 + 40;
                sub_14083DFA0(a3, &v442);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                goto LABEL_5;
              }
              switch ( v10 )
              {
                case 1668116076:
                  v120 = (float)*(__int16 *)(v5 + 340) / MEMORY[0x141775530];
                  if ( v120 > MEMORY[0x141759000] )
                    goto LABEL_856;
                  break;
                case 1668116087:
                  v120 = (float)*(__int16 *)(v5 + 342) / MEMORY[0x141775530];
                  if ( v120 > MEMORY[0x141759000] )
                    goto LABEL_856;
                  break;
                case 1668117603:
LABEL_223:
                  v49 = *(_QWORD *)(qword_141B5AD60 + 72);
                  if ( v49 != 0 )
                  {
                    v50 = *(unsigned int *)(v5 + 8);
                    LODWORD(v3) = 0;
                    if ( (int)v50 < 0 )
                      return (unsigned int)v3;
                    v51 = *(__int64 **)(v49 + 56);
                    if ( (int)v50 >= *((_DWORD *)v51 + 2) )
                      return (unsigned int)v3;
                    v52 = *v51;
                    if ( v52 != 0 )
                    {
                      v53 = (v50 << 6) + v52;
                      v54 = *(__int16 *)(v53 + 2LL * (v10 != 1668117603) + 24);
                      v55 = sub_14083D4F0(v53);
                      DWORD2(v442) = v54;
                      *(_QWORD *)&v442 = v55 + 40;
                      sub_14083DFA0(a3, &v442);
                      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                      goto LABEL_5;
                    }
                  }
                  goto LABEL_1009;
                default:
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
              }
            }
LABEL_790:
            LOBYTE(v3) = 1;
            if ( a3 != &qword_141B5A4A0 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                qword_141B5A4A0,
                &qword_141B5A4A0,
                a3);
            }
            return (unsigned int)v3;
          }
          if ( v10 <= 1818588779 )
          {
            if ( v10 != 1751609443 )
            {
              if ( v10 != 1817331056 )
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              goto LABEL_426;
            }
            a2 = 1751936871;
          }
          else
          {
            if ( v10 != 1835167843 )
            {
              if ( v10 == 1818588780 )
              {
                v286 = *(char *)(v5 + 418);
                if ( v286 != 100 )
                {
                  v303 = sub_14083D4F0(v12);
                  DWORD2(v442) = v286 + 1;
                  *(_QWORD *)&v442 = v303 + 40;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                goto LABEL_790;
              }
              if ( v10 != 1818848875 )
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              v78 = *(_QWORD *)(v5 + 176);
              if ( v78 == 0
                || sub_141758910(v78, 0, &unk_141A80850, &unk_141AAA600, 0) != 0
                && (unsigned __int8)sub_14094B2D0(v5) != 0
                || *(_QWORD *)(v5 + 176) == 0
                || (unsigned __int8)sub_1409083C0() == 0
                && (*(_QWORD *)(v5 + 176) == 0 || (unsigned __int8)sub_140968430() == 0) )
              {
                goto LABEL_1009;
              }
              sub_1407C9510(&v442);
              v79 = *(_QWORD *)(v5 + 176);
              v80 = v5;
              if ( v79 != 0 )
              {
                v80 = v5;
                if ( *(_QWORD *)(v79 + 192) != *(_QWORD *)(v79 + 200) )
                {
                  v80 = v5;
                  if ( (unsigned __int8)sub_140EBA600(v5) == 0 )
                  {
                    v81 = *(_QWORD *)(v5 + 176);
                    v80 = v5;
                    if ( v81 != 0 )
                    {
                      v82 = 0;
                      if ( *(_QWORD *)(v81 + 192) != *(_QWORD *)(v81 + 200) )
                        v82 = *(_QWORD *)(v5 + 176);
                      v83 = *(__int64 **)(v82 + 192);
                      v80 = v5;
                      if ( *(__int64 **)(v82 + 200) != v83 )
                      {
                        v84 = *v83;
                        if ( v84 == 0 )
                        {
                          LODWORD(v3) = 0;
LABEL_364:
                          sub_140833970(&v442);
                          return (unsigned int)v3;
                        }
                        v80 = *(_QWORD *)(v84 + 288);
                      }
                    }
                  }
                }
              }
              v85 = *(_QWORD *)(v80 + 176);
              if ( v85 != 0 )
                v80 = *(_QWORD *)(v85 + 288);
              if ( v80 != 0 && v80 != v5 )
              {
                v86 = *(_QWORD *)(v80 + 176);
                if ( v86 != 0
                  && sub_141751B70(*(_QWORD *)(v86 + 424), *(_QWORD *)(v86 + 432), v5) == *(_QWORD *)(v86 + 432) )
                {
                  v3 = (unsigned __int64)&v440;
                  sub_140FE7190(v80, &v440);
                  sub_140FEAD00(&v440, &v438);
                  sub_140835380(&v442, 1868720756, &v438);
                  (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
                  (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v440 + 1) + 16LL))(
                    *((_QWORD *)&v440 + 1),
                    (char *)&v440 + 8);
                  v88 = sub_14083D4F0(v87);
                  DWORD2(v440) = 1668510576;
                  *(_QWORD *)&v440 = v88 + 56;
                  sub_140835380(&v442, 1936024436, &v440);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                  sub_140FE7190(v5, &v440);
                  sub_140FEAD00(&v440, &v438);
                  sub_140835380(&v442, 1398952803, &v438);
                  (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
                  (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v440 + 1) + 16LL))(
                    *((_QWORD *)&v440 + 1),
                    (char *)&v440 + 8);
                }
              }
              sub_14083DDA0(&v440, &v442);
              sub_14083DFA0(a3, &v440);
              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
              LOBYTE(v3) = 1;
              goto LABEL_364;
            }
            a2 = 1819043682;
          }
        }
        if ( v10 <= 1935894115 )
          break;
        if ( v10 > 1936933736 )
        {
          if ( v10 <= 1937329527 )
          {
            if ( v10 <= 1937072755 )
            {
              if ( v10 > 1936936296 )
              {
                if ( v10 != 1936936297 && v10 != 1936936312 )
                  return sub_140FE3F20((_DWORD *)v5, v10, a3);
              }
              else if ( v10 != 1936933737 && v10 != 1936933752 )
              {
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              }
              goto LABEL_520;
            }
            if ( v10 > 1937326967 )
            {
              if ( v10 != 1937326968 && v10 != 1937329513 )
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              goto LABEL_520;
            }
            if ( v10 != 1937072756 )
            {
              if ( v10 != 1937326953 )
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              goto LABEL_520;
            }
            sub_1407C9510(&v442);
            sub_1407C9510(&v440);
            v166 = sub_14083D4F0(v165);
            LODWORD(v439[0]) = 1128686418;
            v438 = v166 + 56;
            v3 = (unsigned __int64)&v438;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            v168 = sub_14083D4F0(v167);
            LODWORD(v439[0]) = 1128686425;
            v438 = v168 + 56;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            v170 = sub_14083D4F0(v169);
            LODWORD(v439[0]) = 1130917491;
            v438 = v170 + 56;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            v172 = sub_14083D4F0(v171);
            LODWORD(v439[0]) = 1128821620;
            v438 = v172 + 56;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            v174 = sub_14083D4F0(v173);
            LODWORD(v439[0]) = 1129084754;
            v438 = v174 + 56;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            v176 = sub_14083D4F0(v175);
            LODWORD(v439[0]) = 1131366729;
            v438 = v176 + 56;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            sub_1407EAFE0(v5, &v442, &v440);
            sub_14083DDA0(&v438, &v442);
            sub_14083DFA0(a3, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
          }
          else
          {
            if ( v10 <= 1953068139 )
            {
              if ( v10 > 1937331063 )
              {
                if ( v10 != 1937331064 )
                {
                  if ( v10 != 1952605036 )
                    return sub_140FE3F20((_DWORD *)v5, v10, a3);
                  goto LABEL_416;
                }
              }
              else if ( v10 != 1937329528 && v10 != 1937331049 )
              {
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              }
LABEL_520:
              v140 = sub_14083D4F0(v12) + 40;
              DWORD2(v442) = -1;
              *(_QWORD *)&v442 = v140;
              if ( &v442 != (__int128 *)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                v141 = *((_QWORD *)&v442 + 1);
                *(_OWORD *)a3 = v442;
                v140 = sub_14083D4F0(v141) + 8;
                v442 = (unsigned __int64)v140;
              }
              v3 = *(_QWORD *)v140;
              (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v140 + 16LL))(v140, &v442);
              v142 = *(_QWORD *)(v5 + 192);
              if ( v142 == 0 )
                goto LABEL_989;
              if ( v10 > 1936936296 )
              {
                if ( v10 > 1937326952 )
                {
                  v143 = 3;
LABEL_536:
                  v144 = *(__int64 ***)v142;
                  v3 = *(_QWORD *)(v142 + 8);
                  while ( 1 )
                  {
                    if ( v144 == (__int64 **)v3 )
                      goto LABEL_987;
                    v145 = *v144;
                    if ( *v144 != nullptr && *((_BYTE *)v145 + 24) == v143 )
                      break;
                    ++v144;
                  }
                  if ( v144 == (__int64 **)v3 )
                    goto LABEL_987;
                  v146 = 0;
                  if ( v10 > 1936936296 )
                  {
                    if ( v10 > 1937329512 )
                      LOBYTE(v146) = v10 > 1937331048 ? 13 : 10;
                    else
                      LOBYTE(v146) = v10 > 1937326952 ? 7 : 9;
                  }
                  else if ( v10 > 1936085864 )
                  {
                    LOBYTE(v146) = v10 > 1936933736 ? 6 : 11;
                  }
                  else
                  {
                    LOBYTE(v146) = v10 > 1936084328 ? 8 : 5;
                  }
                  v347 = (int **)*v145;
                  v3 = v145[1];
                  if ( *v145 == v3 )
                    goto LABEL_987;
                  while ( 1 )
                  {
                    v348 = *v347;
                    if ( *((_BYTE *)*v347 + 8) == (_BYTE)v146 )
                      break;
                    if ( ++v347 == (int **)v3 )
                      goto LABEL_987;
                  }
                  if ( v347 == (int **)v3 )
                  {
LABEL_987:
                    if ( a3 == &qword_141B5A4A0 )
                      goto LABEL_989;
                    goto LABEL_988;
                  }
                  if ( v10 > 1936936296 )
                  {
                    if ( v10 > 1937329512 )
                    {
                      if ( v10 > 1937331048 )
                      {
                        if ( v10 == 1937331064 )
                          goto LABEL_1110;
                        goto LABEL_1107;
                      }
                      if ( v10 == 1937329513 )
                        goto LABEL_1107;
                    }
                    else if ( v10 > 1937326952 )
                    {
                      if ( v10 == 1937326953 )
                        goto LABEL_1107;
                    }
                    else if ( v10 == 1936936297 )
                    {
                      goto LABEL_1107;
                    }
                  }
                  else if ( v10 > 1936085864 )
                  {
                    if ( v10 > 1936933736 )
                    {
                      if ( v10 == 1936933737 )
                        goto LABEL_1107;
                    }
                    else if ( v10 == 1936085865 )
                    {
                      goto LABEL_1107;
                    }
                  }
                  else
                  {
                    if ( v10 <= 1936084328 )
                    {
                      if ( v10 != 1936081769 )
                        goto LABEL_1110;
LABEL_1107:
                      v395 = v348[1];
                      v396 = sub_14083D4F0(v146) + 40;
                      DWORD2(v442) = v395;
                      *(_QWORD *)&v442 = v396;
                      if ( &v442 != (__int128 *)a3 )
                      {
                        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                        v397 = *((_QWORD *)&v442 + 1);
                        *(_OWORD *)a3 = v442;
                        v396 = sub_14083D4F0(v397) + 8;
                        v442 = (unsigned __int64)v396;
                      }
LABEL_1112:
                      v3 = *(_QWORD *)v396;
                      (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v396 + 16LL))(v396, &v442);
                      v400 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
                      if ( a3 == &qword_141B5A4A0 || v400 != -1 )
                      {
LABEL_989:
                        LOBYTE(v3) = v142 != 0;
                        return (unsigned int)v3;
                      }
LABEL_988:
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                        qword_141B5A4A0,
                        &qword_141B5A4A0,
                        a3);
                      goto LABEL_989;
                    }
                    if ( v10 == 1936084329 )
                      goto LABEL_1107;
                  }
LABEL_1110:
                  v398 = *v348;
                  v396 = sub_14083D4F0(v146) + 40;
                  DWORD2(v442) = v398;
                  *(_QWORD *)&v442 = v396;
                  if ( &v442 != (__int128 *)a3 )
                  {
                    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                    v399 = *((_QWORD *)&v442 + 1);
                    *(_OWORD *)a3 = v442;
                    v396 = sub_14083D4F0(v399) + 8;
                    v442 = (unsigned __int64)v396;
                  }
                  goto LABEL_1112;
                }
              }
              else if ( v10 <= 1936085864 || v10 <= 1936933736 )
              {
                v143 = 1;
                goto LABEL_536;
              }
              v143 = 2;
              goto LABEL_536;
            }
            if ( v10 > 2002936683 )
            {
              if ( v10 != 2002936684 )
              {
                if ( v10 == 2002937198 )
                {
                  v178 = sub_140DBC940();
                  LODWORD(v3) = ((*(_WORD *)(v5 + 324) & 0x1FF) << 8)
                              | (*(unsigned __int16 *)(v5 + 324) >> 9)
                              | (*(unsigned __int16 *)(v5 + 326) << 17);
                  DWORD2(v442) = v3;
                  *(_QWORD *)&v442 = v178;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                if ( v10 == 2002940788 )
                {
                  v34 = sub_140DBC940();
                  LODWORD(v3) = ((*(_WORD *)(v5 + 320) & 0x1FF) << 8)
                              | (*(unsigned __int16 *)(v5 + 320) >> 9)
                              | (*(unsigned __int16 *)(v5 + 322) << 17);
                  DWORD2(v442) = v3;
                  *(_QWORD *)&v442 = v34;
                  sub_14083DFA0(a3, &v442);
                  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                  goto LABEL_5;
                }
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              }
              if ( *(_DWORD *)(v5 + 332) != 0 )
              {
                v177 = sub_141335F60();
                DWORD2(v442) = *(_DWORD *)(v5 + 332);
                *(_QWORD *)&v442 = v177;
                sub_14083DFA0(a3, &v442);
                (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
                goto LABEL_5;
              }
              goto LABEL_790;
            }
            if ( v10 != 1953068140 )
            {
              if ( v10 != 1953784684 )
                return sub_140FE3F20((_DWORD *)v5, v10, a3);
              goto LABEL_419;
            }
            sub_1407C9510(&v442);
            sub_1407C9510(&v440);
            v180 = sub_14083D4F0(v179);
            LODWORD(v439[0]) = 1128686418;
            v438 = v180 + 56;
            v3 = (unsigned __int64)&v438;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            v182 = sub_14083D4F0(v181);
            LODWORD(v439[0]) = 1128686425;
            v438 = v182 + 56;
            sub_14083B5F0(&v440, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
            sub_1407EAFE0(v5, &v442, &v440);
            sub_14083DDA0(&v438, &v442);
            sub_14083DFA0(a3, &v438);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v438 + 16LL))(v438, &v438);
          }
          sub_14083B0A0(&v440);
LABEL_907:
          sub_140833970(&v442);
          goto LABEL_5;
        }
        if ( v10 <= 1936085864 )
        {
          if ( v10 > 1936081783 )
          {
            if ( v10 != 1936081784 && v10 != 1936084329 && v10 != 1936084344 )
              return sub_140FE3F20((_DWORD *)v5, v10, a3);
            goto LABEL_520;
          }
          if ( v10 != 1935894116 )
          {
            if ( v10 == 1935896675 )
              goto LABEL_1009;
            if ( v10 != 1936081769 )
              return sub_140FE3F20((_DWORD *)v5, v10, a3);
            goto LABEL_520;
          }
          v12 = *(_QWORD *)(v5 + 176);
          if ( v12 != 0 )
          {
            v147 = sub_1409A3C20();
            v120 = *(float *)&v147;
          }
          else
          {
            v120 = MEMORY[0x141759000];
          }
LABEL_856:
          v304 = sub_14083D4F0(v12);
          *((float *)&v442 + 2) = v120;
          *(_QWORD *)&v442 = v304 + 104;
          sub_14083DFA0(a3, &v442);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
          goto LABEL_5;
        }
        a2 = 1768124016;
        if ( v10 != 1936552035 )
        {
          if ( v10 != 1936085865 && v10 != 1936085880 )
            return sub_140FE3F20((_DWORD *)v5, v10, a3);
          goto LABEL_520;
        }
      }
      if ( v10 > 1869901170 )
        break;
      if ( v10 > 1851880552 )
      {
        if ( v10 > 1852204898 )
        {
          if ( v10 != 1852204899 )
          {
            if ( v10 != 1853058916 )
            {
              if ( v10 == 1853453411 )
                goto LABEL_223;
              return sub_140FE3F20((_DWORD *)v5, v10, a3);
            }
            goto LABEL_502;
          }
LABEL_419:
          sub_140EBC750(v5, (char *)&v442 + 8);
          *(_QWORD *)&v442 = sub_141335F60();
          sub_14083DFA0(a3, &v442);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
          goto LABEL_5;
        }
        if ( v10 != 1851880553 )
        {
          if ( v10 != 1851942755 )
            return sub_140FE3F20((_DWORD *)v5, v10, a3);
LABEL_416:
          sub_140EBC8F0(v5, &v440);
          v110 = sub_141335F60();
          DWORD2(v442) = v440;
          *(_QWORD *)&v442 = v110;
          sub_14083DFA0(a3, &v442);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v442 + 16LL))(v442, &v442);
          goto LABEL_5;
        }
        goto LABEL_501;
      }
      if ( v10 != 1835954275 )
        return sub_140FE3F20((_DWORD *)v5, v10, a3);
      a2 = 1819240303;
    }
    if ( v10 <= 1919382642 )
    {
      if ( v10 != 1869901171 )
      {
        if ( v10 != 1883333484 && v10 != 1884578668 )
          return sub_140FE3F20((_DWORD *)v5, v10, a3);
        goto LABEL_262;
      }
LABEL_331:
      v423 = v10 == 1330924883;
      LOBYTE(v3) = 1;
      v77 = v5;
      LODWORD(v13) = 0;
LABEL_503:
      LOBYTE(v14) = 1;
      sub_141561880((unsigned int)&v442, v77, v13, v14, 0, v423);
LABEL_504:
      sub_140ECA230(&v442, a3);
LABEL_505:
      if ( (_QWORD)v442 != 0 )
        sub_1407E4890(qword_141ABD470, v442, v443 - v442);
      return (unsigned int)v3;
    }
    if ( v10 != 1935831139 )
    {
      if ( v10 != 1919382643 )
      {
        if ( v10 == 1919968370 )
        {
          v139 = *(_QWORD **)(v5 + 176);
          if ( v139 != nullptr )
          {
            if ( v139[24] != v139[25] )
            {
              if ( (unsigned __int8)sub_140EBA600(v5) != 0 && (unsigned __int8)sub_140EBA780(v5) != 0 )
              {
                v139 = *(_QWORD **)(v5 + 176);
                if ( v139 == nullptr )
                  goto LABEL_1009;
              }
              else
              {
                v139 = *(_QWORD **)(v5 + 176);
                if ( v139 == nullptr )
                  goto LABEL_1009;
                v340 = 0;
                if ( v139[24] != v139[25] )
                  v340 = *(_QWORD *)(v5 + 176);
                v341 = *(unsigned __int64 **)(v340 + 192);
                if ( *(unsigned __int64 **)(v340 + 200) != v341 )
                {
                  v3 = *v341;
                  if ( *v341 != 0 )
                  {
                    sub_140FE7190(*(_QWORD *)(v3 + 288), &v442);
                    sub_140FEAD00(&v442, &v440);
                    sub_14083DFA0(a3, &v440);
                    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
                    (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v442 + 1) + 16LL))(
                      *((_QWORD *)&v442 + 1),
                      (char *)&v442 + 8);
                  }
                  LOBYTE(v3) = v3 != 0;
                  return (unsigned int)v3;
                }
              }
            }
            v342 = v139[36];
            if ( v342 != 0 )
              v343 = *(unsigned int *)(v342 + 12);
            else
              v343 = 0xFFFFFFFFLL;
            v350 = v139[197];
            if ( v350 != 0 && (unsigned __int8)sub_1408FFBF0(v350, v343) == 0xFF )
            {
              sub_140FE7190(*(_QWORD *)(*(_QWORD *)(*(_QWORD *)(v5 + 176) + 1576LL) + 288LL), &v442);
              sub_140FEAD00(&v442, &v440);
              sub_14083DFA0(a3, &v440);
              (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v440 + 16LL))(v440, &v440);
              (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v442 + 1) + 16LL))(
                *((_QWORD *)&v442 + 1),
                (char *)&v442 + 8);
              goto LABEL_5;
            }
          }
LABEL_1009:
          LODWORD(v3) = 0;
          return (unsigned int)v3;
        }
        return sub_140FE3F20((_DWORD *)v5, v10, a3);
      }
      v424 = 0;
      v422 = 1;
      goto LABEL_803;
    }
    v15 = *(_DWORD **)(v5 + 96);
    if ( v15 != nullptr )
      return (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64 *))(*(_QWORD *)v15 + 16LL))(v15, 1919706978, a3);
    v15 = *(_DWORD **)(v5 + 88);
    if ( v15 != nullptr )
      return (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64 *))(*(_QWORD *)v15 + 16LL))(v15, 1919706978, a3);
    v16 = *(unsigned __int64 **)(qword_141B5FDC8 + 128);
    a2 = 1919706978;
    v17 = v16[1] - *v16;
  }
  while ( v17 == 0 );
  v18 = v17 >> 3;
  v19 = v18 - 1;
  while ( 1 )
  {
    if ( (v19 & 0x80000000) == 0LL )
    {
      if ( (_BYTE)word_141B60320 == 0
        && (v3 = *(_QWORD *)(qword_141B5FDC8 + 96),
            (__int64)(*(_QWORD *)(qword_141B5FDC8 + 104) - v3) >> 3 > (unsigned __int64)(unsigned int)v19)
        || (v3 = *v16, v18 > (unsigned int)v19) )
      {
        v15 = *(_DWORD **)(v3 + 8LL * (unsigned int)v19);
        if ( v15 != nullptr && v15[3] == 7 )
          return (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64 *))(*(_QWORD *)v15 + 16LL))(v15, 1919706978, a3);
      }
    }
    if ( v19-- == 0 )
      goto LABEL_7;
  }
}
