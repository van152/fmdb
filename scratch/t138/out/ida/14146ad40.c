char __fastcall sub_14146AD40(__int64 *a1, _QWORD *a2, __int64 a3)
{
  __int64 v6; // rsi
  unsigned __int8 v7; // al
  __int64 *v8; // rcx
  __int64 v9; // rbx
  __int64 v10; // r15
  __int64 *v11; // rsi
  __int64 v12; // rbp
  __int64 v13; // r12
  __int64 v14; // rdi
  unsigned __int64 v15; // rcx
  __int64 v16; // r8
  __int64 v17; // r14
  bool v18; // al
  _QWORD *v19; // r14
  __int64 *v20; // rbx
  __int64 v21; // rsi
  __int64 v22; // r13
  __int64 v23; // rbp
  __int64 *v24; // r12
  unsigned __int64 v25; // r15
  unsigned __int64 v26; // rsi
  __int64 v27; // r14
  __int64 *v28; // rdi
  __int64 v29; // rdi
  unsigned __int64 v30; // rcx
  __int64 v31; // rbx
  __int64 v32; // r12
  bool v33; // al
  __int64 v34; // rsi
  unsigned __int8 v35; // al
  __int64 v36; // rbp
  __int64 v37; // r15
  __int64 v38; // rsi
  __int64 v39; // r12
  __int64 v40; // rdi
  unsigned __int64 v41; // rcx
  __int64 v42; // r8
  __int64 v43; // r14
  bool v44; // al
  __int64 v45; // rsi
  _QWORD *v46; // rdi
  __int64 v47; // r14
  __int64 *v48; // r12
  __int64 v49; // r13
  unsigned __int64 v50; // rax
  unsigned __int64 v51; // r15
  unsigned __int64 v52; // rcx
  unsigned __int64 v53; // r15
  __int64 v54; // rbp
  __int64 *v55; // rdi
  __int64 v56; // rdi
  unsigned __int64 v57; // rcx
  __int64 v58; // r8
  __int64 v59; // r14
  bool v60; // al
  __int64 v61; // rsi
  __int64 v62; // rax
  __int64 v63; // rcx
  __int64 v64; // rsi
  __int64 v65; // rax
  __int64 v66; // rcx
  __int64 v67; // rsi
  _QWORD *v68; // rax
  __int64 v69; // rsi
  _QWORD *v70; // rax
  __int64 v71; // rsi
  __int64 v72; // rax
  __int64 v73; // rsi
  char result; // al
  __int64 v75; // rsi
  char v76; // [rsp+4Eh] [rbp-6Ah] BYREF
  unsigned __int8 v77; // [rsp+4Fh] [rbp-69h] BYREF
  char v78[8]; // [rsp+50h] [rbp-68h] BYREF
  __int64 *v79; // [rsp+58h] [rbp-60h]
  _QWORD *v80; // [rsp+60h] [rbp-58h]
  unsigned __int64 v81; // [rsp+68h] [rbp-50h]
  __int64 v82; // [rsp+70h] [rbp-48h]

  sub_140F9F4A0(a1: v78);
  v76 = 0;
  v77 = 0;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v77, a3: 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    goto LABEL_111;
  v82 = a3;
  v80 = a2;
  v7 = v77;
  v8 = a1;
  v9 = v77;
  v10 = *v8;
  v79 = v8;
  if ( (v8[2] - v10) >> 3 < (unsigned __int64)v77 )
  {
    v11 = v79;
    v12 = v79[1];
    v13 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v77);
    sub_141758A00(a1: v13, a2: *v11, a3: v11[1] - *v11);
    v14 = *v11;
    if ( *v11 != 0 )
    {
      v15 = v11[2] - v14;
      if ( v15 == -1 )
        v15 = *(unsigned int *)(v14 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v16 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v16) >> 3 > v15)
        && (v17 = *(_QWORD *)(v16 + 8 * v15)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v17 + 32, a2: v14 - *(unsigned int *)(v17 + 120));
        v18 = *(_BYTE *)(v17 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17 + 64)) != 0;
        v11 = v79;
        if ( !v18 && *(_BYTE *)(v17 + 97) != 0 )
          sub_1412D33C0(a1: v17);
      }
      else
      {
        MEMORY[0x141948990](a1: v14 - *(unsigned int *)(qword_141ABD470 + 48));
        v11 = v79;
      }
    }
    *v11 = v13;
    v11[1] = v13 + v12 - v10;
    v11[2] = v13 + 8 * v9;
    v7 = v77;
  }
  v19 = v80;
  v20 = v79;
  v21 = v82;
  if ( v7 != 0 )
  {
    v22 = 0;
    while ( 1 )
    {
      if ( dword_141B64138 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B64138);
        if ( dword_141B64138 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B640E8,
            a2: 1100122107,
            a3: 512,
            a4: 56,
            a5: 0,
            a6: 0,
            a7: 512,
            a8: 4096);
          sub_141751048(a1: sub_14146CD60);
          sub_141750EA0(a1: &dword_141B64138);
        }
      }
      v23 = sub_1407E58C0(a1: &unk_141B640E8, a2: 56);
      *(_QWORD *)v23 = 0;
      *(_DWORD *)(v23 + 32) = 124518401;
      *(_QWORD *)(v23 + 8) = 0;
      *(_QWORD *)(v23 + 16) = 0;
      *(_QWORD *)(v23 + 24) = 0;
      *(_QWORD *)(v23 + 36) = -1;
      *(_WORD *)(v23 + 44) = 0;
      *(_BYTE *)(v23 + 46) = 0;
      *(_DWORD *)(v23 + 47) = 16711683;
      *(_WORD *)(v23 + 51) = -1;
      if ( *(unsigned __int16 *)(v21 + 1416) < 0xDC9u )
      {
        if ( (unsigned __int8)sub_141470930(a1: v23, a2: v19) == 0 )
          goto LABEL_111;
      }
      else if ( (unsigned __int8)sub_141470F40(a1: v23, a2: v19) == 0 )
      {
        goto LABEL_111;
      }
      v24 = (__int64 *)v20[1];
      v25 = ((__int64)v24 - *v20) >> 3;
      if ( v24 == (__int64 *)v20[2] )
        break;
      *v24 = v23;
      v20[1] += 8;
