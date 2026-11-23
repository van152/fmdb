char __fastcall sub_140FBC8F0(_QWORD *a1, int a2, __int64 a3)
{
  volatile signed __int32 *v4; // rdi
  unsigned __int16 *v5; // r13
  bool v6; // zf
  __int64 *v7; // r12
  _DWORD *v8; // rsi
  _QWORD *v9; // rdi
  __int64 v10; // rdx
  __int64 v11; // rbx
  __int64 v12; // r8
  __int64 v13; // rdx
  volatile signed __int32 *v15; // rdi
  __int64 v16; // rax
  int v17; // esi
  unsigned __int64 v18; // rsi
  _QWORD *v19; // r14
  _QWORD *v20; // r15
  _QWORD *v21; // rdi
  _QWORD *v22; // rbx
  __int64 v23; // rbx
  unsigned __int64 v24; // rcx
  __int64 v25; // rdx
  __int64 v26; // rbx
  bool v27; // al
  __int64 v28; // rdi
  bool v29; // al
  __int64 v30; // r14
  __int64 v31; // rcx
  unsigned __int64 v32; // rbx
  unsigned __int64 v33; // r13
  unsigned __int64 v34; // rdi
  __int64 *v35; // r15
  unsigned __int64 v36; // rax
  __int64 v37; // rbx
  unsigned __int64 v38; // rdx
  __int64 v39; // rdi
  unsigned __int64 v40; // rcx
  __int64 v41; // rbx
  __int64 v42; // rbx
  bool v43; // al
  __int64 v44; // rax
  __int64 v45; // rax
  signed __int64 v46; // r14
  __int64 *v47; // r13
  _QWORD *v48; // rax
  char v49; // si
  int v50; // eax
  volatile signed __int32 *v51; // rbx
  char v52; // si
  volatile signed __int32 *v53; // rcx
  __int64 *v54; // rbx
  __int64 *v55; // rsi
  unsigned __int16 *v56; // r13
  __int64 v57; // rcx
  __int64 v58; // rax
  __int64 v59; // rdx
  __int64 v60; // rdi
  __int64 *v61; // rbx
  __int64 v62; // rsi
  unsigned __int64 v63; // rsi
  __int64 v64; // rdi
  __int64 v65; // rax
  __int64 v66; // rcx
  __int64 v67; // rcx
  unsigned int v68; // ebx
  _DWORD *v69; // rax
  __int64 v70; // rcx
  __int64 v71; // rax
  __int64 v72; // rdx
  __int64 v73; // rdi
  __int64 v74; // rbx
  unsigned __int64 v75; // rbx
  __int64 v76; // rdi
  __int64 v77; // rax
  __int64 v78; // rcx
  __int64 v79; // rcx
  unsigned int v80; // esi
  _DWORD *v81; // rax
  int v82; // ebx
  __int64 *v83; // r12
  __int64 v84; // r14
  __int64 v85; // rax
  __int64 *v86; // r15
  __int64 v87; // r13
  unsigned __int64 v88; // rsi
  unsigned __int64 v89; // rax
  unsigned __int64 v90; // rcx
  unsigned __int64 v91; // rax
  __int64 v92; // rdi
  __int64 v93; // rsi
  __int64 *v94; // r14
  __int64 v95; // rax
  __int64 v96; // rcx
  unsigned __int64 v97; // rcx
  __int64 v98; // r8
  __int64 v99; // r14
  bool v100; // al
  volatile signed __int32 *v101; // rcx
  __int64 *v102; // [rsp+50h] [rbp-30h]
  __int64 v103; // [rsp+58h] [rbp-28h] BYREF
  __int64 v104; // [rsp+60h] [rbp-20h]
  int v105; // [rsp+68h] [rbp-18h]
  __int64 v106; // [rsp+70h] [rbp-10h]
  __int64 v107; // [rsp+78h] [rbp-8h]
  __int64 v108; // [rsp+80h] [rbp+0h]
  _BYTE v109[13]; // [rsp+88h] [rbp+8h]
  __int64 v110; // [rsp+98h] [rbp+18h]
  _QWORD *v111; // [rsp+A0h] [rbp+20h]
  __int64 *v112; // [rsp+A8h] [rbp+28h] BYREF
  volatile signed __int32 *v113; // [rsp+B0h] [rbp+30h] BYREF
  volatile signed __int32 *v114; // [rsp+B8h] [rbp+38h] BYREF
  unsigned __int64 v115; // [rsp+C0h] [rbp+40h]
  int v116; // [rsp+CCh] [rbp+4Ch] BYREF
  unsigned __int16 *v117; // [rsp+D0h] [rbp+50h]
  int v118; // [rsp+D8h] [rbp+58h] BYREF
  int v119; // [rsp+DCh] [rbp+5Ch]
  __int64 v120; // [rsp+E0h] [rbp+60h]

  v120 = -2;
  v103 = 0x80100004E554C4CLL;
  sub_1407D0F70(a1: (unsigned int)&v103, a2: (unsigned int)&v114, a3: a2, a4: (_DWORD)a1 + 72, a5: a3, a6: 1, a7: 0, 0);
  v4 = v114;
  if ( v114 == nullptr )
    return 1;
  v5 = (unsigned __int16 *)(a1 + 10);
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v114 + 40LL))(
    a1: v114,
    a2: a1 + 10,
    a3: 2);
  v6 = *((_DWORD *)v4 + 4) == 0;
  v118 = 0;
  v7 = a1;
  if ( !v6 )
  {
    v8 = (_DWORD *)a1 + 21;
    *((_DWORD *)a1 + 21) = 0;
    v119 = 0;
LABEL_4:
    sub_140FB5CC0(a1, a2: &v103, a3: *a1, a4: a1[1]);
    if ( a1[7] != 0 )
    {
      a1[7] = 0;
      a1[6] = 0;
    }
    v9 = a1 + 4;
    v10 = a1[4];
    if ( v10 != 0 )
    {
      v11 = a1[5];
      if ( v11 != 0 )
      {
        do
        {
          v13 = *(_QWORD *)(*v9 + 8 * v11-- - 8);
          if ( v13 != 0 )
            sub_1407E6420(a1: qword_141ABE200, a2: v13, a3: 16);
        }
        while ( v11 != 0 );
        v10 = v7[4];
        v12 = 8 * v7[5];
      }
      else
      {
        v12 = 0;
      }
      sub_1407E6420(a1: qword_141ABE200, a2: v10, a3: v12);
    }
    v9[1] = 0;
    *v9 = 0;
    *v8 = 0;
    goto LABEL_62;
  }
  v15 = v114;
  v16 = (*(__int64 (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v114 + 40LL))(
          a1: v114,
          a2: &v118,
          a3: 4);
  LOBYTE(v16) = *((_DWORD *)v15 + 4) == 0;
  v17 = v118;
  *((_DWORD *)a1 + 21) = 0;
  v119 = v16;
  if ( v17 <= 0 )
  {
    v8 = (_DWORD *)a1 + 21;
    goto LABEL_4;
  }
  v18 = (unsigned int)(v17 - 1);
  if ( (__int64)(a1[1] - *a1) >> 3 > v18 )
  {
    v19 = *(_QWORD **)(*a1 + 8 * v18);
    if ( v19 != nullptr )
    {
      v20 = (_QWORD *)*v19;
      v21 = (_QWORD *)v19[1];
      if ( (_QWORD *)*v19 != v21 )
      {
        v22 = (_QWORD *)*v19;
        do
        {
          if ( *v22 != 0 )
            sub_140F6BAB0();
          ++v22;
        }
        while ( v22 != v21 );
        v23 = v19[1] - (_QWORD)v21;
        sub_141758A00(a1: v20, a2: v21, a3: v23);
        v19[1] = (char *)v20 + v23;
        v21 = (_QWORD *)*v19;
      }
      if ( v21 != nullptr )
      {
        v24 = v19[2] - (_QWORD)v21;
        if ( v24 == -1 )
          v24 = *(unsigned int *)((char *)v21 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v25 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v25) >> 3 > v24)
          && (v26 = *(_QWORD *)(v25 + 8 * v24)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v26 + 32, a2: (char *)v21 - *(unsigned int *)(v26 + 120));
          v27 = *(_BYTE *)(v26 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 + 64)) != 0;
          if ( !v27 && *(_BYTE *)(v26 + 97) != 0 )
            sub_1412D33C0(a1: v26);
        }
        else
        {
          MEMORY[0x141948990](a1: (char *)v21 - *(unsigned int *)(qword_141ABD470 + 48));
        }
        v19[2] = 0;
        v19[1] = 0;
        *v19 = 0;
      }
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(a1: &unk_141B59A68);
          sub_141751048(a1: sub_1407E4B20);
          sub_141750EA0(a1: &dword_141B59AA8);
        }
      }
      if ( byte_141B59A9C != 0
        && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0xC1
        && (v28 = *(_QWORD *)(qword_141B59A80 + 192)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v28 + 32, a2: (char *)v19 - *(unsigned int *)(v28 + 120));
        v29 = *(_BYTE *)(v28 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v28 + 64)) != 0;
        if ( !v29 && *(_BYTE *)(v28 + 97) != 0 )
          sub_1412D33C0(a1: v28);
      }
      else
      {
        MEMORY[0x141948990](a1: (char *)v19 - (unsigned int)dword_141B59A98);
      }
    }
  }
  v30 = *v7;
  v31 = v7[1];
  v32 = (v31 - *v7) >> 3;
  if ( v32 <= v18 )
  {
    v117 = v5;
    v33 = v18 + 1;
    v34 = v18 + 1 - v32;
    if ( v18 + 1 >= v32 )
    {
      v35 = v7;
      v36 = (v7[2] - v30) >> 3;
      if ( v36 <= v18 )
      {
        v38 = v36 + (v36 >> 1);
        if ( v38 <= v33 )
          v38 = v18 + 1;
        v115 = v38;
        v30 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v38);
        sub_141758A10(a1: v30 + 8 * v32, a2: 0, a3: 8 * v34);
        sub_141758A00(a1: v30, a2: *v7, a3: v7[1] - *v7);
        v39 = *v7;
        if ( *v7 != 0 )
        {
          v40 = v7[2] - v39;
          if ( v40 == -1 )
            v40 = *(unsigned int *)(v39 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v41 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v41) >> 3 > v40)
            && (v42 = *(_QWORD *)(v41 + 8 * v40)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v42 + 32, a2: v39 - *(unsigned int *)(v42 + 120));
            v43 = *(_BYTE *)(v42 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v42 + 64)) != 0;
            v35 = v7;
            if ( !v43 && *(_BYTE *)(v42 + 97) != 0 )
              sub_1412D33C0(a1: v42);
          }
          else
          {
            MEMORY[0x141948990](a1: v39 - *(unsigned int *)(qword_141ABD470 + 48));
            v35 = v7;
          }
        }
        *v35 = v30;
        v35[1] = v30 + 8 * v33;
        v35[2] = v30 + 8 * v115;
      }
      else
      {
        v37 = v31 + 8 * v34;
        sub_141758A10(a1: v31, a2: 0, a3: 8 * v34);
        v7[1] = v37;
        v30 = *v7;
      }
    }
    else
    {
      v7[1] = v30 + 8 * v33;
    }
    v5 = v117;
  }
  *(_QWORD *)(v30 + 8 * v18) = 0;
