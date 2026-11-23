__int64 __fastcall sub_14009CF00(__int64 a1, _QWORD *a2, int a3, __int64 *a4, unsigned __int64 a5, char a6)
{
  __int64 v7; // rdi
  char v8; // al
  _QWORD *v9; // r12
  _QWORD *v10; // rsi
  _QWORD *v11; // rbp
  __int64 v12; // rbx
  unsigned __int16 v15; // si
  __int64 v16; // rbx
  __int64 v17; // rbp
  __int64 v18; // rsi
  int v19; // ebx
  __int64 v20; // rcx
  unsigned int v21; // ecx
  unsigned int v22; // eax
  _DWORD *v23; // rbp
  unsigned __int16 v24; // ax
  char v25; // r12
  unsigned __int16 v26; // dx
  bool v27; // al
  char v28; // bp
  char v29; // bl
  unsigned __int16 v30; // bp
  __int16 v31; // si
  __int64 v32; // rcx
  __int16 v33; // ax
  __int64 v34; // rbx
  unsigned __int16 v35; // si
  __int64 v36; // rcx
  __int64 v37; // rax
  char v38; // al
  int v39; // eax
  __int64 v40; // rcx
  _DWORD *v41; // rsi
  __int64 v42; // r8
  _DWORD *v43; // rsi
  _DWORD *v44; // rcx
  unsigned int v45; // ebx
  _DWORD *v46; // rbp
  unsigned int v47; // r12d
  __int64 v48; // rax
  __int64 v49; // rax
  __int64 v50; // rsi
  void (__fastcall ***v51)(_QWORD, __int64); // rcx
  void (__fastcall ***v52)(_QWORD, __int64); // rcx
  __int64 v53; // rsi
  __int64 v54; // rsi
  __int64 v55; // rax
  __int64 v56; // rsi
  void (__fastcall ***v57)(_QWORD, __int64); // rcx
  void (__fastcall ***v58)(_QWORD, __int64); // rcx
  __int64 v59; // rsi
  __int64 v60; // rsi
  __int64 v61; // rsi
  __int64 v62; // rsi
  __int64 v63; // rcx
  __int64 v64; // rcx
  __int64 v65; // rsi
  unsigned __int64 v66; // rax
  __int64 *v67; // r15
  unsigned __int64 v68; // r14
  unsigned __int64 v69; // r13
  __int64 v70; // rbx
  _DWORD *v71; // rdi
  _QWORD *v72; // rsi
  __int64 v73; // rcx
  _DWORD *v74; // rbp
  __int64 v75; // rcx
  __int64 v76; // rcx
  __int64 v77; // rbx
  unsigned __int64 v78; // rax
  unsigned __int64 v79; // rbp
  unsigned __int64 v80; // rcx
  unsigned __int64 v81; // rbp
  __int64 v82; // r12
  _DWORD *v83; // r13
  __int64 v84; // rsi
  unsigned __int64 v85; // rax
  unsigned __int64 v86; // rbx
  __int64 v87; // r12
  _DWORD *v88; // rdi
  int v89; // esi
  __int64 v90; // rax
  __int64 v91; // rax
  __int64 v92; // rdx
  __int64 v93; // rax
  unsigned __int64 v94; // rsi
  __int64 v95; // rax
  unsigned __int64 v96; // rsi
  __int64 v97; // r8
  bool v98; // bl
  bool v99; // si
  bool v100; // bl
  _QWORD *v101; // rsi
  _QWORD *v102; // rax
  __int64 v103; // r14
  __int64 v104; // rax
  __int64 v105; // rbx
  __int64 v106; // rax
  __int64 v107; // rbx
  __int64 v108; // rax
  _QWORD *v109; // rax
  __int64 v110; // rax
  __int64 v111; // rbx
  __int64 v112; // rax
  __int64 v113; // rcx
  __int64 v114; // rbx
  __int64 v116; // rbx
  __int64 v117; // r8
  __int64 v118; // [rsp+38h] [rbp-1A0h] BYREF
  _DWORD *v119; // [rsp+40h] [rbp-198h]
  int v120; // [rsp+48h] [rbp-190h]
  bool v121; // [rsp+4Fh] [rbp-189h]
  __int128 v122; // [rsp+50h] [rbp-188h] BYREF
  __int64 v123; // [rsp+60h] [rbp-178h]
  __int64 v124; // [rsp+78h] [rbp-160h]
  __int128 v125; // [rsp+80h] [rbp-158h] BYREF
  __int64 v126; // [rsp+90h] [rbp-148h]
  __int16 v127; // [rsp+A8h] [rbp-130h] BYREF
  __int16 v128; // [rsp+AAh] [rbp-12Eh]
  unsigned int v129; // [rsp+ACh] [rbp-12Ch]
  char v130[8]; // [rsp+B0h] [rbp-128h] BYREF
  __int64 v131; // [rsp+B8h] [rbp-120h]
  int v132; // [rsp+C0h] [rbp-118h] BYREF
  _QWORD *v133; // [rsp+C8h] [rbp-110h]
  _BYTE v134[12]; // [rsp+D0h] [rbp-108h] BYREF
  unsigned int v135; // [rsp+DCh] [rbp-FCh]
  int v136; // [rsp+E0h] [rbp-F8h]
  int v137; // [rsp+E4h] [rbp-F4h]
  __int64 v138; // [rsp+E8h] [rbp-F0h] BYREF
  __int64 v139; // [rsp+F0h] [rbp-E8h]
  int v140; // [rsp+F8h] [rbp-E0h]
  __int64 v141; // [rsp+100h] [rbp-D8h] BYREF
  __int64 v142; // [rsp+108h] [rbp-D0h]
  int v143; // [rsp+110h] [rbp-C8h]
  __int64 v144; // [rsp+118h] [rbp-C0h]
  __int64 v145; // [rsp+120h] [rbp-B8h]
  char v146[8]; // [rsp+128h] [rbp-B0h] BYREF
  __int64 v147; // [rsp+130h] [rbp-A8h]
  __int64 v148; // [rsp+138h] [rbp-A0h]
  __int64 v149; // [rsp+140h] [rbp-98h]
  _QWORD *v150; // [rsp+148h] [rbp-90h]
  __int64 *v151; // [rsp+150h] [rbp-88h]
  _WORD *v152; // [rsp+158h] [rbp-80h]
  char v153[8]; // [rsp+160h] [rbp-78h] BYREF
  char v154; // [rsp+168h] [rbp-70h] BYREF
  unsigned int v155; // [rsp+170h] [rbp-68h] BYREF
  __int64 v156; // [rsp+178h] [rbp-60h] BYREF

  v7 = a1;
  if ( *(_BYTE *)(a1 + 1372) != 0 )
  {
    *(_QWORD *)&v122 = 0;
    sub_140809040(a1: &v122, a2: 0x14190BFADLL, a3: 0xFFFFFFFFLL);
    if ( (unsigned __int8)sub_140809830(a1: &v122) == 0 && *(_BYTE *)(v7 + 1529) == 0 )
    {
      *(_BYTE *)(v7 + 1529) = 1;
      v8 = sub_140887730(a1: v7 + 8, a2: &v122, a3: 0, a4: 0);
      *(_BYTE *)(v7 + 1529) = 0;
      if ( v8 != 0 )
      {
        v9 = *(_QWORD **)(v7 + 1200);
        v10 = *(_QWORD **)(v7 + 1208);
        if ( v9 != v10 )
        {
          v11 = *(_QWORD **)(v7 + 1200);
          do
          {
            v12 = *v11;
            if ( *v11 != 0 )
            {
              sub_1408B5C40(a1: *v11);
              sub_141750CFC(a1: v12);
            }
            ++v11;
          }
          while ( v11 != v10 );
          v114 = *(_QWORD *)(v7 + 1208) - (_QWORD)v10;
          sub_141758A00(a1: v9, a2: v10, a3: v114);
          *(_QWORD *)(v7 + 1208) = (char *)v9 + v114;
        }
        sub_1400D99F0(a1: v7 + 1200, a2: v7 + 1176);
      }
    }
    sub_140808B00(a1: &v122);
    goto LABEL_242;
  }
  v15 = HIWORD(dword_141AAE084);
  if ( v15 < (unsigned __int16)sub_140FC9BB0() && *(_BYTE *)(v7 + 1352) == 0 )
    sub_14006A670(a1: qword_141ABDFF0);
  if ( *(_QWORD *)(v7 + 16) == 0 )
  {
LABEL_242:
    LODWORD(v101) = 0;
    v113 = *a2;
    if ( *a2 == 0 )
      return (unsigned int)v101;
    goto LABEL_243;
  }
  if ( *(_BYTE *)(v7 + 1369) != 0 )
  {
    v16 = *(_QWORD *)(v7 + 576);
    if ( (unsigned __int64)(*(_QWORD *)(v7 + 592) - v16) <= 0x26259FF )
    {
      v17 = *(_QWORD *)(v7 + 584);
      v18 = sub_1407E4490(a1: qword_141ABD470, a2: 40000000);
      sub_141758A00(a1: v18, a2: *(_QWORD *)(v7 + 576), a3: *(_QWORD *)(v7 + 584) - *(_QWORD *)(v7 + 576));
      if ( *(_QWORD *)(v7 + 576) != 0 )
        sub_1407E4890(a1: qword_141ABD470);
      *(_QWORD *)(v7 + 576) = v18;
      *(_QWORD *)(v7 + 584) = v18 + v17 - v16;
      *(_QWORD *)(v7 + 592) = v18 + 40000000;
    }
  }
  if ( *(_BYTE *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 8LL) == 0 )
    sub_141751038();
  v132 = dword_141AAE084;
  v136 = sub_140DB9110(a1: v7 + 1268, a2: &v132);
  sub_14011BE90(a1: qword_141ABF5C0, a2: 4, a3: v136, a4: 0, a5: (__int64)&qword_141B59EE0, a6: 0);
  v152 = (_WORD *)(v7 + 1268);
  sub_140DB9110(a1: v7 + 1268, a2: &v132);
  sub_140310A50(a1: v134);
  v145 = qword_141ABD468;
  sub_140310A50(a1: v146);
  sub_140310A50(a1: v130);
  v19 = *(_DWORD *)(v7 + 1400);
  if ( v19 == -1 )
    a3 = -1;
  v144 = (unsigned int)*(char *)(v7 + 1397);
  byte_141ABEA60 = 1;
  *(_QWORD *)(v7 + 1576) = 0;
  *(_QWORD *)(v7 + 1568) = 0;
  *(_QWORD *)(v7 + 1560) = 0;
  *(_QWORD *)(v7 + 1552) = 0;
  *(_QWORD *)(v7 + 1544) = 0;
  if ( *a2 == 0 )
  {
    sub_140048080(a1: &v122);
    v20 = *a2;
    if ( *a2 == (_QWORD)v122 )
    {
      if ( v20 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v20)(a1: v20, a2: 1);
    }
    else
    {
      if ( v20 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v20)(a1: v20, a2: 1);
      *a2 = v122;
    }
  }
  if ( a4 != nullptr )
  {
    LOWORD(v21) = *(_WORD *)(v7 + 1278);
    LOWORD(v22) = *(_WORD *)(v7 + 1276);
    if ( (unsigned __int16)v21 < HIWORD(dword_141AAE084)
      || (unsigned __int16)v21 <= HIWORD(dword_141AAE084)
      && (unsigned __int16)(*(_WORD *)(v7 + 1276) & 0x1FF) <= (unsigned __int16)(dword_141AAE084 & 0x1FF) )
    {
      sub_140DB8850(a1: &dword_141AAE084, a2: &v122, a3: *(unsigned __int16 *)(v7 + 1400));
      v22 = v122;
      *(_DWORD *)(v7 + 1276) = v122;
      v21 = HIWORD(v22);
    }
  }
  else
  {
    LOWORD(v22) = *(_WORD *)(v7 + 1276);
    LOWORD(v21) = *(_WORD *)(v7 + 1278);
  }
  v129 = a3;
  v119 = (_DWORD *)(v7 + 1276);
  if ( (_WORD)v21 != MEMORY[0x1418761EE] || (((unsigned __int16)v22 ^ MEMORY[0x1418761EC]) & 0x1FF) != 0 )
  {
    v23 = v119;
    do
    {
      v24 = v22 & 0x1FF;
      if ( (unsigned __int16)v21 >= HIWORD(dword_141AAE084)
        && ((unsigned __int16)v21 > HIWORD(dword_141AAE084) || v24 >= (unsigned __int16)(dword_141AAE084 & 0x1FF)) )
      {
        break;
      }
      sub_140DB8850(a1: v23, a2: &v122, a3: v129);
      v22 = v122;
      *v23 = v122;
      v21 = HIWORD(v22);
    }
    while ( MEMORY[0x1418761EE] != HIWORD(v22) || (((unsigned __int16)v22 ^ MEMORY[0x1418761EC]) & 0x1FF) != 0 );
  }
  v150 = (_QWORD *)(v7 + 1544);
  v147 = v7 + 1552;
  v148 = v7 + 1560;
  v149 = v7 + 1576;
  v121 = v19 != -1;
  sub_1408876C0(a1: v7 + 8);
  v128 = sub_140FC9BB0() + 2;
  v127 = 1;
  *(_QWORD *)&v125 = 0x4014000000000000LL;
  sub_140815020(a1: &v122, a2: &v125);
  v141 = 0;
  v142 = v122;
  v143 = 1;
  sub_140815160(a1: &v141);
  *(_QWORD *)&v125 = 0x3FF0000000000000LL;
  sub_140815020(a1: &v122, a2: &v125);
  v138 = 0;
  v139 = v122;
  v140 = 1;
  sub_140815160(a1: &v138);
  v135 = (unsigned __int8)v144;
  v137 = v144 + 1;
  v120 = 0;
  v133 = a2;
  v124 = v7 + 8;
  v25 = a6;
  do
  {
    v26 = *(_WORD *)(v7 + 1270);
    v27 = true;
    if ( HIWORD(dword_141AAE084) >= v26 )
    {
      if ( HIWORD(dword_141AAE084) > v26 )
      {
        v28 = 0;
        v101 = v150;
        if ( *v150 != 0 )
          goto LABEL_212;
        goto LABEL_224;
      }
      v27 = (unsigned __int16)(dword_141AAE084 & 0x1FF) < (unsigned __int16)(*v152 & 0x1FF);
    }
    v28 = 0;
    if ( !v27 || (byte_141ABEA60 & 1) == 0 )
      goto LABEL_211;
    v29 = sub_140DB8260(a1: &dword_141AAE084);
    v30 = dword_141AAE084;
    v31 = HIWORD(dword_141AAE084);
    if ( v29 == (unsigned __int8)sub_140DB8260(a1: &v127)
      && (((unsigned __int16)v127 ^ v30) & 0x1FF) == 0
      && v31 == v128
      && *(_BYTE *)(v7 + 1354) == 0
      && *(_BYTE *)(v7 + 1528) == 0 )
    {
      sub_14009FB30(a1: v7);
    }
    sub_1400A0100(a1: v32, a2: &qword_141B59EE0);
    if ( (((unsigned __int16)dword_141AAE084 ^ *(_WORD *)(v7 + 1264)) & 0x1FF) == 0
      && HIWORD(dword_141AAE084) == *(_WORD *)(v7 + 1266) )
    {
      byte_141ABEA62 = 1;
    }
    v33 = sub_140DB9560(a1: &dword_141AAE084);
    v34 = v124;
    if ( v33 == 0 )
    {
      if ( v25 != 0
        && (unsigned __int16)sub_140DB95E0(a1: &dword_141AAE084) == 1
        && (unsigned __int8)sub_140DB9C10(a1: &dword_141AAE084) == 1 )
      {
        v35 = HIWORD(dword_141AAE084);
        if ( v35 > (unsigned __int16)sub_140FC9BB0() )
        {
          *(_QWORD *)&v125 = 0;
          sub_140809040(a1: &v125, a2: 0x141909590LL, a3: 0xFFFFFFFFLL);
          sub_1407D5F40(a1: &v122, a2: &v125);
          sub_140808B00(a1: &v125);
          sub_1407D8AB0(a1: &v125, a2: 0x1418E2C24LL);
          v36 = *a2;
          if ( *a2 != 0 )
          {
            _InterlockedIncrement((volatile signed __int32 *)(v36 + 8));
            if ( _InterlockedDecrement((volatile signed __int32 *)(v36 + 8)) == 0 )
              (**(void (__fastcall ***)(__int64, __int64))v36)(a1: v36, a2: 1);
          }
          *(_BYTE *)(v7 + 1374) = 1;
          sub_1407D8AB0(a1: &v125, a2: 0x1418E2C24LL);
          v37 = *a2;
          v156 = v37;
          if ( v37 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v37 + 8));
          v38 = sub_1400959F0(a1: v7, a2: &v156, a3: (__int64)&v122, a4: (__int64)&v125);
          *(_BYTE *)(v7 + 1374) = 0;
          if ( v38 == 0 )
          {
            v116 = qword_141B5AD60;
            v101 = (_QWORD *)sub_1400015F0(a1: &v122);
            v118 = 0;
            sub_140809040(a1: &v118, a2: 0x141941E03LL, a3: 0xFFFFFFFFLL);
            sub_140809550(a1: &v118, a2: &v125, a3: v101);
            LODWORD(v101) = 0;
            LOBYTE(v117) = 1;
            (*(void (__fastcall **)(__int64, __int128 *, __int64, _QWORD))(*(_QWORD *)v116 + 120LL))(
              a1: v116,
              a2: &v125,
              a3: v117,
              a4: 0);
            a2 = v133;
            sub_140808B00(a1: &v125);
            sub_140808B00(a1: &v118);
            sub_140808B00(a1: &v122);
            goto LABEL_237;
          }
          sub_140808B00(a1: &v122);
        }
      }
      v39 = *(_DWORD *)(v7 + 1400);
      if ( v121 || v39 == -1 )
      {
        if ( (((unsigned __int16)dword_141AAE084 ^ *(_WORD *)(v7 + 1276)) & 0x1FF) == 0
          && HIWORD(dword_141AAE084) == *(_WORD *)(v7 + 1278) )
        {
          if ( a4 != nullptr )
          {
            if ( (a4[1] - *a4) >> 2 < a5 )
            {
              sub_1407D8AB0(a1: &v122, a2: 0x1418E2C24LL);
              sub_14009FA50(a1: &v125, a2: v119);
              v40 = *a2;
              if ( *a2 != 0 )
              {
                _InterlockedIncrement((volatile signed __int32 *)(v40 + 8));
                if ( _InterlockedDecrement((volatile signed __int32 *)(v40 + 8)) == 0 )
                  (**(void (__fastcall ***)(__int64, __int64))v40)(a1: v40, a2: 1);
              }
              sub_140808B00(a1: &v125);
              v41 = (_DWORD *)a4[1];
              if ( v41 == (_DWORD *)a4[2] )
              {
                v131 = v7;
                v77 = (__int64)v41 - *a4;
                v78 = v77 >> 2;
                v79 = (unsigned __int64)(v77 >> 2) >> 1;
                v80 = 0x3FFFFFFFFFFFFFFFLL - v79;
                v81 = (v77 >> 2) + v79;
                if ( v81 <= (v77 >> 2) + 1 )
                  v81 = v78 + 1;
                if ( v78 > v80 )
                  v81 = 0x3FFFFFFFFFFFFFFFLL;
                v82 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v81);
                *(_DWORD *)(v82 + v77) = *v119;
                v83 = (_DWORD *)a4[1];
                sub_141758A00(a1: v82, a2: *a4, a3: (char *)v41 - *a4);
                if ( v83 != v41 )
                  sub_141758A00(a1: v82 + v77 + 4, a2: v41, a3: a4[1] - (_QWORD)v41);
                if ( *a4 != 0 )
                  sub_1407E4890(a1: qword_141ABD470);
                *a4 = v82;
                a4[1] = v82 + 4 * ((v77 >> 2) + 1);
                a4[2] = v82 + 4 * v81;
                v7 = v131;
                a2 = v133;
                v25 = a6;
                v42 = *(unsigned int *)(v131 + 1400);
                if ( (_DWORD)v42 == -1 )
                  goto LABEL_81;
              }
              else
              {
                *v41 = *v119;
                a4[1] += 4;
                v42 = *(unsigned int *)(v7 + 1400);
                if ( (_DWORD)v42 == -1 )
                {
LABEL_81:
                  v43 = v119;
                  v44 = v119;
                  LOWORD(v42) = 365;
LABEL_172:
                  sub_140DB8850(a1: v44, a2: &v122, a3: v42);
                  *v43 = v122;
                  goto LABEL_173;
                }
              }
LABEL_144:
              if ( v129 == -1 )
              {
                if ( (int)v42 <= 0 )
                  goto LABEL_173;
                v43 = v119;
                v44 = v119;
              }
              else
              {
                v43 = v119;
                v44 = v119;
                v42 = v129;
              }
              goto LABEL_172;
            }
          }
          else
          {
            sub_1407D8AB0(a1: &v122, a2: 0x1418E2C24LL);
            v118 = 0;
            sub_140809040(a1: &v118, a2: 0x14190953ALL, a3: 0xFFFFFFFFLL);
            sub_1407D5F40(a1: &v125, a2: &v118);
            v75 = *a2;
            if ( *a2 != 0 )
            {
              _InterlockedIncrement((volatile signed __int32 *)(v75 + 8));
              if ( _InterlockedDecrement((volatile signed __int32 *)(v75 + 8)) == 0 )
                (**(void (__fastcall ***)(__int64, __int64))v75)(a1: v75, a2: 1);
            }
            sub_140808B00(a1: &v125);
            sub_140808B00(a1: &v118);
          }
          v42 = *(unsigned int *)(v7 + 1400);
          if ( (_DWORD)v42 == -1 )
            goto LABEL_81;
          goto LABEL_144;
        }
LABEL_173:
        v89 = sub_140DB9110(a1: &dword_141AAE084, a2: &v132);
        *(_QWORD *)&v122 = 0;
        sub_140815160(a1: &v122);
        if ( (__int64)v122 - v141 <= v142 )
          goto LABEL_179;
        if ( v143 != 0 )
        {
          if ( v143 != 2 )
          {
            if ( v143 != 1 )
              goto LABEL_179;
            if ( v142 != 0 )
            {
              v90 = ((__int64)v122 - v141) / v142;
              v141 += v142 * (int)v90;
              if ( v90 << 32 == 0 )
              {
LABEL_179:
                v34 = v124;
                goto LABEL_193;
              }
            }
            else
            {
              v141 = v122;
            }
          }
        }
        else
        {
          v141 += v142;
        }
        *(_QWORD *)&v122 = 0;
        sub_140815160(a1: &v122);
        if ( (__int64)v122 - v138 > v139 )
        {
          switch ( v140 )
          {
            case 0:
              v138 += v139;
              goto LABEL_191;
            case 2:
LABEL_191:
              LODWORD(v91) = 1;
              goto LABEL_192;
            case 1:
              if ( v139 != 0 )
              {
                v91 = (int)(((__int64)v122 - v138) / v139);
                v138 += v91 * v139;
LABEL_192:
                v34 = v124;
                v120 += v91;
                sub_14080B990(
                  a1: &v122,
                  a2: 0x14193C715LL,
                  a3: (unsigned int)(v120 / 60),
                  a4: (unsigned int)(v120 % 60));
                sub_14011BE90(a1: qword_141ABF5C0, a2: 4, a3: v136, a4: v89, a5: (__int64)&v122, a6: 0);
                sub_140808B00(a1: &v122);
                goto LABEL_193;
              }
              v138 = v122;
              goto LABEL_191;
            default:
              break;
          }
        }
        LODWORD(v91) = 0;
        goto LABEL_192;
      }
      if ( v39 <= 0
        || (((unsigned __int16)dword_141AAE084 ^ *(_WORD *)(v7 + 1276)) & 0x1FF) != 0
        || HIWORD(dword_141AAE084) != *(_WORD *)(v7 + 1278) )
      {
        goto LABEL_173;
      }
      v131 = v7;
      if ( (_BYTE)v144 == 0 )
      {
LABEL_132:
        if ( a4 != nullptr )
        {
          v7 = v131;
          v25 = a6;
          if ( (a4[1] - *a4) >> 2 < a5 )
          {
            sub_1407D8AB0(a1: &v122, a2: 0x1418E2C24LL);
            sub_14009FA50(a1: &v125, a2: v119);
            v73 = *a2;
            if ( *a2 != 0 )
            {
              _InterlockedIncrement((volatile signed __int32 *)(v73 + 8));
              if ( _InterlockedDecrement((volatile signed __int32 *)(v73 + 8)) == 0 )
                (**(void (__fastcall ***)(__int64, __int64))v73)(a1: v73, a2: 1);
            }
            sub_140808B00(a1: &v125);
            v74 = (_DWORD *)a4[1];
            if ( v74 == (_DWORD *)a4[2] )
            {
              v84 = (__int64)v74 - *a4;
              v85 = v84 >> 2;
              v86 = v85 + (v85 >> 1);
              if ( v86 <= (v84 >> 2) + 1 )
                v86 = v85 + 1;
              if ( v85 > 0x3FFFFFFFFFFFFFFFLL - (v85 >> 1) )
                v86 = 0x3FFFFFFFFFFFFFFFLL;
              v87 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v86);
              *(_DWORD *)(v87 + v84) = *v119;
              v88 = (_DWORD *)a4[1];
              sub_141758A00(a1: v87, a2: *a4, a3: (char *)v74 - *a4);
              if ( v88 != v74 )
                sub_141758A00(a1: v87 + v84 + 4, a2: v74, a3: a4[1] - (_QWORD)v74);
              a2 = v133;
              if ( *a4 != 0 )
                sub_1407E4890(a1: qword_141ABD470);
              *a4 = v87;
              a4[1] = v87 + 4 * ((v84 >> 2) + 1);
              a4[2] = v87 + 4 * v86;
              v7 = v131;
              v25 = a6;
            }
            else
            {
              *v74 = *v119;
              a4[1] += 4;
            }
          }
        }
        else
        {
          sub_1407D8AB0(a1: &v122, a2: 0x1418E2C24LL);
          sub_14009FA50(a1: &v125, a2: v119);
          v76 = *a2;
          if ( *a2 != 0 )
          {
            _InterlockedIncrement((volatile signed __int32 *)(v76 + 8));
            if ( _InterlockedDecrement((volatile signed __int32 *)(v76 + 8)) == 0 )
              (**(void (__fastcall ***)(__int64, __int64))v76)(a1: v76, a2: 1);
          }
          sub_140808B00(a1: &v125);
          v7 = v131;
          v25 = a6;
        }
        v43 = v119;
        v44 = v119;
        v42 = v129;
        goto LABEL_172;
      }
      v45 = v135;
      v151 = a4;
      while ( 1 )
      {
        v47 = v45 - 1;
        sub_14009FA50(a1: &v122, a2: v119);
        v48 = sub_1400015F0(a1: &v122);
        sub_140809100(a1: v134, a2: v48);
        sub_140808B00(a1: &v122);
        *(_QWORD *)&v125 = 0;
        sub_140809040(a1: &v125, a2: 0x14193CC39LL, a3: 0xFFFFFFFFLL);
        sub_140824A20(a1: v145, a2: &v122, a3: &v125);
        sub_140808B00(a1: &v125);
        v49 = sub_1407E4940();
        v50 = sub_1407E4490(a1: v49, a2: 24);
        *(_DWORD *)(v50 + 8) = 0;
        *(_QWORD *)v50 = 0x141759568LL;
        *(_QWORD *)(v50 + 16) = 0;
        sub_140809100(a1: v50 + 16, a2: v134);
        *(_QWORD *)&v125 = v50;
        _InterlockedIncrement((volatile signed __int32 *)(v50 + 8));
        sub_14081D7C0(a1: &v122, a2: 1, a3: &v125, a4: 0);
        v51 = (void (__fastcall ***)(_QWORD, __int64))v125;
        if ( (_QWORD)v125 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v125 + 8)) == 0 )
          (**v51)(a1: v51, a2: 1);
        LODWORD(v118) = v45 - 1;
        sub_140828CE0(a1: &v125, a2: &v118);
        sub_14081D7C0(a1: &v122, a2: 1, a3: &v125, a4: 0);
        v52 = (void (__fastcall ***)(_QWORD, __int64))v125;
        if ( (_QWORD)v125 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v125 + 8)) == 0 )
          (**v52)(a1: v52, a2: 1);
        sub_14081ED40(a1: &v122, a2: &v125, a3: 0);
        sub_140809170(a1: v146, a2: &v125);
        sub_140808B00(a1: &v125);
        sub_1407D5F40(a1: &v125, a2: v146);
        sub_140809170(a1: v130, a2: &v125);
        sub_140808B00(a1: &v125);
        if ( v47 < 2 || v137 != v45 )
          break;
        v53 = *a2;
        if ( *a2 != 0 )
        {
          sub_1407D8AB0(a1: &v125, a2: 0x1418E2C24LL);
          if ( (*(unsigned __int8 (__fastcall **)(__int64, char *, __int128 *))(*(_QWORD *)v53 + 192LL))(
                 a1: v53,
                 a2: v130,
                 a3: &v125) != 0 )
          {
            v54 = *a2;
            sub_1407D8AB0(a1: &v125, a2: 0x1418E2C24LL);
            sub_1407D2460(a1: v54, a2: (unsigned int)&v118, a3: (unsigned int)v130, a4: (unsigned int)&v125, a5: 3);
            if ( a4 != nullptr )
              goto LABEL_115;
            goto LABEL_120;
          }
          goto LABEL_114;
        }
        if ( a4 != nullptr )
        {
LABEL_115:
          if ( (a4[1] - *a4) >> 2 < a5 )
          {
            sub_1407D8AB0(a1: &v125, a2: 0x1418E2C24LL);
            sub_14009FA50(a1: &v118, a2: v119);
            v63 = *a2;
            if ( *a2 != 0 )
            {
              _InterlockedIncrement((volatile signed __int32 *)(v63 + 8));
              if ( _InterlockedDecrement((volatile signed __int32 *)(v63 + 8)) == 0 )
                (**(void (__fastcall ***)(__int64, __int64))v63)(a1: v63, a2: 1);
            }
            sub_140808B00(a1: &v118);
            v46 = (_DWORD *)a4[1];
            if ( v46 == (_DWORD *)a4[2] )
            {
              v65 = (__int64)v46 - *a4;
              v66 = v65 >> 2;
              v67 = a4;
              v68 = (v65 >> 2) + 1;
              v69 = v66 + (v66 >> 1);
              if ( v69 <= v68 )
                v69 = v66 + 1;
              if ( v66 > 0x3FFFFFFFFFFFFFFFLL - (v66 >> 1) )
                v69 = 0x3FFFFFFFFFFFFFFFLL;
              v70 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v69);
              *(_DWORD *)(v70 + v65) = *v119;
              v71 = (_DWORD *)v67[1];
              sub_141758A00(a1: v70, a2: *v67, a3: (char *)v46 - *v67);
              if ( v71 != v46 )
                sub_141758A00(a1: v70 + v65 + 4, a2: v46, a3: v67[1] - (_QWORD)v46);
              v72 = v133;
              if ( *v67 != 0 )
                sub_1407E4890(a1: qword_141ABD470);
              *v67 = v70;
              v67[1] = v70 + 4 * v68;
              v67[2] = v70 + 4 * v69;
              a2 = v72;
              a4 = v67;
            }
            else
            {
              *v46 = *v119;
              a4[1] += 4;
            }
          }
          goto LABEL_89;
        }
