__int64 __fastcall sub_140FDFBE0(__int64 *a1, unsigned int a2, unsigned int a3, char a4)
{
  int *v6; // rax
  int v7; // r15d
  int v8; // ebx
  __int64 v9; // rdi
  volatile signed __int32 *v10; // r14
  unsigned int v11; // eax
  __int64 v12; // rsi
  __int64 v13; // rdx
  _BYTE *v14; // rbx
  __int64 v15; // rdi
  volatile signed __int32 *v16; // rcx
  __int64 v17; // rax
  __int64 *v18; // rdi
  __int64 v19; // rcx
  volatile signed __int32 *v20; // rcx
  int *v21; // rcx
  volatile signed __int32 *v22; // rcx
  __int64 v23; // rcx
  volatile signed __int32 *v24; // rsi
  bool v25; // bl
  volatile signed __int32 *v26; // rcx
  int v28; // esi
  char v29; // bl
  volatile signed __int32 *v30; // rcx
  __int64 v31; // rcx
  __int64 v32; // rcx
  __int64 v33; // rsi
  bool v34; // r12
  __int64 v35; // rbx
  unsigned __int64 v36; // rsi
  unsigned __int64 v37; // rcx
  __int64 v38; // r14
  __int64 v39; // rax
  __int64 v40; // r14
  __int64 v41; // rbx
  __int64 v42; // r15
  int v43; // edi
  __int64 v44; // r12
  int v45; // esi
  void (__fastcall ***v46)(_QWORD, __int64); // rcx
  __int64 *v47; // r15
  __int64 v48; // r13
  __int64 *v49; // r14
  __int64 v50; // rbx
  __int64 *v51; // rax
  unsigned __int64 v52; // rsi
  __int64 v53; // rdx
  unsigned __int64 v54; // rdi
  unsigned __int64 v55; // rbx
  __int64 *v56; // rsi
  __int64 v57; // rcx
  __int64 v58; // rcx
  unsigned __int64 v59; // rsi
  unsigned __int64 v60; // r8
  unsigned __int64 v61; // rax
  unsigned __int64 v62; // r14
  __int64 v63; // rsi
  unsigned __int64 v64; // rcx
  __int64 v65; // rbx
  __int64 v66; // rbx
  bool v67; // al
  unsigned __int64 v68; // r13
  unsigned __int64 v69; // rcx
  unsigned __int64 v70; // r13
  __int64 v71; // rdi
  __int64 *v72; // rsi
  __int64 v73; // rsi
  unsigned __int64 v74; // rcx
  __int64 v75; // rbx
  __int64 v76; // rbx
  bool v77; // al
  __int64 *v78; // r13
  unsigned __int64 v79; // rbx
  unsigned __int64 v80; // r14
  __int64 v81; // rax
  __int64 *v82; // rbx
  __int64 v83; // r12
  __int64 v84; // rdx
  __int64 *v85; // r15
  __int64 v86; // rsi
  unsigned __int64 v87; // rcx
  __int64 v88; // rdi
  __int64 v89; // rdi
  bool v90; // al
  __int64 *v91; // rbx
  __int64 v92; // rcx
  __int64 v93; // rcx
  int v94; // r15d
  __int64 v95; // rbx
  void (__fastcall ***v96)(_QWORD, __int64); // rcx
  __int64 *v97; // r12
  __int64 *v98; // rdi
  __int64 v99; // r13
  unsigned __int64 v100; // rax
  unsigned __int64 v101; // r14
  unsigned __int64 v102; // rcx
  unsigned __int64 v103; // r14
  __int64 v104; // rsi
  __int64 *v105; // rbx
  __int64 v106; // rdi
  unsigned __int64 v107; // rcx
  __int64 v108; // rbx
  __int64 v109; // rbx
  bool v110; // al
  char v111[8]; // [rsp+40h] [rbp-40h] BYREF
  unsigned __int64 v112; // [rsp+48h] [rbp-38h]
  unsigned int v113; // [rsp+50h] [rbp-30h] BYREF
  int v114; // [rsp+54h] [rbp-2Ch] BYREF
  __int64 v115; // [rsp+58h] [rbp-28h] BYREF
  __int128 v116; // [rsp+60h] [rbp-20h] BYREF
  __int64 v117; // [rsp+70h] [rbp-10h] BYREF
  int v118; // [rsp+78h] [rbp-8h]
  __int16 v119; // [rsp+7Ch] [rbp-4h]
  unsigned __int64 v120; // [rsp+88h] [rbp+8h]
  unsigned int v121; // [rsp+94h] [rbp+14h]
  volatile signed __int32 *v122; // [rsp+98h] [rbp+18h] BYREF
  unsigned __int64 v123; // [rsp+A0h] [rbp+20h]
  int *v124; // [rsp+A8h] [rbp+28h] BYREF
  __int64 *v125; // [rsp+B0h] [rbp+30h]
  volatile signed __int32 *v126; // [rsp+B8h] [rbp+38h] BYREF
  int v127; // [rsp+C4h] [rbp+44h]
  __int64 v128; // [rsp+C8h] [rbp+48h]

  v128 = -2;
  LOBYTE(v127) = a4;
  v125 = a1;
  sub_14080D0E0(a1: v111, a2: 0x1418E2C24LL);
  v121 = a2;
  v113 = a2;
  v114 = 21;
  sub_1408085A0(a1: &v122, a2: &v114);
  sub_1408085A0(a1: &v124, a2: &v113);
  v126 = nullptr;
  v6 = v124;
  if ( v124 != nullptr )
  {
    _InterlockedIncrement(v124 - 1);
    v126 = v6;
    v7 = *v6;
  }
  else
  {
    v7 = 0;
  }
  v8 = v7 + 1;
  v9 = sub_1412EC810(a1: 264, a2: (unsigned int)(v7 + 1));
  v10 = (volatile signed __int32 *)v9;
  *(_DWORD *)v9 = 0;
  v11 = 0;
  if ( v7 + 1 <= 0 )
    v8 = 0;
  *(_DWORD *)(v9 + 4) = v8;
  v12 = v9 + 8;
  *(_BYTE *)(v9 + 8) = 0;
  if ( v7 <= 0 )
  {
    v14 = (_BYTE *)(v9 + 8);
    if ( v7 != 0 )
      goto LABEL_12;
  }
  else
  {
    v13 = 0x1419435F1LL;
    if ( v126 != nullptr )
      v13 = (__int64)(v126 + 1);
    sub_141758A00(a1: v9 + 8, a2: v13, a3: (unsigned int)v7);
    v14 = (_BYTE *)(v12 + (unsigned int)v7);
  }
  *v14 = 0;
  v11 = v7;
LABEL_12:
  v15 = v9 + 4;
  *(_WORD *)(v12 + v11) = 95;
  v16 = v126 - 1;
  if ( v126 != nullptr && _InterlockedDecrement(v16) == 0 )
    sub_1412EC9A0(a1: v16);
  v126 = nullptr;
  _InterlockedIncrement(v10);
  v126 = (volatile signed __int32 *)v15;
  sub_140809550(a1: &v126, a2: &v116, a3: &v122);
  v115 = 0;
  v17 = v116;
  v18 = v125;
  if ( (_QWORD)v116 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v116 - 4));
    v19 = v116;
    v115 = v17;
    if ( (_QWORD)v116 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v116 - 4)) == 0 )
      sub_1412EC9A0(a1: v19 - 4);
  }
  v20 = v126;
  if ( v126 != nullptr && _InterlockedDecrement(v126 - 1) == 0 )
    sub_1412EC9A0(a1: v20 - 1);
  v21 = v124;
  if ( v124 != nullptr && _InterlockedDecrement(v124 - 1) == 0 )
    sub_1412EC9A0(a1: v21 - 1);
  v22 = v122;
  if ( v122 != nullptr && _InterlockedDecrement(v122 - 1) == 0 )
    sub_1412EC9A0(a1: v22 - 1);
  *(_QWORD *)&v116 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v116,
    a2: (unsigned int)&v122,
    a3,
    a4: (unsigned int)&v115,
    a5: (__int64)v111,
    a6: 0,
    a7: 0,
    0);
  v23 = v115;
  if ( v115 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v115 - 4)) == 0 )
    sub_1412EC9A0(a1: v23 - 4);
  v24 = v122;
  if ( v122 == nullptr )
    return 0;
  v25 = v18[1] != *v18;
  LODWORD(v124) = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, int **, __int64))(*(_QWORD *)v122 + 40LL))(
    a1: v122,
    a2: &v124,
    a3: 4);
  if ( *((_DWORD *)v24 + 4) != 0 )
    goto LABEL_33;
  if ( (_BYTE)v127 == 0 )
  {
    v33 = (int)v124;
    v34 = v25;
    if ( v25 )
    {
      v35 = (v18[1] - *v18) >> 3;
      v36 = v35 + (int)v124;
      v37 = (v18[2] - *v18) >> 3;
      if ( v37 < v36 )
      {
        if ( v36 >> 61 == 0 )
        {
          v38 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v36);
          sub_141758A00(a1: v38, a2: *v18, a3: v18[1] - *v18);
          if ( *v18 != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          *v18 = v38;
          v18[1] = v38 + 8 * v35;
          v39 = v38 + 8 * v36;
LABEL_66:
          v18[2] = v39;
          goto LABEL_67;
        }
        goto LABEL_208;
      }
    }
    else
    {
      v40 = *v18;
      v37 = (v18[2] - *v18) >> 3;
      if ( v37 < (int)v124 )
      {
        if ( (int)v124 >= 0 )
        {
          v41 = v18[1];
          v42 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v124);
          sub_141758A00(a1: v42, a2: *v18, a3: v18[1] - *v18);
          if ( *v18 != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          *v18 = v42;
          v18[1] = v42 + v41 - v40;
          v39 = v42 + 8 * v33;
          goto LABEL_66;
        }
LABEL_208:
        sub_1400526C0(a1: v37);
      }
    }
LABEL_67:
    if ( (int)v124 <= 0 )
    {
      LOBYTE(a3) = 1;
      goto LABEL_34;
    }
    if ( v34 )
    {
      v43 = 0;
      while ( 1 )
      {
        if ( dword_141B60918 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B60918);
          if ( dword_141B60918 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B608C8,
              a2: 1100150651,
              a3: 2048,
              a4: 32,
              a5: 0,
              a6: 1,
              a7: 2048,
              a8: 4096);
            sub_141751048(a1: sub_140FE16D0);
            sub_141750EA0(a1: &dword_141B60918);
          }
        }
        v44 = sub_1407E58C0(a1: &unk_141B608C8, a2: 32);
        *(_QWORD *)v44 = 0;
        *(_QWORD *)(v44 + 8) = 0;
        *(_QWORD *)(v44 + 16) = 0;
        *(_DWORD *)(v44 + 24) = 0;
        *(_WORD *)(v44 + 28) = -1;
        *(_QWORD *)&v116 = v122;
        if ( v122 != nullptr )
          _InterlockedIncrement(v122 + 2);
        v45 = sub_14118AD80(a1: v44, a2: &v116, a3: v121);
        v46 = (void (__fastcall ***)(_QWORD, __int64))v116;
        v47 = v125;
        if ( (_QWORD)v116 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v116 + 8)) == 0 )
          (**v46)(a1: v46, a2: 1);
        if ( (_BYTE)v45 == 0 )
          goto LABEL_33;
        LODWORD(v123) = v43;
        v127 = v45;
        v48 = *v47;
        v49 = (__int64 *)v47[1];
        v50 = (__int64)v49 - *v47;
        v51 = (__int64 *)*v47;
        if ( v50 > 0 )
        {
          v52 = (unsigned __int64)v50 >> 3;
          v51 = (__int64 *)*v47;
          v53 = (unsigned __int64)v50 >> 3;
          do
          {
            v53 = (unsigned __int64)v53 >> 1;
            if ( *(_DWORD *)(v51[v53] + 24) < *(_DWORD *)(v44 + 24) )
            {
              v51 += v53 + 1;
              v53 = v52 + ~v53;
            }
            v52 = v53;
          }
          while ( v53 > 0 );
        }
        if ( v51 == v49 )
          break;
        v54 = ((__int64)v51 - v48) >> 3;
        if ( *(_DWORD *)(*v51 + 24) == *(_DWORD *)(v44 + 24) )
        {
          v55 = v50 >> 3;
          if ( v55 > v54 )
          {
            v56 = *(__int64 **)(v48 + 8 * v54);
            if ( v56 != nullptr )
            {
              sub_140E44A40(a1: v56 + 2);
              v57 = v56[1];
              if ( v57 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v57 - 4)) == 0 )
                sub_1412EC9A0(a1: v57 - 4);
              v58 = *v56;
              if ( *v56 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v58 - 4)) == 0 )
                sub_1412EC9A0(a1: v58 - 4);
              sub_140FE1570(a1: v56);
              v48 = *v47;
              v49 = (__int64 *)v47[1];
              v55 = ((__int64)v49 - *v47) >> 3;
            }
          }
          if ( v55 <= v54 )
          {
            v59 = v54 + 1;
            v60 = v54 + 1 - v55;
            if ( v54 + 1 < v55 )
            {
              v47[1] = v48 + 8 * v59;
            }
            else if ( v54 + 1 > v55 )
            {
              v61 = (v47[2] - v48) >> 3;
              if ( v61 >= v59 )
              {
                v91 = &v49[v60];
                sub_141758A10(a1: v49, a2: 0, a3: 8 * v60);
                v47[1] = (__int64)v91;
                v48 = *v47;
              }
              else
              {
                v120 = v54 + 1 - v55;
                v37 = v59 >> 61;
                if ( v59 >> 61 != 0 )
                  goto LABEL_208;
                v62 = v61 + (v61 >> 1);
                v112 = v54 + 1;
                if ( v62 <= v59 )
                  v62 = v54 + 1;
                if ( v61 > 0x1FFFFFFFFFFFFFFFLL - (v61 >> 1) )
                  v62 = 0x1FFFFFFFFFFFFFFFLL;
                v48 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v62);
                sub_141758A10(a1: v48 + 8 * v55, a2: 0, a3: 8 * v120);
                sub_141758A00(a1: v48, a2: *v47, a3: v47[1] - *v47);
                v63 = *v47;
                if ( *v47 != 0 )
                {
                  v64 = v47[2] - v63;
                  if ( v64 == -1 )
                    v64 = *(unsigned int *)(v63 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v65 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v65) >> 3 > v64)
                    && (v66 = *(_QWORD *)(v65 + 8 * v64)) != 0 )
                  {
                    MEMORY[0x1419475D8](a1: v66 + 32, a2: v63 - *(unsigned int *)(v66 + 120));
                    v67 = *(_BYTE *)(v66 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v66 + 64)) != 0;
                    if ( !v67 && *(_BYTE *)(v66 + 97) != 0 )
                      sub_1412D33C0(a1: v66);
                  }
                  else
                  {
                    MEMORY[0x141948990](a1: v63 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                }
                *v47 = v48;
                v47[1] = v48 + 8 * v112;
                v47[2] = v48 + 8 * v62;
              }
            }
          }
          *(_QWORD *)(v48 + 8 * v54) = v44;
        }
        else
        {
          v78 = (__int64 *)(v48 + 8 * v54);
          if ( v49 == (__int64 *)v47[2] )
          {
            v79 = v50 >> 3;
            v80 = v79 + (v79 >> 1);
            v120 = v79 + 1;
            if ( v80 <= v79 + 1 )
              v80 = v79 + 1;
            if ( v79 > 0x1FFFFFFFFFFFFFFFLL - (v79 >> 1) )
              v80 = 0x1FFFFFFFFFFFFFFFLL;
            v81 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v80);
            v82 = v47;
            *(_QWORD *)(v81 + 8 * v54) = v44;
            v83 = v81;
            v84 = *v47;
            v85 = (__int64 *)v47[1];
            sub_141758A00(a1: v81, a2: v84, a3: (char *)v78 - v84);
            if ( v85 != v78 )
              sub_141758A00(a1: v83 + 8 * v54 + 8, a2: v78, a3: v82[1] - (_QWORD)v78);
            v86 = *v82;
            if ( *v82 != 0 )
            {
              v87 = v82[2] - v86;
              if ( v87 == -1 )
                v87 = *(unsigned int *)(v86 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v88 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v88) >> 3 > v87)
                && (v89 = *(_QWORD *)(v88 + 8 * v87)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v89 + 32, a2: v86 - *(unsigned int *)(v89 + 120));
                v90 = *(_BYTE *)(v89 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v89 + 64)) != 0;
                v82 = v125;
                if ( !v90 && *(_BYTE *)(v89 + 97) != 0 )
                  sub_1412D33C0(a1: v89);
              }
              else
              {
                MEMORY[0x141948990](a1: v86 - *(unsigned int *)(qword_141ABD470 + 48));
                v82 = v125;
              }
            }
            *v82 = v83;
            v82[1] = v83 + 8 * v120;
            v82[2] = v83 + 8 * v80;
            goto LABEL_72;
          }
          if ( v49 == v78 )
            goto LABEL_131;
          *v49 = *(v49 - 1);
          v47[1] += 8;
          sub_141758A00(a1: v78 + 1, a2: v78, a3: (char *)(v49 - 1) - (char *)v78);
          *v78 = v44;
        }
