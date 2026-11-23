__int64 __fastcall sub_140DD8520(__int64 a1, __int64 *a2, char a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
{
  __int16 *v8; // rsi
  char v9; // di
  __int64 v10; // r13
  char v11; // bl
  __int64 v12; // rax
  bool v13; // dl
  __int64 v14; // rdi
  __int64 v15; // rsi
  _DWORD *v16; // rsi
  __int64 *v17; // rbx
  __int64 *v18; // rax
  __int64 v19; // r8
  __int16 v20; // r14
  __int64 v21; // r15
  __int64 v22; // rbx
  __int64 v23; // rsi
  __int64 v24; // rdi
  unsigned __int64 v25; // rcx
  __int64 v26; // r8
  __int64 v27; // rcx
  __int64 v28; // r13
  __int64 v29; // rcx
  bool v30; // al
  __int64 v31; // rbx
  __int64 v32; // r8
  bool v33; // zf
  unsigned int *v34; // rbx
  __int64 v35; // rdi
  unsigned __int64 v36; // rax
  unsigned __int64 v37; // r15
  unsigned __int64 v38; // rsi
  unsigned __int64 v39; // rcx
  unsigned __int64 v40; // rsi
  __int64 v41; // r12
  __int64 v42; // rdx
  unsigned int *v43; // r13
  __int64 v44; // rdi
  unsigned __int64 v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rbx
  _DWORD *v48; // rax
  _DWORD *v49; // rsi
  __int64 v50; // rdi
  __int64 v51; // r8
  __int64 v52; // rax
  __int64 v53; // r8
  __int64 v54; // rdi
  unsigned __int64 i; // rbx
  __int64 *v56; // r14
  void (__fastcall ***v57)(_QWORD, __int64); // rcx
  __int64 v58; // r8
  __int64 v59; // rax
  __int64 v60; // rsi
  _QWORD *v61; // r14
  __int64 v62; // r8
  unsigned __int8 v63; // al
  __int64 v64; // r14
  __int64 v65; // r15
  __int64 v66; // rsi
  __int64 v67; // r13
  unsigned __int64 v68; // r12
  char *v69; // rax
  volatile signed __int32 **v70; // rbx
  unsigned __int64 v71; // rcx
  _QWORD *v72; // rcx
  unsigned __int64 v73; // rdx
  __int64 v74; // rcx
  __int64 v75; // r8
  unsigned __int64 v76; // rsi
  unsigned __int64 v77; // rdi
  __int64 v78; // rdx
  __int128 v79; // xmm2
  __int128 v80; // xmm2
  __int128 v81; // xmm1
  __int64 v82; // rsi
  volatile signed __int32 **v83; // rsi
  volatile signed __int32 *v84; // rdi
  __int64 v85; // rbx
  volatile signed __int32 *v86; // r14
  char *v87; // r15
  __int64 v88; // rsi
  __int64 v89; // r13
  unsigned __int64 v90; // r12
  unsigned __int64 v91; // rdx
  unsigned __int64 v92; // rax
  unsigned __int64 v93; // rdx
  unsigned __int64 v94; // rbx
  unsigned __int64 v95; // r13
  char *v96; // rax
  char *v97; // rcx
  unsigned __int64 v98; // rcx
  _QWORD *v99; // rcx
  unsigned __int64 v100; // rcx
  _QWORD *v101; // rcx
  __int64 v102; // rcx
  __int64 v103; // r8
  unsigned __int64 v104; // r9
  unsigned __int64 v105; // rsi
  __int64 v106; // rdx
  __int128 v107; // xmm1
  __int128 v108; // xmm1
  __int128 v109; // xmm1
  unsigned __int64 v110; // rax
  unsigned __int64 v111; // r10
  __int64 v112; // r10
  __int64 v113; // r8
  unsigned __int64 v114; // r9
  unsigned __int64 v115; // rsi
  __int64 v116; // rdx
  __int64 v117; // rdi
  __int128 v118; // xmm1
  __int128 v119; // xmm1
  __int128 v120; // xmm1
  _QWORD *v121; // rax
  __int64 v122; // rcx
  __int64 v123; // r8
  unsigned __int64 v124; // rsi
  unsigned __int64 v125; // rdi
  __int64 v126; // rdx
  __int128 v127; // xmm1
  __int128 v128; // xmm1
  __int128 v129; // xmm1
  char *v130; // rsi
  volatile signed __int32 *v131; // rdi
  __int64 v132; // r8
  unsigned __int8 v133; // al
  __int64 v134; // rbx
  __int64 v135; // r15
  __int64 v136; // rdi
  __int64 v137; // r12
  __int64 v138; // rsi
  unsigned __int64 v139; // rcx
  __int64 v140; // r8
  __int64 v141; // r14
  bool v142; // al
  unsigned __int64 j; // r15
  __int64 v144; // r14
  __int64 v145; // rbx
  __int16 *v146; // rdi
  __int64 v147; // r8
  __int64 *v148; // rdi
  __int64 v149; // rbx
  unsigned __int64 v150; // rax
  unsigned __int64 v151; // r12
  unsigned __int64 v152; // rcx
  unsigned __int64 v153; // r12
  __int64 v154; // rax
  __int64 v155; // r14
  __int64 *v156; // rsi
  __int64 v157; // rdi
  unsigned __int64 v158; // rcx
  __int64 v159; // rbx
  __int64 v160; // rsi
  __int64 v161; // r8
  __int64 v162; // rdx
  __int64 v163; // rcx
  __int64 *v164; // rsi
  __int64 v165; // r8
  __int64 v166; // rbx
  __int64 v167; // r14
  __int64 v168; // rdi
  __int64 v169; // r15
  __int64 v170; // rsi
  void *v171; // r14
  __int64 v172; // rdi
  __int64 v173; // rbx
  unsigned __int64 v174; // rax
  void *v175; // rax
  __int64 *v176; // r12
  __int64 *v177; // r14
  __int64 v178; // r15
  unsigned __int64 v179; // rax
  unsigned __int64 v180; // r13
  unsigned __int64 v181; // rcx
  unsigned __int64 v182; // r13
  __int64 v183; // rdi
  __int64 *v184; // rbx
  __int64 v185; // r8
  __int64 v186; // rax
  __int64 v187; // r8
  __int64 v188; // rsi
  __int64 v189; // rdi
  __int64 v190; // rcx
  unsigned __int64 v191; // rbx
  unsigned __int64 v192; // rdx
  unsigned __int64 v193; // rdi
  unsigned __int64 v194; // r15
  __int64 v195; // rcx
  __int64 v196; // rcx
  __int64 v197; // r12
  char *v198; // rax
  unsigned __int64 v199; // rsi
  __int64 v200; // rdi
  char *v201; // r14
  __int64 v202; // rdx
  __int16 v203; // ax
  __int64 v204; // rcx
  __int64 v205; // rsi
  __int64 v206; // rdi
  __int64 v207; // r8
  __int64 v208; // r14
  __int64 v209; // r8
  int v210; // edi
  void (__fastcall ***v211)(_QWORD, __int64); // rcx
  int v213; // [rsp+30h] [rbp-50h]
  __int64 v214; // [rsp+40h] [rbp-40h]
  __int64 *v215; // [rsp+48h] [rbp-38h]
  __int16 *v216; // [rsp+50h] [rbp-30h]
  __int64 *v217; // [rsp+58h] [rbp-28h]
  __int16 *v218; // [rsp+60h] [rbp-20h]
  __int16 *v220; // [rsp+70h] [rbp-10h]
  void (__fastcall ****v221)(_QWORD, __int64); // [rsp+78h] [rbp-8h]
  unsigned __int64 v222; // [rsp+78h] [rbp-8h]
  unsigned __int64 v223; // [rsp+78h] [rbp-8h]
  unsigned __int64 v224; // [rsp+80h] [rbp+0h]
  __int64 *v225; // [rsp+80h] [rbp+0h]
  __int64 v226; // [rsp+88h] [rbp+8h]
  __int16 v228; // [rsp+94h] [rbp+14h] BYREF
  char v229; // [rsp+96h] [rbp+16h] BYREF
  char v230; // [rsp+97h] [rbp+17h] BYREF
  unsigned int v231; // [rsp+98h] [rbp+18h] BYREF
  _BYTE v232[2]; // [rsp+9Ch] [rbp+1Ch] BYREF
  char v233; // [rsp+9Eh] [rbp+1Eh] BYREF
  unsigned __int8 v234; // [rsp+9Fh] [rbp+1Fh] BYREF
  _DWORD *v235; // [rsp+A0h] [rbp+20h] BYREF
  __int16 *v236; // [rsp+A8h] [rbp+28h]
  __int64 v237; // [rsp+B0h] [rbp+30h]
  __int64 *v238; // [rsp+B8h] [rbp+38h]
  unsigned __int8 v239; // [rsp+C7h] [rbp+47h] BYREF
  __int64 v240; // [rsp+C8h] [rbp+48h] BYREF

  v240 = -2;
  v9 = a3;
  v10 = a1;
  v11 = a7;
  v12 = *a2;
  v235 = (_DWORD *)v12;
  if ( v12 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v12 + 8));
  if ( a7 == 0 )
  {
LABEL_418:
    if ( v9 != 0 )
    {
      v238 = nullptr;
      v237 = 0;
      v236 = nullptr;
      LODWORD(v8) = 0;
      if ( (unsigned __int8)sub_140DFB5C0(a1: (int)v10 - 216, a2: (unsigned int)&v235, a3: 0, a4, a5, a6, a7: v11, a8) == 0 )
        goto LABEL_428;
      v210 = *(_DWORD *)(*(_QWORD *)(v10 - 328) + 4LL) + v10 - 336 + 8;
      if ( v237 != 0 && v235 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
      v238 = nullptr;
      v237 = 0;
      v236 = nullptr;
      LOBYTE(v213) = v11;
      LODWORD(v8) = 0;
      if ( (unsigned __int8)sub_141084540(a1: v210, a2: (unsigned int)&v235, a3: 0, a4, a5, a6, a7: v213, a8) == 0 )
        goto LABEL_428;
      if ( v237 != 0 && v235 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
    }
    v238 = nullptr;
    v237 = 0;
    v236 = nullptr;
    LOBYTE(v8) = v235[4] == 0;
    goto LABEL_428;
  }
  v236 = (__int16 *)(a1 - 22);
  v237 = 2;
  v238 = (__int64 *)(a1 - 20);
  v13 = HIBYTE(qword_141B6034C) != 0 && byte_141B5FC2C == 0;
  v14 = 4LL * v13 + 4;
  v15 = 4LL * v13 - 60;
  if ( v235 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: a1 - 22, a3: 2);
  v236 = (__int16 *)(v10 - 64);
  v237 = v14;
  v238 = (__int64 *)(v10 + v15);
  v16 = v235;
  v215 = (__int64 *)(v10 - 22);
  if ( v235 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v10 - 64, a3: v14);
    v236 = (__int16 *)(v10 - 20);
    v237 = 1;
    v238 = (__int64 *)(v10 - 19);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v10 - 20, a3: 1);
    v236 = (__int16 *)(v10 - 18);
    v237 = 1;
    v238 = (__int64 *)(v10 - 17);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v10 - 18, a3: 1);
    v236 = (__int16 *)(v10 - 19);
    v237 = 1;
    v238 = (__int64 *)(v10 - 18);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v10 - 19, a3: 1);
    v236 = (__int16 *)(v10 - 17);
    v237 = 1;
    v218 = (__int16 *)(v10 - 16);
    v238 = (__int64 *)(v10 - 16);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v10 - 17, a3: 1);
    v236 = (__int16 *)(v10 - 48);
    v237 = 8;
    v216 = (__int16 *)(v10 - 40);
    v238 = (__int64 *)(v10 - 40);
    v17 = (__int64 *)(v10 - 15);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v10 - 48, a3: 8);
    v236 = (__int16 *)(v10 - 15);
    v237 = 1;
    v238 = (__int64 *)(v10 - 14);
    v220 = (__int16 *)(v10 - 14);
    if ( (char *)(v10 - 14) == &v233 )
    {
      v237 = 2;
      v238 = (__int64 *)&v234;
      v217 = (__int64 *)(v10 - 15);
      goto LABEL_15;
    }
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v10 - 15, a3: 1);
    v16 = v235;
    goto LABEL_11;
  }
  v218 = (__int16 *)(v10 - 16);
  v216 = (__int16 *)(v10 - 40);
  v17 = (__int64 *)(v10 - 15);
  v236 = (__int16 *)(v10 - 15);
  v220 = (__int16 *)(v10 - 14);
  if ( (char *)(v10 - 14) != &v233 )
  {
    v16 = nullptr;
LABEL_11:
    v18 = (__int64 *)&v233;
    v236 = (__int16 *)&v233;
    v19 = 1;
    goto LABEL_12;
  }
  v19 = 2;
  v18 = (__int64 *)(v10 - 15);
