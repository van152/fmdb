__int64 __fastcall sub_141045D50(char *a1, int a2, __int64 **a3)
{
  __int64 m; // rdi
  __int64 v6; // rdx
  volatile signed __int32 **v7; // rbx
  volatile signed __int32 *v8; // rax
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v10; // rsi
  volatile signed __int32 *v11; // rsi
  char v12; // al
  __int64 *v13; // rcx
  __int64 v14; // rbp
  __int64 *v15; // rbx
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // rdx
  __int64 v19; // rdx
  volatile signed __int32 **v20; // rbx
  volatile signed __int32 *v21; // rax
  volatile signed __int32 *v22; // rcx
  volatile signed __int32 *v23; // rsi
  volatile signed __int32 *v24; // rsi
  __int64 v25; // rdx
  volatile signed __int32 **v26; // rbx
  volatile signed __int32 *v27; // rax
  volatile signed __int32 *v28; // rcx
  volatile signed __int32 *v29; // rsi
  volatile signed __int32 *v30; // rsi
  char v31; // al
  __int64 *v32; // rcx
  __int64 v33; // rbp
  __int64 *v34; // rbx
  __int64 v35; // rax
  __int64 v36; // rcx
  __int64 v37; // rdx
  __int64 v38; // rcx
  __int64 v39; // rax
  char v40; // al
  __int64 *v41; // rcx
  __int64 v42; // rbp
  __int64 *v43; // rbx
  __int64 v44; // rax
  __int64 v45; // rcx
  __int64 v46; // rdx
  unsigned int v47; // eax
  __int64 v48; // rdx
  volatile signed __int32 *v49; // rax
  volatile signed __int32 *v50; // rcx
  volatile signed __int32 *v51; // rsi
  volatile signed __int32 *v52; // rsi
  volatile signed __int32 **v53; // rbx
  volatile signed __int32 *v54; // rax
  volatile signed __int32 *v55; // rcx
  volatile signed __int32 *v56; // rsi
  volatile signed __int32 *v57; // rsi
  unsigned __int64 v58; // rdx
  _QWORD *v59; // r15
  __int64 v60; // rax
  __int64 v61; // rsi
  _QWORD *v62; // rbp
  __int64 v63; // rcx
  __int64 v64; // rax
  unsigned int v65; // edx
  __int64 v66; // rsi
  _QWORD *v67; // rbx
  __int64 v68; // rdx
  _QWORD *v69; // r15
  __int64 v70; // rax
  unsigned __int64 v71; // rax
  __int64 v72; // r12
  __int64 j; // rsi
  __int64 v74; // rax
  __int64 v75; // rbx
  __int64 v76; // rbp
  __int64 v77; // rbp
  __int64 v78; // r14
  __int64 *v79; // r8
  __int64 *v80; // r14
  __int64 v81; // rax
  __int64 *v82; // rcx
  __int64 v83; // rax
  __int64 v84; // rcx
  int v85; // edx
  __int64 v86; // rax
  unsigned __int64 v87; // rax
  __int64 v88; // r12
  __int64 k; // r13
  __int64 *v90; // rdi
  _QWORD *v91; // rsi
  __int64 v92; // rbx
  __int64 v93; // rsi
  __int64 v94; // rbx
  __int64 v95; // rsi
  __int64 v96; // r14
  __int64 *v97; // r8
  __int64 v98; // rax
  unsigned __int64 v99; // rax
  __int64 v100; // rcx
  __int64 *v101; // rbx
  _QWORD *v102; // rsi
  __int64 v103; // rax
  __int64 *v104; // rcx
  __int64 v105; // rax
  __int64 v106; // rbp
  _QWORD *v107; // rbx
  __int64 v108; // r14
  __int64 v109; // r14
  __int64 v110; // r15
  int v111; // eax
  __int64 v112; // rsi
  __int64 v113; // rax
  __int64 v114; // rax
  __int64 v115; // rax
  __int64 v116; // rcx
  char v117; // al
  _QWORD *v118; // rax
  __int64 v119; // rbp
  __int64 v120; // rsi
  __int64 v121; // rbp
  __int64 v122; // r13
  __int64 *v123; // rbx
  __int64 v124; // r14
  __int64 v125; // rcx
  __int64 v126; // rcx
  char v127; // al
  _QWORD *v128; // rax
  __int64 v129; // rbp
  __int64 v130; // rsi
  __int64 v131; // rbp
  __int64 v132; // r13
  __int64 *v133; // rbx
  __int64 v134; // r14
  __int64 v135; // rcx
  _DWORD *v136; // rcx
  __int64 v137; // rsi
  signed __int32 v138; // eax
  _DWORD *v139; // rcx
  __int64 v140; // rcx
  __int64 v141; // rax
  __int64 v142; // rax
  __int64 *v143; // rsi
  __int64 v144; // rcx
  __int64 v145; // rax
  __int64 v146; // rax
  volatile signed __int32 *v147; // rdx
  __int64 v148; // rax
  volatile signed __int32 *v149; // rcx
  volatile signed __int32 *v150; // rbx
  __int64 v151; // rcx
  char v152; // al
  _QWORD *v153; // rax
  __int64 v154; // rbp
  __int64 v155; // rsi
  __int64 v156; // rbp
  __int64 v157; // r13
  __int64 *v158; // rbx
  __int64 v159; // r14
  __int64 v160; // rcx
  _DWORD *v161; // rcx
  __int64 v162; // rsi
  signed __int32 v163; // eax
  _DWORD *v164; // rcx
  __int64 *v165; // rdx
  __int64 *v166; // rdx
  __int64 *v167; // rdx
  unsigned int v168; // eax
  char *v169; // rax
  __int128 *v170; // rbx
  char *v171; // rcx
  __int64 v172; // r8
  int v173; // eax
  __int64 v174; // rbp
  char v175; // al
  __int16 v176; // cx
  __int64 *v178; // r14
  __int64 *v179; // rsi
  __int64 *v180; // rax
  __int64 v181; // rsi
  _QWORD *v182; // rbx
  __int64 v183; // rax
  __int64 v184; // rcx
  __int64 *v185; // rdx
  __int64 v186; // rcx
  __int64 *v187; // r14
  __int64 v188; // rax
  __int64 v189; // rax
  __int64 v190; // rcx
  __int64 *v191; // rdx
  __int64 v192; // rcx
  __int64 v193; // rdx
  __int64 *v194; // rax
  __int64 v195; // rax
  unsigned __int64 v196; // rsi
  __int64 v197; // rbx
  _QWORD *v198; // rbp
  __int64 v199; // rcx
  __int64 v200; // rax
  __int64 v201; // rcx
  __int64 v202; // rax
  __int64 v203; // rcx
  __int64 *v204; // rdx
  __int64 v205; // rcx
  __int64 v206; // rdx
  __int64 *v207; // rax
  unsigned int v208; // ecx
  __int64 v209; // rsi
  __int64 v210; // rbx
  _QWORD *v211; // rbp
  __int64 v212; // rax
  __int64 v213; // rcx
  __int64 v214; // rax
  __int64 v215; // rcx
  __int64 *v216; // rdx
  __int64 v217; // rcx
  __int64 v218; // rdx
  __int64 *v219; // rax
  __int64 v220; // rsi
  char *v221; // rax
  __int128 *v222; // r15
  char *v223; // rcx
  __int64 v224; // r8
  int v225; // eax
  __int64 v226; // rdx
  __int64 v227; // rbx
  __int64 v228; // rax
  __int64 v229; // rcx
  __int64 *v230; // rbx
  int v231; // eax
  __int64 v232; // rcx
  __int64 v233; // rbp
  __int64 v234; // rcx
  __int64 *v235; // rdx
  __int64 v236; // rax
  __int64 *v237; // rbx
  int v238; // eax
  _QWORD *v239; // rsi
  __int64 v240; // rcx
  _QWORD *v241; // rsi
  __int64 v242; // r15
  _QWORD *v243; // rsi
  __int64 v244; // rbp
  __int64 v245; // r15
  __int64 v246; // rbp
  __int64 v247; // rbx
  __int64 *v248; // r8
  int v249; // eax
  __int64 v250; // r14
  __int64 v251; // r15
  __int64 v252; // rbp
  __int64 v253; // rcx
  __int64 *v254; // rdx
  __int64 v255; // rax
  int v256; // eax
  _QWORD *v257; // rsi
  __int64 v258; // rcx
  __int64 **v259; // rax
  __int64 *v260; // r12
  _QWORD *v261; // rbx
  __int64 v262; // r13
  __int64 v263; // rax
  __int64 *v264; // rcx
  __int64 v265; // rax
  __int64 v266; // rbp
  __int64 v267; // rbp
  __int64 v268; // r15
  __int64 *v269; // rdx
  int v270; // eax
  __int64 v271; // rbx
  int v272; // eax
  char *v273; // rdi
  __int64 v274; // rbp
  __int64 v275; // rcx
  __int64 *v276; // rdx
  __int64 v277; // rax
  __int64 *v278; // rbx
  int v279; // eax
  char *v280; // rdx
  __int128 *v281; // rsi
  char *v282; // rcx
  __int64 v283; // r8
  int v284; // eax
  __int64 v285; // rdx
  __int64 i; // rbp
  _QWORD *v287; // rbx
  __int64 v288; // rbp
  __int64 v289; // rbp
  __int64 v290; // rsi
  __int64 *v291; // r8
  unsigned int v292; // eax
  __int64 v293; // r15
  int v294; // eax
  __int64 v295; // rsi
  unsigned int v296; // eax
  __int128 v297; // [rsp+20h] [rbp-A8h] BYREF
  __int16 v298; // [rsp+30h] [rbp-98h]
  int v299; // [rsp+32h] [rbp-96h]
  __int16 v300; // [rsp+36h] [rbp-92h]
  __int128 *v301; // [rsp+40h] [rbp-88h] BYREF
  char **v302; // [rsp+48h] [rbp-80h] BYREF
  _QWORD *v303; // [rsp+50h] [rbp-78h] BYREF
  char *v304; // [rsp+58h] [rbp-70h] BYREF
  __int64 *v305; // [rsp+60h] [rbp-68h]
  __int64 v306; // [rsp+68h] [rbp-60h]

  if ( a2 <= 1315398515 )
  {
    if ( a2 <= 1315140712 )
    {
      if ( a2 <= 1315006321 )
      {
        if ( a2 != 1311992942 )
        {
          if ( a2 != 1313162049 )
          {
            if ( a2 == 1313162066 )
            {
              *(_QWORD *)&v297 = a1;
              *((_QWORD *)&v297 + 1) = a1;
              LOBYTE(v298) = 0;
LABEL_104:
              LODWORD(m) = sub_1415D0B30(&v297, a3);
              return (unsigned int)m;
            }
            goto LABEL_114;
          }
          *(_QWORD *)&v297 = a1;
          *((_QWORD *)&v297 + 1) = a1;
          LOBYTE(v298) = 0;
LABEL_102:
          LODWORD(m) = sub_1415D0D40(&v297, a3);
          return (unsigned int)m;
        }
        m = (__int64)&v297;
        (*(void (__fastcall **)(__int64 *, __int128 *, __int64 **))(**a3 + 128))(*a3, &v297, a3);
        v26 = (volatile signed __int32 **)(a1 + 40);
        if ( a1 + 40 != (char *)&v297 )
        {
          v25 = v297;
          v27 = *v26;
          v28 = *v26 - 1;
          if ( *v26 == nullptr )
            v28 = nullptr;
          v29 = (volatile signed __int32 *)(v297 - 4);
          if ( (_QWORD)v297 != 0 )
          {
            if ( v27 != nullptr && _InterlockedDecrement(v28) == 0 )
              sub_1412EC9A0(v28, v25);
            *v26 = nullptr;
            _InterlockedIncrement(v29);
            v30 = v29 + 1;
          }
          else
          {
            if ( v27 != nullptr && _InterlockedDecrement(v28) == 0 )
              sub_1412EC9A0(v28, v25);
            v30 = nullptr;
          }
          *v26 = v30;
        }
        v140 = v297;
        if ( (_QWORD)v297 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v297 - 4)) == 0 )
          sub_1412EC9A0(v140 - 4, v25);
        v141 = sub_140E78A80();
        v142 = sub_140FF53C0(v141, *((unsigned int *)a1 + 3));
        LOBYTE(m) = 1;
        if ( v142 == 0 )
          return (unsigned int)m;
        v143 = (__int64 *)(v142 + 24);
        if ( (volatile signed __int32 **)(v142 + 24) == v26 )
          return (unsigned int)m;
LABEL_269:
        v147 = *v26;
        v148 = *v143;
        v149 = (volatile signed __int32 *)(*v143 - 4);
        if ( *v143 == 0 )
          v149 = nullptr;
        v150 = v147 - 1;
        if ( v147 != nullptr )
        {
          if ( v148 != 0 && _InterlockedDecrement(v149) == 0 )
            sub_1412EC9A0(v149, v147);
          *v143 = 0;
          _InterlockedIncrement(v150);
          *v143 = (__int64)(v150 + 1);
        }
        else
        {
          if ( v148 != 0 && _InterlockedDecrement(v149) == 0 )
            sub_1412EC9A0(v149, 0);
          *v143 = 0;
        }
        return (unsigned int)m;
      }
      if ( a2 != 1315006322 )
      {
        if ( a2 == 1315139177 )
        {
          v47 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3) - 1;
          if ( v47 > 6 )
            *((_QWORD *)a1 + 30) = 0;
          else
            *((_QWORD *)a1 + 30) = *(_QWORD *)(**(_QWORD **)(qword_141B5FDC8 + 128) + 8LL * v47);
          goto LABEL_346;
        }
        if ( a2 == 1315139689 )
        {
          m = qword_141B5FDB0;
          sub_140FE7960(&v297, a3, 1667855481);
          *((_QWORD *)a1 + 29) = sub_140FA3700(m, &v297);
          goto LABEL_346;
        }
        goto LABEL_114;
      }
      v301 = (__int128 *)a1;
      v302 = (char **)a1;
      *(_QWORD *)&v297 = &v301;
      *((_QWORD *)&v297 + 1) = &v302;
      v40 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
      v41 = *a3;
      v42 = **a3;
      if ( v40 == 10 )
      {
        LODWORD(m) = 0;
        v43 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v42 + 176))(v41, a3, 0);
        v44 = *v43;
        v45 = v43[1];
        if ( *v43 == v45 )
          return (unsigned int)m;
        m = (__int64)&v297 + 8;
        v46 = *v43;
        while ( *(_DWORD *)v46 != 1819504496 )
        {
          v46 += 16;
          if ( v46 == v45 )
            goto LABEL_607;
        }
        if ( v46 != v45 && *(_QWORD *)(v46 + 8) != 0 )
        {
          v167 = nullptr;
          while ( *(_DWORD *)v44 != 1819504496 )
          {
            v44 += 16;
            if ( v44 == v45 )
              goto LABEL_379;
          }
          if ( v44 == v45 )
            v167 = nullptr;
          else
            v167 = *(__int64 **)(v44 + 8);
LABEL_379:
          v187 = &qword_141B5A4A0;
          if ( v167 == nullptr )
            v167 = &qword_141B5A4A0;
          switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v167 + 64LL))(*v167) )
          {
            case 0u:
              v188 = sub_1415D10E0(&v301, v43);
              if ( v188 == 0 )
                v188 = sub_1415D0EF0(&v301);
              LOBYTE(m) = v188 != 0;
              return (unsigned int)m;
            case 1u:
              v214 = *v43;
              v215 = v43[1];
              v216 = nullptr;
              if ( *v43 != v215 )
              {
                while ( *(_DWORD *)v214 != 1869379180 )
                {
                  v214 += 16;
                  if ( v214 == v215 )
                    goto LABEL_535;
                }
                if ( v214 == v215 )
                  v216 = nullptr;
                else
                  v216 = *(__int64 **)(v214 + 8);
              }
LABEL_535:
              if ( v216 == nullptr )
                v216 = &qword_141B5A4A0;
              v272 = sub_1410506F0((char *)&v297 + 8, v216);
              if ( v272 < 0 )
                goto LABEL_607;
              v273 = v302[24];
              if ( v273 == nullptr )
                goto LABEL_607;
              m = (__int64)&v273[16 * v272];
              v274 = *v43;
              v275 = v43[1];
              v276 = nullptr;
              if ( *v43 == v275 )
              {
                v278 = &qword_141B5A4A0;
              }
              else
              {
                v277 = *v43;
                while ( *(_DWORD *)v277 != 1986096245 )
                {
                  v277 += 16;
                  if ( v277 == v275 )
                    goto LABEL_589;
                }
                if ( v277 == v275 )
                  v276 = nullptr;
                else
                  v276 = *(__int64 **)(v277 + 8);
LABEL_589:
                v278 = &qword_141B5A4A0;
                if ( v276 != nullptr )
                  v278 = v276;
                v276 = nullptr;
                while ( *(_DWORD *)v274 != 1768169504 )
                {
                  v274 += 16;
                  if ( v274 == v275 )
                    goto LABEL_610;
                }
                if ( v274 == v275 )
                  v276 = nullptr;
                else
                  v276 = *(__int64 **)(v274 + 8);
              }
LABEL_610:
              if ( v276 != nullptr )
                v187 = v276;
              v296 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v187 + 80LL))(*v187, v187);
              LODWORD(m) = sub_141070E80(m, v296, v278);
              return (unsigned int)m;
            case 2u:
              v217 = *v43;
              v218 = v43[1];
              v219 = nullptr;
              if ( *v43 != v218 )
              {
                while ( *(_DWORD *)v217 != 1869379180 )
                {
                  v217 += 16;
                  if ( v217 == v218 )
                    goto LABEL_548;
                }
                if ( v217 == v218 )
                  v219 = nullptr;
                else
                  v219 = *(__int64 **)(v217 + 8);
              }