LABEL_120:
        sub_1407D8AB0(a1: &v125, a2: 0x1418E2C24LL);
        v64 = *a2;
        if ( *a2 != 0 )
        {
          _InterlockedIncrement((volatile signed __int32 *)(v64 + 8));
          if ( _InterlockedDecrement((volatile signed __int32 *)(v64 + 8)) == 0 )
            (**(void (__fastcall ***)(__int64, __int64))v64)(a1: v64, a2: 1);
        }
LABEL_89:
        sub_14081D040(a1: &v122);
        v45 = v47;
        if ( v47 == 0 )
          goto LABEL_132;
      }
      v118 = 0;
      sub_140809040(a1: &v118, a2: 0x14193CC39LL, a3: 0xFFFFFFFFLL);
      sub_140824A20(a1: v145, a2: &v125, a3: &v118);
      sub_140808B00(a1: &v118);
      v55 = sub_1407E4940();
      v56 = sub_1407E4490(a1: v55, a2: 24);
      *(_DWORD *)(v56 + 8) = 0;
      *(_QWORD *)v56 = 0x141759568LL;
      *(_QWORD *)(v56 + 16) = 0;
      sub_140809100(a1: v56 + 16, a2: v134);
      v118 = v56;
      _InterlockedIncrement((volatile signed __int32 *)(v56 + 8));
      sub_14081D7C0(a1: &v125, a2: 1, a3: &v118, a4: 0);
      v57 = (void (__fastcall ***)(_QWORD, __int64))v118;
      if ( v118 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v118 + 8)) == 0 )
        (**v57)(a1: v57, a2: 1);
      v155 = v45;
      sub_140828CE0(a1: &v118, a2: &v155);
      sub_14081D7C0(a1: &v125, a2: 1, a3: &v118, a4: 0);
      v58 = (void (__fastcall ***)(_QWORD, __int64))v118;
      if ( v118 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v118 + 8)) == 0 )
        (**v58)(a1: v58, a2: 1);
      sub_14081ED40(a1: &v125, a2: &v155, a3: 0);
      sub_1407D5F40(a1: &v118, a2: &v155);
      sub_140808B00(a1: &v155);
      v59 = *a2;
      if ( *a2 != 0 )
      {
        sub_1407D8AB0(a1: &v155, a2: 0x1418E2C24LL);
        if ( (*(unsigned __int8 (__fastcall **)(__int64, char *, unsigned int *))(*(_QWORD *)v59 + 192LL))(
               a1: v59,
               a2: v130,
               a3: &v155) != 0 )
        {
          v60 = *a2;
          sub_1407D8AB0(a1: &v155, a2: 0x1418E2C24LL);
          if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *, unsigned int *))(*(_QWORD *)v60 + 192LL))(
                 a1: v60,
                 a2: &v118,
                 a3: &v155) != 0 )
          {
            v61 = *a2;
            sub_1407D8AB0(a1: &v155, a2: 0x1418E2C24LL);
            sub_1407D2460(a1: v61, a2: (unsigned int)v153, a3: (unsigned int)&v118, a4: (unsigned int)&v155, a5: 3);
          }
          v62 = *a2;
          sub_1407D8AB0(a1: &v155, a2: 0x1418E2C24LL);
          sub_1407D8AB0(a1: v153, a2: 0x1418E2C24LL);
          sub_1407D32B0(
            a1: v62,
            a2: (unsigned int)&v154,
            a3: (unsigned int)v130,
            a4: (unsigned int)v153,
            a5: (__int64)&v118,
            a6: (__int64)&v155);
          a4 = v151;
        }
      }
      sub_140808B00(a1: &v118);
      sub_14081D040(a1: &v125);
