__int64 __fastcall sub_1411D1730(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        char a7,
        __int64 a8)
{
  volatile signed __int32 *v10; // rax
  __int64 v11; // r9
  __int64 *v12; // rsi
  __int64 v13; // r8
  __int64 v14; // rax
  __int64 v15; // r8
  unsigned __int8 *v16; // rbx
  __int64 v17; // r8
  __int64 v18; // rax
  _BYTE *v19; // rbx
  bool v20; // zf
  __int64 v21; // r8
  __int64 v22; // r8
  __int64 v23; // rdx
  __int64 v24; // rcx
  __int64 v25; // rcx
  __int64 v26; // rdi
  __int64 v27; // rax
  __int64 v28; // rcx
  unsigned __int64 v29; // rbx
  unsigned __int64 v30; // rdx
  unsigned __int64 v31; // rsi
  __int64 v32; // r12
  __int64 v33; // rbx
  unsigned __int64 v34; // rcx
  __int64 v35; // r8
  __int64 v36; // r14
  bool v37; // al
  volatile signed __int32 **v38; // rsi
  volatile signed __int32 *v39; // rax
  volatile signed __int32 *v40; // rcx
  volatile signed __int32 *v41; // rbx
  volatile signed __int32 *v42; // rbx
  unsigned __int64 v43; // rdi
  __int64 v44; // rsi
  unsigned __int8 v45; // al
  __int64 v46; // rcx
  __int64 v47; // rsi
  unsigned __int64 v48; // rdi
  __int64 v49; // r8
  __int64 v50; // r14
  unsigned __int8 *v51; // rax
  __int64 v52; // r8
  __int64 v53; // rdi
  __int64 v54; // rax
  __int64 v55; // rcx
  unsigned __int64 v56; // rbx
  unsigned __int64 v57; // rdx
  unsigned __int64 v58; // rsi
  __int64 v59; // r12
  __int64 v60; // rbx
  unsigned __int64 v61; // rcx
  __int64 v62; // r8
  __int64 v63; // r14
  bool v64; // al
  unsigned __int64 v65; // rdi
  __int64 v66; // rsi
  unsigned __int8 v67; // al
  __int64 v68; // rcx
  __int64 v69; // rsi
  unsigned __int64 v70; // rdi
  __int64 v71; // r8
  __int64 v72; // r14
  unsigned __int8 *v73; // rax
  __int64 v74; // r8
  __int64 v75; // rdi
  __int64 v76; // rax
  __int64 v77; // rcx
  unsigned __int64 v78; // rbx
  unsigned __int64 v79; // rdx
  unsigned __int64 v80; // rsi
  __int64 v81; // r14
  __int64 v82; // rdx
  unsigned __int64 v83; // rdi
  __int64 v84; // rsi
  char v85; // al
  __int64 v86; // rcx
  __int64 v87; // rsi
  __int64 v88; // rdi
  __int64 v89; // r8
  __int64 v90; // rbx
  __int64 v91; // r8
  __int64 v92; // rdi
  __int64 v93; // rax
  __int64 v94; // rcx
  unsigned __int64 v95; // rbx
  unsigned __int64 v96; // rdx
  unsigned __int64 v97; // rsi
  __int64 v98; // r14
  __int64 v99; // rdx
  unsigned __int64 v100; // rdi
  __int64 v101; // rsi
  signed __int8 v102; // al
  __int64 v103; // rcx
  __int64 v104; // rsi
  __int64 v105; // rdi
  __int64 v106; // r8
  __int64 v107; // rbx
  __int64 v108; // r8
  __int64 v109; // rdi
  __int64 v110; // rax
  __int64 v111; // rcx
  unsigned __int64 v112; // rbx
  unsigned __int64 v113; // rdx
  unsigned __int64 v114; // rsi
  __int64 v115; // r14
  __int64 v116; // rdx
  unsigned __int64 v117; // rdi
  __int64 v118; // rsi
  unsigned __int8 v119; // al
  __int64 v120; // rcx
  __int64 v121; // rsi
  unsigned __int64 v122; // rdi
  __int64 v123; // r8
  __int64 v124; // rbx
  __int64 v125; // r8
  __int64 *v126; // r14
  unsigned __int8 v127; // al
  __int64 v128; // r8
  unsigned __int8 *v129; // rcx
  __int64 v130; // r15
  unsigned __int64 v131; // rdi
  __int64 v132; // rsi
  __int64 v133; // rbx
  __int64 v134; // r12
  __int64 v135; // r8
  __int64 *v136; // rdi
  void *v137; // rcx
  __int16 v138; // ax
  __int64 v139; // r14
  __int64 v140; // r15
  unsigned __int64 v141; // rdx
  __int64 v142; // rbx
  __int64 v143; // r12
  unsigned __int64 v144; // rcx
  __int64 v145; // r8
  __int64 v146; // rcx
  bool v147; // al
  int v148; // r15d
  __int64 v149; // rdi
  volatile signed __int32 *v150; // rsi
  volatile signed __int32 *v151; // rsi
  volatile signed __int32 *v152; // rbx
  int v153; // esi
  _WORD *v154; // r14
  volatile signed __int32 *v155; // rsi
  volatile signed __int32 *v156; // rsi
  int v157; // ebx
  volatile signed __int32 *v158; // rsi
  __int64 **v159; // r14
  __int64 *v160; // rbx
  __int64 v161; // r12
  unsigned __int64 v162; // rax
  unsigned __int64 v163; // r15
  unsigned __int64 v164; // rcx
  unsigned __int64 v165; // r15
  __int64 *v166; // rdi
  __int64 *v167; // rdi
  unsigned __int64 v168; // rcx
  __int64 v169; // rbx
  __int64 v170; // rbx
  bool v171; // al
  volatile signed __int32 *v172; // rdi
  unsigned int *v173; // rbx
  __int64 v174; // r8
  volatile signed __int32 *v175; // rcx
  __int64 v177; // rax
  volatile signed __int32 *v178; // rcx
  volatile signed __int32 *v179; // rdi
  volatile signed __int32 *v180; // rdi
  __int64 v181; // rcx
  __int64 v182; // rcx
  __int64 v183; // [rsp+48h] [rbp-38h]
  int v184; // [rsp+48h] [rbp-38h]
  __int64 v185; // [rsp+50h] [rbp-30h] BYREF
  int v186; // [rsp+58h] [rbp-28h] BYREF
  char v187; // [rsp+5Fh] [rbp-21h] BYREF
  __int64 v188; // [rsp+60h] [rbp-20h] BYREF
  unsigned __int8 v189; // [rsp+6Eh] [rbp-12h] BYREF
  unsigned __int8 v190; // [rsp+6Fh] [rbp-11h] BYREF
  volatile signed __int32 *v191; // [rsp+70h] [rbp-10h] BYREF
  unsigned __int8 *v192; // [rsp+78h] [rbp-8h]
  __int64 v193; // [rsp+80h] [rbp+0h]
  unsigned __int8 *v194; // [rsp+88h] [rbp+8h]
  __int64 v195; // [rsp+90h] [rbp+10h]

  v195 = -2;
  v10 = *a2;
  v191 = v10;
  if ( v10 != nullptr )
    _InterlockedIncrement(v10 + 2);
  v192 = (unsigned __int8 *)&v187;
  v193 = 1;
  v194 = (unsigned __int8 *)&v188;
  sub_1412E70A0(&v191);
  v12 = (__int64 *)(a1 + 186);
  *(_BYTE *)(a1 + 186) = v187;
  if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDC3u )
  {
    v13 = v193;
    if ( v194 == (unsigned __int8 *)&v185 )
    {
      v14 = ++v193;
      v194 = (unsigned __int8 *)&v185 + 1;
      if ( (__int64 *)((char *)&v185 + 1) == &v188 )
      {
        v20 = v13 == -2;
        v15 = v13 + 2;
        v193 = v15;
        v194 = (unsigned __int8 *)&v188 + 1;
        if ( v20 )
        {
LABEL_22:
          v194 = nullptr;
          v193 = 0;
          v192 = nullptr;
          if ( *(_BYTE *)v12 == 0 )
          {
            *(_BYTE *)(a1 + 356) = v185;
            *(_BYTE *)(a1 + 357) = v188;
          }
          v16 = (unsigned __int8 *)(a1 + 184);
          goto LABEL_25;
        }
LABEL_20:
        if ( v191 != nullptr )
          (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
            v191,
            v192,
            v15);
        goto LABEL_22;
      }
      if ( v13 == -1 )
        goto LABEL_18;
    }
    else
    {
      if ( v193 != 0 && v191 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
          v191,
          v192,
          v193);
      v192 = (unsigned __int8 *)&v185;
      v193 = 1;
      v194 = (unsigned __int8 *)&v185 + 1;
      v14 = 1;
      if ( (__int64 *)((char *)&v185 + 1) == &v188 )
      {
        v193 = 2;
        v15 = 2;
LABEL_19:
        v194 = (unsigned __int8 *)&v188 + 1;
        goto LABEL_20;
      }
    }
    if ( v191 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
        v191,
        v192,
        v14);
LABEL_18:
    v192 = (unsigned __int8 *)&v188;
    v193 = 1;
    v15 = 1;
    goto LABEL_19;
  }
  v16 = (unsigned __int8 *)(a1 + 184);
  if ( v194 != (unsigned __int8 *)(a1 + 184) )
  {
LABEL_25:
    if ( v193 != 0 && v191 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(v191, v192);
    v192 = v16;
    v193 = 1;
    v19 = (_BYTE *)(a1 + 185);
    v194 = (unsigned __int8 *)(a1 + 185);
    if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDC4u )
    {
      v193 = 2;
      v194 = (unsigned __int8 *)(a1 + 186);
      v21 = 2;
      goto LABEL_30;
    }
    v185 = 0;
    v188 = 0;
    v18 = 1;
LABEL_42:
    if ( v191 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
        v191,
        v192,
        v18);
    goto LABEL_44;
  }
  v17 = v193;
  v18 = ++v193;
  v19 = (_BYTE *)(a1 + 185);
  v194 = (unsigned __int8 *)(a1 + 185);
  if ( *(unsigned __int16 *)(a4 + 1416) > 0xDC3u )
  {
    v20 = v17 == -2;
    v21 = v17 + 2;
    v193 = v21;
    v194 = (unsigned __int8 *)(a1 + 186);
    if ( v20 )
    {
LABEL_32:
      v194 = nullptr;
      v193 = 0;
      v192 = nullptr;
      if ( *v19 != 0 && (unsigned __int8)sub_140087030() == 0 )
        *v19 = 0;
      goto LABEL_35;
    }
LABEL_30:
    if ( v191 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
        v191,
        v192,
        v21);
    goto LABEL_32;
  }
  v185 = 0;
  v188 = 0;
  if ( v18 != 0 )
    goto LABEL_42;
