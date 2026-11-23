__int64 __fastcall sub_14154B380(__int64 a1, int a2, __int64 **a3)
{
  __int64 ii; // r14
  _QWORD *v6; // rdx
  volatile signed __int32 **v7; // rdi
  __int64 v8; // rsi
  char v9; // al
  __int64 *v10; // rcx
  __int64 v11; // rbp
  __int64 *v12; // rbx
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rdx
  volatile signed __int32 *v16; // rax
  volatile signed __int32 *v17; // rcx
  volatile signed __int32 *v18; // rsi
  volatile signed __int32 *v19; // rsi
  char v20; // al
  __int64 *v21; // rcx
  __int64 v22; // rbp
  __int64 *v23; // rbx
  __int64 v24; // rax
  __int64 v25; // rcx
  __int64 v26; // rdx
  __int64 **v27; // rbx
  __int64 *v28; // rsi
  __int64 *v29; // r15
  __int64 v30; // rbp
  __int64 v31; // rax
  __int64 v32; // r8
  unsigned __int64 v33; // rbx
  char v34; // al
  __int64 *v35; // rcx
  __int64 v36; // rbp
  __int64 *v37; // rbx
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 v40; // rdx
  __int64 v41; // rsi
  char v42; // al
  __int64 *v43; // rcx
  __int64 v44; // rbp
  __int64 *v45; // rbx
  __int64 v46; // rax
  __int64 v47; // rcx
  __int64 v48; // rdx
  char v49; // al
  __int64 *v50; // rcx
  __int64 v51; // rbp
  __int64 *v52; // rbx
  __int64 v53; // rax
  __int64 v54; // rcx
  __int64 v55; // rdx
  char v56; // al
  __int64 *v57; // rcx
  __int64 v58; // rbp
  __int64 *v59; // rbx
  __int64 v60; // rax
  __int64 v61; // rcx
  __int64 v62; // rdx
  volatile signed __int32 *v64; // rcx
  __int64 v65; // rdx
  __int64 v66; // rdi
  __int64 v67; // rdi
  __int64 v68; // rbx
  _QWORD **v69; // rsi
  __int64 v70; // rcx
  __int64 v71; // rsi
  __int64 v72; // rdi
  bool v73; // zf
  _QWORD *v74; // rbp
  __int64 v75; // rdi
  __int64 v76; // rdi
  __int64 v77; // rbx
  _QWORD **v78; // rsi
  __int64 v79; // rcx
  __int64 v80; // rdi
  __int64 v81; // rdi
  __int64 v82; // rbx
  _QWORD **v83; // rsi
  __int64 v84; // rcx
  _QWORD *v85; // r15
  __int64 v86; // rsi
  __int64 v87; // rbx
  __int64 v88; // rsi
  __int64 v89; // rbp
  __int64 v90; // r12
  __int64 v91; // r13
  __int64 v92; // rdi
  __int64 v93; // rcx
  __int64 v94; // rdi
  __int64 v95; // rdi
  __int64 v96; // rbx
  _QWORD **v97; // rsi
  __int64 v98; // rcx
  __int64 *v99; // rdi
  __int64 v100; // rsi
  __int64 v101; // rdi
  __int64 v102; // rax
  __int64 v103; // rbx
  __int64 i; // rsi
  __int64 v105; // rax
  unsigned __int64 v106; // rax
  __int64 v107; // rbx
  __int64 k; // rbp
  __int64 *v109; // rdx
  __int64 v110; // rax
  __int64 v111; // rax
  unsigned __int64 v112; // rax
  __int64 v113; // rcx
  __int64 *v114; // rsi
  __int64 v115; // rax
  __int64 v116; // r13
  _QWORD *v117; // rsi
  __int64 v118; // rbp
  __int64 v119; // rbp
  __int64 v120; // r12
  __int64 *v121; // rdx
  __int64 v122; // rbx
  __int64 v123; // rdi
  __int64 v124; // rax
  unsigned __int64 v125; // rax
  __int64 v126; // rbx
  __int64 n; // rbp
  __int64 *v128; // rdx
  __int64 v129; // rax
  __int64 v130; // rax
  unsigned __int64 v131; // rax
  __int64 v132; // rbx
  __int64 jj; // rbp
  __int64 *v134; // rdx
  __int64 v135; // rax
  __int64 v136; // rax
  unsigned __int64 v137; // rax
  __int64 v138; // rsi
  __int64 j; // rbx
  __int64 *v140; // rdx
  __int64 v141; // rax
  __int64 v142; // rax
  unsigned __int64 v143; // rax
  __int64 v144; // rbx
  __int64 m; // rbp
  __int64 *v146; // rdx
  __int64 v147; // rax
  __int64 v148; // rcx
  __int64 v149; // rax
  unsigned int v150; // eax
  int v151; // eax
  __int16 v152; // cx
  __int16 v153; // bp
  __int64 *v154; // rdx
  __int64 *v155; // rdx
  __int64 *v156; // rdx
  __int64 *v157; // rdx
  __int64 *v158; // rdx
  __int64 *v159; // rdx
  __int64 *v160; // rsi
  __int64 v161; // rcx
  __int64 v162; // rdx
  __int64 *v163; // rax
  __int64 *v164; // r15
  __int64 *v165; // rsi
  __int64 v166; // rcx
  __int64 v167; // rdx
  __int64 *v168; // rax
  __int64 *v169; // rsi
  __int64 v170; // rcx
  __int64 v171; // rdx
  __int64 *v172; // rax
  __int64 *v173; // rsi
  __int64 v174; // rdx
  __int64 v175; // rax
  __int64 *v176; // rsi
  __int64 v177; // rcx
  __int64 v178; // rdx
  __int64 *v179; // rax
  __int64 v180; // rax
  __int64 v181; // rcx
  __int64 *v182; // rdx
  __int64 v183; // rcx
  __int64 v184; // rdx
  __int64 *v185; // rax
  __int64 v186; // rsi
  __int64 v187; // rsi
  __int64 v188; // rdi
  _QWORD **v189; // rbp
  __int64 v190; // rcx
  __int64 v191; // rax
  __int64 v192; // rcx
  __int64 *v193; // rdx
  __int64 v194; // rcx
  __int64 v195; // rdx
  __int64 *v196; // rax
  __int64 v197; // rsi
  __int64 v198; // rdi
  _QWORD *v199; // rbp
  __int64 v200; // rax
  __int64 v201; // rcx
  __int64 *v202; // rbx
  __int64 v203; // rax
  __int64 v204; // rcx
  __int64 *v205; // rdx
  __int64 v206; // rcx
  __int64 v207; // rdx
  __int64 *v208; // rax
  __int64 v209; // rsi
  __int64 v210; // rsi
  __int64 v211; // rdi
  _QWORD **v212; // rbp
  __int64 v213; // rcx
  __int64 v214; // rax
  __int64 v215; // rcx
  __int64 *v216; // rdx
  __int64 v217; // rcx
  __int64 v218; // rdx
  __int64 *v219; // rax
  __int64 v220; // rsi
  __int64 v221; // rsi
  __int64 v222; // rdi
  _QWORD **v223; // rbp
  __int64 v224; // rcx
  __int64 v225; // rax
  __int64 v226; // rcx
  __int64 *v227; // rdx
  __int64 v228; // rcx
  __int64 v229; // rdx
  __int64 *v230; // rax
  __int64 v231; // rsi
  __int64 v232; // rbp
  __int64 v233; // rsi
  __int64 v234; // rbx
  __int64 v235; // r12
  __int64 v236; // r13
  __int64 v237; // r15
  __int64 v238; // rdi
  __int64 v239; // rcx
  __int64 v240; // rcx
  __int64 v241; // rdx
  __int64 *v242; // rax
  __int64 v243; // rax
  __int64 v244; // rcx
  __int64 *v245; // rdx
  __int64 v246; // rcx
  __int64 v247; // rdx
  __int64 *v248; // rax
  __int64 v249; // rsi
  __int64 v250; // rsi
  __int64 v251; // rdi
  _QWORD **v252; // rbp
  __int64 v253; // rcx
  int v254; // eax
  _QWORD **v255; // rdi
  __int64 v256; // rcx
  int v257; // eax
  _QWORD **v258; // rsi
  __int64 v259; // rcx
  int v260; // eax
  __int64 v261; // rbp
  __int64 v262; // rcx
  __int64 *v263; // rdx
  __int64 v264; // rax
  __int64 *v265; // rdi
  unsigned int v266; // eax
  _QWORD *v267; // rsi
  __int64 v268; // r12
  _QWORD *v269; // r13
  __int64 v270; // rbp
  __int64 v271; // rbp
  __int64 v272; // rbx
  __int64 *v273; // rdx
  __int64 v274; // rsi
  __int64 v275; // rdi
  int v276; // eax
  _QWORD **v277; // rdi
  __int64 v278; // rcx
  int v279; // eax
  _QWORD **v280; // rsi
  __int64 v281; // rcx
  int v282; // eax
  _QWORD **v283; // rdi
  __int64 v284; // rcx
  int v285; // eax
  _QWORD **v286; // rsi
  __int64 v287; // rcx
  int v288; // eax
  __int64 v289; // rbp
  __int64 v290; // rcx
  __int64 *v291; // rdx
  __int64 v292; // rax
  __int64 *v293; // rdi
  int v294; // eax
  __int64 v295; // rdx
  _QWORD **v296; // rbx
  _QWORD *v297; // rsi
  __int64 v298; // rdi
  __int64 v299; // rcx
  int v300; // eax
  _QWORD **v301; // rdi
  __int64 v302; // rcx
  int v303; // eax
  _QWORD **v304; // rsi
  __int64 v305; // rcx
  __int64 v306; // rsi
  __int64 v307; // rbx
  _QWORD *v308; // rbx
  char *v309; // rdi
  char *v310; // rsi
  signed __int64 v311; // rsi
  unsigned __int64 v312; // rcx
  __int64 v313; // rdx
  __int64 v314; // rbx
  bool v315; // al
  int v316; // eax
  __int64 v317; // rax
  volatile signed __int32 *v318; // rcx
  volatile signed __int32 *v319; // rsi
  volatile signed __int32 *v320; // rsi
  _QWORD **v321; // [rsp+20h] [rbp-88h] BYREF
  char **v322; // [rsp+28h] [rbp-80h] BYREF
  _QWORD *v323; // [rsp+30h] [rbp-78h] BYREF
  char *v324; // [rsp+38h] [rbp-70h] BYREF
  char *v325; // [rsp+40h] [rbp-68h]
  __int64 v326; // [rsp+48h] [rbp-60h]
  _QWORD *v327; // [rsp+50h] [rbp-58h] BYREF
  _QWORD *v328; // [rsp+58h] [rbp-50h]
  __int64 v329; // [rsp+60h] [rbp-48h]

  if ( a2 <= 1298951788 )
  {
    if ( a2 > 1298363496 )
    {
      if ( a2 <= 1298426991 )
      {
        if ( a2 == 1298363497 )
        {
          v41 = qword_141B5FDC8;
          ii = (__int64)&v323;
          sub_140FE7960(&v323, a3, 1668247156);
          *(_QWORD *)(a1 + 200) = sub_140FA3700(v41, &v323);
          goto LABEL_152;
        }
        if ( a2 == 1298364777 )
        {
          v8 = qword_141B5FDB0;
          ii = (__int64)&v323;
          sub_140FE7960(&v323, a3, 1667855481);
          *(_QWORD *)(a1 + 192) = sub_140FA3700(v8, &v323);
          goto LABEL_152;
        }
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      }
      if ( a2 == 1298426992 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
        {
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B5C8D0);
            if ( dword_141B5C8D0 == -1 )
            {
              sub_140DBC9B0(&qword_141B5C8A0);
              sub_141751048(sub_140DBCA10);
              sub_141750EA0(&dword_141B5C8D0);
            }
          }
          if ( *a3 == &qword_141B5C8A0 )
          {
            v150 = *((_DWORD *)a3 + 2);
            WORD1(v321) = v150 >> 17;
            LOWORD(v321) = (v150 >> 8) & 0x1FF | ((_WORD)v150 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 27 )
          {
            (*(void (__fastcall **)(__int64 *, _QWORD **, __int64 **))(**a3 + 160))(*a3, &v323, a3);
            sub_1413CA830(&v321, &v323);
          }
          else
          {
            LODWORD(v321) = 124518401;
          }
          v151 = (int)v321;
          *(_DWORD *)(a1 + 212) = (_DWORD)v321;
          LOBYTE(ii) = 1;
          if ( (v151 & 0xFFFF01FF) == 0x76C0001 )
          {
            v152 = word_141AB0260;
            if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
            {
              word_141AB0260 = 2023;
              v152 = 2023;
            }
            *(_WORD *)(a1 + 214) = v152;
            v153 = 3;
            if ( (unsigned __int16)(23593 * v152) < 0xA3Eu )
              v153 = 15;
            *(_WORD *)(a1 + 212) = ((unsigned __int16)(v152 & v153) == 0) + (v151 & 0xFE00) + 182;
          }
          return (unsigned int)ii;
        }
        *(_DWORD *)(a1 + 212) = 124518401;
        goto LABEL_152;
      }
      if ( a2 != 1298691175 )
      {
        if ( a2 == 1298756454 )
        {
          *(_BYTE *)(a1 + 210) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
LABEL_152:
          LOBYTE(ii) = 1;
          return (unsigned int)ii;
        }
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      }
      (*(void (__fastcall **)(__int64 *, _QWORD **, __int64 **))(**a3 + 128))(*a3, &v323, a3);
      v7 = (volatile signed __int32 **)(a1 + 40);
LABEL_45:
      if ( v7 != (volatile signed __int32 **)&v323 )
      {
        v6 = v323;
        v16 = *v7;
        v17 = *v7 - 1;
        if ( *v7 == nullptr )
          v17 = nullptr;
        v18 = (volatile signed __int32 *)v323 - 1;
        if ( v323 != nullptr )
        {
          if ( v16 != nullptr && _InterlockedDecrement(v17) == 0 )
            sub_1412EC9A0(v17, v6);
          *v7 = nullptr;
          _InterlockedIncrement(v18);
          v19 = v18 + 1;
        }
        else
        {
          if ( v16 != nullptr && _InterlockedDecrement(v17) == 0 )
            sub_1412EC9A0(v17, v6);
          v19 = nullptr;
        }
        *v7 = v19;
      }
      v64 = (volatile signed __int32 *)v323;
      if ( v323 != nullptr )
      {
LABEL_101:
        if ( _InterlockedDecrement(v64 - 1) == 0 )
          sub_1412EC9A0(v64 - 1, v6);
      }
      goto LABEL_152;
    }
    if ( a2 <= 1298361448 )
    {
      if ( a2 == 1145392197 )
      {
        LOBYTE(ii) = 1;
        if ( (_BYTE)word_141B60320 != 0 )
        {
          v27 = *(__int64 ***)(qword_141B5FDF0 + 128);
          v28 = *v27;
          v29 = v27[1];
          if ( *v27 != v29 )
          {
            do
            {
              v30 = *v28;
              v31 = *(_QWORD *)(*v28 + 144);
              v32 = *(_QWORD *)(*v28 + 152);
              if ( v32 != v31 )
              {
                v33 = 0;
                do
                {
                  if ( *(_QWORD *)(v31 + 8LL * (int)v33) == a1 )
                  {
                    sub_141758A00(v31 + 8LL * (int)v33, v31 + 8LL * (int)v33 + 8, v32 - (v31 + 8LL * (int)v33 + 8));
                    v31 = *(_QWORD *)(v30 + 144);
                    v32 = *(_QWORD *)(v30 + 152) - 8LL;
                    *(_QWORD *)(v30 + 152) = v32;
                    --v33;
                  }
                  ++v33;
                }
                while ( v33 < (v32 - v31) >> 3 );
              }
              ++v28;
            }
            while ( v28 != v29 );
            v27 = *(__int64 ***)(qword_141B5FDF0 + 128);
            v28 = *v27;
          }
          v99 = &v28[*(int *)(a1 + 8)];
          v100 = *v99;
          if ( *v99 != 0 )
          {
            sub_140FAD900(v100);
            sub_140FADF80(v100);
          }
          sub_141758A00(v99, v99 + 1, (char *)v27[1]-- - (char *)(v99 + 1));
          v101 = qword_141B5FDF0;
          v102 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5FDF0 + 48LL))(qword_141B5FDF0);
          if ( v102 != 0 )
          {
            v103 = v102;
            for ( i = 0; i != v103; ++i )
              *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v101 + 16LL))(v101, (unsigned int)i)
                        + 8) = i;
          }
        }
        return (unsigned int)ii;
      }
      if ( a2 == 1298231395 )
      {
        *(_BYTE *)(a1 + 211) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
        goto LABEL_152;
      }
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    }
    if ( a2 == 1298361449 )
    {
      v321 = (_QWORD **)a1;
      v322 = (char **)a1;
      v323 = &v321;
      v324 = (char *)&v322;
      v49 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
      v50 = *a3;
      v51 = **a3;
      if ( v49 == 10 )
      {
        LODWORD(ii) = 0;
        v52 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v51 + 176))(v50, a3, 0);
        v53 = *v52;
        v54 = v52[1];
        if ( *v52 != v54 )
        {
          v55 = *v52;
          while ( *(_DWORD *)v55 != 1819504496 )
          {
            v55 += 16;
            if ( v55 == v54 )
              goto LABEL_674;
          }
          if ( v55 != v54 && *(_QWORD *)(v55 + 8) != 0 )
          {
            v158 = nullptr;
            while ( *(_DWORD *)v53 != 1819504496 )
            {
              v53 += 16;
              if ( v53 == v54 )
                goto LABEL_332;
            }
            if ( v53 == v54 )
              v158 = nullptr;
            else
              v158 = *(__int64 **)(v53 + 8);
LABEL_332:
            v173 = &qword_141B5A4A0;
            if ( v158 == nullptr )
              v158 = &qword_141B5A4A0;
            switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v158 + 64LL))(*v158) )
            {
              case 0u:
                v175 = sub_141733EF0(&v321);
                goto LABEL_618;
              case 1u:
                v225 = *v52;
                v226 = v52[1];
                v227 = nullptr;
                if ( *v52 != v226 )
                {
                  while ( *(_DWORD *)v225 != 1869379180 )
                  {
                    v225 += 16;
                    if ( v225 == v226 )
                      goto LABEL_576;
                  }
                  if ( v225 == v226 )
                    v227 = nullptr;
                  else
                    v227 = *(__int64 **)(v225 + 8);
                }
LABEL_576:
                if ( v227 == nullptr )
                  v227 = &qword_141B5A4A0;
                v288 = sub_14154FAC0(&v324, v227);
                if ( v288 < 0 )
                  goto LABEL_674;
                ii = *(_QWORD *)&v322[21][8 * v288];
                if ( ii == 0 )
                  goto LABEL_674;
                v289 = *v52;
                v290 = v52[1];
                v291 = nullptr;
                if ( *v52 == v290 )
                {
                  v293 = &qword_141B5A4A0;
                }
                else
                {
                  v292 = *v52;
                  while ( *(_DWORD *)v292 != 1986096245 )
                  {
                    v292 += 16;
                    if ( v292 == v290 )
                      goto LABEL_635;
                  }
                  if ( v292 == v290 )
                    v291 = nullptr;
                  else
                    v291 = *(__int64 **)(v292 + 8);
LABEL_635:
                  v293 = &qword_141B5A4A0;
                  if ( v291 != nullptr )
                    v293 = v291;
                  v291 = nullptr;
                  while ( *(_DWORD *)v289 != 1768169504 )
                  {
                    v289 += 16;
                    if ( v289 == v290 )
                      goto LABEL_669;
                  }
                  if ( v289 == v290 )
                    v291 = nullptr;
                  else
                    v291 = *(__int64 **)(v289 + 8);
                }
LABEL_669:
                if ( v291 != nullptr )
                  v173 = v291;
                v316 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v173 + 80LL))(*v173, v173);
                if ( v316 == 1668641388 )
                {
                  (*(void (__fastcall **)(__int64, _QWORD **, __int64 *))(*(_QWORD *)*v293 + 128LL))(*v293, &v327, v293);
                  ii += 8;
                  if ( (_QWORD **)ii != &v327 )
                  {
                    v6 = v327;
                    v317 = *(_QWORD *)ii;
                    v318 = (volatile signed __int32 *)(*(_QWORD *)ii - 4LL);
                    if ( *(_QWORD *)ii == 0 )
                      v318 = nullptr;
                    v319 = (volatile signed __int32 *)v327 - 1;
                    if ( v327 != nullptr )
                    {
                      if ( v317 != 0 && _InterlockedDecrement(v318) == 0 )
                        sub_1412EC9A0(v318, v6);
                      *(_QWORD *)ii = 0;
                      _InterlockedIncrement(v319);
                      v320 = v319 + 1;
                    }
                    else
                    {
                      if ( v317 != 0 && _InterlockedDecrement(v318) == 0 )
                        sub_1412EC9A0(v318, v6);
                      v320 = nullptr;
                    }
                    *(_QWORD *)ii = v320;
                  }
                  v64 = (volatile signed __int32 *)v327;
                  if ( v327 != nullptr )
                    goto LABEL_101;
                }
                else
                {
                  if ( v316 != 1668052322 )
                    goto LABEL_674;
                  sub_140FE7960(&v327, v293, 1130589301);
                  *(_QWORD *)ii = v327;
                }
                goto LABEL_152;
              case 2u:
                v228 = *v52;
                v229 = v52[1];
                v230 = nullptr;
                if ( *v52 != v229 )
                {
                  while ( *(_DWORD *)v228 != 1869379180 )
                  {
                    v228 += 16;
                    if ( v228 == v229 )
                      goto LABEL_589;
                  }
                  if ( v228 == v229 )
                    v230 = nullptr;
                  else
                    v230 = *(__int64 **)(v228 + 8);
                }
