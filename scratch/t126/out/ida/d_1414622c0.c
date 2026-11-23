__m128d __fastcall sub_1414622C0(__int64 a1, unsigned int a2, int a3, int a4, _QWORD *a5)
{
  double v5; // xmm3_8
  _QWORD *v6; // r14
  __int128 v7; // xmm8
  double v8; // xmm9_8
  int v9; // ebx
  unsigned int v10; // esi
  int v11; // edi
  char v12; // al
  __int64 v13; // rdx
  __m128d v14; // xmm0
  __m128d v15; // xmm11
  int v16; // r8d
  int v17; // r9d
  __m128d v18; // xmm0
  __m128d v19; // xmm10
  int v20; // r8d
  int v21; // r9d
  int v22; // r8d
  int v23; // r9d
  __m128d v24; // xmm0
  __m128d v25; // xmm8
  bool v26; // zf
  int v27; // esi
  int v28; // r8d
  int v29; // r9d
  __m128d v30; // xmm0
  __m128d v31; // xmm6
  __int64 v32; // rax
  double v33; // xmm12_8
  double v34; // xmm13_8
  int v35; // eax
  __m128d v36; // xmm0
  __m128d v37; // xmm6
  int v38; // r8d
  int v39; // r9d
  int v40; // r8d
  int v41; // r9d
  __m128d v42; // xmm0
  __m128d v43; // xmm8
  int v44; // esi
  int v45; // r8d
  int v46; // r9d
  __m128d v47; // xmm0
  __m128d v48; // xmm7
  __int64 v49; // rax
  double v50; // xmm10_8
  double v51; // xmm0_8
  int v52; // eax
  unsigned __int8 **v53; // r15
  unsigned __int8 *v54; // rcx
  float v55; // xmm0_4
  __int64 v56; // rcx
  __int128 v57; // xmm6
  double v58; // xmm7_8
  int v59; // ebx
  double v60; // xmm0_8
  double v61; // xmm1_8
  double v62; // xmm1_8
  __int16 **v63; // rbx
  __int16 *v64; // rbx
  double v65; // xmm0_8
  __int16 **v66; // rbx
  __int64 v67; // rbx
  int v68; // edi
  __int16 *v69; // rdi
  __int16 v70; // bx
  __int16 v71; // bx
  __int64 v72; // rbx
  int v73; // edi
  __int16 **v74; // rbx
  __int16 **v75; // rbx
  __int16 **v76; // rbx
  __int64 v77; // rbx
  int v78; // edi
  __int16 **v79; // rbx
  __int16 **v80; // rbx
  __int64 v81; // rdi
  int v82; // ebx
  __int16 **v83; // rbx
  __int16 *v84; // rdi
  __int16 v85; // bx
  unsigned __int8 *v86; // rdi
  __int16 v87; // bx
  __int64 *v88; // rbx
  __int64 v89; // rbx
  __int16 **v90; // rbx
  double v91; // xmm1_8
  int v92; // ebx
  int v93; // edi
  int v94; // r8d
  int v95; // r9d
  __m128d v96; // xmm0
  __m128d v97; // xmm7
  __int64 v98; // rax
  int v99; // eax
  __m128d v100; // xmm0
  __int64 v101; // rax
  __int128 v102; // xmm1
  double v103; // xmm3_8
  int v104; // eax
  double v105; // xmm2_8
  char v106; // al
  double v107; // xmm4_8
  double v108; // xmm3_8
  double v109; // xmm6_8
  int v110; // r8d
  int v111; // r9d
  double v112; // xmm0_8
  __int64 v113; // xmm0_8^8
  double v114; // xmm6_8
  int v115; // r8d
  int v116; // r9d
  double v117; // xmm0_8
  __int64 v118; // xmm0_8^8
  int v119; // r8d
  int v120; // r9d
  char v121; // al
  __int128 v122; // xmm1
  double v123; // xmm0_8
  __m128d v124; // xmm0
  __int64 v125; // rax
  int v126; // eax
  double v127; // xmm2_8
  double v128; // xmm3_8
  double v130; // xmm7_8
  int v131; // edx
  int v132; // r9d
  int v133; // edx
  double v134; // xmm0_8
  __int128 v135; // xmm10
  _QWORD *v136; // rcx
  int v137; // edx
  int v138; // eax
  int v139; // eax
  double v140; // xmm6_8
  int v141; // ecx
  int v142; // edx
  double v143; // xmm6_8
  int v144; // edx
  int v145; // r9d
  int v146; // edx
  double v147; // xmm0_8
  double v148; // xmm7_8
  int v149; // edx
  int v150; // r9d
  int v151; // edx
  double v152; // xmm0_8
  double v153; // xmm7_8
  int v154; // edx
  int v155; // r9d
  int v156; // edx
  double v157; // xmm0_8
  double v158; // xmm6_8
  double v159; // xmm7_8
  int v160; // edx
  int v161; // r9d
  double v162; // xmm0_8
  __int64 v163; // rax
  double v164; // xmm0_8
  __int64 v165; // rax
  __int64 v166; // rax
  int v167; // ecx
  double v168; // xmm1_8
  double v169; // xmm2_8
  double v170; // xmm0_8
  __int64 v171; // rax
  int v172; // ecx
  double v173; // xmm2_8
  __int128 v174; // xmm3
  __int128 v175; // xmm1
  double v176; // xmm8_8
  __int64 v177; // rax
  __int16 v178; // cx
  int v179; // eax
  double v180; // xmm0_8
  double v181; // xmm1_8
  __int64 v182; // rcx
  __int128 v183; // xmm0
  double v184; // xmm1_8
  _QWORD *v185; // rax
  int v186; // ecx
  int v187; // eax
  int v188; // eax
  __int16 *v189; // rax
  __int64 v190; // rax
  __int64 v191; // rax
  __int64 v192; // rax
  __int64 v193; // rax
  __int64 v194; // rax
  __int64 v195; // rax
  __int64 v196; // rax
  __int64 v197; // rax
  __int64 v198; // rax
  __int64 v199; // rax
  double v200; // xmm0_8
  double v201; // xmm1_8
  __int64 v202; // rax
  double v203; // xmm2_8
  __int64 v204; // rax
  __int64 v205; // rax
  __int64 v206; // rax
  unsigned __int8 *v207; // rcx
  int v208; // eax
  __int64 v209; // rcx
  float v210; // xmm0_4
  __int64 v211; // rax
  __int64 v212; // rax
  __int64 v213; // rax
  __int64 v214; // rax
  __int64 v215; // rax
  int v216; // eax
  __int64 v217; // rax
  __int64 v218; // rax
  __int64 v219; // rax
  __int64 v220; // rax
  __int64 v221; // rcx
  _QWORD *v222; // rcx
  int v223; // eax
  int v224; // ecx
  __int64 v225; // rax
  __int64 v226; // rax
  __int64 v227; // rax
  __int64 v228; // rax
  unsigned __int8 *v229; // rax
  int v230; // ecx
  __int64 v231; // rax
  __int64 v232; // rax
  __int64 v233; // rax
  __int64 v234; // rax
  __int16 v235; // cx
  int v236; // eax
  __int16 *v237; // rdx
  int v238; // ecx
  __int64 v239; // rax
  __int16 v240; // ax
  __int64 v241; // rax
  double v242; // xmm0_8
  double v243; // xmm1_8
  __int64 v244; // rax
  __int64 v245; // rax
  unsigned __int8 *v246; // rcx
  int v247; // ecx
  __int64 v248; // rax
  __int16 v249; // cx
  __int64 v250; // rax
  __int64 v251; // rax
  __int64 v252; // rax
  __int64 v253; // rax
  __int64 v254; // rax
  __int64 v255; // rax
  __int64 v256; // rax
  __int64 v257; // rax
  __int64 v258; // rax
  __int64 v259; // rax
  __int64 v260; // rax
  __int64 v261; // rax
  __int64 v262; // rax
  __int64 v263; // rax
  __int64 v264; // rax
  __int64 v265; // rax
  int v266; // edx
  int v267; // r9d
  double v268; // xmm7_8
  double v269; // xmm0_8
  __int64 v270; // xmm0_8^8
  int v271; // edx
  int v272; // r9d
  double v273; // xmm0_8
  __int128 v274; // xmm2
  int v275; // edx
  int v276; // r9d
  double v277; // xmm0_8
  double v278; // xmm0_8
  __int64 v279; // rax
  double v280; // xmm1_8

  v6 = (_QWORD *)(a1 + 32);
  if ( a5 != nullptr )
    v6 = a5;
  v7 = MEMORY[0x14179AED0];
  if ( (unsigned __int8)a3 > 0xEu )
    return (__m128d)v7;
  v8 = v5;
  v9 = a3;
  v10 = a2;
  v11 = a1;
  if ( (_BYTE)a3 == 8 )
  {
    if ( (unsigned __int16)a2 <= 0x98u )
    {
      if ( (unsigned __int16)(a2 - 81) >= 0x37u
        || (v12 = 1, v13 = 0x6B47FF01000001LL, !_bittest64(&v13, (unsigned __int16)(v10 - 81))) )
      {
        v12 = sub_141464E90(v10);
      }
      if ( (_WORD)v10 == 18 || (unsigned __int16)v10 == 78 )
      {
        LOBYTE(a3) = 1;
        v14.m128d_f64[0] = sub_1414622C0(v11, v10, a3, a4, (__int64)v6);
        v15 = v14;
        LOBYTE(v16) = 2;
        v18.m128d_f64[0] = sub_1414622C0(v11, v10, v16, v17, (__int64)v6);
        v19 = v18;
        LOBYTE(v20) = 3;
        v24.m128d_f64[0] = sub_1414622C0(v11, v10, v20, v21, (__int64)v6);
        v25 = v24;
        v26 = (_WORD)v10 == 18;
        v27 = 60;
        if ( v26 )
          v27 = 73;
        LOBYTE(v22) = 1;
        v30.m128d_f64[0] = sub_1414622C0(v11, v27, v22, v23, (__int64)v6);
        v31 = v30;
        v32 = v6[1];
        v33 = 0.0;
        v34 = 0.0;
        if ( v32 != 0 )
        {
          v35 = *(unsigned __int8 *)(v32 + 13);
          if ( (_BYTE)v35 == 0xFF )
            v34 = MEMORY[0x14179AED0];
          else
            v34 = (double)v35;
        }
        LOBYTE(v28) = 2;
        v96.m128d_f64[0] = sub_1414622C0(v11, v27, v28, v29, (__int64)v6);
        v97 = v96;
        v98 = v6[2];
        if ( v98 != 0 )
        {
          v99 = *(unsigned __int8 *)(v98 + 13);
          if ( (_BYTE)v99 == 0xFF )
            v33 = MEMORY[0x14179AED0];
          else
            v33 = (double)v99;
        }
        v31.m128d_f64[0] = v31.m128d_f64[0] + v34;
        LOBYTE(v94) = 3;
        v100.m128d_f64[0] = sub_1414622C0(v11, v27, v94, v95, (__int64)v6);
        v101 = v6[3];
        v102 = 0;
        v103 = 0.0;
        if ( v101 != 0 )
        {
          v104 = *(unsigned __int8 *)(v101 + 13);
          if ( (_BYTE)v104 == 0xFF )
            v103 = MEMORY[0x14179AED0];
          else
            v103 = (double)v104;
        }
        v97.m128d_f64[0] = v97.m128d_f64[0] + v33;
        if ( (_mm_cvtsi128_si32((__m128i)_mm_and_pd(_mm_cmplt_pd((__m128d)0LL, v15), _mm_cmplt_pd((__m128d)0LL, v31)))
            & 1) != 0 )
        {
          v15.m128d_f64[0] = v15.m128d_f64[0] * v31.m128d_f64[0] + 0.0;
          v105 = v31.m128d_f64[0] + 0.0;
        }
        else
        {
          v105 = 0.0;
          v15 = 0;
        }
        v106 = _mm_cvtsi128_si32((__m128i)_mm_and_pd(_mm_cmplt_pd((__m128d)0LL, v19), _mm_cmplt_pd((__m128d)0LL, v97)));
        v107 = v97.m128d_f64[0];
        if ( (v106 & 1) == 0 )
          v107 = MEMORY[0x1417E9B90];
        v100.m128d_f64[0] = v100.m128d_f64[0] + v103;
        if ( (v106 & 1) != 0 )
          v15.m128d_f64[0] = v15.m128d_f64[0] + v19.m128d_f64[0] * v97.m128d_f64[0];
        v108 = v100.m128d_f64[0];
        if ( (_mm_cvtsi128_si32((__m128i)_mm_and_pd(_mm_cmplt_pd((__m128d)0LL, v100), _mm_cmplt_pd((__m128d)0LL, v25)))
            & 1) != 0 )
          v15.m128d_f64[0] = v15.m128d_f64[0] + v25.m128d_f64[0] * v100.m128d_f64[0];
        else
          v108 = MEMORY[0x1417E9B90];
        if ( v31.m128d_f64[0] + v97.m128d_f64[0] + v100.m128d_f64[0] != 0.0 )
        {
          v15.m128d_f64[0] = v15.m128d_f64[0] / (v105 + v107 + v108);
          return v15;
        }
        return (__m128d)v102;
      }
      if ( v12 != 0 )
      {
        v56 = 1;
        v57 = 0;
        v58 = 0.0;
        while ( 2 )
        {
          switch ( (__int16)v10 )
          {
            case 82:
              v67 = v6[v56];
              if ( v67 == 0 )
                goto LABEL_34;
              v68 = *(unsigned __int8 *)(v67 + 15);
              if ( (_BYTE)v68 == 0xFF )
                goto LABEL_51;
              goto LABEL_48;
            case 83:
              v67 = v6[v56];
              if ( v67 == 0 )
                goto LABEL_34;
              v68 = *(unsigned __int8 *)(v67 + 17);
              if ( (_BYTE)v68 == 0xFF )
                goto LABEL_51;
              goto LABEL_48;
            case 84:
              v67 = v6[v56];
              if ( v67 == 0 )
                goto LABEL_34;
              v68 = *(unsigned __int8 *)(v67 + 16);
              if ( (_BYTE)v68 == 0xFF )
                goto LABEL_51;
              goto LABEL_48;
            case 88:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 8LL);
              goto LABEL_202;
            case 89:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 10LL);
              goto LABEL_202;
            case 90:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 12LL);
              goto LABEL_202;
            case 91:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 14LL);
              goto LABEL_202;
            case 92:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 16LL);
              goto LABEL_202;
            case 93:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 18LL);
              goto LABEL_202;
            case 94:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 20LL);
              goto LABEL_202;
            case 95:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 26LL);
              goto LABEL_202;
            case 96:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 28LL);
              goto LABEL_202;
            case 103:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 54LL);
              goto LABEL_202;
            case 104:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 60LL);
              goto LABEL_202;
            case 106:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 64LL);
              goto LABEL_202;
            case 107:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 66LL);
              goto LABEL_202;
            case 108:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 68LL);
              goto LABEL_202;
            case 109:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 70LL);
              goto LABEL_202;
            case 110:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_212;
              v71 = *(_WORD *)(*(_QWORD *)v69 + 72LL);
              goto LABEL_213;
            case 111:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_212;
              v71 = *(_WORD *)(*(_QWORD *)v69 + 74LL);
              goto LABEL_213;
            case 112:
              v72 = v6[v56];
              v73 = 0;
              if ( v72 != 0 )
                v60 = MEMORY[0x14179AED0];
              else
                v60 = 0.0;
              if ( v72 != 0 )
                v73 = *(__int16 *)(v72 + 10);
              v61 = (double)v73;
              goto LABEL_36;
            case 113:
              v74 = (__int16 **)v6[v56];
              if ( v74 == nullptr )
                goto LABEL_207;
              v64 = *v74;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[13];
              LOWORD(v64) = v64[14];
              goto LABEL_209;
            case 114:
              v75 = (__int16 **)v6[v56];
              if ( v75 == nullptr )
                goto LABEL_207;
              v64 = *v75;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[4];
              LOWORD(v64) = v64[5];
              goto LABEL_209;
            case 115:
            case 129:
              v66 = (__int16 **)v6[v56];
              if ( v66 == nullptr )
                goto LABEL_207;
              v64 = *v66;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[6];
              LOWORD(v64) = v64[7];
              goto LABEL_209;
            case 116:
              v76 = (__int16 **)v6[v56];
              if ( v76 == nullptr )
                goto LABEL_207;
              v64 = *v76;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[8];
              LOWORD(v64) = v64[9];
              goto LABEL_209;
            case 118:
              v77 = v6[v56];
              if ( v77 == 0 )
                goto LABEL_207;
              v78 = *(unsigned __int8 *)(v77 + 18);
              if ( (_BYTE)v78 == 0xFF )
                v65 = MEMORY[0x14179AED0];
              else
                v65 = (double)v78;
              v93 = *(unsigned __int8 *)(v77 + 19);
              goto LABEL_234;
            case 119:
              v79 = (__int16 **)v6[v56];
              if ( v79 == nullptr )
                goto LABEL_207;
              v64 = *v79;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[25];
              LOWORD(v64) = v64[26];
              goto LABEL_209;
            case 120:
            case 122:
            case 123:
              v63 = (__int16 **)v6[v56];
              if ( v63 == nullptr )
                goto LABEL_207;
              v64 = *v63;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[42];
              LOWORD(v64) = v64[43];
              goto LABEL_209;
            case 121:
              v80 = (__int16 **)v6[v56];
              if ( v80 == nullptr )
                goto LABEL_207;
              v64 = *v80;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[13];
              LOWORD(v64) = v64[42];
              goto LABEL_209;
            case 124:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 52LL);
              goto LABEL_202;
            case 125:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 92LL);
              goto LABEL_202;
            case 126:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 96LL);
              goto LABEL_202;
            case 130:
              v81 = v6[v56];
              if ( v81 != 0 )
              {
                if ( *(_QWORD *)v81 != 0 )
                  LOWORD(v82) = *(_WORD *)(*(_QWORD *)v81 + 64LL);
                else
                  LOWORD(v82) = 0;
                v82 = (__int16)v82;
              }
              else
              {
                v82 = 0;
              }
              if ( v81 != 0 )
                v60 = MEMORY[0x14179AED0];
              else
                v60 = 0.0;
              v62 = (double)v82;
              goto LABEL_37;
            case 131:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 76LL);
              goto LABEL_202;
            case 132:
              v83 = (__int16 **)v6[v56];
              if ( v83 == nullptr )
                goto LABEL_207;
              v64 = *v83;
              if ( v64 == nullptr )
                goto LABEL_208;
              v65 = (double)v64[26] / MEMORY[0x1417A50C8];
              LOWORD(v64) = v64[32];
              goto LABEL_209;
            case 133:
              v84 = (__int16 *)v6[v56];
              if ( v84 != nullptr )
              {
                if ( *(_QWORD *)v84 != 0 )
                  v85 = *(_WORD *)(*(_QWORD *)v84 + 38LL);
                else
                  v85 = 0;
                v60 = (double)v85;
                v92 = v84[5];
              }
              else
              {
                v92 = 0;
                v60 = 0.0;
              }
              v62 = (double)v92 / MEMORY[0x1418B72B8];
              goto LABEL_37;
            case 134:
              v86 = (unsigned __int8 *)v6[v56];
              if ( v86 == nullptr )
                goto LABEL_207;
              if ( *(_QWORD *)v86 != 0 )
                v87 = *(_WORD *)(*(_QWORD *)v86 + 26LL);
              else
                v87 = 0;
              v65 = (double)v87;
              v93 = v86[15];