LABEL_548:
              if ( v219 != nullptr )
                v187 = v219;
              v279 = sub_1410506F0((char *)&v297 + 8, v187);
              if ( v279 < 0 )
                goto LABEL_607;
              v280 = v302[24];
              if ( v280 == nullptr )
                goto LABEL_607;
              v281 = v301;
              v282 = *((char **)v301 + 24);
              LOBYTE(m) = 1;
              v283 = *((_QWORD *)v301 + 25) - (_QWORD)v282;
              if ( v283 != 0 )
              {
                v284 = *(_DWORD *)(*(_QWORD *)&v280[16 * v279] + 12LL);
                v285 = 1;
                if ( (unsigned __int64)(v283 >> 4) >= 2 )
                  v285 = v283 >> 4;
                for ( i = 0; *(_DWORD *)(*(_QWORD *)&v282[i] + 12LL) != v284; i += 16 )
                {
                  if ( --v285 == 0 )
                    return (unsigned int)m;
                }
                sub_141758A00(&v282[i], &v282[i + 16], v283 - i - 16);
                *((_QWORD *)v281 + 25) -= 16LL;
              }
              return (unsigned int)m;
            case 3u:
              LOBYTE(m) = 1;
              if ( (unsigned __int64)(unsigned int)(*((_DWORD *)v302 + 50) - *((_DWORD *)v302 + 48)) << 44 >> 48 == 0 )
                return (unsigned int)m;
              v220 = (__int64)((unsigned __int64)(unsigned int)(*((_DWORD *)v302 + 50) - *((_DWORD *)v302 + 48)) << 44) >> 48;
              do
              {
                --v220;
                v221 = v302[24];
                if ( v221 != nullptr )
                {
                  v222 = v301;
                  v223 = *((char **)v301 + 24);
                  v224 = *((_QWORD *)v301 + 25) - (_QWORD)v223;
                  if ( v224 != 0 )
                  {
                    v225 = *(_DWORD *)(*(_QWORD *)&v221[16 * (int)v220] + 12LL);
                    v226 = v224 >> 4;
                    if ( (unsigned __int64)(v224 >> 4) < 2 )
                      v226 = 1;
                    v227 = 0;
                    while ( *(_DWORD *)(*(_QWORD *)&v223[v227] + 12LL) != v225 )
                    {
                      v227 += 16;
                      if ( --v226 == 0 )
                        goto LABEL_431;
                    }
                    sub_141758A00(&v223[v227], &v223[v227 + 16], v224 - v227 - 16);
                    *((_QWORD *)v222 + 25) -= 16LL;
                  }
                }
LABEL_431:
                ;
              }
              while ( v220 != 0 );
              return (unsigned int)m;
            case 4u:
              v228 = *v43;
              v229 = v43[1];
              v230 = nullptr;
              if ( v228 == v229 )
                goto LABEL_561;
              break;
            case 5u:
              sub_140DD5C90(&v297, 0);
              goto LABEL_346;
            default:
              goto LABEL_607;
          }
          while ( *(_DWORD *)v228 != 1869379180 )
          {
            v228 += 16;
            if ( v228 == v229 )
              goto LABEL_561;
          }
          if ( v228 == v229 )
            v230 = nullptr;
          else
            v230 = *(__int64 **)(v228 + 8);