LABEL_114:
      if ( a4 != nullptr )
        goto LABEL_115;
      goto LABEL_120;
    }
LABEL_193:
    sub_140DB8590(a1: &dword_141AAE084);
    if ( (unsigned __int16)sub_140DB9560(a1: &dword_141AAE084) != 0 )
    {
      sub_1400A0810(a1: v7);
      if ( qword_141ABD470 != 0 )
        goto LABEL_196;
LABEL_195:
      qword_141ABD470 = sub_1407E4940();
      goto LABEL_196;
    }
    sub_1400A01D0(a1: v7);
    sub_1400A03B0(a1: v7);
    if ( qword_141ABD470 == 0 )
      goto LABEL_195;
LABEL_196:
    v122 = 0;
    v123 = 0;
    v125 = 0;
    v126 = 0;
    sub_1408A5F40(a1: v34);
    sub_14088B390(a1: v34, a2: &v122, a3: &v125);
    v93 = v122;
    if ( *((_QWORD *)&v122 + 1) != (_QWORD)v122 )
    {
      v94 = 0;
      do
      {
        LOBYTE(v92) = -1;
        sub_1408D0980(a1: *(_QWORD *)(v93 + 8 * v94++), a2: v92, a3: 0);
        v93 = v122;
      }
      while ( v94 < (__int64)(*((_QWORD *)&v122 + 1) - v122) >> 3 );
    }
    v95 = v125;
    if ( *((_QWORD *)&v125 + 1) != (_QWORD)v125 )
    {
      v96 = 0;
      do
      {
        LOBYTE(v92) = -1;
        sub_1408D0820(a1: *(_QWORD *)(v95 + 8 * v96++), a2: v92, a3: 0);
        v95 = v125;
      }
      while ( v96 < (__int64)(*((_QWORD *)&v125 + 1) - v125) >> 3 );
    }
    sub_1408A5FB0(a1: v34);
    sub_1407E09A0();
    if ( byte_141ABEA61 != 0 )
    {
      v118 = 0;
      sub_140809040(a1: &v118, a2: 0x141919783LL, a3: 0xFFFFFFFFLL);
      LOBYTE(v97) = 1;
      sub_14009ACA0(a1: v34, a2: &v118, a3: v97, a4: 0);
      sub_140808B00(a1: &v118);
      byte_141ABEA60 = 0;
    }
    v98 = *(_QWORD *)(v7 + 320) != *(_QWORD *)(v7 + 328) && *(_BYTE *)(v7 + 1362) != 0;
    v99 = *(_BYTE *)(v7 + 1346) == 0;
    if ( (_QWORD)v125 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    v100 = v99 && v98;
    if ( (_QWORD)v122 != 0 )
      sub_1407E4890(a1: qword_141ABD470);
  }
  while ( !v100 );
  v28 = 1;