LABEL_234:
              LODWORD(v64) = -1;
              if ( v93 != 255 )
                LODWORD(v64) = v93;
              goto LABEL_210;
            case 135:
              v88 = (__int64 *)v6[v56];
              if ( v88 != nullptr )
              {
                v89 = *v88;
                if ( v89 != 0 )
                {
                  v65 = (double)*(__int16 *)(v89 + 26);
                  LOWORD(v89) = *(_WORD *)(v89 + 72);
                }
                else
                {
                  v65 = 0.0;
                  LOWORD(v89) = 0;
                }
                LODWORD(v89) = (__int16)v89;
              }
              else
              {
                LODWORD(v89) = 0;
                v65 = 0.0;
              }
              v91 = (double)(int)v89 / MEMORY[0x1417A50C8];
              goto LABEL_211;
            case 136:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 50LL);
              goto LABEL_202;
            case 137:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 22LL);
              goto LABEL_202;
            case 138:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 24LL);
              goto LABEL_202;
            case 139:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_212;
              v71 = *(_WORD *)(*(_QWORD *)v69 + 94LL);
              goto LABEL_213;
            case 140:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 100LL);
              goto LABEL_202;
            case 141:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 102LL);
              goto LABEL_202;
            case 142:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 104LL);
              goto LABEL_202;
            case 143:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 106LL);
              goto LABEL_202;
            case 144:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 114LL);
              goto LABEL_202;
            case 145:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 58LL);
              goto LABEL_202;
            case 146:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 56LL);
              goto LABEL_202;
            case 147:
              v67 = v6[v56];
              if ( v67 == 0 )
                goto LABEL_34;
              v68 = *(unsigned __int8 *)(v67 + 23);
              if ( (_BYTE)v68 == 0xFF )
              {
LABEL_51:
                v60 = MEMORY[0x14179AED0];
                v59 = *(__int16 *)(v67 + 10);
              }
              else
              {
LABEL_48:
                v60 = (double)v68;
                v59 = *(__int16 *)(v67 + 10);
              }
              goto LABEL_35;
            case 148:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 != 0 )
                v71 = *(_WORD *)(*(_QWORD *)v69 + 108LL);
              else
