__int64 __fastcall sub_1411F1090(__int64 *a1, int a2, _QWORD *a3, __int64 a4)
{
  signed __int64 v4; // rax
  char **v5; // rbx
  void *v6; // rsp
  _QWORD *v7; // r14
  __int64 *v10; // rdx
  int v11; // esi
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rdx
  __int64 v15; // rcx
  int v16; // esi
  __int64 v17; // rcx
  __int64 v18; // rax
  char *v19; // rcx
  __int64 v20; // rdx
  char *v21; // rcx
  __int64 v22; // rcx
  void (__fastcall ***v23)(_QWORD, __int64); // rcx
  __int64 v24; // rcx
  __int64 v25; // rdi
  __int64 v26; // rdx
  signed __int64 v27; // rdi
  unsigned __int64 v28; // rcx
  char *v29; // rsi
  unsigned __int64 v30; // rcx
  char *v31; // rsi
  __int64 v33; // rcx
  __int64 *v34; // rax
  int v35; // esi
  __int64 v36; // rax
  char **v37; // rax
  char *v38; // rsi
  __int64 v39; // rax
  __int64 v40; // rdx
  __int64 v41; // rcx
  __int64 v42; // rdx
  __int64 v43; // rdx
  __int64 v44; // rdx
  __int64 v45; // rdx
  __int64 v46; // rax
  __int64 v47; // rsi
  __int64 v48; // rdx
  __int64 v49; // r8
  __int64 v50; // r9
  int v51; // r9d
  __int64 v52; // rcx
  __int64 *v53; // rsi
  __int64 v54; // rcx
  __int64 v55; // rax
  __int64 v56; // rcx
  __int64 *v57; // rcx
  __int64 v58; // r8
  __int64 v59; // rcx
  _QWORD *v60; // rax
  _DWORD *v61; // rax
  __int64 **v62; // rax
  __int64 *v63; // rcx
  __int64 (__fastcall *v64)(__int64 *, _QWORD, _QWORD *); // rax
  _DWORD *v65; // rax
  __int64 *v66; // rsi
  __int64 v67; // rcx
  __int64 v68; // rax
  __int64 v69; // rcx
  __int64 *v70; // rax
  __int64 v71; // rax
  __int64 v72; // rax
  __int64 v73; // rcx
  __int64 *v74; // rsi
  __int64 v75; // rcx
  __int64 v76; // rcx
  __int64 v77; // rdx
  __int64 v78; // r8
  __int64 v79; // r9
  int v80; // r9d
  __int64 i; // rsi
  __int64 j; // rsi
  __int64 v83; // rax
  unsigned __int64 v84; // rax
  __int64 v85; // r13
  __int64 k; // rbx
  __int64 v87; // rsi
  __int64 *v88; // rsi
  __int64 v89; // rcx
  __int64 v90; // rax
  __int64 v91; // rcx
  _DWORD *v92; // rax
  __int64 *v93; // rsi
  __int64 v94; // rcx
  __int64 v95; // rcx
  __int64 v96; // rax
  __int64 *v97; // rcx
  __int64 v98; // rdx
  char **v99; // rdi
  __int64 m; // rbx
  __int64 *v101; // rsi
  __int64 v102; // rcx
  __int64 v103; // rcx
  __int64 *v104; // rax
  __int64 *v105; // rcx
  int v106; // r8d
  __int64 v107; // rsi
  unsigned int v108; // edx
  __int64 v109; // rcx
  __int64 v110; // rax
  int v111; // esi
  __int64 v112; // rax
  __int64 v113; // rcx
  __int64 v114; // rax
  __int64 v115; // rcx
  __int64 v116; // rax
  __int64 v117; // rcx
  __int64 v118; // rax
  __int64 v119; // rcx
  __int64 v120; // rax
  __int64 v121; // rcx
  __int64 v122; // rax
  __int64 v123; // rcx
  __int64 v124; // rax
  __int64 v125; // rcx
  __int64 v126; // rax
  __int64 v127; // rax
  __int64 *v128; // rsi
  _QWORD *v129; // rdi
  __int64 n; // rsi
  __int64 v131; // rdi
  __int64 v132; // rcx
  __int64 v133; // rax
  __int64 v134; // rdi
  __int64 v135; // rcx
  __int64 v136; // rax
  __int64 v137; // rax
  __int64 *v138; // rdx
  __int64 v139; // rax
  __int64 v140; // rcx
  __int64 v141; // rax
  __int64 v142; // rcx
  __int64 v143; // rax
  __int64 v144; // rcx
  __int64 v145; // rax
  __int64 v146; // rcx
  __int64 v147; // rax
  _QWORD v148[2]; // [rsp+30h] [rbp-1888h] BYREF
  __int64 v149; // [rsp+40h] [rbp-1878h]
  _BYTE v150[3856]; // [rsp+80h] [rbp-1838h] BYREF
  char *v151; // [rsp+F90h] [rbp-928h] BYREF
  char *v152; // [rsp+F98h] [rbp-920h] BYREF
  char *v153; // [rsp+FA0h] [rbp-918h]
  __int64 v154; // [rsp+FA8h] [rbp-910h] BYREF
  __int64 v155; // [rsp+FC0h] [rbp-8F8h] BYREF
  __int64 v156; // [rsp+FD8h] [rbp-8E0h] BYREF
  __int64 v157; // [rsp+FF0h] [rbp-8C8h] BYREF
  __int64 v158; // [rsp+1008h] [rbp-8B0h] BYREF
  __int64 v159; // [rsp+1020h] [rbp-898h] BYREF
  __int64 v160; // [rsp+1038h] [rbp-880h] BYREF
  __int64 v161; // [rsp+1050h] [rbp-868h] BYREF
  __int64 v162; // [rsp+1068h] [rbp-850h] BYREF
  __int64 v163; // [rsp+1080h] [rbp-838h] BYREF
  __int64 v164; // [rsp+1098h] [rbp-820h] BYREF
  __int64 v165; // [rsp+10B0h] [rbp-808h] BYREF
  __int64 v166; // [rsp+10C8h] [rbp-7F0h] BYREF
  __int64 v167; // [rsp+10E0h] [rbp-7D8h] BYREF
  __int64 v168; // [rsp+10F8h] [rbp-7C0h] BYREF
  __int64 v169; // [rsp+1110h] [rbp-7A8h] BYREF
  __int64 v170; // [rsp+1128h] [rbp-790h] BYREF
  __int64 v171; // [rsp+1140h] [rbp-778h] BYREF
  __int64 v172; // [rsp+1158h] [rbp-760h] BYREF
  __int64 v173; // [rsp+1170h] [rbp-748h] BYREF
  __int64 v174; // [rsp+1188h] [rbp-730h] BYREF
  __int64 v175; // [rsp+11A0h] [rbp-718h] BYREF
  __int64 v176; // [rsp+11B8h] [rbp-700h] BYREF
  __int64 v177; // [rsp+11D0h] [rbp-6E8h] BYREF
  __int64 v178; // [rsp+11E8h] [rbp-6D0h] BYREF
  __int64 v179; // [rsp+1200h] [rbp-6B8h] BYREF
  __int64 v180; // [rsp+1218h] [rbp-6A0h] BYREF
  __int64 v181; // [rsp+1230h] [rbp-688h] BYREF
  __int64 v182; // [rsp+1248h] [rbp-670h] BYREF
  __int64 v183; // [rsp+1260h] [rbp-658h] BYREF
  __int64 v184; // [rsp+1278h] [rbp-640h] BYREF
  __int64 v185; // [rsp+1290h] [rbp-628h] BYREF
  __int64 v186; // [rsp+12A8h] [rbp-610h] BYREF
  __int64 v187; // [rsp+12C0h] [rbp-5F8h] BYREF
  __int64 v188; // [rsp+12D8h] [rbp-5E0h] BYREF
  __int64 v189; // [rsp+12F0h] [rbp-5C8h] BYREF
  __int64 v190; // [rsp+1308h] [rbp-5B0h] BYREF
  __int64 v191; // [rsp+1320h] [rbp-598h] BYREF
  __int64 v192; // [rsp+1338h] [rbp-580h] BYREF
  __int64 v193; // [rsp+1350h] [rbp-568h] BYREF
  __int64 v194; // [rsp+1368h] [rbp-550h] BYREF
  __int64 v195; // [rsp+1380h] [rbp-538h] BYREF
  __int64 v196; // [rsp+1398h] [rbp-520h] BYREF
  __int64 v197; // [rsp+13B0h] [rbp-508h] BYREF
  __int64 v198; // [rsp+13C8h] [rbp-4F0h] BYREF
  __int64 v199; // [rsp+13E0h] [rbp-4D8h] BYREF
  __int64 v200; // [rsp+13F8h] [rbp-4C0h] BYREF
  __int64 v201; // [rsp+1410h] [rbp-4A8h] BYREF
  __int64 v202; // [rsp+1428h] [rbp-490h] BYREF
  __int64 v203; // [rsp+1440h] [rbp-478h] BYREF
  __int64 v204; // [rsp+1458h] [rbp-460h] BYREF
  __int64 v205; // [rsp+1470h] [rbp-448h] BYREF
  __int64 v206; // [rsp+1488h] [rbp-430h] BYREF
  __int64 v207; // [rsp+14A0h] [rbp-418h] BYREF
  __int64 v208; // [rsp+14B8h] [rbp-400h] BYREF
  __int64 v209; // [rsp+14D0h] [rbp-3E8h] BYREF
  __int64 v210; // [rsp+14E8h] [rbp-3D0h] BYREF
  __int64 v211; // [rsp+1500h] [rbp-3B8h] BYREF
  __int64 v212; // [rsp+1518h] [rbp-3A0h] BYREF
  __int64 v213; // [rsp+1530h] [rbp-388h] BYREF
  __int64 v214; // [rsp+1548h] [rbp-370h] BYREF
  __int64 v215; // [rsp+1560h] [rbp-358h] BYREF
  __int64 v216; // [rsp+1578h] [rbp-340h] BYREF
  __int64 v217; // [rsp+1590h] [rbp-328h] BYREF
  __int64 v218; // [rsp+15A8h] [rbp-310h] BYREF
  __int64 v219; // [rsp+15C0h] [rbp-2F8h] BYREF
  __int64 v220; // [rsp+15D8h] [rbp-2E0h] BYREF
  __int64 v221; // [rsp+15F0h] [rbp-2C8h] BYREF
  __int64 v222; // [rsp+1608h] [rbp-2B0h] BYREF
  __int64 v223; // [rsp+1620h] [rbp-298h] BYREF
  __int64 v224; // [rsp+1638h] [rbp-280h] BYREF
  __int64 v225; // [rsp+1650h] [rbp-268h] BYREF
  __int64 v226; // [rsp+1668h] [rbp-250h] BYREF
  __int64 v227; // [rsp+1680h] [rbp-238h] BYREF
  __int64 v228; // [rsp+1698h] [rbp-220h] BYREF
  __int64 v229; // [rsp+16B0h] [rbp-208h] BYREF
  __int64 v230; // [rsp+16C8h] [rbp-1F0h] BYREF
  __int64 v231; // [rsp+16E0h] [rbp-1D8h] BYREF
  __int64 v232; // [rsp+16F8h] [rbp-1C0h] BYREF
  __int64 v233; // [rsp+1710h] [rbp-1A8h] BYREF
  __int64 v234; // [rsp+1728h] [rbp-190h] BYREF
  __int64 v235; // [rsp+1740h] [rbp-178h] BYREF
  __int64 v236; // [rsp+1758h] [rbp-160h] BYREF
  __int64 v237; // [rsp+1770h] [rbp-148h] BYREF
  __int64 v238; // [rsp+1788h] [rbp-130h] BYREF
  __int64 v239; // [rsp+17A0h] [rbp-118h] BYREF
  __int64 v240; // [rsp+17B8h] [rbp-100h] BYREF
  __int64 v241; // [rsp+17D0h] [rbp-E8h] BYREF
  __int64 v242; // [rsp+17E8h] [rbp-D0h] BYREF
  __int64 v243; // [rsp+1800h] [rbp-B8h] BYREF
  _QWORD v244[3]; // [rsp+1818h] [rbp-A0h] BYREF
  _QWORD v245[2]; // [rsp+1830h] [rbp-88h] BYREF
  __int64 v246; // [rsp+1840h] [rbp-78h] BYREF
  int v247; // [rsp+1848h] [rbp-70h]
  volatile signed __int32 *v248; // [rsp+1858h] [rbp-60h] BYREF
  _QWORD v249[11]; // [rsp+1860h] [rbp-58h] BYREF

  v6 = alloca(v4);
  v249[2] = -2;
  v7 = a3;
  if ( a2 <= 1416324914 )
  {
    switch ( a2 )
    {
      case 1347184494:
        v11 = *((unsigned __int8 *)a1 + 185);
        v12 = sub_14083D4F0(a1) + 40;
        LODWORD(v148[1]) = v11;
        v148[0] = v12;
        if ( v148 != v7 )
        {
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v7 + 16LL))(*v7, v7);
          v13 = v148[1];
          *(_OWORD *)v7 = *(_OWORD *)v148;
          v12 = sub_14083D4F0(v13) + 8;
          *(_OWORD *)v148 = (unsigned __int64)v12;
        }
        v5 = *(char ***)v12;
        (*(void (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v12 + 16LL))(v12, v148);
        goto LABEL_68;
      case 1416324913:
        v10 = a1;
        a3 = nullptr;
        break;
      case 1416324914:
        v10 = a1;
        LOBYTE(a3) = 1;
        break;
      default:
        goto LABEL_16;
    }
    goto LABEL_42;
  }
  if ( a2 <= 1416326961 )
  {
    if ( a2 != 1416324915 )
    {
      if ( a2 == 1416326961 )
      {
        v10 = a1;
        a3 = nullptr;
LABEL_40:
        LOBYTE(a4) = 1;
        goto LABEL_43;
      }
      goto LABEL_16;
    }
    v10 = a1;
    LOBYTE(a3) = 2;
LABEL_42:
    a4 = 0;
LABEL_43:
    sub_1415EB890(&v151, v10, a3, a4);
    v25 = v152 - v151;
    *(_OWORD *)v148 = 0;
    v149 = 0;
    v26 = v152 - v151;
    if ( v152 != v151 )
    {
      if ( v26 < 0 )
        sub_1400526C0(v24, v26);
      v148[0] = sub_1407E4490(qword_141ABD470, v26);
      v149 = v148[0] + 8 * (v25 >> 3);
      v27 = v152 - v151;
      sub_141758A00(v148[0], v151, v152 - v151);
      v148[1] = v148[0] + v27;
    }
    v248 = (volatile signed __int32 *)v148;
    sub_1411FFE30(&v248, v7);
    if ( v148[0] != 0 )
    {
      v28 = v149 - v148[0];
      if ( v149 - v148[0] == -1 )
      {
        v28 = *(unsigned int *)(v148[0] - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_56:
          MEMORY[0x141948990](v148[0] - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_57;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_56;
      }
      v5 = *(char ***)(qword_141ABD470 + 24);
      if ( (__int64)(*(_QWORD *)(qword_141ABD470 + 32) - (_QWORD)v5) >> 3 <= v28 )
        goto LABEL_56;
      v29 = v5[v28];
      if ( v29 == nullptr )
        goto LABEL_56;
      MEMORY[0x1419475D8](v29 + 32, v148[0] - *((unsigned int *)v29 + 30));
      if ( (v29[72] == 0 || _InterlockedDecrement((volatile signed __int32 *)v29 + 16) == 0) && v29[97] != 0 )
        sub_1412D33C0(v29);
    }
LABEL_57:
    if ( v151 == nullptr )
    {
LABEL_68:
      LOBYTE(v5) = 1;
      return (unsigned int)v5;
    }
    v30 = v153 - v151;
    if ( v153 - v151 == -1 )
    {
      v30 = *(unsigned int *)&v151[-*(unsigned int *)(qword_141ABD470 + 48)];
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_67:
        MEMORY[0x141948990](&v151[-*(unsigned int *)(qword_141ABD470 + 48)]);
        goto LABEL_68;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_67;
    }
    v5 = *(char ***)(qword_141ABD470 + 24);
    if ( (__int64)(*(_QWORD *)(qword_141ABD470 + 32) - (_QWORD)v5) >> 3 > v30 )
    {
      v31 = v5[v30];
      if ( v31 != nullptr )
      {
        MEMORY[0x1419475D8](v31 + 32, &v151[-*((unsigned int *)v31 + 30)]);
        if ( (v31[72] == 0 || _InterlockedDecrement((volatile signed __int32 *)v31 + 16) == 0) && v31[97] != 0 )
          sub_1412D33C0(v31);
        goto LABEL_68;
      }
    }
    goto LABEL_67;
  }
  if ( a2 == 1416326962 )
  {
    v10 = a1;
    LOBYTE(a3) = 1;
    goto LABEL_40;
  }
  if ( a2 == 1416326963 )
  {
    v10 = a1;
    LOBYTE(a3) = 2;
    goto LABEL_40;
  }
LABEL_16:
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5FD40 + 32LL))(qword_141B5FD40) == 0 )
  {
    LOBYTE(v5) = 1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *, _QWORD, _QWORD *))(*(_QWORD *)qword_141B5FD40 + 48LL))(
           qword_141B5FD40,
           a1,
           (unsigned int)a2,
           v7) != 0 )
      return (unsigned int)v5;
  }
  if ( a2 <= 1129797490 )
  {
    if ( a2 <= 1129070944 )
    {
      if ( a2 <= 1128746338 )
      {
        if ( a2 <= 1128679267 )
        {
          switch ( a2 )
          {
            case 1128416353:
            case 1128416355:
            case 1128416356:
            case 1128416358:
            case 1128416367:
              goto LABEL_394;
            case 1128416354:
            case 1128416357:
            case 1128416359:
            case 1128416360:
            case 1128416361:
            case 1128416362:
            case 1128416363:
            case 1128416364:
            case 1128416365:
            case 1128416366:
              goto LABEL_362;
            default:
              switch ( a2 )
              {
                case 1128421217:
                case 1128421219:
                case 1128421220:
                case 1128421222:
                case 1128421231:
                  goto LABEL_394;
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
                  goto LABEL_362;
                default:
                  if ( a2 == 1097032556 )
                    goto LABEL_262;
                  goto LABEL_362;
              }
          }
        }
        switch ( a2 )
        {
          case 1128679268:
          case 1128679277:
          case 1128679278:
          case 1128679279:
          case 1128679280:
          case 1128679283:
            goto LABEL_394;
          default:
            goto LABEL_362;
        }
      }
      switch ( a2 )
      {
        case 1128746339:
        case 1128746340:
        case 1128746343:
        case 1128746350:
        case 1128746351:
        case 1128746352:
          goto LABEL_394;
        case 1128746341:
        case 1128746342:
        case 1128746344:
        case 1128746345:
        case 1128746346:
        case 1128746347:
        case 1128746348:
        case 1128746349:
          goto LABEL_362;
        default:
          switch ( a2 )
          {
            case 1128813409:
            case 1128813411:
            case 1128813412:
            case 1128813414:
            case 1128813423:
              goto LABEL_394;
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
              goto LABEL_362;
            default:
              switch ( a2 )
              {
                case 1128808801:
                case 1128808803:
                case 1128808804:
                case 1128808815:
                  goto LABEL_394;
                default:
                  goto LABEL_362;
              }
          }
      }
    }
    if ( a2 <= 1129792356 )
    {
      if ( a2 > 1129075314 )
      {
        switch ( a2 )
        {
          case 1129271395:
          case 1129271396:
          case 1129271405:
          case 1129271406:
          case 1129271407:
          case 1129271408:
            goto LABEL_394;
          case 1129271397:
          case 1129271398:
          case 1129271399:
          case 1129271400:
          case 1129271401:
          case 1129271402:
          case 1129271403:
          case 1129271404:
            goto LABEL_362;
          default:
            switch ( a2 )
            {
              case 1129272163:
              case 1129272164:
              case 1129272173:
              case 1129272174:
              case 1129272175:
              case 1129272176:
                goto LABEL_394;
              case 1129272165:
              case 1129272166:
              case 1129272167:
              case 1129272168:
              case 1129272169:
              case 1129272170:
              case 1129272171:
              case 1129272172:
                goto LABEL_362;
              default:
                if ( a2 != 1129075315 )
                  goto LABEL_362;
                goto LABEL_394;
            }
        }
      }
      switch ( a2 )
      {
        case 1129070945:
        case 1129070947:
        case 1129070948:
        case 1129070959:
          goto LABEL_394;
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
          goto LABEL_362;
        default:
          if ( a2 == 1129075301 || a2 == 1129075303 )
            goto LABEL_394;
          goto LABEL_362;
      }
    }
    if ( a2 > 1129796198 )
    {
      if ( a2 <= 1129796454 )
      {
        if ( a2 != 1129796199 && a2 != 1129796211 && a2 != 1129796453 )
          goto LABEL_362;
      }
      else if ( a2 > 1129797476 )
      {
        if ( a2 != 1129797477 && a2 != 1129797479 )
          goto LABEL_362;
      }
      else if ( a2 != 1129796455 && a2 != 1129796467 )
      {
        goto LABEL_362;
      }
    }
    else if ( a2 <= 1129794660 )
    {
      if ( a2 != 1129792357 && a2 != 1129792359 && a2 != 1129792371 )
        goto LABEL_362;
    }
    else if ( a2 > 1129794674 )
    {
      if ( a2 != 1129794675 && a2 != 1129796197 )
        goto LABEL_362;
    }
    else if ( a2 != 1129794661 && a2 != 1129794663 )
    {
      goto LABEL_362;
    }
LABEL_394:
    JUMPOUT(0x144026350LL);
  }
  if ( a2 > 1413705062 )
  {
    if ( a2 <= 1414947680 )
    {
      if ( a2 > 1413706605 )
      {
        if ( a2 > 1414230080 )
        {
          if ( a2 <= 1414292838 )
          {
            if ( a2 == 1414230081 )
            {
              if ( *((_BYTE *)a1 + 186) != 0 || (*(unsigned int (__fastcall **)(__int64 *))(*a1 + 56))(a1) != 3 )
              {
                v80 = 0;
              }
              else
              {
                LOBYTE(v77) = 8;
                LOBYTE(v78) = 1;
                LOBYTE(v79) = 1;
                v80 = sub_140E675C0(a1, v77, v78, v79);
              }
              v134 = sub_1411D7790((_DWORD)a1, (unsigned int)&v248, (unsigned int)&v246, v80, 0);
              v136 = sub_14083D4F0(v135);
              v152 = nullptr;
              v151 = (char *)(v136 + 8);
              v5 = &v151;
              (*(void (__fastcall **)(__int64, char **, _QWORD *))(*(_QWORD *)(v136 + 8) + 24LL))(
                v136 + 8,
                &v151,
                &v148[1]);
              LODWORD(v148[0]) = -8388609;
              (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v151 + 16LL))(v151, &v151);
              if ( v134 != 0 )
              {
                (*(void (__fastcall **)(__int64, char **))(*(_QWORD *)v134 + 144LL))(v134, &v151);
                LODWORD(v148[0]) = (_DWORD)v151;
                sub_14083DFA0(&v148[1], &v152);
                (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v152 + 16LL))(v152, &v152);
              }
            }
            else
            {
              if ( a2 != 1414230092 )
                goto LABEL_362;
              if ( *((_BYTE *)a1 + 186) != 0 || (*(unsigned int (__fastcall **)(__int64 *))(*a1 + 56))(a1) != 3 )
              {
                v51 = 0;
              }
              else
              {
                LOBYTE(v48) = 8;
                LOBYTE(v49) = 1;
                LOBYTE(v50) = 1;
                v51 = sub_140E675C0(a1, v48, v49, v50);
              }
              v131 = sub_1411D7790((_DWORD)a1, (unsigned int)&v248, (unsigned int)&v246, v51, 1);
              v133 = sub_14083D4F0(v132);
              v152 = nullptr;
              v151 = (char *)(v133 + 8);
              v5 = &v151;
              (*(void (__fastcall **)(__int64, char **, _QWORD *))(*(_QWORD *)(v133 + 8) + 24LL))(
                v133 + 8,
                &v151,
                &v148[1]);
              LODWORD(v148[0]) = -8388609;
              (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v151 + 16LL))(v151, &v151);
              if ( v131 != 0 )
              {
                (*(void (__fastcall **)(__int64, char **))(*(_QWORD *)v131 + 144LL))(v131, &v151);
                LODWORD(v148[0]) = (_DWORD)v151;
                sub_14083DFA0(&v148[1], &v152);
                (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v152 + 16LL))(v152, &v152);
              }
            }
            sub_140FEAD00(v148, &v151);
            sub_14083DFA0(v7, &v151);
            (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v151 + 16LL))(v151, &v151);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[1] + 16LL))(v148[1], &v148[1]);
            goto LABEL_68;
          }
          if ( a2 == 1414292839 )
          {
            LOBYTE(v5) = 1;
            if ( *((_BYTE *)a1 + 186) != 0 )
            {
              if ( *((_BYTE *)a1 + 186) != 1 )
                return (unsigned int)v5;
              v96 = *a1;
              v97 = a1;
              v98 = 1316447088;
            }
            else
            {
              if ( (*(unsigned int (__fastcall **)(__int64 *))(*a1 + 56))(a1) != 3
                || (*((_BYTE *)a1 + 353) & 1) != 0
                || (unsigned __int8)sub_1408FF650(a1) != 0
                || (*(unsigned __int8 (__fastcall **)(__int64 *))(*a1 + 352))(a1) != 0 )
              {
                return (unsigned int)v5;
              }
              v96 = *a1;
              v97 = a1;
              v98 = 1131177328;
            }
            (*(void (__fastcall **)(__int64 *, __int64, _QWORD *))(v96 + 16))(v97, v98, v7);
            return (unsigned int)v5;
          }
          if ( a2 == 1414360658 )
            goto LABEL_234;
        }
        else
        {
          if ( a2 > 1414091586 )
          {
            if ( a2 == 1414091587 )
            {
              LOBYTE(v148[1]) = *((_BYTE *)a1 + 186) == 0;
              v148[0] = sub_14083D4F0(v15) + 24;
              sub_14083DFA0(v7, v148);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
              goto LABEL_68;
            }
            if ( a2 == 1414091598 )
            {
              LOBYTE(v148[1]) = *((_BYTE *)a1 + 186) == 1;
              v148[0] = sub_14083D4F0(v15) + 24;
              sub_14083DFA0(v7, v148);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
              goto LABEL_68;
            }
            goto LABEL_362;
          }
          if ( a2 == 1413706606 )
          {
            v74 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *))(*a1 + 376))(a1);
            v55 = sub_14083D4F0(v75);
            v148[1] = 0;
            if ( &v148[1] != v74 )
            {
              v76 = *v74;
              if ( *v74 != 0 )
                _InterlockedIncrement((volatile signed __int32 *)(v76 - 4));
              v148[1] = v76;
            }
            goto LABEL_329;
          }
          if ( a2 == 1413769037 )
            goto LABEL_234;
        }
      }
      else
      {
        if ( a2 > 1413705576 )
        {
          if ( a2 > 1413706354 )
          {
            if ( a2 == 1413706355 )
            {
              sub_141563EB0(v148, a1);
              sub_1411F47C0(v148, v7);
              if ( v148[0] != 0 )
                sub_1407E4890(qword_141ABD470, v148[0], v149 - v148[0]);
              goto LABEL_68;
            }
            if ( a2 == 1413706599 )
            {
              LODWORD(v148[1]) = (*(char (__fastcall **)(__int64 *))(*a1 + 392))(a1);
              v148[0] = sub_14083D4F0(v59) + 40;
              sub_14083DFA0(v7, v148);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
              goto LABEL_68;
            }
          }
          else
          {
            if ( a2 == 1413705577 )
            {
              LODWORD(v148[1]) = *((_DWORD *)a1 + 3);
              v148[0] = sub_14083D4F0(v15) + 40;
              sub_14083DFA0(v7, v148);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
              goto LABEL_68;
            }
            if ( a2 == 1413706352 )
            {
              v34 = (__int64 *)a1[3];
              v35 = 1500;
              if ( v34 != (__int64 *)a1[4] )
              {
                v36 = *v34;
                if ( v36 != 0 )
                  v35 = *(__int16 *)(v36 + 168);
              }
              LODWORD(v148[1]) = v35;
              v148[0] = sub_14083D4F0(v15) + 40;
              sub_14083DFA0(v7, v148);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
              goto LABEL_68;
            }
          }
          goto LABEL_362;
        }
        if ( a2 <= 1413705325 )
        {
          if ( a2 == 1413705063 )
          {
            v70 = (__int64 *)a1[3];
            if ( v70 != (__int64 *)a1[4] && (v71 = *v70) != 0 && (v72 = *(_QWORD *)(v71 + 128)) != 0 )
            {
              v73 = v72 + *(int *)(*(_QWORD *)(v72 + 8) + 4LL) + 8;
              (*(void (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v73 + 144LL))(v73, v148);
              sub_140FEAD00(v148, &v151);
              sub_14083DFA0(v7, &v151);
              (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v151 + 16LL))(v151, &v151);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[1] + 16LL))(v148[1], &v148[1]);
            }
            else
            {
              sub_140FEAD00(&dword_141B60CC0, v148);
              sub_14083DFA0(v7, v148);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
            }
            goto LABEL_68;
          }
          if ( a2 == 1413705319 )
          {
            LODWORD(v148[1]) = *((char *)a1 + 184);
            v148[0] = sub_14083D4F0(v15) + 40;
            sub_14083DFA0(v7, v148);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
            goto LABEL_68;
          }
          goto LABEL_362;
        }
        if ( a2 == 1413705326 )
          goto LABEL_247;
        if ( a2 == 1413705331 )
        {
          v53 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *))(*a1 + 368))(a1);
          v55 = sub_14083D4F0(v54);
          v148[1] = 0;
          if ( &v148[1] != v53 )
          {
            v56 = *v53;
            if ( *v53 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v56 - 4));
            v148[1] = v56;
          }
          goto LABEL_329;
        }
      }
    }
    else
    {
      if ( a2 > 1718185075 )
      {
        if ( a2 > 1937072755 )
        {
          if ( a2 <= 1952666195 )
          {
            if ( a2 == 1937072756 )
            {
              LOBYTE(v5) = 1;
              if ( qword_141B5FE08 != 0
                && **(_QWORD **)(qword_141B5FE08 + 128) != *(_QWORD *)(*(_QWORD *)(qword_141B5FE08 + 128) + 8LL)
                && (_BYTE)word_141B60320 != 0 )
              {
                sub_1407C9510(v148);
                sub_1407C9510(&v151);
                v114 = sub_14083D4F0(v113);
                LODWORD(v249[0]) = 1415866742;
                v248 = (volatile signed __int32 *)(v114 + 56);
                sub_14083B5F0(&v151, &v248);
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v248 + 16LL))(
                  v248,
                  &v248);
                v116 = sub_14083D4F0(v115);
                LODWORD(v249[0]) = 1416654707;
                v248 = (volatile signed __int32 *)(v116 + 56);
                sub_14083B5F0(&v151, &v248);
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v248 + 16LL))(
                  v248,
                  &v248);
                v118 = sub_14083D4F0(v117);
                LODWORD(v249[0]) = 1415865966;
                v248 = (volatile signed __int32 *)(v118 + 56);
                sub_14083B5F0(&v151, &v248);
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v248 + 16LL))(
                  v248,
                  &v248);
                v120 = sub_14083D4F0(v119);
                LODWORD(v249[0]) = 1315856756;
                v248 = (volatile signed __int32 *)(v120 + 56);
                sub_14083B5F0(&v151, &v248);
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v248 + 16LL))(
                  v248,
                  &v248);
                v122 = sub_14083D4F0(v121);
                LODWORD(v249[0]) = 1416196974;
                v248 = (volatile signed __int32 *)(v122 + 56);
                sub_14083B5F0(&v151, &v248);
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v248 + 16LL))(
                  v248,
                  &v248);
                v124 = sub_14083D4F0(v123);
                LODWORD(v249[0]) = 1413698383;
                v248 = (volatile signed __int32 *)(v124 + 56);
                sub_14083B5F0(&v151, &v248);
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v248 + 16LL))(
                  v248,
                  &v248);
                v126 = sub_14083D4F0(v125);
                LODWORD(v249[0]) = 1131114103;
                v248 = (volatile signed __int32 *)(v126 + 56);
                sub_14083B5F0(&v151, &v248);
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v248 + 16LL))(
                  v248,
                  &v248);
                v127 = qword_141B60C30;
                v128 = nullptr;
                if ( qword_141B60C30 != qword_141B60C38 )
                {
                  while ( *(_DWORD *)v127 != 1399415892 )
                  {
                    v127 += 16;
                    if ( v127 == qword_141B60C38 )
                      goto LABEL_383;
                  }
                  if ( v127 == qword_141B60C38 )
                    v128 = nullptr;
                  else
                    v128 = *(__int64 **)(v127 + 8);
                }