LABEL_211:
  v101 = v150;
  if ( *v150 != 0 )
  {
LABEL_212:
    if ( (byte_141ABEAB4 & 1) != 0 && dword_141ABEAB0 <= 1 )
    {
      v102 = &unk_141ABEA98;
      while ( 1 )
      {
        v102 = (_QWORD *)v102[2];
        if ( v102 == nullptr || *v102 == 0 )
          break;
        if ( (*((_BYTE *)v102 + 28) & 1) == 0 || *((int *)v102 + 6) > 1 )
          goto LABEL_224;
      }
      v103 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v103, a2: 1099915787, a3: 4504, a4: 1099812235, a5: 0, a6: 1);
      v104 = sub_1407DFD00(a1: v103, a2: *v101);
      v105 = sub_1407E0010(a1: v104, a2: 0x141941584LL);
      sub_140814F50(a1: &v122, a2: v147);
      v106 = sub_1407DFD00(a1: v105, a2: (unsigned __int64)v122 / *v101);
      v107 = sub_1407E0010(a1: v106, a2: 0x14194153ELL);
      sub_140814F50(a1: &v125, a2: v148);
      v108 = sub_1407DFD00(a1: v107, a2: (unsigned __int64)v125 / *v101);
      sub_1407E0010(a1: v108, a2: 0x1418E8B7ELL);
      if ( (sub_1407E0380(a1: &unk_141ABEA98, a2: v103) & 4) != 0 )
        sub_1407CD750();
    }
  }
