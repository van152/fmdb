__int64 __fastcall sub_14083B5F0(__int64 *a1, __int64 *a2)
{
  __int64 v4; // rdi
  __int64 v5; // r13
  __int64 v6; // rbx
  __int64 v7; // rsi
  unsigned __int64 v8; // rcx
  __int64 v9; // r8
  __int64 v10; // r12
  bool v11; // al
  __int64 v12; // rdi
  __int64 v13; // rax
  _QWORD *v14; // rbx
  __int64 v15; // rax
  __int64 v16; // rcx
  __int64 result; // rax
  _QWORD *v18; // rdi
  __int64 v19; // rsi
  unsigned __int64 v20; // rax
  unsigned __int64 v21; // r13
  unsigned __int64 v22; // r12
  unsigned __int64 v23; // rdx
  unsigned __int64 v24; // r12
  __int64 v25; // r14
  _QWORD *v26; // rbx
  __int64 v27; // rdi
  unsigned __int64 v28; // rcx
  __int64 v29; // rbx
  __int64 v30; // rsi
  bool v31; // al

  v4 = *a1;
  if ( a1[2] == *a1 )
  {
    v5 = a1[1];
    v6 = sub_1407E4490(qword_141ABD470, 32);
    sub_141758A00(v6, *a1, a1[1] - *a1);
    v7 = *a1;
    if ( *a1 == 0 )
    {
LABEL_12:
      *a1 = v6;
      a1[1] = v6 + v5 - v4;
      a1[2] = v6 + 32;
      goto LABEL_13;
    }
    v8 = a1[2] - v7;
    if ( v8 == -1 )
    {
      v8 = *(unsigned int *)(v7 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_11:
        MEMORY[0x141948990](v7 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_12;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_11;
    }
    v9 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v9) >> 3 > v8 )
    {
      v10 = *(_QWORD *)(v9 + 8 * v8);
      if ( v10 != 0 )
      {
        MEMORY[0x1419475D8](v10 + 32, v7 - *(unsigned int *)(v10 + 120));
        v11 = *(_BYTE *)(v10 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v10 + 64)) != 0;
        if ( !v11 && *(_BYTE *)(v10 + 97) != 0 )
          sub_1412D33C0(v10);
        goto LABEL_12;
      }
    }
    goto LABEL_11;
  }
LABEL_13:
  v12 = sub_140836BC0(a1);
  v13 = MEMORY[0x1419475D0](v12 + 32);
  v14 = (_QWORD *)v13;
  if ( v13 != 0 && *(_BYTE *)(v12 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v12 + 64));
  if ( v13 == 0 )
    v14 = (_QWORD *)sub_1412D31C0(
                      v12,
                      *(unsigned int *)(v12 + 80),
                      *(unsigned int *)(v12 + 4LL * (*(_DWORD *)(v12 + 56) != 0) + 84));
  if ( v14 != nullptr && *(_BYTE *)(v12 + 96) != 0 )
    sub_141758A10(v14, 0, *(unsigned int *)(v12 + 80));
  v15 = *a2;
  v16 = a2[1];
  v14[1] = v16;
  *v14 = v15;
  result = sub_14083D4F0(v16) + 8;
  a2[1] = 0;
  *a2 = result;
  v18 = (_QWORD *)a1[1];
  if ( v18 != (_QWORD *)a1[2] )
  {
    *v18 = v14;
    a1[1] += 8;
    return result;
  }
  v19 = (__int64)v18 - *a1;
  v20 = v19 >> 3;
  v21 = (v19 >> 3) + 1;
  v22 = (unsigned __int64)(v19 >> 3) >> 1;
  v23 = 0x1FFFFFFFFFFFFFFFLL - v22;
  v24 = (v19 >> 3) + v22;
  if ( v24 <= v21 )
    v24 = v20 + 1;
  if ( v20 > v23 )
    v24 = 0x1FFFFFFFFFFFFFFFLL;
  v25 = sub_1407E4490(qword_141ABD470, 8 * v24);
  *(_QWORD *)(v25 + v19) = v14;
  v26 = (_QWORD *)a1[1];
  sub_141758A00(v25, *a1, (char *)v18 - *a1);
  if ( v26 != v18 )
    sub_141758A00(v25 + v19 + 8, v18, a1[1] - (_QWORD)v18);
  v27 = *a1;
  if ( *a1 != 0 )
  {
    v28 = a1[2] - v27;
    if ( v28 == -1 )
    {
      v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_38:
        MEMORY[0x141948990](v27 - *(unsigned int *)(qword_141ABD470 + 48));
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
        MEMORY[0x1419475D8](v30 + 32, v27 - *(unsigned int *)(v30 + 120));
        v31 = *(_BYTE *)(v30 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) != 0;
        if ( !v31 && *(_BYTE *)(v30 + 97) != 0 )
          sub_1412D33C0(v30);
        goto LABEL_39;
      }
    }
    goto LABEL_38;
  }
LABEL_39:
  *a1 = v25;
  a1[1] = v25 + 8 * v21;
  result = v25 + 8 * v24;
  a1[2] = result;
  return result;
}