LABEL_561:
          m = sub_1415D0EF0(&v301);
          if ( m != 0 )
          {
            if ( v230 == nullptr )
              v230 = &qword_141B5A4A0;
            v287 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v230 + 176LL))(
                               *v230,
                               v230,
                               0);
            v288 = v287[1] - *v287;
            if ( v288 != 0 )
            {
              v289 = v288 >> 4;
              v290 = 8;
              do
              {
                v291 = *(__int64 **)(*v287 + v290);
                if ( v291 == nullptr )
                  v291 = &qword_141B5A4A0;
                sub_141070E80(m, *(unsigned int *)(*v287 + v290 - 8), v291);
                v290 += 16;
                --v289;
              }
              while ( v289 != 0 );
            }
          }
          LOBYTE(m) = m != 0;
          return (unsigned int)m;
        }
      }
      else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v42 + 8))(v41, a3) == 11 )
      {
        v69 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
        m = (unsigned __int64)(unsigned int)(*((_DWORD *)v302 + 50) - *((_DWORD *)v302 + 48)) << 44;
        if ( HIWORD(m) != 0 )
        {
          m >>= 48;
          do
          {
            --m;
            v169 = v302[24];
            if ( v169 != nullptr )
            {
              v170 = v301;
              v171 = *((char **)v301 + 24);
              v172 = *((_QWORD *)v301 + 25) - (_QWORD)v171;
              if ( v172 != 0 )
              {
                v173 = *(_DWORD *)(*(_QWORD *)&v169[16 * (int)m] + 12LL);
                v68 = v172 >> 4;
                if ( (unsigned __int64)(v172 >> 4) < 2 )
                  v68 = 1;
                v174 = 0;
                while ( *(_DWORD *)(*(_QWORD *)&v171[v174] + 12LL) != v173 )
                {
                  v174 += 16;
                  if ( --v68 == 0 )
                    goto LABEL_331;
                }
                sub_141758A00(&v171[v174], &v171[v174 + 16], v172 - v174 - 16);
                *((_QWORD *)v170 + 25) -= 16LL;
              }
            }
LABEL_331:
            ;
          }
          while ( m != 0 );
        }
        v70 = v69[1] - *v69;
        if ( v70 != 0 )
        {
          v71 = v70 >> 3;
          v72 = 1;
          if ( v71 >= 2 )
            v72 = v71;
          for ( j = 0; j != v72; ++j )
          {
            m = *(_QWORD *)(*v69 + 8 * j);
            v74 = sub_1415D0EF0(&v301);
            if ( v74 != 0 )
            {
              v75 = v74;
              if ( m == 0 )
                m = (__int64)&qword_141B5A4A0;
              m = (*(__int64 (__fastcall **)(_QWORD, __int64, _QWORD))(**(_QWORD **)m + 176LL))(*(_QWORD *)m, m, 0);
              v76 = *(_QWORD *)(m + 8) - *(_QWORD *)m;
              if ( v76 != 0 )
              {
                v77 = v76 >> 4;
                v78 = 8;
                do
                {
                  v79 = *(__int64 **)(*(_QWORD *)m + v78);
                  if ( v79 == nullptr )
                    v79 = &qword_141B5A4A0;
                  sub_141070E80(v75, *(unsigned int *)(*(_QWORD *)m + v78 - 8), v79);
                  v78 += 16;
                  --v77;
                }
                while ( v77 != 0 );
              }
            }
          }
        }
        v113 = qword_141B60C30;
        if ( qword_141B60C30 == qword_141B60C38 )
          goto LABEL_194;
        while ( *(_DWORD *)v113 != 1986359923 )
        {
          v113 += 16;
          if ( v113 == qword_141B60C38 )
            goto LABEL_194;
        }
        if ( v113 == qword_141B60C38 || (LOBYTE(m) = 1, *(_QWORD *)(v113 + 8) == 0) )
        {
LABEL_194:
          LOBYTE(m) = 1;
          LOBYTE(v68) = 1;
          sub_140DD5C90(&v297, v68);
        }
        return (unsigned int)m;
      }