LABEL_62:
  v44 = v7[8];
  if ( v44 != 0 )
    v45 = *(int *)(v44 + 24);
  else
    v45 = 0;
  v110 = v45;
  if ( v118 > 0 )
  {
    v117 = v5;
    v111 = v7 + 3;
    v46 = 0;
    v102 = v7;
    while ( 1 )
    {
      v47 = v7;
      v48 = (_QWORD *)v7[8];
      v49 = 1;
      if ( v48 != nullptr )
      {
        if ( v46 >= v110
          || (v50 = *(_DWORD *)(*v48 + (((unsigned __int64)v46 >> 3) & 0x1FFFFFFC)), !_bittest(&v50, v46)) )
        {
          v49 = 0;
        }
      }
      v113 = v114;
      _InterlockedIncrement(v114 + 2);
      v51 = v113;
      (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v113 + 40LL))(
        a1: v113,
        a2: &v116,
        a3: 4);
      if ( *((_DWORD *)v51 + 4) == 0 )
        break;
LABEL_72:
      v52 = 0;
LABEL_73:
      v53 = v113;
      if ( v113 != nullptr && _InterlockedDecrement(v113 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v53)(a1: v53, a2: 1);
      if ( v52 == 0 )
      {
        v119 = 0;
        v7 = v47;
        goto LABEL_151;
      }
      ++v46;
      v7 = v47;
      if ( v46 >= v118 )
        goto LABEL_151;
    }
    if ( v116 >= 0 )
    {
      v112 = nullptr;
      v115 = v46;
      if ( v49 != 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(a1: &unk_141B59A68);
            sub_141751048(a1: sub_1407E4B20);
            sub_141750EA0(a1: &dword_141B59AA8);
            v46 = v115;
          }
        }
        v54 = (__int64 *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
        v55 = v7;
        v56 = v117;
        if ( qword_141ABD470 == 0 )
        {
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
              v46 = v115;
            }
          }
          qword_141ABD470 = (__int64)&unk_141B59A68;
        }
        v54[2] = 0;
        v54[1] = 0;
        *v54 = 0;
        v112 = v54;
        sub_140FBD6E0(a1: v7, a2: &v112, a3: v46);
        if ( v116 <= 0 )
        {
LABEL_144:
          v47 = v55;
          v52 = 1;
          goto LABEL_73;
        }
