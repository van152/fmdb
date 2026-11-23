_DWORD *__fastcall sub_143EE0430(_DWORD *a1, _QWORD *a2, __int64 *a3)
{
  unsigned int v6; // esi
  __int64 v7; // r13
  __int64 v8; // r12
  __int64 v9; // rsi
  __int64 v10; // r15
  __int64 v11; // rbp
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // rcx
  __int64 v15; // rbp
  __int64 v16; // rcx
  bool v17; // al
  __int64 v18; // rbp
  unsigned int v20; // [rsp+2Ch] [rbp-5Ch] BYREF
  __int64 v21; // [rsp+30h] [rbp-58h]
  __int64 v22; // [rsp+38h] [rbp-50h] BYREF
  int v23; // [rsp+40h] [rbp-48h]
  char v24; // [rsp+44h] [rbp-44h]

  v20 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v20, 4);
  v6 = v20;
  if ( qword_141AA7808 <= (unsigned __int64)v20 )
  {
LABEL_20:
    *a1 = 1;
    return a1;
  }
  v7 = *a3;
  if ( (a3[2] - *a3) >> 4 < (unsigned __int64)v20 )
  {
    v8 = a3[1];
    v9 = 16LL * v20;
    v10 = sub_1407E4490(qword_141ABD470, v9);
    sub_141758A00();
    v11 = *a3;
    if ( *a3 == 0 )
    {
LABEL_13:
      *a3 = v10;
      a3[1] = v10 + v8 - v7;
      a3[2] = v10 + v9;
      v6 = v20;
      goto LABEL_14;
    }
    v12 = a3[2] - v11;
    if ( v12 == -1 )
    {
      v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](v11 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v13 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12 )
    {
      v14 = *(_QWORD *)(v13 + 8 * v12);
      if ( v14 != 0 )
      {
        v15 = v11 - *(unsigned int *)(v14 + 120);
        v21 = v14;
        MEMORY[0x1419475D8](v14 + 32, v15);
        v16 = v21;
        v17 = *(_BYTE *)(v21 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 + 64)) != 0;
        if ( !v17 && *(_BYTE *)(v16 + 97) != 0 )
          sub_1412D33C0(v16);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_14:
  if ( v6 != 0 )
  {
    v18 = 0;
    while ( 1 )
    {
      v22 = 0;
      v23 = 16777471;
      v24 = 0;
      if ( (unsigned __int8)sub_141072F60(&v22, a2) == 0 )
        goto LABEL_20;
      if ( *(_DWORD *)(*a2 + 16LL) == 0 )
      {
        sub_1408C9770(a3, &v22);
        if ( ++v18 < (unsigned __int64)v20 )
          continue;
      }
      break;
    }
  }
  *a1 = *(_DWORD *)(*a2 + 16LL);
  return a1;
}