LABEL_383:
                v137 = sub_14083D4F0(qword_141B60C38);
                v138 = &qword_141B5A4A0;
                if ( v128 != nullptr )
                  v138 = v128;
                v249[1] = 0;
                v249[0] = v137 + 8;
                sub_140FEB270(&v248, v138);
                if ( (unsigned int)v248 <= 0xFEFFFFFF && ((unsigned int)v248 & 0x7FFFFF) != 0x7FFFFF )
                {
                  v139 = sub_140F5C7E0();
                  if ( v139 != 0 && *(__int64 **)(v139 + 48) == a1 )
                  {
                    v141 = sub_14083D4F0(v140);
                    v247 = 1416521062;
                    v246 = v141 + 56;
                    sub_14083B5F0(&v151, &v246);
                    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v246 + 16LL))(v246, &v246);
                    v143 = sub_14083D4F0(v142);
                    v247 = 1413706612;
                    v246 = v143 + 56;
                    sub_14083B5F0(&v151, &v246);
                    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v246 + 16LL))(v246, &v246);
                    v145 = sub_14083D4F0(v144);
                    v247 = 1413696842;
                    v246 = v145 + 56;
                    sub_14083B5F0(&v151, &v246);
                    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v246 + 16LL))(v246, &v246);
                    if ( *((_BYTE *)a1 + 186) == 0 )
                    {
                      v147 = sub_14083D4F0(v146);
                      v247 = 1131636339;
                      v246 = v147 + 56;
                      sub_14083B5F0(&v151, &v246);
                      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v246 + 16LL))(v246, &v246);
                    }
                  }
                }
                sub_1407EAFE0(a1, v148, &v151);
                sub_14083DDA0(&v246, v148);
                sub_14083DFA0(v7, &v246);
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v246 + 16LL))(v246, &v246);
                (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v249[0] + 16LL))(v249[0], v249);
                sub_14083B0A0(&v151);
                sub_140833970(v148);
              }
              return (unsigned int)v5;
            }
            if ( a2 == 1952605036 )
            {
              sub_1411DE560(a1, &v148[1]);
              v148[0] = sub_141335F60();
              sub_14083DFA0(v7, v148);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
              goto LABEL_68;
            }
          }
          else
          {
            switch ( a2 )
            {
              case 1952666196:
                LODWORD(v148[1]) = 0;
                v148[0] = sub_14083D4F0(v15) + 40;
                sub_14083DFA0(v7, v148);
                (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
                LOBYTE(v5) = 1;
                if ( *((_BYTE *)a1 + 186) == 0 )
                {
                  v104 = (__int64 *)a1[35];
                  v105 = (__int64 *)a1[36];
                  if ( v104 != v105 )
                  {
                    v106 = 1049072;
                    while ( 1 )
                    {
                      v107 = *v104;
                      if ( *(__int64 **)(*v104 + 8) == a1 )
                      {
                        v108 = *(unsigned __int8 *)(v107 + 48);
                        if ( v108 <= 0x14 )
                        {
                          if ( _bittest(&v106, v108) )
                            break;
                        }
                      }
                      if ( ++v104 == v105 )
                        return (unsigned int)v5;
                    }
                    if ( *(_QWORD *)v107 != 0 )
                    {
                      if ( (__int64 *)sub_140E68C40() == a1 )
                      {
                        v110 = sub_14083D4F0(v109);
                        LODWORD(v148[1]) = 3;
                      }
                      else
                      {
                        v110 = sub_14083D4F0(v109);
                        LODWORD(v148[1]) = 13;
                      }
                      v148[0] = v110 + 40;
                      sub_14083DFA0(v7, v148);
                      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
                    }
                  }
                }
                return (unsigned int)v5;
              case 1953784439:
                sub_1411DE560(a1, v148);
                v111 = -16777216;
                if ( BYTE2(v148[0]) + BYTE1(v148[0]) + (unsigned int)LOBYTE(v148[0]) < 0x180 )
                  v111 = -1;
                v112 = sub_141335F60();
                LODWORD(v148[1]) = v111;
                v148[0] = v112;
                sub_14083DFA0(v7, v148);
                (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
                goto LABEL_68;
              case 1953784684:
                sub_1411DE680(a1, &v148[1]);
                v148[0] = sub_141335F60();
                sub_14083DFA0(v7, v148);
                (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
                goto LABEL_68;
              default:
                break;
            }
          }
          goto LABEL_362;
        }
        if ( a2 <= 1883333483 )
        {
          if ( a2 == 1718185076 )
            goto LABEL_234;
          if ( a2 != 1818848875 )
            goto LABEL_362;
LABEL_237:
          LODWORD(v5) = 0;
          return (unsigned int)v5;
        }
        if ( a2 != 1883333484 && a2 != 1884578668 )
          goto LABEL_362;
LABEL_262:
        sub_1411DE060(a1, v148);
        sub_14083DB80(&v151, v148);
        sub_14083DFA0(v7, &v151);
        (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v151 + 16LL))(v151, &v151);
LABEL_263:
        sub_14083B0A0(v148);
        goto LABEL_68;
      }
      if ( a2 > 1417044847 )
      {
        if ( a2 > 1684172396 )
        {
          if ( a2 == 1684172397 )
          {
            v88 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *))(*a1 + 368))(a1);
            v90 = sub_14083D4F0(v89);
            v148[1] = 0;
            if ( &v148[1] != v88 )
            {
              v91 = *v88;
              if ( *v88 != 0 )
                _InterlockedIncrement((volatile signed __int32 *)(v91 - 4));
              v148[1] = v91;
            }
            v148[0] = v90 + 136;
            sub_14083DFA0(v7, v148);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
            v92 = *(_DWORD **)(*(__int64 (__fastcall **)(__int64 *))(*a1 + 368))(a1);
            if ( v92 != nullptr )
            {
              LOBYTE(v5) = 1;
              if ( *v92 != 0 )
                return (unsigned int)v5;
            }
            v93 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *))(*a1 + 376))(a1);
            v55 = sub_14083D4F0(v94);
            v148[1] = 0;
            if ( &v148[1] != v93 )
            {
              v95 = *v93;
              if ( *v93 != 0 )
                _InterlockedIncrement((volatile signed __int32 *)(v95 - 4));
              v148[1] = v95;
            }
            goto LABEL_329;
          }
          if ( a2 != 1684303986 )
            goto LABEL_362;
          v60 = (_QWORD *)a1[3];
          if ( v60 != (_QWORD *)a1[4] && *v60 != 0 )
            return (*(__int64 (__fastcall **)(_QWORD, __int64, _QWORD *))(*(_QWORD *)*v60 + 16LL))(*v60, 1684303986, v7);
          goto LABEL_237;
        }
        if ( a2 != 1417044848 )
        {
          if ( a2 != 1417048944 )
            goto LABEL_362;
          v5 = (char **)v148;
          sub_1407C9510(v148);
          v37 = (char **)a1[3];
          if ( v37 != (char **)a1[4] )
          {
            v38 = *v37;
            if ( *v37 != nullptr && *((_BYTE *)a1 + 186) == 0 )
            {
              v39 = sub_1411A3FA0(*v37);
              if ( v39 != 0 )
              {
                v41 = *(_QWORD *)(v39 + 880) + 3096LL;
                v151 = v38;
                v152 = (char *)v41;
                v153 = (char *)v148;
                LOBYTE(v40) = 7;
                sub_1411F4C60(&v151, v40);
                LOBYTE(v42) = 6;
                sub_1411F4C60(&v151, v42);
                LOBYTE(v43) = 5;
                sub_1411F4C60(&v151, v43);
                LOBYTE(v44) = 4;
                sub_1411F4C60(&v151, v44);
                if ( *((_QWORD *)v38 + 6) != 0 )
                {
                  v46 = *((_QWORD *)v38 + 10);
                  if ( v46 != 0 )
                  {
                    v47 = *(_QWORD *)(v46 + 176);
                    if ( v47 != 0 && (sub_140931AC0(*(_QWORD *)(v46 + 176)) != 0 || sub_140945390(v47, 0, 0) != 0) )
                    {
                      LOBYTE(v45) = 3;
                      sub_1411F4C60(&v151, v45);
                    }
                    LOBYTE(v45) = 2;
                    sub_1411F4C60(&v151, v45);
                  }
                }
                LOBYTE(v45) = 1;
                sub_1411F4C60(&v151, v45);
              }
            }
          }
          sub_14083DB80(&v151, v148);
          sub_14083DFA0(v7, &v151);
          (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v151 + 16LL))(v151, &v151);
          goto LABEL_263;
        }
        v57 = a1;
        v58 = 1417044848;
        return sub_1411F4BD0(v57, 0, v58, v7);
      }
      if ( a2 <= 1415795570 )
      {
        if ( a2 != 1414947681 )
        {
          if ( a2 == 1415792242 )
          {
            LOBYTE(v148[1]) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)qword_141B5FD40 + 72LL))(
                                qword_141B5FD40,
                                a1);
            v148[0] = sub_14083D4F0(v33) + 24;
            sub_14083DFA0(v7, v148);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
            goto LABEL_68;
          }
          goto LABEL_362;
        }
        goto LABEL_234;
      }
      if ( a2 == 1415795571 )
      {
        sub_1407C9510(&v248);
        for ( i = 0; i != 2184; i += 24 )
          sub_1407C9510(&v150[i + 3856]);
        for ( j = 0; j != 492; j += 3 )
          sub_1407C9510(&v148[j]);
        v83 = a1[4] - a1[3];
        if ( v83 != 0 )
        {
          v84 = v83 >> 3;
          v85 = 1;
          if ( v84 >= 2 )
            v85 = v84;
          for ( k = 0; k != v85; ++k )
          {
            v87 = *(_QWORD *)(a1[3] + 8 * k);
            if ( v87 != 0 && (*((_BYTE *)a1 + 186) != 1 || sub_140FE8230() == 0 || v87 == sub_140FE8230()) )
              sub_1411BCD80(v87, &v151, v148);
          }
        }
        sub_1407C9510(&v246);
        v99 = &v151;
        for ( m = 0; m != 91; ++m )
        {
          if ( *v99 != v99[1] )
          {
            sub_14083DB80(v244, v99);
            sub_140835380(&v246, (unsigned int)m, v244);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v244[0] + 16LL))(v244[0], v244);
          }
          v99 += 3;
        }
        sub_1407C9510(v244);
        v129 = v148;
        v5 = nullptr;
        do
        {
          if ( *v129 != v129[1] )
          {
            sub_14083DB80(v245, v129);
            sub_140835380(v244, (unsigned int)v5, v245);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v245[0] + 16LL))(v245[0], v245);
          }
          v5 = (char **)((char *)v5 + 1);
          v129 += 3;
        }
        while ( v5 != (char **)164 );
        sub_14083DDA0(v245, &v246);
        sub_140835380(&v248, 1128885843, v245);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v245[0] + 16LL))(v245[0], v245);
        sub_14083DDA0(v245, v244);
        sub_140835380(&v248, 1128623187, v245);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v245[0] + 16LL))(v245[0], v245);
        sub_14083DDA0(v245, &v248);
        sub_14083DFA0(v7, v245);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v245[0] + 16LL))(v245[0], v245);
        sub_140833970(v244);
        sub_140833970(&v246);
        for ( n = 489; n != -3; n -= 3 )
          sub_14083B0A0(&v148[n]);
        sub_14083B0A0(&v243);
        sub_14083B0A0(&v242);
        sub_14083B0A0(&v241);
        sub_14083B0A0(&v240);
        sub_14083B0A0(&v239);
        sub_14083B0A0(&v238);
        sub_14083B0A0(&v237);
        sub_14083B0A0(&v236);
        sub_14083B0A0(&v235);
        sub_14083B0A0(&v234);
        sub_14083B0A0(&v233);
        sub_14083B0A0(&v232);
        sub_14083B0A0(&v231);
        sub_14083B0A0(&v230);
        sub_14083B0A0(&v229);
        sub_14083B0A0(&v228);
        sub_14083B0A0(&v227);
        sub_14083B0A0(&v226);
        sub_14083B0A0(&v225);
        sub_14083B0A0(&v224);
        sub_14083B0A0(&v223);
        sub_14083B0A0(&v222);
        sub_14083B0A0(&v221);
        sub_14083B0A0(&v220);
        sub_14083B0A0(&v219);
        sub_14083B0A0(&v218);
        sub_14083B0A0(&v217);
        sub_14083B0A0(&v216);
        sub_14083B0A0(&v215);
        sub_14083B0A0(&v214);
        sub_14083B0A0(&v213);
        sub_14083B0A0(&v212);
        sub_14083B0A0(&v211);
        sub_14083B0A0(&v210);
        sub_14083B0A0(&v209);
        sub_14083B0A0(&v208);
        sub_14083B0A0(&v207);
        sub_14083B0A0(&v206);
        sub_14083B0A0(&v205);
        sub_14083B0A0(&v204);
        sub_14083B0A0(&v203);
        sub_14083B0A0(&v202);
        sub_14083B0A0(&v201);
        sub_14083B0A0(&v200);
        sub_14083B0A0(&v199);
        sub_14083B0A0(&v198);
        sub_14083B0A0(&v197);
        sub_14083B0A0(&v196);
        sub_14083B0A0(&v195);
        sub_14083B0A0(&v194);
        sub_14083B0A0(&v193);
        sub_14083B0A0(&v192);
        sub_14083B0A0(&v191);
        sub_14083B0A0(&v190);
        sub_14083B0A0(&v189);
        sub_14083B0A0(&v188);
        sub_14083B0A0(&v187);
        sub_14083B0A0(&v186);
        sub_14083B0A0(&v185);
        sub_14083B0A0(&v184);
        sub_14083B0A0(&v183);
        sub_14083B0A0(&v182);
        sub_14083B0A0(&v181);
        sub_14083B0A0(&v180);
        sub_14083B0A0(&v179);
        sub_14083B0A0(&v178);
        sub_14083B0A0(&v177);
        sub_14083B0A0(&v176);
        sub_14083B0A0(&v175);
        sub_14083B0A0(&v174);
        sub_14083B0A0(&v173);
        sub_14083B0A0(&v172);
        sub_14083B0A0(&v171);
        sub_14083B0A0(&v170);
        sub_14083B0A0(&v169);
        sub_14083B0A0(&v168);
        sub_14083B0A0(&v167);
        sub_14083B0A0(&v166);
        sub_14083B0A0(&v165);
        sub_14083B0A0(&v164);
        sub_14083B0A0(&v163);
        sub_14083B0A0(&v162);
        sub_14083B0A0(&v161);
        sub_14083B0A0(&v160);
        sub_14083B0A0(&v159);
        sub_14083B0A0(&v158);
        sub_14083B0A0(&v157);
        sub_14083B0A0(&v156);
        sub_14083B0A0(&v155);
        sub_14083B0A0(&v154);
        sub_14083B0A0(&v151);
        sub_140833970(&v248);
        goto LABEL_68;
      }
      if ( a2 == 1415799152 )
      {
        v57 = a1;
        v58 = 1415799152;
        return sub_1411F4BD0(v57, 0, v58, v7);
      }
    }