LABEL_212:
                v71 = 0;
LABEL_213:
              v60 = (double)v71 / MEMORY[0x1417A50C8];
              goto LABEL_203;
            case 149:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 112LL);
              goto LABEL_202;
            case 150:
              v69 = (__int16 *)v6[v56];
              if ( v69 == nullptr )
                goto LABEL_34;
              if ( *(_QWORD *)v69 == 0 )
                goto LABEL_201;
              v70 = *(_WORD *)(*(_QWORD *)v69 + 116LL);
              goto LABEL_202;
            case 151:
              v69 = (__int16 *)v6[v56];
              if ( v69 != nullptr )
              {
                if ( *(_QWORD *)v69 != 0 )
                  v70 = *(_WORD *)(*(_QWORD *)v69 + 118LL);
                else
LABEL_201:
                  v70 = 0;
LABEL_202:
                v60 = (double)v70;
LABEL_203:
                v59 = v69[5];
              }
              else
              {
LABEL_34:
                v59 = 0;
                v60 = 0.0;
              }
LABEL_35:
              v61 = (double)v59;
LABEL_36:
              v62 = v61 / MEMORY[0x1418B72A8];
LABEL_37:
              *(double *)&v57 = *(double *)&v57 + v60;
              v58 = v58 + v62;
LABEL_38:
              if ( ++v56 != 4 )
                continue;
              v7 = 0;
              if ( v58 > 0.0 )
              {
                v121 = sub_141464E90(v10);
                v122 = MEMORY[0x14175C310];
                v123 = MEMORY[0x14175C310];
                if ( v121 == 0 )
                  v123 = MEMORY[0x1417A50C8];
                *(double *)&v57 = *(double *)&v57 / v58;
                if ( (unsigned __int16)v10 == 132 )
                {
                  *(double *)&v122 = MEMORY[0x14175C310] - *(double *)&v57;
                  v57 = v122;
                }
                *(double *)&v57 = *(double *)&v57 * v123;
                v7 = v57;
              }
              break;
            case 152:
              v90 = (__int16 **)v6[v56];
              if ( v90 != nullptr )
              {
                v64 = *v90;
                if ( v64 != nullptr )
                {
                  v65 = (double)v64[56];
                  LOWORD(v64) = v64[57];
                }
                else
                {
LABEL_208:
                  v65 = 0.0;
                  LOWORD(v64) = 0;
                }
LABEL_209:
                LODWORD(v64) = (__int16)v64;
              }
              else
              {
LABEL_207:
                LODWORD(v64) = 0;
                v65 = 0.0;
              }
