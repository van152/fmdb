__int64 __fastcall sub_140DC1D30(
        __int64 a1,
        __int64 *a2,
        char a3,
        __int64 a4,
        int a5,
        int a6,
        unsigned __int8 a7,
        __int64 a8)
{
  __int64 v9; // r14
  __int64 v10; // rdi
  __int64 v11; // rax
  __int64 v12; // rbx
  __int64 *v13; // rdi
  __int16 v14; // ax
  __int64 v15; // r13
  __int64 v16; // r14
  __int64 v17; // rbx
  __int64 v18; // r12
  __int64 v19; // rsi
  unsigned __int64 v20; // rcx
  __int64 v21; // r8
  __int64 v22; // rcx
  bool v23; // al
  int v24; // esi
  _BYTE *v25; // rsi
  __int16 *v26; // r13
  __int64 v27; // rbx
  __int64 v28; // r8
  bool v29; // zf
  _DWORD *v30; // rdi
  _DWORD *v31; // rdi
  __int64 v32; // r8
  bool v33; // bl
  _BOOL8 v34; // rax
  __int64 v35; // rdi
  __int64 v36; // rsi
  __int16 *v37; // rdx
  _BYTE *v38; // rsi
  __int16 *v39; // rbx
  __int64 v40; // rax
  __int64 v41; // rdi
  __int64 v42; // r8
  __int16 *v43; // rbx
  unsigned __int8 *v44; // rbx
  __int64 v45; // r8
  unsigned __int16 v46; // bx
  __int64 v47; // rdi
  char v48; // al
  __int64 v49; // r8
  _QWORD *v50; // rdi
  _DWORD *v51; // rcx
  __int64 v52; // r8
  __int64 v53; // rax
  __int64 v54; // rdx
  __int64 v55; // rcx
  _QWORD *v56; // rdi
  __int64 v57; // r8
  _DWORD *v58; // rcx
  __int64 v59; // r8
  __int64 v60; // rdx
  __int64 v61; // rcx
  _QWORD *v62; // rdi
  __int64 v63; // r8
  _DWORD *v64; // rcx
  __int64 v65; // r8
  void (__fastcall ****v66)(_QWORD, __int64); // rdi
  void (__fastcall ***v67)(_QWORD, __int64); // rax
  void (__fastcall ***v68)(_QWORD, __int64); // rcx
  void (__fastcall ***v69)(_QWORD, __int64); // rdi
  __int64 v70; // rax
  __int64 v71; // rdx
  __int64 v72; // rcx
  _QWORD *v73; // rdi
  __int64 v74; // r8
  __int64 v75; // r8
  __int64 v76; // rcx
  __int64 v77; // rcx
  __int64 v78; // rcx
  __int64 v79; // rcx
  unsigned __int64 v80; // rcx
  __int64 v81; // rax
  unsigned __int64 v82; // rcx
  __int64 v83; // r13
  int v84; // ebx
  char v85; // si
  int v86; // ebx
  int v87; // ebx
  __int64 *v88; // rsi
  char v89; // al
  __int64 v90; // r15
  char v91; // r8
  char v92; // r9
  char v93; // r10
  char v94; // r11
  char v95; // r12
  char v96; // r13
  char v97; // dl
  unsigned __int64 v98; // rcx
  _BYTE *v99; // r14
  unsigned int v100; // eax
  void (__fastcall ***v101)(_QWORD, __int64); // rcx
  char v103; // [rsp+30h] [rbp-50h]
  int v104; // [rsp+30h] [rbp-50h]
  _BYTE *v105; // [rsp+48h] [rbp-38h]
  __int64 v106; // [rsp+50h] [rbp-30h]
  _BYTE *v107; // [rsp+58h] [rbp-28h]
  __int64 v108; // [rsp+60h] [rbp-20h]
  __int64 v109; // [rsp+60h] [rbp-20h]
  _BYTE *v110; // [rsp+68h] [rbp-18h]
  __int64 v111; // [rsp+70h] [rbp-10h]
  _BYTE *v112; // [rsp+70h] [rbp-10h]
  __int64 v113; // [rsp+80h] [rbp+0h]
  _BYTE *v114; // [rsp+80h] [rbp+0h]
  __int64 v115; // [rsp+80h] [rbp+0h]
  void (__fastcall ***v116)(_QWORD, __int64); // [rsp+88h] [rbp+8h] BYREF
  char v117; // [rsp+95h] [rbp+15h]
  __int16 v118; // [rsp+96h] [rbp+16h] BYREF
  _DWORD *v119; // [rsp+98h] [rbp+18h] BYREF
  __int16 *v120; // [rsp+A0h] [rbp+20h]
  __int64 v121; // [rsp+A8h] [rbp+28h]
  unsigned __int8 *v122; // [rsp+B0h] [rbp+30h]
  unsigned __int8 v123; // [rsp+BFh] [rbp+3Fh] BYREF
  _QWORD v124[8]; // [rsp+C0h] [rbp+40h] BYREF

  v124[0] = -2;
  v9 = a1;
  LODWORD(v10) = a7;
  v11 = *a2;
  v119 = (_DWORD *)v11;
  if ( v11 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v11 + 8));
  v12 = a1 - 248;
  v122 = nullptr;
  v121 = 0;
  v120 = nullptr;
  if ( a7 != 0 )
  {
    v117 = a3;
    v120 = &v118;
    v121 = 2;
    v122 = (unsigned __int8 *)&v119;
    v106 = a1 - 248;
    if ( v119 != nullptr )
    {
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, &v118, 2);
      v120 = nullptr;
      v121 = 0;
      v122 = nullptr;
      if ( v118 > 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
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
        v13 = (__int64 *)sub_1407E4490(&unk_141B59A68, 24);
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
        }
        v13[2] = 0;
        v13[1] = 0;
        *v13 = 0;
        v113 = v9;
        *(_QWORD *)(v9 - 168) = v13;
        v14 = v118;
        v15 = v118;
        v16 = *v13;
        if ( (v13[2] - *v13) >> 1 < (unsigned __int64)v118 )
        {
          v108 = a4;
          if ( v118 < 0 )
            sub_1400526C0();
          v17 = v13[1];
          v18 = sub_1407E4490(qword_141ABD470, 2LL * v118);
          sub_141758A00(v18, *v13, v13[1] - *v13);
          v19 = *v13;
          if ( *v13 != 0 )
          {
            v20 = v13[2] - v19;
            if ( v20 == -1 )
              v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v21 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v20)
              && (v22 = *(_QWORD *)(v21 + 8 * v20)) != 0 )
            {
              v111 = v22;
              MEMORY[0x1419475D8](v22 + 32, v19 - *(unsigned int *)(v22 + 120));
              v23 = *(_BYTE *)(v111 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v111 + 64)) != 0;
              if ( !v23 && *(_BYTE *)(v111 + 97) != 0 )
                sub_1412D33C0();
            }
            else
            {
              MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *v13 = v18;
          v13[1] = v18 + v17 - v16;
          v13[2] = v18 + 2 * v15;
          v14 = v118;
          a4 = v108;
        }
        v9 = v113;
        if ( v14 > 0 )
        {
          v24 = 0;
          do
          {
            LOWORD(v116) = 25548;
            if ( v121 != 0 && v119 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
            v122 = nullptr;
            v121 = 0;
            v120 = nullptr;
            (*(void (__fastcall **)(_DWORD *, unsigned __int8 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, &v123, 1);
            (*(void (__fastcall **)(_DWORD *, void (__fastcall ****)(_QWORD, __int64), __int64))(*(_QWORD *)v119 + 40LL))(
              v119,
              &v116,
              2);
            if ( v123 <= 2u && ((unsigned __int16)v116 & 0x1FC0) == 0x380 )
              LOWORD(v116) = (unsigned __int16)v116 & 0xE03F | 0x3C0;
            if ( v119[4] != 0 )
              goto LABEL_46;
            sub_140DC3060(v106, (unsigned __int16)v116);
          }
          while ( (__int16)++v24 < v118 );
        }
      }
    }
    else
    {
      v122 = nullptr;
      v121 = 0;
      v120 = nullptr;
    }
    if ( v122 == (unsigned __int8 *)(v9 - 40) )
    {
      v25 = (_BYTE *)(v9 - 30);
      v114 = (_BYTE *)(v9 - 29);
      v107 = (_BYTE *)(v9 - 28);
      v112 = (_BYTE *)(v9 - 27);
      v105 = (_BYTE *)(v9 - 26);
      v26 = (__int16 *)(v9 - 25);
      v27 = v9 - 232;
      v29 = v121 == -15;
      v28 = v121 + 15;
      v121 += 15;
      v122 = (unsigned __int8 *)(v9 - 25);
      if ( v29 )
        goto LABEL_41;
    }
    else
    {
      if ( v121 != 0 && v119 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v121);
      v120 = (__int16 *)(v9 - 40);
      v25 = (_BYTE *)(v9 - 30);
      v114 = (_BYTE *)(v9 - 29);
      v107 = (_BYTE *)(v9 - 28);
      v112 = (_BYTE *)(v9 - 27);
      v105 = (_BYTE *)(v9 - 26);
      v121 = 15;
      v26 = (__int16 *)(v9 - 25);
      v122 = (unsigned __int8 *)(v9 - 25);
      v27 = v9 - 232;
      v28 = 15;
    }
    if ( v119 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v28);
LABEL_41:
    v122 = nullptr;
    v121 = 0;
    v120 = nullptr;
    LOBYTE(v116) = 0;
    *(_DWORD *)(v27 + 56) = 0;
    *(_QWORD *)(v27 + 48) = 0;
    *(_QWORD *)(v27 + 40) = 0;
    *(_QWORD *)(v27 + 32) = 0;
    *(_QWORD *)(v27 + 24) = 0;
    *(_QWORD *)(v27 + 16) = 0;
    *(_QWORD *)(v27 + 8) = 0;
    v30 = v119;
    (*(void (__fastcall **)(_DWORD *, void (__fastcall ****)(_QWORD, __int64), __int64))(*(_QWORD *)v119 + 40LL))(
      v119,
      &v116,
      1);
    if ( v30[4] != 0 )
      goto LABEL_46;
    v31 = v119;
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v119 + 40LL))(
      v119,
      v27 + 8,
      51 - (((unsigned __int8)v116 < 0xAu) - 1LL));
    if ( v31[4] != 0 )
      goto LABEL_46;
    if ( (unsigned __int8)v116 <= 9u )
      *(_BYTE *)(v27 + 59) = 0;
    if ( v119[4] != 0 )
      goto LABEL_46;
    v110 = v25;
    if ( v122 == (unsigned __int8 *)(v9 - 64) )
    {
      v32 = v121 + 4;
    }
    else
    {
      if ( v121 != 0 )
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v121);
      v120 = (__int16 *)(v9 - 64);
      v32 = 4;
    }
    v121 = v32;
    v122 = (unsigned __int8 *)(v9 - 60);
    v33 = HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0;
    v34 = !v33;
    v35 = 4 * v34 + 4;
    v36 = 4 * v34 - 148;
    if ( v32 != 0 && v119 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
    v120 = (__int16 *)(v9 - 152);
    v121 = v35;
    v122 = (unsigned __int8 *)(v9 + v36);
    v37 = (__int16 *)(v9 - 144);
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
    {
      v38 = v110;
      if ( v33 )
      {
        v39 = (__int16 *)(v9 - 60);
        if ( v119 != nullptr )
        {
          (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v119 + 40LL))(v119, v9 - 152, v35);
          v37 = (__int16 *)(v9 - 144);
          v38 = v110;
        }
        v120 = v37;
        v40 = -140;
        v41 = 4;
LABEL_68:
        v121 = v41;
        v122 = (unsigned __int8 *)(v9 + v40);
        if ( v119 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v37, v41);
        v120 = v39;
        v121 = 8;
        v122 = (unsigned __int8 *)(v9 - 52);
        if ( v119 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v39, 8);
        v120 = v26;
        v121 = 1;
        v122 = (unsigned __int8 *)(v9 - 24);
        v42 = 6;
        v43 = v26;
        if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDCBu )
        {
          v43 = (__int16 *)(v9 - 23);
          if ( v119 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v26, 1);
          v120 = (__int16 *)(v9 - 23);
          v42 = 4;
        }
        v121 = v42;
        v122 = (unsigned __int8 *)(v9 - 19);
        if ( v119 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v43);
        v120 = (__int16 *)(v9 - 52);
        v121 = 8;
        v122 = (unsigned __int8 *)(v9 - 44);
        v123 = 0;
        v44 = &v123;
        if ( (unsigned __int8 *)(v9 - 44) == &v123 )
        {
          v45 = 9;
          v44 = (unsigned __int8 *)(v9 - 52);
        }
        else
        {
          if ( v119 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v119 + 40LL))(v119, v9 - 52, 8);
          v120 = (__int16 *)&v123;
          v45 = 1;
        }
        v121 = v45;
        v122 = (unsigned __int8 *)v124;
        if ( v119 != nullptr )
          (*(void (__fastcall **)(_DWORD *, unsigned __int8 *))(*(_QWORD *)v119 + 40LL))(v119, v44);
        v122 = nullptr;
        v121 = 0;
        v120 = nullptr;
        if ( v123 != 0 )
        {
          v46 = *(_WORD *)(a4 + 1416);
          v47 = sub_140DC33A0(v106);
          if ( v121 != 0 && v119 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
          v122 = nullptr;
          v121 = 0;
          v120 = nullptr;
          v48 = v46 < 0xDC9u ? sub_1413F97A0(v47, &v119) : sub_1413F90A0(v47, &v119);
          if ( v48 == 0 )
            goto LABEL_46;
        }
        if ( v122 == &v123 )
        {
          v49 = v121 + 1;
          v121 = v49;
          v122 = (unsigned __int8 *)v124;
          if ( v49 == 0 )
          {
LABEL_101:
            v122 = nullptr;
            v121 = 0;
            v120 = nullptr;
            if ( v123 == 0 )
              goto LABEL_110;
            v50 = (_QWORD *)sub_140DC3550(24);
            if ( qword_141ABD470 == 0 )
              qword_141ABD470 = ((__int64 (*)(void))sub_1407E4940)();
            v50[2] = 0;
            v50[1] = 0;
            *v50 = 0;
            *(_QWORD *)(v9 - 128) = v50;
            if ( v121 != 0 && v119 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
            v122 = nullptr;
            v121 = 0;
            v120 = nullptr;
            if ( (unsigned __int8)sub_1413FE0E0(v50, &v119) == 0 )
              goto LABEL_46;
            if ( v122 == &v123 )
            {
              v52 = v121 + 1;
              v29 = v121++ == -1;
              v122 = (unsigned __int8 *)v124;
              if ( v29 )
              {
LABEL_115:
                v122 = nullptr;
                v121 = 0;
                v120 = nullptr;
                if ( v123 == 0 )
                  goto LABEL_124;
                v53 = sub_1407E4940(v51, v37, v52);
                v56 = (_QWORD *)sub_1407E4490(v53, 24);
                if ( qword_141ABD470 == 0 )
                  qword_141ABD470 = sub_1407E4940(v55, v54, v57);
                v56[2] = 0;
                v56[1] = 0;
                *v56 = 0;
                *(_QWORD *)(v9 - 104) = v56;
                if ( v121 != 0 && v119 != nullptr )
                  (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
                v122 = nullptr;
                v121 = 0;
                v120 = nullptr;
                if ( (unsigned __int8)sub_1413FE6B0(v56, &v119) == 0 )
                  goto LABEL_46;
                if ( v122 == &v123 )
                {
                  v59 = v121 + 1;
                  v29 = v121++ == -1;
                  v122 = (unsigned __int8 *)v124;
                  if ( v29 )
                  {
LABEL_129:
                    v122 = nullptr;
                    v121 = 0;
                    v120 = nullptr;
                    if ( v123 == 0 )
                      goto LABEL_138;
                    v62 = (_QWORD *)sub_140DC3600(v58, v37, v59);
                    if ( qword_141ABD470 == 0 )
                      qword_141ABD470 = sub_1407E4940(v61, v60, v63);
                    v62[2] = 0;
                    v62[1] = 0;
                    *v62 = 0;
                    *(_QWORD *)(v9 - 80) = v62;
                    if ( v121 != 0 && v119 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
                    v122 = nullptr;
                    v121 = 0;
                    v120 = nullptr;
                    if ( (unsigned __int8)sub_1413FECE0(v62, &v119) == 0 )
                      goto LABEL_46;
                    if ( v122 == &v123 )
                    {
                      v65 = v121 + 1;
                      v29 = v121++ == -1;
                      v122 = (unsigned __int8 *)v124;
                      if ( v29 )
                        goto LABEL_143;
                    }
                    else
                    {
LABEL_138:
                      if ( v121 != 0 && v119 != nullptr )
                        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
                      v120 = (__int16 *)&v123;
                      v121 = 1;
                      v122 = (unsigned __int8 *)v124;
                      v65 = 1;
                    }
                    v64 = v119;
                    if ( v119 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v65);
LABEL_143:
                    v122 = nullptr;
                    v121 = 0;
                    v120 = nullptr;
                    if ( v123 == 0 )
                      goto LABEL_153;
                    sub_140DC36B0(&v116, v37, v65);
                    v66 = (void (__fastcall ****)(_QWORD, __int64))(v9 - 136);
                    if ( (void (__fastcall ****)(_QWORD, __int64))(v9 - 136) != &v116 )
                    {
                      v67 = v116;
                      v116 = nullptr;
                      v68 = *v66;
                      *v66 = v67;
                      if ( v68 == nullptr )
                        goto LABEL_149;
                      (**v68)(v68, 1);
                    }
                    if ( v116 != nullptr )
                      (**v116)(v116, 1);
LABEL_149:
                    v69 = *v66;
                    if ( v121 != 0 && v119 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
                    v122 = nullptr;
                    v121 = 0;
                    v120 = nullptr;
                    v38 = v110;
                    if ( ((unsigned __int8 (__fastcall *)(_QWORD, _DWORD **))(*v69)[1])(v69, &v119) == 0 )
                      goto LABEL_46;
LABEL_153:
                    LODWORD(v10) = a7;
                    if ( *(unsigned __int16 *)(a4 + 1416) < 0xDC1u )
                    {
LABEL_187:
                      v76 = (unsigned __int8)*v114;
                      if ( (_BYTE)v76 != 66 && (unsigned __int8)sub_14087A360(v76, v37, v65) == 0 )
                        *v114 = 0;
                      v77 = (unsigned __int8)*v107;
                      if ( (_BYTE)v77 != 66 && (unsigned __int8)sub_14087A360(v77, v37, v65) == 0 )
                        *v107 = *v114;
                      v78 = (unsigned __int8)*v112;
                      if ( (_BYTE)v78 != 66 && (unsigned __int8)sub_14087A360(v78, v37, v65) == 0 )
                        *v112 = 0;
                      v79 = (unsigned __int8)*v105;
                      if ( (_BYTE)v79 != 66 && (unsigned __int8)sub_14087A360(v79, v37, v65) == 0 )
                        *v105 = 0;
                      v80 = (unsigned __int8)*v38;
                      v81 = 0xC3000000000LL;
                      if ( v80 <= 0x2B && _bittest64(&v81, v80) )
                        *v38 = 0;
                      v82 = *(unsigned __int8 *)v26;
                      a3 = v117;
                      if ( v82 <= 0x2B && _bittest64(&v81, v82) )
                        *(_BYTE *)v26 = 0;
                      v12 = v106;
                      goto LABEL_206;
                    }
                    if ( v122 == &v123 )
                    {
                      v65 = v121 + 1;
                      v121 = v65;
                      v122 = (unsigned __int8 *)v124;
                      if ( v65 == 0 )
                        goto LABEL_172;
                    }
                    else
                    {
                      if ( v121 != 0 && v119 != nullptr )
                        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(
                          v119,
                          v120,
                          v121);
                      v120 = (__int16 *)&v123;
                      v121 = 1;
                      v122 = (unsigned __int8 *)v124;
                      v65 = 1;
                    }
                    v64 = v119;
                    if ( v119 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v65);
LABEL_172:
                    v122 = nullptr;
                    v121 = 0;
                    v120 = nullptr;
                    if ( v123 != 0 )
                    {
                      v70 = sub_1407E4940(v64, v37, v65);
                      v73 = (_QWORD *)sub_1407E4490(v70, 24);
                      if ( qword_141ABD470 == 0 )
                        qword_141ABD470 = sub_1407E4940(v72, v71, v74);
                      v73[2] = 0;
                      v73[1] = 0;
                      *v73 = 0;
                      *(_QWORD *)(v9 - 96) = v73;
                      if ( v121 != 0 && v119 != nullptr )
                        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
                      v122 = nullptr;
                      v121 = 0;
                      v120 = nullptr;
                      if ( (unsigned __int8)sub_1413FF240(v73, &v119) == 0 )
                      {
LABEL_46:
                        LODWORD(v10) = 0;
                        goto LABEL_238;
                      }
                    }
                    LODWORD(v10) = a7;
                    if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDD0u )
                    {
                      if ( v122 == (unsigned __int8 *)(v9 - 19) )
                      {
                        v75 = v121 + 1;
                      }
                      else
                      {
                        if ( v121 != 0 && v119 != nullptr )
                          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(
                            v119,
                            v120,
                            v121);
                        v120 = (__int16 *)(v9 - 19);
                        v75 = 1;
                      }
                      v65 = v75 + 6;
                      v121 = v65;
                      v122 = (unsigned __int8 *)(v9 - 12);
                    }
                    goto LABEL_187;
                  }
                }
                else
                {
LABEL_124:
                  if ( v121 != 0 && v119 != nullptr )
                    (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
                  v120 = (__int16 *)&v123;
                  v121 = 1;
                  v122 = (unsigned __int8 *)v124;
                  v59 = 1;
                }
                v58 = v119;
                if ( v119 != nullptr )
                  (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v59);
                goto LABEL_129;
              }
            }
            else
            {
LABEL_110:
              if ( v121 != 0 && v119 != nullptr )
                (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
              v120 = (__int16 *)&v123;
              v121 = 1;
              v122 = (unsigned __int8 *)v124;
              v52 = 1;
            }
            v51 = v119;
            if ( v119 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v52);
            goto LABEL_115;
          }
        }
        else
        {
          if ( v121 != 0 && v119 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v121);
          v120 = (__int16 *)&v123;
          v121 = 1;
          v122 = (unsigned __int8 *)v124;
          v49 = 1;
        }
        if ( v119 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v119 + 40LL))(v119, v120, v49);
        goto LABEL_101;
      }
      v41 = v35 + 4;
      v40 = -140;
    }
    else
    {
      v38 = v110;
      if ( v33 )
      {
        v39 = (__int16 *)(v9 - 60);
        if ( v119 != nullptr )
        {
          (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v119 + 40LL))(v119, v9 - 152, v35);
          v37 = (__int16 *)(v9 - 144);
          v38 = v110;
        }
        v120 = v37;
        v40 = -136;
        v41 = 8;
        goto LABEL_68;
      }
      v41 = v35 + 8;
      v40 = -136;
    }
    v37 = (__int16 *)(v9 - 152);
    v39 = (__int16 *)(v9 - 60);
    goto LABEL_68;
  }
LABEL_206:
  if ( a3 == 0 )
    goto LABEL_221;
  v83 = v12;
  v84 = *(_DWORD *)(*(_QWORD *)(v9 - 240) + 8LL) + v12 + 344;
  if ( v121 != 0 && v119 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
  v122 = nullptr;
  v121 = 0;
  v120 = nullptr;
  v85 = v10;
  v103 = v10;
  LODWORD(v10) = 0;
  if ( (unsigned __int8)sub_140DD8520(v84, (unsigned int)&v119, 0, a4, a5, a6, v103, a8) != 0 )
  {
    v86 = *(_DWORD *)(*(_QWORD *)(v9 - 240) + 8LL) + v83 + 128;
    if ( v121 != 0 && v119 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
    v122 = nullptr;
    v121 = 0;
    v120 = nullptr;
    LODWORD(v10) = 0;
    if ( (unsigned __int8)sub_140DFB5C0(v86, (unsigned int)&v119, 0, a4, a5, a6, v85, a8) != 0 )
    {
      v87 = *(_DWORD *)(*(_QWORD *)(v9 - 240) + 4LL) + v83 + 8;
      if ( v121 != 0 && v119 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
      v122 = nullptr;
      v121 = 0;
      v120 = nullptr;
      LOBYTE(v104) = v85;
      LODWORD(v10) = 0;
      if ( (unsigned __int8)sub_141084540(v87, (unsigned int)&v119, 0, a4, a5, a6, v104, a8) != 0 )
      {
        v12 = v83;
        if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDDBu )
          sub_140E01FF0(*(int *)(*(_QWORD *)(v9 - 240) + 8LL) + v83 + 8);
LABEL_221:
        v115 = v9;
        v109 = a4;
        if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDE2u )
        {
          sub_140DC3790(v12);
          v88 = *(__int64 **)(v9 - 96);
          if ( v88 != nullptr )
          {
            v89 = sub_140DC4DB0(v12, 11, 1);
            v10 = *v88;
            v90 = v88[1];
            if ( v90 != *v88 )
            {
              v91 = *(_BYTE *)(v9 - 19);
              v92 = *(_BYTE *)(v9 - 18);
              v93 = *(_BYTE *)(v9 - 17);
              v94 = *(_BYTE *)(v9 - 16);
              v95 = *(_BYTE *)(v9 - 15);
              v96 = *(_BYTE *)(v9 - 14);
              v97 = *(_BYTE *)(v9 - 13);
              v98 = 0;
              do
              {
                v99 = *(_BYTE **)(v10 + 8 * v98);
                if ( v99 != nullptr )
                {
                  v99[11] = v89;
                  v99[33] = v91;
                  v99[35] = v93;
                  v99[34] = v92;
                  v99[36] = v94;
                  v99[37] = v95;
                  v99[38] = v96;
                  v99[39] = v97;
                  v10 = *v88;
                  v90 = v88[1];
                }
                ++v98;
              }
              while ( v98 < (v90 - v10) >> 3 );
            }
          }
        }
        if ( *(unsigned __int16 *)(v109 + 1418) <= 0xDCBu )
        {
          v100 = *(unsigned __int16 *)(v109 + 1416);
          if ( v100 > 0xDE9 )
          {
LABEL_232:
            if ( (unsigned __int16)v100 <= 0xDEDu )
              *(_BYTE *)(v115 - 22) &= ~1u;
            if ( v121 != 0 && v119 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
            v122 = nullptr;
            v121 = 0;
            v120 = nullptr;
            LOBYTE(v10) = v119[4] == 0;
            goto LABEL_238;
          }
          *(_BYTE *)(v115 - 24) = -1;
        }
        LOWORD(v100) = *(_WORD *)(v109 + 1416);
        goto LABEL_232;
      }
    }
  }
LABEL_238:
  if ( v121 != 0 )
  {
    if ( v119 == nullptr )
      return (unsigned int)v10;
    (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v119 + 40LL))(v119, v120);
  }
  v101 = (void (__fastcall ***)(_QWORD, __int64))v119;
  v122 = nullptr;
  v121 = 0;
  v120 = nullptr;
  if ( v119 != nullptr && _InterlockedDecrement(v119 + 2) == 0 )
    (**v101)(v101, 1);
  return (unsigned int)v10;
}
