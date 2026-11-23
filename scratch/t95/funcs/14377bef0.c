_QWORD *__fastcall sub_14377BEF0(_QWORD *a1, _QWORD *a2)
{
  _QWORD *v2; // rbx
  _QWORD *v4; // r14
  _QWORD *v5; // rdi
  void (__fastcall *v6)(__int64, _QWORD *); // r13
  _QWORD *v7; // r15
  _QWORD *v8; // rsi
  __int64 v9; // rcx
  __int64 v10; // rbx
  __int64 v11; // rsi
  _QWORD *v12; // rsi
  unsigned __int64 v13; // rcx
  __int64 v14; // rdi
  __int64 v15; // rdi

  v2 = a2;
  v4 = (_QWORD *)*a1;
  v5 = (_QWORD *)a1[1];
  if ( (_QWORD *)*a1 != v5 )
  {
    v6 = (void (__fastcall *)(__int64, _QWORD *))MEMORY[0x1419475D8];
    v7 = (_QWORD *)*a1;
    do
    {
      v8 = (_QWORD *)*v7;
      if ( *v7 != 0 )
      {
        (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v8 + 16LL))(*v8, *v7);
        v10 = sub_140836BC0(v9);
        v6(v10 + 32, v8);
        if ( (*(_BYTE *)(v10 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v10 + 64)) == 0)
          && *(_BYTE *)(v10 + 97) != 0 )
        {
          sub_1412D33C0(v10);
        }
      }
      ++v7;
    }
    while ( v7 != v5 );
    v11 = a1[1] - (_QWORD)v5;
    sub_141758A00();
    a1[1] = (char *)v4 + v11;
    v2 = a2;
  }
  if ( a1 != v2 )
  {
    v12 = (_QWORD *)*a1;
    if ( *a1 == 0 )
    {
LABEL_23:
      *a1 = *v2;
      a1[1] = v2[1];
      a1[2] = v2[2];
      v2[2] = 0;
      v2[1] = 0;
      *v2 = 0;
      return a1;
    }
    v13 = a1[2] - (_QWORD)v12;
    if ( v13 == -1 )
    {
      v13 = *(unsigned int *)((char *)v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_21;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_21;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13 )
    {
      v15 = *(_QWORD *)(v14 + 8 * v13);
      if ( v15 != 0 )
      {
        MEMORY[0x1419475D8](v15 + 32, (char *)v12 - *(unsigned int *)(v15 + 120));
        if ( (*(_BYTE *)(v15 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) == 0)
          && *(_BYTE *)(v15 + 97) != 0 )
        {
          sub_1412D33C0(v15);
        }
        goto LABEL_22;
      }
    }
LABEL_21:
    MEMORY[0x141948990]((char *)v12 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_22:
    a1[2] = 0;
    a1[1] = 0;
    *a1 = 0;
    goto LABEL_23;
  }
  return a1;
}