LABEL_589:
                if ( v230 != nullptr )
                  v173 = v230;
                v294 = sub_14154FAC0(&v324, v173);
                if ( v294 < 0 || *(_QWORD *)&v322[21][8 * v294] == 0 )
                  goto LABEL_674;
                v296 = v321;
                v297 = &v321[21][v294];
                v298 = *v297;
                if ( *v297 != 0 )
                {
                  v299 = *(_QWORD *)(v298 + 8);
                  if ( v299 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v299 - 4)) == 0 )
                    sub_1412EC9A0(v299 - 4, v295);
                  sub_140FC6370(v298);
                }
                sub_141758A00(v297, v297 + 1, (char *)v296[22]-- - (char *)(v297 + 1));
                goto LABEL_152;
              case 3u:
                LOBYTE(ii) = 1;
                v231 = v322[22] - v322[21];
                if ( v231 != 0 )
                {
                  v232 = v231 >> 3;
                  v233 = -(__int64)(v231 & 0xFFFFFFFFFFFFFFF8uLL);
                  v234 = (v232 << 32) - 0x100000000LL;
                  do
                  {
                    v235 = v232 - 1;
                    if ( *(_QWORD *)(*(_QWORD *)(*(_QWORD *)v324 + 168LL) + (v234 >> 29)) != 0 )
                    {
                      v236 = *v323;
                      v237 = *(_QWORD *)(*v323 + 168LL);
                      v238 = *(_QWORD *)(v237 + 8 * v232 - 8);
                      if ( v238 != 0 )
                      {
                        v239 = *(_QWORD *)(v238 + 8);
                        if ( v239 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v239 - 4)) == 0 )
                          sub_1412EC9A0(v239 - 4, v174);
                        sub_140FC6370(v238);
                      }
                      sub_141758A00(v237 + 8 * v232 - 8, v237 + 8 * v232, v233 + *(_QWORD *)(v236 + 176) - v237);
                      *(_QWORD *)(v236 + 176) -= 8LL;
                    }
                    v233 += 8;
                    v234 -= 0x100000000LL;
                    --v232;
                  }
                  while ( v235 != 0 );
                }
                return (unsigned int)ii;
              case 4u:
                v240 = *v52;
                v241 = v52[1];
                v242 = nullptr;
                if ( *v52 == v241 )
                  goto LABEL_600;
                break;
              case 5u:
                goto LABEL_452;
              default:
                goto LABEL_674;
            }
            while ( *(_DWORD *)v240 != 1869379180 )
            {
              v240 += 16;
              if ( v240 == v241 )
                goto LABEL_600;
            }
            if ( v240 == v241 )
              v242 = nullptr;
            else
              v242 = *(__int64 **)(v240 + 8);
