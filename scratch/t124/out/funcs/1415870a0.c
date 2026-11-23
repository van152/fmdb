char __fastcall sub_1415870A0(__int64 a1, int a2, __int64 *a3)
{
  __int64 v6; // rdi
  __int64 v7; // r14
  __int64 v8; // rdx
  __int64 v9; // rcx
  __int64 v10; // r8
  __int64 v11; // r9
  __int64 v12; // r15
  int v13; // edi
  char v14; // al
  __int64 v15; // r8
  __int64 v16; // r9
  __int64 v17; // rcx
  __int64 v18; // rdx
  char v19; // di
  __int64 v20; // rax
  __int64 v21; // rcx
  __int64 v22; // rdx
  __int64 v23; // r8
  __int64 v24; // r9
  int v25; // edi
  __int64 v26; // rcx
  __int64 v27; // rdx
  __int64 v28; // r8
  __int64 v29; // r9
  int v30; // edi
  __int64 v31; // rcx
  __int64 v32; // rdx
  __int64 v33; // r8
  __int64 v34; // r9
  int v35; // edi
  __int64 v36; // rcx
  __int64 v37; // rdx
  __int64 v38; // r8
  __int64 v39; // r9
  int v40; // edi
  __int64 v41; // rcx
  __int64 v42; // rdx
  __int64 v43; // r8
  __int64 v44; // r9
  __int64 v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rdx
  __int64 v48; // rdi
  __int64 v49; // rbx
  unsigned __int64 v50; // rcx
  __int64 v51; // rbx
  __int64 v52; // rsi
  bool v53; // al
  int v54; // edi
  __int64 v55; // rcx
  __int64 v56; // rdx
  __int64 v57; // r8
  __int64 v58; // r9
  __int64 v59; // rcx
  int v60; // eax
  int v61; // ecx
  int v62; // edi
  __int64 v63; // rcx
  __int64 v64; // rdx
  __int64 v65; // r8
  __int64 v66; // r9
  _DWORD *v67; // rdi
  int v68; // ebx
  int v69; // edi
  int v70; // eax
  int v71; // ebx
  bool v72; // zf
  int v73; // eax
  __int64 v74; // rcx
  __int64 v75; // rax
  __int64 v76; // rcx
  __int64 v77; // rdx
  __int64 v78; // r8
  __int64 v79; // r9
  int v80; // edi
  __int64 v81; // rcx
  __int64 v82; // rdx
  __int64 v83; // r8
  __int64 v84; // r9
  __int64 v85; // rbx
  __int64 v86; // rdi
  __int64 v87; // rbx
  unsigned __int64 v88; // rcx
  __int64 v89; // rbx
  __int64 v90; // rsi
  bool v91; // al
  char v92; // bl
  __int64 v93; // rcx
  __int64 v94; // rdx
  __int64 v95; // r8
  __int64 v96; // r9
  int v97; // edi
  __int64 v98; // rcx
  __int64 v99; // rdx
  __int64 v100; // r8
  __int64 v101; // r9
  int v102; // edi
  __int64 v103; // rcx
  __int64 v104; // rdx
  __int64 v105; // r8
  __int64 v106; // r9
  char v107; // bl
  __int64 v108; // rcx
  __int64 v109; // rdx
  __int64 v110; // r8
  __int64 v111; // r9
  int v112; // edi
  __int64 v113; // rcx
  __int64 v114; // rdx
  __int64 v115; // r8
  __int64 v116; // r9
  unsigned __int64 v117; // rbx
  float v118; // xmm6_4
  __int64 v119; // rdx
  __int64 v120; // r8
  __int64 v121; // r9
  unsigned __int64 v122; // rcx
  unsigned __int64 v123; // rax
  float v124; // edi
  __int64 v125; // rax
  __int64 *v126; // rax
  __int64 v127; // rcx
  __int64 v128; // rdx
  __int64 v129; // r8
  __int64 v130; // r9
  __int64 v131; // rdx
  __int64 v132; // r8
  __int64 v133; // r9
  unsigned __int64 v134; // rcx
  unsigned __int64 v135; // rax
  float v136; // edi
  __int64 v137; // rax
  __int64 *v138; // rax
  __int64 v139; // rcx
  __int64 v140; // rdx
  __int64 v141; // r8
  __int64 v142; // r9
  __int64 v143; // rdx
  __int64 v144; // r8
  __int64 v145; // r9
  unsigned __int64 v146; // rcx
  unsigned __int64 v147; // rax
  int v148; // edi
  __int64 v149; // rax
  __int64 *v150; // rax
  __int64 v151; // rcx
  __int64 v152; // rdx
  __int64 v153; // r8
  __int64 v154; // r9
  __int64 v155; // rdx
  __int64 v156; // r8
  __int64 v157; // r9
  unsigned __int64 v158; // rcx
  unsigned __int64 v159; // rax
  float v160; // edi
  __int64 v161; // rax
  __int64 *v162; // rax
  __int64 v163; // rcx
  __int64 v164; // rdx
  __int64 v165; // r8
  __int64 v166; // r9
  unsigned __int64 v167; // rcx
  unsigned __int64 v168; // rax
  __int64 v169; // rcx
  __int64 v170; // rax
  __int64 v171; // rax
  __int64 v172; // rcx
  __int64 v173; // rdx
  __int64 v174; // r8
  __int64 v175; // r9
  unsigned __int64 v176; // rcx
  unsigned __int64 v177; // rax
  __int64 v178; // rcx
  __int64 v179; // rax
  __int64 v180; // rax
  __int64 v181; // rcx
  __int64 v182; // rdx
  __int64 v183; // r8
  __int64 v184; // r9
  __int64 v185; // rdx
  __int64 v186; // r8
  __int64 v187; // r9
  unsigned __int64 v188; // rcx
  unsigned __int64 v189; // rax
  float v190; // edi
  __int64 v191; // rax
  __int64 *v192; // rax
  __int64 v193; // rcx
  __int64 v194; // rdx
  __int64 v195; // r8
  __int64 v196; // r9
  __int64 v197; // rdx
  __int64 v198; // r8
  __int64 v199; // r9
  unsigned __int64 v200; // rcx
  unsigned __int64 v201; // rax
  float v202; // edi
  __int64 v203; // rax
  __int64 *v204; // rax
  __int64 v205; // rcx
  __int64 v206; // rdx
  __int64 v207; // r8
  __int64 v208; // r9
  unsigned __int64 v209; // rcx
  unsigned __int64 v210; // rax
  int v211; // edi
  __int64 *v212; // rax
  __int64 *v213; // rax
  __int64 v214; // rcx
  __int64 v215; // rdx
  __int64 v216; // r8
  __int64 v217; // r9
  __int64 v218; // rdx
  __int64 v219; // r8
  __int64 v220; // r9
  unsigned __int64 v221; // rcx
  unsigned __int64 v222; // rax
  float v223; // edi
  __int64 v224; // rax
  __int64 *v225; // rax
  __int64 v226; // rcx
  __int64 v227; // rdx
  __int64 v228; // r8
  __int64 v229; // r9
  __int64 v230; // rdx
  __int64 v231; // r8
  __int64 v232; // r9
  unsigned __int64 v233; // rcx
  unsigned __int64 v234; // rax
  float v235; // edi
  __int64 v236; // rax
  __int64 *v237; // rax
  __int64 v238; // rcx
  __int64 v239; // rdx
  __int64 v240; // r8
  __int64 v241; // r9
  __int64 v242; // rdx
  __int64 v243; // rdx
  int v244; // eax
  int v245; // edi
  _WORD *v246; // rax
  __int64 v247; // rcx
  __int64 v248; // rdx
  __int64 v249; // r8
  __int64 v250; // r9
  int v251; // edi
  __int64 v252; // rcx
  __int64 v253; // rdx
  __int64 v254; // r8
  __int64 v255; // r9
  int v256; // edi
  __int64 v257; // rcx
  __int64 v258; // rdx
  __int64 v259; // r8
  __int64 v260; // r9
  __int64 v262; // rcx
  __int64 v263; // rax
  __int64 v264; // rcx
  __int64 v265; // rdx
  __int64 v266; // r8
  __int64 v267; // r9
  __int64 v268; // rdi
  unsigned __int64 v269; // rcx
  __int64 v270; // rax
  __int64 v271; // rbx
  __int64 v272; // rsi
  bool v273; // al
  __int64 v274; // [rsp+20h] [rbp-60h] BYREF
  __int64 v275; // [rsp+28h] [rbp-58h]
  __int64 v276; // [rsp+30h] [rbp-50h] BYREF
  __int64 v277; // [rsp+38h] [rbp-48h]
  __int64 v278; // [rsp+40h] [rbp-40h]
  __int64 *v279; // [rsp+48h] [rbp-38h] BYREF
  float v280[4]; // [rsp+50h] [rbp-30h] BYREF
  __int128 v281; // [rsp+60h] [rbp-20h] BYREF
  __int64 v282; // [rsp+70h] [rbp-10h]
  __int64 v283; // [rsp+78h] [rbp-8h]

  v283 = -2;
  v6 = -*(_DWORD *)(a1 - 4);
  v7 = a1 + v6 - 312;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5F270 + 32LL))(a1: qword_141B5F270) == 0
    && (*(unsigned __int8 (__fastcall **)(__int64, __int64, _QWORD, __int64 *))(*(_QWORD *)qword_141B5F270 + 40LL))(
         a1: qword_141B5F270,
         a2: v7,
         a3: (unsigned int)a2,
         a4: a3) != 0 )
  {
    return 1;
  }
  v12 = v6 + a1;
  if ( a2 > 1332769888 )
  {
    if ( a2 <= 1347379808 )
    {
      if ( a2 <= 1332897135 )
      {
        if ( a2 == 1332769889 )
        {
          v256 = *(__int16 *)(v12 - 26);
          v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
          DWORD2(v281) = v256;
          *(_QWORD *)&v281 = v20;
          if ( &v281 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v257 = *((_QWORD *)&v281 + 1);
            *(_OWORD *)a3 = v281;
            v20 = sub_14083D4F0(a1: v257, a2: v258, a3: v259, a4: v260) + 8;
            v281 = (unsigned __int64)v20;
          }
          goto LABEL_175;
        }
        if ( a2 == 1332897126 )
        {
          v54 = *(char *)(v12 - 18);
          v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
          DWORD2(v281) = v54;
          *(_QWORD *)&v281 = v20;
          if ( &v281 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v55 = *((_QWORD *)&v281 + 1);
            *(_OWORD *)a3 = v281;
            v20 = sub_14083D4F0(a1: v55, a2: v56, a3: v57, a4: v58) + 8;
            v281 = (unsigned __int64)v20;
          }
          goto LABEL_175;
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1332897136:
            v97 = *(__int16 *)(v12 - 24);
            v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
            DWORD2(v281) = v97;
            *(_QWORD *)&v281 = v20;
            if ( &v281 != (__int128 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
              v98 = *((_QWORD *)&v281 + 1);
              *(_OWORD *)a3 = v281;
              v20 = sub_14083D4F0(a1: v98, a2: v99, a3: v100, a4: v101) + 8;
              v281 = (unsigned __int64)v20;
            }
            goto LABEL_175;
          case 1332901230:
            v102 = *(char *)(v12 - 17);
            v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
            DWORD2(v281) = v102;
            *(_QWORD *)&v281 = v20;
            if ( &v281 != (__int128 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
              v103 = *((_QWORD *)&v281 + 1);
              *(_OWORD *)a3 = v281;
              v20 = sub_14083D4F0(a1: v103, a2: v104, a3: v105, a4: v106) + 8;
              v281 = (unsigned __int64)v20;
            }
            goto LABEL_175;
          case 1333029744:
            v30 = *(char *)(v12 - 16);
            v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
            DWORD2(v281) = v30;
            *(_QWORD *)&v281 = v20;
            if ( &v281 != (__int128 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
              v31 = *((_QWORD *)&v281 + 1);
              *(_OWORD *)a3 = v281;
              v20 = sub_14083D4F0(a1: v31, a2: v32, a3: v33, a4: v34) + 8;
              v281 = (unsigned __int64)v20;
            }
            goto LABEL_175;
          default:
            break;
        }
      }
    }
    else if ( a2 > 1349545326 )
    {
      switch ( a2 )
      {
        case 1349545327:
          sub_1407C9510(a1: &v281);
          if ( *(_BYTE *)(v12 - 128) != 0 )
          {
            v117 = 0;
            v118 = MEMORY[0x141775530];
            do
            {
              sub_1407C9510(a1: &v276);
              v122 = v117 + *(unsigned __int8 *)(v12 - 40);
              v123 = v122 - 10;
              if ( v122 < 0xA )
                v123 = v117 + *(unsigned __int8 *)(v12 - 40);
              LODWORD(v124) = *(unsigned __int8 *)(*(_QWORD *)(v12 + 8 * v123 - 120) + 24LL);
              v125 = sub_14083D4F0(a1: v122, a2: v119, a3: v120, a4: v121) + 40;
              v280[0] = v124;
              v279 = (__int64 *)v125;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v126 = v279;
                v127 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v126;
                v125 = sub_14083D4F0(a1: v127, a2: v128, a3: v129, a4: v130) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v125;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v125 + 16LL))(a1: v125, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v134 = v117 + *(unsigned __int8 *)(v12 - 40);
              v135 = v134 - 10;
              if ( v134 < 0xA )
                v135 = v117 + *(unsigned __int8 *)(v12 - 40);
              LODWORD(v136) = *(unsigned __int8 *)(*(_QWORD *)(v12 + 8 * v135 - 120) + 25LL);
              v137 = sub_14083D4F0(a1: v134, a2: v131, a3: v132, a4: v133) + 40;
              v280[0] = v136;
              v279 = (__int64 *)v137;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v138 = v279;
                v139 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v138;
                v137 = sub_14083D4F0(a1: v139, a2: v140, a3: v141, a4: v142) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v137;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v137 + 16LL))(a1: v137, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v146 = v117 + *(unsigned __int8 *)(v12 - 40);
              v147 = v146 - 10;
              if ( v146 < 0xA )
                v147 = v117 + *(unsigned __int8 *)(v12 - 40);
              v148 = *(unsigned __int8 *)(*(_QWORD *)(v12 + 8 * v147 - 120) + 26LL);
              v149 = sub_14083D4F0(a1: v146, a2: v143, a3: v144, a4: v145) + 104;
              v280[0] = (float)v148 / v118;
              v279 = (__int64 *)v149;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v150 = v279;
                v151 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v150;
                v149 = sub_14083D4F0(a1: v151, a2: v152, a3: v153, a4: v154) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v149;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v149 + 16LL))(a1: v149, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v158 = v117 + *(unsigned __int8 *)(v12 - 40);
              v159 = v158 - 10;
              if ( v158 < 0xA )
                v159 = v117 + *(unsigned __int8 *)(v12 - 40);
              v160 = *(float *)(*(_QWORD *)(v12 + 8 * v159 - 120) + 16LL);
              v161 = sub_14083D4F0(a1: v158, a2: v155, a3: v156, a4: v157) + 40;
              v280[0] = v160;
              v279 = (__int64 *)v161;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v162 = v279;
                v163 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v162;
                v161 = sub_14083D4F0(a1: v163, a2: v164, a3: v165, a4: v166) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v161;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v161 + 16LL))(a1: v161, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v167 = v117 + *(unsigned __int8 *)(v12 - 40);
              v168 = v167 - 10;
              if ( v167 < 0xA )
                v168 = v117 + *(unsigned __int8 *)(v12 - 40);
              v169 = **(_QWORD **)(v12 + 8 * v168 - 120);
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v169 + 144LL))(a1: v169, a2: &v279);
              sub_140FEAD00(a1: &v279, a2: &v274);
              v170 = *a3;
              if ( &v274 != a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v170 + 16LL))(a1: *a3, a2: a3);
                v171 = v274;
                v172 = v275;
                a3[1] = v275;
                *a3 = v171;
                v170 = sub_14083D4F0(a1: v172, a2: v173, a3: v174, a4: v175) + 8;
                v275 = 0;
                v274 = v170;
              }
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v170 + 16LL))(a1: v170, a2: &v274);
              (*(void (__fastcall **)(_QWORD, float *))(**(_QWORD **)v280 + 16LL))(a1: *(_QWORD *)v280, a2: v280);
              sub_14083B2B0(a1: &v276, a2: a3);
              v176 = v117 + *(unsigned __int8 *)(v12 - 40);
              v177 = v176 - 10;
              if ( v176 < 0xA )
                v177 = v117 + *(unsigned __int8 *)(v12 - 40);
              v178 = *(_QWORD *)(*(_QWORD *)(v12 + 8 * v177 - 120) + 8LL);
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v178 + 144LL))(a1: v178, a2: &v279);
              sub_140FEAD00(a1: &v279, a2: &v274);
              v179 = *a3;
              if ( &v274 != a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v179 + 16LL))(a1: *a3, a2: a3);
                v180 = v274;
                v181 = v275;
                a3[1] = v275;
                *a3 = v180;
                v179 = sub_14083D4F0(a1: v181, a2: v182, a3: v183, a4: v184) + 8;
                v275 = 0;
                v274 = v179;
              }
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v179 + 16LL))(a1: v179, a2: &v274);
              (*(void (__fastcall **)(_QWORD, float *))(**(_QWORD **)v280 + 16LL))(a1: *(_QWORD *)v280, a2: v280);
              sub_14083B2B0(a1: &v276, a2: a3);
              v188 = v117 + *(unsigned __int8 *)(v12 - 40);
              v189 = v188 - 10;
              if ( v188 < 0xA )
                v189 = v117 + *(unsigned __int8 *)(v12 - 40);
              LODWORD(v190) = *(unsigned __int8 *)(*(_QWORD *)(v12 + 8 * v189 - 120) + 29LL);
              v191 = sub_14083D4F0(a1: v188, a2: v185, a3: v186, a4: v187) + 40;
              v280[0] = v190;
              v279 = (__int64 *)v191;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v192 = v279;
                v193 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v192;
                v191 = sub_14083D4F0(a1: v193, a2: v194, a3: v195, a4: v196) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v191;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v191 + 16LL))(a1: v191, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v200 = v117 + *(unsigned __int8 *)(v12 - 40);
              v201 = v200 - 10;
              if ( v200 < 0xA )
                v201 = v117 + *(unsigned __int8 *)(v12 - 40);
              LODWORD(v202) = *(unsigned __int8 *)(*(_QWORD *)(v12 + 8 * v201 - 120) + 30LL);
              v203 = sub_14083D4F0(a1: v200, a2: v197, a3: v198, a4: v199) + 40;
              v280[0] = v202;
              v279 = (__int64 *)v203;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v204 = v279;
                v205 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v204;
                v203 = sub_14083D4F0(a1: v205, a2: v206, a3: v207, a4: v208) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v203;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v203 + 16LL))(a1: v203, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v209 = v117 + *(unsigned __int8 *)(v12 - 40);
              v210 = v209 - 10;
              if ( v209 < 0xA )
                v210 = v117 + *(unsigned __int8 *)(v12 - 40);
              v211 = *(_DWORD *)(*(_QWORD *)(v12 + 8 * v210 - 120) + 20LL);
              if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                 + (unsigned int)TlsIndex)
                                               + 4LL) )
              {
                sub_141750E08(a1: &dword_141B5C8D0);
                if ( dword_141B5C8D0 == -1 )
                {
                  qword_141B5C8A0 = 0x141759DF8LL;
                  byte_141B5C8A8 = 32;
                  LOBYTE(v242) = 32;
                  sub_1412EA280(a1: &qword_141B5C8B0, a2: v242);
                  LOBYTE(v243) = 32;
                  sub_1412EB230(a1: &qword_141B5C8C0, a2: v243);
                  qword_141B5C8A0 = 0x141876208LL;
                  qword_141B5C8B0 = 0x1418762E8LL;
                  qword_141B5C8C0 = 0x141876308LL;
                  sub_141751048(a1: sub_140DBCA10);
                  sub_141750EA0(a1: &dword_141B5C8D0);
                }
              }
              LODWORD(v280[0]) = (v211 << 8) & 0x1FF00 | (((unsigned __int16)v211 >> 9) + 2 * (v211 & 0xFFFF0000));
              v212 = &qword_141B5C8A0;
              v279 = &qword_141B5C8A0;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v213 = v279;
                v214 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v213;
                v212 = (__int64 *)(sub_14083D4F0(a1: v214, a2: v215, a3: v216, a4: v217) + 8);
                *(_QWORD *)v280 = 0;
                v279 = v212;
              }
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v212 + 16))(a1: v212, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v221 = v117 + *(unsigned __int8 *)(v12 - 40);
              v222 = v221 - 10;
              if ( v221 < 0xA )
                v222 = v117 + *(unsigned __int8 *)(v12 - 40);
              LODWORD(v223) = *(unsigned __int8 *)(*(_QWORD *)(v12 + 8 * v222 - 120) + 27LL);
              v224 = sub_14083D4F0(a1: v221, a2: v218, a3: v219, a4: v220) + 40;
              v280[0] = v223;
              v279 = (__int64 *)v224;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v225 = v279;
                v226 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v225;
                v224 = sub_14083D4F0(a1: v226, a2: v227, a3: v228, a4: v229) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v224;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v224 + 16LL))(a1: v224, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              v233 = v117 + *(unsigned __int8 *)(v12 - 40);
              v234 = v233 - 10;
              if ( v233 < 0xA )
                v234 = v117 + *(unsigned __int8 *)(v12 - 40);
              LODWORD(v235) = *(unsigned __int8 *)(*(_QWORD *)(v12 + 8 * v234 - 120) + 28LL);
              v236 = sub_14083D4F0(a1: v233, a2: v230, a3: v231, a4: v232) + 40;
              v280[0] = v235;
              v279 = (__int64 *)v236;
              if ( &v279 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
                v237 = v279;
                v238 = *(_QWORD *)v280;
                a3[1] = *(_QWORD *)v280;
                *a3 = (__int64)v237;
                v236 = sub_14083D4F0(a1: v238, a2: v239, a3: v240, a4: v241) + 8;
                *(_QWORD *)v280 = 0;
                v279 = (__int64 *)v236;
              }
              (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v236 + 16LL))(a1: v236, a2: &v279);
              sub_14083B2B0(a1: &v276, a2: a3);
              sub_14083DB80(a1: &v279, a2: &v276);
              sub_140835380(a1: &v281, a2: (unsigned int)v117, a3: &v279);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v279 + 16))(a1: v279, a2: &v279);
              sub_14083B0A0(a1: &v276);
              ++v117;
            }
            while ( v117 < *(unsigned __int8 *)(v12 - 128) );
          }
          sub_14083DDA0(a1: &v276, a2: &v281);
          v262 = *a3;
          if ( &v276 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v262 + 16LL))(a1: v262, a2: a3);
            v263 = v276;
            v264 = v277;
            a3[1] = v277;
            *a3 = v263;
            v262 = sub_14083D4F0(a1: v264, a2: v265, a3: v266, a4: v267) + 8;
            v277 = 0;
            v276 = v262;
          }
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v262 + 16LL))(a1: v262, a2: &v276);
          sub_140833970(a1: &v281);
          return 1;
        case 1349677680:
          v244 = *(__int16 *)(v12 - 24);
          v245 = 0;
          if ( v244 <= 8999 )
          {
            v245 = 1;
            if ( (__int16)v244 <= 7999 )
            {
              v245 = 2;
              if ( (__int16)v244 <= 3249 )
              {
                v245 = 3;
                if ( (__int16)v244 <= 2749 )
                {
                  if ( (v246 = (_WORD *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v12 + 536LL))(a1: v12))[1] == 1900
                    && (_WORD)(v9 = *v246 & 0x1FF) == 1
                    || (v245 = 5, (char)sub_140B78960(a1: v246, a2: 0x1418761ECLL) <= 34) )
                  {
                    v245 = 4;
                  }
                }
              }
            }
          }
          v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
          DWORD2(v281) = v245;
          *(_QWORD *)&v281 = v20;
          if ( &v281 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v247 = *((_QWORD *)&v281 + 1);
            *(_OWORD *)a3 = v281;
            v20 = sub_14083D4F0(a1: v247, a2: v248, a3: v249, a4: v250) + 8;
            v281 = (unsigned __int64)v20;
          }
          goto LABEL_175;
        case 1349678435:
          goto LABEL_45;
        default:
          break;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1347379809:
          v67 = *(_DWORD **)(v12 - 200);
          if ( v67 != nullptr )
          {
            v277 = 0;
            v276 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 8;
            v68 = v67[2];
            v69 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v67 + 56LL))(a1: v67);
            (*(void (__fastcall **)(__int64, __int64 *, char *))(*(_QWORD *)v276 + 24LL))(
              a1: v276,
              a2: &v276,
              a3: (char *)&v281 + 8);
            v70 = v68 & v69;
            v71 = (v69 << 24) | v68 & 0x7FFFFF;
            v72 = v70 == -1;
            v73 = -8388609;
            if ( !v72 )
              v73 = v71;
            LODWORD(v281) = v73;
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v276 + 16LL))(a1: v276, a2: &v276);
            sub_140FEAD00(a1: &v281, a2: &v276);
            v74 = *a3;
            if ( &v276 != a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v74 + 16LL))(a1: v74, a2: a3);
              v75 = v276;
              v76 = v277;
              a3[1] = v277;
              *a3 = v75;
              v74 = sub_14083D4F0(a1: v76, a2: v77, a3: v78, a4: v79) + 8;
              v277 = 0;
              v276 = v74;
            }
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v74 + 16LL))(a1: v74, a2: &v276);
            (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v281 + 1) + 16LL))(
              a1: *((_QWORD *)&v281 + 1),
              a2: (char *)&v281 + 8);
          }
          return 1;
        case 1349478000:
          v80 = *(__int16 *)(v12 - 24);
          v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
          DWORD2(v281) = v80;
          *(_QWORD *)&v281 = v20;
          if ( &v281 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v81 = *((_QWORD *)&v281 + 1);
            *(_OWORD *)a3 = v281;
            v20 = sub_14083D4F0(a1: v81, a2: v82, a3: v83, a4: v84) + 8;
            v281 = (unsigned __int64)v20;
          }
          goto LABEL_175;
        case 1349478003:
          v13 = (int)(float)((float)((float)*(__int16 *)(v12 - 24) / MEMORY[0x141764AD0]) + MEMORY[0x1417597F0]);
          v14 = sub_1400870B0();
          v17 = v13 & 1;
          v18 = 0;
          if ( v14 != 0 )
            v18 = v13 & 1;
          LOBYTE(v18) = v13 + v18;
          v19 = 20;
          if ( (char)v18 < 20 )
            v19 = v18;
          v20 = sub_14083D4F0(a1: v17, a2: v18, a3: v15, a4: v16) + 40;
          DWORD2(v281) = v19;
          *(_QWORD *)&v281 = v20;
          if ( &v281 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v21 = *((_QWORD *)&v281 + 1);
            *(_OWORD *)a3 = v281;
            v20 = sub_14083D4F0(a1: v21, a2: v22, a3: v23, a4: v24) + 8;
            v281 = (unsigned __int64)v20;
          }
          goto LABEL_175;
        default:
          break;
      }
    }
    return sub_140DFD340(a1: v12 - 192, (unsigned int)a2, a3);
  }
  if ( a2 <= 1331917928 )
  {
    if ( a2 > 1331913073 )
    {
      if ( a2 != 1331913074 )
      {
        if ( a2 == 1331916399 )
        {
          v92 = *(_BYTE *)(v12 - 14);
          v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 24;
          BYTE8(v281) = v92;
          *(_QWORD *)&v281 = v20;
          if ( &v281 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v93 = *((_QWORD *)&v281 + 1);
            *(_OWORD *)a3 = v281;
            v20 = sub_14083D4F0(a1: v93, a2: v94, a3: v95, a4: v96) + 8;
            v281 = (unsigned __int64)v20;
          }
          goto LABEL_175;
        }
        if ( a2 == 1331917409 )
        {
          v25 = *(__int16 *)(v12 - 28);
          v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
          DWORD2(v281) = v25;
          *(_QWORD *)&v281 = v20;
          if ( &v281 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v26 = *((_QWORD *)&v281 + 1);
            *(_OWORD *)a3 = v281;
            v20 = sub_14083D4F0(a1: v26, a2: v27, a3: v28, a4: v29) + 8;
            v281 = (unsigned __int64)v20;
          }
          goto LABEL_175;
        }
        return sub_140DFD340(a1: v12 - 192, (unsigned int)a2, a3);
      }
      LOBYTE(v10) = 1;
      sub_1417354D0(a1: &v276, a2: v7, a3: v10);
      v85 = v277 - v276;
      v281 = 0;
      v282 = 0;
      v47 = v277 - v276;
      if ( v277 == v276 )
      {
LABEL_85:
        v279 = (__int64 *)&v281;
        sub_14158ADC0(a1: &v279, a2: a3);
        if ( (_QWORD)v281 != 0 )
        {
          v88 = v282 - v281;
          if ( v282 - (_QWORD)v281 == -1 )
            v88 = *(unsigned int *)(v281 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v89 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v89) >> 3 > v88)
            && (v90 = *(_QWORD *)(v89 + 8 * v88)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v90 + 32, a2: v281 - *(unsigned int *)(v90 + 120));
            v91 = *(_BYTE *)(v90 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v90 + 64)) != 0;
            if ( !v91 && *(_BYTE *)(v90 + 97) != 0 )
              sub_1412D33C0(a1: v90);
          }
          else
          {
            MEMORY[0x141948990](a1: v281 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v268 = v276;
        if ( v276 == 0 )
          return 1;
        v269 = v278 - v276;
        v270 = qword_141ABD470;
        if ( v278 - v276 == -1 )
          v269 = *(unsigned int *)(v276 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
        {
LABEL_191:
          v271 = *(_QWORD *)(v270 + 24);
          if ( (*(_QWORD *)(v270 + 32) - v271) >> 3 > v269 )
          {
            v272 = *(_QWORD *)(v271 + 8 * v269);
            if ( v272 != 0 )
            {
              MEMORY[0x1419475D8](a1: v272 + 32, a2: v268 - *(unsigned int *)(v272 + 120));
              v273 = *(_BYTE *)(v272 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v272 + 64)) != 0;
              if ( !v273 && *(_BYTE *)(v272 + 97) != 0 )
                sub_1412D33C0(a1: v272);
              return 1;
            }
          }
        }
LABEL_195:
        MEMORY[0x141948990](a1: v268 - *(unsigned int *)(v270 + 48));
        return 1;
      }
      if ( v277 - v276 >= 0 )
      {
        v86 = sub_1407E4490(a1: qword_141ABD470, a2: v47);
        *(_QWORD *)&v281 = v86;
        v282 = v86 + 8 * (v85 >> 3);
        v87 = v277 - v276;
        sub_141758A00(a1: v86, a2: v276, a3: v277 - v276);
        *((_QWORD *)&v281 + 1) = v86 + v87;
        goto LABEL_85;
      }
LABEL_211:
      sub_1400526C0(a1: v45, a2: v47);
    }
    if ( a2 == 1331784806 )
    {
      v251 = *(char *)(v12 - 22);
      v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
      DWORD2(v281) = v251;
      *(_QWORD *)&v281 = v20;
      if ( &v281 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
        v252 = *((_QWORD *)&v281 + 1);
        *(_OWORD *)a3 = v281;
        v20 = sub_14083D4F0(a1: v252, a2: v253, a3: v254, a4: v255) + 8;
        v281 = (unsigned __int64)v20;
      }
      goto LABEL_175;
    }
    if ( a2 != 1331913057 )
      return sub_140DFD340(a1: v12 - 192, (unsigned int)a2, a3);
    sub_1417354D0(a1: &v276, a2: v7, a3: 0);
    v46 = v277 - v276;
    v281 = 0;
    v282 = 0;
    v47 = v277 - v276;
    if ( v277 != v276 )
    {
      if ( v277 - v276 < 0 )
        goto LABEL_211;
      v48 = sub_1407E4490(a1: qword_141ABD470, a2: v47);
      *(_QWORD *)&v281 = v48;
      v282 = v48 + 8 * (v46 >> 3);
      v49 = v277 - v276;
      sub_141758A00(a1: v48, a2: v276, a3: v277 - v276);
      *((_QWORD *)&v281 + 1) = v48 + v49;
    }
    v279 = (__int64 *)&v281;
    sub_14158ADC0(a1: &v279, a2: a3);
    if ( (_QWORD)v281 != 0 )
    {
      v50 = v282 - v281;
      if ( v282 - (_QWORD)v281 == -1 )
        v50 = *(unsigned int *)(v281 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v51 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v51) >> 3 > v50)
        && (v52 = *(_QWORD *)(v51 + 8 * v50)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v52 + 32, a2: v281 - *(unsigned int *)(v52 + 120));
        v53 = *(_BYTE *)(v52 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v52 + 64)) != 0;
        if ( !v53 && *(_BYTE *)(v52 + 97) != 0 )
          sub_1412D33C0(a1: v52);
      }
      else
      {
        MEMORY[0x141948990](a1: v281 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    v268 = v276;
    if ( v276 == 0 )
      return 1;
    v269 = v278 - v276;
    v270 = qword_141ABD470;
    if ( v278 - v276 == -1 )
      v269 = *(unsigned int *)(v276 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
      goto LABEL_191;
    goto LABEL_195;
  }
  if ( a2 > 1332110958 )
  {
    switch ( a2 )
    {
      case 1332110959:
        v107 = *(_BYTE *)(v12 - 15);
        v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 24;
        BYTE8(v281) = v107;
        *(_QWORD *)&v281 = v20;
        if ( &v281 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v108 = *((_QWORD *)&v281 + 1);
          *(_OWORD *)a3 = v281;
          v20 = sub_14083D4F0(a1: v108, a2: v109, a3: v110, a4: v111) + 8;
          v281 = (unsigned __int64)v20;
        }
        goto LABEL_175;
      case 1332309357:
        v112 = *(char *)(v12 - 20);
        v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
        DWORD2(v281) = v112;
        *(_QWORD *)&v281 = v20;
        if ( &v281 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v113 = *((_QWORD *)&v281 + 1);
          *(_OWORD *)a3 = v281;
          v20 = sub_14083D4F0(a1: v113, a2: v114, a3: v115, a4: v116) + 8;
          v281 = (unsigned __int64)v20;
        }
        goto LABEL_175;
      case 1332769395:
        v35 = *(char *)(v12 - 19);
        v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
        DWORD2(v281) = v35;
        *(_QWORD *)&v281 = v20;
        if ( &v281 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v36 = *((_QWORD *)&v281 + 1);
          *(_OWORD *)a3 = v281;
          v20 = sub_14083D4F0(a1: v36, a2: v37, a3: v38, a4: v39) + 8;
          v281 = (unsigned __int64)v20;
        }
        goto LABEL_175;
      default:
        break;
    }
    return sub_140DFD340(a1: v12 - 192, (unsigned int)a2, a3);
  }
  if ( a2 == 1331917929 )
  {
    v59 = *(_QWORD *)(v12 - 200);
    if ( v59 != 0 )
    {
      v60 = *(_DWORD *)(v59 + 12);
      v61 = *(_DWORD *)(v59 + 16);
      if ( v61 == 0 )
        v61 = v60;
    }
    else
    {
      v60 = -1;
      v61 = -1;
    }
    *(_QWORD *)&v281 = __PAIR64__(v61, v60);
    sub_140FE72B0(a1: &v281, a2: 1667855481, a3);
    return 1;
  }
  if ( a2 == 1331980659 )
  {
    v62 = *(char *)(v12 - 21);
    v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
    DWORD2(v281) = v62;
    *(_QWORD *)&v281 = v20;
    if ( &v281 != (__int128 *)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
      v63 = *((_QWORD *)&v281 + 1);
      *(_OWORD *)a3 = v281;
      v20 = sub_14083D4F0(a1: v63, a2: v64, a3: v65, a4: v66) + 8;
      v281 = (unsigned __int64)v20;
    }
    goto LABEL_175;
  }
  if ( a2 != 1332106563 )
    return sub_140DFD340(a1: v12 - 192, (unsigned int)a2, a3);
LABEL_45:
  v40 = *(char *)(v12 - 13);
  v20 = sub_14083D4F0(a1: v9, a2: v8, a3: v10, a4: v11) + 40;
  DWORD2(v281) = v40;
  *(_QWORD *)&v281 = v20;
  if ( &v281 != (__int128 *)a3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
    v41 = *((_QWORD *)&v281 + 1);
    *(_OWORD *)a3 = v281;
    v20 = sub_14083D4F0(a1: v41, a2: v42, a3: v43, a4: v44) + 8;
    v281 = (unsigned __int64)v20;
  }
LABEL_175:
  (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v20 + 16LL))(a1: v20, a2: &v281);
  return 1;
}