LABEL_16:
      *(_BYTE *)(v23 + 49) = v25;
      if ( ++v22 >= (unsigned __int64)v77 )
        goto LABEL_46;
    }
    v26 = v25 + (v25 >> 1);
    v81 = v25 + 1;
    if ( v26 <= v25 + 1 )
      v26 = v25 + 1;
    if ( v25 > 0x1FFFFFFFFFFFFFFFLL - (v25 >> 1) )
      v26 = 0x1FFFFFFFFFFFFFFFLL;
    v27 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v26);
    *(_QWORD *)(v27 + 8 * v25) = v23;
    v28 = (__int64 *)v20[1];
    sub_141758A00(a1: v27, a2: *v20, a3: (char *)v24 - *v20);
    if ( v28 != v24 )
      sub_141758A00(a1: v27 + 8 * v25 + 8, a2: v24, a3: v20[1] - (_QWORD)v24);
    v29 = *v20;
    if ( *v20 == 0 )
    {
LABEL_39:
      *v20 = v27;
      v20[1] = v27 + 8 * v81;
      v20[2] = v27 + 8 * v26;
      v19 = v80;
      v21 = v82;
      goto LABEL_16;
    }
    v30 = v20[2] - v29;
    if ( v30 == -1 )
    {
      v30 = *(unsigned int *)(v29 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_38:
        MEMORY[0x141948990](a1: v29 - *(unsigned int *)(qword_141ABD470 + 48));
        v20 = v79;
        goto LABEL_39;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_38;
    }
    v31 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v31) >> 3 > v30 )
    {
      v32 = *(_QWORD *)(v31 + 8 * v30);
      if ( v32 != 0 )
      {
        MEMORY[0x1419475D8](a1: v32 + 32, a2: v29 - *(unsigned int *)(v32 + 120));
        v33 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
        v20 = v79;
        if ( !v33 && *(_BYTE *)(v32 + 97) != 0 )
          sub_1412D33C0(a1: v32);
        goto LABEL_39;
      }
    }
    goto LABEL_38;
  }