LABEL_600:
            if ( v242 != nullptr )
              v173 = v242;
            LODWORD(ii) = sub_14154FDA0(&v323, v173);
            return (unsigned int)ii;
          }
          goto LABEL_674;
        }
        return (unsigned int)ii;
      }
      if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v51 + 8))(v50, a3) != 11 )
        goto LABEL_674;
      v85 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      v86 = v322[22] - v322[21];
      if ( v86 != 0 )
      {
        v87 = v86 >> 3;
        v88 = -(__int64)(v86 & 0xFFFFFFFFFFFFFFF8uLL);
        v89 = (v87 << 32) - 0x100000000LL;
        do
        {
          v90 = v87 - 1;
          if ( *(_QWORD *)(*(_QWORD *)(*(_QWORD *)v324 + 168LL) + (v89 >> 29)) != 0 )
          {
            v91 = *v323;
            ii = *(_QWORD *)(*v323 + 168LL);
            v92 = *(_QWORD *)(ii + 8 * v87 - 8);
            if ( v92 != 0 )
            {
              v93 = *(_QWORD *)(v92 + 8);
              if ( v93 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v93 - 4)) == 0 )
                sub_1412EC9A0(v93 - 4, v65);
              sub_140FC6370(v92);
            }
            sub_141758A00(ii + 8 * v87 - 8, ii + 8 * v87, v88 + *(_QWORD *)(v91 + 176) - ii);
            *(_QWORD *)(v91 + 176) -= 8LL;
          }
          v88 += 8;
          v89 -= 0x100000000LL;
          --v87;
        }
        while ( v90 != 0 );
      }
      v136 = v85[1] - *v85;
      if ( v136 != 0 )
      {
        v137 = v136 >> 3;
        v138 = 1;
        if ( v137 >= 2 )
          v138 = v137;
        for ( j = 0; j != v138; ++j )
        {
          v140 = *(__int64 **)(*v85 + 8 * j);
          if ( v140 == nullptr )
            v140 = &qword_141B5A4A0;
          sub_14154FDA0(&v323, v140);
        }
      }
      v141 = qword_141B60C30;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v141 != 1986359923 )
        {
          v141 += 16;
          if ( v141 == qword_141B60C38 )
            goto LABEL_223;
        }
        if ( v141 != qword_141B60C38 )
        {
          LOBYTE(ii) = 1;
          if ( *(_QWORD *)(v141 + 8) != 0 )
            return (unsigned int)ii;
        }
      }
    }
    else
    {
      if ( a2 != 1298361705 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      v321 = (_QWORD **)a1;
      v322 = (char **)a1;
      v323 = &v321;
      v324 = (char *)&v322;
      v9 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
      v10 = *a3;
      v11 = **a3;
      if ( v9 == 10 )
      {
        LODWORD(ii) = 0;
        v12 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v11 + 176))(v10, a3, 0);
        v13 = *v12;
        v14 = v12[1];
        if ( *v12 != v14 )
        {
          v15 = *v12;
          while ( *(_DWORD *)v15 != 1819504496 )
          {
            v15 += 16;
            if ( v15 == v14 )
              goto LABEL_674;
          }
          if ( v15 != v14 && *(_QWORD *)(v15 + 8) != 0 )
          {
            v154 = nullptr;
            while ( *(_DWORD *)v13 != 1819504496 )
            {
              v13 += 16;
              if ( v13 == v14 )
                goto LABEL_303;
            }
            if ( v13 == v14 )
              v154 = nullptr;
            else
              v154 = *(__int64 **)(v13 + 8);
LABEL_303:
            v160 = &qword_141B5A4A0;
            if ( v154 == nullptr )
              v154 = &qword_141B5A4A0;
            switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v154 + 64LL))(*v154) )
            {
              case 0u:
                v161 = *v12;
                v162 = v12[1];
                v163 = nullptr;
                if ( *v12 == v162 )
                  goto LABEL_493;
                while ( *(_DWORD *)v161 != 1986096245 )
                {
                  v161 += 16;
                  if ( v161 == v162 )
                    goto LABEL_493;
                }
                goto LABEL_490;
              case 1u:
                v180 = *v12;
                v181 = v12[1];
                v182 = nullptr;
                if ( *v12 != v181 )
                {
                  while ( *(_DWORD *)v180 != 1869379180 )
                  {
                    v180 += 16;
                    if ( v180 == v181 )
                      goto LABEL_482;
                  }
                  if ( v180 == v181 )
                    v182 = nullptr;
                  else
                    v182 = *(__int64 **)(v180 + 8);
                }
LABEL_482:
                if ( v182 == nullptr )
                  v182 = &qword_141B5A4A0;
                v254 = sub_14154F4C0(&v324, v182);
                if ( v254 < 0 || *(_QWORD *)&v322[9][8 * v254] == 0 )
                  goto LABEL_674;
                v255 = v321;
                v256 = (__int64)&v321[9][v254];
                sub_141758A00(v256, v256 + 8, (char *)v321[10] - v256 - 8);
                --v255[10];
                v161 = *v12;
                v162 = v12[1];
                v163 = nullptr;
                if ( *v12 == v162 )
                  goto LABEL_493;
                while ( *(_DWORD *)v161 != 1986096245 )
                {
                  v161 += 16;
                  if ( v161 == v162 )
                    goto LABEL_493;
                }
                goto LABEL_490;
              case 2u:
                v183 = *v12;
                v184 = v12[1];
                v185 = nullptr;
                if ( *v12 != v184 )
                {
                  while ( *(_DWORD *)v183 != 1869379180 )
                  {
                    v183 += 16;
                    if ( v183 == v184 )
                      goto LABEL_497;
                  }
                  if ( v183 == v184 )
                    v185 = nullptr;
                  else
                    v185 = *(__int64 **)(v183 + 8);
                }
LABEL_497:
                if ( v185 != nullptr )
                  v160 = v185;
                v257 = sub_14154F4C0(&v324, v160);
                if ( v257 < 0 || *(_QWORD *)&v322[9][8 * v257] == 0 )
                  goto LABEL_674;
                v258 = v321;
                v259 = (__int64)&v321[9][v257];
                sub_141758A00(v259, v259 + 8, (char *)v321[10] - v259 - 8);
                --v258[10];
                goto LABEL_152;
              case 3u:
                LOBYTE(ii) = 1;
                v186 = v322[10] - v322[9];
                if ( v186 != 0 )
                {
                  v187 = v186 >> 3;
                  v188 = (v187 << 32) - 0x100000000LL;
                  do
                  {
                    --v187;
                    if ( *(_QWORD *)&v322[9][v188 >> 29] != 0 )
                    {
                      v189 = v321;
                      v190 = (__int64)&v321[9][v188 >> 32];
                      sub_141758A00(v190, v190 + 8, (char *)v321[10] - v190 - 8);
                      --v189[10];
                    }
                    v188 -= 0x100000000LL;
                  }
                  while ( v187 != 0 );
                }
                return (unsigned int)ii;
              case 4u:
                v161 = *v12;
                v162 = v12[1];
                v163 = nullptr;
                if ( *v12 == v162 )
                  goto LABEL_493;
                break;
              case 5u:
                goto LABEL_452;
              default:
                goto LABEL_674;
            }
            while ( *(_DWORD *)v161 != 1869379180 )
            {
              v161 += 16;
              if ( v161 == v162 )
                goto LABEL_493;
            }