LABEL_44:
  v194 = nullptr;
  v193 = 0;
  v192 = nullptr;
  sub_140814B10(v191, &v186, &v185);
  if ( v186 == 0 )
  {
    if ( v193 != 0 && v191 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(v191, v192);
    v194 = nullptr;
    v193 = 0;
    v192 = nullptr;
    sub_140814B10(v191, &v186, &v188);
    if ( v186 == 0 )
    {
      if ( *(_BYTE *)v12 == 0 )
      {
        v38 = (volatile signed __int32 **)(a1 + 192);
        if ( (__int64 *)(a1 + 192) != &v185 )
        {
          v23 = v185;
          v39 = *v38;
          v40 = *v38 - 1;
          if ( *v38 == nullptr )
            v40 = nullptr;
          v41 = (volatile signed __int32 *)(v185 - 4);
          if ( v185 != 0 )
          {
            if ( v39 != nullptr && _InterlockedDecrement(v40) == 0 )
              sub_1412EC9A0(v40, v23);
            *v38 = nullptr;
            _InterlockedIncrement(v41);
            v42 = v41 + 1;
          }
          else
          {
            if ( v39 != nullptr && _InterlockedDecrement(v40) == 0 )
              sub_1412EC9A0(v40, v23);
            v42 = nullptr;
          }
          *v38 = v42;
        }
        v12 = (__int64 *)(a1 + 200);
        if ( (__int64 *)(a1 + 200) != &v188 )
        {
          v23 = v188;
          v177 = *v12;
          v178 = (volatile signed __int32 *)(*v12 - 4);
          if ( *v12 == 0 )
            v178 = nullptr;
          v179 = (volatile signed __int32 *)(v188 - 4);
          if ( v188 != 0 )
          {
            if ( v177 != 0 && _InterlockedDecrement(v178) == 0 )
              sub_1412EC9A0(v178, v23);
            *v12 = 0;
            _InterlockedIncrement(v179);
            v180 = v179 + 1;
          }
          else
          {
            if ( v177 != 0 && _InterlockedDecrement(v178) == 0 )
              sub_1412EC9A0(v178, v23);
            v180 = nullptr;
          }
          *v12 = (__int64)v180;
        }
      }
      if ( v193 != 0 && v191 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(v191, v192);
      v194 = nullptr;
      v193 = 0;
      v192 = nullptr;
      v181 = v188;
      if ( v188 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v188 - 4)) == 0 )
        sub_1412EC9A0(v181 - 4, v23);
      v182 = v185;
      if ( v185 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v185 - 4)) == 0 )
        sub_1412EC9A0(v182 - 4, v23);