LABEL_12:
  v217 = v17;
  v237 = v19;
  v238 = (__int64 *)&v234;
  v17 = v18;
  if ( v16 != nullptr )
LABEL_15:
    (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v16 + 40LL))(a1: v16, a2: v17);
  v238 = nullptr;
  v237 = 0;
  v236 = nullptr;
  v20 = v233 + 256;
  if ( v233 >= 0 )
    v20 = v233;
  v21 = *(_QWORD *)(v10 - 224);
  v226 = v10;
  if ( (*(_QWORD *)(v10 - 208) - v21) >> 2 >= (unsigned __int64)v20 )
  {
    v23 = *(_QWORD *)(v10 - 224);
    goto LABEL_33;
  }
  if ( v20 < 0 )
    ((void (__noreturn *)(void))sub_1400526C0)();
  v22 = *(_QWORD *)(v10 - 216);
  v23 = sub_1407E4490(a1: qword_141ABD470, a2: 4LL * v20);
  sub_141758A00(a1: v23, a2: *(_QWORD *)(v10 - 224), a3: *(_QWORD *)(v10 - 216) - *(_QWORD *)(v10 - 224));
  v24 = *(_QWORD *)(v10 - 224);
  if ( v24 != 0 )
  {
    v25 = *(_QWORD *)(v10 - 208) - v24;
    if ( v25 == -1 )
    {
      v25 = *(unsigned int *)(v24 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_31:
        MEMORY[0x141948990](a1: v24 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_32;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_31;
    }
    v26 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > v25 )
    {
      v27 = *(_QWORD *)(v26 + 8 * v25);
      if ( v27 != 0 )
      {
        v28 = v27;
        MEMORY[0x1419475D8](a1: v27 + 32, a2: v24 - *(unsigned int *)(v27 + 120));
        v29 = v28;
        v30 = *(_BYTE *)(v28 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v28 + 64)) != 0;
        v10 = v226;
        if ( !v30 && *(_BYTE *)(v29 + 97) != 0 )
          sub_1412D33C0(a1: v29);
        goto LABEL_32;
      }
    }
    goto LABEL_31;
  }
LABEL_32:
  *(_QWORD *)(v10 - 224) = v23;
  *(_QWORD *)(v10 - 216) = v23 + v22 - v21;
  *(_QWORD *)(v10 - 208) = v23 + 4LL * v20;
