bool __fastcall sub_1413F90A0(__int64 *a1, _QWORD *a2)
{
  _QWORD *v2; // rsi
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int16 v7; // ax
  __int64 v8; // r13
  __int64 v9; // r15
  __int64 v10; // rbp
  __int64 v11; // r12
  __int64 v12; // rbx
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // r14
  bool v16; // al
  int v17; // r12d
  __int64 v18; // r14
  __int64 *v19; // rbp
  __int64 v20; // r15
  unsigned __int64 v21; // rax
  unsigned __int64 v22; // r13
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // r13
  __int64 v25; // rbx
  __int64 *v26; // rsi
  __int64 v27; // rsi
  unsigned __int64 v28; // rcx
  __int64 v29; // rbp
  __int64 v30; // rbp
  bool v31; // al
  __int16 v32; // [rsp+44h] [rbp-54h] BYREF
  char v33; // [rsp+47h] [rbp-51h] BYREF
  _QWORD *v34; // [rsp+48h] [rbp-50h]
  unsigned __int64 v35; // [rsp+50h] [rbp-48h]

  v2 = a2;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v33, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v32 = 0;
  v5 = *v2;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v32, a3: 2);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v7 = v32;
  if ( v32 < 0 )
    return false;
  v8 = (unsigned __int16)v32;
  v9 = *a1;
  if ( (a1[2] - *a1) >> 3 < (unsigned __int64)(unsigned __int16)v32 )
  {
    v10 = a1[1];
    v11 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (unsigned __int16)v32);
    sub_141758A00(a1: v11, a2: *a1, a3: a1[1] - *a1);
    v12 = *a1;
    if ( *a1 != 0 )
    {
      v13 = a1[2] - v12;
      if ( v13 == -1 )
        v13 = *(unsigned int *)(v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v14 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13)
        && (v15 = *(_QWORD *)(v14 + 8 * v13)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v15 + 32, a2: v12 - *(unsigned int *)(v15 + 120));
        v16 = *(_BYTE *)(v15 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) != 0;
        if ( !v16 && *(_BYTE *)(v15 + 97) != 0 )
          sub_1412D33C0(a1: v15);
      }
      else
      {
        MEMORY[0x141948990](a1: v12 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *a1 = v11;
    a1[1] = v11 + v10 - v9;
    a1[2] = v11 + 8 * v8;
    v7 = v32;
  }
  if ( v7 > 0 )
  {
    v17 = 0;
    v34 = v2;
    while ( 1 )
    {
      if ( dword_141B5CBC0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5CBC0);
        if ( dword_141B5CBC0 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5CB70,
            a2: 1100154223,
            a3: 4096,
            a4: 40,
            a5: 0,
            a6: 0,
            a7: 512,
            a8: 4096);
          sub_141751048(a1: sub_140DD5990);
          sub_141750EA0(a1: &dword_141B5CBC0);
        }
      }
      v18 = sub_1407E58C0(a1: &unk_141B5CB70, a2: 40);
      *(_QWORD *)v18 = 0;
      *(_QWORD *)(v18 + 8) = 0;
      *(_QWORD *)(v18 + 16) = 0;
      *(_QWORD *)(v18 + 24) = 0;
      *(_DWORD *)(v18 + 32) = 124518401;
      *(_WORD *)(v18 + 36) = 1;
      if ( (unsigned __int8)sub_1413F94B0(a1: v18, a2: v2) == 0 )
        return false;
      v19 = (__int64 *)a1[1];
      if ( v19 == (__int64 *)a1[2] )
        break;
      *v19 = v18;
      a1[1] += 8;
LABEL_19:
      if ( (__int16)++v17 >= v32 )
        return *(_DWORD *)(*v2 + 16LL) == 0;
    }
    v20 = (__int64)v19 - *a1;
    v21 = v20 >> 3;
    v22 = (unsigned __int64)(v20 >> 3) >> 1;
    v23 = 0x1FFFFFFFFFFFFFFFLL - v22;
    v24 = (v20 >> 3) + v22;
    v35 = (v20 >> 3) + 1;
    if ( v24 <= v35 )
      v24 = v21 + 1;
    if ( v21 > v23 )
      v24 = 0x1FFFFFFFFFFFFFFFLL;
    v25 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v24);
    *(_QWORD *)(v25 + v20) = v18;
    v26 = (__int64 *)a1[1];
    sub_141758A00(a1: v25, a2: *a1, a3: (char *)v19 - *a1);
    if ( v26 != v19 )
      sub_141758A00(a1: v25 + v20 + 8, a2: v19, a3: a1[1] - (_QWORD)v19);
    v27 = *a1;
    if ( *a1 == 0 )
    {
LABEL_39:
      *a1 = v25;
      a1[1] = v25 + 8 * v35;
      a1[2] = v25 + 8 * v24;
      v2 = v34;
      goto LABEL_19;
    }
    v28 = a1[2] - v27;
    if ( v28 == -1 )
    {
      v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_38:
        MEMORY[0x141948990](a1: v27 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_39;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_38;
    }
    v29 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28 )
    {
      v30 = *(_QWORD *)(v29 + 8 * v28);
      if ( v30 != 0 )
      {
        MEMORY[0x1419475D8](a1: v30 + 32, a2: v27 - *(unsigned int *)(v30 + 120));
        v31 = *(_BYTE *)(v30 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) != 0;
        if ( !v31 && *(_BYTE *)(v30 + 97) != 0 )
          sub_1412D33C0(a1: v30);
        goto LABEL_39;
      }
    }
    goto LABEL_38;
  }
  return *(_DWORD *)(*v2 + 16LL) == 0;
}