LABEL_35:
      if ( a7 != 0 )
      {
        if ( v194 == (unsigned __int8 *)&v188 )
        {
          v22 = v193 + 1;
        }
        else
        {
          if ( v193 != 0 && v191 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
              v191,
              v192,
              v193);
          v192 = (unsigned __int8 *)&v188;
          v22 = 1;
        }
        v193 = v22;
        v194 = (unsigned __int8 *)&v188 + 1;
        sub_1412E70A0(&v191);
        v26 = (unsigned __int8)v188;
        v27 = *(_QWORD *)(a1 + 24);
        v28 = *(_QWORD *)(a1 + 32);
        v29 = (v28 - v27) >> 3;
        if ( v29 <= (unsigned __int8)v188 )
        {
          if ( v29 < (unsigned __int8)v188 )
          {
            v30 = (*(_QWORD *)(a1 + 40) - v27) >> 3;
            if ( v30 >= (unsigned __int8)v188 )
            {
              v43 = (unsigned __int8)v188 - v29;
              v44 = v28 + 8 * v43;
              sub_141758A10(v28, 0, 8 * v43);
              *(_QWORD *)(a1 + 32) = v44;
            }
            else
            {
              v31 = v30 + (v30 >> 1);
              if ( v31 <= (unsigned __int8)v188 )
                v31 = (unsigned __int8)v188;
              v32 = sub_1407E4490(qword_141ABD470, 8 * v31);
              sub_141758A10(v32 + 8 * v29, 0, 8 * (v26 - v29));
              sub_141758A00(v32, *(_QWORD *)(a1 + 24), *(_QWORD *)(a1 + 32) - *(_QWORD *)(a1 + 24));
              v33 = *(_QWORD *)(a1 + 24);
              if ( v33 != 0 )
              {
                v34 = *(_QWORD *)(a1 + 40) - v33;
                if ( v34 == -1 )
                  v34 = *(unsigned int *)(v33 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v35 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v35) >> 3 > v34)
                  && (v36 = *(_QWORD *)(v35 + 8 * v34)) != 0 )
                {
                  MEMORY[0x1419475D8](v36 + 32, v33 - *(unsigned int *)(v36 + 120));
                  v37 = *(_BYTE *)(v36 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 64)) != 0;
                  if ( !v37 && *(_BYTE *)(v36 + 97) != 0 )
                    sub_1412D33C0(v36);
                }
                else
                {
                  MEMORY[0x141948990](v33 - *(unsigned int *)(qword_141ABD470 + 48));
                }
              }
              *(_QWORD *)(a1 + 24) = v32;
              *(_QWORD *)(a1 + 32) = v32 + 8 * v26;
              *(_QWORD *)(a1 + 40) = v32 + 8 * v31;
            }
          }
        }
        else
        {
          *(_QWORD *)(a1 + 32) = v27 + 8LL * (unsigned __int8)v188;
        }
        v45 = v188;
        if ( (_BYTE)v188 != 0 )
        {
          v46 = (__int64)v194;
          v47 = 0;
          v48 = 0;
          do
          {
            v50 = *(_QWORD *)(a1 + 24);
            if ( v50 + v47 == v46 )
            {
              v49 = v193 + 4;
            }
            else
            {
              if ( v193 != 0 && v191 != nullptr )
              {
                (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
                  v191,
                  v192,
                  v193);
                v45 = v188;
              }
              v192 = (unsigned __int8 *)(v50 + v47);
              v49 = 4;
            }
            v193 = v49;
            v46 = v50 + 8 * v48 + 4;
            v194 = (unsigned __int8 *)(v50 + v47 + 4);
            ++v48;
            v47 += 8;
          }
          while ( v48 < v45 );
          v51 = (unsigned __int8 *)(v50 + v47 - 4);
        }
        else
        {
          v51 = v194;
        }
        if ( v51 == (unsigned __int8 *)&v188 )
        {
          v52 = v193 + 1;
        }
        else
        {
          if ( v193 != 0 && v191 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
              v191,
              v192,
              v193);
          v192 = (unsigned __int8 *)&v188;
          v52 = 1;
        }
        v193 = v52;
        v194 = (unsigned __int8 *)&v188 + 1;
        sub_1412E70A0(&v191);
        v53 = (unsigned __int8)v188;
        v54 = *(_QWORD *)(a1 + 48);
        v55 = *(_QWORD *)(a1 + 56);
        v56 = (v55 - v54) >> 3;
        if ( v56 <= (unsigned __int8)v188 )
        {
          if ( v56 < (unsigned __int8)v188 )
          {
            v57 = (*(_QWORD *)(a1 + 64) - v54) >> 3;
            if ( v57 >= (unsigned __int8)v188 )
            {
              v65 = (unsigned __int8)v188 - v56;
              v66 = v55 + 8 * v65;
              sub_141758A10(v55, 0, 8 * v65);
              *(_QWORD *)(a1 + 56) = v66;
            }
            else
            {
              v58 = v57 + (v57 >> 1);
              if ( v58 <= (unsigned __int8)v188 )
                v58 = (unsigned __int8)v188;
              v59 = sub_1407E4490(qword_141ABD470, 8 * v58);
              sub_141758A10(v59 + 8 * v56, 0, 8 * (v53 - v56));
              sub_141758A00(v59, *(_QWORD *)(a1 + 48), *(_QWORD *)(a1 + 56) - *(_QWORD *)(a1 + 48));
              v60 = *(_QWORD *)(a1 + 48);
              if ( v60 != 0 )
              {
                v61 = *(_QWORD *)(a1 + 64) - v60;
                if ( v61 == -1 )
                  v61 = *(unsigned int *)(v60 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v62 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v62) >> 3 > v61)
                  && (v63 = *(_QWORD *)(v62 + 8 * v61)) != 0 )
                {
                  MEMORY[0x1419475D8](v63 + 32, v60 - *(unsigned int *)(v63 + 120));
                  v64 = *(_BYTE *)(v63 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v63 + 64)) != 0;
                  if ( !v64 && *(_BYTE *)(v63 + 97) != 0 )
                    sub_1412D33C0(v63);
                }
                else
                {
                  MEMORY[0x141948990](v60 - *(unsigned int *)(qword_141ABD470 + 48));
                }
              }
              *(_QWORD *)(a1 + 48) = v59;
              *(_QWORD *)(a1 + 56) = v59 + 8 * v53;
              *(_QWORD *)(a1 + 64) = v59 + 8 * v58;
            }
          }
        }
        else
        {
          *(_QWORD *)(a1 + 56) = v54 + 8LL * (unsigned __int8)v188;
        }
        v67 = v188;
        if ( (_BYTE)v188 != 0 )
        {
          v68 = (__int64)v194;
          v69 = 0;
          v70 = 0;
          do
          {
            v72 = *(_QWORD *)(a1 + 48);
            if ( v72 + v69 == v68 )
            {
              v71 = v193 + 4;
            }
            else
            {
              if ( v193 != 0 && v191 != nullptr )
              {
                (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
                  v191,
                  v192,
                  v193);
                v67 = v188;
              }
              v192 = (unsigned __int8 *)(v72 + v69);
              v71 = 4;
            }
            v193 = v71;
            v68 = v72 + 8 * v70 + 4;
            v194 = (unsigned __int8 *)(v72 + v69 + 4);
            ++v70;
            v69 += 8;
          }
          while ( v70 < v67 );
          v73 = (unsigned __int8 *)(v72 + v69 - 4);
        }
        else
        {
          v73 = v194;
        }
        if ( v73 == (unsigned __int8 *)&v186 )
        {
          v74 = v193 + 1;
        }
        else
        {
          if ( v193 != 0 && v191 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
              v191,
              v192,
              v193);
          v192 = (unsigned __int8 *)&v186;
          v74 = 1;
        }
        v193 = v74;
        v194 = (unsigned __int8 *)&v186 + 1;
        sub_1412E70A0(&v191);
        v75 = (unsigned __int8)v186;
        if ( (char)v186 > 0 )
        {
          v76 = *(_QWORD *)(a1 + 96);
          v77 = *(_QWORD *)(a1 + 104);
          v78 = (v77 - v76) >> 3;
          if ( v78 <= (unsigned __int8)v186 )
          {
            if ( v78 < (unsigned __int8)v186 )
            {
              v79 = (*(_QWORD *)(a1 + 112) - v76) >> 3;
              if ( v79 >= (unsigned __int8)v186 )
              {
                v83 = (unsigned __int8)v186 - v78;
                v84 = v77 + 8 * v83;
                sub_141758A10(v77, 0, 8 * v83);
                *(_QWORD *)(a1 + 104) = v84;
              }
              else
              {
                v80 = v79 + (v79 >> 1);
                if ( v80 <= (unsigned __int8)v186 )
                  v80 = (unsigned __int8)v186;
                v81 = sub_1407E4490(qword_141ABD470, 8 * v80);
                sub_141758A10(v81 + 8 * v78, 0, 8 * (v75 - v78));
                sub_141758A00(v81, *(_QWORD *)(a1 + 96), *(_QWORD *)(a1 + 104) - *(_QWORD *)(a1 + 96));
                v82 = *(_QWORD *)(a1 + 96);
                if ( v82 != 0 )
                  sub_1407E4890(qword_141ABD470, v82, *(_QWORD *)(a1 + 112) - v82);
                *(_QWORD *)(a1 + 96) = v81;
                *(_QWORD *)(a1 + 104) = v81 + 8 * v75;
                *(_QWORD *)(a1 + 112) = v81 + 8 * v80;
              }
            }
          }
          else
          {
            *(_QWORD *)(a1 + 104) = v76 + 8LL * (unsigned __int8)v186;
          }
          v85 = v186;
          if ( (char)v186 > 0 )
          {
            v86 = (__int64)v194;
            v87 = 0;
            v88 = 0;
            do
            {
              v90 = *(_QWORD *)(a1 + 96);
              if ( v90 + v87 == v86 )
              {
                v89 = v193 + 4;
              }
              else
              {
                if ( v193 != 0 && v191 != nullptr )
                {
                  (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
                    v191,
                    v192,
                    v193);
                  v85 = v186;
                }
                v192 = (unsigned __int8 *)(v90 + v87);
                v89 = 4;
              }
              v193 = v89;
              v86 = v90 + 8 * v88 + 4;
              v194 = (unsigned __int8 *)(v90 + v87 + 4);
              ++v88;
              v87 += 8;
            }
            while ( v88 < v85 );
          }
        }
        if ( v194 == &v189 )
        {
          v91 = v193 + 1;
        }
        else
        {
          if ( v193 != 0 && v191 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
              v191,
              v192,
              v193);
          v192 = &v189;
          v91 = 1;
        }
        v193 = v91;
        v194 = &v190;
        sub_1412E70A0(&v191);
        v92 = v189;
        if ( (char)v189 > 0 )
        {
          v93 = *(_QWORD *)(a1 + 120);
          v94 = *(_QWORD *)(a1 + 128);
          v95 = (v94 - v93) >> 3;
          if ( v95 <= v189 )
          {
            if ( v95 < v189 )
            {
              v96 = (*(_QWORD *)(a1 + 136) - v93) >> 3;
              if ( v96 >= v189 )
              {
                v100 = v189 - v95;
                v101 = v94 + 8 * v100;
                sub_141758A10(v94, 0, 8 * v100);
                *(_QWORD *)(a1 + 128) = v101;
              }
              else
              {
                v97 = v96 + (v96 >> 1);
                if ( v97 <= v189 )
                  v97 = v189;
                v98 = sub_1407E4490(qword_141ABD470, 8 * v97);
                sub_141758A10(v98 + 8 * v95, 0, 8 * (v92 - v95));
                sub_141758A00(v98, *(_QWORD *)(a1 + 120), *(_QWORD *)(a1 + 128) - *(_QWORD *)(a1 + 120));
                v99 = *(_QWORD *)(a1 + 120);
                if ( v99 != 0 )
                  sub_1407E4890(qword_141ABD470, v99, *(_QWORD *)(a1 + 136) - v99);
                *(_QWORD *)(a1 + 120) = v98;
                *(_QWORD *)(a1 + 128) = v98 + 8 * v92;
                *(_QWORD *)(a1 + 136) = v98 + 8 * v97;
              }
            }
          }
          else
          {
            *(_QWORD *)(a1 + 128) = v93 + 8LL * v189;
          }
          v102 = v189;
          if ( (char)v189 > 0 )
          {
            v103 = (__int64)v194;
            v104 = 0;
            v105 = 0;
            do
            {
              v107 = *(_QWORD *)(a1 + 120);
              if ( v107 + v104 == v103 )
              {
                v106 = v193 + 4;
              }
              else
              {
                if ( v193 != 0 && v191 != nullptr )
                {
                  (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
                    v191,
                    v192,
                    v193);
                  v102 = v189;
                }
                v192 = (unsigned __int8 *)(v107 + v104);
                v106 = 4;
              }
              v193 = v106;
              v103 = v107 + 8 * v105 + 4;
              v194 = (unsigned __int8 *)(v107 + v104 + 4);
              ++v105;
              v104 += 8;
            }
            while ( v105 < v102 );
          }
        }
        if ( v194 == &v190 )
        {
          v108 = v193 + 1;
        }
        else
        {
          if ( v193 != 0 && v191 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
              v191,
              v192,
              v193);
          v192 = &v190;
          v108 = 1;
        }
        v193 = v108;
        v194 = (unsigned __int8 *)&v191;
        sub_1412E70A0(&v191);
        v109 = v190;
        if ( v190 != 0 )
        {
          v110 = *(_QWORD *)(a1 + 144);
          v111 = *(_QWORD *)(a1 + 152);
          v112 = (v111 - v110) >> 3;
          if ( v112 <= v190 )
          {
            if ( v112 < v190 )
            {
              v113 = (*(_QWORD *)(a1 + 160) - v110) >> 3;
              if ( v113 >= v190 )
              {
                v117 = v190 - v112;
                v118 = v111 + 8 * v117;
                sub_141758A10(v111, 0, 8 * v117);
                *(_QWORD *)(a1 + 152) = v118;
              }
              else
              {
                v114 = v113 + (v113 >> 1);
                if ( v114 <= v190 )
                  v114 = v190;
                v115 = sub_1407E4490(qword_141ABD470, 8 * v114);
                sub_141758A10(v115 + 8 * v112, 0, 8 * (v109 - v112));
                sub_141758A00(v115, *(_QWORD *)(a1 + 144), *(_QWORD *)(a1 + 152) - *(_QWORD *)(a1 + 144));
                v116 = *(_QWORD *)(a1 + 144);
                if ( v116 != 0 )
                  sub_1407E4890(qword_141ABD470, v116, *(_QWORD *)(a1 + 160) - v116);
                *(_QWORD *)(a1 + 144) = v115;
                *(_QWORD *)(a1 + 152) = v115 + 8 * v109;
                *(_QWORD *)(a1 + 160) = v115 + 8 * v114;
              }
            }
          }
          else
          {
            *(_QWORD *)(a1 + 152) = v110 + 8LL * v190;
          }
          v119 = v190;
          if ( v190 != 0 )
          {
            v120 = (__int64)v194;
            v121 = 0;
            v122 = 0;
            do
            {
              v124 = *(_QWORD *)(a1 + 144);
              if ( v124 + v121 == v120 )
              {
                v123 = v193 + 4;
              }
              else
              {
                if ( v193 != 0 && v191 != nullptr )
                {
                  (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
                    v191,
                    v192,
                    v193);
                  v119 = v190;
                }
                v192 = (unsigned __int8 *)(v124 + v121);
                v123 = 4;
              }
              v193 = v123;
              v120 = v124 + 8 * v122 + 4;
              v194 = (unsigned __int8 *)(v124 + v121 + 4);
              ++v122;
              v121 += 8;
            }
            while ( v122 < v119 );
          }
        }
        if ( v194 == (unsigned __int8 *)&v188 )
        {
          v125 = v193 + 1;
        }
        else
        {
          if ( v193 != 0 && v191 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
              v191,
              v192,
              v193);
          v192 = (unsigned __int8 *)&v188;
          v125 = 1;
        }
        v193 = v125;
        v194 = (unsigned __int8 *)&v188 + 1;
        sub_1412E70A0(&v191);
        if ( (_BYTE)v188 != 0 )
        {
          v126 = (__int64 *)(a1 + 72);
          sub_1411FF180(a1 + 72, (unsigned __int8)v188, &v185);
          v127 = v188;
          if ( (_BYTE)v188 != 0 )
          {
            v128 = v193;
            v129 = v194;
            v130 = 16;
            v131 = 0;
            do
            {
              v132 = *v126;
              v133 = *v126 + 16 * v131;
              v134 = *v126 + v130 - 16;
              if ( (unsigned __int8 *)v134 == v129 )
              {
                v128 += 16;
              }
              else
              {
                if ( v128 != 0 && v191 != nullptr )
                {
                  (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(
                    v191,
                    v192);
                  v127 = v188;
                }
                v192 = (unsigned __int8 *)v134;
                v128 = 16;
              }
              v193 = v128;
              v194 = (unsigned __int8 *)(v130 + v132);
              ++v131;
              v130 += 16;
              v129 = (unsigned __int8 *)(v133 + 16);
            }
            while ( v131 < v127 );
          }
        }
        v12 = &v185;
        if ( v194 == (unsigned __int8 *)&v185 )
        {
          v135 = v193 + 2;
        }
        else
        {
          if ( v193 != 0 && v191 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v191 + 40LL))(
              v191,
              v192,
              v193);
          v192 = (unsigned __int8 *)&v185;
          v135 = 2;
        }
        v193 = v135;
        v194 = (unsigned __int8 *)&v185 + 2;
        sub_1412E70A0(&v191);
        if ( (__int16)v185 > 0 )
        {
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(&unk_141B59A68);
              sub_141751048(sub_1407E4B20);
              sub_141750EA0(&dword_141B59AA8);
            }
          }
          v136 = (__int64 *)sub_1407E4490(&unk_141B59A68, 24);
          *v136 = 0;
          v136[1] = 0;
          v136[2] = 0;
          v137 = (void *)qword_141ABD470;
          if ( qword_141ABD470 == 0 )
          {
            if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(&dword_141B59AA8);
              if ( dword_141B59AA8 == -1 )
              {
                sub_1407E3E70(&unk_141B59A68);
                sub_141751048(sub_1407E4B20);
                sub_141750EA0(&dword_141B59AA8);
              }
            }
            qword_141ABD470 = (__int64)&unk_141B59A68;
            v137 = &unk_141B59A68;
          }
          v136[2] = 0;
          v136[1] = 0;
          *v136 = 0;
          *(_QWORD *)(a1 + 168) = v136;
          v138 = v185;
          v139 = (__int16)v185;
          v140 = *v136;
          v141 = (v136[2] - *v136) >> 3;
          if ( v141 < (__int16)v185 )
          {
            if ( (v185 & 0x8000u) != 0LL )
              sub_1400526C0(v137, v141);
            v142 = v136[1];
            v143 = sub_1407E4490(v137, 8LL * (__int16)v185);
            sub_141758A00(v143, *v136, v136[1] - *v136);
            v12 = (__int64 *)*v136;
            if ( *v136 != 0 )
            {
              v144 = v136[2] - (_QWORD)v12;
              if ( v144 == -1 )
                v144 = *(unsigned int *)((char *)v12 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v145 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v145) >> 3 > v144)
                && (v146 = *(_QWORD *)(v145 + 8 * v144)) != 0 )
              {
                v12 = (__int64 *)((char *)v12 - *(unsigned int *)(v146 + 120));
                v183 = v146;
                MEMORY[0x1419475D8](v146 + 32, v12);
                v147 = *(_BYTE *)(v183 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v183 + 64)) != 0;
                if ( !v147 && *(_BYTE *)(v183 + 97) != 0 )
                  sub_1412D33C0(v183);
              }
              else
              {
                v12 = (__int64 *)((char *)v12 - *(unsigned int *)(qword_141ABD470 + 48));
                MEMORY[0x141948990](v12);
              }
            }
            *v136 = v143;
            v136[1] = v143 + v142 - v140;
            v136[2] = v143 + 8 * v139;
            v138 = v185;
          }
          if ( v138 > 0 )
          {
            v148 = 0;
            do
            {
              if ( dword_141B61DF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                 + (unsigned int)TlsIndex)
                                               + 4LL) )
              {
                sub_141750E08(&dword_141B61DF0);
                if ( dword_141B61DF0 == -1 )
                {
                  sub_1407E53D0((unsigned int)&unk_141B61DA0, 1100141710, 1024, 40, 0, 0, 1024, 4096);
                  sub_141751048(sub_1411FA430);
                  sub_141750EA0(&dword_141B61DF0);
                }
              }
              v149 = sub_1407E58C0(&unk_141B61DA0, 40);
              *(_DWORD *)(v149 + 32) = 1900;
              *(_QWORD *)v149 = 0;
              *(_QWORD *)(v149 + 8) = 0;
              *(_QWORD *)(v149 + 16) = -1;
              *(_QWORD *)(v149 + 24) = 0x1076C00010000LL;
              if ( v193 != 0 && v191 != nullptr )
                (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(
                  v191,
                  v192);
              v194 = nullptr;
              v193 = 0;
              v192 = nullptr;
              v150 = v191;
              (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v191 + 40LL))(
                v191,
                v149,
                4);
              if ( *((_DWORD *)v150 + 4) != 0 )
                goto LABEL_55;
              v151 = v191;
              (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v191 + 40LL))(
                v191,
                v149 + 8,
                4);
              if ( *((_DWORD *)v151 + 4) != 0 )
                goto LABEL_55;
              v152 = v191;
              if ( v191 != nullptr )
              {
                _InterlockedIncrement(v191 + 2);
                (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v152 + 40LL))(
                  v152,
                  v149 + 16,
                  8);
              }
              if ( *(_DWORD *)(v149 + 20) == 0 )
                *(_DWORD *)(v149 + 20) = *(_DWORD *)(v149 + 16);
              v153 = *((_DWORD *)v152 + 4);
              if ( _InterlockedDecrement(v152 + 2) == 0 )
                (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v152)(v152, 1);
              if ( v153 != 0 )
                goto LABEL_55;
              v154 = (_WORD *)(v149 + 24);
              v155 = v191;
              (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v191 + 40LL))(
                v191,
                v149 + 24,
                2);
              if ( *((_DWORD *)v155 + 4) != 0 )
                goto LABEL_55;
              v156 = v191;
              if ( v191 != nullptr )
              {
                _InterlockedIncrement(v191 + 2);
                (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v156 + 40LL))(
                  v156,
                  v149 + 26,
                  4);
              }
              v157 = *((_DWORD *)v156 + 4);
              if ( _InterlockedDecrement(v156 + 2) == 0 )
                (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v156)(v156, 1);
              if ( v157 != 0 )
                goto LABEL_55;
              if ( (unsigned __int8)sub_140DB8980(v149 + 30, &v191) == 0 )
                goto LABEL_55;
              v158 = v191;
              (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v191 + 40LL))(
                v191,
                v149 + 34,
                1);
              if ( *((_DWORD *)v158 + 4) != 0 )
                goto LABEL_55;
              v12 = (__int64 *)v191;
              (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v191 + 40LL))(
                v191,
                v149 + 35,
                1);
              if ( *((_DWORD *)v12 + 4) != 0 )
                goto LABEL_55;
              if ( *v154 == 1900 )
                *v154 = 0;
              v159 = *(__int64 ***)(a1 + 168);
              v160 = v159[1];
              if ( v160 == v159[2] )
              {
                v184 = v148;
                v161 = (char *)v160 - (char *)*v159;
                v162 = v161 >> 3;
                v163 = (unsigned __int64)(v161 >> 3) >> 1;
                v164 = 0x1FFFFFFFFFFFFFFFLL - v163;
                v165 = (v161 >> 3) + v163;
                if ( v165 <= (v161 >> 3) + 1 )
                  v165 = v162 + 1;
                if ( v162 > v164 )
                  v165 = 0x1FFFFFFFFFFFFFFFLL;
                v12 = (__int64 *)sub_1407E4490(qword_141ABD470, 8 * v165);
                *(__int64 *)((char *)v12 + v161) = v149;
                v166 = v159[1];
                sub_141758A00(v12, *v159, (char *)v160 - (char *)*v159);
                if ( v166 != v160 )
                  sub_141758A00((char *)v12 + v161 + 8, v160, (char *)v159[1] - (char *)v160);
                v167 = *v159;
                if ( *v159 != nullptr )
                {
                  v168 = (char *)v159[2] - (char *)v167;
                  if ( v168 == -1 )
                    v168 = *(unsigned int *)((char *)v167 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v169 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v169) >> 3 > v168)
                    && (v170 = *(_QWORD *)(v169 + 8 * v168)) != 0 )
                  {
                    MEMORY[0x1419475D8](v170 + 32, (char *)v167 - *(unsigned int *)(v170 + 120));
                    v171 = *(_BYTE *)(v170 + 72) != 0
                        && _InterlockedDecrement((volatile signed __int32 *)(v170 + 64)) != 0;
                    if ( !v171 && *(_BYTE *)(v170 + 97) != 0 )
                      sub_1412D33C0(v170);
                  }
                  else
                  {
                    MEMORY[0x141948990]((char *)v167 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                }
                *v159 = v12;
                v159[1] = &v12[(v161 >> 3) + 1];
                v159[2] = &v12[v165];
                v148 = v184;
              }
              else
              {
                *v160 = v149;
                ++v159[1];
              }
            }
            while ( (__int16)++v148 < (__int16)v185 );
          }
        }
      }
      if ( v193 != 0 )
      {
        if ( v191 == nullptr )
        {
          v194 = nullptr;
          v193 = 0;
          v192 = nullptr;
          goto LABEL_307;
        }
        (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(v191, v192);
      }
      v172 = v191;
      v194 = nullptr;
      v193 = 0;
      v192 = nullptr;
      if ( v191 == nullptr )
      {
LABEL_307:
        v173 = (unsigned int *)(a1 + 8);
        LOBYTE(v12) = 1;
        v172 = nullptr;
        goto LABEL_308;
      }
      _InterlockedIncrement(v191 + 2);
      v173 = (unsigned int *)(a1 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v172 + 40LL))(v172, a1 + 8, 12);
      LODWORD(v12) = 0;
