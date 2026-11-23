__int64 __fastcall sub_14424C720(__int64 a1, __int64 a2, __int16 *a3, __int16 a4)
{
  int v6; // r8d
  __int16 v7; // r9
  __int64 v8; // rax
  __int16 v9; // si
  __int64 v10; // rdx
  __int16 v11; // cx
  unsigned __int16 v12; // dx
  __int16 v13; // r8
  __int16 i; // ax
  __int16 v15; // cx
  __int16 v16; // si
  __int16 v17; // ax
  __int16 v18; // cx
  __int16 v19; // di
  __int16 v20; // ax
  __int16 v21; // ax
  unsigned __int16 v22; // dx
  int v23; // edi
  int v24; // ebx

  v6 = *(unsigned __int16 *)(a1 + 2);
  if ( (_WORD)v6 != 0 )
  {
    v7 = *(char *)(a1 + 5) + a4;
    v8 = *(unsigned __int8 *)(a1 + 4);
    if ( (__int16)v6 <= 30 && (v8 != 2 || (__int16)v6 < 29) )
    {
LABEL_34:
      *(_DWORD *)a2 = 0;
      sub_140051D30(a2, 0, v6, v8, v7, 0);
      return a2;
    }
    LOWORD(a1) = 31;
    if ( (unsigned __int8)(v8 - 13) >= 0xF4u )
    {
      v9 = 3;
      if ( (unsigned __int16)(23593 * v7) < 0xA3Eu )
        v9 = 15;
      if ( ((unsigned __int16)v7 & (unsigned __int16)v9) != 0 )
      {
        if ( (_BYTE)v8 == 12 )
          goto LABEL_32;
        v10 = 0x14175C880LL;
      }
      else
      {
        if ( (_BYTE)v8 == 12 )
          goto LABEL_32;
        v10 = 0x14175C860LL;
      }
      LODWORD(a1) = *(unsigned __int16 *)(v10 + 2 * v8);
      LOWORD(a1) = a1 - *(_WORD *)(v10 + 2 * v8 - 2);
    }
LABEL_32:
    if ( (__int16)a1 < (__int16)v6 )
      v6 = a1;
    goto LABEL_34;
  }
  v11 = *(_WORD *)a1;
  if ( v11 >= 0 )
  {
    v12 = a3[1];
    v13 = *a3;
    for ( i = v11 + (*a3 & 0x1FF) - 1; ; i += v15 )
    {
      v16 = 15;
      if ( 25
         * (unsigned __int16)((((18351 * (unsigned int)v12) >> 16)
                             + ((unsigned __int16)(v12 - ((18351 * (unsigned int)v12) >> 16)) >> 1)) >> 4) != v12 )
        v16 = 3;
      if ( (v12 & (unsigned __int16)v16) != 0 )
      {
        v15 = -365;
        if ( i < 365 )
        {
LABEL_18:
          v17 = (i + 1) & 0x1FF;
          goto LABEL_28;
        }
      }
      else
      {
        v15 = -366;
        if ( i < 366 )
          goto LABEL_18;
      }
      ++v12;
    }
  }
  v18 = v11 - 1;
  v13 = *a3;
  v19 = *a3 & 0x1FF;
  v12 = a3[1];
  v20 = 0x8000;
  if ( v18 < 0 )
    v20 = v18;
  v21 = v19 + v20;
  if ( v21 < 0 )
  {
    v22 = v12 - 1;
    do
    {
      v23 = v22;
      v24 = 3;
      if ( 25
         * (unsigned __int16)((((18351 * (unsigned int)v22) >> 16)
                             + ((unsigned __int16)(v22 - ((18351 * (unsigned int)v22) >> 16)) >> 1)) >> 4) == v22 )
        v24 = 15;
      --v22;
      v21 += ((v23 & v24) == 0) + 365;
    }
    while ( v21 < 0 );
    v12 = v22 + 1;
  }
  v17 = v21 + 1;
LABEL_28:
  *(_WORD *)(a2 + 2) = v12;
  *(_WORD *)a2 = v13 & 0xFE00 | v17;
  return a2;
}
