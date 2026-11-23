// THUNK ALIAS -> sub_144017000 (jmp:0x1411dcd00->0x144017000)
char __fastcall sub_144017000(__int64 a1, char a2, char a3)
{
  char result; // al
  __int64 v4; // rcx
  __int64 v5; // r10
  __int64 v6; // rcx
  unsigned __int64 v7; // rcx
  unsigned __int16 v8; // r9
  __int64 v9; // r11
  __int64 v10; // rcx
  __int64 v11; // rdi
  int v12; // r8d
  __int64 v13; // r8
  unsigned __int16 v14; // dx

  result = 2 * a2;
  v4 = *(_QWORD *)(a1 + 176);
  v5 = *(_QWORD *)(v4 + 120);
  v6 = *(_QWORD *)(v4 + 128) - v5;
  if ( v6 != 0 )
  {
    v7 = v6 >> 3;
    v8 = word_141AB0260;
    v9 = 1;
    if ( v7 >= 2 )
      v9 = v7;
    v10 = 0;
    if ( a3 == 0 )
    {
      while ( 1 )
      {
        v13 = *(_QWORD *)(v5 + 8 * v10);
        v14 = *(_WORD *)(v13 + 32);
        if ( v14 == 0 )
          break;
        if ( v8 >= 0x7E8u )
        {
          word_141AB0260 = 2023;
          v8 = 2023;
          if ( v14 >= 0x7E7u )
            break;
        }
        else if ( v14 >= v8 )
        {
          break;
        }
LABEL_20:
        if ( v9 == ++v10 )
          return result;
      }
      if ( *(_BYTE *)(v13 + 37) != 0 && (*(_BYTE *)(v13 + 35) & 0xE) != 4 && (char)(*(_BYTE *)(v13 + 34) + 1) > result )
        result = *(_BYTE *)(v13 + 34) + 1;
      goto LABEL_20;
    }
    do
    {
      v11 = *(_QWORD *)(v5 + 8 * v10);
      if ( *(int *)(v11 + 24) <= 0 )
      {
        v12 = *(_DWORD *)(v11 + 32);
        if ( (unsigned __int16)(v12 - 1900) >= 0xC9u && *(_BYTE *)(v11 + 36) == 0 && *(_BYTE *)(v11 + 37) != 0 )
        {
          if ( (_WORD)v12 == 0 )
            goto LABEL_16;
          if ( v8 >= 0x7E8u )
          {
            word_141AB0260 = 2023;
            v8 = 2023;
            if ( (unsigned __int16)v12 >= 0x7E7u )
            {
LABEL_16:
              if ( (*(_BYTE *)(v11 + 35) & 0xE) != 4 && (char)(*(_BYTE *)(v11 + 34) + 1) > result )
                result = *(_BYTE *)(v11 + 34) + 1;
            }
          }
          else if ( (unsigned __int16)v12 >= v8 )
          {
            goto LABEL_16;
          }
        }
      }
      ++v10;
    }
    while ( v9 != v10 );
  }
  return result;
}