LABEL_33:
  if ( v20 > 0 )
  {
    while ( v238 == (__int64 *)&v231 )
    {
      v33 = v237 == -4;
      v32 = v237 + 4;
      v237 += 4;
      v238 = (__int64 *)v232;
      if ( !v33 )
        goto LABEL_42;
LABEL_44:
      v238 = nullptr;
      v237 = 0;
      v236 = nullptr;
      v34 = *(unsigned int **)(v10 - 216);
      if ( v34 == *(unsigned int **)(v10 - 208) )
      {
        v35 = (__int64)v34 - *(_QWORD *)(v10 - 224);
        v36 = v35 >> 2;
        v37 = (v35 >> 2) + 1;
        v38 = (unsigned __int64)(v35 >> 2) >> 1;
        v39 = 0x3FFFFFFFFFFFFFFFLL - v38;
        v40 = (v35 >> 2) + v38;
        if ( v40 <= v37 )
          v40 = v36 + 1;
        if ( v36 > v39 )
          v40 = 0x3FFFFFFFFFFFFFFFLL;
        v41 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v40);
        *(_DWORD *)(v41 + v35) = v231;
        v42 = *(_QWORD *)(v10 - 224);
        v43 = *(unsigned int **)(v226 - 216);
        sub_141758A00(a1: v41, a2: v42, a3: (char *)v34 - v42);
        v33 = v43 == v34;
        v10 = v226;
        if ( !v33 )
          sub_141758A00(a1: v41 + v35 + 4, a2: v34, a3: *(_QWORD *)(v226 - 216) - (_QWORD)v34);
        v44 = *(_QWORD *)(v226 - 224);
        if ( v44 == 0 )
          goto LABEL_62;
        v45 = *(_QWORD *)(v226 - 208) - v44;
        if ( v45 == -1 )
        {
          v45 = *(unsigned int *)(v44 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_61;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_61;
        }
        v46 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v46) >> 3 > v45 )
        {
          v47 = *(_QWORD *)(v46 + 8 * v45);
          if ( v47 != 0 )
          {
            MEMORY[0x1419475D8](a1: v47 + 32, a2: v44 - *(unsigned int *)(v47 + 120));
            if ( (*(_BYTE *)(v47 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v47 + 64)) == 0)
              && *(_BYTE *)(v47 + 97) != 0 )
            {
              sub_1412D33C0(a1: v47);
            }
            goto LABEL_62;
          }
        }
LABEL_61:
        MEMORY[0x141948990](a1: v44 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_62:
        *(_QWORD *)(v226 - 224) = v41;
        v31 = v41 + 4 * v37;
        *(_QWORD *)(v226 - 216) = v31;
        *(_QWORD *)(v226 - 208) = v41 + 4 * v40;
        if ( --v20 == 0 )
        {
LABEL_66:
          v23 = *(_QWORD *)(v10 - 224);
          goto LABEL_68;
        }
      }
      else
      {
        *v34 = v231;
        v31 = *(_QWORD *)(v10 - 216) + 4LL;
        *(_QWORD *)(v10 - 216) = v31;
        if ( --v20 == 0 )
          goto LABEL_66;
      }
    }
    if ( v237 != 0 && v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v237);
    v236 = (__int16 *)&v231;
    v237 = 4;
    v238 = (__int64 *)v232;
    v32 = 4;
LABEL_42:
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v32);
    goto LABEL_44;
  }
  v31 = *(_QWORD *)(v10 - 216);
LABEL_68:
  v48 = (_DWORD *)sub_141751AC0(a1: v23, a2: v31, a3: 0xFFFFFFFFLL);
  v49 = v48;
  if ( v48 != (_DWORD *)v31 )
  {
    while ( ++v48 != (_DWORD *)v31 )
    {
      if ( *v48 != -1 )
        *v49++ = *v48;
    }
  }
  if ( v49 != (_DWORD *)v31 )
  {
    v50 = *(_QWORD *)(v10 - 216) - v31;
    sub_141758A00(a1: v49, a2: v31, a3: v50);
    *(_QWORD *)(v10 - 216) = (char *)v49 + v50;
  }
  v51 = v237;
  if ( v238 != (__int64 *)(v10 - 104) )
  {
    if ( v237 != 0 && v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v237);
    v236 = (__int16 *)(v10 - 104);
    v237 = 4;
    v238 = (__int64 *)(v10 - 100);
    v52 = 4;
    if ( (unsigned __int8 *)(v10 - 100) == &v239 )
    {
      v53 = 5;
LABEL_85:
      v237 = v53;
      v238 = &v240;
      goto LABEL_86;
    }
    goto LABEL_82;
  }
  v52 = v237 + 4;
  v237 += 4;
  v238 = (__int64 *)(v10 - 100);
  if ( (unsigned __int8 *)(v10 - 100) != &v239 )
  {
    if ( v51 == -4 )
    {
LABEL_84:
      v236 = (__int16 *)&v239;
      v53 = 1;
      goto LABEL_85;
    }
LABEL_82:
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v52);
    goto LABEL_84;
  }
  v237 = v51 + 5;
  v238 = &v240;
  if ( v51 != -5 )
  {
LABEL_86:
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
  }
  v238 = nullptr;
  v237 = 0;
  v236 = nullptr;
  if ( v239 == 0 )
  {
LABEL_117:
    if ( v237 != 0 && v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
    v236 = (__int16 *)&v239;
    v237 = 1;
    v238 = &v240;
    v62 = 1;
LABEL_121:
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v62);
    goto LABEL_123;
  }
  v221 = (void (__fastcall ****)(_QWORD, __int64))(v10 - 176);
  v54 = 0x1FFFFFFFFFFFFFFFLL;
  for ( i = 0; i < v239; ++i )
  {
    if ( v238 == (__int64 *)&v231 )
    {
      v58 = v237 + 1;
      v237 = v58;
      v238 = (__int64 *)((char *)&v231 + 1);
      if ( v58 == 0 )
        goto LABEL_102;
    }
    else
    {
      if ( v237 != 0 && v235 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v237);
      v236 = (__int16 *)&v231;
      v237 = 1;
      v238 = (__int64 *)((char *)&v231 + 1);
      v58 = 1;
    }
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v58);
LABEL_102:
    v238 = nullptr;
    v237 = 0;
    v236 = nullptr;
    if ( (_BYTE)v231 != 0xFF )
    {
      v59 = sub_140EE7C20();
      if ( v59 != 0 )
      {
        v60 = v59;
        if ( v237 != 0 && v235 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
        v238 = nullptr;
        v237 = 0;
        v236 = nullptr;
        if ( (*(unsigned __int8 (__fastcall **)(__int64, _DWORD **))(*(_QWORD *)v60 + 32LL))(a1: v60, a2: &v235) == 0 )
        {
LABEL_361:
          LODWORD(v8) = 0;
          goto LABEL_428;
        }
        if ( i != 0 )
        {
          v61 = *(_QWORD **)(v226 - 168);
          if ( v61 == nullptr )
          {
            if ( dword_141B5CD28 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(a1: &dword_141B5CD28);
              if ( dword_141B5CD28 == -1 )
              {
                sub_1407E53D0(
                  a1: (unsigned int)&unk_141B5CCD8,
                  a2: 1100129282,
                  a3: 64,
                  a4: 32,
                  a5: 0,
                  a6: 0,
                  a7: 64,
                  a8: 4096);
                sub_141751048(a1: sub_140DF2D30);
                sub_141750EA0(a1: &dword_141B5CD28);
              }
            }
            v61 = (_QWORD *)sub_1407E58C0(a1: &unk_141B5CCD8, a2: 32);
            *v61 = 0;
            v61[1] = 0;
            v61[2] = 0;
            v61[3] = 0;
            *(_QWORD *)(v226 - 168) = v61;
          }
          v57 = (void (__fastcall ***)(_QWORD, __int64))v61[v54];
          v56 = &v61[v54];
          if ( v57 == nullptr )
            goto LABEL_92;
LABEL_91:
          (**v57)(a1: v57, a2: 1);
        }
        else
        {
          v56 = (__int64 *)(v10 - 176);
          v57 = *v221;
          if ( *v221 != nullptr )
            goto LABEL_91;
        }
LABEL_92:
        *v56 = v60;
      }
    }
    ++v54;
  }
  v10 = v226;
  if ( v238 != (__int64 *)&v239 )
    goto LABEL_117;
  v62 = v237 + 1;
  v33 = v237++ == -1;
  v238 = &v240;
  if ( !v33 )
    goto LABEL_121;