LABEL_46:
  v34 = *v19;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*v19 + 40LL))(a1: *v19, a2: &v77, a3: 1);
  if ( *(_DWORD *)(v34 + 16) != 0 )
    goto LABEL_111;
  v35 = v77;
  v36 = v77;
  v37 = v20[3];
  if ( (v20[5] - v37) >> 3 < (unsigned __int64)v77 )
  {
    v38 = v20[4];
    v39 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v77);
    sub_141758A00(a1: v39, a2: v20[3], a3: v20[4] - v20[3]);
    v40 = v20[3];
    if ( v40 != 0 )
    {
      v41 = v20[5] - v40;
      if ( v41 == -1 )
        v41 = *(unsigned int *)(v40 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v42 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v42) >> 3 > v41)
        && (v43 = *(_QWORD *)(v42 + 8 * v41)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v43 + 32, a2: v40 - *(unsigned int *)(v43 + 120));
        v44 = *(_BYTE *)(v43 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v43 + 64)) != 0;
        v20 = v79;
        if ( !v44 && *(_BYTE *)(v43 + 97) != 0 )
          sub_1412D33C0(a1: v43);
      }
      else
      {
        MEMORY[0x141948990](a1: v40 - *(unsigned int *)(qword_141ABD470 + 48));
        v20 = v79;
      }
    }
    v20[3] = v39;
    v20[4] = v39 + v38 - v37;
    v20[5] = v39 + 8 * v36;
    v35 = v77;
    v19 = v80;
  }
  if ( v35 != 0 )
  {
    v45 = 0;
    while ( 1 )
    {
      v46 = v19;
      if ( dword_141B5B780 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5B780);
        if ( dword_141B5B780 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5B730,
            a2: 1100141344,
            a3: 64,
            a4: 32,
            a5: 0,
            a6: 0,
            a7: 64,
            a8: 4096);
          sub_141751048(a1: sub_140B18F10);
          sub_141750EA0(a1: &dword_141B5B780);
        }
      }
      v47 = sub_1407E58C0(a1: &unk_141B5B730, a2: 32);
      *(_DWORD *)v47 = -1;
      *(_WORD *)(v47 + 4) = 2815;
      *(_QWORD *)(v47 + 16) = -4170448895LL;
      *(_DWORD *)(v47 + 24) = -1;
      *(_WORD *)(v47 + 28) = -1;
      *(_QWORD *)(v47 + 8) = 0;
      if ( *(unsigned __int16 *)(v82 + 1416) < 0xDC9u )
      {
        if ( (unsigned __int8)sub_1413C60C0(a1: v47, a2: v46) == 0 )
          goto LABEL_111;
      }
      else if ( (unsigned __int8)sub_1413C62C0(a1: v47, a2: v46) == 0 )
      {
        goto LABEL_111;
      }
      v48 = (__int64 *)v20[4];
      if ( v48 == (__int64 *)v20[5] )
        break;
      *v48 = v47;
      v20[4] += 8;
      v19 = v46;
LABEL_61:
      if ( ++v45 >= (unsigned __int64)v77 )
        goto LABEL_91;
    }
    v49 = (__int64)v48 - v20[3];
    v50 = v49 >> 3;
    v51 = (unsigned __int64)(v49 >> 3) >> 1;
    v52 = 0x1FFFFFFFFFFFFFFFLL - v51;
    v53 = (v49 >> 3) + v51;
    v81 = (v49 >> 3) + 1;
    if ( v53 <= v81 )
      v53 = v50 + 1;
    if ( v50 > v52 )
      v53 = 0x1FFFFFFFFFFFFFFFLL;
    v54 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v53);
    *(_QWORD *)(v54 + v49) = v47;
    v55 = (__int64 *)v20[4];
    sub_141758A00(a1: v54, a2: v20[3], a3: (char *)v48 - v20[3]);
    if ( v55 != v48 )
      sub_141758A00(a1: v54 + v49 + 8, a2: v48, a3: v20[4] - (_QWORD)v48);
    v56 = v20[3];
    if ( v56 == 0 )
    {
LABEL_84:
      v20[3] = v54;
      v20[4] = v54 + 8 * v81;
      v20[5] = v54 + 8 * v53;
      v19 = v80;
      goto LABEL_61;
    }
    v57 = v20[5] - v56;
    if ( v57 == -1 )
    {
      v57 = *(unsigned int *)(v56 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_83:
        MEMORY[0x141948990](a1: v56 - *(unsigned int *)(qword_141ABD470 + 48));
        v20 = v79;
        goto LABEL_84;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_83;
    }
    v58 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v58) >> 3 > v57 )
    {
      v59 = *(_QWORD *)(v58 + 8 * v57);
      if ( v59 != 0 )
      {
        MEMORY[0x1419475D8](a1: v59 + 32, a2: v56 - *(unsigned int *)(v59 + 120));
        v60 = *(_BYTE *)(v59 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v59 + 64)) != 0;
        v20 = v79;
        if ( !v60 && *(_BYTE *)(v59 + 97) != 0 )
          sub_1412D33C0(a1: v59);
        goto LABEL_84;
      }
    }
    goto LABEL_83;
  }