LABEL_607:
      LODWORD(m) = 0;
      return (unsigned int)m;
    }
    if ( a2 <= 1315268160 )
    {
      switch ( a2 )
      {
        case 1315140713:
          m = qword_141B5FDC8;
          sub_140FE7960(&v297, a3, 1668247156);
          *((_QWORD *)a1 + 30) = sub_140FA3700(m, &v297);
          goto LABEL_346;
        case 1315140978:
          m = qword_141B5FDD8;
          sub_140FE7960(&v297, a3, 1668641394);
          *((_QWORD *)a1 + 32) = sub_140FA1860(m, &v297);
          goto LABEL_346;
        case 1315267430:
          a1[464] = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          goto LABEL_346;
        default:
          break;
      }
      goto LABEL_114;
    }
    switch ( a2 )
    {
      case 1315268161:
        *(_QWORD *)&v297 = a1;
        *((_QWORD *)&v297 + 1) = a1;
        LOBYTE(v298) = 1;
        goto LABEL_102;
      case 1315268178:
        *(_QWORD *)&v297 = a1;
        *((_QWORD *)&v297 + 1) = a1;
        LOBYTE(v298) = 1;
        goto LABEL_104;
      case 1315268210:
        *(_QWORD *)&v297 = a1;
        *((_QWORD *)&v297 + 1) = a1;
        LOBYTE(v298) = 0;
LABEL_92:
        v301 = &v297;
        v302 = (char **)&v297 + 1;
        LODWORD(m) = sub_141050CB0(&v301, a3);
        return (unsigned int)m;
      default:
        break;
    }
    goto LABEL_114;
  }
  if ( a2 > 1316187756 )
  {
    if ( a2 <= 1316579181 )
    {
      if ( a2 == 1316187757 )
      {
        if ( (unsigned __int8)sub_141045D50(a1, 1413706606, a3) != 0
          || (v38 = *((_QWORD *)a1 + 33)) != 0 && (unsigned __int8)sub_141063F30(v38, 1413706606, a3) != 0
          || (unsigned __int8)sub_140FE2700(a1, 1413706606, a3) != 0 )
        {
          v39 = sub_140E78A80();
          sub_140FF4D40(v39, *((unsigned int *)a1 + 3), a1 + 32);
          goto LABEL_346;
        }
        goto LABEL_607;
      }
      if ( a2 == 1316188004 )
      {
        a1[460] = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        goto LABEL_346;
      }
      if ( a2 != 1316255858 )
        goto LABEL_114;
      v303 = a1;
      v304 = a1;
      v301 = (__int128 *)&v303;
      v302 = &v304;
      v12 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
      v13 = *a3;
      v14 = **a3;
      if ( v12 == 10 )
      {
        LODWORD(m) = 0;
        v15 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v14 + 176))(v13, a3, 0);
        v16 = *v15;
        v17 = v15[1];
        if ( *v15 == v17 )
          return (unsigned int)m;
        m = (__int64)&v302;
        v18 = *v15;
        while ( *(_DWORD *)v18 != 1819504496 )
        {
          v18 += 16;
          if ( v18 == v17 )
            goto LABEL_607;
        }
        if ( v18 != v17 && *(_QWORD *)(v18 + 8) != 0 )
        {
          v165 = nullptr;
          while ( *(_DWORD *)v16 != 1819504496 )
          {
            v16 += 16;
            if ( v16 == v17 )
              goto LABEL_365;
          }
          if ( v16 == v17 )
            v165 = nullptr;
          else
            v165 = *(__int64 **)(v16 + 8);
LABEL_365:
          v178 = &qword_141B5A4A0;
          if ( v165 == nullptr )
            v165 = &qword_141B5A4A0;
          switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v165 + 64LL))(*v165) )
          {
            case 0u:
              v297 = 0;
              v298 = 0;
              v299 = -65279;
              v300 = 1900;
              sub_140BA1B40(v303 + 12, &v297);
              goto LABEL_346;
            case 1u:
              v189 = *v15;
              v190 = v15[1];
              v191 = nullptr;
              if ( *v15 != v190 )
              {
                while ( *(_DWORD *)v189 != 1869379180 )
                {
                  v189 += 16;
                  if ( v189 == v190 )
                    goto LABEL_468;
                }
                if ( v189 == v190 )
                  v191 = nullptr;
                else
                  v191 = *(__int64 **)(v189 + 8);
              }
LABEL_468:
              if ( v191 == nullptr )
                v191 = &qword_141B5A4A0;
              v231 = sub_1410509E0(&v302, v191);
              if ( v231 < 0 )
                goto LABEL_607;
              v232 = *((_QWORD *)v304 + 12);
              if ( v232 == 0 )
                goto LABEL_607;
              m = v232 + 24LL * (unsigned int)v231;
              v233 = *v15;
              v234 = v15[1];
              v235 = nullptr;
              if ( *v15 == v234 )
              {
                v237 = &qword_141B5A4A0;
              }
              else
              {
                v236 = *v15;
                while ( *(_DWORD *)v236 != 1986096245 )
                {
                  v236 += 16;
                  if ( v236 == v234 )
                    goto LABEL_571;
                }
                if ( v236 == v234 )
                  v235 = nullptr;
                else
                  v235 = *(__int64 **)(v236 + 8);
LABEL_571:
                v237 = &qword_141B5A4A0;
                if ( v235 != nullptr )
                  v237 = v235;
                v235 = nullptr;
                while ( *(_DWORD *)v233 != 1768169504 )
                {
                  v233 += 16;
                  if ( v233 == v234 )
                    goto LABEL_598;
                }
                if ( v233 == v234 )
                  v235 = nullptr;
                else
                  v235 = *(__int64 **)(v233 + 8);
              }
LABEL_598:
              if ( v235 != nullptr )
                v178 = v235;
              v292 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v178 + 80LL))(*v178, v178);
              LODWORD(m) = sub_14144D2B0(m, v292, v237);
              return (unsigned int)m;
            case 2u:
              v192 = *v15;
              v193 = v15[1];
              v194 = nullptr;
              if ( *v15 != v193 )
              {
                while ( *(_DWORD *)v192 != 1869379180 )
                {
                  v192 += 16;
                  if ( v192 == v193 )
                    goto LABEL_481;
                }
                if ( v192 == v193 )
                  v194 = nullptr;
                else
                  v194 = *(__int64 **)(v192 + 8);
              }
