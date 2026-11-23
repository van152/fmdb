__int64 __fastcall sub_140E5B1A0(__int64 a1, __int64 *a2, char a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rax
  char *v12; // rsi
  char v13; // bl
  char *v14; // rsi
  char *v15; // rbx
  __int64 v16; // r8
  __int64 v17; // rax
  unsigned __int64 v18; // rdx
  __int64 *v19; // rbx
  void *v20; // rcx
  __int64 v21; // r13
  __int64 v22; // rsi
  unsigned __int64 v23; // rdi
  unsigned __int64 v24; // r8
  unsigned __int64 v25; // r12
  __int64 v26; // r15
  unsigned __int64 v27; // r13
  __int64 v28; // rsi
  char v29; // al
  __int64 v30; // rcx
  __int64 v31; // rsi
  __int64 v32; // rdi
  __int64 v33; // r8
  __int64 v34; // rbx
  __int64 v35; // r8
  __int64 v36; // rsi
  bool v37; // zf
  unsigned __int16 v38; // ax
  __int16 v39; // cx
  bool v40; // si
  __int64 *v41; // rbx
  void *v42; // rcx
  char v43; // al
  __int64 v44; // rdi
  __int64 v45; // r13
  __int64 v46; // r15
  __int64 v47; // rsi
  unsigned __int64 v48; // rcx
  __int64 v49; // r8
  __int64 v50; // rcx
  bool v51; // al
  char v52; // bl
  __int64 v53; // r12
  __int64 v54; // rsi
  __int64 v55; // rsi
  __int64 v56; // rsi
  int v57; // edi
  __int16 *v58; // r13
  __int64 v59; // rsi
  int v60; // edi
  __int64 v61; // rsi
  __int64 v62; // rsi
  __int64 v63; // rsi
  __int64 v64; // rsi
  __int64 v65; // rsi
  __int64 v66; // rsi
  __int64 v67; // rsi
  int v68; // eax
  unsigned __int16 v69; // cx
  unsigned __int16 v70; // ax
  unsigned int v71; // eax
  int v72; // edx
  __int16 v73; // cx
  __int64 v74; // r8
  char v75; // al
  __int64 *v76; // rbx
  __int64 v77; // r15
  __int64 v78; // r12
  unsigned __int64 v79; // rcx
  __int64 v80; // rsi
  __int64 v81; // r13
  __int64 v82; // rdi
  unsigned __int64 v83; // rcx
  __int64 v84; // r8
  __int64 v85; // rcx
  bool v86; // al
  unsigned __int64 v87; // rdi
  __int64 v88; // rsi
  __int64 v89; // r13
  unsigned __int64 v90; // rsi
  __int64 v91; // rsi
  __int64 v92; // rsi
  __int64 v93; // rsi
  int v94; // edi
  __int64 v95; // rsi
  __int64 *v96; // r15
  __int64 v97; // rcx
  unsigned __int64 v98; // rbx
  unsigned __int64 v99; // rax
  unsigned __int64 v100; // rsi
  __int64 v101; // rbx
  unsigned __int64 v102; // rcx
  __int64 v103; // r8
  __int64 v104; // rcx
  bool v105; // al
  __int64 v106; // r8
  void (__fastcall ***v107)(_QWORD, __int64); // rcx
  unsigned __int16 v109; // [rsp+58h] [rbp-28h]
  __int64 v110; // [rsp+58h] [rbp-28h]
  __int64 v111; // [rsp+60h] [rbp-20h]
  unsigned __int16 v112; // [rsp+60h] [rbp-20h]
  bool v113; // [rsp+6Ch] [rbp-14h]
  int v114; // [rsp+6Ch] [rbp-14h]
  __int64 v115; // [rsp+70h] [rbp-10h]
  int v116; // [rsp+78h] [rbp-8h]
  __int16 v117; // [rsp+78h] [rbp-8h]
  __int64 v118; // [rsp+78h] [rbp-8h]
  unsigned __int64 v119; // [rsp+78h] [rbp-8h]
  int v120; // [rsp+80h] [rbp+0h] BYREF
  char v121; // [rsp+87h] [rbp+7h] BYREF
  __int64 v122; // [rsp+88h] [rbp+8h] BYREF
  char *v123; // [rsp+90h] [rbp+10h]
  __int64 v124; // [rsp+98h] [rbp+18h]
  char *v125; // [rsp+A0h] [rbp+20h]
  char v126; // [rsp+AEh] [rbp+2Eh]
  char v127; // [rsp+AFh] [rbp+2Fh] BYREF
  _QWORD v128[8]; // [rsp+B0h] [rbp+30h] BYREF

  v128[0] = -2;
  v11 = *a2;
  v122 = v11;
  if ( v11 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v11 + 8));
  v123 = (char *)(a1 + 216);
  v124 = 4;
  v125 = (char *)(a1 + 220);
  LODWORD(v12) = v122;
  if ( v122 != 0 )
  {
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 216, 4);
    v123 = (char *)(a1 + 224);
    v124 = 4;
    v125 = (char *)(a1 + 228);
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 224, 4);
    v123 = (char *)(a1 + 232);
    v124 = 4;
    v125 = (char *)(a1 + 236);
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 232, 4);
    v123 = (char *)(a1 + 240);
    v124 = 4;
    v125 = (char *)(a1 + 244);
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 240, 4);
    v123 = (char *)(a1 + 248);
    v124 = 4;
    v125 = (char *)(a1 + 252);
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 248, 4);
  }
  v123 = (char *)(a1 + 352);
  v124 = 4;
  v125 = (char *)(a1 + 356);
  if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDC4u )
  {
    v124 = 6;
    v125 = (char *)(a1 + 358);
    if ( v122 != 0 )
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 352, 6);
    v125 = nullptr;
    v124 = 0;
    v123 = nullptr;
    sub_140814B10(v122, &v120, a1 + 192);
    if ( v120 != 0 )
      goto LABEL_13;
    if ( v124 != 0 && v122 != 0 )
      (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
    v125 = nullptr;
    v124 = 0;
    v123 = nullptr;
    sub_140814B10(v122, &v120, a1 + 200);
    if ( v120 != 0 )
    {
LABEL_13:
      LODWORD(v12) = 0;
      goto LABEL_245;
    }
  }
  v13 = a7;
  if ( a7 == 0 )
    goto LABEL_239;
  v126 = a3;
  if ( v125 == (char *)(a1 + 362) )
  {
    v14 = (char *)(a1 + 363);
    v15 = (char *)(a1 + 358);
    v16 = v124 + 1;
    v124 = v16;
    v125 = (char *)(a1 + 363);
    if ( v16 == 0 )
      goto LABEL_23;
  }
  else
  {
    if ( v124 != 0 && v122 != 0 )
      (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v124);
    v123 = (char *)(a1 + 362);
    v124 = 1;
    v14 = (char *)(a1 + 363);
    v125 = (char *)(a1 + 363);
    v15 = (char *)(a1 + 358);
    v16 = 1;
  }
  if ( v122 != 0 )
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v16);
LABEL_23:
  v123 = v15;
  v124 = 2;
  v125 = (char *)(a1 + 360);
  if ( v122 != 0 )
  {
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v15, 2);
    v123 = (char *)(a1 + 328);
    v124 = 4;
    v125 = (char *)(a1 + 332);
    if ( v122 != 0 )
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 328, 4);
  }
  v123 = v14;
  v124 = 1;
  v125 = (char *)(a1 + 364);
  if ( (char *)(a1 + 364) == &v127 )
  {
    v17 = 2;
  }
  else
  {
    if ( v122 != 0 )
      (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v14, 1);
    v123 = &v127;
    v17 = 1;
  }
  v124 = v17;
  v125 = (char *)v128;
  sub_1412E70A0(&v122);
  v115 = a4;
  if ( v127 > 0 )
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
    v19 = (__int64 *)sub_1407E4490(&unk_141B59A68, 24);
    v20 = (void *)qword_141ABD470;
    if ( qword_141ABD470 == 0 )
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
      qword_141ABD470 = (__int64)&unk_141B59A68;
      v20 = &unk_141B59A68;
    }
    v19[2] = 0;
    v19[1] = 0;
    *v19 = 0;
    *(_QWORD *)(a1 + 272) = v19;
    v18 = (unsigned __int8)v127;
    v21 = v127;
    v22 = *v19;
    v23 = (v19[1] - *v19) >> 3;
    if ( v23 <= v127 )
    {
      if ( v23 < v127 )
      {
        v24 = (v19[2] - v22) >> 3;
        if ( v24 >= v127 )
        {
          v27 = v127 - v23;
          v28 = v19[1] + 8 * v27;
          sub_141758A10(v19[1], 0, 8 * v27);
          v19[1] = v28;
        }
        else
        {
          if ( v127 < 0 )
            sub_1400526C0(v20, (unsigned __int8)v127);
          v25 = v24 + (v24 >> 1);
          if ( v25 <= v127 )
            v25 = v127;
          if ( v24 > 0x1FFFFFFFFFFFFFFFLL - (v24 >> 1) )
            v25 = 0x1FFFFFFFFFFFFFFFLL;
          v26 = sub_1407E4490(v20, 8 * v25);
          sub_141758A10(v26 + 8 * v23, 0, 8 * (v21 - v23));
          sub_141758A00(v26, *v19, v19[1] - *v19);
          v18 = *v19;
          if ( *v19 != 0 )
            sub_1407E4890(qword_141ABD470, v18, v19[2] - v18);
          *v19 = v26;
          v19[1] = v26 + 8 * v21;
          v19[2] = v26 + 8 * v25;
          a4 = v115;
        }
      }
    }
    else
    {
      v19[1] = v22 + 8LL * v127;
    }
    v29 = v127;
    if ( v127 > 0 )
    {
      v30 = (__int64)v125;
      v31 = 0;
      v32 = 0;
      do
      {
        v34 = **(_QWORD **)(a1 + 272);
        if ( v34 + v31 == v30 )
        {
          v33 = v124 + 4;
        }
        else
        {
          if ( v124 != 0 && v122 != 0 )
          {
            (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v124);
            v29 = v127;
          }
          v123 = (char *)(v34 + v31);
          v33 = 4;
        }
        v124 = v33;
        v30 = v34 + 8 * v32 + 4;
        v125 = (char *)(v34 + v31 + 4);
        ++v32;
        v18 = v29;
        v31 += 8;
      }
      while ( v32 < v29 );
    }
  }
  if ( v125 == &v121 )
  {
    v35 = v124 + 1;
    v124 = v35;
    v125 = (char *)&v122;
    if ( v35 == 0 )
      goto LABEL_66;
  }
  else
  {
    if ( v124 != 0 && v122 != 0 )
      (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v124);
    v123 = &v121;
    v124 = 1;
    v125 = (char *)&v122;
    v35 = 1;
  }
  if ( v122 != 0 )
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v35);
LABEL_66:
  v125 = nullptr;
  v124 = 0;
  v123 = nullptr;
  if ( v121 == 1 )
  {
    if ( dword_141B5DDA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5DDA8);
      if ( dword_141B5DDA8 == -1 )
      {
        sub_1407E53D0((unsigned int)&unk_141B5DD58, 1100154900, 100, 2240, 0, 0, 100, 4096);
        sub_141751048(sub_140E9BF80);
        sub_141750EA0(&dword_141B5DDA8);
      }
    }
    v36 = sub_1407E58C0(&unk_141B5DD58, 2240);
    sub_141476BB0(v36);
  }
  else
  {
    if ( v121 != 0 )
    {
      *(_QWORD *)(a1 + 336) = 0;
      goto LABEL_80;
    }
    if ( dword_141B5DD50 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5DD50);
      if ( dword_141B5DD50 == -1 )
      {
        sub_1407E53D0((unsigned int)&unk_141B5DD00, 1100152071, 0x4000, 64, 0, 0, 1024, 4096);
        sub_141751048(sub_140E9BF70);
        sub_141750EA0(&dword_141B5DD50);
      }
    }
    v36 = sub_1407E58C0(&unk_141B5DD00, 64);
    *(_QWORD *)v36 = 0x1418B7E08LL;
    *(_QWORD *)(v36 + 44) = 0x76C0001076C0001LL;
    *(_QWORD *)(v36 + 52) = 124518401;
    *(_QWORD *)(v36 + 8) = 0;
    *(_BYTE *)(v36 + 60) = 0;
    *(_QWORD *)(v36 + 36) = 0x3F80000000000000LL;
    *(_QWORD *)(v36 + 20) = 0;
    *(_QWORD *)(v36 + 28) = 0;
    *(_DWORD *)(v36 + 16) = 0;
  }
  *(_QWORD *)(a1 + 336) = v36;
  if ( v124 != 0 && v122 != 0 )
    (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
  v125 = nullptr;
  v124 = 0;
  v123 = nullptr;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *, __int64, __int64))(*(_QWORD *)v36 + 32LL))(
         v36,
         &v122,
         a1,
         a4) == 0 )
  {
LABEL_229:
    LODWORD(v12) = 0;
    goto LABEL_245;
  }
  if ( v125 == &v127 )
  {
    v37 = v124++ == -1;
    v125 = (char *)v128;
    if ( v37 )
      goto LABEL_86;
    goto LABEL_84;
  }