LABEL_490:
            if ( v161 == v162 )
              v163 = nullptr;
            else
              v163 = *(__int64 **)(v161 + 8);
LABEL_493:
            if ( v163 != nullptr )
              v160 = v163;
            v175 = sub_141733B70(&v321, v160);
LABEL_618:
            LOBYTE(ii) = v175 != 0;
            return (unsigned int)ii;
          }
          goto LABEL_674;
        }
        return (unsigned int)ii;
      }
      if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v11 + 8))(v10, a3) != 11 )
        goto LABEL_674;
      ii = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      v66 = v322[10] - v322[9];
      if ( v66 != 0 )
      {
        v67 = v66 >> 3;
        v68 = (v67 << 32) - 0x100000000LL;
        do
        {
          --v67;
          if ( *(_QWORD *)&v322[9][v68 >> 29] != 0 )
          {
            v69 = v321;
            v70 = (__int64)&v321[9][v68 >> 32];
            sub_141758A00(v70, v70 + 8, (char *)v321[10] - v70 - 8);
            --v69[10];
          }
          v68 -= 0x100000000LL;
        }
        while ( v67 != 0 );
      }
      v105 = *(_QWORD *)(ii + 8) - *(_QWORD *)ii;
      if ( v105 != 0 )
      {
        v106 = v105 >> 3;
        v107 = 1;
        if ( v106 >= 2 )
          v107 = v106;
        for ( k = 0; k != v107; ++k )
        {
          v109 = *(__int64 **)(*(_QWORD *)ii + 8 * k);
          if ( v109 == nullptr )
            v109 = &qword_141B5A4A0;
          sub_141733B70(&v321, v109);
        }
      }
      v110 = qword_141B60C30;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v110 != 1986359923 )
        {
          v110 += 16;
          if ( v110 == qword_141B60C38 )
            goto LABEL_223;
        }
        if ( v110 != qword_141B60C38 )
        {
          LOBYTE(ii) = 1;
          if ( *(_QWORD *)(v110 + 8) != 0 )
            return (unsigned int)ii;
        }
      }
    }