LABEL_308:
      v174 = *v173;
      if ( (unsigned int)v174 >= 0x989681 )
      {
        v174 = a6;
        *v173 = a6;
      }
      if ( a8 != 0 )
      {
        LOBYTE(v11) = 1;
        (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, a1, v174, v11);
      }
      if ( (_BYTE)v12 == 0 && _InterlockedDecrement(v172 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v172)(v172, 1);
      if ( v193 != 0 && v191 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(v191, v192);
      v194 = nullptr;
      v193 = 0;
      v192 = nullptr;
      LOBYTE(v12) = *((_DWORD *)v191 + 4) == 0;
LABEL_319:
      if ( v193 != 0 )
      {
        if ( v191 == nullptr )
          return (unsigned int)v12;
        (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *))(*(_QWORD *)v191 + 40LL))(v191, v192);
      }
      v175 = v191;
      v194 = nullptr;
      v193 = 0;
      v192 = nullptr;
      if ( v191 != nullptr && _InterlockedDecrement(v191 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v175)(v175, 1);
      return (unsigned int)v12;
    }
  }
  v24 = v188;
  if ( v188 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v188 - 4)) == 0 )
    sub_1412EC9A0(v24 - 4, v23);
  v25 = v185;
  if ( v185 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v185 - 4)) == 0 )
    sub_1412EC9A0(v25 - 4, v23);
LABEL_55:
  LODWORD(v12) = 0;
  goto LABEL_319;
}
