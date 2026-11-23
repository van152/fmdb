// THUNK ALIAS -> sub_143C54BD0 (jmp:0x140e82ef0->0x143c54bd0)
__int64 __fastcall sub_143C54BD0(__int64 a1, unsigned int *a2)
{
  __int64 result; // rax
  __int64 v3; // rcx
  int v4; // r9d
  int v5; // ecx
  __int64 v6; // r8
  unsigned int v7; // r11d
  unsigned __int16 v8; // r10
  int i; // r8d
  __int16 v10; // cx
  int v11; // edi
  int v12; // eax
  unsigned int v13; // edi
  int v14; // ecx
  __int16 v15; // ax
  __int16 v16; // r11
  int v17; // eax
  int j; // r10d
  __int16 v19; // cx
  int v20; // eax
  int v21; // esi
  unsigned int v22; // eax
  int v23; // ecx
  __int16 v24; // cx
  int v25; // eax
  unsigned int v26; // eax
  int v27; // ecx
  unsigned __int16 v28; // r10
  __int16 v29; // si
  __int16 v30; // r10
  unsigned __int16 v31; // cx
  int v32; // eax

  result = *(_QWORD *)(a1 + 256);
  if ( ((*(_BYTE *)(result + 297) - 3) & 0xFB) == 0 )
  {
    if ( *(_WORD *)(result + 186) == 1900 && (*(_WORD *)(result + 184) & 0x1FF) == 1 )
    {
      v3 = 0x1418761ECLL;
    }
    else
    {
      v3 = 0x1418761ECLL;
      if ( *(_BYTE *)(result + 293) == 0 )
        v3 = result + 184;
    }
    v4 = *(_DWORD *)v3;
    v5 = HIWORD(*(_DWORD *)v3);
    v6 = *(_QWORD *)(result + 120);
    if ( v6 == 0 )
    {
      for ( i = (v4 & 0x1FF) + 1463; ; i = v11 )
      {
        v12 = (unsigned __int16)v5;
        v13 = 25
            * ((((18351 * (unsigned int)(unsigned __int16)v5) >> 16)
              + ((unsigned __int16)(v5 - ((18351 * (unsigned int)(unsigned __int16)v5) >> 16)) >> 1)) >> 4);
        v14 = 15;
        if ( (_WORD)v12 != (_WORD)v13 )
          v14 = 3;
        if ( (v12 & v14) != 0 )
        {
          v10 = -365;
          if ( (__int16)i < 365 )
          {
LABEL_19:
            result = (unsigned int)(v12 << 16);
            *a2 = result | ((_WORD)i + 1) & 0x1FF | v4 & 0xFE00;
            return result;
          }
        }
        else
        {
          v10 = -366;
          if ( (__int16)i < 366 )
            goto LABEL_19;
        }
        v11 = i + v10;
        LOWORD(v5) = v12 + 1;
      }
    }
    v7 = *(_DWORD *)(v6 + 12);
    result = HIWORD(v7);
    if ( (unsigned __int16)v5 >= HIWORD(v7)
      && ((v8 = v4 & 0x1FF, (unsigned __int16)v5 > HIWORD(v7)) || (unsigned __int16)(result = v7 & 0x1FF) <= v8) )
    {
      v15 = *(unsigned __int8 *)(v6 + 18);
      if ( (char)v15 <= 0 )
      {
        for ( j = v8 + 1463; ; j = v25 )
        {
          v21 = (unsigned __int16)v5;
          v26 = 25
              * ((((18351 * (unsigned int)(unsigned __int16)v5) >> 16)
                + ((unsigned __int16)(v5 - ((18351 * (unsigned int)(unsigned __int16)v5) >> 16)) >> 1)) >> 4);
          v27 = 15;
          if ( (_WORD)v21 != (_WORD)v26 )
            v27 = 3;
          if ( (v21 & v27) != 0 )
          {
            v24 = -365;
            if ( (__int16)j < 365 )
            {
LABEL_37:
              v28 = (j + 1) & 0x1FF;
              goto LABEL_45;
            }
          }
          else
          {
            v24 = -366;
            if ( (__int16)j < 366 )
              goto LABEL_37;
          }
          v25 = j + v24;
          LOWORD(v5) = v21 + 1;
        }
      }
      v16 = 366 * v15;
      v17 = 366 * *(unsigned __int8 *)(v6 + 18) - 1;
      if ( v16 >= 0 )
      {
        for ( j = v17 + v8; ; j = v20 )
        {
          v21 = (unsigned __int16)v5;
          v22 = 25
              * ((((18351 * (unsigned int)(unsigned __int16)v5) >> 16)
                + ((unsigned __int16)(v5 - ((18351 * (unsigned int)(unsigned __int16)v5) >> 16)) >> 1)) >> 4);
          v23 = 15;
          if ( (_WORD)v21 != (_WORD)v22 )
            v23 = 3;
          if ( (v21 & v23) != 0 )
          {
            v19 = -365;
            if ( (__int16)j < 365 )
              goto LABEL_37;
          }
          else
          {
            v19 = -366;
            if ( (__int16)j < 366 )
              goto LABEL_37;
          }
          v20 = j + v19;
          LOWORD(v5) = v21 + 1;
        }
      }
      v29 = 0x8000;
      if ( (v17 & 0x8000u) != 0 )
        v29 = 366 * *(unsigned __int8 *)(v6 + 18) - 1;
      v30 = v29 + v8;
      v31 = v5 - 1;
      do
      {
        v21 = v31;
        v32 = 3;
        if ( 25
           * (unsigned __int16)((((18351 * (unsigned int)v31) >> 16)
                               + ((unsigned __int16)(v31 - ((18351 * (unsigned int)v31) >> 16)) >> 1)) >> 4) == v31 )
          v32 = 15;
        --v31;
        v30 += ((v21 & v32) == 0) + 365;
      }
      while ( v30 < 0 );
      v28 = v30 + 1;
LABEL_45:
      result = (v21 << 16) | v4 & 0xFE00u | v28;
      *a2 = result;
      *(_DWORD *)(v6 + 12) = result;
    }
    else
    {
      *a2 = v7;
    }
  }
  return result;
}