LABEL_210:
              v91 = (double)(int)v64;
LABEL_211:
              *(double *)&v57 = *(double *)&v57 + v91;
              v58 = v58 + v65;
              goto LABEL_38;
            default:
              goto LABEL_38;
          }
          break;
        }
      }
      else
      {
        LOBYTE(a3) = 1;
        v114 = sub_1414622C0(v11, v10, a3, a4, (__int64)v6);
        LOBYTE(v115) = 2;
        v117 = sub_1414622C0(v11, v10, v115, v116, (__int64)v6);
        *((_QWORD *)&v7 + 1) = v118;
        LOBYTE(v119) = 3;
        *(double *)&v7 = v117 + v114 + sub_1414622C0(v11, v10, v119, v120, (__int64)v6);
      }
    }
    return (__m128d)v7;
  }
  if ( (_BYTE)a3 != 12 )
  {
    if ( (unsigned __int16)a2 > 0x98u )
      return (__m128d)v7;
    v53 = (unsigned __int8 **)&v6[(unsigned __int8)a3];
    if ( (unsigned __int8)a3 <= 7u && (unsigned __int16)a2 < 0x4Bu )
    {
      v54 = *v53;
      if ( *v53 != nullptr )
      {
        if ( (_WORD)a2 == 23 )
        {
          if ( *(_QWORD *)v54 != 0 )
            v55 = (float)*(__int16 *)(*(_QWORD *)v54 + 46LL);
          else
            v55 = 0.0;
          v7 = 0;
          *(double *)&v7 = (float)(v55 / MEMORY[0x141775530]);
        }
        else
        {
          v139 = (__int16)sub_1414617A0(v54, a2);
LABEL_307:
          v7 = 0;
          *(double *)&v7 = (double)v139;
        }
        return (__m128d)v7;
      }
      return (__m128d)0LL;
    }
    while ( 2 )
    {
      if ( (unsigned __int8)v9 >= 8u )
      {
        if ( (_WORD)v10 != 80 )
        {
          v139 = 0;
          v140 = 0.0;
          v141 = 0;
LABEL_297:
          v142 = (unsigned __int16)v10 - 75;
          switch ( (__int16)v10 )
          {
            case 75:
              v7 = 0;
              v180 = 0.0;
              v181 = 0.0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v180 = 0.0;
                v181 = 0.0;
                if ( *v53 != nullptr )
                {
                  v182 = *(_QWORD *)*v53;
                  v180 = 0.0;
                  v181 = 0.0;
                  if ( v182 != 0 )
                  {
                    v181 = (double)*(__int16 *)(v182 + 6);
                    v180 = (double)*(__int16 *)(v182 + 4);
                  }
                }
              }
              if ( v139 > 0 )
              {
                v7 = 0;
                *(double *)&v7 = (double)v139 - v180 - v181;
              }
              return (__m128d)v7;
            case 76:
              goto LABEL_307;
            case 78:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v183 = 0;
                  *(double *)&v183 = (double)*((__int16 *)*v53 + 4);
                }
              }
              if ( v141 <= 0 )
                return (__m128d)v7;
              v184 = (double)v141;
              *(double *)&v183 = *(double *)&v183 / MEMORY[0x1417EC5F0];
              goto LABEL_418;
            case 79:
              LOWORD(v142) = 73;
              v143 = sub_1414622C0(v11, v142, v9, a4, (__int64)v6);
              LOWORD(v144) = 76;
              v147 = sub_1414622C0(v11, v144, v9, v145, (__int64)v6);
              LOWORD(v10) = 78;
              v135 = MEMORY[0x1417EC5F0];
              if ( MEMORY[0x1417EC5F0] <= v147 )
                continue;
              v268 = v147;
              if ( v143 == 0.0 || (unsigned __int8)sub_1400015E0() == 0 )
              {
                LOWORD(v146) = 78;
                v277 = sub_1414622C0(v11, v146, v9, a4, (__int64)v6) * v268 / *(double *)&v135;
                *((_QWORD *)&v7 + 1) = *((_QWORD *)&v135 + 1);
                *(double *)&v7 = *(double *)&v135 - v268;
                goto LABEL_670;
              }
              LOWORD(v146) = 18;
              v269 = sub_1414622C0(v11, v146, v9, a4, (__int64)v6);
              *((_QWORD *)&v7 + 1) = v270;
              *(double *)&v7 = v269 / MEMORY[0x1417A50C8];
              LOWORD(v271) = 78;
              v273 = sub_1414622C0(v11, v271, v9, v272, (__int64)v6);
              *((_QWORD *)&v274 + 1) = *((_QWORD *)&v135 + 1);
              *(double *)&v7 = *(double *)&v7 * (*(double *)&v135 - v268) / *(double *)&v135
                             + v273 * v268 / *(double *)&v135;
              if ( v143 + v268 < *(double *)&v135 )
              {
                *(double *)&v274 = (*(double *)&v135 - v268 - v143) * v8 / *(double *)&v135
                                 + (v143 + v268) * *(double *)&v7 / *(double *)&v135;
                return (__m128d)v274;
              }
              return (__m128d)v7;
            case 80:
              goto LABEL_310;
            case 81:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              v185 = *v53;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v186 = -1;
              if ( *((unsigned __int8 *)v185 + 15) != 255 )
                v186 = *((unsigned __int8 *)v185 + 15);
              v7 = 0;
              if ( v186 > 0 )
              {
                v7 = 0;
                *(double *)&v7 = (double)*((__int16 *)v185 + 5) / (double)v186;
              }
              return (__m128d)v7;
            case 82:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 > 7u )
                goto LABEL_642;
              v183 = 0;
              if ( *v53 == nullptr )
                goto LABEL_642;
              v187 = (*v53)[15];
              if ( (_BYTE)v187 != 0xFF )
                goto LABEL_360;
              goto LABEL_364;
            case 83:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 > 7u )
                goto LABEL_642;
              v183 = 0;
              if ( *v53 == nullptr )
                goto LABEL_642;
              v187 = (*v53)[17];
              if ( (_BYTE)v187 == 0xFF )
              {
LABEL_364:
                v183 = MEMORY[0x14179AED0];
              }
              else
              {
LABEL_360:
                v183 = 0;
                *(double *)&v183 = (double)v187;
              }
              goto LABEL_642;
            case 84:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 > 7u )
                goto LABEL_642;
              v183 = 0;
              if ( *v53 == nullptr )
                goto LABEL_642;
              v188 = (*v53)[16];
              if ( (_BYTE)v188 != 0xFF )
                goto LABEL_368;
              goto LABEL_622;
            case 85:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v189 = *(__int16 **)*v53;
                  v183 = 0;
                  if ( v189 != nullptr )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*v189;
                  }
                }
              }
              goto LABEL_642;
            case 86:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v190 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v190 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v190 + 2);
                  }
                }
              }
              goto LABEL_642;
            case 88:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v191 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v191 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v191 + 8);
                  }
                }
              }
              goto LABEL_642;
            case 89:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v192 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v192 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v192 + 10);
                  }
                }
              }
              goto LABEL_642;
            case 90:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v193 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v193 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v193 + 12);
                  }
                }
              }
              goto LABEL_642;
            case 91:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v194 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v194 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v194 + 14);
                  }
                }
              }
              goto LABEL_642;
            case 92:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v195 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v195 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v195 + 16);
                  }
                }
              }
              goto LABEL_642;
            case 93:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v196 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v196 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v196 + 18);
                  }
                }
              }
              goto LABEL_642;
            case 94:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v197 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v197 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v197 + 20);
                  }
                }
              }
              goto LABEL_642;
            case 95:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v198 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v198 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v198 + 26);
                  }
                }
              }
              goto LABEL_642;
            case 96:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v199 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v199 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v199 + 28);
                  }
                }
              }
              goto LABEL_642;
            case 97:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v183 = 0;
                  *(double *)&v183 = (double)*((__int16 *)*v53 + 5);
                }
              }
              if ( v139 <= 0 )
                return (__m128d)v7;
              v184 = (double)v139;