LABEL_481:
              if ( v194 != nullptr )
                v178 = v194;
              v238 = sub_1410509E0(&v302, v178);
              if ( v238 < 0 || *((_QWORD *)v304 + 12) == 0 )
                goto LABEL_607;
              v239 = v303;
              v240 = v303[12] + 24LL * (unsigned int)v238;
              sub_141758A00(v240, v240 + 24, v303[13] - (v240 + 24));
              v239[13] -= 24LL;
              goto LABEL_346;
            case 3u:
              LOBYTE(m) = 1;
              v195 = *((_QWORD *)v304 + 13) - *((_QWORD *)v304 + 12);
              if ( v195 != 0 )
              {
                v196 = ((unsigned __int64)((unsigned __int128)(0x2AAAAAAAAAAAAAABLL * (__int128)v195) >> 64) >> 63)
                     + v195 / 24;
                v197 = (v196 << 32) - 0x100000000LL;
                do
                {
                  --v196;
                  if ( *((_QWORD *)v304 + 12) != 0 )
                  {
                    v198 = v303;
                    v199 = v303[12] + 24 * (v197 >> 32);
                    sub_141758A00(v199, v199 + 24, v303[13] - (v199 + 24));
                    v198[13] -= 24LL;
                  }
                  v197 -= 0x100000000LL;
                }
                while ( v196 != 0 );
              }
              return (unsigned int)m;
            case 4u:
              v200 = *v15;
              v201 = v15[1];
              m = 0;
              if ( *v15 == v201 )
                goto LABEL_487;
              break;
            case 5u:
LABEL_402:
              sub_140DD5C90(&v301, 0);
              goto LABEL_346;
            default:
              goto LABEL_607;
          }
          while ( *(_DWORD *)v200 != 1869379180 )
          {
            v200 += 16;
            if ( v200 == v201 )
              goto LABEL_487;
          }
          if ( v200 == v201 )
            m = 0;
          else
            m = *(_QWORD *)(v200 + 8);
LABEL_487:
          if ( m == 0 )
            m = (__int64)&qword_141B5A4A0;
          v297 = 0;
          v298 = 0;
          v299 = -65279;
          v300 = 1900;
          v241 = v303;
          sub_140BA1B40(v303 + 12, &v297);
          v242 = v241[13];
          v243 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, __int64, _QWORD))(**(_QWORD **)m + 176LL))(
                             *(_QWORD *)m,
                             m,
                             0);
          LOBYTE(m) = 1;
          v244 = v243[1] - *v243;
          if ( v244 != 0 )
          {
            v245 = v242 - 24;
            v246 = v244 >> 4;
            v247 = 8;
            do
            {
              v248 = *(__int64 **)(*v243 + v247);
              if ( v248 == nullptr )
                v248 = &qword_141B5A4A0;
              sub_14144D2B0(v245, *(unsigned int *)(*v243 + v247 - 8), v248);
              v247 += 16;
              --v246;
            }
            while ( v246 != 0 );
          }
          return (unsigned int)m;
        }
        goto LABEL_607;
      }
      if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v14 + 8))(v13, a3) != 11 )
        goto LABEL_607;
      v59 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      v60 = *((_QWORD *)v304 + 13) - *((_QWORD *)v304 + 12);
      if ( v60 != 0 )
      {
        v58 = (unsigned __int128)(0x2AAAAAAAAAAAAAABLL * (__int128)v60) >> 64;
        m = (v58 >> 63) + v60 / 24;
        v61 = (m << 32) - 0x100000000LL;
        do
        {
          --m;
          if ( *((_QWORD *)v304 + 12) != 0 )
          {
            v62 = v303;
            v63 = v303[12] + 24 * (v61 >> 32);
            sub_141758A00(v63, v63 + 24, v303[13] - (v63 + 24));
            v62[13] -= 24LL;
          }
          v61 -= 0x100000000LL;
        }
        while ( m != 0 );
      }
      v86 = v59[1] - *v59;
      if ( v86 != 0 )
      {
        v87 = v86 >> 3;
        v88 = 1;
        if ( v87 >= 2 )
          v88 = v87;
        for ( k = 0; k != v88; ++k )
        {
          v90 = *(__int64 **)(*v59 + 8 * k);
          if ( v90 == nullptr )
            v90 = &qword_141B5A4A0;
          v297 = 0;
          v298 = 0;
          v299 = -65279;
          v300 = 1900;
          v91 = v303;
          sub_140BA1B40(v303 + 12, &v297);
          v92 = v91[13];
          m = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v90 + 176LL))(*v90, v90, 0);
          v93 = *(_QWORD *)(m + 8) - *(_QWORD *)m;
          if ( v93 != 0 )
          {
            v94 = v92 - 24;
            v95 = v93 >> 4;
            v96 = 8;
            do
            {
              v97 = *(__int64 **)(*(_QWORD *)m + v96);
              if ( v97 == nullptr )
                v97 = &qword_141B5A4A0;
              sub_14144D2B0(v94, *(unsigned int *)(*(_QWORD *)m + v96 - 8), v97);
              v96 += 16;
              --v95;
            }
            while ( v95 != 0 );
          }
        }
      }
      v114 = qword_141B60C30;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v114 != 1986359923 )
        {
          v114 += 16;
          if ( v114 == qword_141B60C38 )
            goto LABEL_198;
        }
        if ( v114 != qword_141B60C38 )
        {
          LOBYTE(m) = 1;
          if ( *(_QWORD *)(v114 + 8) != 0 )
            return (unsigned int)m;
        }
      }
      goto LABEL_198;
    }
    if ( a2 == 1316579182 )
    {
      a1[461] = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_346;
    }
    if ( a2 == 1413704814 )
    {
      m = (__int64)&v297;
      (*(void (__fastcall **)(__int64 *, __int128 *, __int64 **))(**a3 + 128))(*a3, &v297, a3);
      v53 = (volatile signed __int32 **)(a1 + 24);
      if ( a1 + 24 != (char *)&v297 )
      {
        v6 = v297;
        v54 = *v53;
        v55 = *v53 - 1;
        if ( *v53 == nullptr )
          v55 = nullptr;
        v56 = (volatile signed __int32 *)(v297 - 4);
        if ( (_QWORD)v297 != 0 )
        {
          if ( v54 != nullptr && _InterlockedDecrement(v55) == 0 )
            sub_1412EC9A0(v55, v6);
          *v53 = nullptr;
          _InterlockedIncrement(v56);
          v57 = v56 + 1;
        }
        else
        {
          if ( v54 != nullptr && _InterlockedDecrement(v55) == 0 )
            sub_1412EC9A0(v55, v6);
          v57 = nullptr;
        }
        *v53 = v57;
      }
      v305 = (__int64 *)(a1 + 24);
      v151 = v297;
      if ( (_QWORD)v297 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v297 - 4)) == 0 )
        sub_1412EC9A0(v151 - 4, v6);
      v152 = 2;
      if ( dword_141B60300 != 12 )
        v152 = 3 * (dword_141B60300 == 18);
      a1[462] = v152;
      v153 = *((_QWORD **)a1 + 8);
      if ( v153 != nullptr )
      {
        v154 = v153[1] - *v153;
        if ( v154 != 0 )
        {
          v155 = v154 >> 3;
          v156 = -(__int64)(v154 & 0xFFFFFFFFFFFFFFF8uLL);
          do
          {
            v157 = v155 - 1;
            v158 = *((__int64 **)a1 + 8);
            v159 = *v158;
            m = *(_QWORD *)(*v158 + 8 * v155 - 8);
            if ( *(_WORD *)(m + 8) == 24 )
            {
              v160 = *(_QWORD *)m;
              if ( *(_QWORD *)m != 0 && _InterlockedDecrement((volatile signed __int32 *)(v160 - 4)) == 0 )
                sub_1412EC9A0(v160 - 4, v6);
              sub_140E469C0(m);
              sub_141758A00(v159 + 8 * v155 - 8, v159 + 8 * v155, v156 + v158[1] - v159);
              v158[1] -= 8;
            }
            v156 += 8;
            --v155;
          }
          while ( v157 != 0 );
        }
      }
      goto LABEL_299;
    }
    if ( a2 != 1413706606 )
      goto LABEL_114;
    m = (__int64)&v297;
    (*(void (__fastcall **)(__int64 *, __int128 *, __int64 **))(**a3 + 128))(*a3, &v297, a3);
    v20 = (volatile signed __int32 **)(a1 + 32);
    if ( a1 + 32 != (char *)&v297 )
    {
      v19 = v297;
      v21 = *v20;
      v22 = *v20 - 1;
      if ( *v20 == nullptr )
        v22 = nullptr;
      v23 = (volatile signed __int32 *)(v297 - 4);
      if ( (_QWORD)v297 != 0 )
      {
        if ( v21 != nullptr && _InterlockedDecrement(v22) == 0 )
          sub_1412EC9A0(v22, v19);
        *v20 = nullptr;
        _InterlockedIncrement(v23);
        v24 = v23 + 1;
      }
      else
      {
        if ( v21 != nullptr && _InterlockedDecrement(v22) == 0 )
          sub_1412EC9A0(v22, v19);
        v24 = nullptr;
      }
      *v20 = v24;
    }
    v305 = (__int64 *)(a1 + 32);
    v126 = v297;
    if ( (_QWORD)v297 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v297 - 4)) == 0 )
      sub_1412EC9A0(v126 - 4, v19);
    v127 = 2;
    if ( dword_141B60300 != 12 )
      v127 = 3 * (dword_141B60300 == 18);
    a1[463] = v127;
    v128 = *((_QWORD **)a1 + 8);
    if ( v128 != nullptr )
    {
      v129 = v128[1] - *v128;
      if ( v129 != 0 )
      {
        v130 = v129 >> 3;
        v131 = -(__int64)(v129 & 0xFFFFFFFFFFFFFFF8uLL);
        do
        {
          v132 = v130 - 1;
          v133 = *((__int64 **)a1 + 8);
          v134 = *v133;
          m = *(_QWORD *)(*v133 + 8 * v130 - 8);
          if ( *(_WORD *)(m + 8) == 25 )
          {
            v135 = *(_QWORD *)m;
            if ( *(_QWORD *)m != 0 && _InterlockedDecrement((volatile signed __int32 *)(v135 - 4)) == 0 )
              sub_1412EC9A0(v135 - 4, v19);
            sub_140E469C0(m);
            sub_141758A00(v134 + 8 * v130 - 8, v134 + 8 * v130, v131 + v133[1] - v134);
            v133[1] -= 8;
          }
          v131 += 8;
          --v130;
        }
        while ( v132 != 0 );
      }
    }
    v136 = *((_DWORD **)a1 + 3);
    if ( v136 != nullptr )
    {
      LOBYTE(m) = 1;
      if ( *v136 != 0 )
        return (unsigned int)m;
      v137 = *v305;
      v138 = _InterlockedExchangeAdd(v136 - 1, 0xFFFFFFFF);
      v139 = v136 - 1;
      if ( v137 != 0 )
      {
        if ( v138 == 1 )
          sub_1412EC9A0(v139, v19);
        goto LABEL_247;
      }
      if ( v138 == 1 )
        sub_1412EC9A0(v139, v19);
    }
    else
    {
      v137 = *v305;
      if ( *v305 != 0 )
      {
LABEL_247:
        *((_QWORD *)a1 + 3) = 0;
        _InterlockedIncrement((volatile signed __int32 *)(v137 - 4));
LABEL_345:
        *((_QWORD *)a1 + 3) = v137;
        a1[462] = a1[463];
        goto LABEL_346;
      }
    }
    v137 = 0;
    goto LABEL_345;
  }
  if ( a2 <= 1315858033 )
  {
    if ( a2 == 1315398516 )
    {
      a1[459] = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_346;
    }
    if ( a2 != 1315729011 )
    {
      if ( a2 != 1315856749 )
        goto LABEL_114;
      m = (__int64)&v297;
      (*(void (__fastcall **)(__int64 *, __int128 *, __int64 **))(**a3 + 128))(*a3, &v297, a3);
      v7 = (volatile signed __int32 **)(a1 + 24);
      if ( a1 + 24 != (char *)&v297 )
      {
        v6 = v297;
        v8 = *v7;
        v9 = *v7 - 1;
        if ( *v7 == nullptr )
          v9 = nullptr;
        v10 = (volatile signed __int32 *)(v297 - 4);
        if ( (_QWORD)v297 != 0 )
        {
          if ( v8 != nullptr && _InterlockedDecrement(v9) == 0 )
            sub_1412EC9A0(v9, v6);
          *v7 = nullptr;
          _InterlockedIncrement(v10);
          v11 = v10 + 1;
        }
        else
        {
          if ( v8 != nullptr && _InterlockedDecrement(v9) == 0 )
            sub_1412EC9A0(v9, v6);
          v11 = nullptr;
        }
        *v7 = v11;
      }
      v305 = (__int64 *)(a1 + 24);
      v116 = v297;
      if ( (_QWORD)v297 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v297 - 4)) == 0 )
        sub_1412EC9A0(v116 - 4, v6);
      v117 = 2;
      if ( dword_141B60300 != 12 )
        v117 = 3 * (dword_141B60300 == 18);
      a1[462] = v117;
      v118 = *((_QWORD **)a1 + 8);
      if ( v118 != nullptr )
      {
        v119 = v118[1] - *v118;
        if ( v119 != 0 )
        {
          v120 = v119 >> 3;
          v121 = -(__int64)(v119 & 0xFFFFFFFFFFFFFFF8uLL);
          do
          {
            v122 = v120 - 1;
            v123 = *((__int64 **)a1 + 8);
            v124 = *v123;
            m = *(_QWORD *)(*v123 + 8 * v120 - 8);
            if ( *(_WORD *)(m + 8) == 24 )
            {
              v125 = *(_QWORD *)m;
              if ( *(_QWORD *)m != 0 && _InterlockedDecrement((volatile signed __int32 *)(v125 - 4)) == 0 )
                sub_1412EC9A0(v125 - 4, v6);
              sub_140E469C0(m);
              sub_141758A00(v124 + 8 * v120 - 8, v124 + 8 * v120, v121 + v123[1] - v124);
              v123[1] -= 8;
            }
            v121 += 8;
            --v120;
          }
          while ( v122 != 0 );
        }
      }