LABEL_362:
    v64 = *(__int64 (__fastcall **)(__int64 *, _QWORD, _QWORD *))(*a1 + 448);
    v63 = a1;
    return v64(v63, (unsigned int)a2, v7);
  }
  if ( a2 <= 1131245152 )
  {
    if ( a2 <= 1129927522 )
    {
      switch ( a2 )
      {
        case 1129926755:
        case 1129926756:
        case 1129926765:
        case 1129926766:
        case 1129926767:
        case 1129926768:
          goto LABEL_394;
        case 1129926757:
        case 1129926758:
        case 1129926759:
        case 1129926760:
        case 1129926761:
        case 1129926762:
        case 1129926763:
        case 1129926764:
          goto LABEL_362;
        default:
          if ( a2 == 1129797491 )
            goto LABEL_394;
          goto LABEL_362;
      }
    }
    if ( a2 <= 1130458227 )
    {
      switch ( a2 )
      {
        case 1129927523:
        case 1129927524:
        case 1129927533:
        case 1129927534:
        case 1129927535:
        case 1129927536:
          goto LABEL_394;
        default:
          goto LABEL_362;
      }
    }
    switch ( a2 )
    {
      case 1130458228:
        v148[0] = a1;
        v151 = (char *)v148;
        sub_141200110(&v151, v7);
        goto LABEL_68;
      case 1130460260:
        LODWORD(v148[1]) = *(_DWORD *)(a1[22] + 104);
        v148[0] = sub_14083D4F0(v15) + 40;
        sub_14083DFA0(v7, v148);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
        goto LABEL_68;
      case 1130591337:
        if ( (*(__int64 (__fastcall **)(__int64 *))(*a1 + 416))(a1) != 0 )
          v52 = *(_QWORD *)((*(__int64 (__fastcall **)(__int64 *))(*a1 + 416))(a1) + 240);
        else
          v52 = 0;
        sub_140FE7860(v52, v7);
        goto LABEL_68;
      default:
        break;
    }
    goto LABEL_362;
  }
  if ( a2 <= 1313302125 )
  {
    if ( a2 > 1312908909 )
    {
      if ( a2 > 1312911460 )
      {
        if ( a2 != 1312911461 && a2 != 1312912238 )
          goto LABEL_362;
      }
      else if ( a2 != 1312908910 && a2 != 1312909164 )
      {
        goto LABEL_362;
      }
      return sub_1411EA620(a1, (unsigned int)a2, v7);
    }
    if ( a2 <= 1131309933 )
    {
      if ( a2 == 1131245153 )
      {
        LODWORD(v148[1]) = *(_DWORD *)(a1[22] + 108);
        v148[0] = sub_14083D4F0(v15) + 40;
        sub_14083DFA0(v7, v148);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
        goto LABEL_68;
      }
      if ( a2 == 1131247713 )
      {
        LODWORD(v148[1]) = *(_DWORD *)(a1[22] + 112);
        v148[0] = sub_14083D4F0(v15) + 40;
        sub_14083DFA0(v7, v148);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
        goto LABEL_68;
      }
      goto LABEL_362;
    }
    if ( a2 != 1131309934 )
    {
      if ( a2 == 1145392197 )
      {
        LOBYTE(v148[1]) = a1[3] == a1[4];
        v148[0] = sub_14083D4F0(v15) + 24;
        sub_14083DFA0(v7, v148);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
        goto LABEL_68;
      }
      goto LABEL_362;
    }
LABEL_247:
    v65 = *(_DWORD **)(a1[22] + 144);
    if ( v65 == nullptr || *v65 == 0 || (LOBYTE(v14) = 1, (unsigned __int8)sub_1411D7240(a1, v14) == 0) )
    {
      v68 = sub_14083D4F0(v15);
      v148[1] = 0;
      v69 = qword_141B59EE8;
      if ( qword_141B59EE8 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE8 - 4));
      v148[1] = v69;
      v148[0] = v68 + 136;
      sub_14083DFA0(v7, v148);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
      goto LABEL_68;
    }
    v66 = (__int64 *)(a1[22] + 144);
    v55 = sub_14083D4F0(v15);
    v148[1] = 0;
    if ( &v148[1] != v66 )
    {
      v67 = *v66;
      if ( *v66 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v67 - 4));
      v148[1] = v67;
    }
    goto LABEL_329;
  }
  if ( a2 <= 1413701999 )
  {
    if ( a2 > 1313304676 )
    {
      if ( a2 != 1313304677 && a2 != 1313305454 )
        goto LABEL_362;
    }
    else if ( a2 != 1313302126 && a2 != 1313302380 )
    {
      goto LABEL_362;
    }
    return sub_1411EA620(a1, (unsigned int)a2, v7);
  }
  if ( a2 > 1413703795 )
  {
    if ( a2 != 1413703796 )
    {
      if ( a2 == 1413704807 )
      {
        LODWORD(v148[1]) = (*(char (__fastcall **)(__int64 *))(*a1 + 384))(a1);
        v148[0] = sub_14083D4F0(v103) + 40;
        sub_14083DFA0(v7, v148);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
        goto LABEL_68;
      }
      if ( a2 == 1413704814 )
      {
        (*(void (__fastcall **)(__int64 *, volatile signed __int32 **))(*a1 + 200))(a1, &v248);
        v16 = (int)v248;
        v246 = 0;
        sub_140809040(&v246, 0x141906485LL, 0xFFFFFFFFLL);
        sub_14081AF20(v16, (unsigned int)&v151, (unsigned int)&v246, 0, 0, 0);
        v18 = sub_14083D4F0(v17);
        v148[1] = 0;
        v19 = v151;
        if ( v151 != nullptr )
          _InterlockedIncrement((volatile signed __int32 *)v151 - 1);
        v148[1] = v19;
        v148[0] = v18 + 136;
        sub_14083DFA0(v7, v148);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
        v21 = v151;
        if ( v151 != nullptr && _InterlockedDecrement((volatile signed __int32 *)v151 - 1) == 0 )
          sub_1412EC9A0(v21 - 4, v20);
        v22 = v246;
        if ( v246 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v246 - 4)) == 0 )
          sub_1412EC9A0(v22 - 4, v20);
        v23 = (void (__fastcall ***)(_QWORD, __int64))v248;
        if ( v248 != nullptr && _InterlockedDecrement(v248 + 2) == 0 )
          (**v23)(v23, 1);
        goto LABEL_68;
      }
      goto LABEL_362;
    }
    v101 = (__int64 *)(a1[22] + 152);
    v55 = sub_14083D4F0(v15);
    v148[1] = 0;
    if ( &v148[1] != v101 )
    {
      v102 = *v101;
      if ( *v101 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v102 - 4));
      v148[1] = v102;
    }