LABEL_224:
  if ( *(_QWORD *)(v7 + 1568) != 0 && (byte_141ABEAB4 & 1) != 0 && dword_141ABEAB0 <= 1 )
  {
    v109 = &unk_141ABEA98;
    while ( 1 )
    {
      v109 = (_QWORD *)v109[2];
      if ( v109 == nullptr || *v109 == 0 )
        break;
      if ( (*((_BYTE *)v109 + 28) & 1) == 0 || *((int *)v109 + 6) > 1 )
        goto LABEL_235;
    }
    v101 = (_QWORD *)sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: (_DWORD)v101, a2: 1099915787, a3: 4508, a4: 1099812235, a5: 0, a6: 1);
    v110 = sub_1407DFD00(a1: v101, a2: *(_QWORD *)(v7 + 1568));
    v111 = sub_1407E0010(a1: v110, a2: 0x141941557LL);
    sub_140814F50(a1: &v122, a2: v149);
    v112 = sub_1407DFD00(a1: v111, a2: (unsigned __int64)v122 / *(_QWORD *)(v7 + 1568));
    sub_1407E0010(a1: v112, a2: 0x1418E8B7ELL);
    if ( (sub_1407E0380(a1: &unk_141ABEA98, a2: v101) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_235:
  sub_14011C160(a1: qword_141ABF5C0);
  byte_141ABEA60 = 0;
  sub_140887AA0(a1: v124);
  LOBYTE(v101) = 1;
  if ( v28 != 0 )
  {
    sub_1400A29C0(a1: v7);
    LODWORD(v101) = 0;
  }
LABEL_237:
  sub_140808B00(a1: v130);
  sub_140808B00(a1: v146);
  sub_140808B00(a1: v134);
  v113 = *a2;
  if ( *a2 != 0 )
  {
LABEL_243:
    if ( _InterlockedDecrement((volatile signed __int32 *)(v113 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v113)(a1: v113, a2: 1);
  }
  return (unsigned int)v101;
}