LABEL_113:
        v82 = 0;
        while ( 2 )
        {
          v104 = -1;
          v105 = 0;
          v103 = 0x141882418LL;
          v108 = 0x76C0001076C0001LL;
          *(_QWORD *)v109 = -4170448895LL;
          *(_WORD *)&v109[10] = 0;
          v107 = 0;
          v106 = 0;
          v109[12] = 1;
          *(_WORD *)&v109[8] = 11;
          if ( (unsigned __int8)sub_1414550A0(a1: &v103, a2: &v113, a3: *v56) == 0 )
          {
            v47 = v55;
            goto LABEL_72;
          }
          v83 = v112;
          if ( v112 != nullptr )
          {
            ++*((_DWORD *)v55 + 21);
            if ( dword_141B5F2D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(a1: &dword_141B5F2D0);
              if ( dword_141B5F2D0 == -1 )
              {
                sub_1407E53D0(
                  a1: (unsigned int)&unk_141B5F280,
                  a2: 1100122401,
                  a3: 128,
                  a4: 64,
                  a5: 0,
                  a6: 0,
                  a7: 128,
                  a8: 4096);
                sub_141751048(a1: sub_140FB3BD0);
                sub_141750EA0(a1: &dword_141B5F2D0);
              }
            }
            v84 = sub_1407E58C0(a1: &unk_141B5F280, a2: 64);
            *(_QWORD *)v84 = 0x1418779A8LL;
            *(_QWORD *)(v84 + 8) = v104;
            *(_DWORD *)(v84 + 16) = v105;
            *(_QWORD *)v84 = 0x141882418LL;
            *(_QWORD *)(v84 + 53) = *(_QWORD *)&v109[5];
            *(_QWORD *)(v84 + 48) = *(_QWORD *)v109;
            *(_QWORD *)(v84 + 40) = v108;
            v85 = v106;
            *(_QWORD *)(v84 + 32) = v107;
            *(_QWORD *)(v84 + 24) = v85;
            v86 = (__int64 *)v83[1];
            if ( v86 == (__int64 *)v83[2] )
            {
              v87 = (__int64)v86 - *v83;
              v88 = v87 >> 3;
              v89 = (unsigned __int64)(v87 >> 3) >> 1;
              v90 = 0x1FFFFFFFFFFFFFFFLL - v89;
              v91 = (v87 >> 3) + v89;
              if ( v91 <= (v87 >> 3) + 1 )
                v91 = v88 + 1;
              v92 = v91;
              if ( v88 > v90 )
                v92 = 0x1FFFFFFFFFFFFFFFLL;
              v93 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v92);
              *(_QWORD *)(v93 + v87) = v84;
              v94 = (__int64 *)v83[1];
              sub_141758A00(a1: v93, a2: *v83, a3: (char *)v86 - *v83);
              if ( v94 != v86 )
                sub_141758A00(a1: v93 + v87 + 8, a2: v86, a3: v83[1] - (_QWORD)v86);
              v95 = *v83;
              v96 = v93;
              if ( *v83 != 0 )
              {
                v97 = v83[2] - v95;
                if ( v97 == -1 )
                {
                  v97 = *(unsigned int *)(v95 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                    goto LABEL_135;
                }
                else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                {
                  goto LABEL_135;
                }
                v98 = *(_QWORD *)(qword_141ABD470 + 24);
                if ( (*(_QWORD *)(qword_141ABD470 + 32) - v98) >> 3 <= v97 || (v99 = *(_QWORD *)(v98 + 8 * v97)) == 0 )
                {
LABEL_135:
                  MEMORY[0x141948990](a1: v95 - *(unsigned int *)(qword_141ABD470 + 48));
                  goto LABEL_136;
                }
                MEMORY[0x1419475D8](a1: v99 + 32, a2: v95 - *(unsigned int *)(v99 + 120));
                v100 = *(_BYTE *)(v99 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v99 + 64)) != 0;
                v96 = v93;
                if ( !v100 && *(_BYTE *)(v99 + 97) != 0 )
                {
                  sub_1412D33C0(a1: v99);
LABEL_136:
                  v96 = v93;
                }
              }
              *v83 = v96;
              v83[1] = v96 + 8 * ((v87 >> 3) + 1);
              v83[2] = v96 + 8 * v92;
              v46 = v115;
              v55 = v102;
              v56 = v117;
            }
            else
            {
              *v86 = v84;
              v83[1] += 8;
              v46 = v115;
            }
          }
          if ( ++v82 >= v116 )
            goto LABEL_144;
          continue;
        }
      }
      v55 = v7;
      v70 = v7[6];
      v71 = v7[7];
      if ( (((_BYTE)v71 + (_BYTE)v70) & 3) == 0 && v7[5] <= (unsigned __int64)(v71 + 4) >> 2 )
      {
        sub_140FBA260(a1: v111);
        v70 = v7[6];
        v71 = v7[7];
      }
      v72 = v7[4];
      v73 = v7[5];
      v74 = v70 & (4 * v73 - 1);
      v7[6] = v74;
      v75 = v71 + v74;
      v76 = (v75 >> 2) & (v73 + 0x3FFFFFFFFFFFFFFFLL);
      v77 = *(_QWORD *)(v72 + 8 * v76);
      if ( v77 == 0 )
      {
        if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
          && (v78 = *(_QWORD *)(qword_141ABE200 + 24),
              (unsigned __int64)(*(_QWORD *)(qword_141ABE200 + 32) - v78) >= 0x81)
          && (v79 = *(_QWORD *)(v78 + 128)) != 0 )
        {
          v80 = *(_DWORD *)(v79 + 88);
          v81 = (_DWORD *)sub_1407E58C0(a1: v79, a2: *(unsigned int *)(v79 + 80));
          if ( v80 == 0 )
          {
LABEL_111:
            v55 = v7;
            *(_QWORD *)(v7[4] + 8 * v76) = v81;
            v77 = *(_QWORD *)(v7[4] + 8 * v76);
            goto LABEL_112;
          }
        }
        else
        {
          v80 = *(_DWORD *)(qword_141ABE200 + 48);
          v81 = (_DWORD *)sub_141601260(a1: v80 + 16, a2: 4096);
          if ( v80 == 0 )
            goto LABEL_111;
        }
        *v81 = 16;
        v81 = (_DWORD *)((char *)v81 + v80);
        goto LABEL_111;
      }