LABEL_223:
    LOBYTE(ii) = 1;
    LOBYTE(v65) = 1;
    sub_140DD5C90(&v323, v65);
    return (unsigned int)ii;
  }
  if ( a2 <= 1299343208 )
  {
    if ( a2 > 1299084392 )
    {
      if ( a2 != 1299084393 )
      {
        if ( a2 == 1299211634 )
        {
          *(_BYTE *)(a1 + 240) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          goto LABEL_152;
        }
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      }
      v321 = (_QWORD **)a1;
      v322 = (char **)a1;
      v323 = &v321;
      v324 = (char *)&v322;
      v56 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
      v57 = *a3;
      v58 = **a3;
      if ( v56 == 10 )
      {
        LODWORD(ii) = 0;
        v59 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v58 + 176))(v57, a3, 0);
        v60 = *v59;
        v61 = v59[1];
        if ( *v59 != v61 )
        {
          v62 = *v59;
          while ( *(_DWORD *)v62 != 1819504496 )
          {
            v62 += 16;
            if ( v62 == v61 )
              goto LABEL_674;
          }
          if ( v62 != v61 && *(_QWORD *)(v62 + 8) != 0 )
          {
            v159 = nullptr;
            while ( *(_DWORD *)v60 != 1819504496 )
            {
              v60 += 16;
              if ( v60 == v61 )
                goto LABEL_337;
            }
            if ( v60 == v61 )
              v159 = nullptr;
            else
              v159 = *(__int64 **)(v60 + 8);
LABEL_337:
            v176 = &qword_141B5A4A0;
            if ( v159 == nullptr )
              v159 = &qword_141B5A4A0;
            switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v159 + 64LL))(*v159) )
            {
              case 0u:
                v177 = *v59;
                v178 = v59[1];
                v179 = nullptr;
                if ( *v59 == v178 )
                  goto LABEL_615;
                while ( *(_DWORD *)v177 != 1986096245 )
                {
                  v177 += 16;
                  if ( v177 == v178 )
                    goto LABEL_615;
                }
                goto LABEL_612;
              case 1u:
                v243 = *v59;
                v244 = v59[1];
                v245 = nullptr;
                if ( *v59 != v244 )
                {
                  while ( *(_DWORD *)v243 != 1869379180 )
                  {
                    v243 += 16;
                    if ( v243 == v244 )
                      goto LABEL_604;
                  }
                  if ( v243 == v244 )
                    v245 = nullptr;
                  else
                    v245 = *(__int64 **)(v243 + 8);
                }
LABEL_604:
                if ( v245 == nullptr )
                  v245 = &qword_141B5A4A0;
                v300 = sub_14154EDE0(&v324, v245);
                if ( v300 < 0 || *(_QWORD *)&v322[12][8 * v300] == 0 )
                  goto LABEL_674;
                v301 = v321;
                v302 = (__int64)&v321[12][v300];
                sub_141758A00(v302, v302 + 8, (char *)v321[13] - v302 - 8);
                --v301[13];
                v177 = *v59;
                v178 = v59[1];
                v179 = nullptr;
                if ( *v59 == v178 )
                  goto LABEL_615;
                while ( *(_DWORD *)v177 != 1986096245 )
                {
                  v177 += 16;
                  if ( v177 == v178 )
                    goto LABEL_615;
                }
                goto LABEL_612;
              case 2u:
                v246 = *v59;
                v247 = v59[1];
                v248 = nullptr;
                if ( *v59 != v247 )
                {
                  while ( *(_DWORD *)v246 != 1869379180 )
                  {
                    v246 += 16;
                    if ( v246 == v247 )
                      goto LABEL_620;
                  }
                  if ( v246 == v247 )
                    v248 = nullptr;
                  else
                    v248 = *(__int64 **)(v246 + 8);
                }
LABEL_620:
                if ( v248 != nullptr )
                  v176 = v248;
                v303 = sub_14154EDE0(&v324, v176);
                if ( v303 < 0 || *(_QWORD *)&v322[12][8 * v303] == 0 )
                  goto LABEL_674;
                v304 = v321;
                v305 = (__int64)&v321[12][v303];
                sub_141758A00(v305, v305 + 8, (char *)v321[13] - v305 - 8);
                --v304[13];
                goto LABEL_152;
              case 3u:
                LOBYTE(ii) = 1;
                v249 = v322[13] - v322[12];
                if ( v249 != 0 )
                {
                  v250 = v249 >> 3;
                  v251 = (v250 << 32) - 0x100000000LL;
                  do
                  {
                    --v250;
                    if ( *(_QWORD *)&v322[12][v251 >> 29] != 0 )
                    {
                      v252 = v321;
                      v253 = (__int64)&v321[12][v251 >> 32];
                      sub_141758A00(v253, v253 + 8, (char *)v321[13] - v253 - 8);
                      --v252[13];
                    }
                    v251 -= 0x100000000LL;
                  }
                  while ( v250 != 0 );
                }
                return (unsigned int)ii;
              case 4u:
                v177 = *v59;
                v178 = v59[1];
                v179 = nullptr;
                if ( *v59 == v178 )
                  goto LABEL_615;
                break;
              case 5u:
LABEL_452:
                sub_140DD5C90(&v323, 0);
                goto LABEL_152;
              default:
                goto LABEL_674;
            }
            while ( *(_DWORD *)v177 != 1869379180 )
            {
              v177 += 16;
              if ( v177 == v178 )
                goto LABEL_615;
            }
LABEL_612:
            if ( v177 == v178 )
              v179 = nullptr;
            else
              v179 = *(__int64 **)(v177 + 8);
