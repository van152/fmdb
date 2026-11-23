_WORD *__fastcall sub_143C20010(__int64 a1, _WORD *a2, char a3)
{
  __int64 v4; // rax
  __int16 v6; // r13
  unsigned int v7; // ebx
  __int16 i; // r13
  __int16 v9; // cx
  __int16 v10; // dx
  unsigned __int16 v11; // si
  __int16 v12; // r8
  unsigned __int16 v13; // dx
  __int16 j; // ax
  __int16 v15; // dx
  __int16 v16; // bp
  __int64 v17; // rcx
  __int64 v18; // r14
  __int64 v19; // r9
  unsigned __int16 v20; // ax
  int v21; // eax
  _DWORD v23[18]; // [rsp+20h] [rbp-48h] BYREF

  v4 = *(_QWORD *)(a1 + 256);
  if ( v4 == 0 )
  {
    v21 = MEMORY[0x88];
    goto LABEL_36;
  }
  v6 = dword_141AAE084;
  v7 = HIWORD(dword_141AAE084);
  if ( a3 == 0 )
    goto LABEL_11;
  for ( i = dword_141AAE084 & 0x1FF; ; i += v9 )
  {
    v10 = 15;
    if ( 25
       * (unsigned __int16)((((18351 * (unsigned int)(unsigned __int16)v7) >> 16)
                           + ((unsigned __int16)(v7 - ((18351 * (unsigned int)(unsigned __int16)v7) >> 16)) >> 1)) >> 4) != (_WORD)v7 )
      v10 = 3;
    if ( ((unsigned __int16)v7 & (unsigned __int16)v10) != 0 )
      break;
    v9 = -366;
    if ( i < 366 )
      goto LABEL_10;
LABEL_5:
    LOWORD(v7) = v7 + 1;
  }
  v9 = -365;
  if ( i >= 365 )
    goto LABEL_5;
LABEL_10:
  v6 = (i + 1) & 0x1FF;
LABEL_11:
  v11 = *(_WORD *)(v4 + 138);
  v12 = *(_WORD *)(v4 + 136);
  v13 = v12 & 0x1FF;
  if ( (v11 < (unsigned __int16)v7 || v11 <= (unsigned __int16)v7 && v13 < (unsigned __int16)(v6 & 0x1FF))
    && v11 != 1900 )
  {
    for ( j = v13 + 363; ; j += v15 )
    {
      v16 = 15;
      if ( 25
         * (unsigned __int16)((((18351 * (unsigned int)v11) >> 16)
                             + ((unsigned __int16)(v11 - ((18351 * (unsigned int)v11) >> 16)) >> 1)) >> 4) != v11 )
        v16 = 3;
      if ( (v11 & (unsigned __int16)v16) != 0 )
      {
        v15 = -365;
        if ( j < 365 )
        {
LABEL_22:
          a2[1] = v11;
          *a2 = (j + 1) & 0x1FF | v12 & 0xFE00;
          return a2;
        }
      }
      else
      {
        v15 = -366;
        if ( j < 366 )
          goto LABEL_22;
      }
      ++v11;
    }
  }
  v17 = *(_QWORD *)(a1 + 216);
  if ( v17 != 0 )
  {
    if ( *(_BYTE *)(a1 + 185) == 0 || (v18 = *(_QWORD *)(v17 + 272)) == 0 )
      v18 = *(_QWORD *)(v17 + 264);
    if ( v13 == 1 && v11 == 1900 && v18 != 0 )
    {
      sub_141072830(v18, a2, a1, 0);
      v20 = a2[1];
      if ( v20 < (unsigned __int16)v7
        || v20 <= (unsigned __int16)v7 && (unsigned __int16)(*a2 & 0x1FF) < (unsigned __int16)(v6 & 0x1FF) )
      {
        LOBYTE(v19) = 1;
        sub_141072830(v18, v23, a1, v19);
        v21 = v23[0];
LABEL_36:
        *(_DWORD *)a2 = v21;
      }
      return a2;
    }
  }
  v21 = *(_DWORD *)(v4 + 136);
  goto LABEL_36;
}