LABEL_299:
      v161 = *((_DWORD **)a1 + 4);
      if ( v161 != nullptr )
      {
        LOBYTE(m) = 1;
        if ( *v161 != 0 )
          return (unsigned int)m;
        v162 = *v305;
        v163 = _InterlockedExchangeAdd(v161 - 1, 0xFFFFFFFF);
        v164 = v161 - 1;
        if ( v162 != 0 )
        {
          if ( v163 == 1 )
            sub_1412EC9A0(v164, v6);
          goto LABEL_305;
        }
        if ( v163 == 1 )
          sub_1412EC9A0(v164, v6);
      }
      else
      {
        v162 = *v305;
        if ( *v305 != 0 )
        {
LABEL_305:
          *((_QWORD *)a1 + 4) = 0;
          _InterlockedIncrement((volatile signed __int32 *)(v162 - 4));
LABEL_309:
          *((_QWORD *)a1 + 4) = v162;
          a1[463] = a1[462];
          goto LABEL_346;
        }
      }
      v162 = 0;
      goto LABEL_309;
    }
    v303 = a1;
    v304 = a1;
    v301 = (__int128 *)&v303;
    v302 = &v304;
    v31 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
    v32 = *a3;
    v33 = **a3;
    if ( v31 == 10 )
    {
      LODWORD(m) = 0;
      v34 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v33 + 176))(v32, a3, 0);
      v35 = *v34;
      v36 = v34[1];
      if ( *v34 == v36 )
        return (unsigned int)m;
      m = (__int64)&v302;
      v37 = *v34;
      while ( *(_DWORD *)v37 != 1819504496 )
      {
        v37 += 16;
        if ( v37 == v36 )
          goto LABEL_607;
      }
      if ( v37 != v36 && *(_QWORD *)(v37 + 8) != 0 )
      {
        v166 = nullptr;
        while ( *(_DWORD *)v35 != 1819504496 )
        {
          v35 += 16;
          if ( v35 == v36 )
            goto LABEL_370;
        }
        if ( v35 == v36 )
          v166 = nullptr;
        else
          v166 = *(__int64 **)(v35 + 8);
LABEL_370:
        v179 = &qword_141B5A4A0;
        if ( v166 == nullptr )
          v166 = &qword_141B5A4A0;
        switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v166 + 64LL))(*v166) )
        {
          case 0u:
            v180 = *(__int64 **)(qword_141B5FDF8 + 128);
            v181 = *v180;
            m = v180[1];
            if ( m != *v180 )
            {
              v182 = v303;
              *(_QWORD *)&v297 = 0;
              BYTE8(v297) = 100;
              sub_1408C9770(v303 + 9, &v297);
              v183 = v182[10];
              if ( qword_141B5FDF8 == 0
                || ((_BYTE)word_141B60320 != 0
                 || (v185 = *(__int64 **)(qword_141B5FDF8 + 96), *(__int64 **)(qword_141B5FDF8 + 104) == v185))
                && (v184 = *(_QWORD *)(qword_141B5FDF8 + 128),
                    v185 = *(__int64 **)v184,
                    *(_QWORD *)(v184 + 8) == *(_QWORD *)v184) )
              {
                v186 = 0;
              }
              else
              {
                v186 = *v185;
              }
              *(_QWORD *)(v183 - 16) = v186;
              *(_BYTE *)(v183 - 8) = 100;
            }
            LOBYTE(m) = m != v181;
            return (unsigned int)m;
          case 1u:
            v202 = *v34;
            v203 = v34[1];
            v204 = nullptr;
            if ( *v34 != v203 )
            {
              while ( *(_DWORD *)v202 != 1869379180 )
              {
                v202 += 16;
                if ( v202 == v203 )
                  goto LABEL_496;
              }
              if ( v202 == v203 )
                v204 = nullptr;
              else
                v204 = *(__int64 **)(v202 + 8);
            }
LABEL_496:
            if ( v204 == nullptr )
              v204 = &qword_141B5A4A0;
            v249 = sub_141050430(&v302, v204);
            if ( v249 < 0 )
              goto LABEL_607;
            v250 = *((_QWORD *)v304 + 9);
            if ( v250 == 0 )
              goto LABEL_607;
            v251 = (unsigned int)v249;
            v252 = *v34;
            v253 = v34[1];
            v254 = nullptr;
            if ( *v34 == v253 )
            {
              m = (__int64)&qword_141B5A4A0;
            }
            else
            {
              v255 = *v34;
              while ( *(_DWORD *)v255 != 1986096245 )
              {
                v255 += 16;
                if ( v255 == v253 )
                  goto LABEL_580;
              }
              if ( v255 == v253 )
                v254 = nullptr;
              else
                v254 = *(__int64 **)(v255 + 8);
LABEL_580:
              m = (__int64)&qword_141B5A4A0;
              if ( v254 != nullptr )
                m = (__int64)v254;
              v254 = nullptr;
              while ( *(_DWORD *)v252 != 1768169504 )
              {
                v252 += 16;
                if ( v252 == v253 )
                  goto LABEL_602;
              }
              if ( v252 == v253 )
                v254 = nullptr;
              else
                v254 = *(__int64 **)(v252 + 8);
            }
LABEL_602:
            v293 = 16 * v251;
            if ( v254 != nullptr )
              v179 = v254;
            v294 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v179 + 80LL))(*v179, v179);
            if ( v294 == 1885696611 )
            {
              *(_BYTE *)(v250 + v293 + 8) = (*(__int64 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)m + 64LL))(
                                              *(_QWORD *)m,
                                              m);
            }
            else
            {
              if ( v294 != 1818324583 )
                goto LABEL_607;
              v295 = qword_141B5FDF8;
              sub_140FE7960(&v297, m, 1818324583);
              *(_QWORD *)(v293 + v250) = sub_140FA1860(v295, &v297);
            }
            goto LABEL_346;
          case 2u:
            v205 = *v34;
            v206 = v34[1];
            v207 = nullptr;
            if ( *v34 != v206 )
            {
              while ( *(_DWORD *)v205 != 1869379180 )
              {
                v205 += 16;
                if ( v205 == v206 )
                  goto LABEL_509;
              }
              if ( v205 == v206 )
                v207 = nullptr;
              else
                v207 = *(__int64 **)(v205 + 8);
            }
