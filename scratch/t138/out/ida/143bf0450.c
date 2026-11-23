__int64 __fastcall sub_143BF0450(_QWORD *a1, __int64 a2)
{
  _QWORD *v2; // r14
  __int64 v3; // rcx
  _QWORD *v4; // rbx
  _QWORD *v5; // rdi
  _QWORD *v6; // rsi
  __int64 v7; // rsi
  unsigned __int64 v8; // rcx
  __int64 v9; // rdx
  __int64 v10; // rbx
  __int64 v11; // rdi
  unsigned __int64 v12; // rcx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 result; // rax

  v2 = (_QWORD *)*a1;
  *a1 = a2;
  if ( v2 != nullptr )
  {
    v3 = v2[13];
    if ( v3 != 0 )
      sub_141750CFC(a1: v3);
    v4 = (_QWORD *)v2[7];
    v5 = (_QWORD *)v2[8];
    if ( v4 != v5 )
    {
      v6 = (_QWORD *)v2[7];
      do
      {
        if ( *v6 != 0 )
          sub_140E409B0();
        ++v6;
      }
      while ( v6 != v5 );
      v7 = v2[8] - (_QWORD)v5;
      sub_141758A00(a1: v4, a2: v5, a3: v7);
      v2[8] = (char *)v4 + v7;
      v5 = (_QWORD *)v2[7];
    }
    if ( v5 != nullptr )
    {
      v8 = v2[9] - (_QWORD)v5;
      if ( v8 == -1 )
        v8 = *(unsigned int *)((char *)v5 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v9 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v9) >> 3 > v8)
        && (v10 = *(_QWORD *)(v9 + 8 * v8)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v10 + 32, a2: (char *)v5 - *(unsigned int *)(v10 + 120));
        if ( (*(_BYTE *)(v10 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v10 + 64)) == 0)
          && *(_BYTE *)(v10 + 97) != 0 )
        {
          sub_1412D33C0(a1: v10);
        }
      }
      else
      {
        MEMORY[0x141948990](a1: (char *)v5 - *(unsigned int *)(qword_141ABD470 + 48));
      }
      v2[9] = 0;
      v2[8] = 0;
      v2[7] = 0;
    }
    v11 = v2[4];
    if ( v11 != 0 )
    {
      v12 = v2[6] - v11;
      if ( v12 == -1 )
        v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v13 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12)
        && (v14 = *(_QWORD *)(v13 + 8 * v12)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
        if ( (*(_BYTE *)(v14 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) == 0)
          && *(_BYTE *)(v14 + 97) != 0 )
        {
          sub_1412D33C0(a1: v14);
        }
      }
      else
      {
        MEMORY[0x141948990](a1: v11 - *(unsigned int *)(qword_141ABD470 + 48));
      }
      v2[6] = 0;
      v2[5] = 0;
      v2[4] = 0;
    }
    return sub_140E40840(a1: v2);
  }
  return result;
}