LABEL_418:
              *(double *)&v183 = *(double *)&v183 / v184;
              return (__m128d)v183;
            case 98:
              if ( v139 == 0 )
                return (__m128d)MEMORY[0x141764698];
              v200 = (double)v139;
              if ( v139 > 9 )
              {
                v7 = 0;
                if ( (unsigned __int8)v9 <= 7u && *v53 != nullptr )
                {
                  v279 = *(_QWORD *)*v53;
                  v280 = 0.0;
                  if ( v279 != 0 )
                  {
                    v7 = 0;
                    *(double *)&v7 = (double)*(__int16 *)(v279 + 4);
                    v280 = (double)*(__int16 *)(v279 + 6);
                  }
                }
                else
                {
                  v280 = 0.0;
                }
                *(double *)&v7 = (*(double *)&v7 * MEMORY[0x1417E28B8] + v200 - *(double *)&v7 - v280) / v200;
              }
              else
              {
                v201 = 0.0;
                if ( (unsigned __int8)v9 <= 7u && *v53 != nullptr )
                {
                  v202 = *(_QWORD *)*v53;
                  v203 = 0.0;
                  if ( v202 != 0 )
                  {
                    v201 = (double)*(__int16 *)(v202 + 4);
                    v203 = (double)*(__int16 *)(v202 + 6);
                  }
                }
                else
                {
                  v203 = 0.0;
                }
                v7 = MEMORY[0x1417EC5F0];
                *(double *)&v7 = ((MEMORY[0x1417EC5F0] - v200) * MEMORY[0x141764698]
                                + v201 * MEMORY[0x1417E28B8]
                                + v200
                                - v201
                                - v203)
                               / MEMORY[0x1417EC5F0];
              }
              return (__m128d)v7;
            case 99:
              LOWORD(v142) = 73;
              v130 = sub_1414622C0(v11, v142, v9, a4, (__int64)v6);
              LOWORD(v131) = 76;
              v134 = sub_1414622C0(v11, v131, v9, v132, (__int64)v6);
              LOWORD(v10) = 82;
              v135 = MEMORY[0x1417EC5F0];
              if ( MEMORY[0x1417EC5F0] <= v134 )
                continue;
              v158 = v134;
              if ( v130 != 0.0 && (unsigned __int8)sub_1400015E0() != 0 )
              {
                LOWORD(v133) = 15;
                v159 = sub_1414622C0(v11, v133, v9, a4, (__int64)v6) / MEMORY[0x1417A50C8];
                LOWORD(v266) = 82;
                v162 = sub_1414622C0(v11, v266, v9, v267, (__int64)v6);
                goto LABEL_663;
              }
              LOWORD(v133) = 82;
              v278 = sub_1414622C0(v11, v133, v9, a4, (__int64)v6);
              goto LABEL_669;
            case 100:
              LOWORD(v142) = 73;
              v148 = sub_1414622C0(v11, v142, v9, a4, (__int64)v6);
              LOWORD(v149) = 76;
              v152 = sub_1414622C0(v11, v149, v9, v150, (__int64)v6);
              LOWORD(v10) = 84;
              v135 = MEMORY[0x1417EC5F0];
              if ( MEMORY[0x1417EC5F0] <= v152 )
                continue;
              v158 = v152;
              if ( v148 != 0.0 && (unsigned __int8)sub_1400015E0() != 0 )
              {
                LOWORD(v151) = 16;
                v159 = sub_1414622C0(v11, v151, v9, a4, (__int64)v6) / MEMORY[0x1417A50C8];
                LOWORD(v275) = 84;
                v162 = sub_1414622C0(v11, v275, v9, v276, (__int64)v6);
                goto LABEL_663;
              }
              LOWORD(v151) = 84;
              v278 = sub_1414622C0(v11, v151, v9, a4, (__int64)v6);
              goto LABEL_669;
            case 101:
              LOWORD(v142) = 73;
              v153 = sub_1414622C0(v11, v142, v9, a4, (__int64)v6);
              LOWORD(v154) = 76;
              v157 = sub_1414622C0(v11, v154, v9, v155, (__int64)v6);
              LOWORD(v10) = 98;
              v135 = MEMORY[0x1417EC5F0];
              if ( MEMORY[0x1417EC5F0] <= v157 )
                continue;
              v158 = v157;
              if ( v153 == 0.0 || (unsigned __int8)sub_1400015E0() == 0 )
              {
                LOWORD(v156) = 98;
                v278 = sub_1414622C0(v11, v156, v9, a4, (__int64)v6);
LABEL_669:
                v277 = v278 * v158 / *(double *)&v135;
                *((_QWORD *)&v7 + 1) = *((_QWORD *)&v135 + 1);
                *(double *)&v7 = *(double *)&v135 - v158;
LABEL_670:
                *(double *)&v7 = *(double *)&v7 * v8;
              }
              else
              {
                LOWORD(v156) = 17;
                v159 = sub_1414622C0(v11, v156, v9, a4, (__int64)v6) / MEMORY[0x1417A50C8];
                LOWORD(v160) = 98;
                v162 = sub_1414622C0(v11, v160, v9, v161, (__int64)v6);
LABEL_663:
                v277 = v162 * v158 / *(double *)&v135;
                *((_QWORD *)&v7 + 1) = *((_QWORD *)&v135 + 1);
                *(double *)&v7 = (*(double *)&v135 - v158) * v159;
              }
              *(double *)&v7 = *(double *)&v7 / *(double *)&v135 + v277;
              break;
            case 102:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v204 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v204 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v204 + 62);
                  }
                }
              }
              goto LABEL_642;
            case 103:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v205 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v205 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v205 + 54);
                  }
                }
              }
              goto LABEL_642;
            case 104:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v206 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v206 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v206 + 60);
                  }
                }
              }
              goto LABEL_642;
            case 105:
              v207 = *v53;
              v7 = 0;
              if ( *v53 != nullptr )
              {
                v208 = *((__int16 *)v207 + 5);
                v209 = *(_QWORD *)v207;
                v210 = v209 != 0 ? (float)*(__int16 *)(v209 + 46) : 0.0;
                if ( (__int16)v208 >= 90 )
                {
                  v7 = 0;
                  *(double *)&v7 = (float)((float)((float)(v210 / MEMORY[0x141775530]) * MEMORY[0x14179E5F0])
                                         / (float)v208);
                }
              }
              return (__m128d)v7;
            case 106:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v211 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v211 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v211 + 64);
                  }
                }
              }
              goto LABEL_642;
            case 107:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v212 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v212 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v212 + 66);
                  }
                }
              }
              goto LABEL_642;
            case 108:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v213 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v213 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v213 + 68);
                  }
                }
              }
              goto LABEL_642;
            case 109:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v214 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v214 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v214 + 70);
                  }
                }
              }
              goto LABEL_642;
            case 110:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 > 7u )
                goto LABEL_628;
              v183 = 0;
              if ( *v53 == nullptr )
                goto LABEL_628;
              v215 = *(_QWORD *)*v53;
              v183 = 0;
              if ( v215 == 0 )
                goto LABEL_628;
              v216 = *(__int16 *)(v215 + 72);
              goto LABEL_627;
            case 111:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 > 7u )
                goto LABEL_628;
              v183 = 0;
              if ( *v53 == nullptr )
                goto LABEL_628;
              v217 = *(_QWORD *)*v53;
              v183 = 0;
              if ( v217 == 0 )
                goto LABEL_628;
              v216 = *(__int16 *)(v217 + 74);
              goto LABEL_627;
            case 112:
              LOWORD(v142) = 128;
              *(double *)&v183 = sub_1414622C0(v11, v142, v9, a4, 0);
              v7 = 0;
              if ( v140 <= 0.0 )
                return (__m128d)v7;
              goto LABEL_643;
            case 113:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v218 = *(_QWORD *)*v53;
              if ( v218 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v218 + 26);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v218 + 28);
              goto LABEL_650;
            case 114:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v219 = *(_QWORD *)*v53;
              if ( v219 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v219 + 8);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v219 + 10);
              goto LABEL_650;
            case 115:
            case 129:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v177 = *(_QWORD *)*v53;
              if ( v177 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v177 + 12);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v177 + 14);
              goto LABEL_650;
            case 116:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v220 = *(_QWORD *)*v53;
              if ( v220 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v220 + 16);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v220 + 18);
              goto LABEL_650;
            case 117:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v221 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v221 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v221 + 4);
                  }
                }
              }
              if ( v139 <= 0 )
                return (__m128d)v7;
              goto LABEL_521;
            case 118:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              v222 = *v53;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v223 = -1;
              if ( *((unsigned __int8 *)v222 + 18) != 255 )
                v223 = *((unsigned __int8 *)v222 + 18);
              v7 = 0;
              if ( v223 <= 0 )
                return (__m128d)v7;
              v224 = *((unsigned __int8 *)v222 + 19);
              if ( (_BYTE)v224 == 0xFF )
              {
                v7 = MEMORY[0x14179AED0];
              }
              else
              {
                v7 = 0;
                *(double *)&v7 = (double)v224;
              }
              goto LABEL_651;
            case 119:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v225 = *(_QWORD *)*v53;
              if ( v225 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v225 + 50);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v225 + 52);
              goto LABEL_650;
            case 120:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v226 = *(_QWORD *)*v53;
              if ( v226 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v226 + 84);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v226 + 88);
              goto LABEL_650;
            case 121:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v227 = *(_QWORD *)*v53;
              if ( v227 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v227 + 26);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v227 + 84);
              goto LABEL_650;
            case 122:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v228 = *(_QWORD *)*v53;
              if ( v228 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v228 + 84);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v228 + 86);
              goto LABEL_650;
            case 123:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              v229 = *v53;
              v7 = 0;
              if ( *v53 == nullptr )
                return (__m128d)v7;
              v7 = 0;
              v183 = 0;
              if ( *(_QWORD *)v229 != 0 )
              {
                v183 = 0;
                *(double *)&v183 = (double)*(__int16 *)(*(_QWORD *)v229 + 88LL);
              }
              v230 = v229[15];
              v139 = -1;
              if ( v230 != 255 )
                v139 = v230;
              if ( v139 <= 0 )
                return (__m128d)v7;
