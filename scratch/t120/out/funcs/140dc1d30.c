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
  __int64 v88; // rdx
  __int64 v89; // r8
  __int64 *v90; // rsi
  char v91; // al
  __int64 v92; // r15
  char v93; // r8
  char v94; // r9
  char v95; // r10
  char v96; // r11
  char v97; // r12
  char v98; // r13
  char v99; // dl
  unsigned __int64 v100; // rcx
  _BYTE *v101; // r14
  unsigned int v102; // eax
  void (__fastcall ***v103)(_QWORD, __int64); // rcx
  char v105; // [rsp+30h] [rbp-50h]
  int v106; // [rsp+30h] [rbp-50h]
  _BYTE *v107; // [rsp+48h] [rbp-38h]
  __int64 v108; // [rsp+50h] [rbp-30h]
  _BYTE *v109; // [rsp+58h] [rbp-28h]
  __int64 v110; // [rsp+60h] [rbp-20h]
  __int64 v111; // [rsp+60h] [rbp-20h]
  _BYTE *v112; // [rsp+68h] [rbp-18h]
  __int64 v113; // [rsp+70h] [rbp-10h]
  _BYTE *v114; // [rsp+70h] [rbp-10h]
  __int64 v115; // [rsp+80h] [rbp+0h]
  _BYTE *v116; // [rsp+80h] [rbp+0h]
  __int64 v117; // [rsp+80h] [rbp+0h]
  void (__fastcall ***v118)(_QWORD, __int64); // [rsp+88h] [rbp+8h] BYREF
  char v119; // [rsp+95h] [rbp+15h]
  __int16 v120; // [rsp+96h] [rbp+16h] BYREF
  _DWORD *v121; // [rsp+98h] [rbp+18h] BYREF
  __int16 *v122; // [rsp+A0h] [rbp+20h]
  __int64 v123; // [rsp+A8h] [rbp+28h]
  unsigned __int8 *v124; // [rsp+B0h] [rbp+30h]
  unsigned __int8 v125; // [rsp+BFh] [rbp+3Fh] BYREF
  _QWORD v126[8]; // [rsp+C0h] [rbp+40h] BYREF

  v126[0] = -2;
  v9 = a1;
  LODWORD(v10) = a7;
  v11 = *a2;
  v121 = (_DWORD *)v11;
  if ( v11 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v11 + 8));
  v12 = a1 - 248;
  v124 = nullptr;
  v123 = 0;
  v122 = nullptr;
  if ( a7 != 0 )
  {
    v119 = a3;
    v122 = &v120;
    v123 = 2;
    v124 = (unsigned __int8 *)&v121;
    v108 = a1 - 248;
    if ( v121 != nullptr )
    {
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: &v120, a3: 2);
      v122 = nullptr;
      v123 = 0;
      v124 = nullptr;
      if ( v120 > 0 )
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
          }
        }
        v13 = (__int64 *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
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
            }
          }
          qword_141ABD470 = (__int64)&unk_141B59A68;
        }
        v13[2] = 0;
        v13[1] = 0;
        *v13 = 0;
        v115 = v9;
        *(_QWORD *)(v9 - 168) = v13;
        v14 = v120;
        v15 = v120;
        v16 = *v13;
        if ( (v13[2] - *v13) >> 1 < (unsigned __int64)v120 )
        {
          v110 = a4;
          if ( v120 < 0 )
            sub_1400526C0();
          v17 = v13[1];
          v18 = sub_1407E4490(a1: qword_141ABD470, a2: 2LL * v120);
          sub_141758A00(a1: v18, a2: *v13, a3: v13[1] - *v13);
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
              v113 = v22;
              MEMORY[0x1419475D8](a1: v22 + 32, a2: v19 - *(unsigned int *)(v22 + 120));
              v23 = *(_BYTE *)(v113 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v113 + 64)) != 0;
              if ( !v23 && *(_BYTE *)(v113 + 97) != 0 )
                sub_1412D33C0(a1: v113);
            }
            else
            {
              MEMORY[0x141948990](a1: v19 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *v13 = v18;
          v13[1] = v18 + v17 - v16;
          v13[2] = v18 + 2 * v15;
          v14 = v120;
          a4 = v110;
        }
        v9 = v115;
        if ( v14 > 0 )
        {
          v24 = 0;
          do
          {
            LOWORD(v118) = 25548;
            if ( v123 != 0 && v121 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
            v124 = nullptr;
            v123 = 0;
            v122 = nullptr;
            (*(void (__fastcall **)(_DWORD *, unsigned __int8 *, __int64))(*(_QWORD *)v121 + 40LL))(
              a1: v121,
              a2: &v125,
              a3: 1);
            (*(void (__fastcall **)(_DWORD *, void (__fastcall ****)(_QWORD, __int64), __int64))(*(_QWORD *)v121 + 40LL))(
              a1: v121,
              a2: &v118,
              a3: 2);
            if ( v125 <= 2u && ((unsigned __int16)v118 & 0x1FC0) == 0x380 )
              LOWORD(v118) = (unsigned __int16)v118 & 0xE03F | 0x3C0;
            if ( v121[4] != 0 )
              goto LABEL_46;
            sub_140DC3060(a1: v108, a2: (unsigned __int16)v118);
          }
          while ( (__int16)++v24 < v120 );
        }
      }
    }
    else
    {
      v124 = nullptr;
      v123 = 0;
      v122 = nullptr;
    }
    if ( v124 == (unsigned __int8 *)(v9 - 40) )
    {
      v25 = (_BYTE *)(v9 - 30);
      v116 = (_BYTE *)(v9 - 29);
      v109 = (_BYTE *)(v9 - 28);
      v114 = (_BYTE *)(v9 - 27);
      v107 = (_BYTE *)(v9 - 26);
      v26 = (__int16 *)(v9 - 25);
      v27 = v9 - 232;
      v29 = v123 == -15;
      v28 = v123 + 15;
      v123 += 15;
      v124 = (unsigned __int8 *)(v9 - 25);
      if ( v29 )
        goto LABEL_41;
    }
    else
    {
      if ( v123 != 0 && v121 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122, a3: v123);
      v122 = (__int16 *)(v9 - 40);
      v25 = (_BYTE *)(v9 - 30);
      v116 = (_BYTE *)(v9 - 29);
      v109 = (_BYTE *)(v9 - 28);
      v114 = (_BYTE *)(v9 - 27);
      v107 = (_BYTE *)(v9 - 26);
      v123 = 15;
      v26 = (__int16 *)(v9 - 25);
      v124 = (unsigned __int8 *)(v9 - 25);
      v27 = v9 - 232;
      v28 = 15;
    }
    if ( v121 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122, a3: v28);
