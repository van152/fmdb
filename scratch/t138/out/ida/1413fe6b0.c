bool __fastcall sub_1413FE6B0(__int64 *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int16 v7; // ax
  __int64 v8; // rsi
  __int64 v9; // r15
  __int64 v10; // rbx
  __int64 v11; // r12
  __int64 v12; // rbp
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // r14
  bool v16; // al
  int v17; // r14d
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  _WORD *v21; // rbx
  __int64 v22; // rbp
  unsigned __int64 v23; // rax
  unsigned __int64 v24; // r15
  __int64 v25; // rsi
  _WORD *v26; // r12
  __int64 v27; // rbx
  unsigned __int64 v28; // rcx
  __int64 v29; // rbp
  __int64 v30; // rbp
  bool v31; // al
  _WORD v32[2]; // [rsp+28h] [rbp-50h] BYREF
  __int16 v33; // [rsp+2Ch] [rbp-4Ch] BYREF
  char v34; // [rsp+2Eh] [rbp-4Ah] BYREF
  char v35; // [rsp+2Fh] [rbp-49h] BYREF
  unsigned __int64 v36; // [rsp+30h] [rbp-48h]

  if ( *a1 != a1[1] )
    a1[1] = *a1;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v35, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v33 = 0;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v33, a3: 2);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v7 = v33;
  if ( v33 < 0 )
    return false;
  v8 = (unsigned __int16)v33;
  v9 = *a1;
  if ( (a1[2] - *a1) >> 1 < (unsigned __int64)(unsigned __int16)v33 )
  {
    v10 = a1[1];
    v11 = sub_1407E4490(a1: qword_141ABD470, a2: 2LL * (unsigned __int16)v33);
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
    a1[2] = v11 + 2 * v8;
    v7 = v33;
  }
  if ( v7 > 0 )
  {
    v17 = 0;
    while ( 1 )
    {
      v32[0] = 255;
      v18 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v34, a3: 1);
      if ( *(_DWORD *)(v18 + 16) != 0 )
        break;
      v19 = *a2;
      (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v32, a3: 1);
      if ( *(_DWORD *)(v19 + 16) != 0 )
        break;
      v20 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (char *)v32 + 1, a3: 1);
      if ( *(_DWORD *)(v20 + 16) != 0 || *(_DWORD *)(*a2 + 16LL) != 0 )
        break;
      v21 = (_WORD *)a1[1];
      if ( v21 == (_WORD *)a1[2] )
      {
        v22 = (__int64)v21 - *a1;
        v23 = v22 >> 1;
        v24 = (v22 >> 1) + ((unsigned __int64)(v22 >> 1) >> 1);
        v36 = (v22 >> 1) + 1;
        if ( v24 <= v36 )
          v24 = v23 + 1;
        if ( v23 > (((unsigned __int64)(v22 >> 1) >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
          v24 = 0x7FFFFFFFFFFFFFFFLL;
        v25 = sub_1407E4490(a1: qword_141ABD470, a2: 2 * v24);
        *(_WORD *)(v25 + v22) = v32[0];
        v26 = (_WORD *)a1[1];
        sub_141758A00(a1: v25, a2: *a1, a3: (char *)v21 - *a1);
        if ( v26 != v21 )
          sub_141758A00(a1: v25 + v22 + 2, a2: v21, a3: a1[1] - (_QWORD)v21);
        v27 = *a1;
        if ( *a1 != 0 )
        {
          v28 = a1[2] - v27;
          if ( v28 == -1 )
            v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v29 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28)
            && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v30 + 32, a2: v27 - *(unsigned int *)(v30 + 120));
            v31 = *(_BYTE *)(v30 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) != 0;
            if ( !v31 && *(_BYTE *)(v30 + 97) != 0 )
              sub_1412D33C0(a1: v30);
          }
          else
          {
            MEMORY[0x141948990](a1: v27 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *a1 = v25;
        a1[1] = v25 + 2 * v36;
        a1[2] = v25 + 2 * v24;
      }
      else
      {
        *v21 = v32[0];
        a1[1] += 2;
      }
      if ( (__int16)++v17 >= v33 )
        return *(_DWORD *)(*a2 + 16LL) == 0;
    }
    return false;
  }
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