LABEL_123:
  v238 = nullptr;
  v237 = 0;
  v236 = nullptr;
  v63 = v239;
  v64 = v239;
  v65 = *(_QWORD *)(v10 - 200);
  if ( (*(_QWORD *)(v10 - 184) - v65) >> 3 < (unsigned __int64)v239 )
  {
    v66 = v10;
    v67 = *(_QWORD *)(v10 - 192);
    v68 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v239);
    v69 = *(char **)(v66 - 200);
    v70 = *(volatile signed __int32 ***)(v66 - 192);
    if ( v69 != (char *)v70 )
    {
      v71 = (char *)v70 - v69 - 8;
      if ( v71 >= 0x98 )
      {
        v73 = ((char *)v70 - v69) & 0xFFFFFFFFFFFFFFF8uLL;
        if ( v68 < (unsigned __int64)&v69[v73] && (unsigned __int64)v69 < v68 + v73 )
        {
          v72 = (_QWORD *)v68;
          goto LABEL_143;
        }
        v74 = (v71 >> 3) + 1;
        v75 = v74 & 0x3FFFFFFFFFFFFFFCLL;
        v76 = (((v74 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1;
        if ( (v74 & 0x3FFFFFFFFFFFFFFCLL) == 4 )
        {
          v78 = 0;
        }
        else
        {
          v77 = v76 & 0xFFFFFFFFFFFFFFFEuLL;
          v78 = 0;
          do
          {
            v79 = *(_OWORD *)&v69[8 * v78 + 16];
            *(_OWORD *)(v68 + 8 * v78) = *(_OWORD *)&v69[8 * v78];
            *(_OWORD *)(v68 + 8 * v78 + 16) = v79;
            *(_OWORD *)&v69[8 * v78] = 0;
            *(_OWORD *)&v69[8 * v78 + 16] = 0;
            v80 = *(_OWORD *)&v69[8 * v78 + 48];
            *(_OWORD *)(v68 + 8 * v78 + 32) = *(_OWORD *)&v69[8 * v78 + 32];
            *(_OWORD *)(v68 + 8 * v78 + 48) = v80;
            *(_OWORD *)&v69[8 * v78 + 32] = 0;
            *(_OWORD *)&v69[8 * v78 + 48] = 0;
            v78 += 8;
            v77 -= 2LL;
          }
          while ( v77 != 0 );
        }
        if ( (v76 & 1) != 0 )
        {
          v81 = *(_OWORD *)&v69[8 * v78 + 16];
          *(_OWORD *)(v68 + 8 * v78) = *(_OWORD *)&v69[8 * v78];
          *(_OWORD *)(v68 + 8 * v78 + 16) = v81;
          *(_OWORD *)&v69[8 * v78] = 0;
          *(_OWORD *)&v69[8 * v78 + 16] = 0;
        }
        if ( v74 != v75 )
        {
          v69 += 8 * v75;
          v72 = (_QWORD *)(v68 + 8 * v75);
          goto LABEL_143;
        }
      }
      else
      {
        v72 = (_QWORD *)v68;
        do
        {
LABEL_143:
          *v72 = *(_QWORD *)v69;
          *(_QWORD *)v69 = 0;
          ++v72;
          v69 += 8;
        }
        while ( v69 != (char *)v70 );
      }
      v70 = *(volatile signed __int32 ***)(v226 - 200);
    }
    v82 = v226;
    if ( v70 != nullptr )
    {
      v83 = *(volatile signed __int32 ***)(v226 - 192);
      if ( v70 == v83 )
      {
        v82 = v226;
      }
      else
      {
        do
        {
          v84 = *v70;
          if ( *v70 != nullptr && _InterlockedDecrement(v84) == 0 )
          {
            sub_14141FE20(a1: v84);
            sub_140DF2D40(a1: v84);
          }
          ++v70;
        }
        while ( v70 != v83 );
        v82 = v226;
        v70 = *(volatile signed __int32 ***)(v226 - 200);
      }
      sub_1407E4890(a1: qword_141ABD470, a2: v70, a3: *(_QWORD *)(v82 - 184) - (_QWORD)v70);
    }
    *(_QWORD *)(v82 - 200) = v68;
    *(_QWORD *)(v82 - 192) = v68 + v67 - v65;
    *(_QWORD *)(v82 - 184) = v68 + 8 * v64;
    v63 = v239;
    v10 = v82;
  }
  if ( v63 != 0 )
  {
    v85 = 0;
    do
    {
      if ( dword_141B5CFC0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5CFC0);
        if ( dword_141B5CFC0 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5CF70,
            a2: 1100134632,
            a3: 256,
            a4: 208,
            a5: 0,
            a6: 0,
            a7: 256,
            a8: 4096);
          sub_141751048(a1: sub_140DF2660);
          sub_141750EA0(a1: &dword_141B5CFC0);
        }
      }
      v86 = (volatile signed __int32 *)sub_1407E58C0(a1: &unk_141B5CF70, a2: 208);
      sub_14141FC50(a1: v86);
      _InterlockedIncrement(v86);
      if ( v237 != 0 && v235 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
      v238 = nullptr;
      v237 = 0;
      v236 = nullptr;
      if ( (unsigned __int8)sub_141420390(a1: v86, a2: &v235) == 0 )
      {
        if ( _InterlockedDecrement(v86) == 0 )
        {
          sub_14141FE20(a1: v86);
          sub_140DF2D40(a1: v86);
        }
        goto LABEL_361;
      }
      v87 = *(char **)(v10 - 192);
      if ( v87 != *(char **)(v10 - 184) )
      {
        *(_QWORD *)v87 = v86;
        _InterlockedIncrement(v86);
        *(_QWORD *)(v10 - 192) += 8LL;
        if ( _InterlockedDecrement(v86) != 0 )
          goto LABEL_158;
        goto LABEL_157;
      }
      v214 = v85;
      v88 = v10;
      v89 = (__int64)&v87[-*(_QWORD *)(v10 - 200)];
      v90 = v89 >> 3;
      v91 = (unsigned __int64)(v89 >> 3) >> 1;
      v92 = 0x1FFFFFFFFFFFFFFFLL - v91;
      v93 = (v89 >> 3) + v91;
      v224 = (v89 >> 3) + 1;
      if ( v93 <= v224 )
        v93 = (v89 >> 3) + 1;
      if ( v90 > v92 )
        v93 = 0x1FFFFFFFFFFFFFFFLL;
      v222 = v93;
      v94 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v93);
      v95 = v89 & 0xFFFFFFFFFFFFFFF8uLL;
      *(_QWORD *)(v94 + v95) = v86;
      _InterlockedIncrement(v86);
      v96 = *(char **)(v88 - 200);
      v97 = *(char **)(v88 - 192);
      if ( v97 != v87 )
      {
        if ( v96 == v87 )
          goto LABEL_195;
        v98 = v87 - v96 - 8;
        if ( v98 < 0x88 )
        {
          v99 = (_QWORD *)v94;
          do
          {
LABEL_193:
            *v99 = *(_QWORD *)v96;
            *(_QWORD *)v96 = 0;
            ++v99;
            v96 += 8;
          }
          while ( v96 != v87 );
LABEL_194:
          v97 = *(char **)(v226 - 192);
LABEL_195:
          if ( v97 == v87 )
            goto LABEL_217;
          v110 = v94 + v95;
          v111 = v97 - v87 - 8;
          if ( v111 >= 0xB8
            && (v94 + v95 + 8 >= (unsigned __int64)&v87[(v111 & 0xFFFFFFFFFFFFFFF8uLL) + 8]
             || (unsigned __int64)v87 >= v94 + (v111 & 0xFFFFFFFFFFFFFFF8uLL) + v95 + 16) )
          {
            v112 = (v111 >> 3) + 1;
            v113 = v112 & 0x3FFFFFFFFFFFFFFCLL;
            v114 = (((v112 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1;
            if ( (v112 & 0x3FFFFFFFFFFFFFFCLL) == 4 )
            {
              v117 = 0;
              if ( (v114 & 1) != 0 )
                goto LABEL_203;
            }
            else
            {
              v115 = v114 & 0xFFFFFFFFFFFFFFFEuLL;
              v116 = v94 + 8 * v90 + 56;
              v117 = 0;
              do
              {
                v118 = *(_OWORD *)&v87[8 * v117 + 16];
                *(_OWORD *)(v116 + 8 * v117 - 48) = *(_OWORD *)&v87[8 * v117];
                *(_OWORD *)(v116 + 8 * v117 - 32) = v118;
                *(_OWORD *)&v87[8 * v117] = 0;
                *(_OWORD *)&v87[8 * v117 + 16] = 0;
                v119 = *(_OWORD *)&v87[8 * v117 + 48];
                *(_OWORD *)(v116 + 8 * v117 - 16) = *(_OWORD *)&v87[8 * v117 + 32];
                *(_OWORD *)(v116 + 8 * v117) = v119;
                *(_OWORD *)&v87[8 * v117 + 32] = 0;
                *(_OWORD *)&v87[8 * v117 + 48] = 0;
                v117 += 8;
                v115 -= 2LL;
              }
              while ( v115 != 0 );
              if ( (v114 & 1) != 0 )
              {
LABEL_203:
                v120 = *(_OWORD *)&v87[8 * v117 + 16];
                *(_OWORD *)(v110 + 8 * v117 + 8) = *(_OWORD *)&v87[8 * v117];
                *(_OWORD *)(v110 + 8 * v117 + 24) = v120;
                *(_OWORD *)&v87[8 * v117] = 0;
                *(_OWORD *)&v87[8 * v117 + 16] = 0;
              }
            }
            if ( v112 == v113 )
              goto LABEL_217;
            v87 += 8 * v113;
            v110 += 8 * v113;
          }
          v121 = (_QWORD *)(v110 + 8);
          do
          {
            *v121 = *(_QWORD *)v87;
            *(_QWORD *)v87 = 0;
            v87 += 8;
            ++v121;
          }
          while ( v87 != v97 );
          goto LABEL_217;
        }
        if ( v94 < (unsigned __int64)&v96[(v98 & 0xFFFFFFFFFFFFFFF8uLL) + 8]
          && (unsigned __int64)v96 < v94 + (v98 & 0xFFFFFFFFFFFFFFF8uLL) + 8 )
        {
          v99 = (_QWORD *)v94;
          goto LABEL_193;
        }
        v102 = (v98 >> 3) + 1;
        v103 = v102 & 0x3FFFFFFFFFFFFFFCLL;
        v104 = (((v102 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1;
        if ( (v102 & 0x3FFFFFFFFFFFFFFCLL) == 4 )
        {
          v106 = 0;
          if ( (v104 & 1) != 0 )
            goto LABEL_190;
        }
        else
        {
          v105 = v104 & 0xFFFFFFFFFFFFFFFEuLL;
          v106 = 0;
          do
          {
            v107 = *(_OWORD *)&v96[8 * v106 + 16];
            *(_OWORD *)(v94 + 8 * v106) = *(_OWORD *)&v96[8 * v106];
            *(_OWORD *)(v94 + 8 * v106 + 16) = v107;
            *(_OWORD *)&v96[8 * v106] = 0;
            *(_OWORD *)&v96[8 * v106 + 16] = 0;
            v108 = *(_OWORD *)&v96[8 * v106 + 48];
            *(_OWORD *)(v94 + 8 * v106 + 32) = *(_OWORD *)&v96[8 * v106 + 32];
            *(_OWORD *)(v94 + 8 * v106 + 48) = v108;
            *(_OWORD *)&v96[8 * v106 + 32] = 0;
            *(_OWORD *)&v96[8 * v106 + 48] = 0;
            v106 += 8;
            v105 -= 2LL;
          }
          while ( v105 != 0 );
          if ( (v104 & 1) != 0 )
          {
LABEL_190:
            v109 = *(_OWORD *)&v96[8 * v106 + 16];
            *(_OWORD *)(v94 + 8 * v106) = *(_OWORD *)&v96[8 * v106];
            *(_OWORD *)(v94 + 8 * v106 + 16) = v109;
            *(_OWORD *)&v96[8 * v106] = 0;
            *(_OWORD *)&v96[8 * v106 + 16] = 0;
          }
        }
        if ( v102 != v103 )
        {
          v96 += 8 * v103;
          v99 = (_QWORD *)(v94 + 8 * v103);
          goto LABEL_193;
        }
        goto LABEL_194;
      }
      if ( v96 == v87 )
      {
        v10 = v226;
        if ( v87 == nullptr )
          goto LABEL_226;
        goto LABEL_218;
      }
      v100 = v87 - v96 - 8;
      if ( v100 >= 0x88 )
      {
        if ( v94 >= (unsigned __int64)&v96[(v100 & 0xFFFFFFFFFFFFFFF8uLL) + 8]
          || (unsigned __int64)v96 >= v94 + (v100 & 0xFFFFFFFFFFFFFFF8uLL) + 8 )
        {
          v122 = (v100 >> 3) + 1;
          v123 = v122 & 0x3FFFFFFFFFFFFFFCLL;
          v124 = (((v122 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1;
          if ( (v122 & 0x3FFFFFFFFFFFFFFCLL) == 4 )
          {
            v126 = 0;
            if ( (v124 & 1) != 0 )
              goto LABEL_213;
          }
          else
          {
            v125 = v124 & 0xFFFFFFFFFFFFFFFEuLL;
            v126 = 0;
            do
            {
              v127 = *(_OWORD *)&v96[8 * v126 + 16];
              *(_OWORD *)(v94 + 8 * v126) = *(_OWORD *)&v96[8 * v126];
              *(_OWORD *)(v94 + 8 * v126 + 16) = v127;
              *(_OWORD *)&v96[8 * v126] = 0;
              *(_OWORD *)&v96[8 * v126 + 16] = 0;
              v128 = *(_OWORD *)&v96[8 * v126 + 48];
              *(_OWORD *)(v94 + 8 * v126 + 32) = *(_OWORD *)&v96[8 * v126 + 32];
              *(_OWORD *)(v94 + 8 * v126 + 48) = v128;
              *(_OWORD *)&v96[8 * v126 + 32] = 0;
              *(_OWORD *)&v96[8 * v126 + 48] = 0;
              v126 += 8;
              v125 -= 2LL;
            }
            while ( v125 != 0 );
            if ( (v124 & 1) != 0 )
            {
LABEL_213:
              v129 = *(_OWORD *)&v96[8 * v126 + 16];
              *(_OWORD *)(v94 + 8 * v126) = *(_OWORD *)&v96[8 * v126];
              *(_OWORD *)(v94 + 8 * v126 + 16) = v129;
              *(_OWORD *)&v96[8 * v126] = 0;
              *(_OWORD *)&v96[8 * v126 + 16] = 0;
            }
          }
          if ( v122 == v123 )
            goto LABEL_217;
          v96 += 8 * v123;
          v101 = (_QWORD *)(v94 + 8 * v123);
          goto LABEL_216;
        }
        v101 = (_QWORD *)v94;
      }
      else
      {
        v101 = (_QWORD *)v94;
      }
      do
      {
LABEL_216:
        *v101 = *(_QWORD *)v96;
        *(_QWORD *)v96 = 0;
        ++v101;
        v96 += 8;
      }
      while ( v96 != v87 );
LABEL_217:
      v10 = v226;
      v87 = *(char **)(v226 - 200);
      if ( v87 != nullptr )
      {
LABEL_218:
        v130 = *(char **)(v10 - 192);
        if ( v87 != v130 )
        {
          do
          {
            v131 = *(volatile signed __int32 **)v87;
            if ( *(_QWORD *)v87 != 0 && _InterlockedDecrement(v131) == 0 )
            {
              sub_14141FE20(a1: v131);
              sub_140DF2D40(a1: v131);
            }
            v87 += 8;
          }
          while ( v87 != v130 );
          v87 = *(char **)(v10 - 200);
        }
        sub_1407E4890(a1: qword_141ABD470, a2: v87, a3: *(_QWORD *)(v10 - 184) - (_QWORD)v87);
      }
LABEL_226:
      *(_QWORD *)(v10 - 200) = v94;
      *(_QWORD *)(v10 - 192) = v94 + 8 * v224;
      *(_QWORD *)(v10 - 184) = v94 + 8 * v222;
      v85 = v214;
      if ( _InterlockedDecrement(v86) == 0 )
      {
LABEL_157:
        sub_14141FE20(a1: v86);
        sub_140DF2D40(a1: v86);
      }
LABEL_158:
      LOBYTE(v85) = v85 + 1;
    }
    while ( (unsigned __int8)v85 < v239 );
  }
  if ( v238 == (__int64 *)&v234 )
  {
    v132 = v237 + 1;
    v237 = v132;
    v238 = (__int64 *)&v235;
    if ( v132 != 0 )
      goto LABEL_244;
  }
  else
  {
    if ( v237 != 0 && v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v237);
    v236 = (__int16 *)&v234;
    v237 = 1;
    v238 = (__int64 *)&v235;
    v132 = 1;
LABEL_244:
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v132);
  }
  v238 = nullptr;
  v237 = 0;
  v236 = nullptr;
  v133 = v234;
  v134 = v234;
  v135 = *(_QWORD *)(v10 - 88);
  if ( (*(_QWORD *)(v10 - 72) - v135) >> 3 < (unsigned __int64)v234 )
  {
    v136 = *(_QWORD *)(v10 - 80);
    v137 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v234);
    sub_141758A00(a1: v137, a2: *(_QWORD *)(v10 - 88), a3: *(_QWORD *)(v10 - 80) - *(_QWORD *)(v10 - 88));
    v138 = *(_QWORD *)(v10 - 88);
    if ( v138 != 0 )
    {
      v139 = *(_QWORD *)(v10 - 72) - v138;
      if ( v139 == -1 )
        v139 = *(unsigned int *)(v138 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v140 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v140) >> 3 > v139)
        && (v141 = *(_QWORD *)(v140 + 8 * v139)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v141 + 32, a2: v138 - *(unsigned int *)(v141 + 120));
        v142 = *(_BYTE *)(v141 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v141 + 64)) != 0;
        if ( !v142 && *(_BYTE *)(v141 + 97) != 0 )
          sub_1412D33C0(a1: v141);
      }
      else
      {
        MEMORY[0x141948990](a1: v138 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *(_QWORD *)(v10 - 88) = v137;
    *(_QWORD *)(v10 - 80) = v137 + v136 - v135;
    *(_QWORD *)(v10 - 72) = v137 + 8 * v134;
    v133 = v234;
  }
  v225 = (__int64 *)(v10 - 88);
  if ( v133 != 0 )
  {
    for ( j = 0; j < v234; ++j )
    {
      v144 = sub_140DDA8F0(a1: 16);
      *(_QWORD *)v144 = 0;
      *(_BYTE *)(v144 + 8) = 0;
      if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
      {
        v146 = (__int16 *)(v144 + 8);
        if ( v238 != (__int64 *)v144 )
        {
          if ( v237 != 0 && v235 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(
              a1: v235,
              a2: v236,
              a3: v237);
          v236 = (__int16 *)v144;
          v237 = 4;
          v238 = (__int64 *)(v144 + 4);
          v147 = 4;
LABEL_274:
          v145 = 1;
          if ( v235 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(
              a1: v235,
              a2: v236,
              a3: v147);
          goto LABEL_279;
        }
        v33 = v237 == -4;
        v147 = v237 + 4;
        v237 += 4;
        v238 = (__int64 *)(v144 + 4);
        if ( !v33 )
          goto LABEL_274;
        v145 = 1;
      }
      else
      {
        if ( v238 == (__int64 *)v144 )
        {
          v33 = v237 == -9;
          v237 += 9;
          v238 = (__int64 *)(v144 + 9);
          v145 = v237;
          if ( v33 )
            goto LABEL_282;
          goto LABEL_280;
        }
        v145 = 9;
        if ( v237 != 0 && v235 != nullptr )
        {
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v237);
          v146 = (__int16 *)v144;
        }
        else
        {
          v146 = (__int16 *)v144;
        }
      }
LABEL_279:
      v236 = v146;
      v237 = v145;
      v238 = (__int64 *)(v144 + 9);
LABEL_280:
      if ( v235 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v145);
LABEL_282:
      v238 = nullptr;
      v237 = 0;
      v236 = nullptr;
      if ( v235[4] != 0 )
        goto LABEL_361;
      v148 = *(__int64 **)(v10 - 80);
      if ( v148 == *(__int64 **)(v10 - 72) )
      {
        v149 = (__int64)v148 - *(_QWORD *)(v10 - 88);
        v150 = v149 >> 3;
        v151 = (unsigned __int64)(v149 >> 3) >> 1;
        v152 = 0x1FFFFFFFFFFFFFFFLL - v151;
        v153 = (v149 >> 3) + v151;
        v223 = (v149 >> 3) + 1;
        if ( v153 <= v223 )
          v153 = v150 + 1;
        if ( v150 > v152 )
          v153 = 0x1FFFFFFFFFFFFFFFLL;
        v154 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v153);
        *(_QWORD *)(v154 + v149) = v144;
        v155 = v154;
        v156 = *(__int64 **)(v10 - 80);
        sub_141758A00(a1: v154, a2: *(_QWORD *)(v10 - 88), a3: (char *)v148 - *(_QWORD *)(v10 - 88));
        if ( v156 != v148 )
          sub_141758A00(a1: v155 + v149 + 8, a2: v148, a3: *(_QWORD *)(v10 - 80) - (_QWORD)v148);
        v157 = *v225;
        if ( *v225 != 0 )
        {
          v158 = *(_QWORD *)(v226 - 72) - v157;
          if ( v158 == -1 )
          {
            v158 = *(unsigned int *)(v157 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
              goto LABEL_300;
          }
          else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
            goto LABEL_300;
          }
          v159 = *(_QWORD *)(qword_141ABD470 + 24);
          if ( (*(_QWORD *)(qword_141ABD470 + 32) - v159) >> 3 > v158 && (v160 = *(_QWORD *)(v159 + 8 * v158)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v160 + 32, a2: v157 - *(unsigned int *)(v160 + 120));
            if ( (*(_BYTE *)(v160 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v160 + 64)) == 0)
              && *(_BYTE *)(v160 + 97) != 0 )
            {
              sub_1412D33C0(a1: v160);
            }
          }
          else
          {
LABEL_300:
            MEMORY[0x141948990](a1: v157 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v10 = v226;
        *(_QWORD *)(v226 - 88) = v155;
        *(_QWORD *)(v226 - 80) = v155 + 8 * v223;
        *(_QWORD *)(v226 - 72) = v155 + 8 * v153;
        continue;
      }
      *v148 = v144;
      *(_QWORD *)(v10 - 80) += 8LL;
    }
  }
  if ( v238 == (__int64 *)&v231 )
  {
    v33 = v237 == -4;
    v161 = v237 + 4;
    v237 += 4;
    v238 = (__int64 *)v232;
    if ( !v33 )
      goto LABEL_310;
  }
  else
  {
    if ( v237 != 0 && v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v237);
    v236 = (__int16 *)&v231;
    v237 = 4;
    v238 = (__int64 *)v232;
    v161 = 4;
LABEL_310:
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v161);
  }
  v238 = nullptr;
  v237 = 0;
  v236 = nullptr;
  if ( v231 == 0 )
    goto LABEL_341;
  if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B59AA8);
    if ( dword_141B59AA8 == -1 )
    {
      sub_1407E3E70(a1: &unk_141B59A68);
      sub_141751048(a1: sub_1407E4B20);
      sub_141750EA0(a1: &dword_141B59AA8);
      v10 = v226;
    }
  }
  v164 = (__int64 *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
  if ( qword_141ABD470 == 0 )
    qword_141ABD470 = sub_1407E4940(a1: v163, a2: v162, a3: v165);
  v164[2] = 0;
  v164[1] = 0;
  *v164 = 0;
  *(_QWORD *)(v10 - 128) = v164;
  v166 = v231;
  v167 = *v164;
  if ( (v164[2] - *v164) >> 3 < (unsigned __int64)v231 )
  {
    v168 = v164[1];
    v169 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v231);
    sub_141758A00(a1: v169, a2: *v164, a3: v164[1] - *v164);
    if ( *v164 != 0 )
      sub_1407E4890(a1: qword_141ABD470, a2: *v164, a3: v164[2] - *v164);
    *v164 = v169;
    v164[1] = v169 + v168 - v167;
    v164[2] = v169 + 8 * v166;
    LODWORD(v166) = v231;
  }
  if ( (_DWORD)v166 == 0 )
  {
LABEL_341:
    if ( v238 == (__int64 *)&v230 )
    {
      v185 = v237 + 1;
      v237 = v185;
      v238 = (__int64 *)&v231;
      if ( v185 == 0 )
      {
LABEL_349:
        v238 = nullptr;
        v237 = 0;
        v236 = nullptr;
        if ( v230 == 0 )
          goto LABEL_354;
        if ( dword_141B5CA08 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B5CA08);
          if ( dword_141B5CA08 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B5C9B8,
              a2: 1100131635,
              a3: 4096,
              a4: 15,
              a5: 0,
              a6: 0,
              a7: 1024,
              a8: 0);
            sub_141751048(a1: sub_140DD54C0);
            sub_141750EA0(a1: &dword_141B5CA08);
          }
        }
        v186 = sub_1407E58C0(a1: &unk_141B5C9B8, a2: 15);
        *(_DWORD *)v186 = 168430090;
        *(_BYTE *)(v186 + 4) = 10;
        *(_QWORD *)(v186 + 5) = 0x10A050501010101LL;
        *(_WORD *)(v186 + 13) = 1281;
        *(_QWORD *)(v10 - 120) = v186;
        if ( (unsigned __int8)sub_141033470(a1: v186, a2: &v235) == 0 )
          goto LABEL_361;
        if ( v238 == (__int64 *)&v228 )
        {
          v33 = v237 == -2;
          v187 = v237 + 2;
          v237 += 2;
          v238 = (__int64 *)&v229;
          if ( v33 )
            goto LABEL_359;
        }
        else
        {
LABEL_354:
          if ( v237 != 0 && v235 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
          v236 = &v228;
          v237 = 2;
          v238 = (__int64 *)&v229;
          v187 = 2;
        }
        if ( v235 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v187);
LABEL_359:
        v238 = nullptr;
        v237 = 0;
        v236 = nullptr;
        v188 = v228;
        v189 = *(_QWORD *)(v10 - 160);
        v190 = *(_QWORD *)(v10 - 152);
        v191 = (v190 - v189) >> 2;
        if ( v191 <= v228 )
        {
          if ( v191 < v228 )
          {
            v192 = (*(_QWORD *)(v10 - 144) - v189) >> 2;
            if ( v192 >= v228 )
            {
              v199 = v228 - v191;
              v200 = v190 + 4 * v199;
              sub_141758A10(a1: v190, a2: 0, a3: 4 * v199);
              *(_QWORD *)(v10 - 152) = v200;
            }
            else
            {
              if ( v228 < 0 )
                sub_1400526C0(a1: v190, a2: v192, a3: v187);
              v193 = v192 + (v192 >> 1);
              if ( v193 <= v228 )
                v193 = v228;
              if ( v192 > 0x3FFFFFFFFFFFFFFFLL - (v192 >> 1) )
                v193 = 0x3FFFFFFFFFFFFFFFLL;
              v194 = 4 * v193;
              if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
                && (v195 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v195) >> 3 > v194)
                && (v196 = *(_QWORD *)(v195 + 32 * v193)) != 0 )
              {
                v197 = *(unsigned int *)(v196 + 88);
                v198 = (char *)sub_1407E58C0(a1: v196, a2: *(unsigned int *)(v196 + 80));
              }
              else
              {
                v197 = *(unsigned int *)(qword_141ABE200 + 48);
                v198 = (char *)sub_141601260(a1: (unsigned int)(v197 + v194), a2: 4096, a3: v187);
              }
              v201 = v198;
              if ( v197 != 0 )
              {
                *(_DWORD *)v198 = v194;
                v201 = &v198[v197];
              }
              sub_141758A10(a1: &v201[4 * v191], a2: 0, a3: 4 * (v188 - v191));
              sub_141758A00(a1: v201, a2: *(_QWORD *)(v10 - 160), a3: *(_QWORD *)(v10 - 152) - *(_QWORD *)(v10 - 160));
              v202 = *(_QWORD *)(v10 - 160);
              if ( v202 != 0 )
                sub_1407E6420(a1: qword_141ABE200, a2: v202, a3: *(_QWORD *)(v10 - 144) - v202);
              *(_QWORD *)(v10 - 160) = v201;
              *(_QWORD *)(v10 - 152) = &v201[4 * v188];
              *(_QWORD *)(v10 - 144) = &v201[4 * v193];
            }
          }
        }
        else
        {
          *(_QWORD *)(v10 - 152) = v189 + 4LL * v228;
        }
        v203 = v228;
        v204 = (__int64)v238;
        if ( v228 > 0 )
        {
          v205 = 0;
          v206 = 0;
          do
          {
            v208 = *(_QWORD *)(v10 - 160);
            if ( v208 + v205 == v204 )
            {
              v207 = v237 + 4;
            }
            else
            {
              if ( v237 != 0 && v235 != nullptr )
              {
                (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(
                  a1: v235,
                  a2: v236,
                  a3: v237);
                v203 = v228;
              }
              v236 = (__int16 *)(v208 + v205);
              v207 = 4;
            }
            v237 = v207;
            v204 = v208 + 4 * v206 + 4;
            v238 = (__int64 *)(v208 + v205 + 4);
            ++v206;
            v205 += 4;
          }
          while ( v206 < v203 );
          v204 = v205 + v208;
        }
        if ( v204 == v10 - 24 )
        {
          v33 = v237 == -2;
          v209 = v237 + 2;
          v237 += 2;
          v238 = v215;
          if ( v33 )
            goto LABEL_405;
        }
        else
        {
          if ( v237 != 0 && v235 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(
              a1: v235,
              a2: v236,
              a3: v237);
          v236 = (__int16 *)(v10 - 24);
          v237 = 2;
          v238 = v215;
          v209 = 2;
        }
        if ( v235 == nullptr )
          goto LABEL_414;
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v209);
LABEL_405:
        v236 = v216;
        v237 = 4;
        v238 = (__int64 *)(v10 - 36);
        if ( v235 != nullptr )
        {
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v216, a3: 4);
          v236 = v218;
          v237 = 1;
          v238 = v217;
          if ( v235 != nullptr )
          {
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v218, a3: 1);
            v236 = (__int16 *)(v10 - 36);
            v237 = 8;
            v238 = (__int64 *)(v10 - 28);
            v8 = (__int16 *)(v10 - 92);
            if ( v235 != nullptr )
            {
              (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v235 + 40LL))(
                a1: v235,
                a2: v10 - 36,
                a3: 8);
              v236 = (__int16 *)(v10 - 92);
              v237 = 4;
              v238 = v225;
              v11 = a7;
              v9 = a3;
              if ( v235 != nullptr )
              {
                (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v235 + 40LL))(
                  a1: v235,
                  a2: v10 - 92,
                  a3: 4);
                v236 = (__int16 *)(v10 - 56);
                v237 = 4;
                v238 = (__int64 *)(v10 - 52);
                if ( v235 != nullptr )
                {
                  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v235 + 40LL))(
                    a1: v235,
                    a2: v10 - 56,
                    a3: 4);
                  v236 = (__int16 *)(v10 - 28);
                  v237 = 4;
                  v238 = (__int64 *)(v10 - 24);
                  if ( v235 != nullptr )
                  {
                    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v235 + 40LL))(
                      a1: v235,
                      a2: v10 - 28,
                      a3: 4);
                    v236 = v220;
                    v237 = 1;
                    v238 = (__int64 *)(v10 - 13);
                    if ( v235 != nullptr )
                    {
                      LODWORD(v8) = v10 - 136;
                      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(
                        a1: v235,
                        a2: v220,
                        a3: 1);
                      v236 = (__int16 *)(v10 - 136);
                      v237 = 8;
                      v238 = (__int64 *)(v10 - 128);
                      if ( v235 != nullptr )
                        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v235 + 40LL))(
                          a1: v235,
                          a2: v10 - 136,
                          a3: 8);
                      goto LABEL_418;
                    }
                  }
                }
              }