LABEL_521:
              *(double *)&v183 = *(double *)&v183 / (double)v139 * MEMORY[0x1417A50C8];
              return (__m128d)v183;
            case 124:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v231 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v231 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v231 + 52);
                  }
                }
              }
              goto LABEL_642;
            case 125:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v232 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v232 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v232 + 92);
                  }
                }
              }
              goto LABEL_642;
            case 126:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v233 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v233 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v233 + 96);
                  }
                }
              }
              goto LABEL_642;
            case 127:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v234 = *(_QWORD *)*v53;
              if ( v234 == 0 )
                return (__m128d)0LL;
              v235 = *(_WORD *)(v234 + 96);
              v7 = 0;
              if ( v235 > 0 )
              {
                v7 = 0;
                *(double *)&v7 = (double)*(__int16 *)(v234 + 98) / (double)v235;
              }
              return (__m128d)v7;
            case 128:
              v236 = 0;
              if ( (unsigned __int8)v9 <= 7u && *v53 != nullptr )
              {
                v237 = *(__int16 **)*v53;
                v238 = 0;
                if ( v237 != nullptr )
                {
                  v236 = v237[9] + v237[8];
                  v238 = v237[25];
                }
                v139 = v238 + v236;
              }
              else
              {
                v139 = 0;
              }
              goto LABEL_307;
            case 130:
              LOWORD(v142) = 128;
              *(double *)&v183 = sub_1414622C0(v11, v142, v9, a4, 0);
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v239 = *(_QWORD *)*v53;
              if ( v239 == 0 )
                return (__m128d)0LL;
              v240 = *(_WORD *)(v239 + 64);
              v7 = 0;
              if ( v240 == 0 )
                return (__m128d)v7;
              *(double *)&v183 = fmin(*(double *)&v183 * MEMORY[0x1417A50C8] / (double)v240, MEMORY[0x1417A50C8]);
              return (__m128d)v183;
            case 131:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v241 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v241 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v241 + 76);
                  }
                }
              }
              goto LABEL_642;
            case 132:
              LOWORD(v142) = 32;
              v242 = sub_1414622C0(v11, v142, v9, a4, 0);
              v7 = 0;
              v243 = 0.0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v243 = 0.0;
                if ( *v53 != nullptr )
                {
                  v244 = *(_QWORD *)*v53;
                  v243 = 0.0;
                  if ( v244 != 0 )
                    v243 = (double)*(__int16 *)(v244 + 52);
                }
              }
              if ( v242 != 0.0 )
              {
                v7 = MEMORY[0x14175C310];
                *(double *)&v7 = fmin(
                                   (MEMORY[0x14175C310] - v243 / MEMORY[0x1417A50C8] / v242) * MEMORY[0x1417A50C8],
                                   MEMORY[0x1417A50C8]);
              }
              return (__m128d)v7;
            case 133:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 > 7u )
                goto LABEL_628;
              v183 = 0;
              if ( *v53 == nullptr )
                goto LABEL_628;
              v245 = *(_QWORD *)*v53;
              v183 = 0;
              if ( v245 == 0 )
                goto LABEL_628;
              v216 = *(__int16 *)(v245 + 38);
              goto LABEL_627;
            case 134:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              v246 = *v53;
              if ( *v53 == nullptr || *(_QWORD *)v246 == 0 )
                return (__m128d)0LL;
              LOWORD(v223) = *(_WORD *)(*(_QWORD *)v246 + 26LL);
              v7 = 0;
              if ( (__int16)v223 <= 0 )
                return (__m128d)v7;
              v247 = v246[15];
              if ( (_BYTE)v247 == 0xFF )
              {
                v7 = MEMORY[0x14179AED0];
              }
              else
              {
                v7 = 0;
                *(double *)&v7 = (double)v247;
              }
              v223 = (__int16)v223;
              goto LABEL_651;
            case 135:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v248 = *(_QWORD *)*v53;
              if ( v248 == 0 )
                return (__m128d)0LL;
              v249 = *(_WORD *)(v248 + 26);
              v7 = 0;
              if ( v249 > 0 )
              {
                v7 = 0;
                *(double *)&v7 = (double)*(__int16 *)(v248 + 72) / MEMORY[0x1417A50C8] / (double)v249;
              }
              return (__m128d)v7;
            case 136:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v250 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v250 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v250 + 50);
                  }
                }
              }
              goto LABEL_642;
            case 137:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v251 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v251 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v251 + 22);
                  }
                }
              }
              goto LABEL_642;
            case 138:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v252 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v252 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v252 + 24);
                  }
                }
              }
              goto LABEL_642;
            case 139:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 > 7u )
                goto LABEL_628;
              v183 = 0;
              if ( *v53 == nullptr )
                goto LABEL_628;
              v253 = *(_QWORD *)*v53;
              v183 = 0;
              if ( v253 == 0 )
                goto LABEL_628;
              v216 = *(__int16 *)(v253 + 94);
              goto LABEL_627;
            case 140:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v254 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v254 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v254 + 100);
                  }
                }
              }
              goto LABEL_642;
            case 141:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v255 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v255 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v255 + 102);
                  }
                }
              }
              goto LABEL_642;
            case 142:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v256 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v256 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v256 + 104);
                  }
                }
              }
              goto LABEL_642;
            case 143:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v257 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v257 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v257 + 106);
                  }
                }
              }
              goto LABEL_642;
            case 144:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v258 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v258 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v258 + 114);
                  }
                }
              }
              goto LABEL_642;
            case 145:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v259 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v259 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v259 + 58);
                  }
                }
              }
              goto LABEL_642;
            case 146:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v260 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v260 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v260 + 56);
                  }
                }
              }
              goto LABEL_642;
            case 147:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 == nullptr )
                  goto LABEL_642;
                v188 = (*v53)[23];
                if ( (_BYTE)v188 == 0xFF )
                {
LABEL_622:
                  v183 = MEMORY[0x14179AED0];
                }
                else
                {
LABEL_368:
                  v183 = 0;
                  *(double *)&v183 = (double)v188;
                }
              }