LABEL_112:
      *(_DWORD *)(v77 + 4 * (v75 & 3)) = v46;
      ++v55[7];
      v56 = v117;
      if ( v116 > 0 )
        goto LABEL_113;
      goto LABEL_144;
    }
    v57 = v7[6];
    v58 = v7[7];
    if ( (((_BYTE)v58 + (_BYTE)v57) & 3) == 0 && v7[5] <= (unsigned __int64)(v58 + 4) >> 2 )
    {
      sub_140FBA260(a1: v111);
      v57 = v7[6];
      v58 = v7[7];
    }
    v59 = v7[4];
    v60 = v7[5];
    v61 = v7;
    v62 = v57 & (4 * v60 - 1);
    v7[6] = v62;
    v63 = v58 + v62;
    v64 = (v63 >> 2) & (v60 + 0x3FFFFFFFFFFFFFFFLL);
    v65 = *(_QWORD *)(v59 + 8 * v64);
    if ( v65 != 0 )
    {
LABEL_108:
      *(_DWORD *)(v65 + 4 * (v63 & 3)) = v46;
      ++v61[7];
      v52 = 1;
      goto LABEL_73;
    }
    if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
      && (v66 = *(_QWORD *)(qword_141ABE200 + 24), (unsigned __int64)(*(_QWORD *)(qword_141ABE200 + 32) - v66) >= 0x81)
      && (v67 = *(_QWORD *)(v66 + 128)) != 0 )
    {
      v68 = *(_DWORD *)(v67 + 88);
      v69 = (_DWORD *)sub_1407E58C0(a1: v67, a2: *(unsigned int *)(v67 + 80));
      if ( v68 == 0 )
        goto LABEL_107;
    }
    else
    {
      v68 = *(_DWORD *)(qword_141ABE200 + 48);
      v69 = (_DWORD *)sub_141601260(a1: v68 + 16, a2: 4096);
      if ( v68 == 0 )
      {
LABEL_107:
        v61 = v7;
        *(_QWORD *)(v7[4] + 8 * v64) = v69;
        v65 = *(_QWORD *)(v7[4] + 8 * v64);
        goto LABEL_108;
      }
    }
    *v69 = 16;
    v69 = (_DWORD *)((char *)v69 + v68);
    goto LABEL_107;
  }
LABEL_151:
  *((_WORD *)v7 + 40) = *((_WORD *)v7 + 41);
  v101 = v114;
  if ( v114 != nullptr && _InterlockedDecrement(v114 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v101)(a1: v101, a2: 1);
  return v119;
}