LABEL_509:
            if ( v207 != nullptr )
              v179 = v207;
            v256 = sub_141050430(&v302, v179);
            if ( v256 < 0 || *((_QWORD *)v304 + 9) == 0 )
              goto LABEL_607;
            v257 = v303;
            v258 = v303[9] + 16LL * (unsigned int)v256;
            sub_141758A00(v258, v258 + 16, v303[10] - (v258 + 16));
            v257[10] -= 16LL;
            goto LABEL_346;
          case 3u:
            v208 = (unsigned int)(*((_DWORD *)v304 + 20) - *((_DWORD *)v304 + 18)) >> 4;
            LOBYTE(m) = 1;
            if ( (_BYTE)v208 != 0 )
            {
              v209 = 16LL * (unsigned __int8)v208;
              v210 = -16LL * (unsigned __int8)v208;
              do
              {
                if ( *((_QWORD *)v304 + 9) != 0 )
                {
                  v211 = v303;
                  sub_141758A00(v303[9] + v209 - 16, v303[9] + v209, v210 + v303[10] - v303[9]);
                  v211[10] -= 16LL;
                }
                v210 += 16;
                v209 -= 16;
              }
              while ( v209 != 0 );
            }
            return (unsigned int)m;
          case 4u:
            v212 = *v34;
            v213 = v34[1];
            m = 0;
            if ( *v34 == v213 )
              goto LABEL_515;
            break;
          case 5u:
            goto LABEL_402;
          default:
            goto LABEL_607;
        }
        while ( *(_DWORD *)v212 != 1869379180 )
        {
          v212 += 16;
          if ( v212 == v213 )
            goto LABEL_515;
        }
        if ( v212 == v213 )
          m = 0;
        else
          m = *(_QWORD *)(v212 + 8);
