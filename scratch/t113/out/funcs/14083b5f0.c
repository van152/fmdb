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
  __int64 v14; // rdx
  _QWORD *v15; // rbx
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 result; // rax
  _QWORD *v19; // rdi
  __int64 v20; // rsi
  unsigned __int64 v21; // rax
  unsigned __int64 v22; // r13
  unsigned __int64 v23; // r12
  unsigned __int64 v24; // rdx
  unsigned __int64 v25; // r12
  __int64 v26; // r14
  _QWORD *v27; // rbx
  __int64 v28; // rdi
  unsigned __int64 v29; // rcx
  __int64 v30; // rbx
  __int64 v31; // rsi
  bool v32; // al

  v4 = *a1;
  if ( a1[2] == *a1 )
  {
    v5 = a1[1];
    v6 = sub_1407E4490(qword_141ABD470);
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
  v15 = (_QWORD *)v13;
  if ( v13 != 0 && *(_BYTE *)(v12 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v12 + 64));
  if ( v13 == 0 )
    v15 = (_QWORD *)sub_1412D31C0(
                      v12,
                      *(unsigned int *)(v12 + 80),
                      *(unsigned int *)(v12 + 4LL * (*(_DWORD *)(v12 + 56) != 0) + 84));
  if ( v15 != nullptr && *(_BYTE *)(v12 + 96) != 0 )
    sub_141758A10(v15, 0, *(unsigned int *)(v12 + 80));
  v16 = *a2;
  v17 = a2[1];
  v15[1] = v17;
  *v15 = v16;
  result = sub_14083D4F0(v17, v14) + 8;
  a2[1] = 0;
  *a2 = result;
  v19 = (_QWORD *)a1[1];
  if ( v19 != (_QWORD *)a1[2] )
  {
    *v19 = v15;
    a1[1] += 8;
    return result;
  }
  v20 = (__int64)v19 - *a1;
  v21 = v20 >> 3;
  v22 = (v20 >> 3) + 1;
  v23 = (unsigned __int64)(v20 >> 3) >> 1;
  v24 = 0x1FFFFFFFFFFFFFFFLL - v23;
  v25 = (v20 >> 3) + v23;
  if ( v25 <= v22 )
    v25 = v21 + 1;
  if ( v21 > v24 )
    v25 = 0x1FFFFFFFFFFFFFFFLL;
  v26 = sub_1407E4490(qword_141ABD470);
  *(_QWORD *)(v26 + v20) = v15;
  v27 = (_QWORD *)a1[1];
  sub_141758A00(v26, *a1, (char *)v19 - *a1);
  if ( v27 != v19 )
    sub_141758A00(v26 + v20 + 8, v19, a1[1] - (_QWORD)v19);
  v28 = *a1;
  if ( *a1 != 0 )
  {
    v29 = a1[2] - v28;
    if ( v29 == -1 )
    {
      v29 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_38:
        MEMORY[0x141948990](v28 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_39;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_38;
    }
    v30 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 > v29 )
    {
      v31 = *(_QWORD *)(v30 + 8 * v29);
      if ( v31 != 0 )
      {
        MEMORY[0x1419475D8](v31 + 32, v28 - *(unsigned int *)(v31 + 120));
        v32 = *(_BYTE *)(v31 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) != 0;
        if ( !v32 && *(_BYTE *)(v31 + 97) != 0 )
          sub_1412D33C0(v31);
        goto LABEL_39;
      }
    }
    goto LABEL_38;
  }
LABEL_39:
  *a1 = v26;
  a1[1] = v26 + 8 * v22;
  result = v26 + 8 * v25;
  a1[2] = result;
  return result;
}