LABEL_72:
        a3 = v127;
        v43 = v123 + 1;
        if ( (int)v123 + 1 >= (int)v124 )
          goto LABEL_34;
      }
      if ( v49 == (__int64 *)v47[2] )
      {
        v68 = (unsigned __int64)(v50 >> 3) >> 1;
        v69 = 0x1FFFFFFFFFFFFFFFLL - v68;
        v70 = (v50 >> 3) + v68;
        v120 = (v50 >> 3) + 1;
        if ( v70 <= v120 )
          v70 = (v50 >> 3) + 1;
        if ( v50 >> 3 > v69 )
          v70 = 0x1FFFFFFFFFFFFFFFLL;
        v71 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v70);
        *(_QWORD *)(v71 + v50) = v44;
        v72 = (__int64 *)v47[1];
        sub_141758A00(a1: v71, a2: *v47, a3: (char *)v49 - *v47);
        if ( v72 != v49 )
          sub_141758A00(a1: v71 + v50 + 8, a2: v49, a3: v47[1] - (_QWORD)v49);
        v73 = *v47;
        if ( *v47 != 0 )
        {
          v74 = v47[2] - v73;
          if ( v74 == -1 )
            v74 = *(unsigned int *)(v73 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v75 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v75) >> 3 > v74)
            && (v76 = *(_QWORD *)(v75 + 8 * v74)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v76 + 32, a2: v73 - *(unsigned int *)(v76 + 120));
            v77 = *(_BYTE *)(v76 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v76 + 64)) != 0;
            v47 = v125;
            if ( !v77 && *(_BYTE *)(v76 + 97) != 0 )
              sub_1412D33C0(a1: v76);
          }
          else
          {
            MEMORY[0x141948990](a1: v73 - *(unsigned int *)(qword_141ABD470 + 48));
            v47 = v125;
          }
        }
        *v47 = v71;
        v47[1] = v71 + 8 * v120;
        v47[2] = v71 + 8 * v70;
        goto LABEL_72;
      }
