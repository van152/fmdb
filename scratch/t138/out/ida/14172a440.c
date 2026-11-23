bool __fastcall sub_14172A440(__int64 *a1, _QWORD *a2)
{
  _QWORD *v4; // rsi
  _QWORD *v5; // rbx
  _QWORD *v6; // rdi
  __int64 v7; // rdi
  __int64 v8; // rsi
  __int64 v9; // rsi
  __int64 v10; // rdx
  __int64 v11; // r8
  char v13; // al
  __int64 v14; // rdi
  __int64 v15; // r15
  unsigned __int64 v16; // rcx
  __int64 v17; // rsi
  __int64 v18; // rbx
  __int64 v19; // rbp
  unsigned __int64 v20; // rcx
  __int64 v21; // r8
  __int64 v22; // r14
  bool v23; // al
  _QWORD *v24; // rdi
  char v25; // r13
  __int64 v26; // r14
  __int64 v27; // rsi
  __int64 v28; // rbp
  __int64 v29; // rsi
  __int64 v30; // r15
  int v31; // esi
  __int64 *v32; // rsi
  __int64 v33; // rbx
  unsigned __int64 v34; // rax
  unsigned __int64 v35; // r15
  unsigned __int64 v36; // rcx
  unsigned __int64 v37; // r15
  __int64 v38; // rdi
  __int64 *v39; // rbp
  __int64 v40; // rbp
  unsigned __int64 v41; // rcx
  __int64 v42; // rbx
  __int64 v43; // rsi
  bool v44; // al
  char v45; // [rsp+44h] [rbp-54h] BYREF
  unsigned __int8 v46; // [rsp+45h] [rbp-53h] BYREF
  unsigned __int8 v47; // [rsp+46h] [rbp-52h] BYREF
  char v48; // [rsp+47h] [rbp-51h] BYREF
  _QWORD *v49; // [rsp+48h] [rbp-50h]
  unsigned __int64 v50; // [rsp+50h] [rbp-48h]

  v4 = (_QWORD *)*a1;
  v5 = (_QWORD *)a1[1];
  if ( (_QWORD *)*a1 != v5 )
  {
    v6 = (_QWORD *)*a1;
    do
    {
      if ( *v6 != 0 )
        sub_140E41CE0();
      ++v6;
    }
    while ( v6 != v5 );
    v7 = a1[1] - (_QWORD)v5;
    sub_141758A00(a1: v4, a2: v5, a3: v7);
    a1[1] = (__int64)v4 + v7;
  }
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v48, a3: 1);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v45, a3: 1);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v49 = a2;
  v13 = v45;
  v14 = v45;
  v15 = *a1;
  v16 = (a1[2] - *a1) >> 3;
  if ( v16 < v45 )
  {
    if ( v45 < 0 )
      sub_1400526C0(a1: v16, a2: v10, a3: v11);
    v17 = a1[1];
    v18 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v45);
    sub_141758A00(a1: v18, a2: *a1, a3: a1[1] - *a1);
    v19 = *a1;
    if ( *a1 != 0 )
    {
      v20 = a1[2] - v19;
      if ( v20 == -1 )
        v20 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v21 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v20)
        && (v22 = *(_QWORD *)(v21 + 8 * v20)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v22 + 32, a2: v19 - *(unsigned int *)(v22 + 120));
        v23 = *(_BYTE *)(v22 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 64)) != 0;
        if ( !v23 && *(_BYTE *)(v22 + 97) != 0 )
          sub_1412D33C0(a1: v22);
      }
      else
      {
        MEMORY[0x141948990](a1: v19 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *a1 = v18;
    a1[1] = v18 + v17 - v15;
    a1[2] = v18 + 8 * v14;
    v13 = v45;
  }
  v24 = v49;
  if ( v13 > 0 )
  {
    v25 = 0;
    while ( 1 )
    {
      if ( dword_141B5D878 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5D878);
        if ( dword_141B5D878 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5D828,
            a2: 1100150454,
            a3: 1024,
            a4: 24,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 0);
          sub_141751048(a1: sub_140E41E50);
          sub_141750EA0(a1: &dword_141B5D878);
        }
      }
      v26 = sub_1407E58C0(a1: &unk_141B5D828, a2: 24);
      *(_DWORD *)v26 = 91084;
      *(_WORD *)(v26 + 4) = 1900;
      *(_DWORD *)(v26 + 6) = dword_141AAE084;
      *(_QWORD *)(v26 + 10) = 0x1000100000000LL;
      *(_WORD *)(v26 + 18) = 0;
      *(_DWORD *)(v26 + 20) = 1310720;
      v27 = *v24;
      (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*v24 + 40LL))(a1: *v24, a2: &v46, a3: 1);
      if ( *(_DWORD *)(v27 + 16) != 0 )
        return false;
      (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*v24 + 40LL))(a1: *v24, a2: &v47, a3: 1);
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v24 + 40LL))(a1: *v24, a2: v26, a3: 2);
      if ( v47 <= 2u && (*(_WORD *)v26 & 0x1FC0) == 0x380 )
        *(_WORD *)v26 = *(_WORD *)v26 & 0xE03F | 0x3C0;
      v28 = *v24;
      if ( *(_DWORD *)(*v24 + 16LL) != 0 )
        return false;
      v29 = v26 + 20;
      _InterlockedIncrement((volatile signed __int32 *)(v28 + 8));
      v30 = 4;
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v28 + 40LL))(a1: v28, a2: v26 + 2, a3: 4);
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v28 + 40LL))(a1: v28, a2: v26 + 10, a3: 2);
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v28 + 40LL))(a1: v28, a2: v26 + 14, a3: 4);
      if ( v46 >= 2u )
      {
        (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v28 + 40LL))(a1: v28, a2: v26 + 20, a3: 4);
        if ( v46 < 3u )
        {
          v30 = 2;
          v29 = v26 + 18;
        }
        else
        {
          v29 = v26 + 6;
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v28 + 40LL))(a1: v28, a2: v26 + 18, a3: 2);
        }
      }
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v28 + 40LL))(a1: v28, a2: v29, a3: v30);
      v31 = *(_DWORD *)(v28 + 16);
      if ( _InterlockedDecrement((volatile signed __int32 *)(v28 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v28)(a1: v28, a2: 1);
      v24 = v49;
      if ( v31 != 0 )
        return false;
      v32 = (__int64 *)a1[1];
      if ( v32 == (__int64 *)a1[2] )
        break;
      *v32 = v26;
      a1[1] += 8;
LABEL_25:
      if ( ++v25 >= v45 )
        return *(_DWORD *)(*v24 + 16LL) == 0;
    }
    v33 = (__int64)v32 - *a1;
    v34 = v33 >> 3;
    v35 = (unsigned __int64)(v33 >> 3) >> 1;
    v36 = 0x1FFFFFFFFFFFFFFFLL - v35;
    v37 = (v33 >> 3) + v35;
    v50 = (v33 >> 3) + 1;
    if ( v37 <= v50 )
      v37 = v34 + 1;
    if ( v34 > v36 )
      v37 = 0x1FFFFFFFFFFFFFFFLL;
    v38 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v37);
    *(_QWORD *)(v38 + v33) = v26;
    v39 = (__int64 *)a1[1];
    sub_141758A00(a1: v38, a2: *a1, a3: (char *)v32 - *a1);
    if ( v39 != v32 )
      sub_141758A00(a1: v38 + v33 + 8, a2: v32, a3: a1[1] - (_QWORD)v32);
    v40 = *a1;
    if ( *a1 == 0 )
    {
LABEL_56:
      *a1 = v38;
      a1[1] = v38 + 8 * v50;
      a1[2] = v38 + 8 * v37;
      v24 = v49;
      goto LABEL_25;
    }
    v41 = a1[2] - v40;
    if ( v41 == -1 )
    {
      v41 = *(unsigned int *)(v40 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_55:
        MEMORY[0x141948990](a1: v40 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_56;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_55;
    }
    v42 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v42) >> 3 > v41 )
    {
      v43 = *(_QWORD *)(v42 + 8 * v41);
      if ( v43 != 0 )
      {
        MEMORY[0x1419475D8](a1: v43 + 32, a2: v40 - *(unsigned int *)(v43 + 120));
        v44 = *(_BYTE *)(v43 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v43 + 64)) != 0;
        if ( !v44 && *(_BYTE *)(v43 + 97) != 0 )
          sub_1412D33C0(a1: v43);
        goto LABEL_56;
      }
    }
    goto LABEL_55;
  }
  return *(_DWORD *)(*v24 + 16LL) == 0;
}