LABEL_615:
            if ( v179 != nullptr )
              v176 = v179;
            v175 = sub_141733800(&v321, v176);
            goto LABEL_618;
          }
          goto LABEL_674;
        }
        return (unsigned int)ii;
      }
      if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v58 + 8))(v57, a3) != 11 )
        goto LABEL_674;
      ii = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      v94 = v322[13] - v322[12];
      if ( v94 != 0 )
      {
        v95 = v94 >> 3;
        v96 = (v95 << 32) - 0x100000000LL;
        do
        {
          --v95;
          if ( *(_QWORD *)&v322[12][v96 >> 29] != 0 )
          {
            v97 = v321;
            v98 = (__int64)&v321[12][v96 >> 32];
            sub_141758A00(v98, v98 + 8, (char *)v321[13] - v98 - 8);
            --v97[13];
          }
          v96 -= 0x100000000LL;
        }
        while ( v95 != 0 );
      }
      v142 = *(_QWORD *)(ii + 8) - *(_QWORD *)ii;
      if ( v142 != 0 )
      {
        v143 = v142 >> 3;
        v144 = 1;
        if ( v143 >= 2 )
          v144 = v143;
        for ( m = 0; m != v144; ++m )
        {
          v146 = *(__int64 **)(*(_QWORD *)ii + 8 * m);
          if ( v146 == nullptr )
            v146 = &qword_141B5A4A0;
          sub_141733800(&v321, v146);
        }
      }
      v147 = qword_141B60C30;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v147 != 1986359923 )
        {
          v147 += 16;
          if ( v147 == qword_141B60C38 )
            goto LABEL_223;
        }
        if ( v147 != qword_141B60C38 )
        {
          LOBYTE(ii) = 1;
          if ( *(_QWORD *)(v147 + 8) != 0 )
            return (unsigned int)ii;
        }
      }
    }
    else
    {
      if ( a2 != 1298951789 )
      {
        if ( a2 != 1299079533 )
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        (*(void (__fastcall **)(__int64 *, _QWORD **, __int64 **))(**a3 + 128))(*a3, &v323, a3);
        v7 = (volatile signed __int32 **)(a1 + 24);
        goto LABEL_45;
      }
      v321 = (_QWORD **)a1;
      v322 = (char **)a1;
      v323 = &v321;
      v324 = (char *)&v322;
      v34 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
      v35 = *a3;
      v36 = **a3;
      if ( v34 == 10 )
      {
        LODWORD(ii) = 0;
        v37 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v36 + 176))(v35, a3, 0);
        v38 = *v37;
        v39 = v37[1];
        if ( *v37 != v39 )
        {
          v40 = *v37;
          while ( *(_DWORD *)v40 != 1819504496 )
          {
            v40 += 16;
            if ( v40 == v39 )
              goto LABEL_674;
          }
          if ( v40 != v39 && *(_QWORD *)(v40 + 8) != 0 )
          {
            v156 = nullptr;
            while ( *(_DWORD *)v38 != 1819504496 )
            {
              v38 += 16;
              if ( v38 == v39 )
                goto LABEL_316;
            }
            if ( v38 == v39 )
              v156 = nullptr;
            else
              v156 = *(__int64 **)(v38 + 8);
LABEL_316:
            v165 = &qword_141B5A4A0;
            if ( v156 == nullptr )
              v156 = &qword_141B5A4A0;
            switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v156 + 64LL))(*v156) )
            {
              case 0u:
                v166 = *v37;
                v167 = v37[1];
                v168 = nullptr;
                if ( *v37 == v167 )
                  goto LABEL_545;
                while ( *(_DWORD *)v166 != 1986096245 )
                {
                  v166 += 16;
                  if ( v166 == v167 )
                    goto LABEL_545;
                }
                goto LABEL_542;
              case 1u:
                v203 = *v37;
                v204 = v37[1];
                v205 = nullptr;
                if ( *v37 != v204 )
                {
                  while ( *(_DWORD *)v203 != 1869379180 )
                  {
                    v203 += 16;
                    if ( v203 == v204 )
                      goto LABEL_534;
                  }
                  if ( v203 == v204 )
                    v205 = nullptr;
                  else
                    v205 = *(__int64 **)(v203 + 8);
                }
LABEL_534:
                if ( v205 == nullptr )
                  v205 = &qword_141B5A4A0;
                v276 = sub_14154F7C0(&v324, v205);
                if ( v276 < 0 || *(_QWORD *)&v322[18][8 * v276] == 0 )
                  goto LABEL_674;
                v277 = v321;
                v278 = (__int64)&v321[18][v276];
                sub_141758A00(v278, v278 + 8, (char *)v321[19] - v278 - 8);
                --v277[19];
                v166 = *v37;
                v167 = v37[1];
                v168 = nullptr;
                if ( *v37 == v167 )
                  goto LABEL_545;
                while ( *(_DWORD *)v166 != 1986096245 )
                {
                  v166 += 16;
                  if ( v166 == v167 )
                    goto LABEL_545;
                }
                goto LABEL_542;
              case 2u:
                v206 = *v37;
                v207 = v37[1];
                v208 = nullptr;
                if ( *v37 != v207 )
                {
                  while ( *(_DWORD *)v206 != 1869379180 )
                  {
                    v206 += 16;
                    if ( v206 == v207 )
                      goto LABEL_549;
                  }
                  if ( v206 == v207 )
                    v208 = nullptr;
                  else
                    v208 = *(__int64 **)(v206 + 8);
                }
LABEL_549:
                if ( v208 != nullptr )
                  v165 = v208;
                v279 = sub_14154F7C0(&v324, v165);
                if ( v279 < 0 || *(_QWORD *)&v322[18][8 * v279] == 0 )
                  goto LABEL_674;
                v280 = v321;
                v281 = (__int64)&v321[18][v279];
                sub_141758A00(v281, v281 + 8, (char *)v321[19] - v281 - 8);
                --v280[19];
                goto LABEL_152;
              case 3u:
                LOBYTE(ii) = 1;
                v209 = v322[19] - v322[18];
                if ( v209 != 0 )
                {
                  v210 = v209 >> 3;
                  v211 = (v210 << 32) - 0x100000000LL;
                  do
                  {
                    --v210;
                    if ( *(_QWORD *)&v322[18][v211 >> 29] != 0 )
                    {
                      v212 = v321;
                      v213 = (__int64)&v321[18][v211 >> 32];
                      sub_141758A00(v213, v213 + 8, (char *)v321[19] - v213 - 8);
                      --v212[19];
                    }
                    v211 -= 0x100000000LL;
                  }
                  while ( v210 != 0 );
                }
                return (unsigned int)ii;
              case 4u:
                v166 = *v37;
                v167 = v37[1];
                v168 = nullptr;
                if ( *v37 == v167 )
                  goto LABEL_545;
                break;
              case 5u:
                goto LABEL_452;
              default:
                goto LABEL_674;
            }
            while ( *(_DWORD *)v166 != 1869379180 )
            {
              v166 += 16;
              if ( v166 == v167 )
                goto LABEL_545;
            }
LABEL_542:
            if ( v166 == v167 )
              v168 = nullptr;
            else
              v168 = *(__int64 **)(v166 + 8);
