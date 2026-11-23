__int64 __fastcall sub_14083B2B0(__int64 *a1, _QWORD *a2)
{
  __int64 v4; // r13
  __int64 v5; // r12
  __int64 v6; // rbx
  __int64 v7; // rdi
  unsigned __int64 v8; // rcx
  __int64 v9; // r8
  __int64 v10; // r14
  bool v11; // al
  __int64 v12; // rbx
  __int64 v13; // rax
  __int64 v14; // rdi
  __int64 *v15; // rbx
  __int64 result; // rax
  __int64 v17; // rdi
  unsigned __int64 v18; // rax
  unsigned __int64 v19; // r12
  unsigned __int64 v20; // r15
  unsigned __int64 v21; // rdx
  unsigned __int64 v22; // r15
  __int64 v23; // r14
  __int64 *v24; // r13
  __int64 v25; // rdi
  unsigned __int64 v26; // rcx
  __int64 v27; // rbx
  __int64 v28; // rbx
  bool v29; // al
  __int64 v30; // [rsp+28h] [rbp-8h]

  v4 = *a1;
  if ( a1[2] == *a1 )
  {
    v5 = a1[1];
    v6 = sub_1407E4490(qword_141ABD470, 32);
    sub_141758A00();
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
  v12 = sub_140836BC0();
  v13 = MEMORY[0x1419475D0](v12 + 32);
  v14 = v13;
  if ( v13 != 0 && *(_BYTE *)(v12 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v12 + 64));
  if ( v13 == 0 )
    v14 = sub_1412D31C0(
            v12,
            *(unsigned int *)(v12 + 80),
            *(unsigned int *)(v12 + 4LL * (*(_DWORD *)(v12 + 56) != 0) + 84));
  if ( v14 != 0 && *(_BYTE *)(v12 + 96) != 0 )
    sub_141758A10(v14, 0, *(unsigned int *)(v12 + 80));
  v30 = v14;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 24LL))(*a2, a2, v14);
  v15 = (__int64 *)a1[1];
  if ( v15 != (__int64 *)a1[2] )
  {
    *v15 = v14;
    a1[1] += 8;
    return v14;
  }
  v17 = (__int64)v15 - *a1;
  v18 = v17 >> 3;
  v19 = (v17 >> 3) + 1;
  v20 = (unsigned __int64)(v17 >> 3) >> 1;
  v21 = 0x1FFFFFFFFFFFFFFFLL - v20;
  v22 = (v17 >> 3) + v20;
  if ( v22 <= v19 )
    v22 = v18 + 1;
  if ( v18 > v21 )
    v22 = 0x1FFFFFFFFFFFFFFFLL;
  v23 = sub_1407E4490(qword_141ABD470, 8 * v22);
  *(_QWORD *)(v23 + v17) = v30;
  v24 = (__int64 *)a1[1];
  sub_141758A00();
  if ( v24 != v15 )
    sub_141758A00();
  v25 = *a1;
  if ( *a1 != 0 )
  {
    v26 = a1[2] - v25;
    if ( v26 == -1 )
    {
      v26 = *(unsigned int *)(v25 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_38:
        MEMORY[0x141948990](v25 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_39;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_38;
    }
    v27 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v27) >> 3 > v26 )
    {
      v28 = *(_QWORD *)(v27 + 8 * v26);
      if ( v28 != 0 )
      {
        MEMORY[0x1419475D8](v28 + 32, v25 - *(unsigned int *)(v28 + 120));
        v29 = *(_BYTE *)(v28 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v28 + 64)) != 0;
        if ( !v29 && *(_BYTE *)(v28 + 97) != 0 )
          sub_1412D33C0(v28);
        goto LABEL_39;
      }
    }
    goto LABEL_38;
  }
LABEL_39:
  *a1 = v23;
  a1[1] = v23 + 8 * v19;
  result = v23 + 8 * v22;
  a1[2] = result;
  return result;
}