LABEL_417:
              v238 = nullptr;
              v237 = 0;
              v236 = nullptr;
              goto LABEL_418;
            }
LABEL_416:
            v236 = v8;
            v237 = 4;
            v238 = v225;
            v11 = a7;
            v9 = a3;
            goto LABEL_417;
          }
LABEL_415:
          v8 = (__int16 *)(v10 - 92);
          goto LABEL_416;
        }
LABEL_414:
        v236 = nullptr;
        goto LABEL_415;
      }
    }
    else
    {
      if ( v237 != 0 && v235 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v237);
      v236 = (__int16 *)&v230;
      v237 = 1;
      v238 = (__int64 *)&v231;
      v185 = 1;
    }
    if ( v235 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236, a3: v185);
    goto LABEL_349;
  }
  v170 = 0;
  v171 = &unk_141B5CD88;
  v172 = 0xC3000000000LL;
  while ( 1 )
  {
    if ( dword_141B5CDD8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B5CDD8);
      if ( dword_141B5CDD8 == -1 )
      {
        sub_1407E53D0(a1: (_DWORD)v171, a2: 1100141292, a3: 128, a4: 16, a5: 0, a6: 0, a7: 128, a8: 4096);
        sub_141751048(a1: sub_140DF2550);
        sub_141750EA0(a1: &dword_141B5CDD8);
      }
    }
    v173 = sub_1407E58C0(a1: v171, a2: 16);
    *(_DWORD *)(v173 + 8) = -16776959;
    *(_QWORD *)v173 = 0;
    *(_BYTE *)(v173 + 12) = 2;
    if ( (unsigned __int8)sub_14141E220(a1: v173, a2: &v235, a3: *(unsigned __int16 *)(a4 + 1416)) == 0 )
      break;
    v174 = *(unsigned __int8 *)(v173 + 10);
    if ( v174 <= 0x2B && _bittest64(&v172, v174) )
    {
      sub_140DF23E0(a1: v173);
    }
    else
    {
      v175 = v171;
      v176 = *(__int64 **)(v10 - 128);
      v177 = (__int64 *)v176[1];
      if ( v177 == (__int64 *)v176[2] )
      {
        v178 = (__int64)v177 - *v176;
        v179 = v178 >> 3;
        v180 = (unsigned __int64)(v178 >> 3) >> 1;
        v181 = 0x1FFFFFFFFFFFFFFFLL - v180;
        v182 = (v178 >> 3) + v180;
        if ( v182 <= (v178 >> 3) + 1 )
          v182 = v179 + 1;
        if ( v179 > v181 )
          v182 = 0x1FFFFFFFFFFFFFFFLL;
        v183 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v182);
        *(_QWORD *)(v183 + v178) = v173;
        v184 = (__int64 *)v176[1];
        sub_141758A00(a1: v183, a2: *v176, a3: (char *)v177 - *v176);
        if ( v184 != v177 )
          sub_141758A00(a1: v183 + v178 + 8, a2: v177, a3: v176[1] - (_QWORD)v177);
        v171 = &unk_141B5CD88;
        if ( *v176 != 0 )
          sub_1407E4890(a1: qword_141ABD470, a2: *v176, a3: v176[2] - *v176);
        *v176 = v183;
        v176[1] = v183 + 8 * ((v178 >> 3) + 1);
        v176[2] = v183 + 8 * v182;
        v10 = v226;
        v172 = 0xC3000000000LL;
      }
      else
      {
        *v177 = v173;
        v176[1] += 8;
        v172 = 0xC3000000000LL;
        v171 = v175;
      }
    }
    if ( ++v170 >= (unsigned __int64)v231 )
      goto LABEL_341;
  }
  sub_140DF23E0(a1: v173);
  LODWORD(v8) = 0;
LABEL_428:
  if ( v237 != 0 )
  {
    if ( v235 != nullptr )
    {
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v235 + 40LL))(a1: v235, a2: v236);
      goto LABEL_431;
    }
  }
  else
  {
LABEL_431:
    v211 = (void (__fastcall ***)(_QWORD, __int64))v235;
    v238 = nullptr;
    v237 = 0;
    v236 = nullptr;
    if ( v235 != nullptr && _InterlockedDecrement(v235 + 2) == 0 )
      (**v211)(a1: v211, a2: 1);
  }
  return (unsigned int)v8;
}
