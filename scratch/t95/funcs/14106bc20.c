// THUNK ALIAS -> sub_143F01630 (jmp:0x14106bc20->0x143f01630)
__int64 __fastcall sub_143F01630(__int64 a1, unsigned int a2)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  char v6; // al
  __int64 v7; // rdx
  __int64 v8; // rcx
  char v9; // al
  unsigned __int64 v10; // rcx
  __int64 v11; // rsi
  __int64 v12; // rbx
  __int64 v13; // rcx

  if ( (_BYTE)word_141B60320 == 0 )
    return 0;
  v4 = *(_QWORD *)(a1 + 368);
  v5 = *(_QWORD *)(v4 + 288);
  if ( v5 != 0 )
  {
    if ( *(_BYTE *)(a1 + 185) == 0 )
      goto LABEL_15;
    if ( *(_QWORD *)(v5 + 624) != 0 )
    {
LABEL_13:
      v13 = *(_QWORD *)(v5 + 624);
      if ( v13 == 0 )
        return 0;
      return sub_1408D2E00(v13, a2);
    }
  }
  v6 = sub_1409A33A0(
         *(_QWORD *)(*(_QWORD *)(v4 + 264) + 368LL),
         *(unsigned __int8 *)(*(_QWORD *)(v4 + 264) + 185LL),
         0,
         0,
         0);
  v7 = *(_QWORD *)(qword_141B5AD60 + 16);
  v8 = *(_QWORD *)(qword_141B5AD60 + 24) - v7;
  if ( v8 == 0 )
    return 0;
  v9 = v6 ^ 0xB;
  v10 = v8 >> 3;
  v11 = 1;
  if ( v10 >= 2 )
    v11 = v10;
  v12 = 0;
  while ( 1 )
  {
    v5 = *(_QWORD *)(v7 + 8 * v12);
    if ( *(_BYTE *)(v5 + 69) == v9 )
      break;
    if ( v11 == ++v12 )
      return 0;
  }
  if ( *(_BYTE *)(a1 + 185) != 0 )
    goto LABEL_13;
LABEL_15:
  v13 = v5 + 88;
  return sub_1408D2E00(v13, a2);
}