LABEL_41:
    v124 = nullptr;
    v123 = 0;
    v122 = nullptr;
    LOBYTE(v118) = 0;
    *(_DWORD *)(v27 + 56) = 0;
    *(_QWORD *)(v27 + 48) = 0;
    *(_QWORD *)(v27 + 40) = 0;
    *(_QWORD *)(v27 + 32) = 0;
    *(_QWORD *)(v27 + 24) = 0;
    *(_QWORD *)(v27 + 16) = 0;
    *(_QWORD *)(v27 + 8) = 0;
    v30 = v121;
    (*(void (__fastcall **)(_DWORD *, void (__fastcall ****)(_QWORD, __int64), __int64))(*(_QWORD *)v121 + 40LL))(
      a1: v121,
      a2: &v118,
      a3: 1);
    if ( v30[4] != 0 )
      goto LABEL_46;
    v31 = v121;
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v121 + 40LL))(
      a1: v121,
      a2: v27 + 8,
      a3: 51 - (((unsigned __int8)v118 < 0xAu) - 1LL));
    if ( v31[4] != 0 )
      goto LABEL_46;
    if ( (unsigned __int8)v118 <= 9u )
      *(_BYTE *)(v27 + 59) = 0;
    if ( v121[4] != 0 )
      goto LABEL_46;
    v112 = v25;
    if ( v124 == (unsigned __int8 *)(v9 - 64) )
    {
      v32 = v123 + 4;
    }
    else
    {
      if ( v123 != 0 )
        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122, a3: v123);
      v122 = (__int16 *)(v9 - 64);
      v32 = 4;
    }
    v123 = v32;
    v124 = (unsigned __int8 *)(v9 - 60);
    v33 = HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0;
    v34 = !v33;
    v35 = 4 * v34 + 4;
    v36 = 4 * v34 - 148;
    if ( v32 != 0 && v121 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
    v122 = (__int16 *)(v9 - 152);
    v123 = v35;
    v124 = (unsigned __int8 *)(v9 + v36);
    v37 = (__int16 *)(v9 - 144);
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
    {
      v38 = v112;
      if ( v33 )
      {
        v39 = (__int16 *)(v9 - 60);
        if ( v121 != nullptr )
        {
          (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v9 - 152, a3: v35);
          v37 = (__int16 *)(v9 - 144);
          v38 = v112;
        }
        v122 = v37;
        v40 = -140;
        v41 = 4;
LABEL_68:
        v123 = v41;
        v124 = (unsigned __int8 *)(v9 + v40);
        if ( v121 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v37, a3: v41);
        v122 = v39;
        v123 = 8;
        v124 = (unsigned __int8 *)(v9 - 52);
        if ( v121 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v39, a3: 8);
        v122 = v26;
        v123 = 1;
        v124 = (unsigned __int8 *)(v9 - 24);
        v42 = 6;
        v43 = v26;
        if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDCBu )
        {
          v43 = (__int16 *)(v9 - 23);
          if ( v121 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v26, a3: 1);
          v122 = (__int16 *)(v9 - 23);
          v42 = 4;
        }
        v123 = v42;
        v124 = (unsigned __int8 *)(v9 - 19);
        if ( v121 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v43);
        v122 = (__int16 *)(v9 - 52);
        v123 = 8;
        v124 = (unsigned __int8 *)(v9 - 44);
        v125 = 0;
        v44 = &v125;
        if ( (unsigned __int8 *)(v9 - 44) == &v125 )
        {
          v45 = 9;
          v44 = (unsigned __int8 *)(v9 - 52);
        }
        else
        {
          if ( v121 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v9 - 52, a3: 8);
          v122 = (__int16 *)&v125;
          v45 = 1;
        }
        v123 = v45;
        v124 = (unsigned __int8 *)v126;
        if ( v121 != nullptr )
          (*(void (__fastcall **)(_DWORD *, unsigned __int8 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v44);
        v124 = nullptr;
        v123 = 0;
        v122 = nullptr;
        if ( v125 != 0 )
        {
          v46 = *(_WORD *)(a4 + 1416);
          v47 = sub_140DC33A0(a1: v108);
          if ( v123 != 0 && v121 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
          v124 = nullptr;
          v123 = 0;
          v122 = nullptr;
          v48 = v46 < 0xDC9u ? sub_1413F97A0(a1: v47, a2: &v121) : sub_1413F90A0(a1: v47, a2: &v121);
          if ( v48 == 0 )
            goto LABEL_46;
        }
        if ( v124 == &v125 )
        {
          v49 = v123 + 1;
          v123 = v49;
          v124 = (unsigned __int8 *)v126;
          if ( v49 == 0 )
          {
LABEL_101:
            v124 = nullptr;
            v123 = 0;
            v122 = nullptr;
            if ( v125 == 0 )
              goto LABEL_110;
            v50 = (_QWORD *)sub_140DC3550(a1: 24);
            if ( qword_141ABD470 == 0 )
              qword_141ABD470 = ((__int64 (*)(void))sub_1407E4940)();
            v50[2] = 0;
            v50[1] = 0;
            *v50 = 0;
            *(_QWORD *)(v9 - 128) = v50;
            if ( v123 != 0 && v121 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
            v124 = nullptr;
            v123 = 0;
            v122 = nullptr;
            if ( (unsigned __int8)sub_1413FE0E0(a1: v50, a2: &v121) == 0 )
              goto LABEL_46;
            if ( v124 == &v125 )
            {
              v52 = v123 + 1;
              v29 = v123++ == -1;
              v124 = (unsigned __int8 *)v126;
              if ( v29 )
              {
LABEL_115:
                v124 = nullptr;
                v123 = 0;
                v122 = nullptr;
                if ( v125 == 0 )
                  goto LABEL_124;
                v53 = sub_1407E4940(a1: v51, a2: v37, a3: v52);
                v56 = (_QWORD *)sub_1407E4490(a1: v53, a2: 24);
                if ( qword_141ABD470 == 0 )
                  qword_141ABD470 = sub_1407E4940(a1: v55, a2: v54, a3: v57);
                v56[2] = 0;
                v56[1] = 0;
                *v56 = 0;
                *(_QWORD *)(v9 - 104) = v56;
                if ( v123 != 0 && v121 != nullptr )
                  (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
                v124 = nullptr;
                v123 = 0;
                v122 = nullptr;
                if ( (unsigned __int8)sub_1413FE6B0(a1: v56, a2: &v121) == 0 )
                  goto LABEL_46;
                if ( v124 == &v125 )
                {
                  v59 = v123 + 1;
                  v29 = v123++ == -1;
                  v124 = (unsigned __int8 *)v126;
                  if ( v29 )
                  {
LABEL_129:
                    v124 = nullptr;
                    v123 = 0;
                    v122 = nullptr;
                    if ( v125 == 0 )
                      goto LABEL_138;
                    v62 = (_QWORD *)sub_140DC3600(a1: v58, a2: v37, a3: v59);
                    if ( qword_141ABD470 == 0 )
                      qword_141ABD470 = sub_1407E4940(a1: v61, a2: v60, a3: v63);
                    v62[2] = 0;
                    v62[1] = 0;
                    *v62 = 0;
                    *(_QWORD *)(v9 - 80) = v62;
                    if ( v123 != 0 && v121 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
                    v124 = nullptr;
                    v123 = 0;
                    v122 = nullptr;
                    if ( (unsigned __int8)sub_1413FECE0(a1: v62, a2: &v121) == 0 )
                      goto LABEL_46;
                    if ( v124 == &v125 )
                    {
                      v65 = v123 + 1;
                      v29 = v123++ == -1;
                      v124 = (unsigned __int8 *)v126;
                      if ( v29 )
                        goto LABEL_143;
                    }
                    else
                    {
LABEL_138:
                      if ( v123 != 0 && v121 != nullptr )
                        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
                      v122 = (__int16 *)&v125;
                      v123 = 1;
                      v124 = (unsigned __int8 *)v126;
                      v65 = 1;
                    }
                    v64 = v121;
                    if ( v121 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(
                        a1: v121,
                        a2: v122,
                        a3: v65);
LABEL_143:
                    v124 = nullptr;
                    v123 = 0;
                    v122 = nullptr;
                    if ( v125 == 0 )
                      goto LABEL_153;
                    sub_140DC36B0(a1: &v118, a2: v37, a3: v65);
                    v66 = (void (__fastcall ****)(_QWORD, __int64))(v9 - 136);
                    if ( (void (__fastcall ****)(_QWORD, __int64))(v9 - 136) != &v118 )
                    {
                      v67 = v118;
                      v118 = nullptr;
                      v68 = *v66;
                      *v66 = v67;
                      if ( v68 == nullptr )
                        goto LABEL_149;
                      (**v68)(a1: v68, a2: 1);
                    }
                    if ( v118 != nullptr )
                      (**v118)(a1: v118, a2: 1);
LABEL_149:
                    v69 = *v66;
                    if ( v123 != 0 && v121 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
                    v124 = nullptr;
                    v123 = 0;
                    v122 = nullptr;
                    v38 = v112;
                    if ( ((unsigned __int8 (__fastcall *)(_QWORD, _DWORD **))(*v69)[1])(a1: v69, a2: &v121) == 0 )
                      goto LABEL_46;
LABEL_153:
                    LODWORD(v10) = a7;
                    if ( *(unsigned __int16 *)(a4 + 1416) < 0xDC1u )
                    {
LABEL_187:
                      v76 = (unsigned __int8)*v116;
                      if ( (_BYTE)v76 != 66 && (unsigned __int8)sub_14087A360(a1: v76, a2: v37, a3: v65) == 0 )
                        *v116 = 0;
                      v77 = (unsigned __int8)*v109;
                      if ( (_BYTE)v77 != 66 && (unsigned __int8)sub_14087A360(a1: v77, a2: v37, a3: v65) == 0 )
                        *v109 = *v116;
                      v78 = (unsigned __int8)*v114;
                      if ( (_BYTE)v78 != 66 && (unsigned __int8)sub_14087A360(a1: v78, a2: v37, a3: v65) == 0 )
                        *v114 = 0;
                      v79 = (unsigned __int8)*v107;
                      if ( (_BYTE)v79 != 66 && (unsigned __int8)sub_14087A360(a1: v79, a2: v37, a3: v65) == 0 )
                        *v107 = 0;
                      v80 = (unsigned __int8)*v38;
                      v81 = 0xC3000000000LL;
                      if ( v80 <= 0x2B && _bittest64(&v81, v80) )
                        *v38 = 0;
                      v82 = *(unsigned __int8 *)v26;
                      a3 = v119;
                      if ( v82 <= 0x2B && _bittest64(&v81, v82) )
                        *(_BYTE *)v26 = 0;
                      v12 = v108;
                      goto LABEL_206;
                    }
                    if ( v124 == &v125 )
                    {
                      v65 = v123 + 1;
                      v123 = v65;
                      v124 = (unsigned __int8 *)v126;
                      if ( v65 == 0 )
                        goto LABEL_172;
                    }
                    else
                    {
                      if ( v123 != 0 && v121 != nullptr )
                        (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(
                          a1: v121,
                          a2: v122,
                          a3: v123);
                      v122 = (__int16 *)&v125;
                      v123 = 1;
                      v124 = (unsigned __int8 *)v126;
                      v65 = 1;
                    }
                    v64 = v121;
                    if ( v121 != nullptr )
                      (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(
                        a1: v121,
                        a2: v122,
                        a3: v65);
LABEL_172:
                    v124 = nullptr;
                    v123 = 0;
                    v122 = nullptr;
                    if ( v125 != 0 )
                    {
                      v70 = sub_1407E4940(a1: v64, a2: v37, a3: v65);
                      v73 = (_QWORD *)sub_1407E4490(a1: v70, a2: 24);
                      if ( qword_141ABD470 == 0 )
                        qword_141ABD470 = sub_1407E4940(a1: v72, a2: v71, a3: v74);
                      v73[2] = 0;
                      v73[1] = 0;
                      *v73 = 0;
                      *(_QWORD *)(v9 - 96) = v73;
                      if ( v123 != 0 && v121 != nullptr )
                        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
                      v124 = nullptr;
                      v123 = 0;
                      v122 = nullptr;
                      if ( (unsigned __int8)sub_1413FF240(a1: v73, a2: &v121) == 0 )
                      {
LABEL_46:
                        LODWORD(v10) = 0;
                        goto LABEL_238;
                      }
                    }
                    LODWORD(v10) = a7;
                    if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDD0u )
                    {
                      if ( v124 == (unsigned __int8 *)(v9 - 19) )
                      {
                        v75 = v123 + 1;
                      }
                      else
                      {
                        if ( v123 != 0 && v121 != nullptr )
                          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(
                            a1: v121,
                            a2: v122,
                            a3: v123);
                        v122 = (__int16 *)(v9 - 19);
                        v75 = 1;
                      }
                      v65 = v75 + 6;
                      v123 = v65;
                      v124 = (unsigned __int8 *)(v9 - 12);
                    }
                    goto LABEL_187;
                  }
                }
                else
                {
LABEL_124:
                  if ( v123 != 0 && v121 != nullptr )
                    (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
                  v122 = (__int16 *)&v125;
                  v123 = 1;
                  v124 = (unsigned __int8 *)v126;
                  v59 = 1;
                }
                v58 = v121;
                if ( v121 != nullptr )
                  (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(
                    a1: v121,
                    a2: v122,
                    a3: v59);
                goto LABEL_129;
              }
            }
            else
            {
LABEL_110:
              if ( v123 != 0 && v121 != nullptr )
                (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
              v122 = (__int16 *)&v125;
              v123 = 1;
              v124 = (unsigned __int8 *)v126;
              v52 = 1;
            }
            v51 = v121;
            if ( v121 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(
                a1: v121,
                a2: v122,
                a3: v52);
            goto LABEL_115;
          }
        }
        else
        {
          if ( v123 != 0 && v121 != nullptr )
            (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(
              a1: v121,
              a2: v122,
              a3: v123);
          v122 = (__int16 *)&v125;
          v123 = 1;
          v124 = (unsigned __int8 *)v126;
          v49 = 1;
        }
        if ( v121 != nullptr )
          (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122, a3: v49);
        goto LABEL_101;
      }
      v41 = v35 + 4;
      v40 = -140;
    }
    else
    {
      v38 = v112;
      if ( v33 )
      {
        v39 = (__int16 *)(v9 - 60);
        if ( v121 != nullptr )
        {
          (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v9 - 152, a3: v35);
          v37 = (__int16 *)(v9 - 144);
          v38 = v112;
        }
        v122 = v37;
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
  if ( v123 != 0 && v121 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
  v124 = nullptr;
  v123 = 0;
  v122 = nullptr;
  v85 = v10;
  v105 = v10;
  LODWORD(v10) = 0;
  if ( (unsigned __int8)sub_140DD8520(a1: v84, a2: (unsigned int)&v121, a3: 0, a4, a5, a6, a7: v105, a8) != 0 )
  {
    v86 = *(_DWORD *)(*(_QWORD *)(v9 - 240) + 8LL) + v83 + 128;
    if ( v123 != 0 && v121 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
    v124 = nullptr;
    v123 = 0;
    v122 = nullptr;
    LODWORD(v10) = 0;
    if ( (unsigned __int8)sub_140DFB5C0(a1: v86, a2: (unsigned int)&v121, a3: 0, a4, a5, a6, a7: v85, a8) != 0 )
    {
      v87 = *(_DWORD *)(*(_QWORD *)(v9 - 240) + 4LL) + v83 + 8;
      if ( v123 != 0 && v121 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
      v124 = nullptr;
      v123 = 0;
      v122 = nullptr;
      LOBYTE(v106) = v85;
      LODWORD(v10) = 0;
      if ( (unsigned __int8)sub_141084540(a1: v87, a2: (unsigned int)&v121, a3: 0, a4, a5, a6, a7: v106, a8) != 0 )
      {
        v12 = v83;
        if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDDBu )
          sub_140E01FF0(a1: *(int *)(*(_QWORD *)(v9 - 240) + 8LL) + v83 + 8);
LABEL_221:
        v117 = v9;
        v111 = a4;
        if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDE2u )
        {
          sub_140DC3790(a1: v12);
          v90 = *(__int64 **)(v9 - 96);
          if ( v90 != nullptr )
          {
            LOBYTE(v88) = 11;
            LOBYTE(v89) = 1;
            v91 = sub_140DC4DB0(a1: v12, a2: v88, a3: v89);
            v10 = *v90;
            v92 = v90[1];
            if ( v92 != *v90 )
            {
              v93 = *(_BYTE *)(v9 - 19);
              v94 = *(_BYTE *)(v9 - 18);
              v95 = *(_BYTE *)(v9 - 17);
              v96 = *(_BYTE *)(v9 - 16);
              v97 = *(_BYTE *)(v9 - 15);
              v98 = *(_BYTE *)(v9 - 14);
              v99 = *(_BYTE *)(v9 - 13);
              v100 = 0;
              do
              {
                v101 = *(_BYTE **)(v10 + 8 * v100);
                if ( v101 != nullptr )
                {
                  v101[11] = v91;
                  v101[33] = v93;
                  v101[35] = v95;
                  v101[34] = v94;
                  v101[36] = v96;
                  v101[37] = v97;
                  v101[38] = v98;
                  v101[39] = v99;
                  v10 = *v90;
                  v92 = v90[1];
                }
                ++v100;
              }
              while ( v100 < (v92 - v10) >> 3 );
            }
          }
        }
        if ( *(unsigned __int16 *)(v111 + 1418) <= 0xDCBu )
        {
          v102 = *(unsigned __int16 *)(v111 + 1416);
          if ( v102 > 0xDE9 )
          {
LABEL_232:
            if ( (unsigned __int16)v102 <= 0xDEDu )
              *(_BYTE *)(v117 - 22) &= ~1u;
            if ( v123 != 0 && v121 != nullptr )
              (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
            v124 = nullptr;
            v123 = 0;
            v122 = nullptr;
            LOBYTE(v10) = v121[4] == 0;
            goto LABEL_238;
          }
          *(_BYTE *)(v117 - 24) = -1;
        }
        LOWORD(v102) = *(_WORD *)(v111 + 1416);
        goto LABEL_232;
      }
    }
  }
LABEL_238:
  if ( v123 != 0 )
  {
    if ( v121 == nullptr )
      return (unsigned int)v10;
    (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)v121 + 40LL))(a1: v121, a2: v122);
  }
  v103 = (void (__fastcall ***)(_QWORD, __int64))v121;
  v124 = nullptr;
  v123 = 0;
  v122 = nullptr;
  if ( v121 != nullptr && _InterlockedDecrement(v121 + 2) == 0 )
    (**v103)(a1: v103, a2: 1);
  return (unsigned int)v10;
}