LABEL_545:
            if ( v168 != nullptr )
              v165 = v168;
            v175 = sub_141733D20(&v321, v165);
            goto LABEL_618;
          }
          goto LABEL_674;
        }
        return (unsigned int)ii;
      }
      if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v36 + 8))(v35, a3) != 11 )
        goto LABEL_674;
      ii = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      v75 = v322[19] - v322[18];
      if ( v75 != 0 )
      {
        v76 = v75 >> 3;
        v77 = (v76 << 32) - 0x100000000LL;
        do
        {
          --v76;
          if ( *(_QWORD *)&v322[18][v77 >> 29] != 0 )
          {
            v78 = v321;
            v79 = (__int64)&v321[18][v77 >> 32];
            sub_141758A00(v79, v79 + 8, (char *)v321[19] - v79 - 8);
            --v78[19];
          }
          v77 -= 0x100000000LL;
        }
        while ( v76 != 0 );
      }
      v124 = *(_QWORD *)(ii + 8) - *(_QWORD *)ii;
      if ( v124 != 0 )
      {
        v125 = v124 >> 3;
        v126 = 1;
        if ( v125 >= 2 )
          v126 = v125;
        for ( n = 0; n != v126; ++n )
        {
          v128 = *(__int64 **)(*(_QWORD *)ii + 8 * n);
          if ( v128 == nullptr )
            v128 = &qword_141B5A4A0;
          sub_141733D20(&v321, v128);
        }
      }
      v129 = qword_141B60C30;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v129 != 1986359923 )
        {
          v129 += 16;
          if ( v129 == qword_141B60C38 )
            goto LABEL_223;
        }
        if ( v129 != qword_141B60C38 )
        {
          LOBYTE(ii) = 1;
          if ( *(_QWORD *)(v129 + 8) != 0 )
            return (unsigned int)ii;
        }
      }
    }
    goto LABEL_223;
  }
  if ( a2 > 1299412088 )
  {
    if ( a2 == 1299412089 )
    {
      *(_BYTE *)(a1 + 208) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_152;
    }
    if ( a2 != 1299478896 )
    {
      if ( a2 != 1299542636 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      (*(void (__fastcall **)(__int64 *, _QWORD **, __int64 **))(**a3 + 128))(*a3, &v323, a3);
      v7 = (volatile signed __int32 **)(a1 + 32);
      goto LABEL_45;
    }
    v323 = (_QWORD *)a1;
    sub_141733370(&v324, a1);
    v321 = &v323;
    v322 = &v324;
    v20 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
    v21 = *a3;
    v22 = **a3;
    if ( v20 == 10 )
    {
      LODWORD(ii) = 0;
      v23 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v22 + 176))(v21, a3, 0);
      v24 = *v23;
      v25 = v23[1];
      if ( *v23 == v25 )
      {
LABEL_649:
        v308 = v324;
        v309 = v325;
        if ( v324 != v325 )
        {
          v310 = v324;
          do
          {
            if ( *(_QWORD *)v310 != 0 )
              sub_141750CFC();
            v310 += 8;
          }
          while ( v310 != v309 );
          v311 = v325 - v309;
          sub_141758A00(v308, v309, v325 - v309);
          v325 = (char *)v308 + v311;
          v309 = v324;
        }
        if ( v309 != nullptr )
        {
          v312 = v326 - (_QWORD)v309;
          if ( v326 - (_QWORD)v309 == -1 )
            v312 = *(unsigned int *)&v309[-*(unsigned int *)(qword_141ABD470 + 48)];
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v313 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v313) >> 3 > v312)
            && (v314 = *(_QWORD *)(v313 + 8 * v312)) != 0 )
          {
            MEMORY[0x1419475D8](v314 + 32, &v309[-*(unsigned int *)(v314 + 120)]);
            v315 = *(_BYTE *)(v314 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v314 + 64)) != 0;
            if ( !v315 && *(_BYTE *)(v314 + 97) != 0 )
              sub_1412D33C0(v314);
          }
          else
          {
            MEMORY[0x141948990](&v309[-*(unsigned int *)(qword_141ABD470 + 48)]);
          }
        }
        return (unsigned int)ii;
      }
      v26 = *v23;
      while ( *(_DWORD *)v26 != 1819504496 )
      {
        v26 += 16;
        if ( v26 == v25 )
          goto LABEL_648;
      }
      if ( v26 != v25 && *(_QWORD *)(v26 + 8) != 0 )
      {
        v155 = nullptr;
        while ( *(_DWORD *)v24 != 1819504496 )
        {
          v24 += 16;
          if ( v24 == v25 )
            goto LABEL_311;
        }
        if ( v24 == v25 )
          v155 = nullptr;
        else
          v155 = *(__int64 **)(v24 + 8);
LABEL_311:
        v164 = &qword_141B5A4A0;
        if ( v155 == nullptr )
          v155 = &qword_141B5A4A0;
        switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v155 + 64LL))(*v155) )
        {
          case 0u:
            LOBYTE(ii) = sub_141733650(&v323) != 0;
            goto LABEL_649;
          case 1u:
            v191 = *v23;
            v192 = v23[1];
            v193 = nullptr;
            if ( *v23 != v192 )
            {
              while ( *(_DWORD *)v191 != 1869379180 )
              {
                v191 += 16;
                if ( v191 == v192 )
                  goto LABEL_503;
              }
              if ( v191 == v192 )
                v193 = nullptr;
              else
                v193 = *(__int64 **)(v191 + 8);
            }
LABEL_503:
            if ( v193 == nullptr )
              v193 = &qword_141B5A4A0;
            v260 = sub_14154EB20(&v322, v193);
            if ( v260 < 0 )
              goto LABEL_648;
            ii = *(_QWORD *)&v324[8 * v260];
            if ( ii == 0 )
              goto LABEL_648;
            v261 = *v23;
            v262 = v23[1];
            v263 = nullptr;
            if ( *v23 == v262 )
            {
              v265 = &qword_141B5A4A0;
            }
            else
            {
              v264 = *v23;
              while ( *(_DWORD *)v264 != 1986096245 )
              {
                v264 += 16;
                if ( v264 == v262 )
                  goto LABEL_626;
              }
              v263 = v264 == v262 ? nullptr : *(__int64 **)(v264 + 8);
LABEL_626:
              v265 = &qword_141B5A4A0;
              if ( v263 != nullptr )
                v265 = v263;
              v263 = nullptr;
              while ( *(_DWORD *)v261 != 1768169504 )
              {
                v261 += 16;
                if ( v261 == v262 )
                  goto LABEL_644;
              }
              v263 = v261 == v262 ? nullptr : *(__int64 **)(v261 + 8);
            }
LABEL_644:
            if ( v263 != nullptr )
              v164 = v263;
            if ( (*(unsigned int (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v164 + 80LL))(*v164, v164) != 1299478896 )
              goto LABEL_648;
            v306 = *(_QWORD *)ii;
            v307 = *(int *)(ii + 8);
            LOBYTE(v327) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v265 + 64LL))(*v265, v265);
            sub_14099B190(v306 + 48, &v327, v307);
            LOBYTE(ii) = 1;
            goto LABEL_649;
          case 2u:
            v194 = *v23;
            v195 = v23[1];
            v196 = nullptr;
            if ( *v23 != v195 )
            {
              while ( *(_DWORD *)v194 != 1869379180 )
              {
                v194 += 16;
                if ( v194 == v195 )
                  goto LABEL_516;
              }
              if ( v194 == v195 )
                v196 = nullptr;
              else
                v196 = *(__int64 **)(v194 + 8);
            }
LABEL_516:
            if ( v196 != nullptr )
              v164 = v196;
            v266 = sub_14154EB20(&v322, v164);
            if ( (v266 & 0x80000000) != 0 || *(_QWORD *)&v324[8 * v266] == 0 )
              goto LABEL_648;
            v267 = v323;
            sub_141758A00(v323[6] + v266, v323[6] + v266 + 1LL, v323[7] - (v323[6] + v266 + 1LL));
            --v267[7];
            LOBYTE(ii) = 1;
            goto LABEL_649;
          case 3u:
            LOBYTE(ii) = 1;
            if ( v325 != v324 )
            {
              v197 = (v325 - v324) >> 3;
              v198 = (v197 << 32) - 0x100000000LL;
              do
              {
                v73 = *(_QWORD *)&v324[8 * v197-- - 8] == 0;
                if ( !v73 )
                {
                  v199 = v323;
                  sub_141758A00(
                    v323[6] + (v198 >> 32),
                    v323[6] + (v198 >> 32) + 1,
                    v323[7] - (v323[6] + (v198 >> 32) + 1));
                  --v199[7];
                }
                v198 -= 0x100000000LL;
              }
              while ( v197 != 0 );
            }
            goto LABEL_649;
          case 4u:
            v200 = *v23;
            v201 = v23[1];
            v202 = nullptr;
            if ( v200 == v201 )
              goto LABEL_522;
            break;
          case 5u:
            sub_140DF3CB0(0);
            LOBYTE(ii) = 1;
            goto LABEL_649;
          default:
            goto LABEL_648;
        }
        while ( *(_DWORD *)v200 != 1869379180 )
        {
          v200 += 16;
          if ( v200 == v201 )
            goto LABEL_522;
        }
        if ( v200 == v201 )
          v202 = nullptr;
        else
          v202 = *(__int64 **)(v200 + 8);
LABEL_522:
        v268 = sub_141733650(&v323);
        if ( v268 != 0 )
        {
          if ( v202 == nullptr )
            v202 = &qword_141B5A4A0;
          v269 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v202 + 176LL))(
                             *v202,
                             v202,
                             0);
          v270 = v269[1] - *v269;
          if ( v270 != 0 )
          {
            v271 = v270 >> 4;
            v272 = 8;
            ii = (__int64)&v327;
            do
            {
              if ( *(_DWORD *)(*v269 + v272 - 8) == 1299478896 )
              {
                v273 = *(__int64 **)(*v269 + v272);
                if ( v273 == nullptr )
                  v273 = &qword_141B5A4A0;
                v274 = *(_QWORD *)v268;
                v275 = *(int *)(v268 + 8);
                LOBYTE(v327) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v273 + 64LL))(*v273);
                sub_14099B190(v274 + 48, &v327, v275);
              }
              v272 += 16;
              --v271;
            }
            while ( v271 != 0 );
          }
        }
        LOBYTE(ii) = v268 != 0;
        goto LABEL_649;
      }
    }
    else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v22 + 8))(v21, a3) == 11 )
    {
      v328 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      if ( v325 != v324 )
      {
        v71 = (v325 - v324) >> 3;
        v72 = (v71 << 32) - 0x100000000LL;
        do
        {
          v73 = *(_QWORD *)&v324[8 * v71-- - 8] == 0;
          if ( !v73 )
          {
            v74 = v323;
            sub_141758A00(v323[6] + (v72 >> 32), v323[6] + (v72 >> 32) + 1, v323[7] - (v323[6] + (v72 >> 32) + 1));
            --v74[7];
          }
          v72 -= 0x100000000LL;
        }
        while ( v71 != 0 );
      }
      v111 = v328[1] - *v328;
      if ( v111 != 0 )
      {
        v112 = v111 >> 3;
        v113 = 1;
        if ( v112 >= 2 )
          v113 = v112;
        v329 = v113;
        for ( ii = 0; ii != v329; ++ii )
        {
          v114 = *(__int64 **)(*v328 + 8 * ii);
          v115 = sub_141733650(&v323);
          if ( v115 != 0 )
          {
            v116 = v115;
            if ( v114 == nullptr )
              v114 = &qword_141B5A4A0;
            v117 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v114 + 176LL))(
                               *v114,
                               v114,
                               0);
            v118 = v117[1] - *v117;
            if ( v118 != 0 )
            {
              v119 = v118 >> 4;
              v120 = 8;
              do
              {
                if ( *(_DWORD *)(*v117 + v120 - 8) == 1299478896 )
                {
                  v121 = *(__int64 **)(*v117 + v120);
                  if ( v121 == nullptr )
                    v121 = &qword_141B5A4A0;
                  v122 = *(_QWORD *)v116;
                  v123 = *(int *)(v116 + 8);
                  LOBYTE(v327) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v121 + 64LL))(*v121);
                  sub_14099B190(v122 + 48, &v327, v123);
                }
                v120 += 16;
                --v119;
              }
              while ( v119 != 0 );
            }
          }
        }
      }
      v148 = qword_141B60C38;
      v149 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_227;
      while ( *(_DWORD *)v149 != 1986359923 )
      {
        v149 += 16;
        if ( v149 == qword_141B60C38 )
          goto LABEL_227;
      }
      if ( v149 == qword_141B60C38 || (LOBYTE(ii) = 1, *(_QWORD *)(v149 + 8) == 0) )
      {
LABEL_227:
        LOBYTE(ii) = 1;
        LOBYTE(v148) = 1;
        sub_140DF3CB0(v148);
      }
      goto LABEL_649;
    }
