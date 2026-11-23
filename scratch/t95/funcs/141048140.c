// THUNK ALIAS -> sub_143ECFC30 (jmp:0x141048140->0x143ecfc30)
_WORD *__fastcall sub_143ECFC30(__int64 a1, int a2, int a3, int a4)
{
  __int64 v4; // r10
  __int64 v5; // rax
  unsigned __int64 v6; // rax
  unsigned __int16 v7; // r11
  __int64 v8; // rsi
  _WORD *result; // rax
  __int64 i; // rdi
  int v11; // ebx
  int v12; // ebp
  unsigned __int16 v13; // bx
  int v14; // ebp
  unsigned __int16 v15; // bx
  int v16; // ebx
  int v17; // ebp
  unsigned __int16 v18; // bx

  v4 = *(_QWORD *)(a1 + 192);
  v5 = *(_QWORD *)(a1 + 200) - v4;
  if ( v5 != 0 )
  {
    v6 = v5 >> 4;
    v7 = dword_141AAE084 & 0x1FF;
    v8 = 1;
    if ( v6 >= 2 )
      v8 = v6;
    result = *(_WORD **)(a1 + 192);
    if ( (HIWORD(dword_141AAE084) ^ 0x76C | dword_141AAE084 & 0x1FF ^ 1) != 0 )
    {
      for ( i = 0; ; ++i )
      {
        if ( *(_QWORD *)result != 0 )
        {
          v11 = *(_DWORD *)(*(_QWORD *)result + 12LL);
          if ( v11 == a4 || v11 == a2 || v11 == a3 )
          {
            if ( (v12 = (unsigned __int16)result[5], v13 = result[4] & 0x1FF, v12 == 1900) && v13 == 1
              || HIWORD(dword_141AAE084) >= (unsigned __int16)v12
              && (HIWORD(dword_141AAE084) > (unsigned __int16)v12 || v7 >= v13) )
            {
              v14 = (unsigned __int16)result[7];
              v15 = result[6] & 0x1FF;
              if ( v14 == 1900 && v15 == 1 )
                return (_WORD *)(16 * i + v4);
              if ( HIWORD(dword_141AAE084) <= (unsigned __int16)v14
                && (HIWORD(dword_141AAE084) < (unsigned __int16)v14 || v7 <= v15) )
              {
                return result;
              }
            }
          }
        }
        result += 8;
        if ( --v8 == 0 )
          return nullptr;
      }
    }
    i = 0;
    do
    {
      if ( *(_QWORD *)result != 0 )
      {
        v16 = *(_DWORD *)(*(_QWORD *)result + 12LL);
        if ( v16 == a4 || v16 == a2 || v16 == a3 )
        {
          v17 = (unsigned __int16)result[7];
          v18 = result[6] & 0x1FF;
          if ( v17 == 1900 && v18 == 1 )
            return (_WORD *)(16 * i + v4);
          if ( HIWORD(dword_141AAE084) <= (unsigned __int16)v17
            && (HIWORD(dword_141AAE084) < (unsigned __int16)v17 || v7 <= v18) )
          {
            return result;
          }
        }
      }
      ++i;
      result += 8;
      --v8;
    }
    while ( v8 != 0 );
  }
  return nullptr;
}