LABEL_515:
        if ( m == 0 )
          m = (__int64)&qword_141B5A4A0;
        v259 = *(__int64 ***)(qword_141B5FDF8 + 128);
        v260 = v259[1];
        v305 = *v259;
        if ( v260 != v305 )
        {
          v261 = v303;
          *(_QWORD *)&v297 = 0;
          BYTE8(v297) = 100;
          sub_1408C9770(v303 + 9, &v297);
          v262 = v261[10];
          if ( qword_141B5FDF8 == 0
            || ((_BYTE)word_141B60320 != 0
             || (v264 = *(__int64 **)(qword_141B5FDF8 + 96), *(__int64 **)(qword_141B5FDF8 + 104) == v264))
            && (v263 = *(_QWORD *)(qword_141B5FDF8 + 128),
                v264 = *(__int64 **)v263,
                *(_QWORD *)(v263 + 8) == *(_QWORD *)v263) )
          {
            v265 = 0;
          }
          else
          {
            v265 = *v264;
          }
          *(_QWORD *)(v262 - 16) = v265;
          *(_BYTE *)(v262 - 8) = 100;
          m = (*(__int64 (__fastcall **)(_QWORD, __int64, _QWORD))(**(_QWORD **)m + 176LL))(*(_QWORD *)m, m, 0);
          v266 = *(_QWORD *)(m + 8) - *(_QWORD *)m;
          if ( v266 != 0 )
          {
            v267 = v266 >> 4;
            v268 = 8;
            do
            {
              v269 = *(__int64 **)(*(_QWORD *)m + v268);
              if ( v269 == nullptr )
                v269 = &qword_141B5A4A0;
              v270 = *(_DWORD *)(*(_QWORD *)m + v268 - 8);
              if ( v270 == 1885696611 )
              {
                *(_BYTE *)(v262 - 8) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v269 + 64LL))(*v269);
              }
              else if ( v270 == 1818324583 )
              {
                v271 = qword_141B5FDF8;
                sub_140FE7960(&v297, v269, 1818324583);
                *(_QWORD *)(v262 - 16) = sub_140FA1860(v271, &v297);
              }
              v268 += 16;
              --v267;
            }
            while ( v267 != 0 );
          }
        }
        LOBYTE(m) = v260 != v305;
        return (unsigned int)m;
      }
      goto LABEL_607;
    }
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v33 + 8))(v32, a3) != 11 )
      goto LABEL_607;
    v64 = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
    v65 = *((_DWORD *)v304 + 20) - *((_DWORD *)v304 + 18);
    v305 = (__int64 *)v64;
    v58 = v65 >> 4;
    if ( (_BYTE)v58 != 0 )
    {
      v66 = 16LL * (unsigned __int8)v58;
      m = -16LL * (unsigned __int8)v58;
      do
      {
        if ( *((_QWORD *)v304 + 9) != 0 )
        {
          v67 = v303;
          sub_141758A00(v303[9] + v66 - 16, v303[9] + v66, m + v303[10] - v303[9]);
          v67[10] -= 16LL;
        }
        m += 16;
        v66 -= 16;
      }
      while ( v66 != 0 );
    }
    v98 = v305[1] - *v305;
    if ( v98 != 0 )
    {
      v99 = v98 >> 3;
      v100 = 1;
      if ( v99 >= 2 )
        v100 = v99;
      v306 = v100;
      for ( m = 0; m != v306; ++m )
      {
        v101 = *(__int64 **)(*v305 + 8 * m);
        if ( v101 == nullptr )
          v101 = &qword_141B5A4A0;
        if ( *(_QWORD *)(*(_QWORD *)(qword_141B5FDF8 + 128) + 8LL) != **(_QWORD **)(qword_141B5FDF8 + 128) )
        {
          v102 = v303;
          *(_QWORD *)&v297 = 0;
          BYTE8(v297) = 100;
          sub_1408C9770(v303 + 9, &v297);
          if ( qword_141B5FDF8 == 0
            || ((_BYTE)word_141B60320 != 0
             || (v104 = *(__int64 **)(qword_141B5FDF8 + 96), *(__int64 **)(qword_141B5FDF8 + 104) == v104))
            && (v103 = *(_QWORD *)(qword_141B5FDF8 + 128),
                v104 = *(__int64 **)v103,
                *(_QWORD *)(v103 + 8) == *(_QWORD *)v103) )
          {
            v105 = 0;
          }
          else
          {
            v105 = *v104;
          }
          v106 = v102[10];
          *(_QWORD *)(v106 - 16) = v105;
          *(_BYTE *)(v106 - 8) = 100;
          v107 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v101 + 176LL))(
                             *v101,
                             v101,
                             0);
          v108 = v107[1] - *v107;
          if ( v108 != 0 )
          {
            v109 = v108 >> 4;
            v110 = 8;
            do
            {
              v58 = *(_QWORD *)(*v107 + v110);
              if ( v58 == 0 )
                v58 = (unsigned __int64)&qword_141B5A4A0;
              v111 = *(_DWORD *)(*v107 + v110 - 8);
              if ( v111 == 1885696611 )
              {
                *(_BYTE *)(v106 - 8) = (*(__int64 (__fastcall **)(_QWORD))(**(_QWORD **)v58 + 64LL))(*(_QWORD *)v58);
              }
              else if ( v111 == 1818324583 )
              {
                v112 = qword_141B5FDF8;
                sub_140FE7960(&v297, v58, 1818324583);
                *(_QWORD *)(v106 - 16) = sub_140FA1860(v112, &v297);
              }
              v110 += 16;
              --v109;
            }
            while ( v109 != 0 );
          }
        }
      }
    }
    v115 = qword_141B60C30;
    if ( qword_141B60C30 != qword_141B60C38 )
    {
      while ( *(_DWORD *)v115 != 1986359923 )
      {
        v115 += 16;
        if ( v115 == qword_141B60C38 )
          goto LABEL_198;
      }
      if ( v115 != qword_141B60C38 )
      {
        LOBYTE(m) = 1;
        if ( *(_QWORD *)(v115 + 8) != 0 )
          return (unsigned int)m;
      }
    }
LABEL_198:
    LOBYTE(m) = 1;
    LOBYTE(v58) = 1;
    sub_140DD5C90(&v301, v58);
    return (unsigned int)m;
  }
  switch ( a2 )
  {
    case 1315858034:
      *(_QWORD *)&v297 = a1;
      *((_QWORD *)&v297 + 1) = a1;
      LOBYTE(v298) = 1;
      goto LABEL_92;
    case 1315861625:
      m = (__int64)&v297;
      (*(void (__fastcall **)(__int64 *, __int128 *, __int64 **))(**a3 + 128))(*a3, &v297, a3);
      v26 = (volatile signed __int32 **)(a1 + 48);
      if ( a1 + 48 != (char *)&v297 )
      {
        v48 = v297;
        v49 = *v26;
        v50 = *v26 - 1;
        if ( *v26 == nullptr )
          v50 = nullptr;
        v51 = (volatile signed __int32 *)(v297 - 4);
        if ( (_QWORD)v297 != 0 )
        {
          if ( v49 != nullptr && _InterlockedDecrement(v50) == 0 )
            sub_1412EC9A0(v50, v48);
          *v26 = nullptr;
          _InterlockedIncrement(v51);
          v52 = v51 + 1;
        }
        else
        {
          if ( v49 != nullptr && _InterlockedDecrement(v50) == 0 )
            sub_1412EC9A0(v50, v48);
          v52 = nullptr;
        }
        *v26 = v52;
      }
      v144 = v297;
      if ( (_QWORD)v297 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v297 - 4)) == 0 )
        sub_1412EC9A0(v144 - 4, v48);
      v145 = sub_140E78A80();
      v146 = sub_140FF53C0(v145, *((unsigned int *)a1 + 3));
      LOBYTE(m) = 1;
      if ( v146 == 0 )
        return (unsigned int)m;
      v143 = (__int64 *)(v146 + 16);
      if ( (volatile signed __int32 **)(v146 + 16) == v26 )
        return (unsigned int)m;
      goto LABEL_269;
    case 1316120425:
      m = qword_141B5FE20;
      sub_140FE7960(&v297, a3, 1919248233);
      *((_QWORD *)a1 + 31) = sub_140FA1860(m, &v297);
      goto LABEL_346;
    default:
      break;
  }
LABEL_114:
  if ( (_BYTE)word_141B60320 == 0 )
    goto LABEL_607;
  LODWORD(m) = 0;
  if ( a2 <= 1315857517 )
  {
    if ( a2 != 1315267939 )
    {
      if ( a2 == 1315337314 )
      {
        v301 = (__int128 *)a1;
        v302 = (char **)a1;
        *(_QWORD *)&v297 = &v301;
        *((_QWORD *)&v297 + 1) = &v302;
        LODWORD(m) = sub_141051740(&v297, a3);
      }
      return (unsigned int)m;
    }
    v168 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
    sub_141047EA0(a1, v168);
LABEL_346:
    LOBYTE(m) = 1;
    return (unsigned int)m;
  }
  if ( a2 == 1315857518 )
  {
    v175 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
    v176 = *((_WORD *)a1 + 228);
    if ( v175 != 0 )
      *((_WORD *)a1 + 228) = v176 | 0x200;
    else
      *((_WORD *)a1 + 228) = v176 & 0xFDFF;
    goto LABEL_346;
  }
  if ( a2 == 1315861353 )
  {
    v80 = (__int64 *)(a1 + 280);
    sub_140FE7EA0(a1 + 280, a3);
    v81 = *((_QWORD *)a1 + 33);
    v82 = *(__int64 **)(v81 + 24);
    LOBYTE(m) = 1;
    if ( *(__int64 **)(v81 + 32) != v82 )
    {
      v83 = *v80;
      if ( *v80 != 0 )
      {
        v84 = *v82;
        *(_QWORD *)(v84 + 120) = v83;
        v85 = *(_DWORD *)(v83 + 108);
        if ( v85 < 0 )
        {
          *(_DWORD *)(v83 + 108) = -v85;
          v83 = *(_QWORD *)(v84 + 120);
        }
        *(_BYTE *)(v83 + 155) &= ~1u;
      }
    }
  }
  return (unsigned int)m;
}