LABEL_642:
              if ( v140 > *(double *)&v7 )
                goto LABEL_643;
              return (__m128d)v7;
            case 148:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 == nullptr )
                  goto LABEL_628;
                v261 = *(_QWORD *)*v53;
                v183 = 0;
                if ( v261 == 0 )
                  goto LABEL_628;
                v216 = *(__int16 *)(v261 + 108);
LABEL_627:
                v183 = 0;
                *(double *)&v183 = (double)v216;
              }
LABEL_628:
              if ( v140 > *(double *)&v7 )
              {
                *(double *)&v183 = *(double *)&v183 / MEMORY[0x1417A50C8];
LABEL_643:
                *(double *)&v183 = *(double *)&v183 / v140;
                return (__m128d)v183;
              }
              return (__m128d)v7;
            case 149:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v262 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v262 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v262 + 112);
                  }
                }
              }
              goto LABEL_642;
            case 150:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v263 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v263 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v263 + 116);
                  }
                }
              }
              goto LABEL_642;
            case 151:
              v7 = 0;
              v183 = 0;
              if ( (unsigned __int8)v9 <= 7u )
              {
                v183 = 0;
                if ( *v53 != nullptr )
                {
                  v264 = *(_QWORD *)*v53;
                  v183 = 0;
                  if ( v264 != 0 )
                  {
                    v183 = 0;
                    *(double *)&v183 = (double)*(__int16 *)(v264 + 118);
                  }
                }
              }
              goto LABEL_642;
            case 152:
              if ( (unsigned __int8)v9 > 7u )
                return (__m128d)0LL;
              if ( *v53 == nullptr )
                return (__m128d)0LL;
              v265 = *(_QWORD *)*v53;
              if ( v265 == 0 )
                return (__m128d)0LL;
              v178 = *(_WORD *)(v265 + 112);
              v7 = 0;
              if ( v178 <= 0 )
                return (__m128d)v7;
              v179 = *(__int16 *)(v265 + 114);
LABEL_650:
              v7 = 0;
              *(double *)&v7 = (double)v179;
              v223 = v178;
LABEL_651:
              *(double *)&v7 = *(double *)&v7 / (double)v223 * MEMORY[0x1417A50C8];
              return (__m128d)v7;
            default:
              return (__m128d)v7;
          }
          return (__m128d)v7;
        }
      }
      else
      {
        v136 = *v53;
        if ( *v53 == nullptr )
          return (__m128d)0LL;
        if ( (_WORD)v10 != 80 )
        {
          v137 = *((unsigned __int8 *)v136 + 12);
          if ( v137 == 255 )
            v137 = -1;
          v138 = *((unsigned __int8 *)v136 + 13);
          if ( v138 == 255 )
            v138 = -1;
          v139 = v137 + v138;
          v140 = (double)*((__int16 *)v136 + 5) / MEMORY[0x1418B72A8];
          v141 = *((unsigned __int8 *)v136 + 14);
          if ( v141 == 255 )
            v141 = -1;
          goto LABEL_297;
        }
      }
      break;
    }