LABEL_648:
    LODWORD(ii) = 0;
    goto LABEL_649;
  }
  if ( a2 != 1299343209 )
  {
    if ( a2 == 1299407728 )
    {
      *(_BYTE *)(a1 + 241) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_152;
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  v321 = (_QWORD **)a1;
  v322 = (char **)a1;
  v323 = &v321;
  v324 = (char *)&v322;
  v42 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
  v43 = *a3;
  v44 = **a3;
  if ( v42 != 10 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v44 + 8))(v43, a3) != 11 )
      goto LABEL_674;
    ii = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
    v80 = v322[16] - v322[15];
    if ( v80 != 0 )
    {
      v81 = v80 >> 3;
      v82 = (v81 << 32) - 0x100000000LL;
      do
      {
        --v81;
        if ( *(_QWORD *)&v322[15][v82 >> 29] != 0 )
        {
          v83 = v321;
          v84 = (__int64)&v321[15][v82 >> 32];
          sub_141758A00(v84, v84 + 8, (char *)v321[16] - v84 - 8);
          --v83[16];
        }
        v82 -= 0x100000000LL;
      }
      while ( v81 != 0 );
    }
    v130 = *(_QWORD *)(ii + 8) - *(_QWORD *)ii;
    if ( v130 != 0 )
    {
      v131 = v130 >> 3;
      v132 = 1;
      if ( v131 >= 2 )
        v132 = v131;
      for ( jj = 0; jj != v132; ++jj )
      {
        v134 = *(__int64 **)(*(_QWORD *)ii + 8 * jj);
        if ( v134 == nullptr )
          v134 = &qword_141B5A4A0;
        sub_1417339B0(&v321, v134);
      }
    }
    v135 = qword_141B60C30;
    if ( qword_141B60C30 != qword_141B60C38 )
    {
      while ( *(_DWORD *)v135 != 1986359923 )
      {
        v135 += 16;
        if ( v135 == qword_141B60C38 )
          goto LABEL_223;
      }
      if ( v135 != qword_141B60C38 )
      {
        LOBYTE(ii) = 1;
        if ( *(_QWORD *)(v135 + 8) != 0 )
          return (unsigned int)ii;
      }
    }
    goto LABEL_223;
  }
  LODWORD(ii) = 0;
  v45 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v44 + 176))(v43, a3, 0);
  v46 = *v45;
  v47 = v45[1];
  if ( *v45 != v47 )
  {
    v48 = *v45;
    while ( *(_DWORD *)v48 != 1819504496 )
    {
      v48 += 16;
      if ( v48 == v47 )
        goto LABEL_674;
    }
    if ( v48 != v47 && *(_QWORD *)(v48 + 8) != 0 )
    {
      v157 = nullptr;
      while ( *(_DWORD *)v46 != 1819504496 )
      {
        v46 += 16;
        if ( v46 == v47 )
          goto LABEL_324;
      }
      if ( v46 == v47 )
        v157 = nullptr;
      else
        v157 = *(__int64 **)(v46 + 8);
LABEL_324:
      v169 = &qword_141B5A4A0;
      if ( v157 == nullptr )
        v157 = &qword_141B5A4A0;
      switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v157 + 64LL))(*v157) )
      {
        case 0u:
          v170 = *v45;
          v171 = v45[1];
          v172 = nullptr;
          if ( *v45 == v171 )
            goto LABEL_566;
          while ( *(_DWORD *)v170 != 1986096245 )
          {
            v170 += 16;
            if ( v170 == v171 )
              goto LABEL_566;
          }
          goto LABEL_563;
        case 1u:
          v214 = *v45;
          v215 = v45[1];
          v216 = nullptr;
          if ( *v45 != v215 )
          {
            while ( *(_DWORD *)v214 != 1869379180 )
            {
              v214 += 16;
              if ( v214 == v215 )
                goto LABEL_555;
            }
            if ( v214 == v215 )
              v216 = nullptr;
            else
              v216 = *(__int64 **)(v214 + 8);
          }
LABEL_555:
          if ( v216 == nullptr )
            v216 = &qword_141B5A4A0;
          v282 = sub_14154F1C0(&v324, v216);
          if ( v282 < 0 || *(_QWORD *)&v322[15][8 * v282] == 0 )
            goto LABEL_674;
          v283 = v321;
          v284 = (__int64)&v321[15][v282];
          sub_141758A00(v284, v284 + 8, (char *)v321[16] - v284 - 8);
          --v283[16];
          v170 = *v45;
          v171 = v45[1];
          v172 = nullptr;
          if ( *v45 == v171 )
            goto LABEL_566;
          while ( *(_DWORD *)v170 != 1986096245 )
          {
            v170 += 16;
            if ( v170 == v171 )
              goto LABEL_566;
          }
          goto LABEL_563;
        case 2u:
          v217 = *v45;
          v218 = v45[1];
          v219 = nullptr;
          if ( *v45 != v218 )
          {
            while ( *(_DWORD *)v217 != 1869379180 )
            {
              v217 += 16;
              if ( v217 == v218 )
                goto LABEL_570;
            }
            if ( v217 == v218 )
              v219 = nullptr;
            else
              v219 = *(__int64 **)(v217 + 8);
          }
LABEL_570:
          if ( v219 != nullptr )
            v169 = v219;
          v285 = sub_14154F1C0(&v324, v169);
          if ( v285 < 0 || *(_QWORD *)&v322[15][8 * v285] == 0 )
            goto LABEL_674;
          v286 = v321;
          v287 = (__int64)&v321[15][v285];
          sub_141758A00(v287, v287 + 8, (char *)v321[16] - v287 - 8);
          --v286[16];
          goto LABEL_152;
        case 3u:
          LOBYTE(ii) = 1;
          v220 = v322[16] - v322[15];
          if ( v220 != 0 )
          {
            v221 = v220 >> 3;
            v222 = (v221 << 32) - 0x100000000LL;
            do
            {
              --v221;
              if ( *(_QWORD *)&v322[15][v222 >> 29] != 0 )
              {
                v223 = v321;
                v224 = (__int64)&v321[15][v222 >> 32];
                sub_141758A00(v224, v224 + 8, (char *)v321[16] - v224 - 8);
                --v223[16];
              }
              v222 -= 0x100000000LL;
            }
            while ( v221 != 0 );
          }
          return (unsigned int)ii;
        case 4u:
          v170 = *v45;
          v171 = v45[1];
          v172 = nullptr;
          if ( *v45 == v171 )
            goto LABEL_566;
          break;
        case 5u:
          goto LABEL_452;
        default:
          goto LABEL_674;
      }
      while ( *(_DWORD *)v170 != 1869379180 )
      {
        v170 += 16;
        if ( v170 == v171 )
          goto LABEL_566;
      }
LABEL_563:
      if ( v170 == v171 )
        v172 = nullptr;
      else
        v172 = *(__int64 **)(v170 + 8);
LABEL_566:
      if ( v172 != nullptr )
        v169 = v172;
      v175 = sub_1417339B0(&v321, v169);
      goto LABEL_618;
    }
LABEL_674:
    LODWORD(ii) = 0;
  }
  return (unsigned int)ii;
}
