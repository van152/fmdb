__int64 __fastcall sub_14105D510(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        char a7,
        __int64 a8)
{
  char v11; // r12
  __int64 v12; // rbp
  unsigned __int16 *v13; // r15
  volatile signed __int32 *v14; // rbp
  volatile signed __int32 *v15; // rbp
  volatile signed __int32 *v16; // rbp
  volatile signed __int32 *v17; // rbp
  volatile signed __int32 *v18; // rbp
  volatile signed __int32 *v19; // rbp
  int v20; // eax
  __int64 v21; // rbp
  __int64 i; // rdi
  volatile signed __int32 *v23; // rbx
  volatile signed __int32 *v24; // rbx
  volatile signed __int32 *v25; // rbx
  volatile signed __int32 *v26; // rbx
  __int16 *v27; // rbp
  volatile signed __int32 *v28; // rbx
  volatile signed __int32 *v29; // rbx
  volatile signed __int32 *v30; // rbx
  volatile signed __int32 *v31; // rbx
  volatile signed __int32 *v32; // rbx
  volatile signed __int32 *v33; // rbx
  volatile signed __int32 *v34; // rbx
  volatile signed __int32 *v35; // rbx
  volatile signed __int32 *v36; // rbx
  volatile signed __int32 *v37; // rbx
  volatile signed __int32 *v38; // rbx
  volatile signed __int32 *v39; // rbx
  volatile signed __int32 *v40; // rbx
  volatile signed __int32 *v41; // rbx
  volatile signed __int32 *v42; // rbx
  volatile signed __int32 *v43; // rbx
  volatile signed __int32 *v44; // rbx
  volatile signed __int32 *v45; // rbx
  volatile signed __int32 *v46; // rbx
  char v47; // di
  volatile signed __int32 *v48; // rbx
  volatile signed __int32 *v49; // rbx
  int v50; // edi
  volatile signed __int32 *v51; // rbx
  volatile signed __int32 *v52; // rbx
  int v53; // edi
  volatile signed __int32 *v54; // rbx
  volatile signed __int32 *v55; // rbx
  __int64 v56; // rbp
  char v57; // di
  volatile signed __int32 *v58; // rbx
  volatile signed __int32 *v59; // rbx
  __int64 v60; // rbp
  char v61; // di
  volatile signed __int32 *v62; // rbx
  volatile signed __int32 *v63; // rbx
  __int64 v64; // rbp
  char v65; // di
  volatile signed __int32 *v66; // rbx
  volatile signed __int32 *v67; // rbx
  __int64 v68; // rbp
  char v69; // di
  volatile signed __int32 *v70; // rbx
  volatile signed __int32 *v71; // rbx
  int v72; // edi
  volatile signed __int32 *v73; // rbx
  volatile signed __int32 *v74; // rbx
  int v75; // edi
  volatile signed __int32 *v76; // rbx
  volatile signed __int32 *v77; // rbx
  int v78; // ebx
  void (__fastcall ***v79)(_QWORD, __int64); // rbp
  volatile signed __int32 *v80; // rbx
  int j; // ebx
  void (__fastcall ***v82)(_QWORD, __int64); // rbp
  volatile signed __int32 *v83; // rbx
  int v84; // edi
  __int64 v85; // rax
  volatile signed __int32 *v86; // rbx
  __int64 v87; // rbp
  __int64 v88; // rax
  __int64 v89; // rax
  _QWORD *v90; // rbp
  volatile signed __int32 *v91; // rbx
  int v92; // edi
  __int64 v93; // rbp
  volatile signed __int32 *v94; // rbx
  int v95; // edi
  volatile signed __int32 *v96; // rbx
  int v97; // ebx
  volatile signed __int32 *v98; // rbx
  char *v99; // rbp
  __int64 v100; // rax
  unsigned __int64 v101; // rdi
  volatile signed __int32 *v102; // rbx
  int *v103; // rbp
  volatile signed __int32 *v104; // rbx
  _QWORD *v105; // rbp
  volatile signed __int32 *v106; // rbx
  volatile signed __int32 *v107; // rbx
  volatile signed __int32 *v108; // rbx
  volatile signed __int32 *v109; // rbx
  volatile signed __int32 *v110; // rbx
  volatile signed __int32 *v111; // rbx
  volatile signed __int32 *v112; // rbx
  unsigned int v113; // ebp
  volatile signed __int32 *v115; // rbx
  volatile signed __int32 *v116; // rbx
  volatile signed __int32 *v117; // rbx
  _BYTE *v118; // rbp
  volatile signed __int32 *v119; // rbx
  __int64 v120; // rdi
  volatile signed __int32 *v121; // rbp
  volatile signed __int32 *v122; // rbx
  volatile signed __int32 *v123; // rbx
  volatile signed __int32 *v124; // rbx
  volatile signed __int32 *v125; // rbx
  volatile signed __int32 *v126; // rbx
  volatile signed __int32 *v127; // rbx
  volatile signed __int32 *v128; // rbx
  volatile signed __int32 *v129; // rbx
  volatile signed __int32 *v130; // rbx
  volatile signed __int32 *v131; // rbx
  volatile signed __int32 *v132; // rbx
  volatile signed __int32 *v133; // rbx
  volatile signed __int32 *v134; // rbx
  volatile signed __int32 *v135; // rbx
  volatile signed __int32 *v136; // rbx
  volatile signed __int32 *v137; // rbx
  volatile signed __int32 *v138; // rbx
  volatile signed __int32 *v139; // rbx
  char v140; // bl
  volatile signed __int32 *v141; // rbx
  char v142; // bl
  volatile signed __int32 *v143; // rbx
  char v144; // bl
  volatile signed __int32 *v145; // rbx
  char v146; // bl
  __int64 v147; // rax
  volatile signed __int32 *v148; // rbx
  int v149; // ebx
  _QWORD *v150; // rax
  volatile signed __int32 *v151; // rbx
  int v152; // ebx
  _QWORD *v153; // rax
  volatile signed __int32 *v154; // rbx
  __int64 v155; // rbp
  volatile signed __int32 *v156; // rbx
  volatile signed __int32 *v157; // rbx
  volatile signed __int32 *v158; // rbx
  volatile signed __int32 *v159; // rbx
  volatile signed __int32 *v160; // rbx
  volatile signed __int32 *v161; // rbx
  volatile signed __int32 *v162; // rbx
  volatile signed __int32 *v163; // rbx
  volatile signed __int32 *v164; // rbx
  volatile signed __int32 *v165; // rbx
  volatile signed __int32 *v166; // rbx
  volatile signed __int32 *v167; // rbx
  volatile signed __int32 *v168; // rbx
  volatile signed __int32 *v169; // rbx
  volatile signed __int32 *v170; // rbx
  volatile signed __int32 *v171; // rbx
  volatile signed __int32 *v172; // rbx
  volatile signed __int32 *v173; // rbx
  volatile signed __int32 *v174; // rbx
  volatile signed __int32 *v175; // rbx
  volatile signed __int32 *v176; // rbx
  volatile signed __int32 *v177; // rbx
  volatile signed __int32 *v178; // rbx
  volatile signed __int32 *v179; // rbx
  volatile signed __int32 *v180; // rbx
  volatile signed __int32 *v181; // rbx
  volatile signed __int32 *v182; // rbx
  unsigned __int64 v183; // rbp
  volatile signed __int32 *v184; // rbx
  volatile signed __int32 *v185; // rbx
  unsigned __int64 v186; // rbp
  volatile signed __int32 *v187; // rbx
  volatile signed __int32 *v188; // rbx
  unsigned __int64 v189; // rbp
  volatile signed __int32 *v190; // rbx
  volatile signed __int32 *v191; // rbx
  __int64 v192; // rbp
  volatile signed __int32 *v193; // rbx
  volatile signed __int32 *v194; // rbx
  volatile signed __int32 *v195; // rbx
  volatile signed __int32 *v196; // rbx
  volatile signed __int32 *v197; // rbx
  volatile signed __int32 *v198; // rbx
  volatile signed __int32 *v199; // rbx
  volatile signed __int32 *v200; // rbx
  volatile signed __int32 *v201; // rbx
  volatile signed __int32 *v202; // rbx
  volatile signed __int32 *v203; // rbx
  volatile signed __int32 *v204; // rbx
  volatile signed __int32 *v205; // rbx
  volatile signed __int32 *v206; // rbx
  volatile signed __int32 *v207; // rbx
  volatile signed __int32 *v208; // rbx
  volatile signed __int32 *v209; // rbx
  volatile signed __int32 *v210; // rbx
  volatile signed __int32 *v211; // rbx
  volatile signed __int32 *v212; // rbx
  int v213; // ecx
  volatile signed __int32 *v214; // rbx
  volatile signed __int32 *v215; // rbx
  volatile signed __int32 *v216; // rbx
  volatile signed __int32 *v217; // rbx
  char v218; // [rsp+47h] [rbp-C1h] BYREF
  __int16 v219[5]; // [rsp+48h] [rbp-C0h] BYREF
  __int16 v220; // [rsp+52h] [rbp-B6h] BYREF
  __int16 v221; // [rsp+54h] [rbp-B4h] BYREF
  __int16 v222; // [rsp+56h] [rbp-B2h] BYREF
  __int64 v223; // [rsp+58h] [rbp-B0h]
  __int16 v224; // [rsp+66h] [rbp-A2h] BYREF
  int v225; // [rsp+68h] [rbp-A0h] BYREF
  __int16 v226; // [rsp+6Ch] [rbp-9Ch] BYREF
  char v227; // [rsp+6Fh] [rbp-99h] BYREF
  __int128 v228; // [rsp+70h] [rbp-98h] BYREF
  __int64 v229; // [rsp+80h] [rbp-88h]
  __int16 v230; // [rsp+88h] [rbp-80h]
  int v231; // [rsp+98h] [rbp-70h] BYREF
  _BYTE v232[8]; // [rsp+A0h] [rbp-68h] BYREF
  __int64 v233; // [rsp+A8h] [rbp-60h]
  _BYTE v234[4]; // [rsp+B4h] [rbp-54h] BYREF
  __int64 v235; // [rsp+B8h] [rbp-50h] BYREF
  char v236; // [rsp+C0h] [rbp-48h]

  v11 = a7;
  v235 = 0;
  v236 = 100;
  if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDC3u )
  {
    if ( dword_141B5F1B0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5F1B0);
      if ( dword_141B5F1B0 == -1 )
      {
        sub_1407E53D0((unsigned int)&unk_141B5F160, 1100140474, 256, 472, 0, 0, 256, 4096);
        sub_141751048(sub_140FB3DB0);
        sub_141750EA0(&dword_141B5F1B0);
      }
    }
    v12 = sub_1407E58C0(&unk_141B5F160, 472);
    sub_14103F5F0(v12);
    *(_QWORD *)(a1 + 368) = v12;
    *(_QWORD *)(v12 + 264) = a1;
  }
  v13 = (unsigned __int16 *)(a4 + 1416);
  if ( v11 != 0 )
  {
    v14 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 412, 2);
    if ( *((_DWORD *)v14 + 4) != 0 )
      return 0;
    v15 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 404, 4);
    if ( *((_DWORD *)v15 + 4) != 0 )
      return 0;
    v16 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 416, 4);
    if ( *((_DWORD *)v16 + 4) != 0 )
      return 0;
    if ( *v13 <= 0xDC3u )
    {
      v17 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int128 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v228, 4);
      if ( *((_DWORD *)v17 + 4) != 0 )
        return 0;
    }
    v18 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 408, 4);
    if ( *((_DWORD *)v18 + 4) != 0 )
      return 0;
    v231 = 16;
    v19 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v231, 4);
    if ( *((_DWORD *)v19 + 4) != 0 )
      return 0;
    v20 = v231;
    if ( v231 > 0 )
    {
      v21 = a1 + 488;
      for ( i = 0; i < v20; ++i )
      {
        if ( *v13 <= 0xDCFu && i == 15 )
        {
          *(_DWORD *)(a1 + 484) = 0;
          *(_DWORD *)(a1 + 548) = 0;
        }
        else
        {
          v23 = *a2;
          (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
            *a2,
            v21 - 64,
            4);
          if ( *((_DWORD *)v23 + 4) != 0 )
            return 0;
          v24 = *a2;
          (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v21, 4);
          if ( *((_DWORD *)v24 + 4) != 0 )
            return 0;
          v20 = v231;
        }
        v21 += 4;
      }
    }
    v25 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 552, 4);
    if ( *((_DWORD *)v25 + 4) != 0 )
      return 0;
    v26 = *a2;
    v27 = (__int16 *)(a1 + 414);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 414, 2);
    if ( *((_DWORD *)v26 + 4) != 0 )
      return 0;
    if ( *v27 <= 999 )
      *v27 = 1000;
    v28 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 556, 4);
    if ( *((_DWORD *)v28 + 4) != 0 )
      return 0;
    v29 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 560, 2);
    if ( *((_DWORD *)v29 + 4) != 0 )
      return 0;
    v30 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 562, 2);
    if ( *((_DWORD *)v30 + 4) != 0 )
      return 0;
    if ( *v13 <= 0xDC3u )
    {
      v31 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 280LL,
        4);
      if ( *((_DWORD *)v31 + 4) != 0 )
        return 0;
    }
    v32 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1146, 1);
    if ( *((_DWORD *)v32 + 4) != 0 )
      return 0;
    v33 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1140, 4);
    if ( *((_DWORD *)v33 + 4) != 0 )
      return 0;
    if ( *v13 <= 0xDC3u )
    {
      v34 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 388LL,
        4);
      if ( *((_DWORD *)v34 + 4) != 0 )
        return 0;
      v35 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 392LL,
        4);
      if ( *((_DWORD *)v35 + 4) != 0 )
        return 0;
      v36 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 396LL,
        4);
      if ( *((_DWORD *)v36 + 4) != 0 )
        return 0;
      v37 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 400LL,
        4);
      if ( *((_DWORD *)v37 + 4) != 0 )
        return 0;
      v38 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 404LL,
        4);
      if ( *((_DWORD *)v38 + 4) != 0 )
        return 0;
      v39 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 408LL,
        4);
      if ( *((_DWORD *)v39 + 4) != 0 )
        return 0;
      v40 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        *(_QWORD *)(a1 + 368) + 458LL,
        1);
      if ( *((_DWORD *)v40 + 4) != 0 )
        return 0;
    }
    v41 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1148, 1);
    if ( *((_DWORD *)v41 + 4) != 0 )
      return 0;
    v42 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1144, 2);
    if ( *((_DWORD *)v42 + 4) != 0 )
      return 0;
    v43 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1128, 4);
    if ( *((_DWORD *)v43 + 4) != 0 )
      return 0;
    v44 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1150, 2);
    if ( *((_DWORD *)v44 + 4) != 0 )
      return 0;
    if ( *v13 <= 0xDC3u )
    {
      *(_WORD *)(*(_QWORD *)(a1 + 368) + 456LL) = *(_WORD *)(a1 + 1150) & 0x200;
      *(_BYTE *)(a1 + 1151) &= ~2u;
    }
    v45 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1136, 4);
    if ( *((_DWORD *)v45 + 4) != 0 )
      return 0;
    sub_140839290(*a2, &v228, a1 + 1160);
    if ( (_DWORD)v228 != 0 )
      return 0;
    sub_140839480(*a2, &v228, a1 + 1184);
    if ( (_DWORD)v228 != 0 )
      return 0;
    sub_14105FA40(&v228, a2, a1 + 564);
    if ( (_DWORD)v228 != 0 )
      return 0;
    sub_14105FA40(&v228, a2, a1 + 808);
    if ( (_DWORD)v228 != 0 )
      return 0;
    v46 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
    if ( *((_DWORD *)v46 + 4) != 0 )
      return 0;
    v223 = a1 + 1056;
    sub_141011F70(a1 + 1056, v218);
    if ( v218 > 0 )
    {
      v47 = 0;
      do
      {
        v48 = *a2;
        (*(void (__fastcall **)(volatile signed __int32 *, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v234, 4);
        if ( *((_DWORD *)v48 + 4) != 0 )
          return 0;
        sub_14105FB30(v223, v234);
      }
      while ( ++v47 < v218 );
    }
    v49 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v221, 2);
    if ( *((_DWORD *)v49 + 4) == 0 )
    {
      v223 = a1 + 1232;
      sub_141011F70(a1 + 1232, v221);
      if ( v221 > 0 )
      {
        v50 = 0;
        do
        {
          v51 = *a2;
          (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v225, 4);
          if ( *((_DWORD *)v51 + 4) != 0 )
            return 0;
          sub_140CD95D0(v223, &v225);
        }
        while ( ++v50 < v221 );
      }
      if ( *v13 >= 0xDC4u )
      {
LABEL_67:
        v233 = 0;
        while ( 1 )
        {
          v55 = *a2;
          (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
          if ( *((_DWORD *)v55 + 4) != 0 )
            return 0;
          v223 = 96 * v233;
          if ( v218 > 0 )
          {
            v56 = a1 + v223 + 1280;
            sub_141011F70(v56, (unsigned __int8)v218);
            if ( v218 > 0 )
            {
              v57 = 0;
              do
              {
                v58 = *a2;
                (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(
                  *a2,
                  &a6,
                  4);
                if ( *((_DWORD *)v58 + 4) != 0 )
                  return 0;
                sub_140CD95D0(v56, &a6);
              }
              while ( ++v57 < v218 );
            }
          }
          v59 = *a2;
          (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
          if ( *((_DWORD *)v59 + 4) != 0 )
            return 0;
          if ( v218 > 0 )
          {
            v60 = a1 + v223 + 1304;
            sub_141011F70(v60, (unsigned __int8)v218);
            if ( v218 > 0 )
            {
              v61 = 0;
              do
              {
                v62 = *a2;
                (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(
                  *a2,
                  &a6,
                  4);
                if ( *((_DWORD *)v62 + 4) != 0 )
                  return 0;
                sub_140CD95D0(v60, &a6);
              }
              while ( ++v61 < v218 );
            }
          }
          v63 = *a2;
          (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
          if ( *((_DWORD *)v63 + 4) != 0 )
            return 0;
          if ( v218 > 0 )
          {
            v64 = a1 + v223 + 1328;
            sub_141011F70(v64, (unsigned __int8)v218);
            if ( v218 > 0 )
            {
              v65 = 0;
              do
              {
                v66 = *a2;
                (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(
                  *a2,
                  &a6,
                  4);
                if ( *((_DWORD *)v66 + 4) != 0 )
                  return 0;
                sub_140CD95D0(v64, &a6);
              }
              while ( ++v65 < v218 );
            }
          }
          v67 = *a2;
          (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
          if ( *((_DWORD *)v67 + 4) != 0 )
            return 0;
          if ( v218 > 0 )
          {
            v68 = a1 + v223 + 1352;
            sub_141011F70(v68, (unsigned __int8)v218);
            if ( v218 > 0 )
            {
              v69 = 0;
              do
              {
                v70 = *a2;
                (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(
                  *a2,
                  &a6,
                  4);
                if ( *((_DWORD *)v70 + 4) != 0 )
                  return 0;
                sub_140CD95D0(v68, &a6);
              }
              while ( ++v69 < v218 );
            }
          }
          if ( ++v233 == 5 )
          {
            v71 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              &v222,
              2);
            if ( *((_DWORD *)v71 + 4) != 0 )
              return 0;
            v223 = a1 + 1208;
            sub_141011F70(a1 + 1208, v222);
            if ( v222 > 0 )
            {
              v72 = 0;
              do
              {
                v73 = *a2;
                (*(void (__fastcall **)(volatile signed __int32 *, __int128 *, __int64))(*(_QWORD *)*a2 + 40LL))(
                  *a2,
                  &v228,
                  4);
                if ( *((_DWORD *)v73 + 4) != 0 )
                  return 0;
                sub_140CD95D0(v223, &v228);
              }
              while ( ++v72 < v222 );
            }
            if ( *v13 <= 0xDC3u )
            {
              v74 = *a2;
              (*(void (__fastcall **)(volatile signed __int32 *, __int128 *, __int64))(*(_QWORD *)*a2 + 40LL))(
                *a2,
                &v228,
                4);
              if ( *((_DWORD *)v74 + 4) != 0 )
                return 0;
              sub_141011F70(*(_QWORD *)(a1 + 368) + 344LL, (int)v228);
              if ( (int)v228 > 0 )
              {
                v75 = 0;
                do
                {
                  v76 = *a2;
                  (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
                    *a2,
                    v219,
                    4);
                  if ( *((_DWORD *)v76 + 4) != 0 )
                    return 0;
                  sub_140CD95D0(*(_QWORD *)(a1 + 368) + 344LL, v219);
                }
                while ( ++v75 < (int)v228 );
              }
            }
            v77 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              &v220,
              2);
            if ( *((_DWORD *)v77 + 4) != 0 )
              return 0;
            sub_140893BE0(*(_QWORD *)(a1 + 1256), v220);
            if ( v220 > 0 )
            {
              v78 = 0;
              while ( 1 )
              {
                v79 = (void (__fastcall ***)(_QWORD, __int64))sub_141750CC0(112);
                sub_141570A20(v79);
                *(_QWORD *)&v228 = v79;
                if ( (unsigned __int8)sub_141571860(v79, a2) == 0 )
                  break;
                sub_14087F540(*(_QWORD *)(a1 + 1256), &v228);
                if ( ++v78 >= v220 )
                  goto LABEL_109;
              }
              (**v79)(v79, 1);
              return 0;
            }
LABEL_109:
            v80 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              &v220,
              2);
            if ( *((_DWORD *)v80 + 4) != 0 )
              return 0;
            sub_140893BE0(*(_QWORD *)(a1 + 1264), v220);
            if ( v220 > 0 )
            {
              for ( j = 0; j < v220; ++j )
              {
                v82 = (void (__fastcall ***)(_QWORD, __int64))sub_141750CC0(112);
                sub_141570A20(v82);
                *(_QWORD *)&v228 = v82;
                if ( (unsigned __int8)sub_141571860(v82, a2) != 0 )
                  sub_14087F540(*(_QWORD *)(a1 + 1264), &v228);
                else
                  (**v82)(v82, 1);
              }
            }
            if ( *v13 < 0xDC4u )
            {
              v83 = *a2;
              (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
                *a2,
                v219,
                2);
              if ( *((_DWORD *)v83 + 4) != 0 )
                return 0;
              sub_140893BE0(*(_QWORD *)(*(_QWORD *)(a1 + 368) + 368LL), v219[0]);
              if ( v219[0] > 0 )
              {
                v84 = 0;
                do
                {
                  v85 = sub_1410415F0(56);
                  *(_QWORD *)v85 = 0;
                  *(_QWORD *)(v85 + 8) = 0;
                  *(_QWORD *)(v85 + 16) = 0;
                  *(_QWORD *)(v85 + 24) = 0;
                  *(_DWORD *)(v85 + 32) = 124518401;
                  *(_QWORD *)(v85 + 36) = -1;
                  *(_QWORD *)(v85 + 44) = -1;
                  *(_QWORD *)&v228 = v85;
                  if ( (unsigned __int8)sub_1415CFD70(v85, a2) == 0 )
                    return 0;
                  sub_14087F540(*(_QWORD *)(*(_QWORD *)(a1 + 368) + 368LL), &v228);
                }
                while ( ++v84 < v219[0] );
              }
            }
            v86 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v227, 1);
            if ( *((_DWORD *)v86 + 4) != 0 )
              return 0;
            if ( v227 != 0 )
            {
              v87 = *(_QWORD *)(a1 + 1272);
              if ( v87 != 0 )
              {
                sub_140B247F0(*(_QWORD *)(a1 + 1272));
                v88 = sub_1407E4940();
                sub_1407E4890(v88, v87, 24);
              }
              *(_QWORD *)(a1 + 1272) = 0;
              v89 = sub_1407E4940();
              v90 = (_QWORD *)sub_1407E4490(v89, 24);
              *v90 = 0;
              v90[1] = 0;
              v90[2] = 0;
              if ( qword_141ABD470 == 0 )
                qword_141ABD470 = sub_1407E4940();
              v90[2] = 0;
              v90[1] = 0;
              *v90 = 0;
              *(_QWORD *)(a1 + 1272) = v90;
              if ( (unsigned __int8)sub_14105FCB0(v90, a2) == 0 )
                return 0;
            }
            v91 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              &v226,
              2);
            if ( *((_DWORD *)v91 + 4) != 0 )
              return 0;
            sub_140893BE0(a1 + 1760, v226);
            if ( v226 > 0 )
            {
              v92 = 0;
              do
              {
                v93 = sub_141060080();
                *(_QWORD *)v93 = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
                *(_DWORD *)(v93 + 8) = 0;
                *(_BYTE *)(v93 + 12) = 1;
                *(_QWORD *)&v228 = v93;
                if ( (unsigned __int8)sub_141060130(v93, a2) == 0 )
                  return 0;
                if ( *(_QWORD *)v93 != 0 )
                  sub_14087F540(a1 + 1760, &v228);
                else
                  sub_1410601F0(v93);
              }
              while ( ++v92 < v226 );
            }
            sub_141073D90(&v228, a2, a1 + 1808);
            if ( (_DWORD)v228 != 0 )
              return 0;
            sub_141073D90(&v228, a2, a1 + 1784);
            if ( (_DWORD)v228 != 0 )
              return 0;
            if ( *v13 <= 0xDC3u )
            {
              v228 = 0;
              v229 = 0x76CFFFF01010000LL;
              *(_DWORD *)v219 = 0;
              v94 = *a2;
              (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
                *a2,
                v219,
                4);
              if ( *((_DWORD *)v94 + 4) != 0 )
                return 0;
              sub_1410416A0(*(_QWORD *)(a1 + 368) + 96LL, *(int *)v219);
              if ( *(int *)v219 > 0 )
              {
                v95 = 0;
                while ( (unsigned __int8)sub_14144C6A0(&v228, a2) != 0 )
                {
                  sub_140BA1B40(*(_QWORD *)(a1 + 368) + 96LL, &v228);
                  if ( ++v95 >= *(int *)v219 )
                    goto LABEL_148;
                }
                return 0;
              }
            }
LABEL_148:
            v228 = 0;
            v230 = 0;
            v229 = 0;
            v224 = 0;
            v96 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              &v224,
              2);
            if ( *((_DWORD *)v96 + 4) != 0 )
              return 0;
            sub_141060360(a1 + 192, v224);
            if ( v224 > 0 )
            {
              v97 = 0;
              while ( (unsigned __int8)sub_1410604A0(&v228, a2) != 0 )
              {
                sub_14103AF20(a1 + 192, &v228);
                if ( ++v97 >= v224 )
                  goto LABEL_153;
              }
              return 0;
            }
LABEL_153:
            if ( *v13 <= 0xDC3u )
            {
              sub_14104F0B0(v219, a2, *(_QWORD *)(a1 + 368) + 120LL, v232);
              if ( *(_DWORD *)v219 != 0 )
                return 0;
            }
            sub_141074100(v219, a2, a1 + 216);
            if ( *(_DWORD *)v219 != 0 )
              return 0;
            v98 = *a2;
            v99 = (char *)(a1 + 1152);
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              a1 + 1152,
              1);
            if ( *((_DWORD *)v98 + 4) != 0 )
              return 0;
            if ( *v99 <= 0 )
            {
              if ( *(_BYTE *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 8LL) == 0 )
                sub_141751038();
              v100 = *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex);
              v101 = *(_QWORD *)(v100 + 328);
              *(_QWORD *)(v100 + 328) = *(_QWORD *)(v100 + 336) + 0x5851F42D4C957F2DLL * v101;
              *v99 = ((5 * (unsigned __int64)(unsigned int)__ROR4__((v101 >> 27) ^ (v101 >> 45), v101 >> 59)) >> 32)
                   + 10;
            }
            v102 = *a2;
            v103 = (int *)(a1 + 1132);
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              a1 + 1132,
              4);
            if ( *((_DWORD *)v102 + 4) != 0 )
              return 0;
            if ( *v103 >= 3001 )
              *v103 = -1;
            v104 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              v219,
              1);
            if ( *((_DWORD *)v104 + 4) != 0 )
              return 0;
            if ( LOBYTE(v219[0]) != 0 )
            {
              v105 = (_QWORD *)sub_141750CC0(24);
              if ( qword_141ABD470 == 0 )
                qword_141ABD470 = sub_1407E4940();
              v105[2] = 0;
              v105[1] = 0;
              *v105 = 0;
              *(_QWORD *)(a1 + 392) = v105;
              if ( (unsigned __int8)sub_14155BE50(v105, a2) == 0 )
                return 0;
            }
            goto LABEL_169;
          }
        }
      }
      v52 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v221, 2);
      if ( *((_DWORD *)v52 + 4) == 0 )
      {
        sub_140893BE0(*(_QWORD *)(a1 + 368) + 296LL, v221);
        if ( v221 > 0 )
        {
          v53 = 0;
          while ( 1 )
          {
            *(_QWORD *)&v228 = 0;
            v54 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int128 *, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              &v228,
              4);
            if ( *((_DWORD *)v54 + 4) != 0 )
              return 0;
            sub_14087F540(*(_QWORD *)(a1 + 368) + 296LL, &v228);
            if ( ++v53 >= v221 )
              goto LABEL_67;
          }
        }
        goto LABEL_67;
      }
    }
    return 0;
  }
