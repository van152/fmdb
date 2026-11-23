// THUNK ALIAS -> sub_143F01920 (jmp:0x14106bd10->0x143f01920)
__int64 __fastcall sub_143F01920(__int64 a1, char a2)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  char v6; // al
  __int64 v7; // rdx
  __int64 v8; // rcx
  char v9; // al
  unsigned __int64 v10; // rcx
  __int64 v11; // rbx
  __int64 v12; // rdi
  _QWORD *v13; // rcx
  __int64 v14; // rdx
  __int64 v15; // rax
  unsigned __int64 v16; // rax
  __int64 v17; // rbx
  __int64 v18; // rsi
  int v19; // r8d
  __int64 v20; // rdi
  __int64 result; // rax
  unsigned int v22; // ebp
  __int64 **v23; // rax
  __int64 *v24; // rcx
  __int64 *v25; // rdx
  __int64 v26; // rsi
  int v27; // ebx
  __int64 v28; // rdi
  unsigned int v29; // ebp

  if ( (_BYTE)word_141B60320 == 0 )
  {
LABEL_29:
    v23 = *(__int64 ***)(qword_141B5FDC0 + 128);
    v24 = *v23;
    v25 = v23[1];
    if ( *v23 == v25 )
      return 0;
    v26 = *(_QWORD *)(a1 + 368);
    result = 0;
    v27 = 16387;
    do
    {
      v28 = *v24;
      if ( *(_QWORD *)(*v24 + 96) == v26 && v26 != 0 )
      {
        v29 = *(unsigned __int8 *)(v28 + 244);
        if ( v29 <= 0xE
          && _bittest(&v27, v29)
          && *(_BYTE *)(v28 + 418) == a2
          && *(_QWORD *)(v28 + 104) == 0
          && (result == 0 || *(_WORD *)(v28 + 384) > *(_WORD *)(result + 384)) )
        {
          result = *v24;
        }
      }
      ++v24;
    }
    while ( v24 != v25 );
    return result;
  }
  v4 = *(_QWORD *)(a1 + 368);
  v5 = *(_QWORD *)(v4 + 288);
  if ( v5 != 0 )
  {
    if ( *(_BYTE *)(a1 + 185) == 0 )
    {
LABEL_15:
      v13 = (_QWORD *)(v5 + 88);
      goto LABEL_16;
    }
    if ( *(_QWORD *)(v5 + 624) != 0 )
      goto LABEL_13;
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
    goto LABEL_29;
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
      goto LABEL_29;
  }
  if ( *(_BYTE *)(a1 + 185) == 0 )
    goto LABEL_15;
LABEL_13:
  v13 = *(_QWORD **)(v5 + 624);
  if ( v13 == nullptr )
    goto LABEL_29;
LABEL_16:
  v14 = v13[1];
  v15 = v13[2] - v14;
  if ( v15 == 0 )
    goto LABEL_29;
  v16 = v15 >> 3;
  v17 = 1;
  if ( v16 >= 2 )
    v17 = v16;
  v18 = 0;
  v19 = 16387;
  while ( 1 )
  {
    v20 = *(_QWORD *)(v14 + 8 * v18);
    if ( v20 != 0 )
    {
      result = *(_QWORD *)(v20 + 288);
      if ( result != 0 && *(_QWORD *)(result + 96) != 0 )
      {
        v22 = *(unsigned __int8 *)(v20 + 572);
        if ( v22 <= 0xE && _bittest(&v19, v22) && *(_BYTE *)(v20 + 841) == a2 )
          return result;
      }
    }
    if ( v17 == ++v18 )
    {
      if ( *(_QWORD *)(*v13 + 24LL) == *(_QWORD *)(a1 + 368) )
        return 0;
      goto LABEL_29;
    }
  }
}