LABEL_131:
      *v49 = v44;
      v47[1] += 8;
      goto LABEL_72;
    }
    v94 = 0;
    while ( 1 )
    {
      if ( dword_141B60918 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B60918);
        if ( dword_141B60918 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B608C8,
            a2: 1100150651,
            a3: 2048,
            a4: 32,
            a5: 0,
            a6: 1,
            a7: 2048,
            a8: 4096);
          sub_141751048(a1: sub_140FE16D0);
          sub_141750EA0(a1: &dword_141B60918);
        }
      }
      v95 = sub_1407E58C0(a1: &unk_141B608C8, a2: 32);
      *(_QWORD *)v95 = 0;
      *(_QWORD *)(v95 + 8) = 0;
      *(_QWORD *)(v95 + 16) = 0;
      *(_DWORD *)(v95 + 24) = 0;
      *(_WORD *)(v95 + 28) = -1;
      *(_QWORD *)&v116 = v122;
      if ( v122 != nullptr )
        _InterlockedIncrement(v122 + 2);
      a3 = sub_14118AD80(a1: v95, a2: &v116, a3: v121);
      v96 = (void (__fastcall ***)(_QWORD, __int64))v116;
      if ( (_QWORD)v116 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v116 + 8)) == 0 )
        (**v96)(a1: v96, a2: 1);
      if ( (_BYTE)a3 == 0 )
        goto LABEL_34;
      v97 = v125;
      v98 = (__int64 *)v125[1];
      if ( v98 == (__int64 *)v125[2] )
        break;
      *v98 = v95;
      v97[1] += 8;