LABEL_91:
  v61 = *v19;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v19 + 40LL))(a1: *v19, a2: &v76, a3: 1);
  if ( *(_DWORD *)(v61 + 16) != 0 )
    goto LABEL_111;
  if ( v76 != 0 )
  {
    v62 = sub_14146CD70();
    *(_DWORD *)v62 = 124518401;
    *(_DWORD *)(v62 + 32) = 0;
    *(_BYTE *)(v62 + 38) = 0;
    *(_BYTE *)(v62 + 41) = 0;
    *(_QWORD *)(v62 + 4) = 0xFFFFFFFF00000000uLL;
    *(_QWORD *)(v62 + 16) = 0;
    *(_QWORD *)(v62 + 24) = 0;
    *(_DWORD *)(v62 + 12) = -1;
    *(_WORD *)(v62 + 36) = 0;
    *(_WORD *)(v62 + 39) = 0;
    v63 = v20[6];
    v20[6] = v62;
    if ( v63 != 0 )
    {
      sub_140E41E60();
      v62 = v20[6];
    }
    if ( (unsigned __int8)sub_14146B8B0(a1: v62, a2: v19) == 0 )
      goto LABEL_111;
  }
  v64 = *v19;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v19 + 40LL))(a1: *v19, a2: &v76, a3: 1);
  if ( *(_DWORD *)(v64 + 16) != 0 )
    goto LABEL_111;
  if ( v76 != 0 )
  {
    v65 = sub_14146CE20();
    *(_QWORD *)(v65 + 40) = 0;
    *(_QWORD *)(v65 + 12) = -1;
    *(_QWORD *)(v65 + 20) = -1;
    *(_DWORD *)(v65 + 28) = -1;
    *(_QWORD *)(v65 + 32) = 0xFFFFFFFF00000000uLL;
    *(_DWORD *)(v65 + 8) = 0;
    *(_QWORD *)v65 = 0;
    *(_QWORD *)(v65 + 48) = 0;
    *(_WORD *)(v65 + 56) = 0;
    v66 = v20[7];
    v20[7] = v65;
    if ( v66 != 0 )
    {
      sub_140E41FE0();
      v65 = v20[7];
    }
    if ( (unsigned __int8)sub_14146BA90(a1: v65, a2: v19) == 0 )
      goto LABEL_111;
  }
  v67 = *v19;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v19 + 40LL))(a1: *v19, a2: &v76, a3: 1);
  if ( *(_DWORD *)(v67 + 16) != 0 )
    goto LABEL_111;
  if ( v76 != 0 )
  {
    v68 = (_QWORD *)sub_140E15560(a1: 64);
    *v68 = 0;
    v68[1] = 0x76C0001076C0001LL;
    v68[2] = 0;
    v68[3] = 0;
    v68[4] = 0;
    v68[5] = 0;
    v68[6] = 0;
    v68[7] = 0;
    v20[8] = (__int64)v68;
    if ( (unsigned __int8)sub_14146BD20(a1: v68, a2: v19) == 0 )
      goto LABEL_111;
  }
  v69 = *v19;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v19 + 40LL))(a1: *v19, a2: &v76, a3: 1);
  if ( *(_DWORD *)(v69 + 16) != 0 )
    goto LABEL_111;
  if ( v76 != 0 )
  {
    v70 = (_QWORD *)sub_140E15360(a1: 16);
    *v70 = 124518401;
    v70[1] = 0;
    v20[9] = (__int64)v70;
    if ( (unsigned __int8)sub_14146BF70(a1: v70, a2: v19) == 0 )
      goto LABEL_111;
  }
  v71 = *v19;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v19 + 40LL))(a1: *v19, a2: &v76, a3: 1);
  if ( *(_DWORD *)(v71 + 16) != 0 )
    goto LABEL_111;
  if ( v76 != 0 )
  {
    v72 = sub_140E15410(a1: 24);
    *(_DWORD *)v72 = 124518401;
    *(_QWORD *)(v72 + 4) = 0;
    *(_QWORD *)(v72 + 12) = 0;
    *(_DWORD *)(v72 + 20) = 0;
    v20[10] = v72;
    if ( (unsigned __int8)sub_14146C040(a1: v72, a2: v19) == 0 )
      goto LABEL_111;
  }
  v73 = *v19;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v19 + 40LL))(a1: *v19, a2: &v76, a3: 1);
  if ( *(_DWORD *)(v73 + 16) != 0
    || v76 != 0
    && (v75 = sub_140E140E0(a1: 40),
        sub_1414724A0(a1: v75),
        v79[11] = v75,
        (unsigned __int8)sub_141473960(a1: v75, a2: v80) == 0) )
  {
LABEL_111:
    result = 0;
    if ( v78[0] != 0 )
      return result;
    goto LABEL_112;
  }
  result = 1;
  if ( v78[0] == 0 )
LABEL_112:
    byte_141B5FC2C = 0;
  return result;
}