LABEL_329:
    v148[0] = v55 + 136;
    sub_14083DFA0(v7, v148);
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
    goto LABEL_68;
  }
  if ( a2 != 1413702000 )
  {
    if ( a2 == 1413703790 )
    {
      v61 = *(_DWORD **)(a1[22] + 144);
      LOBYTE(v5) = 1;
      if ( v61 != nullptr && *v61 != 0 )
      {
        LOBYTE(v14) = 1;
        LODWORD(v5) = sub_1411D7240(a1, v14);
        LOBYTE(v5) = (unsigned __int8)v5 ^ 1;
      }
      LOBYTE(v148[1]) = (_BYTE)v5;
      v148[0] = sub_14083D4F0(v15) + 24;
      sub_14083DFA0(v7, v148);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v148[0] + 16LL))(v148[0], v148);
      goto LABEL_68;
    }
    goto LABEL_362;
  }
LABEL_234:
  v62 = (__int64 **)a1[3];
  if ( v62 == (__int64 **)a1[4] )
    goto LABEL_237;
  v63 = *v62;
  if ( *v62 == nullptr )
    goto LABEL_237;
  v64 = *(__int64 (__fastcall **)(__int64 *, _QWORD, _QWORD *))(*v63 + 16);
  return v64(v63, (unsigned int)a2, v7);
}