LABEL_176:
      if ( ++v94 >= (int)v124 )
        goto LABEL_34;
    }
    v127 = a3;
    v99 = (__int64)v98 - *v125;
    v100 = v99 >> 3;
    v101 = (unsigned __int64)(v99 >> 3) >> 1;
    v102 = 0x1FFFFFFFFFFFFFFFLL - v101;
    v103 = (v99 >> 3) + v101;
    v123 = (v99 >> 3) + 1;
    if ( v103 <= v123 )
      v103 = v100 + 1;
    if ( v100 > v102 )
      v103 = 0x1FFFFFFFFFFFFFFFLL;
    v104 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v103);
    *(_QWORD *)(v104 + v99) = v95;
    v105 = (__int64 *)v97[1];
    sub_141758A00(a1: v104, a2: *v97, a3: (char *)v98 - *v97);
    if ( v105 != v98 )
      sub_141758A00(a1: v104 + v99 + 8, a2: v98, a3: v97[1] - (_QWORD)v98);
    v106 = *v97;
    a3 = v127;
    if ( *v97 == 0 )
    {
LABEL_201:
      *v97 = v104;
      v97[1] = v104 + 8 * v123;
      v97[2] = v104 + 8 * v103;
      goto LABEL_176;
    }
    v107 = v97[2] - v106;
    if ( v107 == -1 )
    {
      v107 = *(unsigned int *)(v106 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_200:
        MEMORY[0x141948990](a1: v106 - *(unsigned int *)(qword_141ABD470 + 48));
        v97 = v125;
        goto LABEL_201;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_200;
    }
    v108 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v108) >> 3 > v107 )
    {
      v109 = *(_QWORD *)(v108 + 8 * v107);
      if ( v109 != 0 )
      {
        MEMORY[0x1419475D8](a1: v109 + 32, a2: v106 - *(unsigned int *)(v109 + 120));
        v110 = *(_BYTE *)(v109 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v109 + 64)) != 0;
        v97 = v125;
        if ( !v110 && *(_BYTE *)(v109 + 97) != 0 )
          sub_1412D33C0(a1: v109);
        goto LABEL_201;
      }
    }
    goto LABEL_200;
  }
  LOBYTE(a3) = 1;
  if ( (int)v124 <= 0 )
    goto LABEL_34;
  v28 = 0;
  while ( 1 )
  {
    v116 = 0;
    v118 = 0;
    v117 = 0;
    v119 = -1;
    v126 = v122;
    if ( v122 != nullptr )
      _InterlockedIncrement(v122 + 2);
    v29 = sub_14118AD80(a1: &v116, a2: &v126, a3: v121);
    v30 = v126;
    if ( v126 != nullptr && _InterlockedDecrement(v126 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v30)(a1: v30, a2: 1);
    if ( v29 == 0 )
      break;
    sub_14118AB90(a1: &v116);
    sub_140E44A40(a1: &v117);
    v31 = *((_QWORD *)&v116 + 1);
    if ( *((_QWORD *)&v116 + 1) != 0
      && _InterlockedDecrement((volatile signed __int32 *)(*((_QWORD *)&v116 + 1) - 4LL)) == 0 )
    {
      sub_1412EC9A0(a1: v31 - 4);
    }
    v32 = v116;
    if ( (_QWORD)v116 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v116 - 4)) == 0 )
      sub_1412EC9A0(a1: v32 - 4);
    if ( ++v28 >= (int)v124 )
      goto LABEL_34;
  }
  sub_140E44A40(a1: &v117);
  v92 = *((_QWORD *)&v116 + 1);
  if ( *((_QWORD *)&v116 + 1) != 0
    && _InterlockedDecrement((volatile signed __int32 *)(*((_QWORD *)&v116 + 1) - 4LL)) == 0 )
  {
    sub_1412EC9A0(a1: v92 - 4);
  }
  v93 = v116;
  if ( (_QWORD)v116 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v116 - 4)) == 0 )
    sub_1412EC9A0(a1: v93 - 4);
LABEL_33:
  a3 = 0;
LABEL_34:
  v26 = v122;
  if ( v122 != nullptr && _InterlockedDecrement(v122 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v26)(a1: v26, a2: 1);
  return a3;
}
