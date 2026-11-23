void __fastcall sub_14377A980(_QWORD *a1)
{
  _QWORD *v2; // r14
  _QWORD *v3; // r13
  void (__fastcall *v4)(__int64, _QWORD *); // r12
  _QWORD *v5; // rdi
  _QWORD *v6; // rsi
  __int64 v7; // rcx
  __int64 v8; // rbx
  __int64 v9; // rsi
  unsigned __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 v12; // rbx

  v2 = (_QWORD *)*a1;
  v3 = (_QWORD *)a1[1];
  if ( (_QWORD *)*a1 != v3 )
  {
    v4 = (void (__fastcall *)(__int64, _QWORD *))MEMORY[0x1419475D8];
    v5 = (_QWORD *)*a1;
    do
    {
      v6 = (_QWORD *)*v5;
      if ( *v5 != 0 )
      {
        (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v6 + 16LL))(a1: *v6, a2: *v5);
        v8 = sub_140836BC0(a1: v7);
        v4(a1: v8 + 32, a2: v6);
        if ( (*(_BYTE *)(v8 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v8 + 64)) == 0)
          && *(_BYTE *)(v8 + 97) != 0 )
        {
          sub_1412D33C0(a1: v8);
        }
      }
      ++v5;
    }
    while ( v5 != v3 );
    v9 = a1[1] - (_QWORD)v3;
    sub_141758A00(a1: v2, a2: v3, a3: v9);
    a1[1] = (char *)v2 + v9;
    v3 = (_QWORD *)*a1;
  }
  if ( v3 != nullptr )
  {
    v10 = a1[2] - (_QWORD)v3;
    if ( v10 == -1 )
    {
      v10 = *(unsigned int *)((char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_20;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_20;
    }
    v11 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v11) >> 3 > v10 )
    {
      v12 = *(_QWORD *)(v11 + 8 * v10);
      if ( v12 != 0 )
      {
        MEMORY[0x1419475D8](a1: v12 + 32, a2: (char *)v3 - *(unsigned int *)(v12 + 120));
        if ( (*(_BYTE *)(v12 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v12 + 64)) == 0)
          && *(_BYTE *)(v12 + 97) != 0 )
        {
          sub_1412D33C0(a1: v12);
        }
        goto LABEL_21;
      }
    }
LABEL_20:
    MEMORY[0x141948990](a1: (char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_21:
    a1[2] = 0;
    a1[1] = 0;
    *a1 = 0;
  }
}