LABEL_169:
  v106 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 360, 4);
  if ( *((_DWORD *)v106 + 4) != 0 )
    return 0;
  if ( *v13 <= 0xDC3u )
  {
    v107 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)(a1 + 368) + 460LL,
      1);
    if ( *((_DWORD *)v107 + 4) != 0 )
      return 0;
  }
  v108 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1949, 1);
  if ( *((_DWORD *)v108 + 4) != 0 )
    return 0;
  v109 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1950, 1);
  if ( *((_DWORD *)v109 + 4) != 0 )
    return 0;
  v110 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1951, 1);
  if ( *((_DWORD *)v110 + 4) != 0 )
    return 0;
  v111 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1952, 1);
  if ( *((_DWORD *)v111 + 4) != 0 )
    return 0;
  v112 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1953, 1);
  if ( *((_DWORD *)v112 + 4) != 0 )
    return 0;
  if ( *v13 <= 0xDC3u )
  {
    v115 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)(a1 + 368) + 464LL,
      1);
    if ( *((_DWORD *)v115 + 4) != 0 )
      return 0;
    v116 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)(a1 + 368) + 461LL,
      1);
    if ( *((_DWORD *)v116 + 4) != 0 )
      return 0;
  }
  v117 = *a2;
  v118 = (_BYTE *)(a1 + 1956);
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1956, 1);
  if ( *((_DWORD *)v117 + 4) != 0 )
    return 0;
  if ( *v118 == 0 )
    *v118 = 21;
  v119 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1955, 1);
  if ( *((_DWORD *)v119 + 4) != 0 )
    return 0;
  v120 = a1 + 368;
  v121 = *a2;
  if ( *v13 < 0xDC4u )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v121 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 459LL,
      1);
    if ( *((_DWORD *)v121 + 4) != 0 )
      return 0;
    v214 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 240LL,
      4);
    if ( *((_DWORD *)v214 + 4) != 0 )
      return 0;
    v215 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 248LL,
      4);
    if ( *((_DWORD *)v215 + 4) != 0 )
      return 0;
    v216 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 232LL,
      4);
    if ( *((_DWORD *)v216 + 4) != 0 )
      return 0;
    v217 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 256LL,
      4);
    if ( *((_DWORD *)v217 + 4) != 0 )
      return 0;
  }
  else
  {
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v121 + 40LL))(*a2, a1 + 368, 4);
    if ( *((_DWORD *)v121 + 4) != 0 )
      return 0;
  }
  v122 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1936, 1);
  if ( *((_DWORD *)v122 + 4) != 0 )
    return 0;
  v123 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1937, 1);
  if ( *((_DWORD *)v123 + 4) != 0 )
    return 0;
  v124 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1938, 1);
  if ( *((_DWORD *)v124 + 4) != 0 )
    return 0;
  v125 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1939, 1);
  if ( *((_DWORD *)v125 + 4) != 0 )
    return 0;
  v126 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1940, 1);
  if ( *((_DWORD *)v126 + 4) != 0 )
    return 0;
  v127 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1941, 1);
  if ( *((_DWORD *)v127 + 4) != 0 )
    return 0;
  v128 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1942, 1);
  if ( *((_DWORD *)v128 + 4) != 0 )
    return 0;
  v129 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1943, 1);
  if ( *((_DWORD *)v129 + 4) != 0 )
    return 0;
  v130 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1944, 1);
  if ( *((_DWORD *)v130 + 4) != 0 )
    return 0;
  v131 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1945, 1);
  if ( *((_DWORD *)v131 + 4) != 0 )
    return 0;
  v132 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1946, 1);
  if ( *((_DWORD *)v132 + 4) != 0 )
    return 0;
  v133 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1947, 1);
  if ( *((_DWORD *)v133 + 4) != 0 )
    return 0;
  if ( *v13 <= 0xDC3u )
  {
    v134 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 436LL,
      4);
    if ( *((_DWORD *)v134 + 4) != 0 )
      return 0;
  }
  v135 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1957, 1);
  if ( *((_DWORD *)v135 + 4) != 0 )
    return 0;
  v136 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1958, 1);
  if ( *((_DWORD *)v136 + 4) != 0 )
    return 0;
  v137 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1959, 1);
  if ( *((_DWORD *)v137 + 4) != 0 )
    return 0;
  v138 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1960, 1);
  if ( *((_DWORD *)v138 + 4) != 0 )
    return 0;
  if ( *v13 <= 0xDC3u )
  {
    v139 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
    if ( *((_DWORD *)v139 + 4) != 0 )
      return 0;
    sub_1410418B0(*(_QWORD *)v120 + 72LL, v218);
    if ( v218 > 0 )
    {
      v140 = 0;
      while ( (unsigned __int8)sub_141060550(&v235, a2) != 0 )
      {
        sub_1408C9770(*(_QWORD *)v120 + 72LL, &v235);
        if ( ++v140 >= v218 )
          goto LABEL_212;
      }
      return 0;
    }
  }
