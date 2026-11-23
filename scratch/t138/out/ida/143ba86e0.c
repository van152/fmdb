__int64 __fastcall sub_143BA86E0(_QWORD *a1)
{
  _QWORD *v1; // r14
  __int64 v2; // rcx
  _QWORD *v3; // rbx
  _QWORD *v4; // rdi
  _QWORD *v5; // rsi
  __int64 v6; // rsi
  unsigned __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // rbx
  __int64 v10; // rdi
  unsigned __int64 v11; // rcx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 result; // rax

  v1 = (_QWORD *)*a1;
  if ( *a1 != 0 )
  {
    v2 = v1[13];
    if ( v2 != 0 )
      sub_141750CFC(a1: v2);
    v3 = (_QWORD *)v1[7];
    v4 = (_QWORD *)v1[8];
    if ( v3 != v4 )
    {
      v5 = (_QWORD *)v1[7];
      do
      {
        if ( *v5 != 0 )
          sub_140E409B0();
        ++v5;
      }
      while ( v5 != v4 );
      v6 = v1[8] - (_QWORD)v4;
      sub_141758A00(a1: v3, a2: v4, a3: v6);
      v1[8] = (char *)v3 + v6;
      v4 = (_QWORD *)v1[7];
    }
    if ( v4 != nullptr )
    {
      v7 = v1[9] - (_QWORD)v4;
      if ( v7 == -1 )
        v7 = *(unsigned int *)((char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v8 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v8) >> 3 > v7)
        && (v9 = *(_QWORD *)(v8 + 8 * v7)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v9 + 32, a2: (char *)v4 - *(unsigned int *)(v9 + 120));
        if ( (*(_BYTE *)(v9 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v9 + 64)) == 0)
          && *(_BYTE *)(v9 + 97) != 0 )
        {
          sub_1412D33C0(a1: v9);
        }
      }
      else
      {
        MEMORY[0x141948990](a1: (char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
      }
      v1[9] = 0;
      v1[8] = 0;
      v1[7] = 0;
    }
    v10 = v1[4];
    if ( v10 != 0 )
    {
      v11 = v1[6] - v10;
      if ( v11 == -1 )
        v11 = *(unsigned int *)(v10 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v12 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v12) >> 3 > v11)
        && (v13 = *(_QWORD *)(v12 + 8 * v11)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v13 + 32, a2: v10 - *(unsigned int *)(v13 + 120));
        if ( (*(_BYTE *)(v13 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v13 + 64)) == 0)
          && *(_BYTE *)(v13 + 97) != 0 )
        {
          sub_1412D33C0(a1: v13);
        }
      }
      else
      {
        MEMORY[0x141948990](a1: v10 - *(unsigned int *)(qword_141ABD470 + 48));
      }
      v1[6] = 0;
      v1[5] = 0;
      v1[4] = 0;
    }
    return sub_140E40840(a1: v1);
  }
  return result;
}
