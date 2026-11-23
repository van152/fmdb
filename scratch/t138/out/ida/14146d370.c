__int64 __fastcall sub_14146D370(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v8; // rsi
  __int64 v9; // rdi
  __int64 v10; // rbp
  __int64 v11; // rbx
  __int64 v12; // rdx
  unsigned __int64 v13; // rsi
  __int64 v14; // rbp
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 *v21; // r15
  __int64 v22; // r8
  __int64 v23; // r12
  unsigned __int64 v24; // rax
  unsigned __int64 v25; // rbx
  unsigned __int64 v26; // rcx
  unsigned __int64 v27; // rbx
  __int64 v28; // rdi
  __int64 *v29; // rbp
  __int64 v30; // rbp
  unsigned __int64 v31; // rcx
  __int64 v32; // r8
  __int64 v33; // r15
  bool v34; // al
  __int64 v35; // rbp
  __int64 v36; // r15
  __int64 v37; // rbp
  __int64 v38; // rbx
  __int64 v39; // r12
  __int64 v40; // rcx
  int v41; // edi
  int v42; // eax
  int v43; // edx
  unsigned __int16 v44; // r10
  int v45; // r9d
  unsigned __int16 v46; // r11
  __int64 v47; // rbx
  __int64 v48; // rdx
  __int64 v49; // r8
  __int64 v50; // rcx
  __int64 v51; // rsi
  __int64 v52; // rax
  __int64 v53; // r12
  _QWORD *v54; // rsi
  char v55; // r15
  _QWORD *v56; // rbp
  char v57; // al
  char v58; // bl
  __int64 v59; // rbp
  unsigned __int64 v60; // rdi
  unsigned __int64 v61; // rcx
  unsigned __int64 v62; // rdi
  __int64 v63; // rsi
  _DWORD *v64; // rbx
  char v65; // di
  unsigned __int8 v66; // al
  __int64 v67; // rbp
  unsigned __int64 v68; // rax
  __int64 v69; // rbx
  __int64 v70; // rbx
  __int64 v71; // rbx
  __int64 v72; // rbp
  __int64 v73; // rbx
  __int64 v74; // rbx
  __int64 v75; // rbx
  __int64 v76; // rbx
  __int64 v77; // rbx
  _QWORD *v78; // rax
  __int64 v79; // rcx
  char v80; // [rsp+4Dh] [rbp-6Bh] BYREF
  __int16 v81; // [rsp+4Eh] [rbp-6Ah] BYREF
  __int64 v82; // [rsp+50h] [rbp-68h] BYREF
  unsigned int v83; // [rsp+5Ch] [rbp-5Ch] BYREF
  char v84[8]; // [rsp+60h] [rbp-58h] BYREF
  unsigned __int64 v85; // [rsp+68h] [rbp-50h]
  unsigned __int64 v86; // [rsp+70h] [rbp-48h]

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v81, a3: 2);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return 0;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 162, a3: 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return 0;
  v83 = 0;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v83, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return 0;
  v8 = v83;
  v9 = *(_QWORD *)(a1 + 56);
  if ( (*(_QWORD *)(a1 + 72) - v9) >> 3 >= (unsigned __int64)v83 )
  {
    v11 = *(_QWORD *)(a1 + 56);
  }
  else
  {
    v10 = *(_QWORD *)(a1 + 64);
    v11 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v83);
    sub_141758A00(a1: v11, a2: *(_QWORD *)(a1 + 56), a3: *(_QWORD *)(a1 + 64) - *(_QWORD *)(a1 + 56));
    v12 = *(_QWORD *)(a1 + 56);
    if ( v12 != 0 )
      sub_1407E4890(a1: qword_141ABD470, a2: v12, a3: *(_QWORD *)(a1 + 72) - v12);
    *(_QWORD *)(a1 + 56) = v11;
    *(_QWORD *)(a1 + 64) = v11 + v10 - v9;
    *(_QWORD *)(a1 + 72) = v11 + 8 * v8;
    LODWORD(v8) = v83;
  }
  if ( (_DWORD)v8 != 0 )
  {
    v13 = 0;
    do
    {
      if ( dword_141B5D5B0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5D5B0);
        if ( dword_141B5D5B0 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5D560,
            a2: 1100129513,
            a3: 256,
            a4: 32,
            a5: 0,
            a6: 0,
            a7: 256,
            a8: 4096);
          sub_141751048(a1: sub_140E40B20);
          sub_141750EA0(a1: &dword_141B5D5B0);
        }
      }
      v14 = sub_1407E58C0(a1: &unk_141B5D560, a2: 32);
      *(_QWORD *)v14 = 0;
      *(_QWORD *)(v14 + 8) = 0;
      *(_QWORD *)(v14 + 16) = 0x76C0001076C0001LL;
      *(_DWORD *)(v14 + 24) = 0;
      *(_WORD *)(v14 + 28) = 0;
      v15 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v82, a3: 2);
      if ( *(_DWORD *)(v15 + 16) != 0 )
        return 0;
      v16 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v14 + 28, a3: 1);
      if ( *(_DWORD *)(v16 + 16) != 0 )
        return 0;
      v17 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v14 + 24, a3: 4);
      if ( *(_DWORD *)(v17 + 16) != 0 )
        return 0;
      v18 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v14 + 29, a3: 1);
      if ( *(_DWORD *)(v18 + 16) != 0 )
        return 0;
      if ( HIWORD(qword_141B6034C) != 0 )
      {
        v19 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v14, a3: 4);
        if ( *(_DWORD *)(v19 + 16) != 0 )
          return 0;
        v20 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v14 + 8, a3: 4);
        if ( *(_DWORD *)(v20 + 16) != 0 )
          return 0;
      }
      else if ( (unsigned __int8)sub_140F83460(a1: v14, a2) == 0 || (unsigned __int8)sub_140F83460(a1: v14 + 8, a2) == 0 )
      {
        return 0;
      }
      if ( (unsigned __int8)sub_140DB8980(a1: v14 + 16, a2) == 0
        || (unsigned __int8)sub_140DB8980(a1: v14 + 20, a2) == 0 )
      {
        return 0;
      }
      v21 = *(__int64 **)(a1 + 64);
      if ( v21 == *(__int64 **)(a1 + 72) )
      {
        v85 = v13;
        v23 = (__int64)v21 - *(_QWORD *)(a1 + 56);
        v24 = v23 >> 3;
        v25 = (unsigned __int64)(v23 >> 3) >> 1;
        v26 = 0x1FFFFFFFFFFFFFFFLL - v25;
        v27 = (v23 >> 3) + v25;
        v86 = (v23 >> 3) + 1;
        if ( v27 <= v86 )
          v27 = v24 + 1;
        if ( v24 > v26 )
          v27 = 0x1FFFFFFFFFFFFFFFLL;
        v28 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v27);
        *(_QWORD *)(v28 + v23) = v14;
        v29 = *(__int64 **)(a1 + 64);
        sub_141758A00(a1: v28, a2: *(_QWORD *)(a1 + 56), a3: (char *)v21 - *(_QWORD *)(a1 + 56));
        if ( v29 != v21 )
          sub_141758A00(a1: v28 + v23 + 8, a2: v21, a3: *(_QWORD *)(a1 + 64) - (_QWORD)v21);
        v30 = *(_QWORD *)(a1 + 56);
        v13 = v85;
        if ( v30 != 0 )
        {
          v31 = *(_QWORD *)(a1 + 72) - v30;
          if ( v31 == -1 )
            v31 = *(unsigned int *)(v30 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v32 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v32) >> 3 > v31)
            && (v33 = *(_QWORD *)(v32 + 8 * v31)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v33 + 32, a2: v30 - *(unsigned int *)(v33 + 120));
            v34 = *(_BYTE *)(v33 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v33 + 64)) != 0;
            if ( !v34 && *(_BYTE *)(v33 + 97) != 0 )
              sub_1412D33C0(a1: v33);
          }
          else
          {
            MEMORY[0x141948990](a1: v30 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *(_QWORD *)(a1 + 56) = v28;
        v22 = v28 + 8 * v86;
        *(_QWORD *)(a1 + 64) = v22;
        *(_QWORD *)(a1 + 72) = v28 + 8 * v27;
      }
      else
      {
        *v21 = v14;
        v22 = *(_QWORD *)(a1 + 64) + 8LL;
        *(_QWORD *)(a1 + 64) = v22;
      }
      ++v13;
    }
    while ( v13 < v83 );
    v11 = *(_QWORD *)(a1 + 56);
  }
  else
  {
    v22 = *(_QWORD *)(a1 + 64);
  }
  v35 = v22 - v11;
  if ( v22 != v11 )
  {
    v36 = v35 >> 3;
    v37 = -(__int64)(v35 & 0xFFFFFFFFFFFFFFF8uLL);
    do
    {
      v38 = v36--;
      v39 = *(_QWORD *)(a1 + 56);
      v40 = *(_QWORD *)(v39 + 8 * v38 - 8);
      if ( v40 != 0 )
      {
        v41 = *(unsigned __int16 *)(v40 + 22);
        v42 = *(_WORD *)(v40 + 20) & 0x1FF;
        if ( v41 == 1900 && (_WORD)v42 == 1 )
          goto LABEL_55;
        v43 = dword_141AAE084 & 0x1FF;
        v44 = HIWORD(dword_141AAE084);
        v45 = 365;
        if ( HIWORD(dword_141AAE084) <= (unsigned __int16)v41
          && (HIWORD(dword_141AAE084) < (unsigned __int16)v41 || (unsigned __int16)v43 < (unsigned __int16)v42) )
        {
          v45 = -365;
          v46 = *(_WORD *)(v40 + 22);
        }
        else
        {
          v46 = HIWORD(dword_141AAE084);
          v44 = *(_WORD *)(v40 + 22);
        }
        if ( v45 * (v46 - v44) + v43 - v42 < 366 )
          goto LABEL_55;
        sub_140E409B0();
        v22 = *(_QWORD *)(a1 + 64);
      }
      sub_141758A00(a1: v39 + 8 * v38 - 8, a2: v39 + 8 * v38, a3: v37 + v22 - v39);
      v22 = *(_QWORD *)(a1 + 64) - 8LL;
      *(_QWORD *)(a1 + 64) = v22;
LABEL_55:
      v37 += 8;
    }
    while ( v36 != 0 );
  }
  v80 = 0;
  if ( v81 <= 25 )
  {
    v82 = 0;
    v47 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v80, a3: 1);
    if ( *(_DWORD *)(v47 + 16) != 0 )
      return 0;
    v50 = qword_141ABD470;
    if ( qword_141ABD470 == 0 )
    {
      v50 = sub_1407E4940(a1: 0, a2: v48, a3: v49);
      qword_141ABD470 = v50;
    }
    v51 = v80;
    if ( v80 != 0 )
    {
      if ( v80 < 0 )
        sub_1400526C0(a1: v50, a2: v48, a3: v49);
      v52 = sub_1407E4490(a1: v50, a2: 8LL * v80);
      v53 = v52;
      if ( v80 <= 0 )
      {
        if ( v52 != 0 )
          sub_1407E4890(a1: qword_141ABD470, a2: v52, a3: 8 * v51);
      }
      else
      {
        v54 = (_QWORD *)(v52 + 8 * v51);
        v55 = 0;
        v56 = (_QWORD *)v52;
        do
        {
          v57 = sub_140F938D0(
                  a1: (unsigned int)&qword_141B5FDA8,
                  a2: (unsigned int)&v82,
                  a3: (_DWORD)a2,
                  a4: qword_141B5FE08,
                  a5: (unsigned __int8)byte_141B5FC2C ^ 1u);
          if ( v57 == 0 )
          {
            if ( v53 != 0 )
              sub_1407E4890(a1: qword_141ABD470, a2: v53, a3: (char *)v54 - v53);
            return 0;
          }
          v58 = v57;
          if ( v56 == v54 )
          {
            LOBYTE(v85) = v57;
            v59 = (__int64)v56 - v53;
            v60 = (unsigned __int64)(v59 >> 3) >> 1;
            v61 = 0x1FFFFFFFFFFFFFFFLL - v60;
            v62 = (v59 >> 3) + v60;
            v86 = (v59 >> 3) + 1;
            if ( v62 <= v86 )
              v62 = (v59 >> 3) + 1;
            if ( v59 >> 3 > v61 )
              v62 = 0x1FFFFFFFFFFFFFFFLL;
            v63 = v53;
            v53 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v62);
            *(_QWORD *)(v53 + v59) = v82;
            sub_141758A00(a1: v53, a2: v63, a3: v59);
            if ( v63 != 0 )
              sub_1407E4890(a1: qword_141ABD470, a2: v63, a3: v59);
            v56 = (_QWORD *)(v53 + 8 * v86);
            v54 = (_QWORD *)(v53 + 8 * v62);
            v58 = v85;
          }
          else
          {
            *v56++ = v82;
          }
          ++v55;
        }
        while ( v55 < v80 );
        if ( v53 != 0 )
          sub_1407E4890(a1: qword_141ABD470, a2: v53, a3: (char *)v54 - v53);
        if ( v58 == 0 )
          return 0;
      }
    }
  }
  sub_14151D760(a1: &v82, a2, a3: a1 + 32, a4: v84);
  if ( (_DWORD)v82 != 0 )
    return 0;
  v64 = (_DWORD *)*a2;
  if ( *(_DWORD *)(*a2 + 16LL) != 0 )
    return 0;
  if ( v81 <= 25 )
  {
    v82 = 0;
    if ( (unsigned __int8)sub_140F938D0(
                            a1: (unsigned int)&qword_141B5FDA8,
                            a2: (unsigned int)&v82,
                            a3: (_DWORD)a2,
                            a4: qword_141B5FE08,
                            a5: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
      return 0;
    v64 = (_DWORD *)*a2;
  }
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v64 + 40LL))(a1: v64, a2: &v80, a3: 1);
  if ( v64[4] != 0 )
    return 0;
  if ( v80 > 0 )
  {
    v65 = 0;
    do
    {
      v67 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v82, a3: 1);
      if ( *(_DWORD *)(v67 + 16) != 0 )
        return 0;
      v68 = *(unsigned __int8 *)(a1 + 128);
      if ( v68 > 9 )
      {
        *(_BYTE *)(a1 + *(unsigned __int8 *)(a1 + 139) + 129) = v82;
        v66 = *(_BYTE *)(a1 + 139) + 1;
        if ( v66 >= 0xAu )
          v66 = 0;
        *(_BYTE *)(a1 + 139) = v66;
      }
      else
      {
        *(_BYTE *)(a1 + v68 + 129) = v82;
        *(_BYTE *)(a1 + 128) = v68 + 1;
      }
    }
    while ( ++v65 < v80 );
  }
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 140, a2) == 0 )
    return 0;
  v69 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 160, a3: 2);
  if ( *(_DWORD *)(v69 + 16) != 0 )
    return 0;
  v70 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 163, a3: 1);
  if ( *(_DWORD *)(v70 + 16) != 0
    || (unsigned __int8)sub_140DB8980(a1: a1 + 120, a2) == 0
    || v81 >= 28 && (unsigned __int8)sub_140DB8980(a1: a1 + 124, a2) == 0 )
  {
    return 0;
  }
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 148, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 144, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 152, a2) == 0 )
    return 0;
  v71 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 167, a3: 1);
  if ( *(_DWORD *)(v71 + 16) != 0 )
    return 0;
  v72 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 164, a3: 1);
  if ( *(_DWORD *)(v72 + 16) != 0 )
    return 0;
  if ( v81 <= 26 )
    *(_BYTE *)(a1 + 164) = (10995116280LL * *(char *)(a1 + 164) < 0) + 8 * *(char *)(a1 + 164) / 0x64uLL;
  v73 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 165, a3: 1);
  if ( *(_DWORD *)(v73 + 16) != 0 )
    return 0;
  v74 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 166, a3: 1);
  if ( *(_DWORD *)(v74 + 16) != 0 )
    return 0;
  v75 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 156, a3: 4);
  if ( *(_DWORD *)(v75 + 16) != 0 )
    return 0;
  v76 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 112, a3: 4);
  if ( *(_DWORD *)(v76 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_14146DE90(a1: a1 + 80, a2) == 0 )
    return 0;
  LOBYTE(v82) = 0;
  v77 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v82, a3: 1);
  if ( *(_DWORD *)(v77 + 16) != 0 )
    return 0;
  if ( (_BYTE)v82 != 0 )
  {
    v78 = (_QWORD *)sub_141750CC0(a1: 16);
    *v78 = 0x76C0001076C0001LL;
    v78[1] = 0xFFFFFFFF00000000uLL;
    v79 = *(_QWORD *)(a1 + 104);
    *(_QWORD *)(a1 + 104) = v78;
    if ( v79 != 0 )
    {
      sub_141750CFC(a1: v79);
      v78 = *(_QWORD **)(a1 + 104);
    }
    if ( (unsigned __int8)sub_14146CFC0(a1: v78, a2) == 0 )
      return 0;
  }
  return sub_14141F7B0(a1, a2);
}