LABEL_212:
  v141 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
  if ( *((_DWORD *)v141 + 4) != 0 )
    return 0;
  v223 = a1 + 240;
  sub_1410418B0(a1 + 240, v218);
  if ( v218 > 0 )
  {
    v142 = 0;
    do
    {
      LODWORD(v228) = 17706258;
      BYTE4(v228) = 0;
      *((_QWORD *)&v228 + 1) = 0;
      if ( (unsigned __int8)sub_14141D4A0(&v228, a2) == 0 )
        return 0;
      sub_1408C9770(v223, &v228);
    }
    while ( ++v142 < v218 );
  }
  v143 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
  if ( *((_DWORD *)v143 + 4) != 0 )
    return 0;
  v223 = a1 + 264;
  sub_1410418B0(a1 + 264, v218);
  if ( v218 > 0 )
  {
    v144 = 0;
    do
    {
      LODWORD(v228) = 17706258;
      *((_QWORD *)&v228 + 1) = 0;
      if ( (unsigned __int8)sub_14141D570(&v228, a2) == 0 )
        return 0;
      sub_1408C9770(v223, &v228);
    }
    while ( ++v144 < v218 );
  }
  v145 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v218, 1);
  if ( *((_DWORD *)v145 + 4) != 0 )
    return 0;
  v223 = a1 + 288;
  sub_1410418B0(a1 + 288, v218);
  if ( v218 > 0 )
  {
    v146 = 0;
    do
    {
      LODWORD(v228) = 17706258;
      *((_QWORD *)&v228 + 1) = 0;
      if ( (unsigned __int8)sub_14141D570(&v228, a2) == 0 )
        return 0;
      sub_1408C9770(v223, &v228);
    }
    while ( ++v146 < v218 );
  }
  if ( *v13 <= 0xDC3u )
  {
    v147 = *(_QWORD *)(*(_QWORD *)v120 + 72LL);
    if ( *(_QWORD *)(*(_QWORD *)v120 + 80LL) - v147 == 16 )
      *(_BYTE *)(v147 + 8) = 100;
    v148 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v231, 4);
    if ( *((_DWORD *)v148 + 4) != 0 )
      return 0;
    sub_140893BE0(*(_QWORD *)v120 + 168LL, v231);
    if ( v231 > 0 )
    {
      v149 = 0;
      do
      {
        v150 = (_QWORD *)sub_141750CC0(48);
        *v150 = 0;
        v150[1] = 0;
        v150[2] = 0;
        v150[3] = 0;
        v150[4] = 0;
        v150[5] = 0x76C0001076C0001LL;
        *(_QWORD *)&v228 = v150;
        if ( (unsigned __int8)sub_1415CFEA0(v150, a2) == 0 )
          return 0;
        sub_14087F540(*(_QWORD *)v120 + 168LL, &v228);
      }
      while ( ++v149 < v231 );
    }
    v151 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v225, 4);
    if ( *((_DWORD *)v151 + 4) != 0 )
      return 0;
    sub_140893BE0(*(_QWORD *)v120 + 144LL, v225);
    if ( v225 > 0 )
    {
      v152 = 0;
      do
      {
        v153 = (_QWORD *)sub_141750CC0(48);
        *v153 = 0;
        v153[1] = 0;
        v153[2] = 0;
        v153[3] = 0;
        v153[4] = 0;
        v153[5] = 0x76C0001076C0001LL;
        *(_QWORD *)&v228 = v153;
        if ( (unsigned __int8)sub_1415CFEA0(v153, a2) == 0 )
          return 0;
        sub_14087F540(*(_QWORD *)v120 + 144LL, &v228);
      }
      while ( ++v152 < v225 );
    }
    v154 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v219, 4);
    if ( *((_DWORD *)v154 + 4) != 0 )
      return 0;
    sub_1410418B0(*(_QWORD *)v120 + 192LL, *(int *)v219);
    if ( *(int *)v219 > 0 )
    {
      v155 = 0;
      do
      {
        *(_QWORD *)&v228 = 0;
        *((_QWORD *)&v228 + 1) = 0x76C0001076C0001LL;
        if ( (unsigned __int8)sub_1410605B0(&v228, a2) == 0 )
          return 0;
        sub_1410419F0(*(_QWORD *)v120 + 192LL, &v228, v155++);
      }
      while ( v155 < *(int *)v219 );
    }
  }
  v156 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1924, 2);
  if ( *((_DWORD *)v156 + 4) != 0 )
    return 0;
  v157 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1926, 2);
  if ( *((_DWORD *)v157 + 4) != 0 )
    return 0;
  v158 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1928, 2);
  if ( *((_DWORD *)v158 + 4) != 0 )
    return 0;
  v159 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1932, 2);
  if ( *((_DWORD *)v159 + 4) != 0 )
    return 0;
  if ( v11 == 0 )
    goto LABEL_316;
  if ( *v13 <= 0xDC3u )
  {
    v160 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 420LL,
      4);
    if ( *((_DWORD *)v160 + 4) != 0 )
      return 0;
    v161 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 424LL,
      4);
    if ( *((_DWORD *)v161 + 4) != 0 )
      return 0;
    v162 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 432LL,
      4);
    if ( *((_DWORD *)v162 + 4) != 0 )
      return 0;
    v163 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 428LL,
      4);
    if ( *((_DWORD *)v163 + 4) != 0 )
      return 0;
    v164 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 440LL,
      4);
    if ( *((_DWORD *)v164 + 4) != 0 )
      return 0;
    v165 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 444LL,
      4);
    if ( *((_DWORD *)v165 + 4) != 0 )
      return 0;
    v166 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 448LL,
      4);
    if ( *((_DWORD *)v166 + 4) != 0 )
      return 0;
    v167 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 452LL,
      4);
    if ( *((_DWORD *)v167 + 4) != 0 )
      return 0;
  }
  v168 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1856, 4);
  if ( *((_DWORD *)v168 + 4) != 0 )
    return 0;
  v169 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1860, 4);
  if ( *((_DWORD *)v169 + 4) != 0 )
    return 0;
  v170 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1864, 4);
  if ( *((_DWORD *)v170 + 4) != 0 )
    return 0;
  v171 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1868, 4);
  if ( *((_DWORD *)v171 + 4) != 0 )
    return 0;
  v172 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1872, 4);
  if ( *((_DWORD *)v172 + 4) != 0 )
    return 0;
  v173 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1876, 4);
  if ( *((_DWORD *)v173 + 4) != 0 )
    return 0;
  v174 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1880, 4);
  if ( *((_DWORD *)v174 + 4) != 0 )
    return 0;
  v175 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1147, 1);
  if ( *((_DWORD *)v175 + 4) != 0 )
    return 0;
  if ( *v13 <= 0xDC3u )
  {
    v176 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 380LL,
      4);
    if ( *((_DWORD *)v176 + 4) != 0 )
      return 0;
    v177 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
      *a2,
      *(_QWORD *)v120 + 384LL,
      4);
    if ( *((_DWORD *)v177 + 4) != 0 )
      return 0;
  }
  v178 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 420, 4);
  if ( *((_DWORD *)v178 + 4) != 0 )
    return 0;
  v179 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1886, 1);
  if ( *((_DWORD *)v179 + 4) != 0 )
    return 0;
  v180 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1884, 2);
  if ( *((_DWORD *)v180 + 4) != 0 )
    return 0;
  v181 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1887, 1);
  if ( *((_DWORD *)v181 + 4) != 0 )
    return 0;
  v182 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v219, 1);
  if ( *((_DWORD *)v182 + 4) != 0 )
    return 0;
  if ( LOBYTE(v219[0]) != 0 )
  {
    *(_QWORD *)(a1 + 1080) = sub_141750CC0(80);
    v223 = 0;
    v183 = 0;
    do
    {
      v184 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        v223 + *(_QWORD *)(a1 + 1080),
        4);
      if ( *((_DWORD *)v184 + 4) != 0 )
        return 0;
      ++v183;
      v223 += 4;
    }
    while ( v183 < LOBYTE(v219[0]) );
  }
  v185 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v222, 1);
  if ( *((_DWORD *)v185 + 4) != 0 )
    return 0;
  if ( (_BYTE)v222 != 0 )
  {
    *(_QWORD *)(a1 + 1088) = sub_141750CC0(80);
    v223 = 0;
    v186 = 0;
    do
    {
      v187 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        v223 + *(_QWORD *)(a1 + 1088),
        4);
      if ( *((_DWORD *)v187 + 4) != 0 )
        return 0;
      ++v186;
      v223 += 4;
    }
    while ( v186 < (unsigned __int8)v222 );
  }
  v188 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v220, 1);
  if ( *((_DWORD *)v188 + 4) != 0 )
    return 0;
  if ( (_BYTE)v220 != 0 )
  {
    *(_QWORD *)(a1 + 1096) = sub_141750CC0(80);
    v223 = 0;
    v189 = 0;
    do
    {
      v190 = *a2;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
        *a2,
        v223 + *(_QWORD *)(a1 + 1096),
        4);
      if ( *((_DWORD *)v190 + 4) != 0 )
        return 0;
      ++v189;
      v223 += 4;
    }
    while ( v189 < (unsigned __int8)v220 );
  }
  if ( *v13 <= 0xDC3u )
  {
    v225 = 0;
    v191 = *a2;
    (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v225, 4);
    if ( *((_DWORD *)v191 + 4) != 0 )
      return 0;
    if ( v225 != 0 )
    {
      v192 = 0;
      do
      {
        LODWORD(v228) = 0;
        *(_QWORD *)((char *)&v228 + 4) = 0x76C0001076C0001LL;
        v193 = *a2;
        (*(void (__fastcall **)(volatile signed __int32 *, __int128 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v228, 4);
        if ( *((_DWORD *)v193 + 4) != 0
          || (unsigned __int8)sub_140DB8980((char *)&v228 + 4, a2) == 0
          || (unsigned __int8)sub_140DB8980((char *)&v228 + 8, a2) == 0 )
        {
          return 0;
        }
        sub_141041800(*(_QWORD *)v120 + 216LL, &v231, *(_QWORD *)(*(_QWORD *)v120 + 216LL), &v228);
      }
      while ( ++v192 < (unsigned __int64)(unsigned int)v225 );
    }
  }
  v194 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1961, 1);
  if ( *((_DWORD *)v194 + 4) != 0 )
    return 0;
  v195 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1962, 1);
  if ( *((_DWORD *)v195 + 4) != 0 )
    return 0;
  v196 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1963, 1);
  if ( *((_DWORD *)v196 + 4) != 0 )
    return 0;
  v197 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1964, 1);
  if ( *((_DWORD *)v197 + 4) != 0 )
    return 0;
  v198 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1965, 1);
  if ( *((_DWORD *)v198 + 4) != 0 )
    return 0;
  v199 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1966, 1);
  if ( *((_DWORD *)v199 + 4) != 0 )
    return 0;
  v200 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1967, 1);
  if ( *((_DWORD *)v200 + 4) != 0 )
    return 0;
  v201 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1968, 1);
  if ( *((_DWORD *)v201 + 4) != 0 )
    return 0;
  v202 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1969, 1);
  if ( *((_DWORD *)v202 + 4) != 0 )
    return 0;
  v203 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1970, 1);
  if ( *((_DWORD *)v203 + 4) != 0 )
    return 0;
  v204 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1971, 1);
  if ( *((_DWORD *)v204 + 4) != 0 )
    return 0;
  v205 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1972, 1);
  if ( *((_DWORD *)v205 + 4) != 0 )
    return 0;
  v206 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1973, 1);
  if ( *((_DWORD *)v206 + 4) != 0 )
    return 0;
  v207 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1888, 4);
  if ( *((_DWORD *)v207 + 4) != 0 )
    return 0;
  v208 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1892, 4);
  if ( *((_DWORD *)v208 + 4) != 0 )
    return 0;
  v209 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1930, 2);
  if ( *((_DWORD *)v209 + 4) != 0 )
    return 0;
  v210 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1948, 1);
  if ( *((_DWORD *)v210 + 4) != 0 )
    return 0;
  v211 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1954, 1);
  if ( *((_DWORD *)v211 + 4) != 0 )
    return 0;
  v212 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 1934, 2);
  if ( *((_DWORD *)v212 + 4) != 0 )
    return 0;
LABEL_316:
  v113 = 0;
  if ( (unsigned __int8)sub_1411D1730(a1, a2, 0, a4, a5, a6, v11, a8) != 0 )
  {
    LOBYTE(v113) = 1;
    if ( *v13 <= 0xDC3u )
    {
      sub_141041A50(*(_QWORD *)(a1 + 368));
      *(_DWORD *)(*(_QWORD *)(a1 + 368) + 12LL) = *(_DWORD *)(a1 + 12);
      v213 = *(_DWORD *)(a1 + 16);
      if ( v213 == 0 )
        v213 = *(_DWORD *)(a1 + 12);
      *(_DWORD *)(*(_QWORD *)(a1 + 368) + 16LL) = v213;
      sub_140FA1340(*(_QWORD *)(a4 + 40), *(_QWORD *)(a1 + 368));
      *(_QWORD *)(a1 + 368) = *(int *)(*(_QWORD *)(a1 + 368) + 8LL);
    }
  }
  return v113;
}