LABEL_80:
  if ( v124 != 0 && v122 != 0 )
    (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
  v123 = &v127;
  v124 = 1;
  v125 = (char *)v128;
LABEL_84:
  if ( v122 != 0 )
    (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
LABEL_86:
  v125 = nullptr;
  v124 = 0;
  v123 = nullptr;
  LODWORD(a4) = v115;
  if ( v127 > 0 )
  {
    v38 = word_141AB0260;
    if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
    {
      word_141AB0260 = 2023;
      v38 = 2023;
    }
    v109 = v38;
    v39 = 3;
    if ( (unsigned __int16)(23593 * v38) < 0xA3Eu )
      v39 = 15;
    v116 = v38;
    v40 = (unsigned __int16)(v38 & v39) == 0;
    if ( dword_141B5DBF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5DBF0);
      if ( dword_141B5DBF0 == -1 )
      {
        sub_1407E53D0((unsigned int)&unk_141B5DBA0, 1100123319, 64, 24, 0, 0, 64, 4096);
        sub_141751048(sub_140E9BDE0);
        sub_141750EA0(&dword_141B5DBF0);
      }
    }
    v41 = (__int64 *)sub_1407E58C0(&unk_141B5DBA0, 24);
    v42 = (void *)qword_141ABD470;
    if ( qword_141ABD470 == 0 )
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
          LODWORD(a4) = v115;
        }
      }
      v42 = &unk_141B59A68;
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    v41[2] = 0;
    v41[1] = 0;
    *v41 = 0;
    *(_QWORD *)(a1 + 304) = v41;
    v43 = v127;
    v44 = v127;
    v45 = *v41;
    v18 = (v41[2] - *v41) >> 3;
    if ( v18 < v127 )
    {
      v113 = v40;
      if ( v127 < 0 )
        sub_1400526C0(v42, v18);
      a4 = v41[1];
      v46 = sub_1407E4490(v42, 8LL * v127);
      sub_141758A00(v46, *v41, v41[1] - *v41);
      v47 = *v41;
      if ( *v41 != 0 )
      {
        v48 = v41[2] - v47;
        if ( v48 == -1 )
          v48 = *(unsigned int *)(v47 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v49 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v49) >> 3 > v48)
          && (v50 = *(_QWORD *)(v49 + 8 * v48)) != 0 )
        {
          v111 = v50;
          MEMORY[0x1419475D8](v50 + 32, v47 - *(unsigned int *)(v50 + 120));
          v51 = *(_BYTE *)(v111 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v111 + 64)) != 0;
          if ( !v51 && *(_BYTE *)(v111 + 97) != 0 )
            sub_1412D33C0(v111);
        }
        else
        {
          MEMORY[0x141948990](v47 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *v41 = v46;
      v41[1] = v46 + a4 - v45;
      v41[2] = v46 + 8 * v44;
      v43 = v127;
      LODWORD(a4) = v115;
      v40 = v113;
    }
    if ( v43 > 0 )
    {
      v112 = v40 | 0xB6;
      v114 = (v116 << 16) | v112;
      v117 = v116 + 1;
      v52 = 0;
      do
      {
        if ( dword_141B5DF88 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B5DF88);
          if ( dword_141B5DF88 == -1 )
          {
            sub_1407E53D0((unsigned int)&unk_141B5DF38, 1100152707, 0x2000, 24, 0, 0, 1024, 0);
            sub_141751048(sub_140E9BDD0);
            sub_141750EA0(&dword_141B5DF88);
          }
        }
        v53 = sub_1407E58C0(&unk_141B5DF38, 24);
        *(_QWORD *)v53 = 0x76C0001076C0001LL;
        *(_QWORD *)(v53 + 8) = 0;
        *(_WORD *)(v53 + 16) = 0;
        *(_DWORD *)(v53 + 18) = -16777210;
        *(_BYTE *)(v53 + 22) = 0;
        if ( v124 != 0 && v122 != 0 )
          (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
        v125 = nullptr;
        v124 = 0;
        v123 = nullptr;
        v54 = v122;
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)v122 + 40LL))(v122, &v120, 1);
        if ( *(_DWORD *)(v54 + 16) != 0 )
          goto LABEL_229;
        v55 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 18, 1);
        if ( *(_DWORD *)(v55 + 16) != 0 )
          goto LABEL_229;
        v56 = v122;
        if ( v122 != 0 )
        {
          _InterlockedIncrement((volatile signed __int32 *)(v122 + 8));
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v56 + 40LL))(v56, v53, 4);
        }
        v57 = *(_DWORD *)(v56 + 16);
        if ( _InterlockedDecrement((volatile signed __int32 *)(v56 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v56)(v56, 1);
        if ( v57 != 0 )
          goto LABEL_229;
        v58 = (__int16 *)(v53 + 4);
        v59 = v122;
        if ( v122 != 0 )
        {
          _InterlockedIncrement((volatile signed __int32 *)(v122 + 8));
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v59 + 40LL))(v59, v53 + 4, 4);
        }
        v60 = *(_DWORD *)(v59 + 16);
        if ( _InterlockedDecrement((volatile signed __int32 *)(v59 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v59)(v59, 1);
        if ( v60 != 0 )
          goto LABEL_229;
        v61 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 19, 1);
        if ( *(_DWORD *)(v61 + 16) != 0 )
          goto LABEL_229;
        v62 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 8, 4);
        if ( *(_DWORD *)(v62 + 16) != 0 )
          goto LABEL_229;
        v63 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 16, 2);
        if ( *(_DWORD *)(v63 + 16) != 0 )
          goto LABEL_229;
        v64 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 20, 1);
        if ( *(_DWORD *)(v64 + 16) != 0 )
          goto LABEL_229;
        v65 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 21, 1);
        if ( *(_DWORD *)(v65 + 16) != 0 )
          goto LABEL_229;
        v66 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 22, 1);
        if ( *(_DWORD *)(v66 + 16) != 0 )
          goto LABEL_229;
        v67 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, v53 + 12, 4);
        if ( *(_DWORD *)(v67 + 16) != 0 || *(_DWORD *)(v122 + 16) != 0 )
          goto LABEL_229;
        sub_140E5CBB0(a1, v53);
        v68 = *(unsigned __int16 *)(v53 + 6);
        if ( (v68 != 1900 || (*v58 & 0x1FF) != 1) && (*(_WORD *)v53 & 0x1FF) == 1 && *(_WORD *)(v53 + 2) == 1900 )
          *(_DWORD *)v53 = v114;
        v69 = *v58;
        v18 = *v58 & 0x1FF;
        if ( (_WORD)v18 == 1 )
        {
          v18 = (unsigned __int16)v68;
          if ( (unsigned __int16)v68 == 1900 )
          {
            v18 = *(_WORD *)v53 & 0x1FF;
            LOWORD(v68) = 1900;
            if ( (_WORD)v18 == 1 )
            {
              v18 = *(unsigned __int16 *)(v53 + 2);
              if ( (_DWORD)v18 == 1900 )
              {
                *(_DWORD *)v53 = v114;
                *(_WORD *)v53 = 1;
                *(_DWORD *)(v53 + 4) = v114;
                LOWORD(v68) = v117;
                *(_WORD *)(v53 + 6) = v117;
                *(_BYTE *)(v53 + 19) = 1;
                v69 = v112;
              }
            }
          }
        }
        if ( (v69 & 0x1FF) == 1 && (unsigned __int16)v68 == 1900 )
        {
          v70 = *(_WORD *)(v53 + 2);
          if ( v70 <= v109 && (v70 < v109 || (unsigned __int16)(*(_WORD *)v53 & 0x1FF) <= v112) )
          {
            *(_WORD *)v53 = 1;
            *(_WORD *)(v53 + 2) = v109;
          }
          v71 = *(_DWORD *)v53;
          *(_DWORD *)(v53 + 4) = *(_DWORD *)v53;
          *(_WORD *)(v53 + 6) = HIWORD(v71) + 1;
          v72 = 15;
          if ( (unsigned __int16)(23593 * (HIWORD(v71) + 1)) >= 0xA3Eu )
            v72 = 3;
          v73 = ((v72 & (HIWORD(v71) + 1)) == 0) + 365;
          v18 = (v71 & 0x1FF) - 1;
          if ( v73 == (v71 & 0x1FF) - 1 )
            *v58 = v71 & 0xFE00 | v73;
          *(_BYTE *)(v53 + 19) = 1;
        }
        ++v52;
        LODWORD(a4) = v115;
      }
      while ( v52 < v127 );
    }
  }
  if ( v125 == &v127 )
  {
    v74 = v124 + 1;
    v124 = v74;
    v125 = (char *)v128;
    a3 = v126;
    if ( v74 == 0 )
      goto LABEL_166;
  }
  else
  {
    a3 = v126;
    if ( v124 != 0 && v122 != 0 )
      (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v124);
    v123 = &v127;
    v124 = 1;
    v125 = (char *)v128;
    v74 = 1;
  }
  if ( v122 != 0 )
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v74);
LABEL_166:
  v125 = nullptr;
  v124 = 0;
  v123 = nullptr;
  v75 = v127;
  if ( v127 > 0 )
  {
    v76 = *(__int64 **)(a1 + 312);
    if ( v76 == nullptr )
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
      v76 = (__int64 *)sub_1407E4490(&unk_141B59A68, 24);
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      v76[2] = 0;
      v76[1] = 0;
      *v76 = 0;
      *(_QWORD *)(a1 + 312) = v76;
      v75 = v127;
    }
    v77 = v75;
    v78 = *v76;
    v79 = (v76[2] - *v76) >> 3;
    if ( v79 < v75 )
    {
      if ( v75 < 0 )
        sub_1400526C0(v79, v18);
      v80 = v76[1];
      v81 = sub_1407E4490(qword_141ABD470, 8LL * v75);
      sub_141758A00(v81, *v76, v76[1] - *v76);
      v82 = *v76;
      if ( *v76 != 0 )
      {
        v83 = v76[2] - v82;
        if ( v83 == -1 )
          v83 = *(unsigned int *)(v82 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v84 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v84) >> 3 > v83)
          && (v85 = *(_QWORD *)(v84 + 8 * v83)) != 0 )
        {
          v118 = v85;
          MEMORY[0x1419475D8](v85 + 32, v82 - *(unsigned int *)(v85 + 120));
          v86 = *(_BYTE *)(v118 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v118 + 64)) != 0;
          if ( !v86 && *(_BYTE *)(v118 + 97) != 0 )
            sub_1412D33C0(v118);
        }
        else
        {
          MEMORY[0x141948990](v82 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *v76 = v81;
      v76[1] = v81 + v80 - v78;
      v76[2] = v81 + 8 * v77;
      v75 = v127;
    }
    LODWORD(a4) = v115;
    a3 = v126;
    if ( v75 > 0 )
    {
      v87 = 0;
      do
      {
        if ( dword_141B5DC48 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B5DC48);
          if ( dword_141B5DC48 == -1 )
          {
            sub_1407E53D0((unsigned int)&unk_141B5DBF8, 1100140931, 0x8000, 12, 0, 0, 1024, 0);
            sub_141751048(sub_140E9BF60);
            sub_141750EA0(&dword_141B5DC48);
          }
        }
        v119 = v87;
        a4 = sub_1407E58C0(&unk_141B5DBF8, 12);
        *(_QWORD *)a4 = -1;
        *(_BYTE *)(a4 + 10) = 0;
        *(_WORD *)(a4 + 8) = 0;
        if ( v124 != 0 && v122 != 0 )
          (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
        v125 = nullptr;
        v124 = 0;
        v123 = nullptr;
        v91 = v122;
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)v122 + 40LL))(v122, &v120, 1);
        if ( *(_DWORD *)(v91 + 16) != 0 )
          goto LABEL_229;
        v92 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a4 + 10, 1);
        if ( *(_DWORD *)(v92 + 16) != 0 )
          goto LABEL_229;
        v93 = v122;
        if ( v122 != 0 )
        {
          _InterlockedIncrement((volatile signed __int32 *)(v122 + 8));
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v93 + 40LL))(v93, a4, 8);
        }
        if ( *(_DWORD *)(a4 + 4) == 0 )
          *(_DWORD *)(a4 + 4) = *(_DWORD *)a4;
        v94 = *(_DWORD *)(v93 + 16);
        if ( _InterlockedDecrement((volatile signed __int32 *)(v93 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v93)(v93, 1);
        if ( v94 != 0 )
          goto LABEL_229;
        v95 = v122;
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v122 + 40LL))(v122, a4 + 8, 2);
        if ( *(_DWORD *)(v95 + 16) != 0 || *(_DWORD *)(v122 + 16) != 0 )
          goto LABEL_229;
        v96 = *(__int64 **)(a1 + 312);
        v89 = *v96;
        v97 = v96[1];
        v98 = (v97 - *v96) >> 3;
        v90 = v119;
        if ( v98 > v119 && *(_QWORD *)(v89 + 8 * v119) != 0 )
        {
          sub_140E9BDF0(*(_QWORD *)(v89 + 8 * v119));
          v89 = *v96;
          v97 = v96[1];
          v98 = (v97 - *v96) >> 3;
        }
        v87 = v119 + 1;
        if ( v98 <= v119 )
        {
          v99 = (v96[2] - v89) >> 3;
          if ( v99 > v119 )
          {
            v88 = v97 + 8 * (v87 - v98);
            sub_141758A10(v97, 0, 8 * (v87 - v98));
            v96[1] = v88;
            v89 = *v96;
          }
          else
          {
            v100 = v99 + (v99 >> 1);
            if ( v100 <= v87 )
              v100 = v119 + 1;
            if ( v99 > 0x1FFFFFFFFFFFFFFFLL - (v99 >> 1) )
              v100 = 0x1FFFFFFFFFFFFFFFLL;
            v89 = sub_1407E4490(qword_141ABD470, 8 * v100);
            sub_141758A10(v89 + 8 * v98, 0, 8 * (v87 - v98));
            sub_141758A00(v89, *v96, v96[1] - *v96);
            v101 = *v96;
            if ( *v96 != 0 )
            {
              v102 = v96[2] - v101;
              if ( v102 == -1 )
                v102 = *(unsigned int *)(v101 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v103 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v103) >> 3 > v102)
                && (v104 = *(_QWORD *)(v103 + 8 * v102)) != 0 )
              {
                v110 = v104;
                MEMORY[0x1419475D8](v104 + 32, v101 - *(unsigned int *)(v104 + 120));
                v105 = *(_BYTE *)(v110 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v110 + 64)) != 0;
                if ( !v105 && *(_BYTE *)(v110 + 97) != 0 )
                  sub_1412D33C0(v110);
              }
              else
              {
                MEMORY[0x141948990](v101 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *v96 = v89;
            v96[1] = v89 + 8 * v87;
            v96[2] = v89 + 8 * v100;
          }
          v90 = v119;
        }
        *(_QWORD *)(v89 + 8 * v90) = a4;
        LODWORD(a4) = v115;
        a3 = v126;
      }
      while ( (__int64)v87 < v127 );
    }
  }
  if ( v125 != (char *)(a1 + 360) )
  {
    v13 = a7;
    if ( v124 != 0 && v122 != 0 )
      (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v124);
    v123 = (char *)(a1 + 360);
    v124 = 2;
    v125 = (char *)(a1 + 362);
    v12 = (char *)(a1 + 320);
    v106 = 2;
    goto LABEL_236;
  }
  v12 = (char *)(a1 + 320);
  v37 = v124 == -2;
  v106 = v124 + 2;
  v124 += 2;
  v125 = (char *)(a1 + 362);
  v13 = a7;
  if ( !v37 )
  {
LABEL_236:
    if ( v122 != 0 )
      (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, v123, v106);
  }
  v123 = v12;
  v124 = 4;
  v125 = (char *)(a1 + 324);
LABEL_239:
  if ( a3 == 0 )
    goto LABEL_244;
  if ( v124 != 0 && v122 != 0 )
    (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
  v125 = nullptr;
  v124 = 0;
  v123 = nullptr;
  LODWORD(v12) = 0;
  if ( (unsigned __int8)sub_1411D1730(a1, (unsigned int)&v122, 0, a4, a5, a6, v13, a8) != 0 )
LABEL_244:
    LOBYTE(v12) = 1;
LABEL_245:
  if ( v124 != 0 )
  {
    if ( v122 == 0 )
      return (unsigned int)v12;
    (*(void (__fastcall **)(__int64, char *))(*(_QWORD *)v122 + 40LL))(v122, v123);
  }
  v107 = (void (__fastcall ***)(_QWORD, __int64))v122;
  v125 = nullptr;
  v124 = 0;
  v123 = nullptr;
  if ( v122 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122 + 8)) == 0 )
    (**v107)(v107, 1);
  return (unsigned int)v12;
}