LABEL_310:
    v163 = v6[1];
    if ( v163 != 0 )
    {
      v164 = (double)*(unsigned __int8 *)(v163 + 14);
      v7 = 0;
      *(double *)&v7 = (double)*(__int16 *)(v163 + 8) / MEMORY[0x1417EC5F0] + 0.0;
    }
    else
    {
      v7 = 0;
      v164 = 0.0;
    }
    v165 = v6[2];
    if ( v165 != 0 )
    {
      v164 = v164 + (double)*(unsigned __int8 *)(v165 + 14);
      *(double *)&v7 = *(double *)&v7 + (double)*(__int16 *)(v165 + 8) / MEMORY[0x1417EC5F0];
    }
    if ( MEMORY[0x141861B50] <= v164 )
      *(double *)&v7 = *(double *)&v7 / v164;
    else
      v7 = COERCE_UNSIGNED_INT64(((MEMORY[0x141861B50] - v164) * MEMORY[0x141861B40] + *(double *)&v7) / MEMORY[0x141861B50]);
    v166 = v6[3];
    if ( v166 != 0 )
    {
      v167 = *(unsigned __int8 *)(v166 + 14);
      v168 = (double)v167;
      v169 = (double)*(__int16 *)(v166 + 8) / MEMORY[0x1417EC5F0] + 0.0;
      if ( (unsigned __int8)v167 > 7u )
      {
        v170 = v169 / v168;
        goto LABEL_323;
      }
    }
    else
    {
      v168 = 0.0;
      v169 = 0.0;
    }
    v170 = ((MEMORY[0x1417E28B0] - v168) * MEMORY[0x1417E28B8] + v169) * MEMORY[0x1417EB5A0];
LABEL_323:
    v171 = v6[4];
    if ( v171 != 0 )
    {
      v172 = *(unsigned __int8 *)(v171 + 14);
      v173 = (double)v172;
      v174 = 0;
      *(double *)&v174 = (double)*(__int16 *)(v171 + 8) / MEMORY[0x1417EC5F0] + 0.0;
      if ( (unsigned __int8)v172 > 4u )
      {
        *(double *)&v174 = *(double *)&v174 / v173;
        v175 = v174;
        goto LABEL_328;
      }
    }
    else
    {
      v173 = 0.0;
      *(_QWORD *)&v174 = 0;
    }
    v175 = MEMORY[0x141861B40];
    *(double *)&v175 = (MEMORY[0x141861B40] - v173 + *(double *)&v174) / MEMORY[0x141861B40];
LABEL_328:
    switch ( (char)v9 )
    {
      case 9:
        v176 = *(double *)&v7 * MEMORY[0x1418B72B0] + v170 * MEMORY[0x14186AAD8];
        *(double *)&v175 = *(double *)&v175 * MEMORY[0x141764698];
        goto LABEL_337;
      case 10:
        v176 = *(double *)&v7 + *(double *)&v7 + v170 * MEMORY[0x141861B40];
        *(double *)&v175 = *(double *)&v175 * MEMORY[0x1417E28B8];
        goto LABEL_337;
      case 11:
        v176 = *(double *)&v7 + v170 * MEMORY[0x141774A20];
        *(double *)&v175 = *(double *)&v175 * MEMORY[0x141861B40];
LABEL_337:
        *(double *)&v175 = (*(double *)&v175 + v176) / MEMORY[0x1417EC5F0];
        v7 = v175;
        break;
      case 13:
        *(double *)&v7 = (*(double *)&v7 * MEMORY[0x1418623A0] + v170 * MEMORY[0x1417E28B8]) / MEMORY[0x1417EC5F0];
        break;
      case 14:
        return (__m128d)v7;
      default:
        *(double *)&v7 = (*(double *)&v7 + v170 + *(double *)&v175) / MEMORY[0x1417E28B8];
        break;
    }
    return (__m128d)v7;
  }
  if ( (unsigned __int16)a2 <= 0x98u )
  {
    if ( (_WORD)a2 == 18 || (unsigned __int16)a2 == 78 )
    {
      LOBYTE(a3) = 1;
      v36.m128d_f64[0] = sub_1414622C0(a1, a2, a3, a4, (__int64)v6);
      v37 = v36;
      LOBYTE(v38) = 2;
      v42.m128d_f64[0] = sub_1414622C0(v11, v10, v38, v39, (__int64)v6);
      v43 = v42;
      v26 = (_WORD)v10 == 18;
      v44 = 60;
      if ( v26 )
        v44 = 73;
      LOBYTE(v40) = 1;
      v47.m128d_f64[0] = sub_1414622C0(v11, v44, v40, v41, (__int64)v6);
      v48 = v47;
      v49 = v6[1];
      v50 = 0.0;
      v51 = 0.0;
      if ( v49 != 0 )
      {
        v52 = *(unsigned __int8 *)(v49 + 13);
        if ( (_BYTE)v52 == 0xFF )
          v51 = MEMORY[0x14179AED0];
        else
          v51 = (double)v52;
      }
      v48.m128d_f64[0] = v48.m128d_f64[0] + v51;
      LOBYTE(v45) = 2;
      v124.m128d_f64[0] = sub_1414622C0(v11, v44, v45, v46, (__int64)v6);
      v125 = v6[2];
      if ( v125 != 0 )
      {
        v126 = *(unsigned __int8 *)(v125 + 13);
        if ( (_BYTE)v126 == 0xFF )
          v50 = MEMORY[0x14179AED0];
        else
          v50 = (double)v126;
      }
      v124.m128d_f64[0] = v124.m128d_f64[0] + v50;
      v102 = 0;
      if ( (_mm_cvtsi128_si32((__m128i)_mm_and_pd(_mm_cmplt_pd((__m128d)0LL, v37), _mm_cmplt_pd((__m128d)0LL, v48))) & 1) != 0 )
      {
        v37.m128d_f64[0] = v37.m128d_f64[0] * v48.m128d_f64[0] + 0.0;
        v127 = v48.m128d_f64[0] + 0.0;
      }
      else
      {
        v127 = 0.0;
        v37 = 0;
      }
      v128 = v124.m128d_f64[0];
      if ( (_mm_cvtsi128_si32((__m128i)_mm_and_pd(_mm_cmplt_pd((__m128d)0LL, v124), _mm_cmplt_pd((__m128d)0LL, v43))) & 1) != 0 )
        v37.m128d_f64[0] = v37.m128d_f64[0] + v43.m128d_f64[0] * v124.m128d_f64[0];
      else
        v128 = MEMORY[0x1417E9B90];
      if ( v48.m128d_f64[0] + v124.m128d_f64[0] != 0.0 )
      {
        v37.m128d_f64[0] = v37.m128d_f64[0] / (v127 + v128);
        return v37;
      }
      return (__m128d)v102;
    }
    LOBYTE(a3) = 1;
    v109 = sub_1414622C0(a1, a2, a3, a4, (__int64)v6);
    LOBYTE(v110) = 2;
    v112 = sub_1414622C0(v11, v10, v110, v111, (__int64)v6);
    *((_QWORD *)&v7 + 1) = v113;
    *(double *)&v7 = v112 + v109;
  }
  return (__m128d)v7;
}
